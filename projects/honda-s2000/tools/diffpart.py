"""Cut a moving panel out of the full car using a state scan where that panel is OPEN/absent (levelled frame, mm):
part = car triangles inside --zone that are > --dist mm from every state-scan triangle (and not dropped by --keep-small).
Writes the part and the car-minus-part. Small islands of the part (< --min-island tris, by 2D grid connectivity) are
returned to the car.
    python projects/honda-s2000/tools/diffpart.py car_lvl.stl state_lvl.stl part.stl rest.stl --zone x0,x1,y0,y1,z0,z1 [--dist 10]"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("state"); ap.add_argument("part"); ap.add_argument("rest")
ap.add_argument("--zone", required=True); ap.add_argument("--dist", type=float, default=10)
ap.add_argument("--min-island", type=int, default=2000); ap.add_argument("--nz", type=float, default=-2, help="min normal z (top-facing skins)")
a = ap.parse_args()
z = [float(v) for v in a.zone.split(",")]
m = np.fromfile(a.car, dtype=TRI, offset=84); c = m["v"].mean(1).astype(float)
s = np.fromfile(a.state, dtype=TRI, offset=84)["v"].mean(1).astype(float)
inz = (c[:, 0] > z[0]) & (c[:, 0] < z[1]) & (c[:, 1] > z[2]) & (c[:, 1] < z[3]) & (c[:, 2] > z[4]) & (c[:, 2] < z[5])
nrm = m["n"].astype(float); nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-12
inz &= nrm[:, 2] >= a.nz
d, _ = cKDTree(s).query(c[inz], distance_upper_bound=a.dist)
sel = np.zeros(len(m), bool); sel[np.where(inz)[0][~np.isfinite(d)]] = True
# keep the largest connected blob in top view (20 mm grid)
g = 20.0; ij = np.floor(c[sel][:, :2] / g).astype(int); ij -= ij.min(0)
grid = np.zeros(ij.max(0) + 1, bool); grid[ij[:, 0], ij[:, 1]] = True
grid = ndimage.binary_closing(grid, iterations=2)
lab, n = ndimage.label(grid); sizes = ndimage.sum(grid, lab, range(1, n + 1))
big = 1 + np.argmax(sizes); keep = lab[ij[:, 0], ij[:, 1]] == big
idx = np.where(sel)[0]; sel[idx[~keep]] = False
print(f"zone tris {inz.sum()}, part {sel.sum()}  bbox {np.round(c[sel].min(0))} .. {np.round(c[sel].max(0))}")
for p, mm in ((a.part, m[sel]), (a.rest, m[~sel])):
    with open(p, "wb") as f:
        f.write(b"ive diffpart".ljust(80)); f.write(struct.pack("<I", len(mm))); mm.tofile(f)
