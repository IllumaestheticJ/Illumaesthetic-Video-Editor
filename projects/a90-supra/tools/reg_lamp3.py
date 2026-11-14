"""Refine a lamp part pose with SYMMETRIC trimmed ICP (part->car and car-lamp-patch->part) from flipped starts around a seed pose.
The car patch = car points inside --box (the lamp's outer face region). Starts: seed pose x {identity, 180 deg about each part PCA
axis} x {as scanned, mirrored about the part's own PCA plane}. Score = mean of the two 'within 2 mm' fractions.
    python projects/a90-supra/tools/reg_lamp3.py part.stl --seed seed.json --side R --box=... --out T.json"""
import argparse, json
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def pts(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); D = np.eye(3); D[2, 2] = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ D @ U.T; return R, cb - R @ ca
ap = argparse.ArgumentParser(); ap.add_argument("part"); ap.add_argument("--seed"); ap.add_argument("--side", default="R")
ap.add_argument("--box", required=True); ap.add_argument("--out"); ap.add_argument("--keep", type=float, default=0.7)
a = ap.parse_args()
rng = np.random.default_rng(0)
P0 = pts(a.part); P0 = P0[rng.choice(len(P0), min(len(P0), 20000), replace=False)]
car = pts("/home/user/media/work/a90/car_2mm.stl")
x0, x1, y0, y1, z0, z1 = [float(v) for v in a.box.split(",")]; s = -1 if a.side == "R" else 1
T = car[(car[:, 0] > x0) & (car[:, 0] < x1) & (s * car[:, 1] > y0) & (s * car[:, 1] < y1) & (car[:, 2] > z0) & (car[:, 2] < z1)]
T = T[rng.choice(len(T), min(len(T), 40000), replace=False)]; tt = cKDTree(T)
M0 = np.array(json.load(open(a.seed))["T_part_to_car_mm"])
cp = P0.mean(0); _, V = np.linalg.eigh(np.cov((P0 - cp).T))
def flip(axis):
    F = np.eye(3)
    if axis is not None:
        F = 2 * np.outer(V[:, axis], V[:, axis]) - np.eye(3)       # 180 deg about that axis
    return F
best = None
for mir in (None, 0, 1, 2):
    Mm = np.eye(3) if mir is None else np.eye(3) - 2 * np.outer(V[:, mir], V[:, mir])   # reflect across a PCA plane
    for fl in (None, 0, 1, 2):
        A = flip(fl) @ Mm; P = (P0 - cp) @ A.T + cp
        R, t = M0[:3, :3], M0[:3, 3]
        for ub in (25, 12, 6, 3):
            for _ in range(20):
                Q = P @ R.T + t; tp = cKDTree(Q)
                d1, i1 = tt.query(Q, distance_upper_bound=ub * 3, workers=4); d2, i2 = tp.query(T, distance_upper_bound=ub * 3, workers=4)
                k1 = np.isfinite(d1); k2 = np.isfinite(d2)
                if k1.sum() < 50 or k2.sum() < 50: break
                k1 &= d1 <= np.quantile(d1[k1], a.keep); k2 &= d2 <= np.quantile(d2[k2], a.keep)
                src = np.r_[P[k1], P[i2[k2]]]; dst = np.r_[T[i1[k1]], T[k2]]
                R, t = kabsch(src, dst)
        Q = P @ R.T + t; d1, _ = tt.query(Q, distance_upper_bound=30, workers=4); d2, _ = cKDTree(Q).query(T, distance_upper_bound=30, workers=4)
        sc = 0.5 * ((d1 < 2).mean() + (d2 < 2).mean())
        print(f"mirror_plane={mir} flip_axis={fl}: part->car {(d1<2).mean():.2f}  car->part {(d2<2).mean():.2f}  median {np.median(d1):.1f} mm", flush=True)
        if best is None or sc > best[0]: best = (sc, mir, fl, R, t, A, float((d1 < 2).mean()), float((d2 < 2).mean()), float(np.median(d1)))
sc, mir, fl, R, t, A, f1, f2, med = best
# full transform on raw part points: x -> R (A (x - cp) + cp) + t
M = np.eye(4); M[:3, :3] = R @ A; M[:3, 3] = R @ (cp - A @ cp) + t
print("BEST mirror_plane", mir, "flip", fl, "part->car %.2f car->part %.2f median %.1f" % (f1, f2, med))
if a.out: json.dump(dict(part=a.part, side=a.side, mirrored=bool(np.linalg.det(M[:3, :3]) < 0), part_to_car_within2=f1, car_to_part_within2=f2,
                         median_mm=med, T_part_to_car_mm=M.tolist(), note="apply to raw part points; flip triangle winding if mirrored"), open(a.out, "w"), indent=1)
