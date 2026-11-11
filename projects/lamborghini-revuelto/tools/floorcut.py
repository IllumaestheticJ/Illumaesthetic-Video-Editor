"""Drop triangles below the levelled ground plane (z < ZMIN mm) - sub-floor scan noise the footprint crop keeps.
  floorcut.py in.stl out.stl [zmin=8]"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
d = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
z = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
k = d[d["v"][:, :, 2].min(1) >= z]
with open(sys.argv[2], "wb") as f:
    f.write(b"ive floorcut".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(sys.argv[2], len(d), "->", len(k))
