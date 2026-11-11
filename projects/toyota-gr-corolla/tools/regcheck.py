"""Registration check of part/state scans against the full car (raw Artec mm, no transforms).

    python projects/toyota-gr-corolla/tools/regcheck.py car_4mm.stl part1.stl [part2.stl ...]

For each part: fraction of its points within 15 mm of the car surface and their median distance
(same Artec frame -> ~1-3 mm), plus the rigid correction a trimmed point-to-point ICP would apply
(reported, not applied). Adapted from projects/huracan-evo/tools/regcheck.py.
"""
import os
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def load(p, n=400_000):
    m = np.memmap(p, dtype=TRI, offset=84, mode="r")
    return m["v"][:: max(1, len(m) // n)].mean(1).astype(np.float64)


car = load(sys.argv[1], 1_500_000)
tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f)
    dist, _ = tree.query(p)
    near = dist < 15
    q = p[near].copy()
    Rt, tt = np.eye(3), np.zeros(3)
    for _ in range(20):
        dd, ii = tree.query(q)
        m = dd < 10
        A, B = q[m], car[ii[m]]
        ca, cb = A.mean(0), B.mean(0)
        U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb))
        R = Vt.T @ U.T
        if np.linalg.det(R) < 0:
            Vt[-1] *= -1
            R = Vt.T @ U.T
        t = cb - R @ ca
        q = q @ R.T + t
        Rt, tt = R @ Rt, R @ tt + t
    ang = np.degrees(np.arccos(np.clip((np.trace(Rt) - 1) / 2, -1, 1)))
    d2, _ = tree.query(q)
    print(f"{os.path.basename(f)[:-4][:44]:44s} overlap<15mm={near.mean()*100:5.1f}%  median={np.median(dist[near]):5.2f}mm"
          f"  | ICP corr {np.linalg.norm(tt):6.1f}mm {ang:5.2f}deg -> median {np.median(d2):5.2f}mm")
