"""MR2 SW20: level.py's RANSAC locked onto the cabin floor (car is on stands, the real ground is ~350 mm lower).
Refit the ground plane on up-facing triangles below z=-250 in the first-pass frame, compose with level.json
and re-yaw the long axis. usage: relevel.py level.json first_pass_levelled.stl out.json"""
import json, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
T = json.load(open(sys.argv[1])); R0 = np.array(T["R"]); o0 = np.array(T["origin"])
m = np.fromfile(sys.argv[2], dtype=TRI, offset=84); c = m["v"].mean(1).astype(float)
g = c[(c[:, 2] < -250) & (m["n"][:, 2] > 0.9)]
rng = np.random.default_rng(0); best = (0, None, None)
for _ in range(2000):
    p = g[rng.choice(len(g), 3, replace=False)]; n = np.cross(p[1] - p[0], p[2] - p[0]); L = np.linalg.norm(n)
    if L < 1e-6: continue
    n /= L; n = n if n[2] > 0 else -n
    if n[2] < 0.95: continue
    inl = np.abs((g - p[0]) @ n) < 5
    if inl.sum() > best[0]: best = (inl.sum(), n, p[0])
P = g[np.abs((g - best[2]) @ best[1]) < 5]; cen = P.mean(0)
n = np.linalg.svd(P - cen, full_matrices=False)[2][2]; n = n if n[2] > 0 else -n
z = np.array([0, 0, 1.0]); v = np.cross(n, z); s = np.linalg.norm(v); ct = n @ z
vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
R1 = np.eye(3) + vx + vx @ vx * ((1 - ct) / s ** 2)
q = (c - cen) @ R1.T; body = q[q[:, 2] > 600]
xy = body[:, :2] - body[:, :2].mean(0); e = np.linalg.eigh(np.cov(xy.T))[1][:, -1]; ang = np.arctan2(e[0], e[1])
Rz = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
Rn = Rz @ R1
# full transform: x' = Rn((R0(x-o0)) - cen) = Rn R0 (x - o0 - R0^T cen)
R = Rn @ R0; o = o0 + R0.T @ cen
q = (c - cen) @ Rn.T; b = q[q[:, 2] > 400]
print("ground inliers", len(P), "normal", n.round(4), "tilt deg", np.degrees(np.arccos(n[2])).round(2))
print("body x", np.percentile(b[:, 0], [0.5, 99.5]).round(), "y", np.percentile(b[:, 1], [0.5, 99.5]).round(), "z max", np.percentile(q[:, 2], 99.9).round())
json.dump({"R": R.tolist(), "origin": o.tolist(), "ground_inliers": int(len(P)), "note": "relevel.py on true ground"}, open(sys.argv[3], "w"), indent=1)
