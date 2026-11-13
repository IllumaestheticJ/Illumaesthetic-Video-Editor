"""Add only the NEW geometry of a registered state scan to a base composite (binary STLs, same mm frame).
    python addnew.py base.stl state.stl out.stl --new 8 --avoid part1.stl part2.stl --avoid-mm 12 [--box ...]
Keeps state triangles whose centroid is > --new mm from the base and > --avoid-mm from every moving part
(so no ghost of a removable panel stays behind), then appends them to the base."""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("base"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--new", type=float, default=8); ap.add_argument("--avoid", nargs="*", default=[])
ap.add_argument("--avoid-mm", type=float, default=12); ap.add_argument("--box", type=float, nargs=6)
ap.add_argument("--only", help="also write the kept state triangles alone")
a = ap.parse_args()
ld = lambda p: np.fromfile(p, dtype=TRI, offset=84)
base, st = ld(a.base), ld(a.state)
c = st["v"].mean(1)
keep = np.ones(len(st), bool)
if a.box:
    b = np.array(a.box); keep &= np.all((c >= b[0::2]) & (c <= b[1::2]), axis=1)
bc = base["v"].mean(1)
near = bc[np.all((bc >= c.min(0) - 50) & (bc <= c.max(0) + 50), axis=1)]
keep &= cKDTree(near).query(c, distance_upper_bound=a.new)[0] > a.new
for p in a.avoid:
    keep &= cKDTree(ld(p)["v"].mean(1)).query(c, distance_upper_bound=a.avoid_mm)[0] > a.avoid_mm
print("state", len(st), "kept", int(keep.sum()))
def save(p, m):
    with open(p, "wb") as f:
        f.write(b"addnew".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
save(a.out, np.concatenate([base, st[keep]]))
if a.only:
    save(a.only, st[keep])
