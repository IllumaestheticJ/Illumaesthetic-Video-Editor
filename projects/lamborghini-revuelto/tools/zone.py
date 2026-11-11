"""Close-up car: 2 mm full-car triangles inside the close-up boxes + 3 mm car everywhere else (style guide: <=2 mm for
close-ups). Inputs levelled mm STLs: 2 mm car (floor-cut), 3 mm cleaned car.
  zone.py car2.stl car3.stl out.stl "x0,x1,y0,y1,z0,z1" [...]"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
c2 = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c3 = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
def inbox(c, b):
    return (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
m2 = np.zeros(len(c2), bool); m3 = np.zeros(len(c3), bool)
k2, k3 = c2["v"].mean(1), c3["v"].mean(1)
for s in sys.argv[4:]:
    b = [float(v) for v in s.split(",")]
    m2 |= inbox(k2, b); m3 |= inbox(k3, b)
res = np.concatenate([c3[~m3], c2[m2]])
with open(sys.argv[3], "wb") as f:
    f.write(b"ive revuelto zone".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
print(sys.argv[3], "2mm tris", int(m2.sum()), "total", len(res))
