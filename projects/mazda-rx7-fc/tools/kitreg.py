"""Place the HertLife FC3S time-attack kit (FC3_TA.obj, KeyShot, cm, Y up) in the S5 levelled frame (mm).
  1. kit -> HertLife scan frame: axis swap (x, -z, y)*10, then ICP onto the 'bodykit' concept that Review/OLD/
     'FC3S_TA_with scan.obj' stores together with FC3S_scan_1 (OBJ (x,y,z) = STL (x, z, -y)).
  2. HertLife scan -> S5 levelled frame (lvl/car_4mm_clean.stl): 180 deg about Z (HertLife front = -Y) + ICP.
Writes kit_xform.json: M (4x4) kit-cm -> levelled-mm, with both ICP residuals.
    kitreg.py kit_dir lvl_car.stl out.json"""
import sys, json, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __import__("os").path.dirname(__file__))
from icp import icp
K, CAR, OUT = sys.argv[1:4]
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
w = np.load(f"{K}/ta_with_scan.npz"); V, F, O = w["V"], w["F"], w["obj"]
toS = lambda P: np.c_[P[:, 0], -P[:, 2], P[:, 1]]
tri = toS(V)[F[O == 0]]
rng = np.random.default_rng(0); A = np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1) / 2
n = 400000; ti = rng.choice(len(tri), n, p=A / A.sum()); r1, r2 = rng.random(n), rng.random(n); s = np.sqrt(r1)
bk = (1 - s)[:, None] * tri[ti, 0] + (s * (1 - r2))[:, None] * tri[ti, 1] + (s * r2)[:, None] * tri[ti, 2]
bk = np.r_[bk, bk * [-1, 1, 1]]
d = np.load(f"{K}/ta_parts.npz"); KV, KF, part = d["V"], d["F"], d["part"]
P = KV[np.unique(KF[np.isin(part, [16, 17, 84, 20, 55])])]
S0 = np.array([[10, 0, 0], [0, 0, -10], [0, 10, 0.0]])         # kit cm (Y up, +Z front) -> HertLife mm
Q = P @ S0.T; c0 = np.r_[bk.mean(0)[:2] - Q.mean(0)[:2], 0]
R1, t1, m1, p1 = icp((Q + c0)[::3], cKDTree(bk), 60, 0.7)
M1 = np.eye(4); M1[:3, :3] = R1 @ S0; M1[:3, 3] = R1 @ c0 + t1
print(f"kit -> HertLife: median {m1:.1f} mm p90 {p1:.1f}")
hs = toS(V)[F[O == 1]].mean(1)                                   # HertLife scan (from the same OBJ, same frame)
car = np.fromfile(CAR, dtype=TRI, offset=84)["v"].mean(1).astype(float)
Tc = cKDTree(car[::3])
Rz = np.diag([-1.0, -1.0, 1.0])
H = hs[::4] @ Rz.T; c1 = car.mean(0) - H.mean(0)
R2, t2, m2, p2 = icp(H + c1, Tc, 80, 0.8)
M2 = np.eye(4); M2[:3, :3] = R2 @ Rz; M2[:3, 3] = R2 @ c1 + t2
print(f"HertLife -> S5 levelled: median {m2:.2f} mm p90 {p2:.1f}")
M = M2 @ M1
json.dump({"M": M.tolist(), "kit_to_hertlife": M1.tolist(), "hertlife_to_lvl": M2.tolist(),
           "icp_kit_mm": [m1, p1], "icp_scan_mm": [m2, p2]}, open(OUT, "w"), indent=1)
print("->", OUT)
