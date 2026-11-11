"""Quick stats of binary STLs: header tri count, bbox (mm), percentiles. usage: stlstat.py a.stl [b.stl ...]"""
import sys, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
for p in sys.argv[1:]:
    with open(p, "rb") as f:
        f.seek(80); n = struct.unpack("<I", f.read(4))[0]
    m = np.memmap(p, dtype=TRI, mode="r", offset=84)
    c = np.asarray(m["v"][::max(1, len(m) // 400000)]).mean(1)
    lo, hi = np.percentile(c, 0.5, 0), np.percentile(c, 99.5, 0)
    print(f"{p.split('/')[-1]:45s} tris={n:,} lo={lo.round(0)} hi={hi.round(0)} ext={(hi-lo).round(0)}")
