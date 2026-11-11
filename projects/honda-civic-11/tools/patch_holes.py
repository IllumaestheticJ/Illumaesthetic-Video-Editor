"""Fill holes on the upper body of one scan with triangles from another scan of the SAME car in the SAME frame.

    python patch_holes.py base.stl donor.stl out.stl --zmin -700 --gap 8

Only donor triangles whose centroid is > --gap mm from every base vertex, above --zmin (raw mm), facing up
(n.z > --nz), are added. Prints the donor-vs-base distance on overlapping upper surfaces (registration check).
"""
import argparse
import sys
import os
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(__file__))
from stlio import read, write  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("base"); ap.add_argument("donor"); ap.add_argument("out")
ap.add_argument("--zmin", type=float, default=-700); ap.add_argument("--gap", type=float, default=8)
ap.add_argument("--nz", type=float, default=0.35)
ap.add_argument("--box", type=float, nargs=4, help="xmin xmax ymin ymax (raw mm) to limit patching")
a = ap.parse_args()
b = read(a.base); d = read(a.donor)
bv = b["v"].reshape(-1, 3)
t = cKDTree(bv[bv[:, 2] > a.zmin - 50])
c = d["v"].mean(1)
# local rigid ICP (point-to-point, trimmed) of the donor's upper body onto the base before measuring gaps
up = (c[:, 2] > a.zmin) & (d["n"][:, 2] > a.nz)
src = c[up][:: max(1, up.sum() // 150000)]
R, T = np.eye(3), np.zeros(3)
for it in range(25):
    q = src @ R.T + T
    dd, ii = t.query(q, distance_upper_bound=30)
    ok = dd < max(4, np.percentile(dd[np.isfinite(dd)], 70))
    P, Q = q[ok], t.data[ii[ok]]
    mp, mq = P.mean(0), Q.mean(0)
    U, S, Vt = np.linalg.svd((P - mp).T @ (Q - mq))
    Ri = (U @ Vt).T
    if np.linalg.det(Ri) < 0:
        Vt[-1] *= -1; Ri = (U @ Vt).T
    R, T = Ri @ R, Ri @ T + (mq - Ri @ mp)
print("ICP R deg %.3f  T %s mm" % (np.degrees(np.arccos(min(1, (np.trace(R) - 1) / 2))), np.round(T, 1)))
v = d["v"].reshape(-1, 3) @ R.T + T
d["v"] = v.reshape(-1, 3, 3).astype(np.float32)
d["n"] = (d["n"] @ R.T).astype(np.float32)
c = d["v"].mean(1)
sel = (c[:, 2] > a.zmin) & (d["n"][:, 2] > a.nz)
if a.box:
    sel &= (c[:, 0] > a.box[0]) & (c[:, 0] < a.box[1]) & (c[:, 1] > a.box[2]) & (c[:, 1] < a.box[3])
dist, _ = t.query(c[sel], distance_upper_bound=200)
print("donor->base on upper surfaces: p25 %.1f p50 %.1f p75 %.1f mm" % tuple(np.percentile(dist[dist < 50], [25, 50, 75])))
add = d[sel][dist > a.gap]
# keep only patches that are mostly enclosed by base surface (holes), not donor-only geometry outside the car
# hole test: base surface exists on at least 3 of 4 sides within 120 mm (in XY, upper body) -> enclosed gap
tb = cKDTree(bv[bv[:, 2] > a.zmin - 50][::4])
ca = add["v"].mean(1)
sides = 0
for dx, dy in ((120, 0), (-120, 0), (0, 120), (0, -120)):
    q = ca.copy(); q[:, 0] += dx; q[:, 1] += dy
    dq, _ = tb.query(q, distance_upper_bound=60)
    sides = sides + (dq < 60)
add = add[sides >= 3]
print("added", len(add), "triangles")
write(a.out, np.concatenate([b, add]))
