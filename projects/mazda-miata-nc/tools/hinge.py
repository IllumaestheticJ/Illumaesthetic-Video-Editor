"""Fit a panel hinge (axis ~X with small tilt, through (y_h, z_h)) + angle mapping the closed panel (cut from the
car) onto the open panel captured in a state scan. Adapted from huracan-evo/tools/hinge.py. Levelled mm in,
prepped Blender frame (m) out.
    hinge.py closed.stl open_state.stl car_clean.stl car4.json out.json --ymin 1300 [--end front|rear]
--end: which edge of the closed panel the hinge sits at (trunk lid: front = min y)."""
import argparse, json
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
for k in ("closed", "state", "car", "like", "out"):
    ap.add_argument(k)
ap.add_argument("--ymin", type=float, default=-1e9); ap.add_argument("--ymax", type=float, default=1e9)
ap.add_argument("--end", default="front")
a = ap.parse_args()
ld = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
panel, car, st = ld(a.closed), ld(a.car), ld(a.state)
cell = 40.0
key = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(key(car[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, car[:, 2])
ks = key(st[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[i] == ks, top[i], -1e9)
openp = st[(st[:, 2] > roof + 40) & (st[:, 1] > a.ymin) & (st[:, 1] < a.ymax)]
rng = np.random.default_rng(0)
H = panel[rng.choice(len(panel), min(3000, len(panel)), replace=False)]
T = cKDTree(openp)
print("panel y", H[:, 1].min().round(), H[:, 1].max().round(), "open pts", len(openp))
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H)); return np.mean(np.minimum(d, 60))
y0 = H[:, 1].min() if a.end == "front" else H[:, 1].max()
z0 = H[np.abs(H[:, 1] - y0) < 50][:, 2].mean()
grid = sorted((cost([y0 + dy, z0 + dz, ang, 0, 0]), ang, dy, dz) for ang in range(-90, 91, 5)
              for dy in (-150, -75, 0, 75, 150) for dz in (-150, -75, 0, 75))
print("grid best", [tuple(round(x, 1) for x in g) for g in grid[:3]])
best = None
for c0, ang, dy, dz in grid[:4]:
    r = minimize(cost, [y0 + dy, z0 + dz, ang, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.3, "fatol": 0.01})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, H))
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(d).round(2), "mm  <5mm", (d < 5).mean().round(2))
like = json.load(open(a.like)); s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
out = {"p": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]),
       "fit_median_mm": float(np.median(d)), "fit_lt5mm": float((d < 5).mean())}
json.dump(out, open(a.out, "w"), indent=1); print(out)
