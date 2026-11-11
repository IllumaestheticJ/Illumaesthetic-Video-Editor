"""Registration check of every levelled part scan against the levelled full car (adapted from huracan-evo).
    python regcheck.py car.stl parts_dir
Per part: overlap (<15 mm) fraction, median distance on the overlap, and the rigid correction a point-to-point
ICP would make (reported, not applied). Same Artec frame => median ~1-3 mm, ICP corr a few mm / <0.5 deg."""
import sys, glob, os, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
car = load(sys.argv[1]); car = car[car[:, 2] > 40]
tree = cKDTree(car)
for f in sorted(glob.glob(f"{sys.argv[2]}/*.stl")):
    p = load(f); p = p[p[:, 2] > 40]; p = p[:: max(1, len(p) // 400000)]
    dist, _ = tree.query(p)
    near = dist < 15
    if near.sum() < 100:
        print(f"{os.path.basename(f)[:-4]:34s} n={len(p):7d} overlap {near.mean()*100:5.1f}%  NO OVERLAP  median all {np.median(dist):7.1f}mm"); continue
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
    print(f"{os.path.basename(f)[:-4]:34s} n={len(p):7d} overlap {near.mean()*100:5.1f}%  median {np.median(dist[near]):5.2f}mm"
          f" | ICP corr {np.linalg.norm(tt):6.1f}mm {ang:5.2f}deg -> {np.median(d2):5.2f}mm")
