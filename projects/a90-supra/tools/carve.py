"""Carve part zones out of the base car and splice state scans in (all raw STL, mm, same frame).
    python projects/a90-supra/tools/carve.py car_4mm.stl out.stl --remove fb_out.stl fb_in.stl ... --add ufb.stl ... [--dist 12]
Removes base triangles whose centroid lies within --dist mm of any --remove part's surface, then appends --add meshes.
"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("base"); ap.add_argument("out")
ap.add_argument("--remove", nargs="*", default=[]); ap.add_argument("--add", nargs="*", default=[])
ap.add_argument("--dist", type=float, default=12.0)
a = ap.parse_args()
m = np.fromfile(a.base, dtype=TRI, offset=84)
c = m["v"].mean(1)
keep = np.ones(len(m), bool)
for p in a.remove:
    pv = np.fromfile(p, dtype=TRI, offset=84)["v"].reshape(-1, 3)
    d, _ = cKDTree(pv).query(c, distance_upper_bound=a.dist)
    hit = np.isfinite(d)
    print(f"remove {p.split('/')[-1]}: {hit.sum()} base tris")
    keep &= ~hit
out = [m[keep]] + [np.fromfile(p, dtype=TRI, offset=84) for p in a.add]
allm = np.concatenate(out)
with open(a.out, "wb") as f:
    f.write(b"ive carve".ljust(80)); f.write(struct.pack("<I", len(allm))); allm.tofile(f)
print(a.out, len(allm))
