"""Global registration (FPFH + RANSAC, then point-to-plane ICP) of a scan in an unknown frame onto
the base car (both binary STLs in mm). Used for the 2021 rear-state scans.
    python projects/a90-supra/tools/globalreg.py car_4mm.stl part_3mm.stl --crop-x-max -900 [--save T.json]
Prints fitness / inlier RMSE; the saved 4x4 maps part mm -> car mm (raw STL frames).
"""
import argparse, json
import numpy as np
import open3d as o3d

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def pcd(path, voxel, xmax=None, xmin=None):
    c = np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    if xmax is not None:
        c = c[c[:, 0] < xmax]
    if xmin is not None:
        c = c[c[:, 0] > xmin]
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c)).voxel_down_sample(voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 3, max_nn=30))
    f = o3d.pipelines.registration.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 6, max_nn=100))
    return p, f


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("car"); ap.add_argument("part")
    ap.add_argument("--crop-x-max", type=float); ap.add_argument("--crop-x-min", type=float)
    ap.add_argument("--voxel", type=float, default=15.0)
    ap.add_argument("--save")
    ap.add_argument("--tries", type=int, default=5)
    a = ap.parse_args()
    reg = o3d.pipelines.registration
    T, Tf = pcd(a.car, a.voxel, a.crop_x_max, a.crop_x_min)
    S, Sf = pcd(a.part, a.voxel)
    best = None
    for k in range(a.tries):
        r = reg.registration_ransac_based_on_feature_matching(
            S, T, Sf, Tf, True, a.voxel * 1.5, reg.TransformationEstimationPointToPoint(False), 3,
            [reg.CorrespondenceCheckerBasedOnEdgeLength(0.9), reg.CorrespondenceCheckerBasedOnDistance(a.voxel * 1.5)],
            reg.RANSACConvergenceCriteria(400000, 0.999))
        icp = reg.registration_icp(S, T, a.voxel * 0.6, r.transformation, reg.TransformationEstimationPointToPlane())
        icp = reg.registration_icp(S, T, 6.0, icp.transformation, reg.TransformationEstimationPointToPlane())
        print(f"try {k}: ransac fit={r.fitness:.3f}  icp fit(6mm)={icp.fitness:.3f} rmse={icp.inlier_rmse:.2f}mm")
        if best is None or icp.fitness > best.fitness:
            best = icp
    print("BEST fitness", round(best.fitness, 3), "rmse", round(best.inlier_rmse, 2))
    if a.save:
        json.dump({"T_part_to_car_mm": best.transformation.tolist(), "fitness": best.fitness, "rmse_mm": best.inlier_rmse}, open(a.save, "w"), indent=1)
