"""Exploded-view base: full car with every removable panel trimmed + the All-Parts-Removed scan where it adds
what those panels hide. All inputs are levelled+cropped 3 mm STLs in one frame (mm).
  composite.py car.stl apr.stl out_base.stl part1.stl part2.stl ...
- car triangles within TRIM mm of any part scan point = that panel on the car -> removed (the part scan replaces it)
- APR triangles farther than ADD mm from the trimmed car = newly exposed structure -> added
- APR triangles more than 30 mm above the car's own roofline (per 40 mm XY cell) = APR's propped-open hood -> dropped
"""
import struct, sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
TRIM, ADD = 6.0, 6.0
car_p, apr_p, out, parts = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
car = np.fromfile(car_p, dtype=TRI, offset=84); apr = np.fromfile(apr_p, dtype=TRI, offset=84)
cc = car["v"].mean(1); ac = apr["v"].mean(1)
P = np.concatenate([np.fromfile(p, dtype=TRI, offset=84)["v"].reshape(-1, 3) for p in parts])
d, _ = cKDTree(P).query(cc, distance_upper_bound=TRIM + 1)
keep_car = d > TRIM
print("car tris trimmed (panels):", int((~keep_car).sum()), "of", len(car))
kc = car[keep_car]
d2, _ = cKDTree(kc["v"].reshape(-1, 3)).query(ac, distance_upper_bound=ADD + 1)
add = d2 > ADD
# roofline of the full car per 40 mm cell
cell = 40.0
key = lambda xy: (np.floor(xy[:, 0] / cell).astype(np.int64) * 100000 + np.floor(xy[:, 1] / cell).astype(np.int64))
kcar = key(cc[:, :2]); u, inv = np.unique(kcar, return_inverse=True)
top = np.full(len(u), -1e9); np.maximum.at(top, inv, cc[:, 2])
ka = key(ac[:, :2]); idx = np.searchsorted(u, ka); idx = np.clip(idx, 0, len(u) - 1)
roof = np.where(u[idx] == ka, top[idx], -1e9)
hood_up = (ac[:, 2] > roof + 30) & (ac[:, 1] < 0)  # front half only (nose at -Y)
add &= ~hood_up
print("apr tris added:", int(add.sum()), "dropped as open hood:", int(hood_up.sum()))
res = np.concatenate([kc, apr[add]])
with open(out, "wb") as f:
    f.write(b"ive huracan composite".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
print(out, len(res))
