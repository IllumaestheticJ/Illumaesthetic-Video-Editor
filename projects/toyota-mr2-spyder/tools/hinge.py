"""Fit a hinge (axis ~X through (0, yh, zh), small tilt, angle) that maps a closed panel (from diffpart.py) onto the
same panel captured open in a state scan (open points = state-scan points above the closed car's surface + 30 mm
inside a box). Output in metres in the prepped Blender frame (scaled, plus the prep root_location) for tools/shot.py hinges.
  hinge.py closed_L.stl state_L.stl car_L.stl prep.json out.json --box x0,x1,y0,y1 [--guess yh,zh,deg]"""
import argparse, json, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ("closed", "state", "car", "prep", "out")]
ap.add_argument("--box", required=True); ap.add_argument("--guess", default="-1000,950,60")
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
lid, st, car = L(a.closed), L(a.state), L(a.car)
x0, x1, y0, y1 = map(float, a.box.split(","))
inb = lambda P: (P[:, 0] > x0) & (P[:, 0] < x1) & (P[:, 1] > y0) & (P[:, 1] < y1)
cell = 30.0
k = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k(car[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, car[:, 2])
ks = k(st[:, :2]); i = np.clip(np.searchsorted(u, ks), 0, len(u) - 1); roof = np.where(u[i] == ks, top[i], -1e9)
openp = st[(st[:, 2] > roof + 30) & inb(st)]
H = lid[np.random.default_rng(0).choice(len(lid), min(3000, len(lid)), replace=False)]
T = cKDTree(openp)
print("open pts", len(openp), "lid y", H[:, 1].min().round(), H[:, 1].max().round())
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H)); return np.mean(np.minimum(d, 60))
g = list(map(float, a.guess.split(",")))
best = None
for ang in (g[2], -g[2], g[2] * 1.4, -g[2] * 1.4):
    for dy in (-80, 0, 80):
        r = minimize(cost, [g[0] + dy, g[1], ang, 0, 0], method="Nelder-Mead", options=dict(maxiter=1500, xatol=0.1, fatol=0.01))
        if best is None or r.fun < best.fun: best = r
d, _ = T.query(xf(best.x, H))
yh, zh, ang, tz, ty = best.x
prep = json.load(open(a.prep)); s = prep["unit_scale"]; root = np.array(prep["root_location"])
p_m = np.array([0, yh, zh]) * s + root  # scan_prep: prepped = scaled + root.location
ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
out = {"p": p_m.tolist(), "axis": ax.tolist(), "open_deg": float(ang), "median_mm": float(np.median(d)), "fit_mm": [yh, zh]}
json.dump(out, open(a.out, "w"), indent=1); print(out)
