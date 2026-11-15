"""Keep only the hatch's own shell (the v1 seam cut also picked up cargo-floor faces that swung under the car when the
hatch hinged open). Per 20 mm height bin and 100 mm width column, keep faces within --depth mm of the rearmost face.
    hatchclean.py p_hatch.stl out_hatch.stl rest.stl --depth 90 --zmax 400   (rest = faces that go back to the car)"""
import argparse, struct
import numpy as np
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("hatch"); ap.add_argument("out"); ap.add_argument("rest"); ap.add_argument("--depth", type=float, default=90); ap.add_argument("--zmax", type=float, default=400, help="filter only below this height: above it the hatch carries the roof spoiler, whose underside is legitimately deep")
a = ap.parse_args()
h = np.fromfile(a.hatch, dtype=DT, offset=84); c = h["v"].mean(1)
key = (np.floor(c[:, 2] / 20).astype(int) * 1000) + np.floor(c[:, 0] / 100).astype(int)
order = np.argsort(key); ks = key[order]; ys = c[order, 1]
uniq, start = np.unique(ks, return_index=True); mx = np.maximum.reduceat(ys, start)
ymax = mx[np.searchsorted(uniq, key)]
keep = (c[:, 1] > ymax - a.depth) | (c[:, 2] >= a.zmax)
print("hatch", len(h), "-> shell", int(keep.sum()), "| back to the car", int((~keep).sum()))
for p, m in ((a.out, h[keep]), (a.rest, h[~keep])):
    with open(p, "wb") as f: f.write(b"grc hatchclean".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
