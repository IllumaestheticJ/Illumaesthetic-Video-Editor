"""Apply a saved 4x4 (json {"T": ...}, part mm -> car mm) to a binary STL.   python xform_stl.py in.stl T.json out.stl"""
import json, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
hdr = open(sys.argv[1], "rb").read(84)
t = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
T = np.array(json.load(open(sys.argv[2]))["T"])
t["v"] = (t["v"].reshape(-1, 3) @ T[:3, :3].T + T[:3, 3]).reshape(-1, 3, 3).astype("<f4")
t["n"] = (t["n"] @ T[:3, :3].T).astype("<f4")
with open(sys.argv[3], "wb") as f:
    f.write(hdr); t.tofile(f)
print(sys.argv[3], t["v"].reshape(-1, 3).min(0).round(), t["v"].reshape(-1, 3).max(0).round())
