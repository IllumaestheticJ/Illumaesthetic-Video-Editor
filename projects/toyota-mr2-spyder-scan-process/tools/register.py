"""Register a part-state scan (different Artec frame) onto the aligned full-car scan.
FPFH + RANSAC global match, then point-to-plane ICP; writes the registered STL + 4x4 (mm).
Usage: register.py ref_al.stl src_al.stl out.stl out.json [--crop-y ymin,ymax]"""
import json, sys, struct
import numpy as np, open3d as o3d
TRI = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])

def pcd(path, crop=None, every=1):
    m = np.fromfile(path, TRI, offset=84); c = m['v'].mean(1)[::every].astype(np.float64)
    if crop: c = c[(c[:, 1] > crop[0]) & (c[:, 1] < crop[1])]
    p = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(c)); return p

def feats(p, vox):
    d = p.voxel_down_sample(vox)
    d.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=vox * 2.5, max_nn=30))
    f = o3d.pipelines.registration.compute_fpfh_feature(d, o3d.geometry.KDTreeSearchParamHybrid(radius=vox * 5, max_nn=100))
    return d, f

ref, src, out, outj = sys.argv[1:5]
crop = None
if '--crop-y' in sys.argv: crop = [float(v) for v in sys.argv[sys.argv.index('--crop-y') + 1].split(',')]
R = pcd(ref, crop); S = pcd(src)
best = None
for vox in (40.0, 25.0):
    rd, rf = feats(R, vox); sd, sf = feats(S, vox)
    for seed in range(4):
        o3d.utility.random.seed(seed)
        res = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
            sd, rd, sf, rf, True, vox * 1.5,
            o3d.pipelines.registration.TransformationEstimationPointToPoint(False), 3,
            [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
             o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(vox * 1.5)],
            o3d.pipelines.registration.RANSACConvergenceCriteria(400000, 0.999))
        if best is None or res.fitness > best.fitness: best = res
    print('vox', vox, 'ransac fitness %.3f rmse %.1f' % (best.fitness, best.inlier_rmse))
T = best.transformation
Rf = R.voxel_down_sample(8.0); Rf.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=25, max_nn=30))
Sf = S.voxel_down_sample(8.0)
for thr in (40.0, 15.0, 6.0):
    icp = o3d.pipelines.registration.registration_icp(Sf, Rf, thr, T, o3d.pipelines.registration.TransformationEstimationPointToPlane())
    T = icp.transformation; print('icp thr', thr, 'fitness %.3f rmse %.2f mm' % (icp.fitness, icp.inlier_rmse))
m = np.fromfile(src, TRI, offset=84); v = m['v'].astype(np.float64)
m['v'] = (v @ T[:3, :3].T + T[:3, 3]).astype('<f4'); m['n'] = (m['n'] @ T[:3, :3].T).astype('<f4')
with open(out, 'wb') as f:
    f.write(b'mr2 registered'.ljust(80)); f.write(struct.pack('<I', len(m))); m.tofile(f)
json.dump({'T_mm': T.tolist(), 'icp_fitness': icp.fitness, 'icp_rmse_mm': icp.inlier_rmse, 'ref': ref, 'src': src}, open(outj, 'w'), indent=1)
