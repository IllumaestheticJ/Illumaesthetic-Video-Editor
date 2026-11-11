"""Fit the 400Z hood hinge (after projects/huracan-evo/tools/hinge.py): axis ~X through (y_h, z_h) + angle that maps
the closed hood (cut from the full car) onto the propped-open hood captured in 'Hood Open'. Levelled mm in,
prepped Blender metres out (pivot for tools/shot.py parts).  hinge.py out.json"""
import json, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ld = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(float)
hood = ld("/home/user/media/nissan-400z/parts/hood.stl")
car = ld("/home/user/media/nissan-400z/lev/Full_Car_3mm.stl")
ho = ld("/home/user/media/nissan-400z/lev/Hood_Open_3mm.stl")
cell = 40.0
k = lambda xy: np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64)
u, inv = np.unique(k(car[:, :2]), return_inverse=True); top = np.full(len(u), -1e9); np.maximum.at(top, inv, car[:, 2])
kh = k(ho[:, :2]); i = np.clip(np.searchsorted(u, kh), 0, len(u) - 1); roof = np.where(u[i] == kh, top[i], -1e9)
openh = ho[(roof > -1e8) & (ho[:, 2] > roof + 40) & (ho[:, 2] > 0) & (ho[:, 1] < -500) & (ho[:, 1] > -2500)]
H = hood[np.random.default_rng(0).choice(len(hood), 30000, replace=False)]
O = openh[np.random.default_rng(1).choice(len(openh), min(4000, len(openh)), replace=False)]
T = cKDTree(openh)
print("open-hood pts", len(openh), "z range", openh[:, 2].min().round(), openh[:, 2].max().round())
def xf(p, P):
    yh, zh, ang, tz, ty = p
    ax = np.array([1.0, ty, tz]); ax /= np.linalg.norm(ax)
    R = Rot.from_rotvec(np.radians(ang) * ax).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
# open scan is fragmentary: score open-hood points against the moved closed hood (open subset of hood)
cost = lambda p: np.mean(np.minimum(cKDTree(xf(p, H)).query(O)[0], 60))
y0 = H[:, 1].max(); z0 = H[H[:, 1] > y0 - 50][:, 2].mean()
grid = sorted((cost([y0 + dy, z0 + dz, a, 0, 0]), a, dy, dz) for a in range(-90, 91, 6) for dy in (-150, 0, 150) for dz in (-100, 0, 100))
print("grid best", grid[:3])
best = None
for c0, a, dy, dz in grid[:3]:
    r = minimize(cost, [y0 + dy, z0 + dz, a, 0, 0], method="Nelder-Mead", options={"maxiter": 1000, "xatol": 0.5, "fatol": 0.02})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = cKDTree(xf(p, H)).query(O)
like = json.load(open("/home/user/media/work/z400/blend/car.json"))
s, rl = like["unit_scale"], np.array(like["root_location"])
ax = np.array([1.0, p[4], p[3]]); ax /= np.linalg.norm(ax)
out = {"pivot": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": ax.tolist(), "open_deg": float(p[2]),
       "fit_median_mm": float(np.median(d)), "fit_p75_mm": float(np.percentile(d, 75))}
json.dump(out, open(sys.argv[1], "w"), indent=1); print(out)
