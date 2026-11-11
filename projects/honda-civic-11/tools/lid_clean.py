"""Clean the open lid: drop triangles within --near mm of the car (body bits near the hinge picked up by the z/y box)
and, after rotating closed (hinge2.json), anything outside the car's deck width or > --gap mm from any car surface.

    python lid_clean.py car.stl lid_open.stl hinge2.json car4.json out.stl
"""
import json, os, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write  # noqa: E402
car_p, lid_p, h_p, like, out = sys.argv[1:6]
pj = json.load(open(like)); s = pj["unit_scale"]; rl = np.array(pj["root_location"])
h = json.load(open(h_p)); piv = np.array(h["pivot_prepped"])
M = Rot.from_euler("xyz", h["blender_closed_euler_deg"], degrees=True).as_matrix()
car = read(car_p); lid = read(lid_p)
cp = car["v"].mean(1) * s + rl
lp = lid["v"].mean(1).astype(float) * s + rl
T = cKDTree(cp)
d_open, _ = T.query(lp, distance_upper_bound=0.03)
near = d_open < 0.010
closed = (lp - piv) @ M.T + piv + np.array(h["blender_closed_loc"])
deck = cp[(cp[:, 1] < -1.5) & (cp[:, 2] > 0.85)]
x0, x1 = np.percentile(deck[:, 0], [0.2, 99.8])
wide = (closed[:, 0] < x0 - 0.01) | (closed[:, 0] > x1 + 0.01)
d_cl, _ = T.query(closed, distance_upper_bound=0.3)
# the lid's own inner structure sits up to ~0.15 m under the skin; anything farther from every car surface is stray
stray = d_cl > 0.18
keep = ~(near | wide | stray)
print("lid tris", len(lid), "dropped near-body", int(near.sum()), "too wide", int(wide.sum()), "stray", int(stray.sum()), "deck x", round(x0, 3), round(x1, 3))
write(out, lid[keep])
