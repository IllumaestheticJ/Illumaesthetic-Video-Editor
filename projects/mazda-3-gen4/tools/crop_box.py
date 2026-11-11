"""Crop a levelled STL (mm) to a box given in the PREPPED frame (metres, car4.json offsets), for close-up shots.
    crop_box.py in.stl out.stl car4.json xmin,xmax ymin,ymax zmin,zmax"""
import json, struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
src, out, cj = sys.argv[1:4]
J = json.load(open(cj)); s = J["unit_scale"]; r = np.array(J["root_location"])
lo = [float(v.split(",")[0]) for v in sys.argv[4:7]]; hi = [float(v.split(",")[1]) for v in sys.argv[4:7]]
m = np.memmap(src, dtype=TRI, mode="r", offset=84); keep = []
for i in range(0, len(m), 2_000_000):
    ch = np.array(m[i:i + 2_000_000]); c = ch["v"].mean(1) * s + r
    keep.append(ch[np.all((c >= lo) & (c <= hi), axis=1)])
k = np.concatenate(keep)
with open(out, "wb") as f: f.write(b"crop".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(out, len(k))
