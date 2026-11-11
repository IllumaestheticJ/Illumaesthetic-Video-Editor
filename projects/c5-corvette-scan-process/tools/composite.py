"""Stripped-front base (adapted from huracan-evo/tools/composite.py): full car minus every triangle within TRIM mm
of the removed-part scans (= those panels on the car), plus state-scan triangles more than ADD mm from the trimmed
car (= structure the panels hid). All inputs: binary STL, mm, shared Artec frame.
  composite.py car.stl out.stl --parts p1.stl p2.stl --states s1.stl s2.stl [--state-xmax 40 ...]"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("out")
ap.add_argument("--parts", nargs="+", required=True); ap.add_argument("--states", nargs="+", required=True)
ap.add_argument("--trim", type=float, default=8.0); ap.add_argument("--add", type=float, default=6.0)
ap.add_argument("--xmax", default="", type=lambda s: [float(x) for x in s.split(",") if x], help="per-state: keep only x < value (mm)")
ap.add_argument("--xmin", default="", type=lambda s: [float(x) for x in s.split(",") if x], help="per-state: keep only x > value (mm)")
ap.add_argument("--below-top", type=float, default=25.0, help="drop state tris higher than car-top-in-40mm-cell minus this (duplicate panels)")
ap.add_argument("--zmin", type=float, default=100.0, help="drop state tris below this z (mm, raw frame) - ground scraps")
ap.add_argument("--drop-box", default="", help="xmin,xmax,ymin,ymax,zmin,zmax (mm): drop state tris inside (e.g. a re-steered wheel)")
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)
car = L(a.car); cc = car["v"].mean(1)
P = np.concatenate([L(p)["v"].reshape(-1, 3) for p in a.parts])
d, _ = cKDTree(P).query(cc, distance_upper_bound=a.trim + 1)
kc = car[d > a.trim]; print("trimmed", int((d <= a.trim).sum()), "of", len(car))
tree = cKDTree(kc["v"].mean(1)); out = [kc]
cell = 40.0; key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
for i, s in enumerate(a.states):
    st = L(s); sc = st["v"].mean(1); m = np.ones(len(st), bool)
    if i < len(a.xmax) and a.xmax[i] < 1e8: m &= sc[:, 0] < a.xmax[i]
    if i < len(a.xmin) and a.xmin[i] > -1e8: m &= sc[:, 0] > a.xmin[i]
    d2, _ = tree.query(sc, distance_upper_bound=a.add + 1); m &= d2 > a.add
    ks = key(sc[:, :2]); ii = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[ii] == ks, top[ii], 1e9)
    m &= (sc[:, 2] < roof - a.below_top) & (sc[:, 2] > a.zmin)
    if a.drop_box:
        b = [float(x) for x in a.drop_box.split(",")]
        m &= ~((sc[:, 0] > b[0]) & (sc[:, 0] < b[1]) & (sc[:, 1] > b[2]) & (sc[:, 1] < b[3]) & (sc[:, 2] > b[4]) & (sc[:, 2] < b[5]))
    print(s.split("/")[-1], "added", int(m.sum())); out.append(st[m])
o = np.concatenate(out)
with open(a.out, "wb") as f:
    f.write(b"c5 composite".ljust(80)); f.write(struct.pack("<I", len(o))); o.tofile(f)
print(a.out, len(o))
