"""Trunk-open state on the full car (all levelled+cleaned mm STLs in one frame).
  trunk_comp.py car.stl rear.stl trunkopen.stl out.stl [xmin xmax [ymax]]   (trunk: -3000 0 640)
Also used for the hood: car, Hood Scoop Removed (closed, same 2024-01 session), Hood Open, xmin 1100 (front only).
'Rear' (closed) and 'Trunk open' are the same 2024-04 session, so the surfaces that MOVED between them are
rear points > MOVED mm from the trunk-open scan (= closed lid + wing). Car triangles within CUT mm of those
are removed; trunk-open triangles > NEW mm from the remaining car (open lid, trunk interior) are added.
Partial-coverage holes in 'Trunk open' therefore never delete car surface.
"""
import struct
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
MOVED, CUT, NEW = 12.0, 10.0, 8.0
car_p, rear_p, to_p, out = sys.argv[1:5]
XMIN, XMAX = (float(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 else (-1e9, 1e9)
car = np.fromfile(car_p, dtype=TRI, offset=84); rear = np.fromfile(rear_p, dtype=TRI, offset=84)
to = np.fromfile(to_p, dtype=TRI, offset=84)
to = to[(to["v"].mean(1)[:, 0] > XMIN) & (to["v"].mean(1)[:, 0] < XMAX)]
rear = rear[(rear["v"].mean(1)[:, 0] > XMIN) & (rear["v"].mean(1)[:, 0] < XMAX)]
cc, rc, tc = car["v"].mean(1), rear["v"].mean(1), to["v"].mean(1)
d, _ = cKDTree(tc).query(rc, distance_upper_bound=MOVED * 2)
lo, hi = tc.min(0), tc.max(0)
inbox = np.all((rc >= lo) & (rc <= hi), 1)
YMAX = float(sys.argv[7]) if len(sys.argv) > 7 else 1e9  # lid half-width: quarter-panel coverage gaps are not "moved"
moved = rc[(d > MOVED) & inbox & (np.abs(rc[:, 1] - np.median(rc[:, 1])) < YMAX)]
print("moved rear pts (closed lid + wing):", len(moved))
d2, _ = cKDTree(moved).query(cc, distance_upper_bound=CUT * 2)
keep = d2 > CUT
kc = car[keep]
d3, _ = cKDTree(kc["v"].mean(1)).query(tc, distance_upper_bound=NEW * 2)
add = to[d3 > NEW]
print("car removed", int((~keep).sum()), "trunk-open added", len(add))
m = np.concatenate([kc, add])
with open(out, "wb") as f:
    f.write(b"wrx trunk_comp".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(out, len(m))
