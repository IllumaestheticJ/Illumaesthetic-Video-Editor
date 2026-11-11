"""Keep triangles whose centroid is inside an axis box (levelled mm).  boxcrop.py in.stl out.stl xmin,xmax ymin,ymax zmin,zmax"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c = m["v"].mean(1)
k = np.ones(len(m), bool)
for i, s in enumerate(sys.argv[3:6]):
    lo, hi = (float(v) for v in s.split(",")); k &= (c[:, i] >= lo) & (c[:, i] <= hi)
o = m[k]
with open(sys.argv[2], "wb") as f:
    f.write(b"boxcrop".ljust(80)); f.write(struct.pack("<I", len(o))); o.tofile(f)
print(sys.argv[2], len(o))
