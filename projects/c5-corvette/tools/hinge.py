"""C5 hood hinge from real data. The C5 hood is front-hinged; 'C5 Supplement Hood Open' (registered, levelled) has it
propped open. Fit an axis (~X through (y_h, z_h), small tilt) + angle that rotates the open-hood points back DOWN onto
the closed hood of the full car. Writes:
  - hinge.json (prepped Blender frame, m): p, axis, open_deg (closed->open) for huracan tools/shot.py "hinges"
  - hood_part.stl : the open hood rotated closed (a real hood scan incl. its underside) in the levelled mm frame
usage: hinge.py car_clean.stl hood_open_c.stl car.json hinge.json hood_part.stl"""
import json, struct, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car_p, open_p, like_p, out_j, out_s = sys.argv[1:6]
car = np.fromfile(car_p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
ho = np.fromfile(open_p, dtype=TRI, offset=84)
hc = ho["v"].mean(1).astype(float)
cell = 40.0
k = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k(car[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, car[:, 2])
ka = k(hc[:, :2]); i = np.clip(np.searchsorted(u, ka), 0, len(u) - 1); roof = np.where(u[i] == ka, top[i], -1e9)
is_open = (roof > -1e8) & (hc[:, 2] > roof + 40) & (hc[:, 2] > 800) & (hc[:, 1] < 0)
# keep the big connected sheet only: points above roof+40 in the front half; drop stray props (prop rod) by z-span later
openh = hc[is_open]
print("open hood pts", len(openh), "y", openh[:, 1].min().round(), openh[:, 1].max().round(), "z", openh[:, 2].min().round(), openh[:, 2].max().round())
front = car[(car[:, 1] < -500) & (car[:, 2] > 500)]
T = cKDTree(front)
rng = np.random.default_rng(0)
H = openh[rng.choice(len(openh), min(1500, len(openh)), replace=False)]
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):
    d, _ = T.query(xf(p, H), distance_upper_bound=60); return np.mean(np.minimum(d, 60))
grid = [(cost([y, z, a, 0, 0]), y, z, a) for a in range(-90, 91, 6) for y in range(-2300, -1300, 125) for z in range(450, 1000, 125)]
grid.sort(); print("grid best", [tuple(round(v, 1) for v in g) for g in grid[:3]])
best = None
for c0, y, z, a in grid[:4]:
    r = minimize(cost, [y, z, a, 0, 0], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.3, "fatol": 0.01})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = T.query(xf(p, openh), distance_upper_bound=60)
print("fit", p.round(3), "mean", round(best.fun, 2), "median", np.median(d).round(2), "mm; within 6mm:", (d < 6).mean().round(3))
like = json.load(open(like_p)); s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
json.dump({"p": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(-p[2]),
           "fit_median_mm": float(np.median(d)), "note": "closed->open angle about axis through p (prepped m)"}, open(out_j, "w"), indent=1)
# hood part: open-hood triangles rotated closed
part = ho[is_open].copy()
v = part["v"].reshape(-1, 3).astype(float)
part["v"] = xf(p, v).reshape(-1, 3, 3).astype(np.float32)
with open(out_s, "wb") as f:
    f.write(b"ive c5 hood".ljust(80)); f.write(struct.pack("<I", len(part))); part.tofile(f)
print(out_j, out_s, len(part))
