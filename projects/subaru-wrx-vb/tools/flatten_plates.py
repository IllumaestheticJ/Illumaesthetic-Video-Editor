"""Erase licence-plate characters from scan STLs (raw Artec mm): inside each plate box, vertices within --tol mm of the
plate's fitted plane (median-based robust fit) are projected onto it, so the embossed number disappears and the plate
reads as a blank plate. The car is a customer/shop car - plate numbers never go into a public reel.
    python projects/subaru-wrx-vb/tools/flatten_plates.py in.stl out.stl"""
import struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
# (xmin,xmax, ymin,ymax, zmin,zmax) raw mm, found from point histograms + close-up renders (chk/plate.jpg)
BOXES = {"front": (-250, 130, -2400, -2335, 212, 412), "rear": (-220, 90, 2150, 2265, 665, 885)}
TOL = 9.0
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
v = m["v"].reshape(-1, 3).astype(np.float64)
for name, (x0, x1, y0, y1, z0, z1) in BOXES.items():
    inb = (v[:, 0] > x0) & (v[:, 0] < x1) & (v[:, 1] > y0) & (v[:, 1] < y1) & (v[:, 2] > z0) & (v[:, 2] < z1)
    if inb.sum() < 100:
        print(name, "not in this mesh"); continue
    P = v[inb]
    n = np.array([0.0, 1.0, 0.0]); c = np.median(P, 0)
    for _ in range(6):  # robust plane: keep the dominant (plate face) points
        d = (P - c) @ n
        keep = np.abs(d - np.median(d)) < 6
        Q = P[keep]; c = Q.mean(0)
        _, _, vt = np.linalg.svd(Q - c, full_matrices=False); n = vt[2]
    d = (P - c) @ n
    near = np.abs(d) < TOL
    idx = np.where(inb)[0][near]
    v[idx] -= np.outer(((v[idx] - c) @ n), n)
    print(name, "plane n", n.round(3), "flattened verts", len(idx), "of", int(inb.sum()))
m["v"] = v.reshape(-1, 3, 3).astype("<f4")
with open(sys.argv[2], "wb") as f:
    f.write(b"wrx plates flattened".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print("->", sys.argv[2])
