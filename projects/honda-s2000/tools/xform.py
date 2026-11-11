"""Apply a saved 4x4 (part raw mm -> levelled car mm) to a binary STL. xform.py in.stl T.json out.stl"""
import json, struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
src, tj, out = sys.argv[1:4]
T = np.array(json.load(open(tj))["T_part_to_car_mm"])
m = np.fromfile(src, dtype=TRI, offset=84)
m["v"] = (m["v"].reshape(-1, 3).astype(np.float64) @ T[:3, :3].T + T[:3, 3]).reshape(-1, 3, 3).astype(np.float32)
m["n"] = (m["n"].astype(np.float64) @ T[:3, :3].T).astype(np.float32)
with open(out, "wb") as f:
    f.write(b"ive xform s2k".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(out, len(m))
