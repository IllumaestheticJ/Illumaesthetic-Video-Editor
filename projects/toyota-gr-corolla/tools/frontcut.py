"""Front-bumper-off base, v2 (user on v4: "the front end scan is missing a huge chunk of the car").
v4's remove-diff dropped every car face in the bumper's bbox that the Chassis Stripped scan lacks - which also
deleted the headlights and fender corners (the stripped shell has neither). Here a car face is removed only when it
is BUMPER skin: within --cut mm of the separate bumper scan, or (not on the stripped chassis AND within --skin mm of
the bumper scan) to catch skin that sits a little off the bumper scan at the corners.
    frontcut.py car.stl bumper.stl chassis.stl out.stl --cut 9 --skin 20"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("bumper"); ap.add_argument("chassis"); ap.add_argument("out")
ap.add_argument("--cut", type=float, default=9); ap.add_argument("--skin", type=float, default=20); ap.add_argument("--gap", type=float, default=10)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=DT, offset=84)
car = L(a.car); cc = car["v"].mean(1); bu = L(a.bumper)["v"].mean(1)
lo, hi = bu.min(0) - a.skin, bu.max(0) + a.skin; inz = np.where(np.all((cc >= lo) & (cc <= hi), 1))[0]
db, _ = cKDTree(bu).query(cc[inz], distance_upper_bound=a.skin + 1, workers=-1)
dch, _ = cKDTree(L(a.chassis)["v"].mean(1)).query(cc[inz], distance_upper_bound=a.gap + 1, workers=-1)
drop = (db < a.cut) | ((db < a.skin) & (dch > a.gap))
keep = np.ones(len(car), bool); keep[inz[drop]] = False
print("car", len(car), "-> removed", int(drop.sum()))
out = car[keep]
with open(a.out, "wb") as f:
    f.write(b"grc frontcut".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
