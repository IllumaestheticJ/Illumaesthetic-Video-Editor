"""Split a diffparts door+T-top component (levelled mm frame) into door and T-top: T-top = roof panel
(z > 1260 and inboard of |x| = 560, sign given by side), door = the rest.
usage: split_door_ttop.py part.stl side(L|R) door_out.stl ttop_out.stl"""
import struct, sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84); c = m["v"].mean(1)
inboard = (c[:, 0] > -560) if sys.argv[2] == "L" else (c[:, 0] < 580)
roof = (c[:, 2] > 1260) & inboard
for sel, out in ((~roof, sys.argv[3]), (roof, sys.argv[4])):
    k = m[sel]
    with open(out, "wb") as f: f.write(b"ive split".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
    print(out, len(k))
