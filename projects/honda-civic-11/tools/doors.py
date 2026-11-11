"""Right-side doors from the full car, using the 'Door Open' state scan as the doors-open body.

    python doors.py car.stl door_open.stl outdir car4.json

door = full-car triangles on the right flank (prepped x > 0.45) inside the door outline (side view y,z traced on
the panel gaps, prepped m) AND > 8 mm from the Door Open scan (surfaces still there with the doors open: sill,
arches, jambs). Writes front_door.stl, rear_door.stl, doors_base.stl (car minus doors + Door Open scan where it adds).
"""
import json, os, sys
import numpy as np
from matplotlib.path import Path
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write  # noqa: E402

FRONT = [(-0.12, 0.45), (1.05, 0.40), (1.02, 1.0), (0.95, 1.04), (0.6, 1.26), (0.3, 1.415), (-0.15, 1.465), (-0.12, 0.95)]
REAR = [(-0.86, 0.47), (-0.12, 0.45), (-0.12, 0.95), (-0.15, 1.465), (-0.83, 1.435), (-1.08, 1.15), (-0.97, 0.9), (-0.92, 0.6)]
car_p, do_p, out, like = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
pj = json.load(open(like)); s = pj["unit_scale"]; rl = np.array(pj["root_location"])
car = read(car_p); do = read(do_p)
cp = car["v"].mean(1) * s + rl
dp = do["v"].reshape(-1, 3) * s + rl
d, _ = cKDTree(dp).query(cp, distance_upper_bound=0.02)
flank = (cp[:, 0] > 0.45) & ((d > 0.008) | (cp[:, 2] > 0.55)) & ((car["n"][:, 0] > 0.1) | (cp[:, 2] < 1.0)) & ((car["n"][:, 0] > 0.3) | (cp[:, 2] < 1.3))
taken = np.zeros(len(car), bool)
for name, poly in (("front_door", FRONT), ("rear_door", REAR)):
    m = flank & Path(poly).contains_points(cp[:, 1:3]) & ~taken
    taken |= m
    write(f"{out}/{name}.stl", car[m]); print(name, int(m.sum()))
# doors-open body = car minus doors + Door Open triangles not already on the car (jamb faces, inner sill)
dc = do["v"].mean(1) * s + rl
d2, _ = cKDTree(cp[~taken]).query(dc, distance_upper_bound=0.02)
add = (d2 > 0.006) & (dc[:, 2] > 0.3) & (dc[:, 0] < 0.92)   # inside the body only: the open doors' edges stick out
print("door-open tris added", int(add.sum()))
write(f"{out}/doors_base_car.stl", car[~taken])
write(f"{out}/doors_open_add.stl", do[add])
