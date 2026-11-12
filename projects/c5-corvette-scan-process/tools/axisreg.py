"""Register a scan whose axes are permuted/flipped vs the car: try all 24 proper rotations of the axes, align bbox
centres of the part to a car region, coarse trimmed ICP, keep the best; then fine ICP. Saves a 4x4 (part mm -> car mm).
  axisreg.py car.stl part.stl out.json [--car-ymax mm]"""
import sys, json, itertools, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].mean(1).astype(float)
part = np.fromfile(sys.argv[2], dtype=TRI, offset=84)["v"].mean(1).astype(float)
ymax = float(sys.argv[5]) if len(sys.argv) > 5 else 1e9
carR = car[car[:, 1] < ymax]; rng = np.random.default_rng(0)
C = carR[rng.choice(len(carR), min(60000, len(carR)), replace=False)]; tree = cKDTree(C)
Pp = part[rng.choice(len(part), min(8000, len(part)), replace=False)]
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb))
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); R = Vt.T @ D @ U.T; return R, cb - R @ ca
def icp(P, R, t, gate, it=40):
    for _ in range(it):
        s = P @ R.T + t; d, j = tree.query(s, distance_upper_bound=gate); ok = np.isfinite(d)
        if ok.sum() < 50: return R, t, 0, 1e9
        dR, dt = kabsch(s[ok], C[j[ok]]); R, t = dR @ R, dR @ t + dt
    d, _ = tree.query(P @ R.T + t); return R, t, float(np.mean(d < 6)), float(np.median(d))
best = None
for perm in itertools.permutations(range(3)):
    for sg in itertools.product([1, -1], repeat=3):
        R0 = np.zeros((3, 3)); [R0.__setitem__((i, perm[i]), sg[i]) for i in range(3)]
        if np.linalg.det(R0) < 0: continue
        q = Pp @ R0.T
        # align bbox: x centre, y front (min y), z bottom
        t0 = np.array([C[:, 0].mean() - (q[:, 0].min() + q[:, 0].max()) / 2, C[:, 1].min() - q[:, 1].min(), C[:, 2].min() - q[:, 2].min()])
        R, t, fit, med = icp(Pp, R0, t0, 150, 30)
        R, t, fit, med = icp(Pp, R, t, 30, 30)
        if best is None or fit > best[2]: best = (R, t, fit, med, perm, sg)
        print(perm, sg, "fit<6mm %.3f med %.1f" % (fit, med))
R, t, fit, med, perm, sg = best
R, t, fit, med = icp(Pp, R, t, 8, 60)
print("BEST", perm, sg, "fit %.3f median %.1f mm" % (fit, med))
T = np.eye(4); T[:3, :3] = R; T[:3, 3] = t
json.dump({"T_part_to_car_mm": T.tolist(), "fit6mm": fit, "median_mm": med}, open(sys.argv[3], "w"), indent=1)
