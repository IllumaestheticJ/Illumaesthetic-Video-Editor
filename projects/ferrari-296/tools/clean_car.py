"""Remove known scan debris from the full-car STL (raw mm, Artec frame). Boxes found by inspecting renders."""
import struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
BOXES = [  # (xmin,xmax, ymin,ymax, zmin,zmax) raw mm
    (-1000, -500, -2700, -1900, -900, -630),   # strap/scrap hanging under the front bumper (car's right)
]
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
c = m["v"].mean(1)
drop = np.zeros(len(m), bool)
for x0, x1, y0, y1, z0, z1 in BOXES:
    drop |= (c[:, 0] > x0) & (c[:, 0] < x1) & (c[:, 1] > y0) & (c[:, 1] < y1) & (c[:, 2] > z0) & (c[:, 2] < z1)
# Second pass (needs the bumper scans): the strap also overlaps the bumper's height, so in this box
# drop only triangles > 10 mm from the bumper outer/inner scans (real bumper surface is kept).
if len(sys.argv) > 3:
    from scipy.spatial import cKDTree
    ref = np.concatenate([np.fromfile(f, dtype=TRI, offset=84)["v"].reshape(-1, 3) for f in sys.argv[3:]])
    box = (c[:, 0] > -900) & (c[:, 0] < -600) & (c[:, 1] > -2660) & (c[:, 1] < -2250) & (c[:, 2] > -660) & (c[:, 2] < -440)
    d, _ = cKDTree(ref).query(c[box])
    drop[np.where(box)[0][d > 10]] = True
k = m[~drop]
with open(sys.argv[2], "wb") as f:
    f.write(b"ferrari-296 clean_car".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print("dropped", int(drop.sum()), "->", sys.argv[2])
