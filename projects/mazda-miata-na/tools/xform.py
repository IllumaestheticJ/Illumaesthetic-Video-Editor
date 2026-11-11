"""Apply a 4x4 (mm) from globalreg.py JSON to an STL (vertices + normals).  xform.py T.json in.stl out.stl"""
import json, struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
T = np.array(json.load(open(sys.argv[1]))["T_part_to_car_mm"]); R, t = T[:3, :3], T[:3, 3]
m = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
m["v"] = (m["v"].reshape(-1, 3).astype(np.float64) @ R.T + t).reshape(-1, 3, 3).astype(np.float32)
m["n"] = (m["n"].astype(np.float64) @ R.T).astype(np.float32)
with open(sys.argv[3], "wb") as f:
    f.write(b"ive xform".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(sys.argv[3], len(m))
