"""Registration check for Miata part/state scans (levelled, mm) against the levelled full car.
Prints overlap fraction (<15 mm), median distance, bbox, and the rigid correction a trimmed ICP would apply
(reported only). Adapted from projects/huracan-evo/tools/regcheck.py.
  regcheck.py car_lvl.stl part1.stl [part2.stl ...]"""
import sys, os, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
car = load(sys.argv[1]); car = car[car[:, 2] > 40]
tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f); n0 = len(p); p = p[p[:, 2] > 40]
    if len(p) > 400000: p = p[:: len(p) // 400000]
    dist, _ = tree.query(p)
    near = dist < 15
    q = p[near].copy(); Rt = np.eye(3); tt = np.zeros(3)
    for _ in range(15):
        dd, ii = tree.query(q); m = dd < 10
        A, B = q[m], car[ii[m]]
        ca, cb = A.mean(0), B.mean(0); H = (A - ca).T @ (B - cb)
        U, S, Vt = np.linalg.svd(H); R = Vt.T @ U.T
        if np.linalg.det(R) < 0: Vt[-1] *= -1; R = Vt.T @ U.T
        t = cb - R @ ca; q = q @ R.T + t; Rt = R @ Rt; tt = R @ tt + t
    ang = np.degrees(np.arccos(np.clip((np.trace(Rt) - 1) / 2, -1, 1)))
    d2, _ = tree.query(q)
    lo, hi = p.min(0), p.max(0)
    print(f"{os.path.basename(f)[:-4]:30s} tris={n0:8d} overlap<15mm={near.mean()*100:5.1f}% median={np.median(dist[near]):5.2f}mm "
          f"| ICP {np.linalg.norm(tt):6.1f}mm {ang:5.2f}deg -> {np.median(d2):5.2f}mm | bbox {lo.round(0)} {hi.round(0)}")
