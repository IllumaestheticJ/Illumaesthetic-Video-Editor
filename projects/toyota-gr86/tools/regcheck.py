"""Registration check (adapted from huracan-evo): distance from each part/state scan to the nearest point of a
full-car scan (both levelled). Registered parts sit 1-3 mm median on overlapping surface; a part in its own frame
shows tens/hundreds of mm. Also reports the rigid ICP correction it would take (not applied).
  regcheck.py car_lev.stl part_lev.stl [...]"""
import sys, os, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p):
    c = np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    return c[:: max(1, len(c) // 600000)]
car = load(sys.argv[1]); car = car[car[:, 2] > 40]
tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f); p = p[p[:, 2] > 40]
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
    np.save(f[:-4] + "_icp.npy", np.vstack([np.c_[Rt, tt], [0, 0, 0, 1]]))
    print(f"{os.path.basename(f)[:-4]:32s} overlap<15mm={near.mean()*100:5.1f}%  median={np.median(dist[near]):5.2f}mm"
          f"  | ICP corr {np.linalg.norm(tt):5.1f}mm {ang:4.2f}deg -> median {np.median(d2):5.2f}mm", flush=True)
