"""Level the BRZ full-car frame (raw Artec, arbitrary orientation, no ground scanned):
  1. PCA of the body: longest axis -> Y, shortest (height) -> Z.
  2. Z sign: the roof is narrower than the sills (x-extent of the top 15 % < bottom 15 %).
  3. Y sign: the nose is where the 'Front Bumper Only' part scan sits -> -Y (house convention).
  4. Tilt: plane through the four tyre contact points (lowest 0.3 % in each wheel quadrant) -> z = 0.
Writes the same {R, origin} json as level.py ('apply' with level.py).
  level2.py full.stl front_bumper.stl transform.json"""
import json, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ld = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
c = ld(sys.argv[1]); fb = ld(sys.argv[2])
cen = c.mean(0)
w, V = np.linalg.eigh(np.cov((c[::10] - cen).T))
X, Y, Z = V[:, 1], V[:, 2], V[:, 0]
q = (c - cen) @ np.array([X, Y, Z]).T
top, bot = q[q[:, 2] > np.percentile(q[:, 2], 85)], q[q[:, 2] < np.percentile(q[:, 2], 15)]
if np.ptp(top[:, 0]) > np.ptp(bot[:, 0]): Z = -Z
if (fb.mean(0) - cen) @ Y > 0: Y = -Y
X = np.cross(Y, Z)
R = np.array([X, Y, Z])
q = (c - cen) @ R.T
# tyre contacts: wheel quadrants = outer 30 % of width, y within the wheel arches (largest-gap-free clusters)
ylo, yhi = np.percentile(q[:, 1], [1, 99]); L = yhi - ylo
pts = []
for yc in (ylo + 0.21 * L, yhi - 0.20 * L):
    for s in (-1, 1):
        m = (np.abs(q[:, 1] - yc) < 0.08 * L) & (s * q[:, 0] > 0.25 * np.ptp(q[:, 0]))
        p = q[m]; lo = p[p[:, 2] < np.percentile(p[:, 2], 0.3)]
        pts.append(lo.mean(0)); print("tyre", lo.mean(0).round())
P = np.array(pts); pc = P.mean(0)
n = np.linalg.svd(P - pc)[2][2]
if n[2] < 0: n = -n
z = np.array([0, 0, 1.0]); v = np.cross(n, z); sv = np.linalg.norm(v); cth = n @ z
vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
R1 = np.eye(3) + vx + vx @ vx * ((1 - cth) / max(sv, 1e-12) ** 2)
Rf = R1 @ R
q = (c - cen) @ Rf.T
zg = ((P - 0) @ R1.T)[:, 2].mean()
origin = cen + Rf[2] * zg  # ground plane -> z=0
q = (c - origin) @ Rf.T
print("tilt corr deg", np.degrees(np.arccos(cth)).round(2), "bbox", np.percentile(q, 0.5, axis=0).round(), np.percentile(q, 99.5, axis=0).round())
json.dump({"R": Rf.tolist(), "origin": origin.tolist(), "method": "level2 PCA + front bumper + tyre plane"},
          open(sys.argv[3], "w"), indent=1)
