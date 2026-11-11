"""Make the rear licence plate unreadable (after projects/subaru-sti-blobeye/tools/deplate.py).

    python deplate.py car  in.stl out.stl      # full car (prepped frame = raw*0.001 + car4 root)
    python deplate.py lid  in.stl out.stl      # trunk lid (Trunk Open pose -> closed pose via hinge2.json, and back)

Inside the plate box (closed pose, prepped m; from an orthographic depth plot of the tail, checks/plate_ortho.png) fit a
robust plane to the plate (normal ~ -Y) and project every vertex within 8 mm of it onto the plane: the embossed characters
flatten, the plate stays a smooth slab in its recess.
"""
import json
import sys

import numpy as np
from scipy.spatial.transform import Rotation as R

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import stlio  # noqa: E402

M = "/home/user/media/honda-civic-11"
ROOT = np.array(json.load(open(f"{M}/prep/car4.json"))["root_location"])
H = json.load(open(f"{M}/trunk/hinge2.json"))
BOX = {"car": (-0.13, 0.19, 0.985, 1.10), "lid": (-0.09, 0.19, 0.985, 1.09)}   # x0 x1 z0 z1, y < -2.0

kind, src, dst = sys.argv[1:4]
m = stlio.read(src)
v = m["v"].reshape(-1, 3).astype(np.float64) * 0.001 + ROOT
piv = np.array(H["pivot_prepped"])
rot = R.from_euler("xyz", H["blender_closed_euler_deg"], degrees=True)
loc = np.array(H["blender_closed_loc"])
if kind == "lid":
    v = piv + loc + rot.apply(v - piv)
x0, x1, z0, z1 = BOX[kind]
bx = (v[:, 0] > x0) & (v[:, 0] < x1) & (v[:, 2] > z0) & (v[:, 2] < z1) & (v[:, 1] < -2.0)
q = v[bx]
pts = q.copy()
cen = np.median(pts, 0)
n = np.array([0, -1.0, 0])
for tol in (0.03, 0.015, 0.008, 0.006):
    r = (pts - cen) @ n
    pts = pts[np.abs(r) < tol]
    cen = pts.mean(0)
    n = np.linalg.svd(pts - cen, full_matrices=False)[2][2]
dist = (q - cen) @ n
near = np.abs(dist) < 0.008
q[near] -= np.outer(dist[near], n)
v[bx] = q
print(kind, "box verts", int(bx.sum()), "flattened", int(near.sum()), "normal", n.round(3), "centre", cen.round(3))
if kind == "lid":
    v = piv + rot.inv().apply(v - piv - loc)
m["v"] = ((v - ROOT) / 0.001).reshape(-1, 3, 3).astype(np.float32)
stlio.write(dst, m)
print("->", dst)
