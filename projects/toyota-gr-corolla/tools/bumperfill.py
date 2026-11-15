"""Complete front bumper part (user on v5: "the front bumper was missing a chunk").
The separate bumper scan is torn at its upper corners. Every car face that the bumper-off cut removed is bumper skin
by definition; the ones the bumper scan does not cover (> --gap mm from it) are added to the moving part, so the part
is whole and nothing of it is left behind on the car.
    bumperfill.py car.stl car_cut.stl bumper.stl out.stl --gap 6"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("car_cut"); ap.add_argument("bumper"); ap.add_argument("out")
ap.add_argument("--gap", type=float, default=6)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=DT, offset=84)
car, cut, bu = L(a.car), L(a.car_cut), L(a.bumper)
cc = car["v"].mean(1)
d, _ = cKDTree(cut["v"].mean(1)).query(cc, distance_upper_bound=0.5, workers=-1); removed = np.where(np.isinf(d))[0]
db, _ = cKDTree(bu["v"].mean(1)).query(cc[removed], distance_upper_bound=a.gap + 1, workers=-1)
add = car[removed[db > a.gap]]
print("removed from car", len(removed), "| not covered by the bumper scan -> added to the part", len(add))
out = np.concatenate([bu, add])
with open(a.out, "wb") as f:
    f.write(b"grc bumperfill".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
