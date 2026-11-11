"""Remove the two jack stands under the car (seen in the orthographic side render; located by a z<0.30 m occupancy grid).
Boxes are in prepped Blender metres (frame.json root applied); input/output are raked mm STLs (tools/rake.py).
    stands.py frame.json in.stl out.stl"""
import json, struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
root = np.array(json.load(open(sys.argv[1]))["root_location"]) * 1000
BOXES = [  # x0,x1, y0,y1, z0,z1 (Blender m)
    (0.45, 0.80, 0.45, 0.85, -1, 0.30),    # stand under the +X sill, mid car
    (0.45, 0.68, -1.32, -0.88, -1, 0.30),  # stand behind the +X front wheel
]
m = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
b = (m["v"].mean(1) + root) / 1000
drop = np.zeros(len(m), bool)
for x0, x1, y0, y1, z0, z1 in BOXES:
    drop |= (b[:, 0] > x0) & (b[:, 0] < x1) & (b[:, 1] > y0) & (b[:, 1] < y1) & (b[:, 2] > z0) & (b[:, 2] < z1)
k = m[~drop]
with open(sys.argv[3], "wb") as f:
    f.write(b"infiniti-g35 stands".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print("dropped", int(drop.sum()), "->", sys.argv[3])
