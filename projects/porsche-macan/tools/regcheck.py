"""Numeric registration check (adapted from huracan-evo/tools/regcheck.py): for each part STL (same levelled mm
frame as the car), nearest-surface distance to the full car where they overlap, plus what a point-to-point ICP
would correct (reported, not applied).
    python projects/porsche-macan/tools/regcheck.py car.stl part1.stl part2.stl ..."""
import os, sys
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p, n=600_000):
    c = np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    c = c[c[:, 2] > 40]
    return c[np.random.default_rng(0).choice(len(c), min(n, len(c)), replace=False)]
car = load(sys.argv[1], 3_000_000); tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f, 200_000); dist, _ = tree.query(p); near = dist < 15
    q = p[near].copy(); Rt = np.eye(3); tt = np.zeros(3)
    for _ in range(15):
        dd, ii = tree.query(q); m = dd < 10
        A, B = q[m], car[ii[m]]; ca, cb = A.mean(0), B.mean(0)
        U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); R = Vt.T @ U.T
        if np.linalg.det(R) < 0: Vt[-1] *= -1; R = Vt.T @ U.T
        t = cb - R @ ca; q = q @ R.T + t; Rt = R @ Rt; tt = R @ tt + t
    ang = np.degrees(np.arccos(np.clip((np.trace(Rt) - 1) / 2, -1, 1))); d2, _ = tree.query(q)
    print(f"{os.path.basename(f)[:-4]:28s} overlap<15mm={near.mean()*100:5.1f}%  median={np.median(dist[near]):5.2f}mm"
          f"  | ICP corr {np.linalg.norm(tt):5.1f}mm {ang:4.2f}deg -> median {np.median(d2):5.2f}mm")
