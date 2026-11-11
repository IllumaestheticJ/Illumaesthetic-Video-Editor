"""Cut a panel out of the full car: car triangles inside a box that are > --far mm from EVERY 'without' state scan
(the panel's skin is exactly what those scans lack). Writes the panel and the car minus panel (raw frame-A STLs, mm).
    python carve_part.py car.stl panel.stl rest.stl --box x0,x1,y0,y1,z0,z1 --without a.stl b.stl [--far 10]
          [--exclude-cyl x,y,z,r,halfwidth ...]   # skip wheels: cylinders along X (centre, radius, half-length) in mm
          [--grow 2]   # rounds of including neighbours (shared verts) that are inside the box & > far/2 (closes speckle)
"""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def save(p, m):
    with open(p, "wb") as f: f.write(b"sti carve".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("panel"); ap.add_argument("rest")
ap.add_argument("--box", required=True); ap.add_argument("--without", nargs="+", required=True)
ap.add_argument("--far", type=float, default=10); ap.add_argument("--exclude-cyl", nargs="*", default=[])
ap.add_argument("--min-island", type=int, default=200)
a = ap.parse_args()
m = np.fromfile(a.car, dtype=TRI, offset=84); c = m["v"].mean(1).astype(float)
b = np.array([float(v) for v in a.box.split(",")])
inb = np.all((c >= b[0::2]) & (c <= b[1::2]), axis=1)
for s in a.exclude_cyl:
    x, y, z, r, hw = (float(v) for v in s.split(","))
    inb &= ~((np.hypot(c[:, 1] - y, c[:, 2] - z) < r) & (np.abs(c[:, 0] - x) < hw))
far = inb.copy()
for w in a.without:
    wv = np.fromfile(w, dtype=TRI, offset=84)["v"].mean(1)
    d, _ = cKDTree(wv).query(c[inb], distance_upper_bound=a.far)
    far[np.where(inb)[0][np.isfinite(d)]] = False
# drop tiny islands of the panel selection (connectivity through shared vertex positions)
idx = np.where(far)[0]
v = np.round(m["v"][idx].reshape(-1, 3), 3)
_, vid = np.unique(v, axis=0, return_inverse=True); vid = vid.reshape(-1, 3)
import scipy.sparse as sp, scipy.sparse.csgraph as cg
n = len(idx); nv = vid.max() + 1
rows = np.repeat(np.arange(n), 3); A = sp.csr_matrix((np.ones(3 * n), (rows, vid.ravel())), shape=(n, nv))
k, lab = cg.connected_components(A @ A.T, directed=False)
sizes = np.bincount(lab); keep = sizes[lab] >= a.min_island
far[idx[~keep]] = False
print(f"box {inb.sum()} tris -> panel {far.sum()} ({k} islands, kept {np.sum(sizes>=a.min_island)})")
save(a.panel, m[far]); save(a.rest, m[~far])
