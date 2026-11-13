"""Cut a panel from the levelled car STL with a polygon traced on the high-pass height map (chk/hood_hp.png, 3 mm/px,
image up = +Y). Shut lines show there as dark grooves (v4 hood cut was traced on a shaded render and missed them).
  extract_hp.py car.stl out.stl hp.json "x,y x,y ..." --zmin-lvl 543"""
import argparse, json, struct, numpy as np
from matplotlib.path import Path
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("out"); ap.add_argument("hp"); ap.add_argument("poly")
ap.add_argument("--zmin-lvl", type=float, default=543)
a = ap.parse_args()
g = json.load(open(a.hp)); px = np.array([[float(v) for v in p.split(",")] for p in a.poly.split()])
lvl = np.c_[g["x0"] + px[:, 0] * g["res"], g["y0"] + (g["ny"] - 1 - px[:, 1]) * g["res"]]
m = np.fromfile(a.car, dtype=TRI, offset=84); c = m["v"].mean(1)
sel = Path(lvl).contains_points(c[:, :2]) & (c[:, 2] > a.zmin_lvl)
k = m[sel]
with open(a.out, "wb") as f: f.write(b"miata extract_hp".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(a.out, len(k), c[sel].min(0).round(), c[sel].max(0).round())
