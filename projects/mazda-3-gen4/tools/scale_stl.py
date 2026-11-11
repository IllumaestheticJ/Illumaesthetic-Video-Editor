"""Scale a binary STL (e.g. inches -> mm: 25.4).  scale_stl.py in.stl out.stl 25.4"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84); m["v"] *= float(sys.argv[3])
with open(sys.argv[2], "wb") as f: f.write(b"scaled".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(sys.argv[2], len(m))
