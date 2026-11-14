"""Multi-start trimmed ICP of a loose lamp part onto the car's rear corner (raw mm). Starts: the part's PCA frame aligned to the
crop's PCA frame in all 4 proper sign combinations x 3 axis orders x (as scanned, mirrored), centroid-matched, plus jitter.
Trimmed point-to-point ICP (closest 60 %), 30 -> 10 -> 3 mm. Score: share of part points within 2 mm of the car.
    python projects/a90-supra/tools/reg_lamp2.py part.stl --side R --out T.json [--box xmin,xmax,ymin,ymax,zmin,zmax]"""
import argparse, itertools, json
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def pts(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); D = np.eye(3); D[2, 2] = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ D @ U.T; return R, cb - R @ ca
def icp(P, tree, T, R, t, steps=((30, 25), (10, 25), (3, 30)), keep=0.6):
    for ub, n in steps:
        for _ in range(n):
            Q = P @ R.T + t; d, i = tree.query(Q, distance_upper_bound=ub * 3, workers=4); ok = np.isfinite(d)
            if ok.sum() < 50: return R, t
            thr = np.quantile(d[ok], keep); m = ok & (d <= max(thr, 1e-6))
            R, t = kabsch(P[m], T[i[m]])
    return R, t
ap = argparse.ArgumentParser(); ap.add_argument("part"); ap.add_argument("--side", default="R"); ap.add_argument("--out")
ap.add_argument("--box", default="-2200,-1700,250,1000,550,950"); ap.add_argument("--ref")
a = ap.parse_args()
P0 = pts(a.part); P0 = P0[np.random.default_rng(0).choice(len(P0), min(len(P0), 25000), replace=False)]
car = pts(a.ref) if a.ref else pts("/home/user/media/work/a90/car_2mm.stl")
x0, x1, y0, y1, z0, z1 = [float(v) for v in a.box.split(",")]; s = -1 if a.side == "R" else 1
if a.ref: T = car
else: T = car[(car[:, 0] > x0) & (car[:, 0] < x1) & (s * car[:, 1] > y0) & (s * car[:, 1] < y1) & (car[:, 2] > z0) & (car[:, 2] < z1)]
tree = cKDTree(T); allt = cKDTree(car[np.random.default_rng(1).choice(len(car), min(len(car), 3000000), replace=False)])
ct = T.mean(0); et, Vt = np.linalg.eigh(np.cov((T - ct).T))
best = None
for mirror in (False, True):
    P = P0 * ([1, -1, 1] if mirror else [1, 1, 1]); cp = P.mean(0); ep, Vp = np.linalg.eigh(np.cov((P - cp).T))
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            A = Vp[:, perm] * sg
            if np.linalg.det(A) * np.linalg.det(Vt) < 0: continue
            R = Vt @ A.T; t = ct - R @ cp
            R, t = icp(P, tree, T, R, t)
            d, _ = allt.query(P @ R.T + t, distance_upper_bound=20, workers=4)
            f2 = float((d < 2).mean())
            if best is None or f2 > best[0]: best = (f2, mirror, R, t, float((d < 4).mean()), float(np.median(d)))
    print("mirror", mirror, "best so far within 2mm %.2f 4mm %.2f median %.1f" % (best[0], best[4], best[5]), flush=True)
f2, mirror, R, t, f4, med = best
M = np.eye(4); M[:3, :3] = R; M[:3, 3] = t
if mirror: M = M @ np.diag([1, -1, 1, 1])
print("BEST side", a.side, "mirror", mirror, "within 2mm %.2f 4mm %.2f median %.1f mm" % (f2, f4, med), "centre", (P0.mean(0) @ M[:3, :3].T + M[:3, 3]).round())
if a.out: json.dump(dict(part=a.part, side=a.side, mirror_y=mirror, f2=f2, f4=f4, median_mm=med, T_part_to_car_mm=M.tolist(),
                         note="T already includes the y-mirror (apply T to the raw part points; flip triangle winding when mirror_y)"), open(a.out, "w"), indent=1)
