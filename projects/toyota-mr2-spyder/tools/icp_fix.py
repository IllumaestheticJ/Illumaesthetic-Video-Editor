"""Small rigid ICP correction for a scan that is already near the car frame (second-session offset of a few mm):
trimmed point-to-point ICP of the part's points within NEAR mm of the car, optionally inside a Y band of the part.
Writes {"T": 4x4} for tools/xform.py.   icp_fix.py car_L.stl part_L.stl out_T.json [--y y0,y1] [--near 25]"""
import argparse, json, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("part"); ap.add_argument("out")
ap.add_argument("--y"); ap.add_argument("--near", type=float, default=25)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
car = L(a.car); P = L(a.part)[::3]
if a.y:
    y0, y1 = map(float, a.y.split(",")); P = P[(P[:, 1] > y0) & (P[:, 1] < y1)]
tree = cKDTree(car); T = np.eye(4)
for it in range(40):
    Q = P @ T[:3, :3].T + T[:3, 3]; d, j = tree.query(Q)
    near = a.near if it > 5 else a.near * 1.6
    m = d < near; m &= d <= np.quantile(d[m], 0.85)
    A, B = Q[m], car[j[m]]; ma, mb = A.mean(0), B.mean(0)
    U, _, Vt = np.linalg.svd((B - mb).T @ (A - ma)); S = np.eye(3); S[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ S @ Vt; D = np.eye(4); D[:3, :3] = R; D[:3, 3] = mb - R @ ma; T = D @ T
    if it in (0, 39): print(f"iter {it}: {m.sum()} pairs, median {np.median(d[m]):.2f} mm")
ang = np.degrees(np.arccos(np.clip((np.trace(T[:3, :3]) - 1) / 2, -1, 1)))
print(f"correction: {np.linalg.norm(T[:3,3]):.1f} mm, {ang:.2f} deg")
json.dump({"T": T.tolist()}, open(a.out, "w"))
