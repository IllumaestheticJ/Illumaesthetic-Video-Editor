"""v0 assembly: 15 fps Blender renders -> 30 fps 1080x1920 frames with character composites, scan labels, sale card and
Epsilon+ wordmark; then mux the music (from its start), loudness to -14 LUFS / TP < -1 dBFS.

    python post.py            -> /home/user/media/work/out/bf-miata-mr2-night-meet_v0.mp4
"""
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

M = "/home/user/media/bf-miata-mr2-night-meet"
OUT = f"{M}/work/frames"; os.makedirs(OUT, exist_ok=True)
FINAL = "/home/user/media/work/out/bf-miata-mr2-night-meet_v0.1.mp4"   # v0.1: no Del & Eps (owner, e05c325)
TL = json.load(open(os.path.join(os.path.dirname(__file__), "..", "specs", "timeline.json")))
F30 = TL["f30"]
W, H = 1080, 1920
FD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FM = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf"
if not os.path.exists(FM):
    FM = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
OFF = (232, 236, 242)
LOGO = Image.open(f"{M}/logo/Epsilon+ Logo.png").convert("RGBA")


def font(p, s): return ImageFont.truetype(p, s)


def ease(t): t = min(max(t, 0), 1); return t * t * (3 - 2 * t)


def shot_frame(shot, i):
    d = f"{M}/work/{shot}"; fs = sorted(os.listdir(d)); fs = [f for f in fs if f.endswith(".png")]
    im = Image.open(os.path.join(d, fs[min(i // 2, len(fs) - 1)])).convert("RGB")
    return im.resize((W, H), Image.LANCZOS)


def put_char(base, img, h, cx, by, alpha=1.0, shadow=True):
    r = img.resize((int(img.width * h / img.height), h), Image.LANCZOS)
    if shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
        d.ellipse([cx - r.width * 0.42, by - h * 0.03, cx + r.width * 0.42, by + h * 0.03], fill=(0, 0, 0, int(150 * alpha)))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(h * 0.02)))
    if alpha < 1:
        a = r.getchannel("A").point(lambda v: int(v * alpha)); r.putalpha(a)
    base.alpha_composite(r, (int(cx - r.width / 2), int(by - h)))


def label(base, t, line1, line2, y=300):
    a = int(255 * ease(t * 4)); d = ImageDraw.Draw(base)
    d.text((90, y), line1, font=font(FD, 66), fill=(*OFF, a))
    d.text((92, y + 92), line2, font=font(FM, 34), fill=(*OFF, int(a * 0.8)))


def card(base_img, i, n):
    bg = base_img.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.32)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    a1 = int(255 * ease(i / 6)); a2 = int(255 * ease((i - 25) / 6))      # list lands on the next hit (+0.82 s)
    d.text((W / 2, 250), "BLACK FRIDAY", font=font(FM, 40), fill=(*OFF, a1), anchor="mm")
    d.text((W / 2, 380), "20% OFF", font=font(FD, 170), fill=(255, 255, 255, a1), anchor="mm")
    d.text((W / 2, 510), "MR2 SPYDER + NC MIATA AERO", font=font(FD, 50), fill=(*OFF, a1), anchor="mm")
    rows = [("MR2 SPYDER", None, None), ("Side Skirt / Fender Combo", "$700", "$560"), ("Rear Spats", "$350", "$280"),
            ("Headlight Eyelids", "$100", "$80"), ("Hood Vents", "$400", "$320"), ("Rear Duckbill", "$220", "$176"),
            ("NC MIATA", None, None), ("Front Bumper + Lip", "$1,100", "$880"), ("Fender Cuts", "$300", "$240"),
            ("Side Skirts", "$500", "$400"), ("Rear Spats (NC1)", "$250", "$200"), ("Canards", "$200", "$160")]
    y = 650; fr, fh, fp = font(FD, 40), font(FD, 44), font(FM, 38)
    for name, was, now in rows:
        if was is None:
            y += 18; d.text((110, y), name, font=fh, fill=(255, 255, 255, a2)); y += 74; continue
        d.text((130, y), name, font=fr, fill=(*OFF, a2))
        wb = d.textbbox((0, 0), was, font=fp); nb = d.textbbox((0, 0), now, font=fp)
        xn = W - 110 - (nb[2] - nb[0]); xw = xn - 30 - (wb[2] - wb[0])
        d.text((xw, y + 2), was, font=fp, fill=(150, 154, 160, a2))
        d.line([(xw - 4, y + 24), (xw + wb[2] - wb[0] + 4, y + 24)], fill=(150, 154, 160, a2), width=3)
        d.text((xn, y + 2), now, font=fp, fill=(255, 255, 255, a2))
        y += 66
    return bg


def logo(i, n):
    bg = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    a = ease(i / 4) * (1 - ease((i - (n - 14)) / 14))
    lw = 720; lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
    bg.alpha_composite(lg, ((W - lw) // 2, H // 2 - lg.height // 2 - 40))
    ImageDraw.Draw(bg).text((W / 2, H / 2 + 90), "epsilon.plus", font=font(FM, 44), fill=(*OFF, int(255 * a)), anchor="mm")
    return bg


def main():
    shots = ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "s11", "s12"]
    k = 0; last10 = None
    for si, s in enumerate(shots):
        n = F30[si + 1] - F30[si] - (1 if si == 0 else 0) + (1 if si == 0 else 0)
        for i in range(n):
            if s == "s11":
                fr = card(last10, i, n)
            elif s == "s12":
                fr = logo(i, n)
            else:
                fr = shot_frame(s, i).convert("RGBA"); t = i / n
                if s == "s02":
                    if i > n * 0.62: label(fr, (i - n * 0.62) / n, "SIDE SKIRT / FENDER", "MR2 SPYDER · FIBERGLASS")
                if s == "s07" and i > n * 0.62: label(fr, (i - n * 0.62) / n, "FRONT BUMPER", "NC MIATA · FIBERGLASS")
                if s == "s08":
                    if i > n * 0.62: label(fr, (i - n * 0.62) / n, "FENDER CUTS", "NC MIATA · FIBERGLASS", y=1380)
                if s == "s10":   # both kitted scans (owner: no characters, typical branding)
                    if i > 8: label(fr, (i - 8) / n, "MR2 SPYDER + NC MIATA", "EPSILON+ · FIBERGLASS AERO")
                    last10 = fr.convert("RGB")
            fr.convert("RGB").save(f"{OUT}/{k:05d}.jpg", quality=92); k += 1
    print("frames", k)
    dur = k / 30
    vid = f"{M}/work/v01_silent.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{OUT}/%05d.jpg", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", vid], check=True)
    seg = f"{M}/work/music_seg.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{M}/music/tokyo_midnight.wav", "-t", f"{dur:.3f}",
                    "-af", f"afade=t=out:st={dur - 1.4:.3f}:d=1.4", "-ar", "48000", seg], check=True)
    r = subprocess.run(["ffmpeg", "-nostats", "-i", seg, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float(r.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0]); TP = float(r.split("True peak:")[1].split("Peak:")[1].split("dBFS")[0])
    g = min(-14 - I, -1.2 - TP)            # static gain: -14 LUFS unless the true-peak ceiling wins (lesson: 'Going Up North')
    print("music I", I, "TP", TP, "gain", round(g, 2))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", seg, "-af", f"volume={g:.2f}dB,alimiter=limit=0.70:level=false:attack=1:release=50", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "256k", "-shortest", FINAL], check=True)
    print("OUT", FINAL)


if __name__ == "__main__":
    main()
