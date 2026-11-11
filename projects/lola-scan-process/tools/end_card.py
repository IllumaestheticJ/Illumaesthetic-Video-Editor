"""ILLUMAESTHETIC end card (no listing for this car): logo fades in, then ILLUMAESTHETIC.COM under it fades in last.
1080x1920 @30 on pure black, slow 3 % push, optional fade to black at the end (track tail).
usage: end_card.py logo.png out.mp4 duration [fade_out_s] [--no-url]   (v3: user asked to remove ILLUMAESTHETIC.COM)"""
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont

NO_URL = "--no-url" in sys.argv; sys.argv = [a for a in sys.argv if a != "--no-url"]
logo_p, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
fade_out = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
W, H, FPS = 1080, 1920, 30
logo = Image.open(logo_p).convert("RGBA")
lw = 842; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
font = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", 54)
txt = "ILLUMAESTHETIC.COM"
# tracked text (+6 tracking like the HUD titles)
tw = sum(font.getlength(c) for c in txt) + 6 * (len(txt) - 1)
tl = Image.new("RGBA", (int(tw) + 4, 80), (0, 0, 0, 0)); d = ImageDraw.Draw(tl); x = 0
for c in txt:
    d.text((x, 0), c, font=font, fill=(232, 236, 242, 255)); x += font.getlength(c) + 6

def ease(t): return t * t * (3 - 2 * t)
def ramp(t, a, b): return ease(min(1.0, max(0.0, (t - a) / (b - a))))

n = int(round(dur * FPS))
p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
for i in range(n):
    t = i / FPS
    s = 1.0 + 0.03 * t / dur
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    a_logo = ramp(t, 0.0, 0.45); a_txt = ramp(t, 0.75, 1.25)
    L = logo.resize((round(logo.width * s), round(logo.height * s)), Image.LANCZOS)
    L.putalpha(L.getchannel("A").point(lambda v: int(v * a_logo)))
    cy = H // 2 - (0 if NO_URL else 60)
    fr.alpha_composite(L, (W // 2 - L.width // 2, cy - L.height // 2))
    if NO_URL: a_txt = 0.0
    T = tl.copy(); T.putalpha(T.getchannel("A").point(lambda v: int(v * a_txt)))
    fr.alpha_composite(T, (W // 2 - T.width // 2, cy + L.height // 2 + 70))
    arr = np.asarray(fr.convert("RGB")).astype(np.float32)
    if fade_out and t > dur - fade_out:
        arr *= max(0.0, (dur - t) / fade_out)
    p.stdin.write(arr.astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
print(out)
