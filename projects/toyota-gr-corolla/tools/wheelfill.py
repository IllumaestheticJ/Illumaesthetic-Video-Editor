"""Fill the full-car scan's missing rear wheels from the 'GR Corolla rear' state scan (same Artec frame, 1.9 mm).

    python projects/toyota-gr-corolla/tools/wheelfill.py car_clean.stl "GR Corolla rear.stl" out.stl

Keeps only rear-scan triangles inside the two rear-wheel boxes (raw mm: |x - xc| 550..1000, y -60..650,
z -445..260) that are > --new mm from the car, i.e. the wheel/tyre/brake the full-car capture missed.
The output is prepped with --like car4.json so the car's transform does not change.
"""
import struct
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
XC, NEW = -198.1, 6.0
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
st = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
c = st["v"].mean(1)
dx = np.abs(c[:, 0] - XC)
box = (dx > 550) & (dx < 1000) & (c[:, 1] > -60) & (c[:, 1] < 650) & (c[:, 2] > -445) & (c[:, 2] < 260)
d, _ = cKDTree(car["v"].mean(1)).query(c[box], distance_upper_bound=NEW * 2)
sel = np.where(box)[0][d > NEW]
out = np.concatenate([car, st[sel]])
with open(sys.argv[3], "wb") as f:
    f.write(b"gr-corolla car + rear wheels".ljust(80))
    f.write(struct.pack("<I", len(out)))
    out.tofile(f)
print("car", len(car), "+ wheels", len(sel), "->", sys.argv[3])
