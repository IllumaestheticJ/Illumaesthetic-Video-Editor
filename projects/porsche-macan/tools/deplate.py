"""Blank the licence plate (privacy: the scan carries a real, legible registration). Adapted from
mazda-miata-na/tools/deplate.py with the plate box as an argument. Flattens every vertex on the plate face onto its
fitted plane (y = a + b x + c z, levelled mm frame) so the embossed characters disappear and a plain plate remains.
Macan rear plate box (from a rear-most-surface depth map of car3): x -125..200, z 440..605, face tilted ~20 deg, y 2185..2250
(the plate bracket sides at x -140 and +210 protrude further and are excluded).
    deplate.py in.stl out.stl [--box x0,x1,y0,y1,z0,z1]"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
X0, X1, Y0, Y1, Z0, Z1 = -125, 200, 2170, 2265, 440, 605
if "--box" in sys.argv:
    X0, X1, Y0, Y1, Z0, Z1 = (float(v) for v in sys.argv[sys.argv.index("--box") + 1].split(","))
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
v = m["v"].reshape(-1, 3).astype(np.float64)
box = (v[:, 0] > X0) & (v[:, 0] < X1) & (v[:, 2] > Z0) & (v[:, 2] < Z1) & (v[:, 1] > Y0) & (v[:, 1] < Y1)
if box.sum() > 100:
    q = v[box]
    # fit on the OUTERMOST surface only (max y per 10 mm x/z cell): the Macan plate is tilted ~20 deg in front of
    # a flat backing, and a plain fit locks onto the backing and leaves the characters (seen in a close-up render)
    ij = np.floor(q[:, [0, 2]] / 10).astype(np.int64); key = ij[:, 0] * 100000 + ij[:, 1]
    order = np.lexsort((-q[:, 1], key)); first = np.r_[True, key[order][1:] != key[order][:-1]]
    q = q[order[first]]
    A = np.c_[np.ones(len(q)), q[:, 0], q[:, 2]]
    coef = np.linalg.lstsq(A, q[:, 1], rcond=None)[0]
    for _ in range(4):  # refit on the plate face only (drop the recess walls)
        r = q[:, 1] - A @ coef; k = np.abs(r) < 4
        coef = np.linalg.lstsq(A[k], q[k, 1], rcond=None)[0]
    r = v[:, 1] - (coef[0] + coef[1] * v[:, 0] + coef[2] * v[:, 2])
    flat = box & (np.abs(r) < 8)  # characters are embossed ~2-4 mm
    v[flat, 1] -= r[flat]
    m["v"] = v.reshape(-1, 3, 3).astype(np.float32)
    print("plate plane y = %.1f %+.4f x %+.4f z; flattened %d verts" % (*coef, int(flat.sum())))
else:
    print("no plate in box")
with open(sys.argv[2], "wb") as f:
    f.write(b"ive deplate".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
