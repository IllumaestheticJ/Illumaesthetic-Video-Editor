"""Make the scanned licence plates unreadable: inside each plate box, fit a plane to the plate (median normal ~ +-Y) and
project every vertex within 30 mm of it onto the plane - the embossed characters flatten, the plate stays a smooth slab.
(v1 snapped to a 25 mm grid: left spiky blocks - rejected after looking at the previews.) Boxes from orthographic front/rear renders (reg/plates.jpg), Blender m.
    deplate.py frame.json in.stl out.stl"""
import json, struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
root = np.array(json.load(open(sys.argv[1]))["root_location"]) * 1000
BOXES = [(-0.58, -0.20, -2.40, -2.10, 0.52, 0.74), (-0.22, 0.17, 2.08, 2.40, 0.42, 0.64)]
m = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
v = m["v"].reshape(-1, 3).astype(np.float64)
b = (v + root) / 1000
for x0, x1, y0, y1, z0, z1 in BOXES:
    bx = (b[:, 0] > x0) & (b[:, 0] < x1) & (b[:, 1] > y0) & (b[:, 1] < y1) & (b[:, 2] > z0) & (b[:, 2] < z1)
    q = v[bx]
    # plate = the outermost flat layer along Y: robust plane through points near the extreme y
    sgn = 1 if y0 > 0 else -1
    ext = np.percentile(q[:, 1] * sgn, 97) * sgn
    pts = q[np.abs(q[:, 1] - ext) < 25]
    cen = np.median(pts, 0)
    for _ in range(3):
        n = np.linalg.svd(pts - cen, full_matrices=False)[2][2]
        r = (pts - cen) @ n
        pts = pts[np.abs(r) < 6]; cen = pts.mean(0)
    dist = (q - cen) @ n
    near = np.abs(dist) < 30
    q[near] -= np.outer(dist[near], n)
    v[bx] = q
    print("plate box", (x0, y0), "flattened", int(near.sum()), "verts, normal", n.round(3))
m["v"] = v.reshape(-1, 3, 3).astype(np.float32)
with open(sys.argv[3], "wb") as f:
    f.write(b"infiniti-g35 deplate".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print("->", sys.argv[3])
