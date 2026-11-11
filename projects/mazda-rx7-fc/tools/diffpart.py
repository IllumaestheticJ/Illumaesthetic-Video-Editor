"""Cut a panel out of a scan as the geometry that a state scan lacks (same Artec frame, levelled mm).

    python projects/mazda-rx7-fc/tools/diffpart.py src.stl --minus state.stl [--minus ...] --zone x0,x1,y0,y1,z0,z1 \
        --dist 12 --out part.stl [--keep-rest rest.stl] [--min-island 0]

Keeps src triangles inside --zone whose centroid is > --dist mm from every --minus scan (i.e. present in src,
absent in the state scan = the removed panel). The state scans must cover the zone, or coverage holes leak in.
"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def load(p): return np.fromfile(p, dtype=TRI, offset=84)
def save(p, m):
    with open(p, "wb") as f:
        f.write(b"rx7 diffpart".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("--minus", nargs="+", required=True)
ap.add_argument("--zone", required=True); ap.add_argument("--dist", type=float, default=12)
ap.add_argument("--out", required=True); ap.add_argument("--keep-rest")
a = ap.parse_args()
m = load(a.src); c = m["v"].mean(1)
z = [float(v) for v in a.zone.split(",")]
inz = (c[:, 0] > z[0]) & (c[:, 0] < z[1]) & (c[:, 1] > z[2]) & (c[:, 1] < z[3]) & (c[:, 2] > z[4]) & (c[:, 2] < z[5])
far = inz.copy()
for s in a.minus:
    sc = load(s)["v"].mean(1)
    d, _ = cKDTree(sc).query(c[inz], distance_upper_bound=a.dist)
    far[np.where(inz)[0][d < a.dist]] = False
save(a.out, m[far]); print(a.out, int(far.sum()), "of", int(inz.sum()), "in zone")
if a.keep_rest: save(a.keep_rest, m[~far]); print(a.keep_rest, int((~far).sum()))
