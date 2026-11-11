"""Exploded-view base for the Revuelto (extends projects/huracan-evo/tools/composite.py to several zone state scans).
All inputs: levelled + cropped STLs in one frame (mm).
  composite.py car.stl out_base.stl --parts p1.stl p2.stl ... --states s1.stl s2.stl ...
- car triangles within TRIM mm of any part = that panel on the car -> removed (the part scan replaces it)
- each state scan (as captured, e.g. 'Fender Removed') adds its triangles that are > ADD mm from the base built so
  far AND > PART_EX mm from every part at home (state scans still contain the *other* parts, which must not stay
  behind as ghosts when those parts fly off) AND not above the full car's top surface (Hood Open's raised lid).
"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("out")
ap.add_argument("--parts", nargs="+", required=True); ap.add_argument("--states", nargs="*", default=[])
ap.add_argument("--trim", type=float, default=6.0); ap.add_argument("--add", type=float, default=6.0)
ap.add_argument("--part-ex", type=float, default=8.0)
a = ap.parse_args()
ld = lambda p: np.fromfile(p, dtype=TRI, offset=84)
car = ld(a.car); cc = car["v"].mean(1)
P = np.concatenate([ld(p)["v"].mean(1) for p in a.parts]).astype(np.float32)
ptree = cKDTree(P)
d, _ = ptree.query(cc, distance_upper_bound=a.trim + 1)
base = car[d > a.trim]
print("car tris trimmed (panels):", len(car) - len(base), "of", len(car), flush=True)
cell = 40.0
key = lambda xy: (np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64))
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
for s in a.states:
    st = ld(s); sc = st["v"].mean(1)
    d1, _ = cKDTree(base["v"].mean(1)).query(sc, distance_upper_bound=a.add + 1)
    d2, _ = ptree.query(sc, distance_upper_bound=a.part_ex + 1)
    ks = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[i] == ks, top[i], 1e9)
    add = (d1 > a.add) & (d2 > a.part_ex) & (sc[:, 2] < roof + 30)
    print(f"{s.split('/')[-1]}: +{int(add.sum())} of {len(st)}", flush=True)
    base = np.concatenate([base, st[add]])
with open(a.out, "wb") as f:
    f.write(b"ive revuelto composite".ljust(80)); f.write(struct.pack("<I", len(base))); base.tofile(f)
print(a.out, len(base))
