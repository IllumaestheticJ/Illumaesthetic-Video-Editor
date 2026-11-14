"""Register a loose tail-light part scan onto the car's tail lamp (car raw mm frame).
FPFH + RANSAC over the car's rear corner (each side, part as scanned and mirrored), then point-to-plane ICP 6 -> 2 mm.
Score = share of part points within 2 / 4 mm of the car. The LENS is the outer face of the lamp, so it must lie on the car skin.
    python projects/a90-supra/tools/reg_lamp.py part.stl --out T.json [--tries 8] [--ref other_registered.stl]
--ref: register against an already-placed part instead of the car (housing behind the lens, insert inside the housing)."""
import argparse, json
import numpy as np, open3d as o3d
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
reg = o3d.pipelines.registration
def pts(p): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
def cloud(P, vox):
    c = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(P)).voxel_down_sample(vox)
    c.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=vox * 3, max_nn=30))
    return c, reg.compute_fpfh_feature(c, o3d.geometry.KDTreeSearchParamHybrid(radius=vox * 6, max_nn=100))
ap = argparse.ArgumentParser(); ap.add_argument("part"); ap.add_argument("--out"); ap.add_argument("--tries", type=int, default=8)
ap.add_argument("--ref"); ap.add_argument("--vox", type=float, default=5.0); ap.add_argument("--sides", default="R,L")
a = ap.parse_args()
P = pts(a.part); car = pts(a.ref) if a.ref else pts("/home/user/media/work/a90/car_2mm.stl")
best = None
for side in a.sides.split(","):
    if a.ref: T = car
    else:
        s = -1 if side == "R" else 1
        T = car[(car[:, 0] < -1600) & (s * car[:, 1] > 150) & (s * car[:, 1] < 1050) & (car[:, 2] > 400) & (car[:, 2] < 1000)]
    tc, tf = cloud(T, a.vox); tt = o3d.geometry.KDTreeFlann(tc)
    for mirror in (False, True):
        Q = P * ([1, -1, 1] if mirror else [1, 1, 1]); sc, sf = cloud(Q, a.vox)
        for k in range(a.tries):
            r = reg.registration_ransac_based_on_feature_matching(sc, tc, sf, tf, True, a.vox * 1.5, reg.TransformationEstimationPointToPoint(False), 3,
                [reg.CorrespondenceCheckerBasedOnEdgeLength(0.9), reg.CorrespondenceCheckerBasedOnDistance(a.vox * 1.5)], reg.RANSACConvergenceCriteria(400000, 0.999))
            M = reg.registration_icp(sc, tc, 6.0, r.transformation, reg.TransformationEstimationPointToPlane()).transformation
            M = reg.registration_icp(sc, tc, 2.0, M, reg.TransformationEstimationPointToPlane()).transformation
            q = (np.c_[Q, np.ones(len(Q))] @ M.T)[:, :3][::7]
            d = np.array([np.sqrt(tt.search_knn_vector_3d(x, 1)[2][0]) for x in q])
            f2, f4 = (d < 2).mean(), (d < 4).mean()
            if best is None or f2 > best["f2"]:
                best = dict(side=side, mirror=mirror, f2=float(f2), f4=float(f4), T=M.tolist(), med=float(np.median(d)))
            print(f"{side} mirror={mirror} try{k}: within 2mm {f2:.2f} 4mm {f4:.2f} median {np.median(d):.1f}", flush=True)
print("BEST", {k: v for k, v in best.items() if k != "T"})
if a.out: json.dump(dict(part=a.part, ref=a.ref or "car_2mm", mirror_y=best["mirror"], T_part_to_car_mm=best["T"], **{k: best[k] for k in ("side", "f2", "f4", "med")}), open(a.out, "w"), indent=1)
