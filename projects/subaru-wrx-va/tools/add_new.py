"""Append triangles of a state scan that are NEW relative to a base (> NEW mm away) inside a box (mm, levelled frame).
  add_new.py base.stl state.stl out.stl xmin xmax zmin [new_mm]
Used to add the propped hood captured in 'Front End Bumper Removed' (2024-01) to the hood-open composite:
'Hood Open' (same session) only caught fragments of the raised hood."""
import struct, sys
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
bp, sp, op = sys.argv[1:4]; x0, x1, z0 = map(float, sys.argv[4:7]); NEW = float(sys.argv[7]) if len(sys.argv) > 7 else 8.0
b = np.fromfile(bp, dtype=TRI, offset=84); s = np.fromfile(sp, dtype=TRI, offset=84)
sc = s["v"].mean(1)
box = (sc[:, 0] > x0) & (sc[:, 0] < x1) & (sc[:, 2] > z0) & (sc[:, 2] < 1850)  # scrap floats at 2.15-2.35 m
d, _ = cKDTree(b["v"].mean(1)).query(sc[box], distance_upper_bound=NEW * 2)
add = s[np.where(box)[0][d > NEW]]
m = np.concatenate([b, add])
with open(op, "wb") as f:
    f.write(b"wrx add_new".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print("added", len(add), "->", op, len(m))
