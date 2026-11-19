"""v2.1 (user: "MR2 Spyder needs the front bumper scan to transition to the 'bumper removed scan' for a clean cut").
Same method as nc_bumper_state.py, with the engineering Drive scan 'Front Bumper Data/hood closed no bumper.stl'
(1Id9y9SVLsgm4Ta4EJRfC4smGDkmshsQU). It is a separate front-end project in its own frame, so:
1. Global registration onto the full-car scan (GLB frame): Open3D FPFH + RANSAC, then point-to-plane ICP (30 -> 6 mm).
   Result 2026-11-19: 43 % of the state within 6 mm at 2.6 mm RMSE (the rest is what the bumper hid).
   Open3D needs libEGL to import: a stub of its 13 egl* symbols is enough (LD_LIBRARY_PATH=/opt/egl).
2. Bumper zone = full-car nose triangles the bumper-off state does NOT confirm (nearest > TOL) = the real shut line.
3. 'under' = state triangles the full car does not have (crash bar, radiators, supports): shown once the bumper is off.
    LD_LIBRARY_PATH=/opt/egl python mr2_bumper_state.py -> dec/mr2off_glbframe.stl, mr2_bumper_idx.npy, mr2_under_bumper.stl"""
import json, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl
M = "/home/user/media/bf-miata-mr2-night-meet"; D = f"{M}/dec"; TOL = 0.010
j = json.load(open(f"{D}/mr2_glbframe.json")); r = json.load(open(f"{D}/mr2_glbframe_refine.json"))
SC = 0.001 * j["s"] / r["s"]                      # same mm -> lookbook scale as the full-car scan
S = read_stl(f"{M}/scans_mr2off/hood closed no bumper.stl") * SC
F = read_stl(f"{D}/mr2_glbframe.stl"); Cf = F.mean(1)
TP = f"{D}/mr2off_T.npy"
if not os.path.exists(TP):
    import open3d as o3d
    R = o3d.pipelines.registration
    def pc(T, vox):
        n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
        p = o3d.geometry.PointCloud(); p.points = o3d.utility.Vector3dVector(T.mean(1)); p.normals = o3d.utility.Vector3dVector(n)
        return p.voxel_down_sample(vox)
    Ff = F[Cf[:, 1] < -0.2]; a, b = pc(S, 0.02), pc(Ff, 0.02)
    fa, fb = (R.compute_fpfh_feature(x, o3d.geometry.KDTreeSearchParamHybrid(radius=0.10, max_nn=100)) for x in (a, b))
    best = None
    for seed in range(4):
        o3d.utility.random.seed(seed)
        res = R.registration_ransac_based_on_feature_matching(a, b, fa, fb, True, 0.03, R.TransformationEstimationPointToPoint(False), 3,
            [R.CorrespondenceCheckerBasedOnEdgeLength(0.9), R.CorrespondenceCheckerBasedOnDistance(0.03)], R.RANSACConvergenceCriteria(2000000, 0.9999))
        if best is None or res.fitness > best.fitness: best = res
    T = best.transformation; af, bf = pc(S, 0.006), pc(Ff, 0.006)
    for dist in (0.03, 0.012, 0.006):
        res = R.registration_icp(af, bf, dist, T, R.TransformationEstimationPointToPlane()); T = res.transformation
        print("icp", dist, "fitness %.3f rmse %.2f mm" % (res.fitness, res.inlier_rmse * 1e3))
    np.save(TP, T)
T = np.load(TP)
V = (S.reshape(-1, 3) @ T[:3, :3].T + T[:3, 3]).reshape(-1, 3, 3); Cs = V.mean(1)
tf = cKDTree(Cf); d, _ = tf.query(Cs, workers=-1)
print("state->full: within 5 mm %.0f %%, median %.1f mm; bbox" % (100 * np.mean(d < 0.005), np.median(d) * 1e3), Cs.min(0).round(2), Cs.max(0).round(2))
write_stl(f"{D}/mr2off_glbframe.stl", V)
ts = cKDTree(Cs)
# the state is a partial scan: only judge full-car triangles inside the state's coverage (lateral x range, nose, below the hood line)
x0, x1 = np.percentile(Cs[:, 0], [0.5, 99.5])
nose = (Cf[:, 1] < -1.05) & (Cf[:, 2] < 0.80)
idx = np.where(nose)[0]; dfs, _ = ts.query(Cf[nose], workers=-1)
bump = idx[dfs > TOL]; np.save(f"{D}/mr2_bumper_idx_raw.npy", bump)
print("state x coverage %.2f..%.2f; unconfirmed nose tris %d of %d; bbox" % (x0, x1, len(bump), int(nose.sum())), Cf[bump].min(0).round(2), Cf[bump].max(0).round(2))
und = (d > TOL) & (Cs[:, 1] < -1.05) & (Cs[:, 2] < 0.80)
write_stl(f"{D}/mr2_under_bumper_raw.stl", V[und]); print("under tris", int(und.sum()))
# 4. the state is a partial scan, so "unconfirmed" also flags places it never captured (arch liners, tyres, underside).
#    Gate with the lookbook stock bumper as a coarse region (within 60 mm); the state still decides the actual shut line.
K = f"{M}/kit_mr2"
def samp(T, step=0.006):
    rng = np.random.default_rng(0); a = np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1) / 2
    k = np.minimum(np.maximum(1, np.ceil(a / step ** 2)).astype(int), 3000); i = np.repeat(np.arange(len(T)), k)
    q = rng.random((len(i), 2)); m = q.sum(1) > 1; q[m] = 1 - q[m]
    return T[i, 0] + q[:, :1] * (T[i, 1] - T[i, 0]) + q[:, 1:] * (T[i, 2] - T[i, 0])
G = cKDTree(np.concatenate([samp(read_stl(f"{K}/{n}.stl")) for n in ("body_front_bumper_stock", "trim_front_bumper_stock")]))
dg, _ = G.query(Cf[bump], workers=-1); zone = bump[dg < 0.060]
np.save(f"{D}/mr2_bumper_idx.npy", zone); print("bumper zone tris", len(zone))
du, _ = G.query(Cs[und], workers=-1); U = V[und][du < 0.25]
U = U[(U.mean(1)[:, 1] > -1.92) & (U.mean(1)[:, 2] > 0.17)]      # drop stray fragments below the car / ahead of the nose
write_stl(f"{D}/mr2_under_bumper.stl", U); print("under tris kept", len(U))
