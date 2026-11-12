"""In-place highlight: dim everything except the masked part(s) while a label is up.
    python projects/porsche-gt3rs-992/tools/highlight.py <beauty_dir> <matte_dir> <out_dir> --t0 0.15 --t1 1.8 [--dim 0.55] [--fps 15]
out = frame * (1 - dim(t) * (1 - soft_mask)); dim ramps in/out over 0.3 s around [t0, t1] (shot-local seconds)."""
import argparse, glob, os
import numpy as np
from PIL import Image, ImageFilter
ap = argparse.ArgumentParser(); ap.add_argument("beauty"); ap.add_argument("matte"); ap.add_argument("out")
ap.add_argument("--t0", type=float, required=True); ap.add_argument("--t1", type=float, required=True)
ap.add_argument("--dim", type=float, default=0.55); ap.add_argument("--fps", type=float, default=15); a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
fs = sorted(glob.glob(f"{a.beauty}/*.png")); ms = sorted(glob.glob(f"{a.matte}/*.png"))
assert len(fs) == len(ms), (len(fs), len(ms))
for i, (f, m) in enumerate(zip(fs, ms)):
    t = i / a.fps
    k = min(1.0, max(0.0, (t - a.t0) / 0.3)) * min(1.0, max(0.0, (a.t1 - t) / 0.3))
    im = Image.open(f).convert("RGB")
    if k > 0:
        mk = Image.open(m).convert("L").point(lambda v: 255 if v > 96 else 0)
        soft = np.maximum(np.asarray(mk, np.float32), np.asarray(mk.filter(ImageFilter.GaussianBlur(10)), np.float32) * 1.4).clip(0, 255) / 255
        g = 1 - a.dim * k * (1 - soft)
        im = Image.fromarray((np.asarray(im, np.float32) * g[..., None]).clip(0, 255).astype(np.uint8))
    im.save(os.path.join(a.out, os.path.basename(f)))
print(a.out, len(fs))
