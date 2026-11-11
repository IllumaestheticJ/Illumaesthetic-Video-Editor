"""v3 interior: a seats-out base for the exploded views (user: "show the interior and exploded views").

    python projects/porsche-macan/tools/build_int.py /home/user/media/porsche-macan/comp

Input: comp_explode.stl (from build.py) + the interior part scans (Driver Seat, Pass Seat, Rear Bench Bottom /
Two Thirds Top / Third Top), all levelled with the same transform and checked in place (reg/interior*/sheet.jpg:
the cabin scan fills the door openings exactly; the seats sit in it).
Output: comp_explode_int.stl = comp_explode minus every triangle within 25 mm of a seat scan (the car's own seat
surfaces seen through the openings), plus only NEW geometry from "Interior No Seats" inside the cabin
(|x| < 600 mm keeps its door cards out: the doors are off in this base), and x_seat_*.stl part files.
"""
import os, sys
import numpy as np
from build import L, load, save, near, fill_new

out = sys.argv[1]
base = load(f"{out}/comp_explode.stl"); bc = base["v"].mean(1)
parts = {"seat_driver": "seat_driver", "seat_pass": "seat_pass", "bench_bottom": "bench_bottom",
         "bench_23top": "bench_23top", "bench_13top": "bench_13top"}
drop = np.zeros(len(base), bool)
for name, f in parts.items():
    p = load(f"{L}/{f}.stl"); pc = p["v"].mean(1)
    lo, hi = pc.min(0) - 60, pc.max(0) + 60
    inb = np.all((bc >= lo) & (bc <= hi), 1)
    sel = np.zeros(len(base), bool); sel[inb] = near(bc[inb], pc, 25)
    print(name, "base tris dropped", int(sel.sum()))
    drop |= sel
    save(f"{out}/x_{name}.stl", p)
keep = base[~drop]; kc = bc[~drop]
cabin = load(f"{L}/int_noseats.stl"); cc = cabin["v"].mean(1)
z = (cc.min(0), cc.max(0))
add = fill_new(cabin, kc, [z], [], lambda c: (np.abs(c[:, 0]) < 600) & (c[:, 2] < 1300))
print("cabin fill +", len(add))
save(f"{out}/comp_explode_int.stl", np.concatenate([keep, add]))
