"""Multi-start ICP of a scan in an unknown frame onto a cropped region of the levelled car (binary STLs, mm).
    python multireg.py car.stl part.stl --box xmin xmax ymin ymax zmin zmax --save T.json [--init T0.json]
Starts: 24 axis-aligned rotations x yaw jitter, centroid-aligned; coarse point-to-point ICP (60 mm), then
point-to-plane refinement (25 -> 8 mm). Picks the start with the most inliers at 8 mm. T maps part mm -> car mm."""
import argparse, itertools, json
import numpy as np
import open3d as o3d

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
R = o3d.pipelines.registration


def cloud(path, voxel, box=None):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    if box is not None:
        m = np.all((c >= box[0::2]) & (c <= box[1::2]), axis=1)
        c = c[m]
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c)).voxel_down_sample(voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 3, max_nn=30))
    return p


ap = argparse.ArgumentParser()
ap.add_argument("car"); ap.add_argument("part")
ap.add_argument("--box", type=float, nargs=6); ap.add_argument("--save"); ap.add_argument("--init")
ap.add_argument("--voxel", type=float, default=12.0)
a = ap.parse_args()
tgt = cloud(a.car, a.voxel, np.array(a.box) if a.box else None)
src = cloud(a.part, a.voxel)
print("target pts", len(tgt.points), "source pts", len(src.points))
ct, cs = np.asarray(tgt.points).mean(0), np.asarray(src.points).mean(0)
starts = []
if a.init:
    starts = [np.array(json.load(open(a.init))["T"])]
else:
    rots = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3))
            for i, (p, s) in enumerate(zip(perm, signs)):
                M[i, p] = s
            if np.linalg.det(M) > 0:
                rots.append(M)
    for M in rots:
        T = np.eye(4); T[:3, :3] = M; T[:3, 3] = ct - M @ cs
        starts.append(T)
best = None
for k, T0 in enumerate(starts):
    T = T0
    for d, est in ((150, R.TransformationEstimationPointToPoint()), (60, R.TransformationEstimationPointToPoint()),
                   (25, R.TransformationEstimationPointToPlane())):
        r = R.registration_icp(src, tgt, d, T, est, R.ICPConvergenceCriteria(max_iteration=60))
        T = r.transformation
    e = R.evaluate_registration(src, tgt, 8.0, T)
    print(k, "fit8 %.3f rmse %.2f" % (e.fitness, e.inlier_rmse))
    if best is None or e.fitness > best[0]:
        best = (e.fitness, e.inlier_rmse, T)
r = R.registration_icp(src, tgt, 8.0, best[2], R.TransformationEstimationPointToPlane(), R.ICPConvergenceCriteria(max_iteration=80))
e = R.evaluate_registration(src, tgt, 5.0, r.transformation)
print("BEST fit8 %.3f -> refined fit5 %.3f rmse %.2f" % (best[0], e.fitness, e.inlier_rmse))
print(np.round(r.transformation, 4))
if a.save:
    json.dump({"T": r.transformation.tolist(), "fit5": e.fitness, "rmse": e.inlier_rmse}, open(a.save, "w"), indent=1)
