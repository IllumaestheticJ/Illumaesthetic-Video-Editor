"""Register a roof/panel part by PCA: part axes (long, mid, thin) -> car (x width, y length, z up); try the 4 proper
sign flips x several y positions along the roof, trimmed ICP on upward-facing part triangles vs the car roof.
  pcareg.py car_roof.stl part.stl out.json"""
import sys, json, itertools, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].mean(1).astype(float); tree = cKDTree(car)
pv = np.fromfile(sys.argv[2], dtype=TRI, offset=84)["v"].astype(float); P = pv.mean(1)
mu = P.mean(0); U, S, Vt = np.linalg.svd(P[np.random.default_rng(0).choice(len(P), 20000)] - mu, full_matrices=False)
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb))
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); R = Vt.T @ D @ U.T; return R, cb - R @ ca
best = None
for sx, sy in itertools.product([1, -1], repeat=2):
    B = np.vstack([sx * Vt[0], sy * Vt[1], np.cross(sx * Vt[0], sy * Vt[1])])  # rows: part dirs -> car x,y,z
    R0 = B; q = (P - mu) @ R0.T
    nrm = np.cross(pv[:, 1] - pv[:, 0], pv[:, 2] - pv[:, 0]) @ R0.T; up = nrm[:, 2] > 0
    Q = q[up][::40]
    for y0 in np.arange(-300, 500, 200):
        t = np.array([car[:, 0].mean(), y0, car[:, 2].max() - q[:, 2].max()]); R = np.eye(3)
        for gate in (120, 40, 15, 8):
            for _ in range(15):
                s = Q @ R.T + t; d, j = tree.query(s, distance_upper_bound=gate); ok = np.isfinite(d)
                if ok.sum() < 100: break
                dR, dt = kabsch(s[ok], car[j[ok]]); R, t = dR @ R, dR @ t + dt
        d, _ = tree.query(Q @ R.T + t); fit = np.mean(d < 4); med = np.median(d)
        if best is None or fit > best[0]: best = (fit, med, R @ R0, t - (R @ R0) @ mu * 0 + 0, R, R0, t)
fit, med, _, _, R, R0, t = best
Rt = R @ R0; tt = R @ (-R0 @ mu) + t   # x -> R(R0(x-mu)) + t
T = np.eye(4); T[:3, :3] = Rt; T[:3, 3] = tt
print("BEST fit<4mm %.3f median %.1f mm" % (fit, med))
json.dump({"T_part_to_car_mm": T.tolist(), "fit4mm": fit, "median_mm": med}, open(sys.argv[3], "w"), indent=1)
