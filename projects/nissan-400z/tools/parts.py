"""Cut a removable part out of a scan by diffing against the matching 'removed' state scan (same Artec frame).
Part = triangles of SRC farther than --far mm from STATE, inside --zone, connected (voxel --link mm) to the one
nearest --seed. Writes an STL of SRC's own triangles (levelled raw mm), so the part is the real scanned skin.
  parts.py SRC.stl STATE.stl out.stl --seed x,y,z --zone x0,x1,y0,y1,z0,z1 [--far 10] [--link 9] [--grow 4]
--grow re-adds SRC triangles within N mm of the component (fills seams the threshold nibbled)."""
import argparse, struct
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("state"); ap.add_argument("out")
ap.add_argument("--seed", required=True); ap.add_argument("--zone", required=True)
ap.add_argument("--far", type=float, default=10); ap.add_argument("--link", type=float, default=9)
ap.add_argument("--grow", type=float, default=4)
a = ap.parse_args()
m = np.fromfile(a.src, dtype=TRI, offset=84); c = m["v"].mean(1).astype(np.float64)
s = np.fromfile(a.state, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
z = [float(v) for v in a.zone.split(",")]
inz = (c[:, 0] > z[0]) & (c[:, 0] < z[1]) & (c[:, 1] > z[2]) & (c[:, 1] < z[3]) & (c[:, 2] > z[4]) & (c[:, 2] < z[5])
d, _ = cKDTree(s).query(c[inz], distance_upper_bound=a.far * 3)
idx = np.where(inz)[0][d > a.far]
p = c[idx]
g = np.floor((p - p.min(0)) / a.link).astype(int)
vol = np.zeros(g.max(0) + 1, bool); vol[tuple(g.T)] = True
lab, n = ndimage.label(vol, structure=np.ones((3, 3, 3)))
pl = lab[tuple(g.T)]
seed = np.array([float(v) for v in a.seed.split(",")])
k = pl[np.argmin(np.linalg.norm(p - seed, axis=1))]
sel = idx[pl == k]
if a.grow > 0:
    dd, _ = cKDTree(c[sel]).query(c[inz], distance_upper_bound=a.grow)
    sel = np.union1d(sel, np.where(inz)[0][np.isfinite(dd) & (dd < a.grow)])
part = m[sel]
with open(a.out, "wb") as f:
    f.write(b"400z part".ljust(80)); f.write(struct.pack("<I", len(part))); part.tofile(f)
v = c[sel]
print(a.out, len(part), "tris  bbox", v.min(0).round(), v.max(0).round(), " components in zone:", n)
