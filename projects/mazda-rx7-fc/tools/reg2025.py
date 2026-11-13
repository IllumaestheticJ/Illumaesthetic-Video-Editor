"""Bring 'FC3S Full Car.stl' (2025, Drive Mazda RX7 (FC3S) folder: a stock FC3S on mesh wheels = the scan the
illumaesthetic.com FC3S listing's 360 viewer shows) into the S5 levelled frame (mm). It is stored upside down with the
length along X: try the 4 flip/turn hypotheses, ICP each onto the S5 car (same model, different car), keep the best.
    reg2025.py car2025.stl s5_lvl_car.stl out.stl out.json"""
import sys, json, struct, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __import__("os").path.dirname(__file__))
from icp import icp
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
src, dst, out, oj = sys.argv[1:5]
m = np.fromfile(src, dtype=TRI, offset=84); c = m["v"].mean(1).astype(float)
car = np.fromfile(dst, dtype=TRI, offset=84)["v"].mean(1).astype(float); T = cKDTree(car[::3])
flip = np.diag([1.0, -1.0, -1.0])                       # 180 deg about X (upside down)
best = None
for k in range(4):
    a = np.radians(90 * k); Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    R0 = Rz @ flip; Q = c[::6] @ R0.T; t0 = car.mean(0) - Q.mean(0); t0[2] = car[:, 2].min() - Q[:, 2].min()
    R, t, med, p90 = icp(Q + t0, T, 60, 0.7)
    print(f"turn {90*k:3d}: median {med:.1f} mm p90 {p90:.1f}")
    if best is None or med < best[0]:
        best = (med, R @ R0, R @ t0 + t, p90)
med, R, t, p90 = best
v = m["v"].reshape(-1, 3).astype(float) @ R.T + t
m["v"] = v.reshape(-1, 3, 3).astype(np.float32); m["n"] = (m["n"].astype(float) @ R.T).astype(np.float32)
with open(out, "wb") as f:
    f.write(b"FC3S 2025 scan in S5 levelled frame".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
json.dump({"R": R.tolist(), "t": t.tolist(), "icp_median_mm": med, "icp_p90_mm": p90}, open(oj, "w"), indent=1)
print("best median", round(med, 1), "->", out)
