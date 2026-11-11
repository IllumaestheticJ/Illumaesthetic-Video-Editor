"""Exploded-view base for the MR2: roof-down full car with the removable panels trimmed + the state scans *as captured*
where the panels used to hide structure (lessons: state scan over the full car trimmed back, smallest zone).
All inputs levelled, 3 mm, same frame (mm).
  composite.py car.stl out.stl --parts a.stl b.stl ... --state S.stl:y0:y1 [--state ...]
- car tris within TRIM mm of any part = that panel on the car -> removed (the part scan replaces it)
- state tris added only if: inside its Y band, > ADD mm from the trimmed car, < NEAR mm from a removed panel
  (the zone the panel hid), not above the car's own roofline + 30 mm (= the panel captured open), not in a wheel
  cylinder (the state sessions' wheels/steering differ), not near a panel's fitted open pose (--open), and above z 25 mm (floor scraps)."""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
TRIM, ADD, NEAR = 6.0, 6.0, 220.0
WHEELS = [(1270, 300), (-1300, 300)]  # (y, z) axle centres, mm (front / rear), |x| > 560

ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("out")
ap.add_argument("--parts", nargs="+", required=True); ap.add_argument("--state", action="append", default=[])
ap.add_argument("--open", action="append", default=[], help="part.stl:hinge.json - drop state points within 30 mm of the part rotated to its fitted open pose")
a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84); cc = car["v"].mean(1)
P = np.concatenate([np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1) for p in a.parts])
tp = cKDTree(P)
d, _ = tp.query(cc, distance_upper_bound=TRIM + 1)
keep = d > TRIM
kc = car[keep]
print("car tris trimmed:", int((~keep).sum()), "of", len(car))
# roofline of the untrimmed car + parts (40 mm cells)
allp = np.concatenate([cc, P]); cell = 40.0
key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(allp[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, allp[:, 2])
tk = cKDTree(kc["v"].mean(1))
import json
from scipy.spatial.transform import Rotation as Rot
opens = []
for o in a.open:
    pp, hj = o.split(":"); h = json.load(open(hj)); yh, zh = h["fit_mm"]
    R = Rot.from_rotvec(np.radians(h["open_deg"]) * np.array(h["axis"])).as_matrix(); c = np.array([0, yh, zh])
    q = np.fromfile(pp, dtype=TRI, offset=84)["v"].mean(1); opens.append((q - c) @ R.T + c)
to = cKDTree(np.concatenate(opens)) if opens else None
adds = []
for s in a.state:
    path, y0, y1 = s.rsplit(":", 2); y0, y1 = float(y0), float(y1)
    st = np.fromfile(path, dtype=TRI, offset=84); sc = st["v"].mean(1)
    m = (sc[:, 1] > y0) & (sc[:, 1] < y1) & (sc[:, 2] > 25)
    ks = key(sc[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1)
    roof = np.where(u[i] == ks, top[i], -1e9)
    m &= sc[:, 2] < roof + 30
    for wy, wz in WHEELS:
        m &= ~((np.abs(sc[:, 0]) > 560) & (np.hypot(sc[:, 1] - wy, sc[:, 2] - wz) < 330))
    for tree, lim, far in ((tk, ADD, True), (to, 30.0, True), (tp, NEAR, False)):  # cheap masks first, query survivors only
        if tree is None: continue
        idx = np.where(m)[0]; dd, _ = tree.query(sc[idx], distance_upper_bound=lim + 1, workers=-1)
        m[idx] = dd > lim if far else dd < lim
    print(path.split("/")[-1], "added", int(m.sum()))
    adds.append(st[m])
res = np.concatenate([kc] + adds)
with open(a.out, "wb") as f:
    f.write(b"ive mr2 composite".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
print(a.out, len(res))
