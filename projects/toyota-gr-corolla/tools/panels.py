"""Split the full GR Corolla scan into body panels for the exploded view (raw Artec mm, shared frame).

    python projects/toyota-gr-corolla/tools/panels.py car4w.stl outdir/

Real part scans are the panels where they exist (front bumper 'Bumper (1.2m)', rear bumper outer + inner side,
diffuser): the car skin within --cut mm of them is removed. Hood, fenders, doors and hatch have no separate
scans, so they are cut from the full car at their seam positions (read off grid_side/grid_top contact sheets).
Wheels, roof, pillars, quarters and sills stay on the base; the 'Chassis Stripped' scan is added beneath
(base.stl = car leftovers + chassis), so lifting a panel shows the real stripped shell under it.
Coordinates: raw mm; front = -Y, car's right = -X (body centre x = -198), floor z = -440.
"""
import os
import struct
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
SC = "/home/user/media/toyota-gr-corolla/scans/"
XC, CUT = -198.0, 12.0
AXLES = {"front": (-2350.0, -110.0), "rear": (290.0, -110.0)}  # (y, z) wheel centres
load = lambda p: np.fromfile(p, dtype=TRI, offset=84)


def save(p, m):
    with open(p, "wb") as f:
        f.write(b"gr-corolla panel".ljust(80))
        f.write(struct.pack("<I", len(m)))
        m.tofile(f)
    print(f"{os.path.basename(p):18s} {len(m):8d}")


car = load(sys.argv[1])
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
c = car["v"].mean(1)
x, y, z = c.T
dx = np.abs(x - XC)
right = x < XC
nx = np.abs(car["n"][:, 0])

near = lambda f: cKDTree(load(SC + f)["v"].mean(1)[::2]).query(c, distance_upper_bound=CUT * 2)[0] < CUT
fb = near("Bumper (1.2m).stl")
rb = near("GR Corolla bumper .stl") | near("GR Corolla bumper inner side.stl") | near("GR Corolla diffuser.stl")
wheel = np.zeros(len(c), bool)
for ay, az in AXLES.values():
    wheel |= (dx > 560) & (np.hypot(y - ay, z - az) < 350)
free = ~(fb | rb | wheel)
side = (dx > 640) | ((z > 330) & (dx > 470) & (nx > 0.35))  # body side incl. door glass (tumblehome)
hood = free & (y > -3080) & (y < -1985) & (dx < 640) & (z > 250)
fender = free & ~hood & (y > -3080) & (y < -1960) & (z > -330) & (dx > 520)
door_f = free & side & (y >= -1960) & (y < -705) & (z > -320) & (z < 600)
door_r = free & side & (y >= -705) & (y < np.where(z > 0, 60, -30)) & (z > -320) & (z < 600)
hatch = free & ~side & (y > 330) & (z > 60) & (dx < 640)
taken = hood | fender | door_f | door_r | hatch
groups = {"hood": hood, "fender_R": fender & right, "fender_L": fender & ~right,
          "door_FR": door_f & right, "door_FL": door_f & ~right, "door_RR": door_r & right, "door_RL": door_r & ~right,
          "hatch": hatch}
for k, m in groups.items():
    save(f"{out}/p_{k}.stl", car[m])
base = car[~(fb | rb | taken)]
save(f"{out}/base_car.stl", base)
ch = load(sys.argv[3]) if len(sys.argv) > 3 else None
if ch is not None:
    # chassis only where it adds structure: > 8 mm from the leftover car skin
    d, _ = cKDTree(base["v"].mean(1)).query(ch["v"].mean(1), distance_upper_bound=16)
    save(f"{out}/base.stl", np.concatenate([base, ch[d > 8]]))
