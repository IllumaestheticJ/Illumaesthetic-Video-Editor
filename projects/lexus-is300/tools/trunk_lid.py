"""Trunk lid from the full-car scan (the OEM Trunk part scan is only the lid's rear face, ragged on top, so it
can't be the animated panel itself; it defines the lid's rear face and width).
lid = car tris on the rear deck (y > HINGE_Y, z > DECK_Z, |x| < lid half-width from the OEM scan) plus car tris
within 12 mm of the OEM lid's main body, minus anything within 12 mm of the rear bumper part scan.
Levelled mm (nose -Y, up +Z).   python trunk_lid.py car_lv.stl oemtrunk_lv.stl rearbumper_lv.stl out.stl
"""
import struct, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
HINGE_Y, DECK_Z = 1565.0, 250.0
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84); cc = car["v"].mean(1)
oem = np.fromfile(sys.argv[2], dtype=TRI, offset=84)["v"].mean(1)
rb = np.fromfile(sys.argv[3], dtype=TRI, offset=84)["v"].mean(1)
v = np.floor((oem - oem.min(0)) / 15).astype(int)
g = np.zeros(v.max(0) + 1, bool); g[tuple(v.T)] = True
lab, n = ndimage.label(g, structure=np.ones((3, 3, 3)))
big = np.argmax(ndimage.sum(g, lab, range(1, n + 1))) + 1
main = oem[lab[tuple(v.T)] == big]
print("OEM lid main body", len(main), "of", len(oem), main.min(0).round(), main.max(0).round())
xh = np.abs(main[:, 0]).max() - 15
d_oem, _ = cKDTree(main).query(cc, distance_upper_bound=30)
d_rb, _ = cKDTree(rb).query(cc, distance_upper_bound=30)
deck = (cc[:, 1] > HINGE_Y) & (cc[:, 2] > DECK_Z) & (np.abs(cc[:, 0]) < xh)
face = (d_oem < 12) & (cc[:, 2] > main[:, 2].min() - 10) & (cc[:, 1] > HINGE_Y)
sel = (deck | face) & ~(d_rb < 12)
m = car[sel]
print("lid tris", len(m), m["v"].reshape(-1, 3).min(0).round(), m["v"].reshape(-1, 3).max(0).round())
with open(sys.argv[4], "wb") as f:
    f.write(b"is300 trunk lid (from car)".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
