"""Panels-off composite (levelled mm STLs): base car minus each --cut panel (tris within --cut-mm of it), plus
NEW geometry from state scans under the panels. Per (panel, fill) pair:
  keep fill tris whose XY falls in the panel's 20 mm footprint grid (dilated --dilate cells), below the panel's
  top surface there (minus --below mm, so a propped-open panel in the state scan is dropped), above --zmin,
  and > --new mm from the base car (only what the panel was hiding).
    fill.py out.stl --car car.stl --pair hood.stl:hb_off.stl --pair lid.stl:tr_open.stl [--cut panel.stl ...]"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ld = lambda p: np.fromfile(p, dtype=TRI, offset=84)
ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--car", required=True)
ap.add_argument("--pair", action="append", default=[]); ap.add_argument("--cut", action="append", default=[])
ap.add_argument("--cut-mm", type=float, default=9.0); ap.add_argument("--new", type=float, default=7.0)
ap.add_argument("--below", type=float, default=10.0); ap.add_argument("--dilate", type=int, default=1)
ap.add_argument("--zmin", type=float, default=-1e9)
a = ap.parse_args()
car = ld(a.car); cc = car["v"].mean(1); keep = np.ones(len(car), bool)
for p in a.cut:
    v = ld(p)["v"].reshape(-1, 3)
    d, _ = cKDTree(v[:: max(1, len(v) // 1_500_000)]).query(cc, distance_upper_bound=a.cut_mm)
    keep &= ~(d < a.cut_mm)
print("base", len(car), "cut", int((~keep).sum()))
pieces = [car[keep]]; tcar = cKDTree(cc[keep][::2]); acc = None
G = 20.0
for pr in a.pair:
    pf, ff = pr.split(":")
    pc = ld(pf)["v"].mean(1); lo = pc[:, :2].min(0) - G * (a.dilate + 1)
    gi = np.floor((pc[:, :2] - lo) / G).astype(int); shape = gi.max(0) + a.dilate + 3
    top = np.full(shape, -1e9); np.maximum.at(top, (gi[:, 0], gi[:, 1]), pc[:, 2])
    occ = top > -1e8
    if a.dilate:
        occ2 = ndimage.binary_dilation(occ, iterations=a.dilate)
        top = np.where(occ, top, ndimage.maximum_filter(top, size=2 * a.dilate + 1)); occ = occ2
    m = ld(ff); c = m["v"].mean(1)
    g = np.floor((c[:, :2] - lo) / G).astype(int)
    inb = np.all((g >= 0) & (g < shape), axis=1)
    ok = np.zeros(len(c), bool); gg = g[inb]
    ok[inb] = occ[gg[:, 0], gg[:, 1]] & (c[inb, 2] < top[gg[:, 0], gg[:, 1]] - a.below) & (c[inb, 2] > a.zmin)
    idx = np.where(ok)[0]
    d, _ = tcar.query(c[idx], distance_upper_bound=a.new * 2); idx = idx[d > a.new]
    if acc is not None and len(idx):
        d2, _ = cKDTree(acc).query(c[idx], distance_upper_bound=a.new * 2); idx = idx[d2 > a.new]
    acc = c[idx] if acc is None else np.concatenate([acc, c[idx]])
    print(pr, "fill +", len(idx)); pieces.append(m[idx])
out = np.concatenate(pieces)
with open(a.out, "wb") as f:
    f.write(b"miata panels-off composite".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
print(a.out, len(out))
