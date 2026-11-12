"""Register the designed bodykit (CAD STLs in the designer's car-aligned frame: front at -Y, z=0 ground, mm)
into the raw Artec scan frame. Initial yaw from the car's forward axis, translation from the stock bumper extents,
then trimmed ICP (yaw + translation only, nearest --keep fraction) of front+rear kit bumpers against the full car.
Writes the transformed STLs and the 4x4 matrix.
    python tools/kit_register.py full.stl out_dir kitfront.stl kitrear.stl"""
import sys, json, math, numpy as np
from scipy.spatial import cKDTree
T = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
full, out, kf, kr = sys.argv[1:5]
F = np.fromfile(full, dtype=T, offset=84)["v"].mean(1).astype(np.float64)
K = [np.fromfile(p, dtype=T, offset=84) for p in (kf, kr)]
P = np.concatenate([k["v"].reshape(-1, 3) for k in K]).astype(np.float64)[::7]
f = np.array([0.258, 0.966]); f /= np.linalg.norm(f)
def Rz(a): c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
yaw = math.atan2(f[0], -f[1])           # kit forward (0,-1) -> scan forward
R = Rz(yaw)
# initial translation: kit centre (x=0, y mid of front/rear extremes) -> car centre along f; ground z
u = F[:, 0] * f[0] + F[:, 1] * f[1]; r = np.array([f[1], -f[0]]); v = F[:, 0] * r[0] + F[:, 1] * r[1]
cu, cv = (np.percentile(u, 0.2) + np.percentile(u, 99.8)) / 2, (np.percentile(v, 0.5) + np.percentile(v, 99.5)) / 2
kc = np.array([0.0, (P[:, 1].min() + P[:, 1].max()) / 2, 0.0])
t = np.array([cu * f[0] + cv * r[0], cu * f[1] + cv * r[1], np.percentile(F[:, 2], 0.05)]) - R @ kc
tree = cKDTree(F)
def apply(R, t, X): return X @ R.T + t
for keep in (0.5, 0.4, 0.3, 0.3):
    for it in range(15):
        Q = apply(R, t, P); d, i = tree.query(Q, distance_upper_bound=150)
        ok = np.isfinite(d); thr = np.quantile(d[ok], keep); m = ok & (d <= thr)
        A, B = Q[m], F[i[m]]
        ca, cb = A.mean(0), B.mean(0); H = ((A - ca)[:, :2]).T @ ((B - cb)[:, :2])
        da = math.atan2(H[0, 1] - H[1, 0], H[0, 0] + H[1, 1])
        dR = Rz(da); R = dR @ R; t = dR @ (t - ca) + cb
    print(f"keep {keep}: median {np.median(d[m]):.1f} mm, yaw {math.degrees(math.atan2(R[1,0],R[0,0])):.2f} deg, t {t.round(1)}")
M = np.eye(4); M[:3, :3] = R; M[:3, 3] = t
json.dump({"matrix": M.tolist()}, open(f"{out}/kit_to_scan.json", "w"), indent=1)
for name, k in zip(("kit_front", "kit_rear"), K):
    o = k.copy(); o["v"] = (k["v"].reshape(-1, 3).astype(np.float64) @ R.T + t).reshape(-1, 3, 3).astype(np.float32)
    o["n"] = (k["n"].astype(np.float64) @ R.T).astype(np.float32)
    with open(f"{out}/{name}.stl", "wb") as fh:
        fh.write(b"tools/kit_register.py".ljust(80)); fh.write(np.uint32(len(o)).tobytes()); o.tofile(fh)
    print(name, len(o))
