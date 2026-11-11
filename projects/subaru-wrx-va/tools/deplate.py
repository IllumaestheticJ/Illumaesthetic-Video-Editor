"""Blank the rear licence plate (privacy: the scan carries a real, legible registration). Adapted from
projects/mazda-miata-na/tools/deplate.py for this frame (plate on the -X tail face). Box from an x-depth map of the
tail (car_2mm): y -205..120, z 705..880 mm, levelled+cleaned frame. Fits the plate plane x = a + b*y + c*z on the
face, then projects every vertex within 8 mm of it onto the plane - embossed characters vanish, a plain plate stays.
    deplate.py in.stl out.stl"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
Y0, Y1, Z0, Z1, X1 = -205, 120, 705, 880, -1900
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
v = m["v"].reshape(-1, 3).astype(np.float64)
box = (v[:, 1] > Y0) & (v[:, 1] < Y1) & (v[:, 2] > Z0) & (v[:, 2] < Z1) & (v[:, 0] < X1)
if box.sum() > 100:
    q = v[box]
    A = np.c_[np.ones(len(q)), q[:, 1], q[:, 2]]
    coef = np.linalg.lstsq(A, q[:, 0], rcond=None)[0]
    for _ in range(4):
        r = q[:, 0] - A @ coef; k = np.abs(r) < 4
        coef = np.linalg.lstsq(A[k], q[k, 0], rcond=None)[0]
    r = v[:, 0] - (coef[0] + coef[1] * v[:, 1] + coef[2] * v[:, 2])
    flat = box & (np.abs(r) < 8)
    v[flat, 0] -= r[flat]
    m["v"] = v.reshape(-1, 3, 3).astype(np.float32)
    print("plate plane x = %.1f %+.4f y %+.4f z; flattened %d verts" % (*coef, int(flat.sum())))
else:
    print("no plate in", sys.argv[1])
with open(sys.argv[2], "wb") as f:
    f.write(b"wrx deplate".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
