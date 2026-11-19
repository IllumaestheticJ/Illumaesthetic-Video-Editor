"""ibf-clearance-shelf v0: a continuous left->right "shelf" pan across four bays, price tag per bay.

No real shelf pan exists yet, so each bay is a real clip (or a FOOTAGE NEEDED placeholder) laid side by
side on a strip and the camera pans across it without stopping (slows near each item, never holds).
When the owner films the real shelf pan, it replaces the strip and the tag timing stays.

Usage: python build_v0.py [--version v0]
"""
import json, math, subprocess, sys, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = Path(__file__).resolve().parents[3]
MEDIA = Path("/home/user/media/ibf-clearance-shelf")
WORK = MEDIA / "work"; WORK.mkdir(parents=True, exist_ok=True)
AKIRA = str(REPO / "assets/fonts/akira/AkiraExpanded-SuperBold.otf")
UNB = lambda w: str(REPO / f"assets/fonts/unbounded/Unbounded-{w}.ttf")
LOGO = MEDIA / "illum_logo.png"
W, H, FPS = 1080, 1920, 30
BAR = 4 * 60 / 92.3            # 2.600 s, "Free Smoke" 92.3 BPM
MUSIC = MEDIA / "music/freesmoke.mp3"; MUSIC_T0 = 27.71   # the drop lands on video t=0
TONEMAP = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")

# Prices: projects/_illum-bf26/PRICES.md (owner's planned sale prices). Never type any other number.
BAYS = [
    dict(name="VB WRX FRONT LIP", price="$79.99", src=MEDIA / "raw/vblip.mov", ss=15.0,
         # crop under the burned-in captions of the 2023 reel (captions sit at y 300-400)
         vf="crop=760:1350:160:450,scale=1080:1918,pad=1080:1920:0:1"),
    dict(name="SUPRA LENSES", sub="TINTED CLEAR", price="$72", src=MEDIA / "raw/supra_0707_1635.mov", ss=13.4,
         vf=TONEMAP + ",scale=1188:2112,crop=1080:1920:100:150", hlg=True),
    dict(name="S13 BEZEL", sub="B-GRADE", price="$62.72", src=None),
    dict(name="S13 GTR GRILLE", price="$105", src=None),
]
N = len(BAYS)
T_PAN_END = N * BAR            # 10.4 s; end card after
T_END = T_PAN_END + 2 * BAR    # 15.6 s


def cam_u(t):
    """Camera position in bay units (0 = bay 0 centred). Never stops: speed 15 %..185 % of mean."""
    u = (t - 0.9) / BAR                     # bay k centred 0.9 s after its tag pops
    return u - 0.85 * math.sin(2 * math.pi * u) / (2 * math.pi)


def prep_bays():
    for i, b in enumerate(BAYS):
        out = WORK / f"bay{i}.mp4"; b["mp4"] = out
        if b["src"] is None or out.exists():
            continue
        dur = 2 * BAR + 1.5
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(b["ss"]), "-t", str(dur), "-i", str(b["src"]),
                        "-vf", b["vf"] + f",fps={FPS},tpad=stop_mode=clone:stop_duration=6", "-an",
                        "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out)], check=True)


class Reader:
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        self.idx = -1; self.frame = None

    def get(self, i):
        while self.idx < i:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            self.frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3); self.idx += 1
        return self.frame


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(text, path, size, maxw):
    while size > 10:
        f = font(path, size)
        if f.getbbox(text)[2] <= maxw:
            return f
        size -= 2
    return font(path, size)


def placeholder(b):
    im = Image.new("RGB", (W, H), (18, 18, 20)); d = ImageDraw.Draw(im)
    d.rectangle([120, 760, 960, 1360], outline=(90, 90, 90), width=4)
    f = font(UNB(500), 34)
    for k, line in enumerate(["FOOTAGE NEEDED", b["name"] + (" " + b["sub"] if b.get("sub") else "")]):
        tw = f.getbbox(line)[2]; d.text((540 - tw // 2, 1010 + 60 * k), line, font=f, fill=(150, 150, 150))
    return np.asarray(im)


def tag_image(b):
    """Hanging price tag (RGBA), drawn once. Width 760."""
    tw, th = 760, 430
    im = Image.new("RGBA", (tw, th + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line([(tw // 2, 0), (tw // 2, 60)], fill=(235, 235, 235, 255), width=5)        # string
    d.rounded_rectangle([0, 60, tw - 1, 60 + th], 28, fill=(250, 250, 248, 255))
    d.ellipse([tw // 2 - 16, 82, tw // 2 + 16, 114], fill=(0, 0, 0, 0))               # hole
    d.rectangle([0, 130, tw - 1, 200], fill=(10, 10, 10, 255))
    f = font(AKIRA, 40); s = "BLACK FRIDAY"; w = f.getbbox(s)[2]; d.text((tw // 2 - w // 2, 143), s, font=f, fill=(255, 255, 255))
    f = fit(b["name"], UNB(700), 50, tw - 80); w = f.getbbox(b["name"])[2]
    d.text((tw // 2 - w // 2, 222), b["name"], font=f, fill=(15, 15, 15))
    y = 290
    if b.get("sub"):
        f = font(UNB(500), 30); w = f.getbbox(b["sub"])[2]; d.text((tw // 2 - w // 2, 288), b["sub"], font=f, fill=(90, 90, 90)); y = 330
    f = fit(b["price"], AKIRA, 120, tw - 80); bb = f.getbbox(b["price"])
    d.text((tw // 2 - bb[2] // 2, y + (60 + th - 25 - y - bb[3]) // 2), b["price"], font=f, fill=(200, 16, 30))
    return im


def endcard():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im); boxes = []
    def ctext(y, s, f, fill, key=False):
        bb = f.getbbox(s); x = 484 - bb[2] // 2; d.text((x, y), s, font=f, fill=fill)
        boxes.append(dict(x=x, y=y + bb[1], w=bb[2], h=bb[3] - bb[1], label=s, key=key))
    ctext(330, "BLACK FRIDAY", font(AKIRA, 72), (255, 255, 255), True)
    ctext(425, "CLEARANCE", font(AKIRA, 72), (200, 16, 30), True)
    y = 580
    for b in BAYS:
        nm = b["name"] + (" B-GRADE" if b.get("sub") == "B-GRADE" else "")
        fn = fit(nm, UNB(600), 40, 500); fp = font(AKIRA, 64)
        d.text((70, y + 14), nm, font=fn, fill=(220, 220, 220))
        pb = fp.getbbox(b["price"]); d.text((900 - pb[2], y), b["price"], font=fp, fill=(255, 255, 255))
        boxes.append(dict(x=70, y=y, w=830, h=80, label=nm + " " + b["price"], key=True)); y += 115
    ctext(y + 20, "ENDS NOV 30", font(AKIRA, 44), (200, 16, 30), True)
    logo = Image.open(LOGO).convert("RGBA"); lw = 600
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    ly = 1170; im.alpha_composite(logo, (484 - lw // 2, ly))
    boxes.append(dict(x=484 - lw // 2, y=ly, w=lw, h=logo.height, label="logo"))
    ctext(ly + logo.height + 40, "WWW.ILLUMAESTHETIC.COM", font(UNB(400), 34), (255, 255, 255), True)
    return im, boxes


def ease_out_back(x):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--version", default="v0"); a = ap.parse_args()
    prep_bays()
    readers = [Reader(b["mp4"]) if b["src"] else None for b in BAYS]
    holds = [None if b["src"] else placeholder(b) for b in BAYS]
    lead = None
    tags = [tag_image(b) for b in BAYS]
    end, end_boxes = endcard()
    TAG_X, TAG_Y = 484 - 380, 300          # tag top (string) at y 300, card y 360-790
    boxes = []
    out_v = WORK / f"video_{a.version}.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                            "-pix_fmt", "yuv420p", str(out_v)], stdin=subprocess.PIPE)
    nf = round(T_END * FPS)
    for n in range(nf):
        t = n / FPS
        if t < T_PAN_END:
            u = cam_u(t); left = u * W          # strip x of the frame's left edge (bay i at i*W)
            frame = np.zeros((H, W, 3), np.uint8)
            for i in range(-1, N):
                x0 = int(round(i * W - left))
                if x0 >= W or x0 + W <= 0:
                    continue
                if i == -1:                              # shelf edge before bay 0: dark blur of bay 0
                    if lead is None:
                        src = readers[0].get(0)
                        lead = np.asarray(Image.fromarray(src).filter(ImageFilter.GaussianBlur(40))) // 4
                    img = lead
                elif readers[i] is not None:
                    vis0 = max(0.0, 0.9 + (i - 1) * BAR)   # time this bay first enters the frame
                    img = readers[i].get(max(0, int((t - vis0) * FPS)))
                else:
                    img = holds[i]
                a0, a1 = max(0, x0), min(W, x0 + W)
                frame[:, a0:a1] = img[:, a0 - x0:a1 - x0]
            im = Image.fromarray(frame).convert("RGBA")
            k = min(N - 1, int(t // BAR)); tt = t - k * BAR       # tag k on [k*BAR, (k+1)*BAR)
            sc = ease_out_back(min(1, tt / 0.18)) if tt < 0.18 else 1.0
            al = 1.0 if tt < BAR - 0.12 else max(0, (BAR - tt) / 0.12)
            tg = tags[k]
            if sc != 1.0 or al != 1.0:
                tw, th = tg.size; s = max(0.05, sc)
                tg = tg.resize((max(1, int(tw * s)), max(1, int(th * s))), Image.BILINEAR)
                if al < 1:
                    tg.putalpha(tg.getchannel("A").point(lambda v: int(v * al)))
                im.alpha_composite(tg, (484 - tg.size[0] // 2, TAG_Y))
            else:
                im.alpha_composite(tg, (TAG_X, TAG_Y))
            frame = np.asarray(im.convert("RGB"))
        else:
            te = t - T_PAN_END
            im = end.copy()
            if te < 0.25:                                  # quick fade up from the last pan frame's black
                im = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), im, te / 0.25)
            frame = np.asarray(im.convert("RGB"))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close(); enc.wait()
    for k, b in enumerate(BAYS):
        boxes.append(dict(t0=k * BAR + 0.18, t1=(k + 1) * BAR - 0.12, x=TAG_X, y=TAG_Y + 60, w=760, h=430,
                          label=f"tag {b['name']} {b['price']}", key=True))
    for bx in end_boxes:
        boxes.append(dict(t0=T_PAN_END + 0.25, t1=T_END, **bx))
    (WORK / f"boxes_{a.version}.json").write_text(json.dumps(boxes, indent=1))
    # audio: track from the drop, fade out the last 0.8 s, two-pass loudnorm to -14 LUFS / TP -1.5
    raw_a = WORK / "music_cut.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(MUSIC_T0), "-t", str(T_END), "-i", str(MUSIC),
                    "-af", f"afade=t=out:st={T_END - 0.8}:d=0.8", "-ar", "48000", "-ac", "2", str(raw_a)], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw_a), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    out = Path(f"/home/user/media/work/out/ibf-clearance-shelf_{a.version}.mp4"); out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out_v), "-i", str(raw_a), "-af", ln + ",aresample=48000",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
