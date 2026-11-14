"""Seat the two fog-lamp bench scans behind the rectangular lamp frames of the SEMA fog/duct inserts.
Lens normal = smallest principal axis of the dense lamp body (wires removed by density), signed away from the wires;
lamp long axis -> car X, lens -> -Y (forward). Lens centre on the frame-hole centre, `--back` mm behind the frame face.
fogplace.py fog.stl insert.stl out.stl --side driver|passenger [--back 12]"""
import argparse, numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("fog"); ap.add_argument("insert"); ap.add_argument("out")
ap.add_argument("--side", default="driver"); ap.add_argument("--back", type=float, default=12)
a = ap.parse_args()
d = np.fromfile(a.fog, dtype=TRI, offset=84); v = d["v"].reshape(-1, 3).astype(float); c = d["v"].mean(1).astype(float)
T = cKDTree(c[::5]); cnt = np.array([len(x) for x in T.query_ball_point(c[::5], 6)])
dense = cnt > np.percentile(cnt, 40); body = c[::5][dense]; wires = c[::5][~dense]
mu = body.mean(0); _, _, Vt = np.linalg.svd(body - mu, full_matrices=False)
n = Vt[2]
if (wires.mean(0) - mu) @ n > 0: n = -n          # lens faces away from the wires
u = Vt[0] - (Vt[0] @ n) * n; u /= np.linalg.norm(u); w = np.cross(n, u)
R = np.stack([u, -n, w])                          # rows: lamp axes expressed in target x, y, z  (lens -> -Y)
if R[2] @ np.array([0, 0, 1.0]) < 0 and False: pass
if np.linalg.det(R) < 0: R[2] = -R[2]
p = (v - mu) @ R.T
lens_front = np.percentile(p[:, 1], 0.5)           # most forward (min y) of the lamp
# frame hole on the insert (x-z occupancy), then the frame face y around the hole rim
ic = np.fromfile(a.insert, dtype=TRI, offset=84)["v"].mean(1)
x0, z0 = ic[:, 0].min(), ic[:, 2].min()
occ = np.zeros((400, 400), bool); occ[np.clip(((ic[:, 2] - z0)).astype(int), 0, 399), np.clip(((ic[:, 0] - x0)).astype(int), 0, 399)] = True
occ = ndimage.binary_closing(occ, iterations=2); holes = ndimage.binary_fill_holes(occ) & ~occ
lab, k = ndimage.label(holes); best = None
for i in range(1, k + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 500: continue
    wdt, hgt = np.ptp(xs), np.ptp(ys)
    if best is None or wdt / max(hgt, 1) > best[0]: best = (wdt / max(hgt, 1), xs, ys)
_, xs, ys = best
hx, hz = x0 + (xs.min() + xs.max()) / 2, z0 + (ys.min() + ys.max()) / 2
rim = ic[(np.abs(ic[:, 0] - hx) < np.ptp(xs) / 2 + 8) & (np.abs(ic[:, 2] - hz) < np.ptp(ys) / 2 + 8)]
face_y = np.percentile(rim[:, 1], 5)
print("hole centre x %.0f z %.0f size %d x %d  face y %.0f" % (hx, hz, np.ptp(xs), np.ptp(ys), face_y))
off = np.array([hx, face_y + a.back - lens_front, hz])
out = ((d["v"].reshape(-1, 3) - mu) @ R.T + off).reshape(-1, 3, 3).astype(np.float32)
d2 = d.copy(); d2["v"] = out
with open(a.out, "wb") as f: f.write(b"\0" * 80); f.write(np.uint32(len(d2)).tobytes()); d2.tofile(f)
print("lamp extents in place", (out.reshape(-1, 3).max(0) - out.reshape(-1, 3).min(0)).round(0))
