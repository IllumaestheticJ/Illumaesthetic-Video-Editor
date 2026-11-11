"""Quick STL stats: triangle count (header), bbox (raw units), centroid. Streams in chunks.
    python projects/honda-s2000/tools/stlinfo.py a.stl [b.stl ...]"""
import sys, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
for p in sys.argv[1:]:
    m = np.memmap(p, dtype=TRI, offset=84, mode="r")
    lo = np.full(3, np.inf); hi = -lo; s = np.zeros(3); n = len(m)
    for i in range(0, n, 2_000_000):
        v = np.asarray(m["v"][i:i + 2_000_000]).reshape(-1, 3)
        lo = np.minimum(lo, v.min(0)); hi = np.maximum(hi, v.max(0)); s += v.sum(0)
    hdr = int(np.fromfile(p, "<u4", 1, offset=80)[0])
    print(f"{p.split('/')[-1]:40s} tris={hdr:,} lo={np.round(lo)} hi={np.round(hi)} size={np.round(hi-lo)} mean={np.round(s/(3*n))}")
