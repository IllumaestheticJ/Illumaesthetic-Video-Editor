"""Exploded-view base for the C5: full car with every removable panel trimmed, plus the 'removed' state scans as
captured where they add structure the panels hide (lesson: state scans as captured over the full car trimmed back).
All inputs: levelled + cropped STLs in one frame (mm). Parts must be in their CLOSED (installed) pose.
  composite.py car.stl out.stl --parts p1.stl p2.stl ... --states s1.stl s2.stl ... [--exclude-open hood_open.stl]
- car tris within TRIM mm of any part point = that panel on the car -> removed
- state tris farther than ADD mm from the trimmed car AND from every part = newly exposed structure -> added
  (a state scan still has the other panels on; those coincide with a part and are not added back)
- --states-first-wins: later states skip tris within ADD of what earlier states already added (no doubled skins)"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("out")
ap.add_argument("--parts", nargs="+", required=True); ap.add_argument("--states", nargs="*", default=[])
ap.add_argument("--trim", type=float, default=7.0); ap.add_argument("--add", type=float, default=7.0)
ap.add_argument("--state-zmin", type=float, default=70.0, help="drop state tris below this height (mm): scanned ground scraps under the sills")
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)
car = L(a.car); cc = car["v"].mean(1)
P = np.concatenate([L(p)["v"].mean(1) for p in a.parts])
ptree = cKDTree(P)
d, _ = ptree.query(cc, distance_upper_bound=a.trim + 1)
kc = car[d > a.trim]
print(f"car {len(car)} -> trimmed {len(kc)} ({len(car)-len(kc)} panel tris removed)", flush=True)
# roofline of the full car for the propped-hood rule
cell = 40.0
key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(cc[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
pieces = [kc]
ref = cKDTree(kc["v"].mean(1))
added = None
for sp in a.states:
    s = L(sp); sc = s["v"].mean(1)
    d1, _ = ref.query(sc, distance_upper_bound=a.add + 1)
    d2, _ = ptree.query(sc, distance_upper_bound=a.add + 1)
    keep = (d1 > a.add) & (d2 > a.add)
    ka = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ka), 0, len(u) - 1); roof = np.where(u[i] == ka, top[i], -1e9)
    keep &= ~((sc[:, 2] > roof + 40) & (sc[:, 1] < 0))           # propped-open hood / anything above the car
    keep &= sc[:, 2] > a.state_zmin
    if added is not None:
        d3, _ = added.query(sc, distance_upper_bound=a.add + 1); keep &= d3 > a.add
    print(f"{sp.split('/')[-1]}: +{int(keep.sum())} of {len(s)}", flush=True)
    pieces.append(s[keep])
    allv = np.concatenate([p["v"].mean(1) for p in pieces[1:]])
    added = cKDTree(allv) if len(allv) else None
res = np.concatenate(pieces)
with open(a.out, "wb") as f:
    f.write(b"ive c5 composite".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
print(a.out, len(res))
