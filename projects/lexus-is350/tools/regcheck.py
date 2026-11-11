"""Registration check: distance from each part scan's points to the nearest full-car point (both levelled, 8 mm).
# Lexus: parts subsampled to 150k points (full-res ICP took >30 min).
A part captured in the same Artec frame sits ON the car surface where it overlaps it (median ~1-3 mm);
a part in its own frame shows tens/hundreds of mm. Also runs a point-to-point ICP on the overlap to see
whether a small correction would help (reports the rigid correction; does not apply it)."""
import sys, glob, os, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
d = sys.argv[1]
car = load(os.environ.get("CAR", f"{d}/full_car.stl")); car = car[car[:, 2] > 40]
tree = cKDTree(car)
for f in sorted(glob.glob(f"{d}/*.stl")):
    if "full_car" in f: continue
    p = load(f); p = p[p[:, 2] > 40]; p = p[np.random.default_rng(0).choice(len(p), min(len(p), 150000), replace=False)]
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
    print(f"{os.path.basename(f)[:-4]:40s} n={len(p):7d} overlap<15mm={near.mean()*100:5.1f}%  median={np.median(dist[near]):5.2f}mm"
          f"  | ICP corr: {np.linalg.norm(tt):5.1f}mm {ang:4.2f}deg -> median {np.median(d2):5.2f}mm")
