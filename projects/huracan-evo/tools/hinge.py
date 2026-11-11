"""Fit the front-hood hinge: find axis (through (x?, y_h, z_h), direction ~X, small tilt) + angle that maps the
closed 'Hood Only' scan onto the propped-open hood captured in 'All Parts Removed'. Output in the prepped Blender
frame (m) for tools/shot.py hinges."""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
C = "/home/user/media/huracan-evo/clean/"
hood = np.fromfile(C + "Hood_Only.stl", dtype=TRI, offset=84)["v"].mean(1).astype(float)
car = np.fromfile(C + "car.stl", dtype=TRI, offset=84)["v"].mean(1)
apr = np.fromfile(C + "All_Parts_Removed.stl", dtype=TRI, offset=84)["v"].mean(1).astype(float)
# open hood = APR points above the car roofline in the front half (same rule as composite.py)
cell = 40.0
k = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k(car[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, car[:, 2])
ka = k(apr[:, :2]); i = np.clip(np.searchsorted(u, ka), 0, len(u) - 1); roof = np.where(u[i] == ka, top[i], -1e9)
openh = apr[(apr[:, 2] > roof + 30) & (apr[:, 1] < 0)]
rng = np.random.default_rng(0)
H = hood[rng.choice(len(hood), min(2500, len(hood)), replace=False)]
T = cKDTree(openh)
print("hood y range", H[:, 1].min().round(), H[:, 1].max().round(), "open pts", len(openh))
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix()
    c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H)); return np.mean(np.minimum(d, 60))
y0 = H[:, 1].max(); z0 = H[H[:, 1] > y0 - 50][:, 2].mean()
grid = [(cost([y0 + dy, z0 + dz, a, 0, 0]), a, dy, dz) for a in range(-80, 81, 5) for dy in (-150, 0, 150) for dz in (-100, 0, 100)]
grid.sort(); print("grid best", grid[:3])
best = None
for c0, a, dy, dz in grid[:3]:
    r = minimize(cost, [y0 + dy, z0 + dz, a, 0, 0], method="Nelder-Mead", options={"maxiter": 800, "xatol": 0.5, "fatol": 0.02})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, H))
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(d).round(2), "mm")
like = json.load(open("/home/user/media/work/huracan/blend/car.json"))
s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
out = {"p": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]),
       "fit_median_mm": float(np.median(d))}
json.dump(out, open(sys.argv[1], "w"), indent=1); print(out)
