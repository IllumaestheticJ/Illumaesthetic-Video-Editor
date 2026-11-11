"""Blank the licence plate: flatten every vertex on the plate face (levelled frame, mm) onto its fitted plane, so the
embossed characters disappear and a plain plate remains (privacy - the scan carries a real registration).
Plate box measured from a y-depth map of the car's tail: x -296..70, z 574..734, face y 1612-1648 (recessed).
    deplate.py in.stl out.stl"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
X0, X1, Z0, Z1, Y0, Y1 = -296, 70, 574, 734, 1595, 1660
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
v = m["v"].reshape(-1, 3).astype(np.float64)
box = (v[:, 0] > X0) & (v[:, 0] < X1) & (v[:, 2] > Z0) & (v[:, 2] < Z1) & (v[:, 1] > Y0) & (v[:, 1] < Y1)
if box.sum() > 100:
    q = v[box]
    A = np.c_[np.ones(len(q)), q[:, 0], q[:, 2]]
    coef = np.linalg.lstsq(A, q[:, 1], rcond=None)[0]
    for _ in range(3):  # refit on the plate face only (drop the recess walls)
        r = q[:, 1] - A @ coef; k = np.abs(r) < 4
        coef = np.linalg.lstsq(A[k], q[k, 1], rcond=None)[0]
    r = v[:, 1] - (coef[0] + coef[1] * v[:, 0] + coef[2] * v[:, 2])
    flat = box & (np.abs(r) < 8)
    v[flat, 1] -= r[flat]
    m["v"] = v.reshape(-1, 3, 3).astype(np.float32)
    print("plate plane y = %.1f %+.4f x %+.4f z; flattened %d verts" % (*coef, int(flat.sum())))
with open(sys.argv[2], "wb") as f:
    f.write(b"ive deplate".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
