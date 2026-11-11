"""Make the licence plate unreadable: project the embossed characters onto the plate's fitted plane (levelled mm).
Plate found as the near-planar patch behind the rear bumper centre (box below); only triangles within +-12 mm of the
plane and inside the plate rectangle move, so the bumper around it is untouched.
  flatten_plate.py in.stl out.stl"""
import sys, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
BOX = (-240, 200, 1950, 2300, 220, 470)  # x, y, z (levelled mm) around the plate, below the plate lights
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
c = m["v"].mean(1)
b = BOX
sel = (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
P = c[sel]
# rearmost surface in the box = plate face: robust plane by iterating on inliers
cen = np.median(P, 0); n = np.array([0, 1.0, 0])
inl = np.abs((P - cen) @ n) < 40
for _ in range(6):
    Q = P[inl]; cen = Q.mean(0); n = np.linalg.svd(Q - cen, full_matrices=False)[2][2]
    if n[1] < 0: n = -n
    inl = np.abs((P - cen) @ n) < 12
idx = np.where(sel)[0][inl]
v = m["v"][idx].astype(float)
d = (v - cen) @ n
m["v"][idx] = (v - d[..., None] * n).astype(np.float32)
m["n"][idx] = n.astype(np.float32)
with open(sys.argv[2], "wb") as f: f.write(b"miata plate flattened".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(sys.argv[2], "flattened", len(idx), "tris; plane centre", cen.round(), "normal", n.round(3), "spread before", np.percentile(np.abs(d), 95).round(1), "mm")
