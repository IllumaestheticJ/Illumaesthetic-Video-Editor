"""Registration check of part/state scans against one or more full-car scans (raw Artec frames, mm, 4 mm decimated).
For each part: % of points within 15 mm of the car and the median distance of those. Same-frame parts show ~2-4 mm
medians and high overlap; a part in its own frame shows near-zero overlap.
  regcheck.py car1.stl [car2.stl] -- part1.stl part2.stl ..."""
import sys, os, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
i = sys.argv.index("--"); cars, parts = sys.argv[1:i], sys.argv[i + 1:]
trees = [(os.path.basename(c), cKDTree(load(c))) for c in cars]
for p in parts:
    q = load(p); q = q[:: max(1, len(q) // 150000)]
    row = f"{os.path.basename(p)[:-4]:38s}"
    for name, t in trees:
        d, _ = t.query(q, distance_upper_bound=60)
        near = d < 15
        med = np.median(d[near]) if near.any() else np.nan
        row += f" | {name[:-4]}: ov={near.mean()*100:5.1f}% med={med:5.2f}"
    print(row, flush=True)
