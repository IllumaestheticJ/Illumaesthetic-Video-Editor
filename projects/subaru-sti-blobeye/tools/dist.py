"""Part -> car surface distance on the overlap (both in the same frame, mm). dist.py car.stl part.stl ..."""
import sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
pts = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
tree = cKDTree(pts(sys.argv[1]))
for p in sys.argv[2:]:
    c = pts(p); c = c[:: max(1, len(c) // 200000)]
    d, _ = tree.query(c); o = d < 15
    print(f"{p.split('/')[-1]:28s} overlap<15mm {o.mean()*100:5.1f}%  p50 {np.median(d[o]):5.2f}  p75 {np.percentile(d[o],75):5.2f}  <3mm {np.mean(d[o]<3)*100:4.0f}%")
