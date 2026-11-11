"""Blank the GR Corolla's licence plate (privacy - the scan carries a real, legible registration).
Replaces the plate face (embossed characters included) with one plain flat panel on its fitted plane.
Adapted from projects/mazda-miata-na/tools/deplate.py. Plate box (raw Artec mm, measured from a y-depth map of
'GR Corolla diffuser.stl'): x -330..5, z -260..-80, face y 1135..1220.
    deplate.py in.stl out.stl
"""
import struct
import sys

import numpy as np

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
X0, X1, Z0, Z1, Y0, Y1 = -330, 5, -260, -80, 1135, 1220
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
v = m["v"].reshape(-1, 3).astype(np.float64)
box = (v[:, 0] > X0) & (v[:, 0] < X1) & (v[:, 2] > Z0) & (v[:, 2] < Z1) & (v[:, 1] > Y0) & (v[:, 1] < Y1)
if box.sum() > 100:
    q = v[box]
    A = np.c_[np.ones(len(q)), q[:, 0], q[:, 2]]
    coef = np.linalg.lstsq(A, q[:, 1], rcond=None)[0]
    for _ in range(4):  # refit on the plate face only
        r = q[:, 1] - A @ coef
        k = np.abs(r - np.median(r)) < 4
        coef = np.linalg.lstsq(A[k], q[k, 1], rcond=None)[0]
    # delete the plate face (characters included) and replace it with one plain flat panel on the fitted plane:
    # flattening in place left z-fighting blobs where the raised characters had been
    r = v[:, 1] - (coef[0] + coef[1] * v[:, 0] + coef[2] * v[:, 2])
    on = (box & (np.abs(r) < 8)).reshape(-1, 3).all(1)
    pv = v.reshape(-1, 3, 3)[on].reshape(-1, 3)
    xa, xb = np.percentile(pv[:, 0], [0.5, 99.5]); za, zb = np.percentile(pv[:, 2], [0.5, 99.5])
    Y = lambda x, z: coef[0] + coef[1] * x + coef[2] * z - 0.3
    # a 60 x 30 grid (3,600 tris) so `prep --drop-islands` doesn't delete it as debris
    gx, gz = np.linspace(xa, xb, 61), np.linspace(za, zb, 31)
    tris = []
    for i in range(60):
        for j in range(30):
            q = [(gx[i], gz[j]), (gx[i + 1], gz[j]), (gx[i + 1], gz[j + 1]), (gx[i], gz[j + 1])]
            P = [(x, Y(x, z), z) for x, z in q]
            tris += [[P[0], P[2], P[1]], [P[0], P[3], P[2]]]  # wound so the normal faces +y (out of the tail)
    quad = np.zeros(len(tris), TRI)
    quad["v"] = tris
    quad["n"] = [0, 1, 0]
    m = np.concatenate([m[~on], quad])
    print("plate plane y = %.1f %+.4f x %+.4f z; replaced %d tris with a %.0f x %.0f mm panel"
          % (*coef, int(on.sum()), xb - xa, zb - za))
else:
    print("no plate in", sys.argv[1])
with open(sys.argv[2], "wb") as f:
    f.write(b"gr-corolla deplate".ljust(80))
    f.write(struct.pack("<I", len(m)))
    m.tofile(f)
