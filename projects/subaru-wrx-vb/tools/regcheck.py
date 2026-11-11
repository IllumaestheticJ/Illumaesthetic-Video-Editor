"""Registration check (raw Artec mm): for each part/state scan, distance from its triangle centres to the nearest
full-car point. A scan in the car's frame sits ON the car where it overlaps (median ~1-3 mm at 3-4 mm decimation);
a scan in its own frame shows overlap ~0 % and medians of tens/hundreds of mm. Also prints the bbox (raw mm).
    python projects/subaru-wrx-vb/tools/regcheck.py car_4mm.stl part1.stl part2.stl ...
Based on projects/huracan-evo/tools/regcheck.py."""
import os, sys
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
car = load(sys.argv[1]); tree = cKDTree(car)
for f in sys.argv[2:]:
    p = load(f)
    p = p[:: max(1, len(p) // 300000)]
    d, _ = tree.query(p, distance_upper_bound=500)
    near = d < 10
    med = np.median(d[near]) if near.any() else float("nan")
    lo, hi = p.min(0), p.max(0)
    print(f"{os.path.basename(f)[:-4]:38s} n={len(p):6d} on-car<10mm={near.mean()*100:5.1f}% med={med:4.1f}mm  "
          f"x[{lo[0]:6.0f},{hi[0]:6.0f}] y[{lo[1]:6.0f},{hi[1]:6.0f}] z[{lo[2]:5.0f},{hi[2]:5.0f}]")
