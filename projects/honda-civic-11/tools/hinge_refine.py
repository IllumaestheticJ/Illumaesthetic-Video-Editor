"""Refine the trunk hinge: start from hinge.json (X-axis fit), run trimmed 6-DOF ICP of the lid's OUTER skin (closed pose)
onto the full car's deck, then express open->closed as a rotation about a pivot ON the screw axis (prepped frame).

    python hinge_refine.py car.stl lid_open.stl hinge.json car4.json out.json
"""
import json, os, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read  # noqa: E402

car_p, lid_p, h_p, like, out = sys.argv[1:6]
pj = json.load(open(like)); s = pj["unit_scale"]; rl = np.array(pj["root_location"])
h = json.load(open(h_p))
car = read(car_p); lid = read(lid_p)
cp = car["v"].mean(1) * s + rl
lp = lid["v"].mean(1).astype(float) * s + rl; ln = lid["n"].astype(float)
piv = np.array(h["pivot_prepped"]); a = np.radians(h["closed_rot_x_deg"])
R0 = Rot.from_euler("x", a).as_matrix()
P0 = (lp - piv) @ R0.T + piv; N0 = ln @ R0.T
skin = (N0[:, 2] > 0.35) | (N0[:, 1] < -0.5)          # closed lid outer skin faces up / backwards
src = P0[skin][:: max(1, skin.sum() // 30000)]
deck = cp[(cp[:, 1] < -1.2) & (cp[:, 2] > 0.75)]
T = cKDTree(deck)
R, t = np.eye(3), np.zeros(3)
for it in range(40):
    q = src @ R.T + t
    d, i = T.query(q, distance_upper_bound=0.05)
    fin = np.isfinite(d)
    thr = max(0.003, np.percentile(d[fin], 60))
    ok = fin & (d < thr)
    Pm, Qm = q[ok], T.data[i[ok]]
    mp, mq = Pm.mean(0), Qm.mean(0)
    U, S, Vt = np.linalg.svd((Pm - mp).T @ (Qm - mq))
    Ri = (U @ Vt).T
    if np.linalg.det(Ri) < 0:
        Vt[-1] *= -1; Ri = (U @ Vt).T
    R, t = Ri @ R, Ri @ t + (mq - Ri @ mp)
d, _ = T.query(src @ R.T + t, distance_upper_bound=0.05)
d = d[np.isfinite(d)] * 1000
print("refine: extra rot %.2f deg, shift %s mm; skin dist p50 %.1f p75 %.1f mm, frac<5mm %.2f" % (
    np.degrees(Rot.from_matrix(R).magnitude()), np.round(t * 1000, 1), np.median(d), np.percentile(d, 75), (d < 5).mean()))
# total open->closed: x -> R (R0 (x - piv) + piv) + t  = M x + c
M = R @ R0; c = R @ (piv - R0 @ piv) + t
rv = Rot.from_matrix(M).as_rotvec(); ang = np.linalg.norm(rv); ax = rv / ang
# point on screw axis closest to old pivot: solve (I - M) p = c - (ax.c) ax  (least squares)
p, *_ = np.linalg.lstsq(np.eye(3) - M, c - np.dot(ax, c) * ax, rcond=None)
p = p + ax * np.dot(ax, piv - p)
slide = np.dot(ax, c)
eul = Rot.from_matrix(M).as_euler("XYZ", degrees=True)
res = {"pivot_prepped": p.tolist(), "axis": ax.tolist(), "angle_deg": float(np.degrees(ang)), "slide_along_axis_m": float(slide),
       "closed_euler_xyz_deg": eul.tolist(), "skin_p50_mm": float(np.median(d)), "note": "lid_open.blend rotated by closed_euler about pivot = closed lid"}
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res, indent=1))
