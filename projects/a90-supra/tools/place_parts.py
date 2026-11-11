"""Register bench-scanned suspension parts into the car frame, per wheel corner.

The base chassis scan (car on stands, wheels off) still contains the hubs, knuckles, coilovers and brakes inside
the arches, so each part is matched against the car points inside a box around that arch:
FPFH + RANSAC (several tries) -> point-to-plane ICP (coarse then 3 mm). The part is tried as scanned and mirrored
in Y (left/right hand). A pose is accepted only if several tries agree (same pose within 5 mm / 3 deg) and the
fitness at 3 mm is high enough.

    python projects/a90-supra/tools/place_parts.py car_2mm.stl part.stl --corner FR [--out T.json] [--tries 6]
Corners (car mm frame, +X nose, -Y right): FR/FL x 650..1750, RR/RL x -1800..-700, |y| 250..1050, z -50..800.
"""
import argparse
import json

import numpy as np
import open3d as o3d

TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
BOX = {"FR": ((650, 1750), (-1050, -250)), "FL": ((650, 1750), (250, 1050)),
       "RR": ((-1800, -700), (-1050, -250)), "RL": ((-1800, -700), (250, 1050))}
reg = o3d.pipelines.registration


def load(path):
    return np.fromfile(path, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)


def cloud(pts, voxel):
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pts)).voxel_down_sample(voxel)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 3, max_nn=30))
    f = reg.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=voxel * 6, max_nn=100))
    return p, f


def rot_angle(R):
    return np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))


def run(car_pts, part_pts, corner, tries, voxel):
    (x0, x1), (y0, y1) = BOX[corner]
    m = (car_pts[:, 0] > x0) & (car_pts[:, 0] < x1) & (car_pts[:, 1] > y0) & (car_pts[:, 1] < y1) & (car_pts[:, 2] < 800)
    T, Tf = cloud(car_pts[m], voxel)
    out = []
    for mirror in (False, True):
        P = part_pts * ([1, -1, 1] if mirror else [1, 1, 1])
        S, Sf = cloud(P, voxel)
        for k in range(tries):
            r = reg.registration_ransac_based_on_feature_matching(
                S, T, Sf, Tf, True, voxel * 1.5, reg.TransformationEstimationPointToPoint(False), 3,
                [reg.CorrespondenceCheckerBasedOnEdgeLength(0.9), reg.CorrespondenceCheckerBasedOnDistance(voxel * 1.5)],
                reg.RANSACConvergenceCriteria(300000, 0.999))
            icp = reg.registration_icp(S, T, voxel, r.transformation, reg.TransformationEstimationPointToPlane())
            icp = reg.registration_icp(S, T, 3.0, icp.transformation, reg.TransformationEstimationPointToPlane())
            out.append({"mirror": mirror, "fit3": icp.fitness, "rmse": icp.inlier_rmse, "T": icp.transformation})
    return out


def agree(a, b):
    return np.linalg.norm(a["T"][:3, 3] - b["T"][:3, 3]) < 5 and rot_angle(a["T"][:3, :3].T @ b["T"][:3, :3]) < 3


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("car"); ap.add_argument("part")
    ap.add_argument("--corner", required=True, choices=list(BOX))
    ap.add_argument("--tries", type=int, default=6)
    ap.add_argument("--voxel", type=float, default=6.0)
    ap.add_argument("--out")
    a = ap.parse_args()
    res = run(load(a.car), load(a.part), a.corner, a.tries, a.voxel)
    res.sort(key=lambda r: -r["fit3"])
    best = res[0]
    votes = sum(agree(best, r) for r in res if r["mirror"] == best["mirror"])
    name = a.part.split("/")[-1]
    print(f"{name:30s} {a.corner} mirror={best['mirror']} fit@3mm={best['fit3']:.3f} rmse={best['rmse']:.2f} "
          f"agree={votes}/{a.tries}  t={np.round(best['T'][:3, 3]).tolist()}  "
          f"(other hand best fit {max(r['fit3'] for r in res if r['mirror'] != best['mirror']):.3f})")
    if a.out:
        json.dump({"part": a.part, "corner": a.corner, "mirror_y": bool(best["mirror"]), "fit3": float(best["fit3"]), "rmse": float(best["rmse"]),
                   "agree": int(votes), "tries": a.tries, "T_part_to_car_mm": best["T"].tolist()}, open(a.out, "w"), indent=1)
