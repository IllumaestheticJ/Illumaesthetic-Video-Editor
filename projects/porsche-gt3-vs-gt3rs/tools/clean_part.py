"""Drop part-scan debris: keep only triangles within --max mm of the full car (levelled mm frames).
    python projects/porsche-gt3rs-992/tools/clean_part.py car_4mm.stl part.stl out.stl [--max 100]"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("part"); ap.add_argument("out")
ap.add_argument("--max", type=float, default=100.0); a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84)["v"].mean(1)
m = np.fromfile(a.part, dtype=TRI, offset=84); c = m["v"].mean(1)
lo, hi = c.min(0) - 300, c.max(0) + 300
car = car[np.all((car > lo) & (car < hi), 1)]
d, _ = cKDTree(car).query(c, distance_upper_bound=a.max)
k = m[np.isfinite(d)]
with open(a.out, "wb") as f:
    f.write(b"gt3 clean_part".ljust(80)); f.write(struct.pack("<I", len(k))); k.tofile(f)
print(a.part.split("/")[-1], len(m), "->", len(k))
