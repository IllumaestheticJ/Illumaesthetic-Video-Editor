"""Register a part/state scan (raw Artec mm) onto the full car (raw mm).
The IS300 part scans (2022-23 sessions) are NOT in the full car's frame (median 37-180 mm off), but close,
so: multi-scale point-to-plane ICP from identity (100 -> 6 mm), optional FPFH+RANSAC global start.
    python projects/lexus-is300/tools/register.py car_4mm.stl part_2mm.stl [--global] [--save T.json] [--apply out.stl]
Reports fitness (share of part points within 5 mm of the car after alignment) and inlier RMSE.
A state scan only overlaps the car where nothing changed, so expect fitness < 1 for "removed/open" states.
"""
import argparse, json, struct
import numpy as np
import open3d as o3d

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
reg = o3d.pipelines.registration


def pcd(c, voxel):
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c)).voxel_down_sample(voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 3, max_nn=30))
    return p


def fpfh(p, voxel):
    return reg.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 6, max_nn=100))


def ms_icp(S, T, T0, dists):
    T_ = T0
    for d in dists:
        r = reg.registration_icp(S, T, d, T_, reg.TransformationEstimationPointToPlane(),
                                 reg.ICPConvergenceCriteria(max_iteration=60))
        T_ = r.transformation
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("car"); ap.add_argument("part")
    ap.add_argument("--global", dest="glob", action="store_true")
    ap.add_argument("--pad", type=float, default=300, help="crop the car to the part bbox + pad (mm)")
    ap.add_argument("--save"); ap.add_argument("--apply")
    ap.add_argument("--init", help="T.json to start from")
    a = ap.parse_args()
    car = np.fromfile(a.car, dtype=TRI, offset=84)["v"].mean(1).astype(float)
    pm = np.fromfile(a.part, dtype=TRI, offset=84)
    pc = pm["v"].mean(1).astype(float)
    lo, hi = pc.min(0) - a.pad, pc.max(0) + a.pad
    car = car[np.all((car > lo) & (car < hi), 1)]
    T = pcd(car, 5.0); S = pcd(pc, 5.0)
    T0 = np.array(json.load(open(a.init))["T_part_to_car_mm"]) if a.init else np.eye(4)
    cands = [ms_icp(S, T, T0, [120, 60, 30, 15, 8, 5])]
    if a.glob:
        Tg, Sg = pcd(car, 15), pcd(pc, 15)
        Tf, Sf = fpfh(Tg, 15), fpfh(Sg, 15)
        for k in range(4):
            r = reg.registration_ransac_based_on_feature_matching(
                Sg, Tg, Sf, Tf, True, 22, reg.TransformationEstimationPointToPoint(False), 3,
                [reg.CorrespondenceCheckerBasedOnEdgeLength(0.9), reg.CorrespondenceCheckerBasedOnDistance(22)],
                reg.RANSACConvergenceCriteria(400000, 0.999))
            cands.append(ms_icp(S, T, r.transformation, [40, 15, 8, 5]))
    for i, c in enumerate(cands):
        print(f"cand {i}: fitness(5mm)={c.fitness:.3f} rmse={c.inlier_rmse:.2f}")
    best = max(cands, key=lambda c: c.fitness)
    M = best.transformation
    ang = np.degrees(np.arccos(np.clip((np.trace(M[:3, :3]) - 1) / 2, -1, 1)))
    print(f"BEST fitness={best.fitness:.3f} rmse={best.inlier_rmse:.2f}mm  shift={np.round(M[:3,3],1)} rot={ang:.2f}deg")
    if a.save:
        json.dump({"T_part_to_car_mm": M.tolist(), "fitness_5mm": best.fitness, "rmse_mm": best.inlier_rmse,
                   "rot_deg": ang}, open(a.save, "w"), indent=1)
    if a.apply:
        R, t = M[:3, :3].astype(np.float32), M[:3, 3].astype(np.float32)
        out = pm.copy()
        out["v"] = pm["v"] @ R.T + t
        out["n"] = pm["n"] @ R.T
        with open(a.apply, "wb") as f:
            f.write(b"is300 registered".ljust(80)); f.write(struct.pack("<I", len(out))); out.tofile(f)
        print("wrote", a.apply)


if __name__ == "__main__":
    main()
