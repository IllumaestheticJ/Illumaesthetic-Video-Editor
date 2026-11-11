"""v3 cleaning (replaces ive crop + floorcut z<8): the RANSAC 'ground' of level.json is the car's flat UNDERTRAY - the
tyres hang 165 mm below it and no floor was scanned. Keep everything inside the car's XY footprint down to the tyre
bottoms; drop only what lies outside the footprint or below the tyres.
  clean2.py in.stl out.stl [zmin=-180] [pad=15]"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
FOOT = (-1076.0, 1089.0, -2311.0, 2607.0)  # levelled mm, measured on the cropped full car (mirrors included)
d = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c = d["v"].mean(1)
zmin = float(sys.argv[3]) if len(sys.argv) > 3 else -180.0
pad = float(sys.argv[4]) if len(sys.argv) > 4 else 15.0
k = d[(c[:, 0] > FOOT[0] - pad) & (c[:, 0] < FOOT[1] + pad) & (c[:, 1] > FOOT[2] - pad) & (c[:, 1] < FOOT[3] + pad) & (c[:, 2] > zmin)]
with open(sys.argv[2], "wb") as f:
    f.write(b"ive clean2".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(sys.argv[2], len(d), "->", len(k))
