"""Fit the front-lid hinge (adapted from projects/huracan-evo/tools/hinge.py): axis ~X through (y_h, z_h) with a
small tilt + angle mapping the closed lid cut from the full car (hood.py) onto the open lid captured in the
'Hood Open' state scan. Output in the prepped Blender frame (m) for tools/shot.py hinges.
  hinge.py hood_closed.stl hood_open_pts.npy car_prep.json out.json"""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
hood = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].mean(1).astype(float)
openh = np.load(sys.argv[2]); openh = openh[openh[:, 2] > 760]
openh = openh[np.random.default_rng(1).choice(len(openh), min(200000, len(openh)), replace=False)]
rng = np.random.default_rng(0)
H = hood[rng.choice(len(hood), min(3000, len(hood)), replace=False)]
T = cKDTree(openh)
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix()
    c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H), distance_upper_bound=60); return np.mean(np.minimum(d, 60))
y0 = H[:, 1].max(); z0 = H[H[:, 1] > y0 - 50][:, 2].mean()
grid = [(cost([y0 + dy, z0 + dz, a, 0, 0]), a, dy, dz) for a in range(-90, 91, 5) for dy in (-150, 0, 150) for dz in (-100, 0, 100)]
grid.sort(); print("grid best", grid[:3])
best = None
for c0, a, dy, dz in grid[:3]:
    r = minimize(cost, [y0 + dy, z0 + dz, a, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.5, "fatol": 0.02})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, H))
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(d).round(2), "mm")
like = json.load(open(sys.argv[3]))
s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
out = {"p": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]),
       "fit_median_mm": float(np.median(d)), "hinge_mm": [0, float(p[0]), float(p[1])]}
json.dump(out, open(sys.argv[4], "w"), indent=1); print(out)
