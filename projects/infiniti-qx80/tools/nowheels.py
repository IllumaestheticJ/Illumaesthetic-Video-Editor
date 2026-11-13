"""Cut the stock scanned wheels/tyres out of the levelled full car so the designer's wheels (Volk CE28 + R888R from
Ecky's preview.blend) can replace them in the final render. Axles measured on the scan (prepped m): y +1.65 / -1.44,
centre z 0.42; wheel+tyre radius 0.43; outboard of |x| 0.62. Works in the levelled mm frame (prepped = lev*0.001 + root).
  nowheels.py car_lev_clean.stl out.stl"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ROOT = np.array([0.0609, -0.3212, 0.0232])
a = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
c = a["v"].mean(1) * 0.001 + ROOT
cut = np.zeros(len(a), bool)
for yc in (1.65, -1.44):
    r2 = (c[:, 1] - yc) ** 2 + (c[:, 2] - 0.42) ** 2
    cut |= (r2 < 0.43 ** 2) & (np.abs(c[:, 0]) > 0.62)
print("removed", int(cut.sum()), "of", len(a))
k = a[~cut]
with open(sys.argv[2], "wb") as f:
    f.write(b"qx80 car without stock wheels".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
