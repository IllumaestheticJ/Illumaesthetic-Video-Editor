"""Split the 'Hood Underside' (hood-open) state scan into a hinged hood panel + static base (levelled mm frame).
  hood.py car4_clean.stl hood_under_4mm.stl hood_hinge.json out_base.stl out_hood.stl
- state tris that land within 12 mm of the car once rotated closed by the fitted hinge = hood panel (its underside
  and edges), kept in the CLOSED pose so the part's rest pose sits on the car (animate it open with +|close_deg|)
- car tris within 15 mm of that closed panel = the hood skin on the car -> moved into the hood part (top surface)
- base = car minus hood skin + state tris >12 mm from the car that are not hood (what the open-hood capture saw
  under the hood), restricted to below the closed hood surface."""
import json, struct, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car_p, st_p, hj, ob, oh = sys.argv[1:6]
car = np.fromfile(car_p, dtype=TRI, offset=84); st = np.fromfile(st_p, dtype=TRI, offset=84)
H = json.load(open(hj)); c = np.array(H["pivot_mm"]); ax = np.array(H["dir"])
R = Rot.from_rotvec(np.radians(H["close_deg"]) * ax).as_matrix()
cc = car["v"].mean(1); sc = st["v"].mean(1)
Tc = cKDTree(cc)
closed_c = (sc - c) @ R.T + c
d_closed, _ = Tc.query(closed_c, distance_upper_bound=40)
d_open, _ = Tc.query(sc, distance_upper_bound=40)
hood = (d_closed < 12) & (d_open > 20) & (sc[:, 1] > c[1] - 50)
print("hood panel tris", int(hood.sum()))
hp = st[hood].copy()
v = hp["v"].reshape(-1, 3).astype(float); hp["v"] = ((v - c) @ R.T + c).reshape(-1, 3, 3).astype(np.float32)
hp["n"] = (hp["n"].astype(float) @ R.T).astype(np.float32)
dh, _ = cKDTree(hp["v"].mean(1)).query(cc, distance_upper_bound=40)
skin = (dh < 15) & (cc[:, 2] > 850)
print("car hood skin tris", int(skin.sum()))
# static under-hood capture: far from car, not hood, below the closed hood
static = (~hood) & (d_open > 12) & (sc[:, 1] > c[1] - 100) & (sc[:, 2] < 1150)
print("static under-hood tris", int(static.sum()))
def w(path, arr):
    with open(path, "wb") as f:
        f.write(b"ive qx80 hood".ljust(80)); f.write(struct.pack("<I", len(arr))); arr.tofile(f)
w(ob, np.concatenate([car[~skin], st[static]])); w(oh, np.concatenate([hp, car[skin]]))
print("written")
