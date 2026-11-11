"""Drop leftover ground scraps: up-facing (n.z > 0.85) faces within --h mm of the floor (the car's underside faces down),
plus anything below --hmin mm above the floor. Raw scan frame (mm, z up).

    python deground.py in.stl out.stl --floor -1560.46 --h 180 --hmin 40
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write  # noqa: E402
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--floor", type=float, required=True); ap.add_argument("--h", type=float, default=180)
ap.add_argument("--hmin", type=float, default=40)
ap.add_argument("--zone", type=float, nargs=4, action="append", help="ymin ymax h nz_min: extra rule for a Y band (raw mm)")
ap.add_argument("--box", type=float, nargs=7, action="append", help="xmin xmax ymin ymax zmin zmax nz_min: drop faces facing up in a box (props)")
a = ap.parse_args()
d = read(a.inp); c = d["v"].mean(1)
bad = ((d["n"][:, 2] > 0.85) & (c[:, 2] < a.floor + a.h)) | (c[:, 2] < a.floor + a.hmin)
for y0, y1, h, nz in a.zone or []:
    bad |= (c[:, 1] > y0) & (c[:, 1] < y1) & (c[:, 2] < a.floor + h) & (d["n"][:, 2] > nz)
for x0, x1, y0, y1, z0, z1, nz in a.box or []:
    bad |= (c[:, 0] > x0) & (c[:, 0] < x1) & (c[:, 1] > y0) & (c[:, 1] < y1) & (c[:, 2] > z0) & (c[:, 2] < z1) & (d["n"][:, 2] > nz)
print("removed", int(bad.sum()), "of", len(d))
write(a.out, d[~bad])
