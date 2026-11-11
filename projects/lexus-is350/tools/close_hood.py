"""Rotate the facelift car's own hood (the panel in 'Hood Open', captured propped open) shut about the fitted hinge
(hinge.json, prepped metres -> levelled mm via car4 json), i.e. the inverse of the hinge fit. Writes the closed hood (mm).
    close_hood.py hood_open_panel.stl hinge.json car4.json out_closed.stl"""
import json, struct, sys, numpy as np
from scipy.spatial.transform import Rotation as Rot
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
h = json.load(open(sys.argv[2])); like = json.load(open(sys.argv[3]))
s, rl = like["unit_scale"], np.array(like["root_location"])
c = (np.array(h["pivot"]) - rl) / s                       # pivot in levelled mm (x arbitrary on the axis)
R = Rot.from_rotvec(np.radians(-h["open_deg"]) * np.array(h["axis"])).as_matrix()   # open -> closed
v = (m["v"].reshape(-1, 3).astype(float) - c) @ R.T + c
m["v"] = v.reshape(-1, 3, 3).astype(np.float32); m["n"] = (m["n"].astype(float) @ R.T).astype(np.float32)
with open(sys.argv[4], "wb") as f:
    f.write(b"facelift hood closed".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print("pivot mm", c.round(1), "closed bbox", v.min(0).round(), v.max(0).round())
