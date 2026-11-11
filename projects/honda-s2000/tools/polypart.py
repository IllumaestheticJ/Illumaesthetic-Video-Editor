"""Cut a panel out of the levelled car (mm) with a top-view polygon traced on the ortho render (match/panels_px.json),
optionally keeping only triangles that are missing from a state scan where that panel is open (--state, --dist).
    python projects/honda-s2000/tools/polypart.py car_lvl.stl hood part.stl rest.stl [--zmin 400] [--zmax 2000] [--state s.stl --dist 10]
prep frame (m) = levelled (mm)/1000 + (0, 0, 0.0900) (car4.json root_location)."""
import argparse, json, os, struct
import numpy as np
from scipy.spatial import cKDTree


def inside(poly, pts):
    """Vectorised even-odd ray casting."""
    x, y = pts[:, 0], pts[:, 1]; res = np.zeros(len(pts), bool)
    for (x1, y1), (x2, y2) in zip(poly, np.roll(poly, -1, axis=0)):
        cond = (y1 > y) != (y2 > y)
        xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1 + 1e-12)
        res ^= cond & (x < xi)
    return res


TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ZOFF = 90.025  # mm, prep z = lvl z + ZOFF
ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("panel"); ap.add_argument("part"); ap.add_argument("rest")
ap.add_argument("--zmin", type=float, default=-1e9); ap.add_argument("--zmax", type=float, default=1e9)
ap.add_argument("--top", type=float, default=0, help="keep only tris within this many mm of the highest surface per 20 mm cell")
ap.add_argument("--state"); ap.add_argument("--dist", type=float, default=10)
a = ap.parse_args()
J = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "match", "panels_px.json")))[a.panel]
s = 0.10125 * (25.6 - J["z"]) / 1080 * 1000  # mm per px
poly = np.array([[(u - 540) * s, 170 + (960 - v) * s] for u, v in J["px"]])
m = np.fromfile(a.car, dtype=TRI, offset=84); c = m["v"].mean(1).astype(float)
sel = inside(poly, c[:, :2]) & (c[:, 2] + ZOFF > a.zmin) & (c[:, 2] + ZOFF < a.zmax)
if a.top:
    idx = np.where(sel)[0]; ij = np.floor(c[idx, :2] / 20).astype(np.int64); key = ij[:, 0] * 100000 + ij[:, 1]
    order = np.argsort(key); k2 = key[order]; zz = c[idx[order], 2]
    starts = np.r_[0, np.where(np.diff(k2))[0] + 1]; zmax = np.maximum.reduceat(zz, starts)
    cell = np.repeat(np.arange(len(starts)), np.diff(np.r_[starts, len(k2)]))
    drop = zz < zmax[cell] - a.top; sel[idx[order][drop]] = False
if a.state:
    st = np.fromfile(a.state, dtype=TRI, offset=84)["v"].mean(1).astype(float)
    d, _ = cKDTree(st).query(c[sel], distance_upper_bound=a.dist)
    idx = np.where(sel)[0]; sel[idx[np.isfinite(d)]] = False
print(f"{a.panel}: {sel.sum()} tris, bbox {np.round(c[sel].min(0))} .. {np.round(c[sel].max(0))} (lvl mm)")
for p, mm in ((a.part, m[sel]), (a.rest, m[~sel])):
    if p == "-": continue
    with open(p, "wb") as f:
        f.write(f"ive polypart {a.panel}".encode().ljust(80)); f.write(struct.pack("<I", len(mm))); mm.tofile(f)
