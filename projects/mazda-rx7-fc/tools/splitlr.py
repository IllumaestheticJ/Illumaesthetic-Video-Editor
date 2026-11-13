"""Split a part STL into left (x<cx) / right (x>=cx) halves by triangle centroid (cx = car centre in the levelled frame).
    splitlr.py in.stl out_prefix cx_mm"""
import sys, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84); cx = float(sys.argv[3])
c = m["v"].mean(1)[:, 0]
for tag, sel in (("_l", c < cx), ("_r", c >= cx)):   # levelled +x = car's right after prep (root x = -cx)
    with open(sys.argv[2] + tag + ".stl", "wb") as f:
        f.write(b"rx7 kit half".ljust(80)); f.write(struct.pack("<I", int(sel.sum()))); m[sel].tofile(f)
    print(tag, int(sel.sum()))
