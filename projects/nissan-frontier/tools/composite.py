"""Exploded/open-front base for the Frontier (levelled mm). Logic of ferrari-296/tools/composite.py, but each fill (state
scan) is limited to explicit zones so a state's small offsets elsewhere (doors, bed) never add double skins.
  1. car minus triangles within --cut mm of any removed part (the panel's skin on the car)
  2. per fill: state triangles > --new mm from the trimmed car... and > --new mm from the original car, inside its zones
  composite.py out.stl --remove a.stl b.stl --fill state.stl:zone[;zone] ...
  zone = x0,x1,y0,y1,z0,z1 (mm); 'outer' prefix -> |x| >= x0 on both sides"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--car", default="/home/user/media/nissan-frontier/lev/full_4mm.stl")
ap.add_argument("--remove", nargs="+", required=True); ap.add_argument("--fill", nargs="*", default=[])
ap.add_argument("--cut", type=float, default=9.0); ap.add_argument("--new", type=float, default=7.0)
a = ap.parse_args()
car = load(a.car); cc = car["v"].mean(1); keep = np.ones(len(car), bool)
for r in a.remove:
    v = load(r)["v"].mean(1)
    d, _ = cKDTree(v).query(cc, distance_upper_bound=a.cut + 1); keep &= ~(d < a.cut)
print("car", len(car), "-> trimmed", int((~keep).sum()))
pieces = [car[keep]]; tc = cKDTree(cc[::2])
for spec in a.fill:
    path, zs = spec.split(":"); m = load(path); c = m["v"].mean(1); inz = np.zeros(len(c), bool)
    for z in zs.split(";"):
        outer = z.startswith("outer"); z = z.replace("outer", "")
        x0, x1, y0, y1, z0, z1 = map(float, z.split(","))
        xx = np.abs(c[:, 0]) if outer else c[:, 0]
        inz |= (xx >= x0) & (xx <= x1) & (c[:, 1] >= y0) & (c[:, 1] <= y1) & (c[:, 2] >= z0) & (c[:, 2] <= z1)
    d, _ = tc.query(c[inz], distance_upper_bound=a.new * 2)
    sel = np.zeros(len(m), bool); sel[np.where(inz)[0][d > a.new]] = True
    print(path, "fill +", int(sel.sum())); pieces.append(m[sel])
res = np.concatenate(pieces)
with open(a.out, "wb") as f:
    f.write(b"ive frontier composite".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
print(a.out, len(res))
