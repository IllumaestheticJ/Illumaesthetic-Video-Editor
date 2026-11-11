"""Rear bumper part = the full car's outer rear-fascia skin (car triangles within DIST mm of the 'rear bumper inside'
scan, y > YMIN) + that inside scan. Both in the shared Artec frame (mm).
  rear_part.py car.stl rear_inside.stl out.stl [DIST] [YMIN]"""
import sys, struct, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84); ins = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
dist = float(sys.argv[4]) if len(sys.argv) > 4 else 25.0; ymin = float(sys.argv[5]) if len(sys.argv) > 5 else 1500.0
cc = car["v"].mean(1)
d, _ = cKDTree(ins["v"].mean(1)).query(cc, distance_upper_bound=dist + 1)
skin = car[(d <= dist) & (cc[:, 1] > ymin)]
o = np.concatenate([skin, ins])
with open(sys.argv[3], "wb") as f:
    f.write(b"c5 rear bumper".ljust(80)); f.write(struct.pack("<I", len(o))); o.tofile(f)
print("skin", len(skin), "inside", len(ins), "->", sys.argv[3])
