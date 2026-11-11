"""Refine a rigid registration (part -> target, raw STL mm) with dense point-to-plane ICP and report residuals.
    python refine.py target.stl part.stl T_in.json T_out.json [--voxel 5] [--max 8]
T json: {"T_part_to_car_mm": 4x4} (globalreg.py format) or {"T": 4x4}; identity if T_in is 'I'.
Prints the median / p75 / share<3 mm of part->target nearest distances on the overlap (<15 mm) before and after."""
import argparse, json
import numpy as np, open3d as o3d
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def pts(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
def loadT(p):
    if p == "I": return np.eye(4)
    j = json.load(open(p)); return np.array(j.get("T_part_to_car_mm", j.get("T")))
ap = argparse.ArgumentParser(); ap.add_argument("target"); ap.add_argument("part"); ap.add_argument("Tin"); ap.add_argument("Tout")
ap.add_argument("--box", help="fit only part points inside x0,x1,y0,y1,z0,z1 (target frame, mm, after T_in)")
ap.add_argument("--voxel", type=float, default=5); ap.add_argument("--max", type=float, default=8)
a = ap.parse_args()
tc, pc = pts(a.target), pts(a.part)
T0 = loadT(a.Tin)
fit = pc
if a.box:
    b = [float(v) for v in a.box.split(",")]; q = pc @ T0[:3, :3].T + T0[:3, 3]
    m = np.all((q >= b[0::2]) & (q <= b[1::2]), axis=1); fit = pc[m]; print("box keeps", m.sum(), "of", len(pc))
def pcd(c):
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c)).voxel_down_sample(a.voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=a.voxel * 3, max_nn=30)); return p
T, S = pcd(tc), pcd(fit)
reg = o3d.pipelines.registration
r = reg.registration_icp(S, T, a.max * 2, T0, reg.TransformationEstimationPointToPlane())
r = reg.registration_icp(S, T, a.max, r.transformation, reg.TransformationEstimationPointToPlane(), reg.ICPConvergenceCriteria(max_iteration=60))
tree = cKDTree(tc)
def rep(M, pc=fit):
    q = pc[:: max(1, len(pc) // 300000)] @ M[:3, :3].T + M[:3, 3]
    d, _ = tree.query(q); o = d < 15
    return f"overlap {o.mean()*100:.0f}% p50={np.median(d[o]):.2f} p75={np.percentile(d[o],75):.2f} <3mm={np.mean(d[o]<3)*100:.0f}%"
print("before", rep(T0)); print("after ", rep(r.transformation), "fitness", round(r.fitness, 3))
D = np.linalg.inv(T0) @ r.transformation
print("delta: shift %.1f mm, rot %.2f deg" % (np.linalg.norm(D[:3, 3]), np.degrees(np.arccos(np.clip((np.trace(D[:3, :3]) - 1) / 2, -1, 1)))))
json.dump({"T": r.transformation.tolist(), "fitness": r.fitness, "rmse_mm": r.inlier_rmse}, open(a.Tout, "w"), indent=1)
