"""Exploded-view base: car (hood already split off, tools/hood.py) minus every panel a part scan covers.
  explode_base.py base_hood.stl out.stl part1.stl part2.stl ...   (levelled mm frame)
Car tris within TRIM mm of any part point are that panel on the car -> removed (the part scan replaces it)."""
import struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
TRIM = 8.0
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
P = np.concatenate([np.fromfile(p, dtype=TRI, offset=84)["v"].reshape(-1, 3) for p in sys.argv[3:]])
d, _ = cKDTree(P).query(car["v"].mean(1), distance_upper_bound=TRIM + 1)
keep = d > TRIM
print("trimmed", int((~keep).sum()), "of", len(car))
with open(sys.argv[2], "wb") as f:
    f.write(b"ive qx80 explode base".ljust(80)); f.write(struct.pack("<I", int(keep.sum()))); car[keep].tofile(f)
