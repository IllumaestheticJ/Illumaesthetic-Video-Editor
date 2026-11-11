"""Fade a rendered PNG sequence to the render black over its last N seconds of PLAY time (frames past the play length
are black too, so minterpolate's tail can't flash the car back).
    fade_frames.py src_dir out_dir --play 2.4 --fade 1.2 [--fps 15] [--bg 7,7,9]
bg = the scan renders' black (0.004 linear, AgX), which is also the logo card's background."""
import argparse, os
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--play", type=float, required=True); ap.add_argument("--fade", type=float, required=True)
ap.add_argument("--fps", type=float, default=15); ap.add_argument("--bg", default="7,7,9")
a = ap.parse_args()
bg = np.array([float(v) for v in a.bg.split(",")])
os.makedirs(a.out, exist_ok=True)
fs = sorted(f for f in os.listdir(a.src) if f.endswith(".png"))
for i, f in enumerate(fs):
    t = i / a.fps                       # time of this frame from the clip start
    u = np.clip((a.play - t) / a.fade, 0, 1)   # 1 before the fade, 0 at/after the end of play
    k = u * u * (3 - 2 * u)
    im = np.asarray(Image.open(os.path.join(a.src, f)).convert("RGB")).astype(float)
    Image.fromarray(np.clip(bg + (im - bg) * k, 0, 255).astype(np.uint8)).save(os.path.join(a.out, f))
print(len(fs), "frames ->", a.out)
