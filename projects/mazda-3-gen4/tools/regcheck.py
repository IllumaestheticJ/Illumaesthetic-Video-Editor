"""Registration check of part scans vs the full car (levelled frame, mm): % of part points within 15 mm of the car,
median distance, and what a trimmed ICP would change (not applied).  regcheck.py car.stl part.stl [...]"""
import sys, os, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
car = load(sys.argv[1]); tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f); dist, _ = tree.query(p); near = dist < 15
    q = p[near].copy(); Rt = np.eye(3); tt = np.zeros(3)
    for _ in range(20):
        dd, ii = tree.query(q); m = dd < 10
        A, B = q[m], car[ii[m]]; ca, cb = A.mean(0), B.mean(0)
        U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
        R = Vt.T @ D @ U.T; t = cb - R @ ca; q = q @ R.T + t; Rt = R @ Rt; tt = R @ tt + t
    ang = np.degrees(np.arccos(np.clip((np.trace(Rt) - 1) / 2, -1, 1))); d2, _ = tree.query(q)
    print(f"{os.path.basename(f):22s} n={len(p):7d} within15mm={near.mean()*100:5.1f}% median={np.median(dist[near]):5.2f}mm"
          f" | ICP would move {np.linalg.norm(tt):5.1f}mm {ang:4.2f}deg -> median {np.median(d2):5.2f}mm")
