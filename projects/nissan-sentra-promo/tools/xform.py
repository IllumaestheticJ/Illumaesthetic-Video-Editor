"""Apply a 4x4 (raw mm -> design mm) to a binary STL. xform.py M.json in.stl out.stl  (M.json: {"M": 4x4})"""
import json, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = np.array(json.load(open(sys.argv[1]))["M"], float)
d = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
v = d["v"].reshape(-1, 3).astype(np.float64) @ M[:3, :3].T + M[:3, 3]
d["v"] = v.reshape(-1, 3, 3).astype(np.float32)
n = np.cross(d["v"][:, 1] - d["v"][:, 0], d["v"][:, 2] - d["v"][:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
d["n"] = n
with open(sys.argv[3], "wb") as f:
    f.write(b"\0" * 80); f.write(np.uint32(len(d)).tobytes()); d.tofile(f)
