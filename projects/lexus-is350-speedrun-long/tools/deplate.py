"""Flatten both licence plates of the IS350 (9JTY488) full-car scan (brief: plate must not be legible). Copied from projects/lexus-is350/tools/deplate.py with this car's boxes.
every vertex on a plate face is projected onto the plate's fitted plane, so the embossed characters disappear and a plain
plate remains. Levelled frame (mm, nose -Y); boxes measured from y-depth maps of the nose/tail (chk/depth_*.png).
    deplate.py in.stl out.stl"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
# name: x0, x1, z0, z1, side (-1 front: face = min y, +1 rear: face = max y)
PLATES = {"front": (-130, 195, 320, 505, -1), "rear": (-100, 265, 670, 825, 1)}  # 9JTY488 car, levelled with scan-process level.py (nose -Y); boxes from tools faceview depth maps
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
v = m["v"].reshape(-1, 3).astype(np.float64)
for name, (x0, x1, z0, z1, side) in PLATES.items():
    inb = (v[:, 0] > x0) & (v[:, 0] < x1) & (v[:, 2] > z0) & (v[:, 2] < z1)
    inb &= (v[:, 1] < -2400) if side < 0 else (v[:, 1] > 1700)
    if inb.sum() < 200:
        print(name, "not in this mesh"); continue
    q = v[inb]; face = np.percentile(q[:, 1] * side, 97) * side      # outermost surface in the box = plate face
    box = inb & (np.abs(v[:, 1] - face) < 25)
    q = v[box]; A = np.c_[np.ones(len(q)), q[:, 0], q[:, 2]]
    coef = np.linalg.lstsq(A, q[:, 1], rcond=None)[0]
    for _ in range(4):
        r = q[:, 1] - A @ coef; k = np.abs(r) < 4
        coef = np.linalg.lstsq(A[k], q[k, 1], rcond=None)[0]
    r = v[:, 1] - (coef[0] + coef[1] * v[:, 0] + coef[2] * v[:, 2])
    flat = box & (np.abs(r) < 8)
    v[flat, 1] -= r[flat]
    print("%s plate plane y = %.1f %+.4f x %+.4f z; flattened %d verts" % (name, *coef, int(flat.sum())))
m["v"] = v.reshape(-1, 3, 3).astype(np.float32)
with open(sys.argv[2], "wb") as f:
    f.write(b"ive deplate".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
