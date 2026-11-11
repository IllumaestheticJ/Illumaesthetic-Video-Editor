"""Extract the closed hood panel from the full car (levelled mm): car triangles in the hood zone that are absent
(> GAP mm) from BOTH 'Bumper and Hood Removed' and 'Hood Open' (in both states the hood is not in its closed
position), above the fender line, keep the largest connected-ish cluster by XY grid.
  hood.py car_2mm.stl bumper_hood_removed.stl hood_open.stl out.stl"""
import struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)
car, bhr, ho = L(sys.argv[1]), L(sys.argv[2]), L(sys.argv[3])
cc = car["v"].mean(1)
GAP = 10.0
zone = (cc[:, 1] < -1200) & (cc[:, 2] > 650)
idx = np.where(zone)[0]
d1, _ = cKDTree(bhr["v"].mean(1)).query(cc[idx], distance_upper_bound=GAP)
d2, _ = cKDTree(ho["v"].mean(1)).query(cc[idx], distance_upper_bound=GAP)
sel = idx[np.isinf(d1) & np.isinf(d2)]
print("candidates", len(sel))
h = car[sel]
c = h["v"].mean(1)
print("bbox", c.min(0).round(), c.max(0).round())
with open(sys.argv[4], "wb") as f:
    f.write(b"lexus hood".ljust(80)); f.write(struct.pack("<I", len(h))); h.tofile(f)
