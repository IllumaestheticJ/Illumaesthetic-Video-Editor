"""Global registration (FPFH + RANSAC, then point-to-plane ICP) of a scan in its own Artec frame onto the C5 full car
(both binary STLs, mm). Based on projects/a90-supra/tools/globalreg.py, with axis crops on the car and the part.
  globalreg.py car.stl part.stl [--car-crop "y<0"] [--part-crop "z>-1300"] [--voxel 15] [--tries 5] [--save T.json]
The saved 4x4 maps part mm -> car mm (raw frames). Verify by looking (tools/overlay views), not just fitness."""
import argparse, json
import numpy as np
import open3d as o3d
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
AX = {"x": 0, "y": 1, "z": 2}

def crop(c, expr):
    for e in (expr or "").split(","):
        e = e.strip()
        if not e: continue
        ax, op, v = AX[e[0]], e[1], float(e[2:])
        c = c[c[:, ax] < v] if op == "<" else c[c[:, ax] > v]
    return c

def pcd(path, voxel, expr):
    c = crop(np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64), expr)
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c)).voxel_down_sample(voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 3, max_nn=30))
    f = o3d.pipelines.registration.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 6, max_nn=100))
    return p, f

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("car"); ap.add_argument("part")
    ap.add_argument("--car-crop"); ap.add_argument("--part-crop")
    ap.add_argument("--voxel", type=float, default=15.0)
    ap.add_argument("--tries", type=int, default=5)
    ap.add_argument("--save")
    a = ap.parse_args()
    reg = o3d.pipelines.registration
    o3d.utility.random.seed(1)
    T, Tf = pcd(a.car, a.voxel, a.car_crop)
    S, Sf = pcd(a.part, a.voxel, a.part_crop)
    best = None
    for k in range(a.tries):
        r = reg.registration_ransac_based_on_feature_matching(
            S, T, Sf, Tf, True, a.voxel * 1.5, reg.TransformationEstimationPointToPoint(False), 3,
            [reg.CorrespondenceCheckerBasedOnEdgeLength(0.9), reg.CorrespondenceCheckerBasedOnDistance(a.voxel * 1.5)],
            reg.RANSACConvergenceCriteria(400000, 0.999))
        icp = reg.registration_icp(S, T, a.voxel * 0.6, r.transformation, reg.TransformationEstimationPointToPlane())
        icp = reg.registration_icp(S, T, 6.0, icp.transformation, reg.TransformationEstimationPointToPlane())
        print(f"try {k}: ransac fit={r.fitness:.3f}  icp fit(6mm)={icp.fitness:.3f} rmse={icp.inlier_rmse:.2f}mm  t={np.round(icp.transformation[:3,3],0)}", flush=True)
        if best is None or icp.fitness > best.fitness:
            best = icp
    print("BEST fitness", round(best.fitness, 3), "rmse", round(best.inlier_rmse, 2))
    if a.save:
        json.dump({"T_part_to_car_mm": best.transformation.tolist(), "fitness": best.fitness, "rmse_mm": best.inlier_rmse}, open(a.save, "w"), indent=1)
