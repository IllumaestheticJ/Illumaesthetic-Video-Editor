"""v0: rigid ICP of Ron's 'FE1 Fl' scan copy (his design frame, m, front -Y) onto our prepped FE1 scan (car.json frame, m, front +Y).
Writes kit/ron_to_scan.json {R, t} (Ron m -> prepped m), same convention as honda-civic-11 kit_parts2.py.
    python tools_register_ron.py
"""
import json, sys, numpy as np, open3d as o3d
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/projects/honda-civic-11/tools")
from stlio import read
M = "/home/user/media/bf-civic-parts-rain"
j = json.load(open(f"{M}/prep/car.json")); root = np.array(j["root_location"])
d = read(f"{M}/dec/fe1_4mm_dg.stl"); P = d["v"].mean(1).astype(np.float64) * 0.001 + root
P = P[P[:, 2] > 0.02]
Q = np.load(f"{M}/kit/ron_fe1fl_pts.npy").astype(np.float64)
def pc(x):
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(x)); return p
src, dst = pc(Q), pc(P)
R0 = np.diag([-1., -1., 1.])  # 180 deg about Z
T = np.eye(4); T[:3, :3] = R0
T[:3, 3] = np.median(P, 0) - R0 @ np.median(Q, 0)
for vox, dist in [(0.04, 0.3), (0.015, 0.08), (0.006, 0.03), (0.004, 0.012)]:
    s = src.voxel_down_sample(vox); t = dst.voxel_down_sample(vox)
    t.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=vox * 3, max_nn=30))
    r = o3d.pipelines.registration.registration_icp(s, t, dist, T, o3d.pipelines.registration.TransformationEstimationPointToPlane(),
                                                    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=60))
    T = r.transformation; print(f"vox {vox}: fitness {r.fitness:.3f} rmse {r.inlier_rmse*1000:.1f} mm")
Qt = (np.asarray(src.points) @ T[:3, :3].T) + T[:3, 3]
dd = np.asarray(o3d.geometry.PointCloud(o3d.utility.Vector3dVector(Qt)).compute_point_cloud_distance(dst))
print("Ron->ours distance median %.1f mm, p80 %.1f mm, within 6 mm %.0f%%" % (np.median(dd) * 1000, np.percentile(dd, 80) * 1000, (dd < .006).mean() * 100))
json.dump({"R": T[:3, :3].tolist(), "t": T[:3, 3].tolist(), "median_mm": float(np.median(dd) * 1000)}, open(f"{M}/kit/ron_to_scan.json", "w"), indent=1)
print("bbox of Ron scan in our frame", Qt.min(0).round(3), Qt.max(0).round(3))
