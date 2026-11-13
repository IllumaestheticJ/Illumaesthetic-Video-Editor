"""Fender off -> chassis-side body (v9, user: "the fender off the car should show the chassis-side body under the car").
Through v8 the composite still had the car's fender skin (61k triangles within 5 mm of the Fender 2 scan), so the fender
lifted off and an identical fender stayed on the car. Cut the composite within CUT mm of the fender, then fill from the
fender-off "Front Fully Removed" state scans: only triangles > NEW mm from what's left (inner arch, A-pillar mount, inner
panel and structure the car scan never saw), inside the fender bbox + PAD, right side only, below the propped hood.

    python fender_off.py comp_v8b.stl fender_2_2mm.stl comp_v9.stl front_fully_removed_2mm.stl [front_fully_removed_2_2mm.stl]
"""
import sys

import numpy as np
from scipy.spatial import cKDTree

from composite import load, save

CUT, NEW, PAD, ZMAX = 9.0, 7.0, 60.0, 140.0


def main(comp, fender, out, *fills):
    c, f = load(comp), load(fender)
    fv = np.concatenate([f["v"].reshape(-1, 3), f["v"].mean(1)])
    d, _ = cKDTree(fv).query(c["v"].mean(1), distance_upper_bound=CUT * 2)
    rest = c[d > CUT]
    print(f"cut {len(c) - len(rest)} fender-skin triangles")
    lo, hi = fv.min(0) - PAD, fv.max(0) + PAD
    hi[2] = min(hi[2], ZMAX)
    tree = cKDTree(np.concatenate([rest["v"].reshape(-1, 3), rest["v"].mean(1)]))
    add = []
    for p in fills:
        s = load(p)
        cc = s["v"].mean(1)
        zone = np.all((cc > lo) & (cc < hi), axis=1) & (cc[:, 0] < -450)
        dd, _ = tree.query(cc[zone], distance_upper_bound=NEW * 2)
        new = s[zone][dd > NEW]
        print(f"{p.rsplit('/', 1)[-1]}: zone {zone.sum()}, new {len(new)}")
        add.append(new)
        tree = cKDTree(np.concatenate([tree.data, new["v"].reshape(-1, 3)]))  # 2nd capture fills only what the 1st missed
    save(out, np.concatenate([rest] + add))


if __name__ == "__main__":
    main(*sys.argv[1:])
