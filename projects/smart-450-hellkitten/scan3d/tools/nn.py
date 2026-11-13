"""median NN distance (mm) from sample of A to B. nn.py A.stl B.stl"""
import sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)
a, b = L(sys.argv[1]), L(sys.argv[2])
a = a[a[:, 2] > np.percentile(a[:, 2], 20)]
rng = np.random.default_rng(0); a = a[rng.choice(len(a), 60000, replace=False)]
d, _ = cKDTree(b).query(a, distance_upper_bound=200)
d = d[np.isfinite(d)]
print(sys.argv[1], "->", sys.argv[2], "p50 %.1f p75 %.1f  within5mm %.0f%%  within20 %.0f%%" % (np.median(d), np.percentile(d, 75), 100*(d < 5).mean(), 100*(d<20).mean()))
