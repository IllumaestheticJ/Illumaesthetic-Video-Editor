"""Global registration of a part/state scan in an unknown frame onto the levelled MR2 car (numpy + scipy only:
open3d has no wheel for this box's Python 3.13, so a90-supra/tools/globalreg.py can't run here).

  globalreg.py car_L.stl part_L.stl out_T.json [--region y0,y1] [--rots 600] [--init identity]

1. voxel-downsample both (20 mm), car optionally limited to a Y band (front / rear zone of the car).
2. coarse search: ~N rotations (Fibonacci 'up' directions x yaw steps) x centroid alignment, 12 trimmed ICP iterations each
   (keep the best 60 % pairs) -> score = fraction of part points within 15 mm of the car.
3. refine the best 6 at 8 mm voxels, 40 iterations, trimmed 70 %, then report fitness (<6 mm) and median distance.
Saves {"T": 4x4 part_L mm -> car_L mm, "fitness6": .., "median_mm": ..}. Always confirm with an overlay render.
"""
import argparse, json
import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)


def voxel(P, s):
    k = np.floor(P / s).astype(np.int64) + 100000
    _, idx = np.unique((k[:, 0] * 200000 + k[:, 1]) * 200000 + k[:, 2], return_index=True)
    return P[idx]


def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0)
    U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb))
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
    R = Vt.T @ D @ U.T
    return R, cb - R @ ca


def icp(src, tree, dst, R, t, iters, keep):
    for _ in range(iters):
        s = src @ R.T + t
        d, j = tree.query(s)
        m = d <= np.quantile(d, keep)
        dR, dt = kabsch(s[m], dst[j[m]])
        R, t = dR @ R, dR @ t + dt
    return R, t


def rotations(n):
    out = []
    ndir = max(8, n // 12)
    g = (1 + 5 ** 0.5) / 2
    for i in range(ndir):
        z = 1 - 2 * (i + 0.5) / ndir
        r = (1 - z * z) ** 0.5
        th = 2 * np.pi * i / g
        up = np.array([r * np.cos(th), r * np.sin(th), z])
        # R0 maps part 'up' direction -> +Z
        a = np.cross(up, [0, 0, 1.0]); s = np.linalg.norm(a); c = up[2]
        if s < 1e-9:
            R0 = np.eye(3) if c > 0 else np.diag([1, -1, -1.0])
        else:
            vx = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
            R0 = np.eye(3) + vx + vx @ vx * ((1 - c) / s ** 2)
        for k in range(12):
            y = 2 * np.pi * k / 12
            Rz = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
            out.append(Rz @ R0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("car"); ap.add_argument("part"); ap.add_argument("out")
    ap.add_argument("--region", help="y0,y1 mm band of the car to match against")
    ap.add_argument("--rots", type=int, default=600)
    ap.add_argument("--init", choices=["search", "identity"], default="search")
    a = ap.parse_args()
    car = load(a.car)
    if a.region:
        y0, y1 = map(float, a.region.split(","))
        car = car[(car[:, 1] > y0) & (car[:, 1] < y1)]
    part = load(a.part)
    C20, P20 = voxel(car, 20), voxel(part, 20)
    C8, P8 = voxel(car, 8), voxel(part, 8)
    t20, t8 = cKDTree(C20), cKDTree(C8)
    print("pts car", len(C20), "part", len(P20))
    cands = []
    if a.init == "identity":
        inits = [np.eye(3)]
    else:
        inits = rotations(a.rots)
    for R0 in inits:
        t0 = C20.mean(0) - (P20 @ R0.T).mean(0) if a.init == "search" else np.zeros(3)
        R, t = icp(P20, t20, C20, R0, t0, 12, 0.6)
        d, _ = t20.query(P20 @ R.T + t)
        cands.append((np.mean(d < 15), R, t))
    cands.sort(key=lambda c: -c[0])
    best = None
    for sc, R, t in cands[:6]:
        R, t = icp(P8, t8, C8, R, t, 40, 0.7)
        d, _ = t8.query(P8 @ R.T + t)
        f6, med = float(np.mean(d < 6)), float(np.median(d))
        print(f"coarse {sc:.3f} -> fit6 {f6:.3f} median {med:.1f} mm  rot {np.degrees(np.arccos(np.clip((np.trace(R)-1)/2,-1,1))):.1f} deg  t {t.round(0)}")
        if best is None or f6 > best[0]:
            best = (f6, med, R, t)
    T = np.eye(4); T[:3, :3] = best[2]; T[:3, 3] = best[3]
    json.dump({"T": T.tolist(), "fitness6": best[0], "median_mm": best[1]}, open(a.out, "w"), indent=1)
    print("BEST fit6", round(best[0], 3), "median", round(best[1], 1), "->", a.out)


if __name__ == "__main__":
    main()
