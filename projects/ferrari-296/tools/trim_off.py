"""Engine-bay trims off (v8, user: "im pretty certain there were underhood plastics that weren't included"): the Drive
folder has two "Frunk Trim" scans the earlier fetch skipped. They register onto the ENGINE BAY (rear, mid-engine car;
front = -Y): "Frunk Trim " = left + right side trims around the engine, "Frunk Trim" = the cross panel behind the cabin.
The Engine Bay scan was captured WITH them fitted, so lifting them off would leave a copy behind: cut every composite
triangle within D mm of a trim surface, then split the side trims by x.

    python projects/ferrari-296/tools/trim_off.py comp_v5.stl frunk_trim_2mm.stl "frunk_trim_b_2mm.stl" comp_v8.stl x_etrim_c.stl x_etrim_l.stl x_etrim_r.stl
"""
import sys

import numpy as np
from scipy.spatial import cKDTree

from wheel_off import load, save

D = 7.0


def main(comp, trim_c, trim_lr, out_comp, out_c, out_l, out_r):
    c, a, b = load(comp), load(trim_c), load(trim_lr)
    tv = np.concatenate([a["v"].reshape(-1, 3), b["v"].reshape(-1, 3)])
    # densify: vertices + triangle centroids so the 2 mm mesh has no gaps
    tv = np.concatenate([tv, a["v"].mean(1), b["v"].mean(1)])
    d, _ = cKDTree(tv).query(c["v"].mean(1), distance_upper_bound=D * 2)
    keep = d > D
    print(f"composite {len(c)} tris, cut {np.count_nonzero(~keep)} within {D} mm of the trims")
    save(out_comp, c[keep])
    save(out_c, a)
    x = b["v"].mean(1)[:, 0]
    # Artec frame: car's right = -X
    save(out_r, b[x < 0])
    save(out_l, b[x >= 0])
    print("trim c", len(a), "r", np.count_nonzero(x < 0), "l", np.count_nonzero(x >= 0))


if __name__ == "__main__":
    main(*sys.argv[1:8])
