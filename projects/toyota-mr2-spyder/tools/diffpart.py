"""Extract a part as 'tris of scan A farther than TOL mm from scan B' (both in the car frame), inside an optional box,
keeping only big connected-ish chunks (voxel flood fill at 15 mm). E.g. hardtop = Full Car (hardtop on) - Full Car Top Down.
  diffpart.py A.stl B.stl out.stl [--tol 12] [--box x0,x1,y0,y1,z0,z1] [--minvox 400]"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("A"); ap.add_argument("B"); ap.add_argument("out")
ap.add_argument("--tol", type=float, default=12); ap.add_argument("--box"); ap.add_argument("--minvox", type=int, default=400)
a = ap.parse_args()
A = np.fromfile(a.A, dtype=TRI, offset=84); ca = A["v"].mean(1)
B = np.fromfile(a.B, dtype=TRI, offset=84)["v"].mean(1)
m = np.ones(len(A), bool)
if a.box:
    b = list(map(float, a.box.split(",")))
    for k in range(3):
        m &= (ca[:, k] > b[2 * k]) & (ca[:, k] < b[2 * k + 1])
d, _ = cKDTree(B).query(ca[m], distance_upper_bound=a.tol + 1)
sel = np.where(m)[0][d > a.tol]
# drop small islands: voxelise at 15 mm, label 26-connected components
P = ca[sel]; lo = P.min(0); k = np.floor((P - lo) / 15).astype(int)
g = np.zeros(k.max(0) + 1, bool); g[tuple(k.T)] = True
lab, n = ndimage.label(g, structure=np.ones((3, 3, 3)))
sizes = ndimage.sum(g, lab, range(1, n + 1))
keep = np.isin(lab[tuple(k.T)], 1 + np.where(sizes >= a.minvox)[0])
res = A[sel[keep]]
with open(a.out, "wb") as f:
    f.write(b"ive mr2 diffpart".ljust(80)); f.write(struct.pack("<I", len(res))); res.tofile(f)
print(a.out, len(res), "tris; components kept", int((sizes >= a.minvox).sum()), "of", n)
