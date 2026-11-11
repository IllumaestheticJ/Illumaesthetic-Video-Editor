"""Doors-open composite from the partial 'Door Open' capture (both butterfly doors up, cabin only).
Inside the door zone (car-local u along forward, v across, raw Artec mm) full-car triangles with no captured geometry
within --tol mm (the closed doors / door glass) are dropped and the capture's triangles are added; outside the zone the
full car is kept unchanged (the capture is partial and ragged there).
    python tools/doors_comp.py full.stl door.stl out.stl"""
import argparse, numpy as np
from scipy.spatial import cKDTree
T = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("full"); ap.add_argument("door"); ap.add_argument("out")
ap.add_argument("--tol", type=float, default=15.0)
ap.add_argument("--u", default="-520,760", help="door zone along forward (mm)")
ap.add_argument("--zmin", type=float, default=-700.0, help="raw z of the sill line")
ap.add_argument("--vside", type=float, default=430.0, help="|v| beyond which a triangle is on a side")
ap.add_argument("--zroof", type=float, default=120.0, help="raw z above which roof glass belongs to the doors")
a = ap.parse_args()
F = np.fromfile(a.full, dtype=T, offset=84); D = np.fromfile(a.door, dtype=T, offset=84)
U = lambda c: c[:, 0] * 0.258 + c[:, 1] * 0.966; V = lambda c: c[:, 0] * 0.966 - c[:, 1] * 0.258
u0, u1 = (float(x) for x in a.u.split(","))
def zone(c, m=0.0):
    u, v, z = U(c), V(c), c[:, 2]
    return (u > u0 - m) & (u < u1 + m) & (z > a.zmin - m) & ((np.abs(v) > a.vside - m) | (z > a.zroof - m))
cf = F["v"].mean(1); cd = D["v"].mean(1)
zf = zone(cf)
d, _ = cKDTree(cd[::2]).query(cf[zf], distance_upper_bound=a.tol)
drop = np.zeros(len(F), bool); drop[np.nonzero(zf)[0][~np.isfinite(d)]] = True
add = D[zone(cd, 150.0) | (cd[:, 2] > np.percentile(cf[:, 2], 99.5) + 50)]
out = np.concatenate([F[~drop], add])
with open(a.out, "wb") as f:
    f.write(b"tools/doors_comp.py".ljust(80)); f.write(np.uint32(len(out)).tobytes()); out.tofile(f)
print({"full": int(len(F)), "dropped": int(drop.sum()), "door_added": int(len(add)), "out": int(len(out))})
