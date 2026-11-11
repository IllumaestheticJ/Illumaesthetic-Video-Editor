"""Registration check of part/state scans against the full car (adapted from projects/huracan-evo/tools/regcheck.py).
  regcheck.py car.stl part1.stl part2.stl ...      (all levelled, mm)
Per part: overlap (<15 mm from the car), median distance on the overlap, and the rigid correction a
point-to-point ICP on the overlap would apply (reported, written to <part>.icp.json; not applied)."""
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p, n=600000):
    c = np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    c = c[c[:, 2] > 40]
    if len(c) > n: c = c[np.random.default_rng(0).choice(len(c), n, replace=False)]
    return c
car = load(sys.argv[1], 2_000_000); tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f)
    dist, _ = tree.query(p)
    near = dist < 15
    q = p[near].copy(); Rt = np.eye(3); tt = np.zeros(3)
    for _ in range(20):
        dd, ii = tree.query(q); m = dd < 10
        A, B = q[m], car[ii[m]]
        ca, cb = A.mean(0), B.mean(0); H = (A - ca).T @ (B - cb)
        U, S, Vt = np.linalg.svd(H); R = Vt.T @ U.T
        if np.linalg.det(R) < 0: Vt[-1] *= -1; R = Vt.T @ U.T
        t = cb - R @ ca; q = q @ R.T + t; Rt = R @ Rt; tt = R @ tt + t
    ang = np.degrees(np.arccos(np.clip((np.trace(Rt) - 1) / 2, -1, 1)))
    d2, _ = tree.query(q)
    json.dump({"R": Rt.tolist(), "t": tt.tolist()}, open(f[:-4] + ".icp.json", "w"))
    print(f"{os.path.basename(f)[:-4]:40s} n={len(p):7d} overlap<15mm={near.mean()*100:5.1f}%  median={np.median(dist[near]):5.2f}mm"
          f"  p90all={np.percentile(dist,90):6.1f}mm | ICP corr: {np.linalg.norm(tt):5.1f}mm {ang:4.2f}deg -> median {np.median(d2):5.2f}mm", flush=True)
