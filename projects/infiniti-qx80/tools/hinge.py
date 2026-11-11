"""Fit a hinge that closes a panel captured open in a state scan onto the full car (levelled mm frame).
  hinge.py car.stl state.stl axis(x|z) out.json [--box xmin,xmax,ymin,ymax,zmin,zmax]
moved = state-scan centroids > 25 mm from the car (and inside --box) = the panel in its open position.
Search: rotation about an axis ~X (hood) or ~Z (door) through (a,b) in the other two coords; cost = mean clipped
distance of the rotated panel to the car. Writes axis point/direction/angle (mm, level frame) + the closed panel's
car triangles mask count."""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car_p, st_p, axis, out = sys.argv[1:5]
box = None
if "--box" in sys.argv: box = [float(v) for v in sys.argv[sys.argv.index("--box") + 1].split(",")]
car = np.fromfile(car_p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
if box: car = car[(car[:, 0] > box[0] - 300) & (car[:, 0] < box[1] + 300) & (car[:, 1] > box[2] - 300) & (car[:, 1] < box[3] + 300) & (car[:, 2] > box[4] - 300)]
st = np.fromfile(st_p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
T = cKDTree(car)
d, _ = T.query(st, distance_upper_bound=30)
mv = st[d > 25]
if box: mv = mv[(mv[:, 0] > box[0]) & (mv[:, 0] < box[1]) & (mv[:, 1] > box[2]) & (mv[:, 1] < box[3]) & (mv[:, 2] > box[4]) & (mv[:, 2] < box[5])]
rng = np.random.default_rng(0); H = mv[rng.choice(len(mv), min(2000, len(mv)), replace=False)]
print("moved pts", len(mv), "bbox", mv.min(0).round(), mv.max(0).round())
def R_of(p):
    a, b, ang, t1, t2 = p
    if axis == "x": ax = np.array([1.0, t1, t2]); c = np.array([0, a, b])
    else: ax = np.array([t1, t2, 1.0]); c = np.array([a, b, 0])
    ax /= np.linalg.norm(ax); return Rot.from_rotvec(np.radians(ang) * ax).as_matrix(), c, ax
def xf(p, P): R, c, _ = R_of(p); return (P - c) @ R.T + c
def cost(p): dd, _ = T.query(xf(p, H), distance_upper_bound=80); return np.mean(np.minimum(dd, 80))
if axis == "x":  # hood: hinge near its rear (min y) edge
    y0 = H[:, 1].min(); z0 = H[H[:, 1] < y0 + 80][:, 2].mean(); seeds = [(y0 + dy, z0 + dz) for dy in (-150, 0, 150) for dz in (-150, 0, 150)]
else:            # door: hinge at its front (max y) edge, x near the body side
    y0 = H[:, 1].max(); x0 = H[H[:, 1] > y0 - 80][:, 0].mean(); seeds = [(x0 + dx, y0 + dy) for dx in (-200, -100, 0) for dy in (-150, 0, 150)]
grid = sorted((cost([a, b, ang, 0, 0]), a, b, ang) for ang in range(-85, 86, 5) for a, b in seeds)
print("grid best", [tuple(round(v, 1) for v in g) for g in grid[:3]])
best = None
for c0, a, b, ang in grid[:4]:
    r = minimize(cost, [a, b, ang, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.3, "fatol": 0.01})
    if best is None or r.fun < best.fun: best = r
p = best.x; dd, _ = T.query(xf(p, H), distance_upper_bound=200); R, c, ax = R_of(p)
res = {"axis": axis, "pivot_mm": c.tolist(), "dir": ax.tolist(), "close_deg": float(p[2]), "fit_median_mm": float(np.median(dd)),
       "fit_frac_within_10mm": float((dd < 10).mean())}
json.dump(res, open(out, "w"), indent=1); print(res)
