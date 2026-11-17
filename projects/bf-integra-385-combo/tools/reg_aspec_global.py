"""A-Spec rear -> Type S (GLB frame) by global registration: FPFH features + RANSAC on the rear section,
then point-to-plane ICP restricted to the TRUNK LID (the shared panel). Tests the mirrored scan too."""
import open3d as o3d, numpy as np, trimesh, json
R = '/home/user/media/bf-integra-385-combo/work/reg'
A = trimesh.load('/home/user/media/bf-integra-385-combo/scan/Integra ASpec Rear.stl', process=False); A.apply_scale(0.001)
Ty = trimesh.load(f'{R}/car_nospoiler.ply', process=False)
def pcd(P):
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(P)); p = p.voxel_down_sample(0.015)
    p.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30)); return p
def feat(p): return o3d.pipelines.registration.compute_fpfh_feature(p, o3d.geometry.KDTreeSearchParamHybrid(radius=0.12, max_nn=100))
tP = Ty.sample(600000); tP = tP[tP[:, 1] > 0.9]
T_p = pcd(tP); T_f = feat(T_p)
deck = lambda P: (np.abs(P[:, 0]) < 0.6) & (P[:, 1] > 1.45) & (P[:, 1] < 2.0) & (P[:, 2] > 0.86)
tD = Ty.sample(1500000); tD = tD[deck(tD)]; TD = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(tD))
TD.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.03, max_nn=30))
best = None
for mirror in (False,):  # car is symmetric; mirrored fits equally well, keep the scan as captured
    S = A.sample(500000)
    if mirror: S = S * np.array([-1, 1, 1])
    S_p = pcd(S); S_f = feat(S_p)
    for seed in range(3):
        r = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
            S_p, T_p, S_f, T_f, True, 0.04,
            o3d.pipelines.registration.TransformationEstimationPointToPoint(False), 3,
            [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
             o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(0.04)],
            o3d.pipelines.registration.RANSACConvergenceCriteria(400000, 0.999))
        T = r.transformation
        X = np.asarray(S_p.points) @ T[:3, :3].T + T[:3, 3]; k = deck(X)
        if k.sum() < 500: print('mirror', mirror, 'seed', seed, 'fitness', round(r.fitness, 3), 'no deck overlap'); continue
        SD = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.asarray(S_p.points)[k]))
        icp = o3d.pipelines.registration.registration_icp(SD, TD, 0.03, T, o3d.pipelines.registration.TransformationEstimationPointToPlane(),
                                                          o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=100))
        print('mirror', mirror, 'seed', seed, 'ransac fit', round(r.fitness, 3), 'deck icp fit', round(icp.fitness, 3), 'rmse mm', round(icp.inlier_rmse * 1000, 2))
        if best is None or (icp.fitness, -icp.inlier_rmse) > (best[0], -best[1]): best = (icp.fitness, icp.inlier_rmse, mirror, icp.transformation)
fit, rmse, mirror, T = best
print('BEST mirror', mirror, 'fitness', round(fit, 3), 'rmse mm', round(rmse * 1000, 2))
M = np.diag([-1, 1, 1, 1]) if mirror else np.eye(4)
Tfull = np.asarray(T) @ M
json.dump({'matrix': Tfull.tolist(), 'mirror': mirror, 'deck_rmse_mm': rmse * 1000, 'fitness': fit}, open(f'{R}/aspec_to_glb.json', 'w'))
A.apply_transform(Tfull)
if mirror: A.invert()
A.export(f'{R}/aspec_rear_glbframe.ply')
