"""Trunk composite with the refined hinge (hinge2.json): car minus lid skin (within 10 mm of the CLOSED lid) +
Trunk Open triangles (not lid) > 8 mm from the trimmed car above 0.6 m (trunk interior, gutters, goose-neck mounts).
All in the prepped frame (m); writes raw-frame STLs so `ive prep --like car4.json` maps them back.

    python trunk_base.py car.stl trunkopen.stl lid_open.stl hinge2.json car4.json out_base.stl [out_skin.stl]
"""
import json, os, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write  # noqa: E402
car_p, to_p, lid_p, h_p, like, out = sys.argv[1:7]
pj = json.load(open(like)); s = pj["unit_scale"]; rl = np.array(pj["root_location"])
h = json.load(open(h_p)); piv = np.array(h["pivot_prepped"]); ax = np.array(h["axis"])
M = Rot.from_euler("XYZ", h["closed_euler_xyz_deg"], degrees=True).as_matrix()
car = read(car_p); to = read(to_p); lid = read(lid_p)
P = lambda d: d["v"].mean(1).astype(float) * s + rl
lv = lid["v"].reshape(-1, 3).astype(float) * s + rl
closed = (lv - piv) @ M.T + piv + ax * h["slide_along_axis_m"]
cp = P(car)
dc, _ = cKDTree(closed).query(cp, distance_upper_bound=0.015)
skin = dc < 0.010
print("lid skin tris removed", int(skin.sum()))
kc = car[~skin]
# interior: Trunk Open minus its lid (same rule as trunk.py) farther than 8 mm from the trimmed car
tc = P(to)
lid_m = (tc[:, 2] > 1.36) & (tc[:, 1] < -1.40)
rest = to[~lid_m]; rc = tc[~lid_m]
d2, _ = cKDTree(P(kc)).query(rc, distance_upper_bound=0.012)
inter = (d2 > 0.008) & (rc[:, 2] > 0.6)
print("interior tris added", int(inter.sum()))
write(out, np.concatenate([kc, rest[inter]]))
if len(sys.argv) > 7:
    write(sys.argv[7], car[skin])
