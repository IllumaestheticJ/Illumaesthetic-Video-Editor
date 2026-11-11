"""Trim the hood cut (car minus 'Hood Up' state) to the hood skin: y in [y0, y1] (levelled mm) and within
--below mm under the per-100 mm median hood height (drops cowl/windscreen and engine-bay bits seen through gaps).
    python projects/mazda-rx7-fc/tools/hoodtrim.py hood_v1.stl hood_v2.stl --y0 600 --y1 2000 --below 50"""
import argparse, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--y0", type=float, default=600); ap.add_argument("--y1", type=float, default=2000); ap.add_argument("--below", type=float, default=50)
a = ap.parse_args()
m = np.fromfile(a.src, dtype=TRI, offset=84); c = m["v"].mean(1)
keep = (c[:, 1] > a.y0) & (c[:, 1] < a.y1)
bins = np.arange(a.y0, a.y1 + 100, 100); med = []
for y in bins[:-1]:
    s = c[(c[:, 1] >= y) & (c[:, 1] < y + 100)]
    med.append(np.median(s[:, 2]) if len(s) else np.nan)
zc = np.interp(c[:, 1], bins[:-1] + 50, np.array(med))
keep &= c[:, 2] > zc - a.below
with open(a.out, "wb") as f:
    f.write(b"rx7 hood".ljust(80)); f.write(struct.pack("<I", int(keep.sum()))); m[keep].tofile(f)
print(a.out, int(keep.sum()), "of", len(m))
