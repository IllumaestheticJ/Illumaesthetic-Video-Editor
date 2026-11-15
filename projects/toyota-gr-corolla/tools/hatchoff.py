"""Hatch-off base: BASE minus the hatch panel's faces (within --d mm of the panel cut from the closed car) + the cargo
area from the 'trunk open (removed)' state scan (cargo.stl, tools/cargofill.py). Used for every shot after the hatch
comes off so the car never changes state between shots.
    hatchoff.py base.stl p_hatch.stl cargo.stl out.stl --d 1.5"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
DT = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("base"); ap.add_argument("hatch"); ap.add_argument("cargo"); ap.add_argument("out")
ap.add_argument("--d", type=float, default=1.5)
a = ap.parse_args()
L = lambda p: np.fromfile(p, dtype=DT, offset=84)
b, h, c = L(a.base), L(a.hatch), L(a.cargo)
d, _ = cKDTree(h["v"].mean(1)).query(b["v"].mean(1), distance_upper_bound=a.d + 1, workers=-1)
keep = d > a.d; print("base", len(b), "-> hatch faces removed", int((~keep).sum()), "| cargo +", len(c))
out = np.concatenate([b[keep], c])
with open(a.out, "wb") as f:
    f.write(b"grc hatchoff".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
