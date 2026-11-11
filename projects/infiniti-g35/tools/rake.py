"""Second levelling step: the scanned ground is not the car's reference - the front was jacked (stand under the sill),
so the body sits nose-up 3.7 deg (wheel centres 40 px / 633 px in an orthographic side render, arch tops 3.9 deg) and
rolled 0.65 deg (sill bottoms: -X side 20-24 mm higher than +X). Rotate about the origin; applied identically to the
car and every part (rigid, shared frame), AFTER clean_car.py (which cuts at the scanned ground).
    rake.py in.stl out.stl [pitch_deg] [roll_deg]"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
p = np.radians(float(sys.argv[3]) if len(sys.argv) > 3 else 3.7)
r = np.radians(float(sys.argv[4]) if len(sys.argv) > 4 else -0.65)
Rx = np.array([[1, 0, 0], [0, np.cos(p), -np.sin(p)], [0, np.sin(p), np.cos(p)]])
Ry = np.array([[np.cos(r), 0, np.sin(r)], [0, 1, 0], [-np.sin(r), 0, np.cos(r)]])
R = Ry @ Rx
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
m["v"] = (m["v"].reshape(-1, 3).astype(np.float64) @ R.T).reshape(-1, 3, 3).astype(np.float32)
m["n"] = (m["n"].astype(np.float64) @ R.T).astype(np.float32)
with open(sys.argv[2], "wb") as f:
    f.write(b"infiniti-g35 rake".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(sys.argv[2])
