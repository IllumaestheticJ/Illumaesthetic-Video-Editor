"""Trunk lid from the FE1 'Trunk Open' state scan: hinge fit + composites. Raw scan frame (mm, z up, front +Y).

    python trunk.py car.stl trunkopen.stl outdir car4.json

Writes outdir/lid_open.stl (lid as captured, open), outdir/trunk_base.stl (full car minus the closed lid skin
+ newly exposed trunk interior from the state scan) and outdir/hinge.json (pivot in the PREPPED frame, angle about X).
- lid = state-scan triangles above the car's deck line (z > ZLID) behind the rear glass (y < YLID)
- hinge: rotation about an X-parallel axis through (y_h, z_h) by a, fitted so the rotated lid lands on the car's
  closed deck (trimmed mean distance, Nelder-Mead from a coarse grid)
"""
import json, os, sys
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write  # noqa: E402

car_p, to_p, out, like = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
pj = json.load(open(like)); s = pj["unit_scale"]; rl = np.array(pj["root_location"])
raw = lambda p: (np.asarray(p) - rl) / s          # prepped m -> raw mm
ZLID, YLID = raw([0, 0, 1.36])[2], raw([0, -1.40, 0])[1]
car = read(car_p); to = read(to_p)
cc, tc = car["v"].mean(1), to["v"].mean(1)
lid_m = (tc[:, 2] > ZLID) & (tc[:, 1] < YLID)
lid = to[lid_m]
print("lid tris", len(lid))
L = lid["v"].mean(1).astype(float)
L = L[np.random.default_rng(0).choice(len(L), min(4000, len(L)), replace=False)]
deck = cc[(cc[:, 1] < YLID + 600) & (cc[:, 2] > raw([0, 0, 0.8])[2])].astype(float)
T = cKDTree(deck)


def rotx(P, yh, zh, a):
    c, sn = np.cos(np.radians(a)), np.sin(np.radians(a))
    y, z = P[:, 1] - yh, P[:, 2] - zh
    return np.stack([P[:, 0], yh + c * y - sn * z, zh + sn * y + c * z], 1)


def cost(p):
    d, _ = T.query(rotx(L, *p)); return np.mean(np.minimum(d, 40))


h0 = raw([0, -1.55, 1.38])
grid = sorted((cost([h0[1] + dy, h0[2] + dz, a]), dy, dz, a) for a in range(-120, 121, 6) for dy in (-100, 0, 100) for dz in (-100, 0, 100))
best = None
for c0, dy, dz, a in grid[:4]:
    r = minimize(cost, [h0[1] + dy, h0[2] + dz, a], method="Nelder-Mead", options={"maxiter": 1500, "xatol": 0.2, "fatol": 0.01})
    if best is None or r.fun < best.fun:
        best = r
yh, zh, a = best.x
d, _ = T.query(rotx(L, yh, zh, a))
print("hinge y %.1f z %.1f angle %.2f deg; trimmed mean %.2f, median %.2f mm, frac<5mm %.2f" % (yh, zh, a, best.fun, np.median(d), (d < 5).mean()))
closed = rotx(lid["v"].reshape(-1, 3).astype(float), yh, zh, a)
# car skin under the closed lid
dc, _ = cKDTree(closed).query(cc, distance_upper_bound=12)
skin = dc < 10
print("car tris removed as lid skin", int(skin.sum()))
base_car = car[~skin]
# newly exposed interior from the state scan: not lid, > 8 mm from the trimmed car, above the bumper top, not the prop
rest = to[~lid_m]; rc = rest["v"].mean(1)
d2, _ = cKDTree(base_car["v"].mean(1)).query(rc, distance_upper_bound=10)
inter = (d2 > 8) & (rc[:, 2] > raw([0, 0, 0.6])[2])
print("interior tris added", int(inter.sum()))
write(f"{out}/trunk_base.stl", np.concatenate([base_car, rest[inter]]))
write(f"{out}/lid_open.stl", lid)
write(f"{out}/lid_skin_car.stl", car[skin])
pv = np.array([0, yh, zh]) * s + rl
json.dump({"pivot_prepped": [0.0, float(pv[1]), float(pv[2])], "open_from_closed_deg": float(-a),
           "closed_rot_x_deg": float(a), "fit_median_mm": float(np.median(d))}, open(f"{out}/hinge.json", "w"), indent=1)
print(open(f"{out}/hinge.json").read())
