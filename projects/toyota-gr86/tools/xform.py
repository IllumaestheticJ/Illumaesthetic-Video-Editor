"""Apply a pinned 4x4 rigid transform (mm, levelled frame; e.g. regcheck's *_icp.npy) to an STL.
  xform.py M.npy in.stl out.stl"""
import struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
M = np.load(sys.argv[1]); m = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
m["v"] = (m["v"].reshape(-1, 3).astype(np.float64) @ M[:3, :3].T + M[:3, 3]).reshape(-1, 3, 3).astype(np.float32)
m["n"] = (m["n"].astype(np.float64) @ M[:3, :3].T).astype(np.float32)
with open(sys.argv[3], "wb") as f:
    f.write(b"ive xform gr86".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(sys.argv[3])
