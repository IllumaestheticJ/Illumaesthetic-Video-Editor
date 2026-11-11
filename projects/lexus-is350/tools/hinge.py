"""Fit the hood hinge: axis ~X through (y_h, z_h) (+ small tilt) and angle mapping the closed hood (extracted from the
full car, tools/hood.py) onto the 'Hood Open' scan (which is only the propped-open hood). Output in the prepped Blender
frame (m) for shot.py parts: pivot + rotation about X.   hinge.py hood.stl hood_open.stl car4.json out.json"""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
rng = np.random.default_rng(0)
hood, op = L(sys.argv[1]), L(sys.argv[2])
H = hood[rng.choice(len(hood), 3000, replace=False)]
O = op[rng.choice(len(op), 300000, replace=False)]
T = cKDTree(O)
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H)); return np.mean(np.minimum(d, 60))
y0 = H[:, 1].max(); z0 = H[H[:, 1] > y0 - 60][:, 2].mean()
print("hood rear edge y,z", round(y0), round(z0))
grid = sorted((cost([y0 + dy, z0 + dz, a, 0, 0]), a, dy, dz) for a in range(-90, 0, 4) for dy in (-150, -50, 50, 150) for dz in (-100, 0, 100))
print("grid best", [tuple(round(x, 1) for x in g) for g in grid[:3]])
best = None
for c0, a, dy, dz in grid[:3]:
    r = minimize(cost, [y0 + dy, z0 + dz, a, 0, 0], method="Nelder-Mead", options={"maxiter": 600, "xatol": 0.3, "fatol": 0.01})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, H))
print("fit", p.round(3), "median", np.median(d).round(2), "mm  p90", np.percentile(d, 90).round(1))
like = json.load(open(sys.argv[3])); s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
out = {"pivot": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]),
       "fit_median_mm": float(np.median(d)), "fit_p90_mm": float(np.percentile(d, 90))}
json.dump(out, open(sys.argv[4], "w"), indent=1); print(out)
