"""Drop triangles below a height (levelled frame, mm): python zcut.py in.stl out.stl -10
GT3 full car: 8 debris triangles at z -94..-232 mm (below the scanned ground) set prep's floor 0.23 m too low."""
import sys, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
m = m[m["v"][:, :, 2].min(1) > float(sys.argv[3])]
with open(sys.argv[2], "wb") as f:
    f.write(b"gt3 zcut".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print(len(m))
