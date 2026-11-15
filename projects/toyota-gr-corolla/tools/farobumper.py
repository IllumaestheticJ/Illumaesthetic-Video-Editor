"""Stock front bumper from the FARO full-car scan (user on v6: the full-car scan's bumper misses a huge chunk; use the
other full car scan - not the facelift one). FARO is registered to car4w (faro_reg.stl, ICP 0.3 deg / 22 mm).
Bumper = FARO faces within --near mm of the bumper zone (the car faces the bumper-off cut removed + the separate bumper
scan), not on the kept car (> --keep mm from car_cut: headlights, fenders stay ours) and below the bumper's top edge;
+ the separate bumper scan where FARO has no data (inner face, gaps) + any removed car face neither covers.
    farobumper.py car.stl car_cut.stl faro_reg.stl bumper.stl bumper_out.stl car_out.stl"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
for n in ("car", "car_cut", "faro", "bumper", "bumper_out", "car_out"): ap.add_argument(n)
ap.add_argument("--near", type=float, default=20); ap.add_argument("--keep", type=float, default=4); ap.add_argument("--fill", type=float, default=8)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=DT, offset=84)
def save(p, m):
    with open(p, "wb") as f: f.write(b"grc farobumper".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
car, cut, fa, bu = L(a.car), L(a.car_cut), L(a.faro), L(a.bumper)
cc, ct, fc, bc = (m["v"].mean(1) for m in (car, cut, fa, bu))
d, _ = cKDTree(ct).query(cc, distance_upper_bound=0.5, workers=-1); removed = cc[np.isinf(d)]
zone = cKDTree(np.concatenate([removed, bc[::2]]))
lo, hi = np.minimum(removed.min(0), bc.min(0)) - a.near, np.maximum(removed.max(0), bc.max(0)) + a.near
cand = np.where(np.all((fc > lo) & (fc < hi), 1))[0]
dz, _ = zone.query(fc[cand], distance_upper_bound=a.near + 1, workers=-1); cand = cand[dz < a.near]
dk, _ = cKDTree(ct).query(fc[cand], distance_upper_bound=a.keep + 1, workers=-1); cand = cand[dk > a.keep]
# top edge: per 20 mm column of the bumper scan (98th pct), capped at the corners (headlight shards)
edges = np.arange(bc[:, 0].min() - 20, bc[:, 0].max() + 20, 20); k = np.digitize(bc[:, 0], edges); top = np.full(len(edges) + 1, np.inf)
for i in np.unique(k): top[i] = np.percentile(bc[k == i, 2], 98)
xc = 0.5 * (bc[:, 0].min() + bc[:, 0].max())
line = lambda x: np.where(np.abs(x - xc) > 450, np.minimum(top[np.digitize(x, edges)], 32), top[np.digitize(x, edges)])
cand = cand[fc[cand, 2] <= line(fc[cand, 0]) + 8]
fb = fa[cand]; T = cKDTree(fb["v"].mean(1))
db, _ = T.query(bc, distance_upper_bound=a.fill + 1, workers=-1); add_bu = bu[db > a.fill]
rem = car[np.isinf(d)]; dr1, _ = T.query(removed, distance_upper_bound=a.fill + 1, workers=-1)
dr2, _ = cKDTree(bc).query(removed, distance_upper_bound=a.fill + 1, workers=-1); add_car = rem[(dr1 > a.fill) & (dr2 > a.fill)]
part = np.concatenate([fb, add_bu, add_car])
print("FARO bumper", len(fb), "| + bumper scan where FARO is empty", len(add_bu), "| + car skin neither covers", len(add_car), "| part", len(part))
save(a.bumper_out, part); save(a.car_out, np.concatenate([cut, part]))
