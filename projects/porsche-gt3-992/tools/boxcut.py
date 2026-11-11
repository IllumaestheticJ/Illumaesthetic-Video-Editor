"""Keep triangles whose centroid is inside a box (levelled mm): python boxcut.py in.stl out.stl x0 x1 y0 y1 z0 z1
Used for 2 mm close-up crops (whole 2 mm car = 15M tris; a corner is ~3M)."""
import sys, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
b = [float(x) for x in sys.argv[3:9]]
m = np.memmap(sys.argv[1], dtype=TRI, mode="r", offset=84); keep = []
for i in range(0, len(m), 2_000_000):
    ch = np.array(m[i:i + 2_000_000]); c = ch["v"].mean(1)
    keep.append(ch[(c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])])
m = np.concatenate(keep)
with open(sys.argv[2], "wb") as f:
    f.write(b"gt3 boxcut".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(sys.argv[2], len(m))
