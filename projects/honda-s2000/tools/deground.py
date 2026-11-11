"""Remove the scanned floor from a state scan in its own frame: largest plane (RANSAC) + everything on the far side
of it (below the floor) + a --band mm above it. Writes a binary STL.
    python projects/honda-s2000/tools/deground.py in.stl out.stl [--band 15]"""
import argparse, struct
import numpy as np
import open3d as o3d
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--band", type=float, default=15)
a = ap.parse_args()
m = np.fromfile(a.src, dtype=TRI, offset=84); c = m["v"].mean(1).astype(np.float64)
p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c[::4]))
(A, B, C, Dd), inl = p.segment_plane(8.0, 3, 2000)
n = np.array([A, B, C]); d = c @ n + Dd
# the car is on the side where most points are
if np.median(d) < 0: d = -d; n = -n
keep = d > a.band
print(f"plane n={np.round(n,3)} inliers={len(inl)} ({len(inl)/len(p.points)*100:.0f}% of sample); dropped {(~keep).sum()} of {len(m)}")
with open(a.out, "wb") as f:
    f.write(b"ive deground".ljust(80)); f.write(struct.pack("<I", int(keep.sum()))); m[keep].tofile(f)
json_n = n
np.save(a.out + ".floor_n.npy", np.r_[n, Dd])
