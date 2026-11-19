"""ibf-scan-teardown draft builder: real CAD/scan screen recordings -> 9:16 reel, cuts on the music grid.

Usage: python projects/ibf-scan-teardown/tools/build.py [version]
Media in /home/user/media/ibf-scan-teardown (screens/ = Dropbox /Footage Library/Videos/CAD & Scan Screens).
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

VER = sys.argv[1] if len(sys.argv) > 1 else "v0.1"
M = "/home/user/media/ibf-scan-teardown"
SC = f"{M}/screens"
W, H, FPS = 1080, 1920, 30
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
AKIRA = f"{REPO}/assets/fonts/akira/AkiraExpanded-SuperBold.otf"
UNB = lambda w: f"{REPO}/assets/fonts/unbounded/Unbounded-{w}.ttf"

# music: "Machine Protocol" - Wbsound (TikTok CML 7671666742675539969). Grid fitted on onset strength:
# beat 0.4615 s (130 BPM), drop at track 15.250. Video t0 = track 14.327 (2 beats before the drop).
T0, BEAT, DROP_V = 14.327, 0.4615, 0.923
def fr(t): return round(t * FPS)
cuts_t = [0.0, DROP_V + 6 * BEAT, DROP_V + 10 * BEAT, DROP_V + 16 * BEAT, DROP_V + 22 * BEAT, DROP_V + 32 * BEAT]
cuts = [fr(t) for t in cuts_t]

BG = "0x0a0a0a"
# id, src, src_in, src_out, crop (w:h:x:y), panel centre y
SHOTS = [
    ("s1_spin", "2026-07-21_09.42.03.mp4", 5.2, 11.0, "2040:1250:260:60", 920),
    ("s2_teardown", "2026-07-13_07.40.52.mp4", 0.6, 4.29, "1500:1250:420:60", 950),
    ("s3_mounts", "2025-07-01_02.53.17.mp4", 3.0, 8.54, "1038:1038:190:0", 960),
    ("s4_design", "2025-07-17_23.04.26.mp4", 2.8, 8.34, "1150:1150:0:0", 960),
]
WORK = f"{M}/work/{VER}"; os.makedirs(WORK, exist_ok=True)

def shot(i, s):
    sid, src, a, b, crop, cy = s
    n = cuts[i + 1] - cuts[i]
    speed = (b - a) / (n / FPS)
    cw, ch = map(int, crop.split(":")[:2]); ph = round(ch * W / cw / 2) * 2
    y = cy - ph // 2
    vf = (f"setpts=(PTS-STARTPTS)/{speed:.5f},fps={FPS},crop={crop},scale={W}:{ph}:flags=lanczos,"
          f"pad={W}:{H}:0:{y}:color={BG},format=yuv420p")
    out = f"{WORK}/{sid}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a + 0.5), "-i", f"{SC}/{src}",
                    "-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", out], check=True)
    return out, (y, y + ph)

def endcard(n):
    out = f"{WORK}/s5_end.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={BG}:s={W}x{H}:r={FPS}",
                    "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", out], check=True)
    return out

def text_png(path, lines):
    """lines: (text, font, size, fill, centre_y). Returns list of text boxes."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); boxes = []
    for t, f, sz, fill, y in lines:
        ft = ImageFont.truetype(f, sz)
        x0, y0, x1, y1 = d.textbbox((0, 0), t, font=ft)
        x = (W - (x1 - x0)) // 2 - x0; yy = y - (y1 - y0) // 2 - y0
        d.text((x, yy), t, font=ft, fill=fill)
        boxes.append([x + x0, yy + y0, x + x1, yy + y1])
    return im, boxes

RED = (226, 35, 26, 255); WHITE = (255, 255, 255, 255)
def build():
    parts = []; spans = []
    for i, s in enumerate(SHOTS):
        p, span = shot(i, s); parts.append(p); spans.append(span)
    parts.append(endcard(cuts[5] - cuts[4]))
    lst = f"{WORK}/list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    base = f"{WORK}/base.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base], check=True)

    ov = []  # (png, t0, t1, key, boxes)
    # title over s1: offer within the first 2 s (pops at 0.1 s), readable until the cut at 3.69 s
    top = spans[0][0]
    im, bx = text_png(f"{WORK}/t_title.png", [("5% OFF", AKIRA, 150, RED, top - 175), ("EVERY SCAN", AKIRA, 74, WHITE, top - 55)])
    im.save(f"{WORK}/t_title.png"); ov.append(("t_title.png", 0.1, cuts_t[1], True, bx))
    for k, (lab, sz) in ((2, ("BUMPER MOUNTS", 54)), (3, ("DESIGNED ON THE SCAN", 50))):
        top = spans[k][0]
        im, bx = text_png("", [(lab, UNB(600), sz, WHITE, top - 70)])
        im.save(f"{WORK}/t_lab{k}.png"); ov.append((f"t_lab{k}.png", cuts_t[k] + 0.05, cuts_t[k + 1], False, bx))
    # end card: logo + offer (Akira) + URL / deadline (Unbounded, next to the logo)
    lg = Image.open(f"{M}/assets/logo_src.png").convert("RGBA"); lw = 720
    lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
    im, bx = text_png("", [("5% OFF", AKIRA, 170, RED, 560), ("EVERY SCAN", AKIRA, 84, WHITE, 720),
                           ("WWW.ILLUMAESTHETIC.COM", UNB(400), 40, WHITE, 1180), ("SALE ENDS NOV 30", UNB(300), 36, (200, 200, 200, 255), 1250)])
    ly = 1000 - lg.height // 2; im.alpha_composite(lg, ((W - lw) // 2, ly)); bx.append([(W - lw) // 2, ly, (W + lw) // 2, ly + lg.height])
    im.save(f"{WORK}/t_end.png"); ov.append(("t_end.png", cuts_t[4] + 0.03, cuts_t[5], True, bx))

    # overlay chain with a short fade-in per text (0.12 s) -> readable time = t1 - t0 - 0.12
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", base]
    fc = []; last = "0:v"
    for j, (png, t0, t1, key, b) in enumerate(ov):
        cmd += ["-loop", "1", "-t", f"{cuts_t[5]:.3f}", "-i", f"{WORK}/{png}"]
        fc.append(f"[{j+1}:v]format=rgba,fade=in:st={t0}:d=0.12:alpha=1[o{j}]")
        fc.append(f"[{last}][o{j}]overlay=0:0:enable='between(t,{t0},{t1 - 0.001:.3f})'[v{j}]"); last = f"v{j}"
    music = f"{M}/music/machine.m4a"; dur = cuts[5] / FPS
    cmd += ["-ss", f"{T0}", "-t", f"{dur:.3f}", "-i", music]
    ai = len(ov) + 1
    fc.append(f"[{ai}:a]afade=t=out:st={dur - 0.6:.3f}:d=0.6,volume=VOL,alimiter=limit=0.85:level=disabled[a]")
    out = f"{M}/out/ibf-scan-teardown_{VER}.mp4"; os.makedirs(os.path.dirname(out), exist_ok=True)
    vol = float(os.environ.get("VOL", "1.0"))
    fcs = ";".join(fc).replace("VOL", f"{vol}")
    cmd += ["-filter_complex", fcs, "-map", f"[{last}]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-r", str(FPS), "-frames:v", str(cuts[5]), out]
    subprocess.run(cmd, check=True)
    json.dump([{"file": p, "t0": t0, "t1": t1, "key": k, "boxes": b, "readable": round(t1 - t0 - 0.12, 2)} for p, t0, t1, k, b in ov],
              open(f"{WORK}/overlay_boxes.json", "w"), indent=1)
    json.dump({"cuts_frames": cuts, "cuts_t": cuts_t, "T0": T0, "beat": BEAT}, open(f"{WORK}/timing.json", "w"))
    print(out, cuts)

build()
