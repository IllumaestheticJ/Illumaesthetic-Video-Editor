"""Rigid trimmed ICP: register a scan of the same car from another session (e.g. the 2025 full car) to the
reference frame (levelled July Interior scan). Tries yaw 0/180 from bbox-centre alignment, keeps the best.
usage: icp_register.py moving.stl reference.stl out_transform.json [out_moved.stl]"""
import json, struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
mv = np.fromfile(sys.argv[1], dtype=TRI, offset=84); rf = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
rng = np.random.default_rng(0)
M = mv["v"].mean(1).astype(float); R_ = rf["v"].mean(1).astype(float)
def body(c):  # upper body shell: above wheel hubs, drops ground / stands
    z0 = np.percentile(c[:, 2], 1); return c[c[:, 2] > z0 + 350]
Mb = body(M); Rb = body(R_)
Mb = Mb[rng.choice(len(Mb), min(60000, len(Mb)), replace=False)]
T = cKDTree(Rb[rng.choice(len(Rb), min(400000, len(Rb)), replace=False)])
def centre(c): return (np.percentile(c, 2, 0) + np.percentile(c, 98, 0)) / 2
def icp(R, t, iters=60):
    for it in range(iters):
        P = Mb @ R.T + t; d, i = T.query(P)
        thr = max(8.0, np.percentile(d, 70)) if it < 30 else 15.0
        k = d < thr; A = Mb[k]; B = T.data[i[k]]
        ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb))
        D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); R = Vt.T @ D @ U.T; t = cb - R @ ca
    d, _ = T.query(Mb @ R.T + t)
    return R, t, np.median(d), (d < 10).mean()
best = None
for yaw in (0, 180):
    a = np.radians(yaw); R0 = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1.0]])
    t0 = centre(Rb) - R0 @ centre(Mb)
    R, t, med, inl = icp(R0, t0)
    print(f"yaw {yaw}: median {med:.1f} mm, within 10 mm {inl:.2f}")
    if best is None or med < best[2]: best = (R, t, med, inl, yaw)
R, t, med, inl, yaw = best
print("best yaw", yaw, "median", round(med, 2), "inliers<10mm", round(inl, 3))
json.dump({"R": R.tolist(), "t": t.tolist(), "median_mm": med, "inlier10": inl}, open(sys.argv[3], "w"), indent=1)
if len(sys.argv) > 4:
    o = mv.copy(); o["v"] = (mv["v"].reshape(-1, 3) @ R.T + t).reshape(-1, 3, 3).astype(np.float32); o["n"] = (mv["n"] @ R.T).astype(np.float32)
    with open(sys.argv[4], "wb") as f: f.write(b"ive icp".ljust(80)); f.write(struct.pack("<I", len(o))); o.tofile(f)
