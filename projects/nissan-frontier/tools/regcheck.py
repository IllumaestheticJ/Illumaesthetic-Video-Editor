"""Registration check of state/part scans against the full truck (levelled mm STLs, after clean).
Median distance of each scan's points to the nearest full-car point where they overlap (<15 mm), and the rigid
correction a point-to-point ICP on that overlap would apply (reported only). Adapted from huracan-evo/tools/regcheck.py.
  regcheck.py full.stl part1.stl part2.stl ..."""
import sys, os, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
car = load(sys.argv[1]); car = car[car[:, 2] > 220]
tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f); p = p[p[:, 2] > 220]
    dist, _ = tree.query(p)
    near = dist < 15
    q = p[near][::3].copy(); Rt = np.eye(3); tt = np.zeros(3)
    for _ in range(20):
        dd, ii = tree.query(q); m = dd < 10
        A, B = q[m], car[ii[m]]
        ca, cb = A.mean(0), B.mean(0); H = (A - ca).T @ (B - cb)
        U, S, Vt = np.linalg.svd(H); R = Vt.T @ U.T
        if np.linalg.det(R) < 0: Vt[-1] *= -1; R = Vt.T @ U.T
        t = cb - R @ ca; q = q @ R.T + t; Rt = R @ Rt; tt = R @ tt + t
    ang = np.degrees(np.arccos(np.clip((np.trace(Rt) - 1) / 2, -1, 1)))
    d2, _ = tree.query(q)
    print(f"{os.path.basename(f)[:-4]:14s} n={len(p):8d} overlap<15mm={near.mean()*100:5.1f}%  median={np.median(dist[near]):5.2f}mm"
          f"  p90 all={np.percentile(dist,90):7.1f}mm | ICP corr {np.linalg.norm(tt):5.1f}mm {ang:4.2f}deg -> median {np.median(d2):5.2f}mm")
