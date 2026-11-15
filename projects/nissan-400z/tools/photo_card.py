"""Photo card for the 1:1 match cut: the still the HERO render ends on, at exactly the solved framing on its first frame,
then a slow push-in about the car and a dip to black into the end card. No text over the photo (CLAUDE.md).
  python photo_card.py photo.jpg out.mp4 [--frames 84] [--push 0.05] [--anchor 600,1170] [--fade 12]"""
import argparse, subprocess
from PIL import Image

ap = argparse.ArgumentParser(); ap.add_argument("photo"); ap.add_argument("out")
ap.add_argument("--frames", type=int, default=84); ap.add_argument("--push", type=float, default=0.05)
ap.add_argument("--anchor", default="600,1170"); ap.add_argument("--fade", type=int, default=12)
a = ap.parse_args()
im = Image.open(a.photo).convert("RGB"); W, H = im.size; ax, ay = (float(v) for v in a.anchor.split(","))
assert abs(W / H - 1080 / 1920) < 1e-3, "photo must be 9:16 so frame 1 is the solved framing"
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30",
                      "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
for i in range(a.frames):
    t = i / max(1, a.frames - 1); s = 1 + a.push * (t * t * (3 - 2 * t)) if i else 1.0
    x0, y0 = ax * (1 - 1 / s), ay * (1 - 1 / s)
    f = im.resize((1080, 1920), Image.LANCZOS, box=(x0, y0, x0 + W / s, y0 + H / s))
    k = a.frames - 1 - i
    if k < a.fade:
        f = Image.eval(f, lambda v, g=k / a.fade: int(v * g))
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
