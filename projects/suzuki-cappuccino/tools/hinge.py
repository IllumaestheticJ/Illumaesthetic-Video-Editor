"""Fit a lid hinge (axis ~X through (y_h, z_h), small tilt) + angle mapping the closed lid (cut from the full car by
lids.py) onto the open lid captured in a state scan (state points > 30 mm above the car's own surface, per 40 mm cell).
Tries hinge lines at both the lid's front and rear edge. Output in the prepped Blender frame (m) for tools/shot.py.
  hinge.py lid.stl state.stl car.stl car.json out.json ymin ymax      (ymin/ymax mm: zone of the open lid)"""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
lid, st, car = load(sys.argv[1]), load(sys.argv[2]), load(sys.argv[3])
like, out, ymin, ymax = json.load(open(sys.argv[4])), sys.argv[5], float(sys.argv[6]), float(sys.argv[7])
cell = 40.0
k = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k(car[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, car[:, 2])
ka = k(st[:, :2]); i = np.clip(np.searchsorted(u, ka), 0, len(u) - 1); roof = np.where(u[i] == ka, top[i], -1e9)
openl = st[(st[:, 2] > roof + 30) & (st[:, 1] > ymin) & (st[:, 1] < ymax) & (st[:, 2] > 600)]
rng = np.random.default_rng(0)
H = lid[rng.choice(len(lid), min(3000, len(lid)), replace=False)]
T = cKDTree(openl)
print("lid y", H[:, 1].min().round(), H[:, 1].max().round(), "open pts", len(openl), "open y", np.percentile(openl[:, 1], [1, 99]).round(), "z", np.percentile(openl[:, 2], [1, 99]).round())
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):  # one-sided: every open-lid point should be explained by the moved lid (open capture is partial)
    d, _ = cKDTree(xf(p, H)).query(openl); return np.mean(np.minimum(d, 60))
grid = []
for edge in (H[:, 1].max(), H[:, 1].min()):
    z0 = H[np.abs(H[:, 1] - edge) < 60][:, 2].mean()
    grid += [(cost([edge + dy, z0 + dz, a, 0, 0]), a, edge + dy, z0 + dz) for a in range(-85, 86, 5) if a for dy in (-80, 0, 80) for dz in (-60, 0, 60)]
grid.sort(); print("grid best", [tuple(round(v, 1) for v in g) for g in grid[:3]])
best = None
for c0, a, y, z in grid[:4]:
    r = minimize(cost, [y, z, a, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.5, "fatol": 0.01})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = cKDTree(xf(p, H)).query(openl)
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(d).round(2), "mm")
# lev(mm) -> prepped(m): prep subtracts the bbox centre/floor -> p_m = p_mm*scale + root_location
s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
res = {"p": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]), "fit_median_mm": float(np.median(d)),
       "fit_mean_mm": float(best.fun)}
json.dump(res, open(out, "w"), indent=1); print(res)
