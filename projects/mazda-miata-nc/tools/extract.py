"""Cut a moving panel out of the full car: car triangles inside a box (levelled mm) that are > --far mm from
every 'panel removed/moved' state scan given with --absent (the panel is missing or elsewhere there)
and < --near mm from every --present scan (same panel captured closed in another session).
    extract.py car.stl out.stl --absent a.stl [b.stl] --box x0 x1 y0 y1 z0 z1 [--far 8] [--grow 2]
Then keeps the largest connected blob on a 20 mm voxel grid (drops stray matches) and prints its bbox."""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("out")
ap.add_argument("--absent", nargs="+", required=True)
ap.add_argument("--present", nargs="*", default=[], help="state scans where the panel IS in this position (keep only tris within --near of them)")
ap.add_argument("--near", type=float, default=6.0)
ap.add_argument("--box", nargs=6, type=float, required=True)
ap.add_argument("--far", type=float, default=8.0)
ap.add_argument("--vox", type=float, default=20.0)
a = ap.parse_args()
car = np.fromfile(a.car, dtype=TRI, offset=84)
c = car["v"].mean(1)
b = a.box
sel = (c[:, 0] > b[0]) & (c[:, 0] < b[1]) & (c[:, 1] > b[2]) & (c[:, 1] < b[3]) & (c[:, 2] > b[4]) & (c[:, 2] < b[5])
idx = np.where(sel)[0]
for f in a.absent:
    v = np.fromfile(f, dtype=TRI, offset=84)["v"].mean(1)
    d, _ = cKDTree(v).query(c[idx], distance_upper_bound=a.far)
    idx = idx[~(d < a.far)]
for f in a.present:
    v = np.fromfile(f, dtype=TRI, offset=84)["v"].mean(1)
    d, _ = cKDTree(v).query(c[idx], distance_upper_bound=a.near)
    idx = idx[d < a.near]
p = c[idx]
lo = p.min(0); g = np.floor((p - lo) / a.vox).astype(int)
grid = np.zeros(g.max(0) + 1, bool); grid[tuple(g.T)] = True
lab, n = ndimage.label(grid, structure=np.ones((3, 3, 3)))
sizes = np.bincount(lab[tuple(g.T)])
keep = lab[tuple(g.T)] == np.argmax(sizes[1:]) + 1 if n else np.ones(len(idx), bool)
idx = idx[keep]
m = car[idx]
with open(a.out, "wb") as f:
    f.write(b"miata panel".ljust(80)); f.write(struct.pack("<I", len(m))); m.tofile(f)
q = c[idx]
print(a.out, len(m), "bbox", q.min(0).round(), q.max(0).round())
