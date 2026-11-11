"""Cut a panel out of the levelled full-car STL (mm) by a top-view polygon traced on a near-orthographic top render
(reg/top_front.png / top_rear.png: 1080x1920, 2.0 m across, centre (0, cy) prepped m, image up = +Y, crop offset 360 px),
keeping triangles above --zmin (prepped m). Writes the panel STL and prints its bbox.
  extract.py car_lvl.stl out.stl --cy -1.0 --poly "x,y x,y ..." --zmin 0.6 [--like car4.json]"""
import argparse, json, struct, numpy as np
from matplotlib.path import Path
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("out")
ap.add_argument("--cy", type=float, required=True); ap.add_argument("--poly", required=True)
ap.add_argument("--zmin", type=float, default=0.0); ap.add_argument("--like", default="/home/user/media/work/miata/prep/car4.json")
a = ap.parse_args()
L = json.load(open(a.like)); root = np.array(L["root_location"]); s = 2.0 / 1080
px = np.array([[float(v) for v in p.split(",")] for p in a.poly.split()])
prep = np.c_[(px[:, 0] - 540) * s, a.cy - (px[:, 1] + 360 - 960) * s]
lvl = (prep - root[:2]) / L["unit_scale"]
m = np.fromfile(a.car, dtype=TRI, offset=84); c = m["v"].mean(1)
sel = Path(lvl).contains_points(c[:, :2]) & (c[:, 2] > (a.zmin - root[2]) / L["unit_scale"])
k = m[sel]
with open(a.out, "wb") as f: f.write(b"miata extract".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(a.out, len(k), c[sel].min(0).round(), c[sel].max(0).round())
