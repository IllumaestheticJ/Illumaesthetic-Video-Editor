"""Explode base v2 (raw STL, mm, Artec frame). Like projects/a90-supra/tools/carve.py, plus a zone replace:
inside --zone (xmin,zmax in mm), base triangles survive only if they lie within --keep-dist of a --zone-scan
surface, so the 'Under Front Bumper' state scan replaces the full-car scan's loose bumper-lip strips there.
    python carve2.py car_4mm.stl out.stl --remove fb_out.stl ... --zone 1350,750 --zone-scan under_fb.stl \
        --add under_fb.stl under_fender.stl liners.stl [--dist 12 --keep-dist 8]
"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("base"); ap.add_argument("out")
ap.add_argument("--remove", nargs="*", default=[]); ap.add_argument("--add", nargs="*", default=[])
ap.add_argument("--zone", default=""); ap.add_argument("--zone-scan", default="")
ap.add_argument("--dist", type=float, default=12.0); ap.add_argument("--keep-dist", type=float, default=8.0)
a = ap.parse_args()
m = np.fromfile(a.base, dtype=TRI, offset=84)
c = m["v"].mean(1)
keep = np.ones(len(m), bool)
for p in a.remove:
    pv = np.fromfile(p, dtype=TRI, offset=84)["v"].reshape(-1, 3)
    d, _ = cKDTree(pv).query(c, distance_upper_bound=a.dist)
    hit = np.isfinite(d); keep &= ~hit
    print(f"remove {p.split('/')[-1]}: {hit.sum()} base tris")
if a.zone:
    xmin, zmax = (float(v) for v in a.zone.split(","))
    inz = (c[:, 0] > xmin) & (c[:, 2] < zmax)
    zv = np.fromfile(a.zone_scan, dtype=TRI, offset=84)["v"].reshape(-1, 3)
    d, _ = cKDTree(zv).query(c[inz & keep], distance_upper_bound=a.keep_dist)
    idx = np.nonzero(inz & keep)[0][~np.isfinite(d)]
    keep[idx] = False
    print(f"zone x>{xmin} z<{zmax}: dropped {len(idx)} base tris not on {a.zone_scan.split('/')[-1]}")
allm = np.concatenate([m[keep]] + [np.fromfile(p, dtype=TRI, offset=84) for p in a.add])
with open(a.out, "wb") as f:
    f.write(b"ive carve2".ljust(80)); f.write(struct.pack("<I", len(allm))); allm.tofile(f)
print(a.out, len(allm))
