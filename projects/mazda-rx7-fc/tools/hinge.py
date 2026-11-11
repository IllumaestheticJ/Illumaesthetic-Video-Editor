"""Fit the hood hinge (adapted from huracan-evo/tools/hinge.py): axis ~X through (y_h, z_h) + angle that maps the
closed hood (hood_v2) onto the propped-open hood captured in 'Hood Up'. Levelled mm in, prepped Blender frame out.
    python projects/mazda-rx7-fc/tools/hinge.py hood_v2.stl hup_clean.stl car_4mm_clean.stl car4.json out.json"""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ld = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
hood, hup, car = ld(sys.argv[1]), ld(sys.argv[2]), ld(sys.argv[3])
# open hood = Hood Up points well above the closed car's top surface (40 mm grid), front half
cell = 40.0
k = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k(car[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, car[:, 2])
ka = k(hup[:, :2]); i = np.clip(np.searchsorted(u, ka), 0, len(u) - 1); roof = np.where(u[i] == ka, top[i], -1e9)
openh = hup[(hup[:, 2] > roof + 40) & (hup[:, 1] > 500)]
rng = np.random.default_rng(0)
H = hood[rng.choice(len(hood), 1500, replace=False)]
openh = openh[rng.choice(len(openh), min(150000, len(openh)), replace=False)]
T = cKDTree(openh)
print("open pts", len(openh), "hood y", H[:, 1].min().round(), H[:, 1].max().round())
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H), distance_upper_bound=60); d[~np.isfinite(d)] = 60; return np.mean(np.minimum(d, 60))
y0 = H[:, 1].min(); z0 = H[H[:, 1] < y0 + 50][:, 2].mean()
grid = sorted((cost([y0 + dy, z0 + dz, a, 0, 0]), a, dy, dz) for a in range(-80, 81, 4) for dy in (-100, 0, 100) for dz in (-80, 0, 80))
print("grid best", grid[:3])
best = None
for c0, a, dy, dz in grid[:3]:
    r = minimize(cost, [y0 + dy, z0 + dz, a, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.3, "fatol": 0.01})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, H))
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(d).round(2), "mm")
like = json.load(open(sys.argv[4])); s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
out = {"p": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]), "fit_median_mm": float(np.median(d))}
json.dump(out, open(sys.argv[5], "w"), indent=1); print(out)
