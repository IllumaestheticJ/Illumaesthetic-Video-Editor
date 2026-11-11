"""v2 explode base: base_explode + side-panel state scans + under-rear-bumper fill (raw STL, mm, car frame).

    python projects/a90-supra/tools/composite_v2.py /home/user/media/work/a90/base_explode.stl \
        /home/user/media/work/a90/new/base_v2.stl

Lessons applied (ferrari-296 / lexus-is350 / mazda-3): splice by SURFACE DISTANCE, not by bbox.
  1. drop base tris within --cut mm of each removable panel (upper skirt, lower skirt, door trim)
  2. add each state scan's tris that are > --fill mm from the trimmed base AND inside its own zone box
     (the panel bbox it replaces, +30 mm) -> no duplicated shells, no stray fragments elsewhere
  3. Under Rear Bumper: only the hollow behind the rear bumper (x < -1270 mm raw), > --fill mm from base
"""
import argparse
import struct

import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
N = "/home/user/media/work/a90/new/"


def load(p):
    return np.fromfile(p, dtype=TRI, offset=84)


def near(src_c, ref_pts, d):
    dd, _ = cKDTree(ref_pts).query(src_c, distance_upper_bound=d)
    return np.isfinite(dd)


def box(m, pad):
    v = m["v"].reshape(-1, 3)
    return v.min(0) - pad, v.max(0) + pad


def inbox(c, b):
    return np.all((c >= b[0]) & (c <= b[1]), axis=1)


ap = argparse.ArgumentParser()
ap.add_argument("base")
ap.add_argument("out")
ap.add_argument("--cut", type=float, default=9.0)
ap.add_argument("--fill", type=float, default=7.0)
a = ap.parse_args()

base = load(a.base)
bc = base["v"].mean(1)
keep = np.ones(len(base), bool)
panels = {k: load(N + f) for k, f in [("uskirt", "uskirt_3mm.stl"), ("lskirt", "lskirt_3mm.stl"), ("dtrim", "dtrim_3mm.stl")]}
for k, m in panels.items():
    hit = near(bc, m["v"].reshape(-1, 3), a.cut)
    print(f"carve {k}: {hit.sum()} base tris")
    keep &= ~hit
base = base[keep]
ref = cKDTree(base["v"].mean(1))
adds = []
fills = [("uskirt_under_3mm.stl", [panels["uskirt"], panels["lskirt"]], None),
         ("udtrim_3mm.stl", [panels["dtrim"]], None),
         ("urb_3mm.stl", None, (np.array([-2400, -1100, -200.0]), np.array([-1270, 1100, 1000.0])))]
for f, zone_parts, zb in fills:
    m = load(N + f)
    c = m["v"].mean(1)
    if zone_parts is not None:
        z = np.zeros(len(m), bool)
        for p in zone_parts:
            z |= inbox(c, box(p, 30))
    else:
        z = inbox(c, zb)
    dd, _ = ref.query(c, distance_upper_bound=a.fill)
    sel = z & ~np.isfinite(dd)
    print(f"fill {f}: {sel.sum()} of {len(m)} tris")
    adds.append(m[sel])
allm = np.concatenate([base] + adds)
with open(a.out, "wb") as fh:
    fh.write(b"ive composite_v2".ljust(80))
    fh.write(struct.pack("<I", len(allm)))
    allm.tofile(fh)
print(a.out, len(allm))
