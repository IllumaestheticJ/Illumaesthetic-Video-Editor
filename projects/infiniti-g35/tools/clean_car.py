"""Drop scan debris below the levelled ground (Z=0 after tools/level.py): a pit/jack scraps under the car down to
-167 mm and floor scraps. Tyres touch Z~0, so the cut is at +4 mm.
    clean_car.py in.stl out.stl [zcut_mm]"""
import struct, sys
import numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84)
z = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
k = m[m["v"][:, :, 2].min(1) > z]
with open(sys.argv[2], "wb") as f:
    f.write(b"infiniti-g35 clean_car".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print("dropped", len(m) - len(k), "->", sys.argv[2])
