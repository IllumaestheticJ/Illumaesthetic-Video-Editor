"""Check / refine part-scan registration against the base car (trimmed point-to-point ICP on
triangle centroids, mm). Prints residuals before/after and the rigid transform found.
    python projects/a90-supra/tools/register.py car_4mm.stl part_3mm.stl [--max 15] [--save T.json]
"""
import argparse, json
import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def cent(p):
    return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)


def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0)
    H = (A - ca).T @ (B - cb)
    U, S, Vt = np.linalg.svd(H)
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
    R = Vt.T @ D @ U.T
    return R, cb - R @ ca


def icp(src, tree, dst, maxd=15.0, iters=40):
    R, t = np.eye(3), np.zeros(3)
    for i in range(iters):
        s = src @ R.T + t
        d, j = tree.query(s, distance_upper_bound=maxd)
        ok = np.isfinite(d)
        if ok.sum() < 100:
            break
        dR, dt = kabsch(s[ok], dst[j[ok]])
        R, t = dR @ R, dR @ t + dt
        if np.linalg.norm(dt) < 0.01:
            break
    return R, t


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("car"); ap.add_argument("part")
    ap.add_argument("--max", type=float, default=15)
    ap.add_argument("--save")
    a = ap.parse_args()
    car = cent(a.car); tree = cKDTree(car)
    p = cent(a.part)[::5]
    d0, _ = tree.query(p)
    R, t = icp(p, tree, car, a.max)
    d1, _ = tree.query(p @ R.T + t)
    ang = np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
    f = lambda d: f"p50={np.median(d):.1f} p75={np.percentile(d,75):.1f} <3mm={np.mean(d<3)*100:.0f}%"
    print(f"{a.part.split('/')[-1]:22s} before {f(d0)} | after {f(d1)} | shift={np.round(t,1)} rot={ang:.2f}deg")
    if a.save:
        json.dump({"R": R.tolist(), "t_mm": t.tolist(), "rot_deg": ang}, open(a.save, "w"), indent=1)
