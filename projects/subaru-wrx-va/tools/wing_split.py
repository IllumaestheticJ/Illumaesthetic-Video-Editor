"""Split the STI wing off the car (levelled+cleaned mm STLs).
  wing_split.py base.stl wing_scan.stl base_out.stl wing_out.stl
Wing.stl (2024-04) holds the uprights + blade underside; the car scan holds the blade's top skin. So:
- wing zone = Wing.stl bbox + 25 mm (XY), z above (wing feet - 25 mm) so the tail panel below the lid never counts as deck
- deck height per 20 mm XY cell = lowest base triangle in that column inside the zone (the deck is the lowest surface)
- base triangles more than LIFT mm above their column's deck AND (within 40 mm of Wing.stl or >120 mm above the deck) -> wing
- wing part = those triangles + Wing.stl triangles farther than 3 mm from them (underside / uprights the car lacks)
"""
import struct
import sys

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
LIFT, CELL = 10.0, 20.0
bp, wp, bo, wo = sys.argv[1:5]
base = np.fromfile(bp, dtype=TRI, offset=84); wing = np.fromfile(wp, dtype=TRI, offset=84)
bc, wc = base["v"].mean(1), wing["v"].mean(1)
lo, hi = wc.min(0) - 25, wc.max(0) + 25
zone = np.all((bc[:, :2] >= lo[:2]) & (bc[:, :2] <= hi[:2]), 1) & (bc[:, 2] > wc[:, 2].min() - 25)
zi = np.where(zone)[0]
key = np.floor(bc[zi, :2] / CELL).astype(np.int64)
k = key[:, 0] * 100000 + key[:, 1]
u, inv = np.unique(k, return_inverse=True)
deck = np.full(len(u), np.inf); np.minimum.at(deck, inv, bc[zi, 2])
# columns whose lowest point is already high (only wing in them: the blade overhangs the deck edge) -> whole column is wing
dw, _ = cKDTree(wc).query(bc[zi], distance_upper_bound=50)
# lifted AND (touching the wing scan, or blade-high): keeps the lid's raised rear lip on the car
up = (bc[zi, 2] > deck[inv] + LIFT) & ((dw < 40) | (bc[zi, 2] > deck[inv] + 120))
over = deck[inv] > np.percentile(deck, 30) + 120  # blade-only columns sit ~200 mm above the lid
w_sel = np.zeros(len(base), bool); w_sel[zi[up | over]] = True
wing_from_car = base[w_sel]
d, _ = cKDTree(wing_from_car["v"].mean(1)).query(wc, distance_upper_bound=6)
part = np.concatenate([wing_from_car, wing[d > 3]])
for p, m in ((bo, base[~w_sel]), (wo, part)):
    with open(p, "wb") as f:
        f.write(b"wrx wing_split".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
print("wing from car", int(w_sel.sum()), "+ wing scan", int((d > 3).sum()), "| base", int((~w_sel).sum()))
