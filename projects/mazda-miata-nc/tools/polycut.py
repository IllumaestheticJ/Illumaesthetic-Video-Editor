"""Cut a panel out of a levelled STL by an XY outline traced on the raw-scan seam map (tools/seam map: 2 mm/px,
x = -950 + 2 px, y = -1800 + 2 (799 - py)) and keep only its top skin (within --skin mm of the highest surface
in each 10 mm cell). Also writes the complement (car minus panel) with --rest.
    polycut.py car.stl hood.stl --rest car_nohood.stl --poly "px,py px,py ..." [--skin 25]"""
import argparse, struct
import numpy as np
from matplotlib.path import Path as MPath
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--rest")
ap.add_argument("--poly", required=True); ap.add_argument("--skin", type=float, default=25)
a = ap.parse_args()
pp = np.array([[float(v) for v in p.split(",")] for p in a.poly.split()])
poly = np.c_[-950 + 2 * pp[:, 0], -1800 + 2 * (799 - pp[:, 1])]
m = np.fromfile(a.src, dtype=TRI, offset=84); c = m["v"].mean(1)
ins = MPath(poly).contains_points(c[:, :2])
k = np.floor(c[:, 0] / 10).astype(np.int64) * 100000 + np.floor(c[:, 1] / 10).astype(np.int64)
u, inv = np.unique(k, return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, c[:, 2])
sel = ins & (c[:, 2] > top[inv] - a.skin)
def save(p, x):
    with open(p, "wb") as f:
        f.write(b"miata polycut".ljust(80)); f.write(struct.pack("<I", len(x))); x.tofile(f)
save(a.out, m[sel]); print(a.out, int(sel.sum()), c[sel].min(0).round(), c[sel].max(0).round())
if a.rest:
    save(a.rest, m[~sel]); print(a.rest, int((~sel).sum()))
