"""Hood part = the full car's own hood skin (car tris within TRIM mm of the rotated-closed open-hood scan) + the
open-hood scan's tris farther than that from the car (its underside / inner frame). Closed, it is identical to the
car; opened, it shows the real underside from 'C5 Supplement Hood Open'.
  hoodcombo.py car.stl hood_part.stl out.stl"""
import struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84); hp = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
cc, hc = car["v"].mean(1), hp["v"].mean(1)
d, _ = cKDTree(hc).query(cc, distance_upper_bound=8); skin = car[d <= 7]
d2, _ = cKDTree(skin["v"].mean(1)).query(hc, distance_upper_bound=8); under = hp[d2 > 7]
res = np.concatenate([skin, under])
with open(sys.argv[3], "wb") as f:
    f.write(b"ive c5 hood combo".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
print("skin", len(skin), "underside", len(under))
