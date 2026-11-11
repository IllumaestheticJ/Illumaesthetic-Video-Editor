"""Fit a lid hinge (axis along X through (y_h, z_h), angle) mapping the CLOSED lid (top skin cut from the full car)
onto the OPEN lid captured in a state scan. Adapted from projects/huracan-evo/tools/hinge.py, but:
- the open capture is often partial (Miata hood: ~2/3 of the lid), so the cost is open -> rotated-closed distance
  (every open point must lie on the rotated lid), trimmed at 40 mm;
- the axis is pure X (lids hinge across the car), 3 parameters, grid + Nelder-Mead.
    python hinge.py closed.npy open.npy out.json --like frame.json --hinge-end max|min
Output: pivot p and axis in the prepped Blender frame (m), open_deg (rotation about +X), fit stats (mm)."""
import argparse, json, numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation as Rot
ap = argparse.ArgumentParser(); ap.add_argument("closed"); ap.add_argument("open"); ap.add_argument("out")
ap.add_argument("--like", required=True); ap.add_argument("--hinge-end", choices=["min", "max"], required=True)
a = ap.parse_args()
H = np.load(a.closed); O = np.load(a.open)
rng = np.random.default_rng(0)
O = O[rng.choice(len(O), min(2500, len(O)), replace=False)]
def xf(p, P):
    yh, zh, ang = p
    R = Rot.from_rotvec(np.radians(ang) * np.array([1.0, 0, 0])).as_matrix(); c = np.array([0, yh, zh])
    return (P - c) @ R.T + c
def cost(p):  # open points -> lid rotated back to closed by -ang must coincide with the closed lid
    d, _ = TC.query(xf([p[0], p[1], -p[2]], O)); return np.mean(np.minimum(d, 40))
TC = cKDTree(H[rng.choice(len(H), min(60000, len(H)), replace=False)])
y0 = H[:, 1].max() if a.hinge_end == "max" else H[:, 1].min()
z0 = H[np.abs(H[:, 1] - y0) < 60][:, 2].mean()
grid = sorted((cost([y0 + dy, z0 + dz, ang]), ang, dy, dz) for ang in range(-80, 81, 4) for dy in (-120, -40, 40, 120) for dz in (-80, 0, 80))
best = None
for c0, ang, dy, dz in grid[:4]:
    r = minimize(cost, [y0 + dy, z0 + dz, ang], method="Nelder-Mead", options={"maxiter": 600, "xatol": 0.2, "fatol": 0.005})
    if best is None or r.fun < best.fun: best = r
p = best.x; d, _ = TC.query(xf([p[0], p[1], -p[2]], O))
like = json.load(open(a.like)); s, rl = like["unit_scale"], np.array(like["root_location"])
out = {"p": (np.array([0, p[0], p[1]]) * s + rl).tolist(), "axis": [1, 0, 0], "open_deg": float(p[2]),
       "fit_median_mm": float(np.median(d)), "fit_p90_mm": float(np.percentile(d, 90)), "raw_mm": p.tolist()}
json.dump(out, open(a.out, "w"), indent=1); print(out)
