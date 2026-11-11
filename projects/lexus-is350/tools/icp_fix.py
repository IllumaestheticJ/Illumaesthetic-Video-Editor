"""Point-to-point ICP of a part onto the base where they overlap (<15 mm), then apply the rigid correction to the
whole part. Writes the corrected STL + transform json.   icp_fix.py base.stl part.stl out.stl out.json"""
import json, struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
base = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].mean(1).astype(float)
m = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
p = m["v"].mean(1).astype(float); rng = np.random.default_rng(0)
p = p[rng.choice(len(p), min(len(p), 200000), replace=False)]
T = cKDTree(base); d0, _ = T.query(p); q = p[d0 < 15].copy()
Rt, tt = np.eye(3), np.zeros(3)
for it in range(30):
    dd, ii = T.query(q); k = dd < 10
    A, B = q[k], base[ii[k]]; ca, cb = A.mean(0), B.mean(0)
    U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); R = Vt.T @ U.T
    if np.linalg.det(R) < 0: Vt[-1] *= -1; R = Vt.T @ U.T
    t = cb - R @ ca; q = q @ R.T + t; Rt = R @ Rt; tt = R @ tt + t
d1, _ = T.query(p @ Rt.T + tt)
print(f"overlap median {np.median(d0[d0<15]):.2f} -> {np.median(d1[d0<15]):.2f} mm; shift {np.linalg.norm(tt):.1f} mm "
      f"rot {np.degrees(np.arccos(np.clip((np.trace(Rt)-1)/2,-1,1))):.2f} deg")
v = m["v"].reshape(-1, 3).astype(float) @ Rt.T + tt
m["v"] = v.reshape(-1, 3, 3).astype(np.float32); m["n"] = (m["n"].astype(float) @ Rt.T).astype(np.float32)
with open(sys.argv[3], "wb") as f:
    f.write(b"icp_fix".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
json.dump({"R": Rt.tolist(), "t_mm": tt.tolist()}, open(sys.argv[4], "w"), indent=1)
