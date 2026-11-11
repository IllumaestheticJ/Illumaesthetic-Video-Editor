"""Triangle count (header) + bbox (mm) of binary STLs, streamed (works on 1.25 GB files)."""
import sys, struct, numpy as np
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
for p in sys.argv[1:]:
    n = struct.unpack("<I", open(p, "rb").read(84)[80:])[0]
    m = np.memmap(p, dtype=TRI, mode="r", offset=84)
    lo, hi = np.full(3, 1e18), np.full(3, -1e18)
    for i in range(0, len(m), 4_000_000):
        v = np.asarray(m[i:i + 4_000_000]["v"]).reshape(-1, 3)
        lo = np.minimum(lo, v.min(0)); hi = np.maximum(hi, v.max(0))
    print(f"{p.split('/')[-1][:44]:44s} tris={n:>10,d} lo={lo.round(0)} hi={hi.round(0)} size={(hi-lo).round(0)}")
