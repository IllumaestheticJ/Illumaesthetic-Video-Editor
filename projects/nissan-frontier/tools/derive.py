"""Derive a removable part from the full truck and a "... removed" state scan (levelled mm STLs, one Artec frame).
Part = full-car triangles farther than --gap mm from the state scan (the panel is missing there), restricted to the
state's bbox (+/- --pad) and optional --box limits, minus triangles already claimed by --exclude STLs.
Also writes the trimmed car (car minus part) with --rest.
  derive.py car.stl state.stl part.stl [--gap 12] [--box ymax=-1500 zmin=300] [--exclude other_part.stl] [--rest rest.stl]"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def save(p, m):
    with open(p, "wb") as f:
        f.write(b"ive frontier derive".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--gap", type=float, default=12); ap.add_argument("--pad", type=float, default=0)
ap.add_argument("--box", nargs="*", default=[]); ap.add_argument("--exclude", nargs="*", default=[])
ap.add_argument("--rest")
ap.add_argument("--near", type=float, default=0, help="also require the state to have geometry within this many mm (flares: the body under them was scanned)")
a = ap.parse_args()
car = load(a.car); cc = car["v"].mean(1)
st = load(a.state)["v"].reshape(-1, 3)
lo, hi = st.min(0) - a.pad, st.max(0) + a.pad
for b in a.box:
    k, v = b.split("="); i = "xyz".index(k[0]); (lo if k.endswith("min") else hi)[i] = float(v)
inz = np.all((cc >= lo) & (cc <= hi), axis=1)
d, _ = cKDTree(st[::2]).query(cc[inz], distance_upper_bound=max(a.gap * 2, a.near + 1))
ok = d > a.gap
if a.near: ok &= d < a.near
sel = np.zeros(len(car), bool); sel[np.where(inz)[0][ok]] = True
for e in a.exclude:
    ev = load(e)["v"].mean(1)
    de, _ = cKDTree(ev).query(cc[sel], distance_upper_bound=4)
    idx = np.where(sel)[0]; sel[idx[de < 3]] = False
save(a.out, car[sel]); print(a.out, int(sel.sum()), "zone", lo.round(), hi.round())
if a.rest: save(a.rest, car[~sel]); print(a.rest, int((~sel).sum()))
