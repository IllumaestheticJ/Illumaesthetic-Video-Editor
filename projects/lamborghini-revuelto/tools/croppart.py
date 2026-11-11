"""Keep only the part itself from a part scan that also captured surrounding car skin.
  croppart.py in.stl out.stl "x0,x1,y0,y1,z0,z1"     (levelled mm; keeps triangles whose centroid is inside)
Side Mirrors scan: the head sits outboard of the door skin (x > 985 mm) between y -850..-400; the rest of the scan
is door/window skin that left a jagged hole in the base when trimmed."""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
d = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c = d["v"].mean(1)
b = [float(v) for v in sys.argv[3].split(",")]
k = d[(c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])]
with open(sys.argv[2], "wb") as f:
    f.write(b"ive croppart".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(sys.argv[2], len(d), "->", len(k))
