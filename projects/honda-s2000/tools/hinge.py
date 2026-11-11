"""Fit the trunk-lid hinge: axis ~X through (y_h, z_h) + angle that maps the closed lid (cut from the car) onto the
propped-open lid captured in the trunk state scan (points above the closed deck). Adapted from projects/huracan-evo/tools/hinge.py.
Output in the prepped Blender frame (m) for tools/shot.py parts (pivot + rot X).
    python projects/honda-s2000/tools/hinge.py lid_lvl.stl trunk_lvl.stl car4.json out.json"""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
lid = np.fromfile(sys.argv[1], dtype=TRI, offset=84)["v"].mean(1).astype(float)
tr = np.fromfile(sys.argv[2], dtype=TRI, offset=84)["v"].mean(1).astype(float)
openl = tr[(tr[:, 2] > 880) & (np.abs(tr[:, 0]) < 620)]
H = lid[np.random.default_rng(0).choice(len(lid), 3000, replace=False)]
T = cKDTree(openl)
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H)); return np.mean(np.minimum(d, 60))
y0 = H[:, 1].min(); z0 = H[H[:, 1] < y0 + 50][:, 2].mean()
grid = sorted((cost([y0 + dy, z0 + dz, a, 0, 0]), a, dy, dz) for a in range(-110, 111, 5) for dy in (-100, 0, 100) for dz in (-100, 0, 100))
print("open pts", len(openl), "grid best", grid[:3])
best = None
for c0, a, dy, dz in grid[:3]:
    r = minimize(cost, [y0 + dy, z0 + dz, a, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.5, "fatol": 0.02})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, H))
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(d).round(2), "mm, <5mm", round(np.mean(d < 5) * 100), "%")
like = json.load(open(sys.argv[3])); s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
out = {"pivot_prep_m": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]), "fit_median_mm": float(np.median(d))}
json.dump(out, open(sys.argv[4], "w"), indent=1); print(out)
