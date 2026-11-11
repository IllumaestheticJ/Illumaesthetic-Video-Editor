"""Global registration (FPFH + RANSAC, then point-to-plane ICP) of a state/part scan in its own Artec frame onto
the LEVELLED full car (binary STLs, mm). Adapted from projects/a90-supra/tools/globalreg.py (crop on Y = car length).
    python projects/honda-s2000/tools/globalreg.py car_lvl_4mm.stl part_3mm.stl --car-y-max -300 [--part-zmin ..] --save T.json
Saved 4x4 maps part raw mm -> levelled car mm. Prints fitness/RMSE per try; consistent poses across tries = trustworthy."""
import argparse, json
import numpy as np
import open3d as o3d
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])


def pcd(c, voxel):
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c)).voxel_down_sample(voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 3, max_nn=30))
    f = o3d.pipelines.registration.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 6, max_nn=100))
    return p, f


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("car"); ap.add_argument("part")
    ap.add_argument("--car-y-max", type=float); ap.add_argument("--car-y-min", type=float)
    ap.add_argument("--voxel", type=float, default=15.0)
    ap.add_argument("--tries", type=int, default=5)
    ap.add_argument("--init", help="T.json to start ICP from (skip RANSAC)")
    ap.add_argument("--save")
    a = ap.parse_args()
    reg = o3d.pipelines.registration
    c = np.fromfile(a.car, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    if a.car_y_max is not None: c = c[c[:, 1] < a.car_y_max]
    if a.car_y_min is not None: c = c[c[:, 1] > a.car_y_min]
    s = np.fromfile(a.part, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
    T, Tf = pcd(c, a.voxel); S, Sf = pcd(s, a.voxel)
    res = []
    inits = [np.array(json.load(open(a.init))["T_part_to_car_mm"])] if a.init else []
    for k in range(len(inits) or a.tries):
        if inits:
            T0 = inits[k]
        else:
            r = reg.registration_ransac_based_on_feature_matching(
                S, T, Sf, Tf, True, a.voxel * 1.5, reg.TransformationEstimationPointToPoint(False), 3,
                [reg.CorrespondenceCheckerBasedOnEdgeLength(0.9), reg.CorrespondenceCheckerBasedOnDistance(a.voxel * 1.5)],
                reg.RANSACConvergenceCriteria(400000, 0.999))
            T0 = r.transformation
        icp = reg.registration_icp(S, T, a.voxel * 0.8, T0, reg.TransformationEstimationPointToPlane())
        icp = reg.registration_icp(S, T, 8.0, icp.transformation, reg.TransformationEstimationPointToPlane())
        icp = reg.registration_icp(S, T, 4.0, icp.transformation, reg.TransformationEstimationPointToPlane())
        M = icp.transformation
        print(f"try {k}: icp fit(4mm)={icp.fitness:.3f} rmse={icp.inlier_rmse:.2f}mm  t={np.round(M[:3,3]).tolist()}")
        res.append(icp)
    best = max(res, key=lambda r: r.fitness)
    print("BEST fitness", round(best.fitness, 3), "rmse", round(best.inlier_rmse, 2))
    if a.save:
        json.dump({"T_part_to_car_mm": best.transformation.tolist(), "fitness": best.fitness, "rmse_mm": best.inlier_rmse}, open(a.save, "w"), indent=1)
