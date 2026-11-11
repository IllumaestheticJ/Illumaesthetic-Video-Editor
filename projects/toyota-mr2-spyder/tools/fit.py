"""Registration quality of part STLs already in the car frame: for part points within 30 mm of the car,
share within 3/6 mm and their median distance (a registered part sits at the decimation noise floor ~1.5-3 mm).
  fit.py car_L.stl part1.stl [part2.stl ...] [--ymin -2100 --ymax 2100]"""
import sys, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
args = sys.argv[1:]
yr = (-1e9, 1e9)
if "--ymin" in args:
    i = args.index("--ymin"); yr = (float(args[i + 1]), float(args[i + 3])); del args[i:i + 4]
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)
car = L(args[0]); car = car[(car[:, 1] > yr[0]) & (car[:, 1] < yr[1])]
t = cKDTree(car[::2])
for p in args[1:]:
    q = L(p)[::5]; d, _ = t.query(q, distance_upper_bound=60)
    n = d < 30
    print(f"{p.split('/')[-1]:40s} near30 {n.mean()*100:5.1f}%  <3mm {np.mean(d<3)*100:5.1f}%  <6mm {np.mean(d<6)*100:5.1f}%  median(near) {np.median(d[n]):5.2f} mm")
