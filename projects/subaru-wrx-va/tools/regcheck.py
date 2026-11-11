"""Is a state/part scan in the full car's frame? (after the same level transform, both mm)
  regcheck.py car_clean.stl part_lvl.stl [...]
Prints the share of part points within 5/15 mm of the car and the median distance of the near ones;
then a trimmed point-to-point ICP on the overlap (reports the correction, does not apply it).
Same-frame Artec states: >50 % within 5 mm, median 1-3 mm, ICP correction < 3 mm / 0.2 deg.
"""
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def load(p, k=400000):
    c = np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    c = c[c[:, 2] > 40]
    if len(c) > k:
        c = c[np.random.default_rng(0).choice(len(c), k, replace=False)]
    return c


car = load(sys.argv[1], 1500000)
tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f)
    d, _ = tree.query(p)
    q = p[d < 15].copy(); Rt = np.eye(3); tt = np.zeros(3)
    for _ in range(20):
        dd, ii = tree.query(q); m = dd < 8
        if m.sum() < 200:
            break
        A, B = q[m], car[ii[m]]
        ca, cb = A.mean(0), B.mean(0); H = (A - ca).T @ (B - cb)
        U, S, Vt = np.linalg.svd(H); R = Vt.T @ U.T
        if np.linalg.det(R) < 0:
            Vt[-1] *= -1; R = Vt.T @ U.T
        t = cb - R @ ca; q = q @ R.T + t; Rt = R @ Rt; tt = R @ tt + t
    ang = np.degrees(np.arccos(np.clip((np.trace(Rt) - 1) / 2, -1, 1)))
    d2, _ = tree.query(q)
    print(f"{f.split('/')[-1]:32s} n={len(p):7d} <5mm {np.mean(d < 5):5.2f} <15mm {np.mean(d < 15):5.2f} "
          f"med(near) {np.median(d[d < 15]) if (d < 15).any() else -1:5.1f}  ICP: {ang:5.2f} deg, "
          f"|t|={np.linalg.norm(tt):6.1f} mm (centroid move {np.linalg.norm(q.mean(0) - p[d < 15].mean(0)):5.1f}), "
          f"after med {np.median(d2):4.1f}")
