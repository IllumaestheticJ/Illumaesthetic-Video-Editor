"""Grade the end of a silver-on-black render sequence toward a grey product render (listing photo look).
Linear per-pixel map  out = bg_to + (in - bg_from) * (car_to - bg_to) / (car_from - bg_from), blended in over
[t0, t1] (fractions of the sequence, smoothstep). Values measured with median luma (render vs listing photo).
Also lifts the frame outside the WebZoom box (y outside [box_top, box_bot]) to the page colour at full ramp.
usage: greygrade.py in_dir out_dir --bg-from 7 --car-from 218 --bg-to 57 --car-to 140 --t0 0.55 --t1 1.0"""
import argparse, glob, os
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--bg-from", type=float, default=7); ap.add_argument("--car-from", type=float, default=218)
ap.add_argument("--bg-to", type=float, default=57); ap.add_argument("--car-to", type=float, default=140)
ap.add_argument("--t0", type=float, default=0.55); ap.add_argument("--t1", type=float, default=1.0)
ap.add_argument("--box", default="", help="top,bottom px (output res) of the listing image box; outside -> --page")
ap.add_argument("--page", type=float, default=11)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
fs = sorted(glob.glob(os.path.join(a.inp, "*.png")))
n = len(fs)
for i, f in enumerate(fs):
    t = i / max(1, n - 1)
    k = min(1.0, max(0.0, (t - a.t0) / max(1e-6, a.t1 - a.t0)))
    k = k * k * (3 - 2 * k)
    im = np.asarray(Image.open(f).convert("RGB"), np.float32)
    g = a.bg_to + (im - a.bg_from) * (a.car_to - a.bg_to) / (a.car_from - a.bg_from)
    if a.box:
        top, bot = [int(float(v) * im.shape[0] / 1920) for v in a.box.split(",")]
        g[:top] = a.page; g[bot:] = a.page
    o = im * (1 - k) + g * k
    Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).save(os.path.join(a.out, os.path.basename(f)))
print("graded", n, "frames")
