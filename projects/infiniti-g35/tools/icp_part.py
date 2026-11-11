"""Point-to-plane ICP of a part scan onto the full car (both levelled mm STLs), restricted to the part's overlap.
Reports signed-distance stats before/after; with --save writes the corrected part STL + the 4x4 (mm).
    icp_part.py car.stl part.stl [--save out.stl T.json]"""
import sys, json, struct, numpy as np, open3d as o3d
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
car = np.fromfile(sys.argv[1], dtype=TRI, offset=84); part = np.fromfile(sys.argv[2], dtype=TRI, offset=84)
pc = part["v"].mean(1).astype(np.float64); lo, hi = pc.min(0) - 60, pc.max(0) + 60
cc = car["v"].mean(1).astype(np.float64); cn = car["n"].astype(np.float64)
sel = np.all((cc > lo) & (cc < hi), 1)
T = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(cc[sel])); T.normals = o3d.utility.Vector3dVector(cn[sel])
T.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=12, max_nn=30)); T.orient_normals_to_align_with_direction([0, 0, 1])
S = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pc[:: max(1, len(pc) // 300000)]))
S.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=12, max_nn=30))
reg = o3d.pipelines.registration
def stats(M, tag):
    e = reg.evaluate_registration(S, T, 8.0, M); print(f"{tag}: fitness(8mm)={e.fitness:.3f} rmse={e.inlier_rmse:.2f}mm")
stats(np.eye(4), "as captured")
M = np.eye(4)
for thr in (20, 10, 6, 4):
    M = reg.registration_icp(S, T, thr, M, reg.TransformationEstimationPointToPlane()).transformation
stats(M, "after ICP")
ang = np.degrees(np.arccos(np.clip((np.trace(M[:3, :3]) - 1) / 2, -1, 1)))
print("correction: t=", M[:3, 3].round(2), "|t|=", np.linalg.norm(M[:3, 3]).round(2), "mm, rot", ang.round(3), "deg")
if "--save" in sys.argv:
    out, tj = sys.argv[sys.argv.index("--save") + 1: sys.argv.index("--save") + 3]
    v = part["v"].reshape(-1, 3).astype(np.float64) @ M[:3, :3].T + M[:3, 3]
    part["v"] = v.reshape(-1, 3, 3).astype(np.float32); part["n"] = (part["n"] @ M[:3, :3].T).astype(np.float32)
    with open(out, "wb") as f:
        f.write(b"infiniti-g35 icp_part".ljust(80)); f.write(struct.pack("<I", len(part))); part.tofile(f)
    json.dump({"M_mm": M.tolist()}, open(tj, "w"), indent=1); print("saved", out, tj)
