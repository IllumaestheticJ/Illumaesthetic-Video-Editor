"""Re-register a front/rear state scan when FPFH lands in a wrong minimum: sweep yaw/pitch/offset inits,
point-to-plane ICP fitted only on a rigid region of the reference (e.g. fenders |x|>min_x), keep the best.
usage: register_sweep.py ref_al.stl src_reg.stl out.stl out.json --y 600,2100 --min-absx 450"""
import sys, json, struct, argparse, itertools, numpy as np, open3d as o3d
TRI = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
ap = argparse.ArgumentParser(); ap.add_argument('ref'); ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('outj')
ap.add_argument('--y', default='600,2100'); ap.add_argument('--min-absx', type=float, default=450)
a = ap.parse_args(); y0, y1 = map(float, a.y.split(','))
r = np.fromfile(a.ref, TRI, offset=84)['v'].mean(1).astype(float)
r = r[(r[:, 1] > y0) & (r[:, 1] < y1) & (np.abs(r[:, 0]) > a.min_absx)]
R = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(r)).voxel_down_sample(6); R.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=25, max_nn=30))
m = np.fromfile(a.src, TRI, offset=84); s = m['v'].mean(1).astype(float)
S = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(s)).voxel_down_sample(6)
c = s.mean(0); best = None
for yaw, pit, dy, dz in itertools.product((-6, -3, 0, 3, 6), (-3, 0, 3), (-80, -40, 0, 40), (-30, 0, 30)):
    Y, Pp = np.radians(yaw), np.radians(pit)
    Rz = np.array([[np.cos(Y), -np.sin(Y), 0], [np.sin(Y), np.cos(Y), 0], [0, 0, 1]]); Rx = np.array([[1, 0, 0], [0, np.cos(Pp), -np.sin(Pp)], [0, np.sin(Pp), np.cos(Pp)]])
    Ri = Rz @ Rx; T = np.eye(4); T[:3, :3] = Ri; T[:3, 3] = c - Ri @ c + [0, dy, dz]
    for thr in (30.0, 10.0):
        T = o3d.pipelines.registration.registration_icp(S, R, thr, T, o3d.pipelines.registration.TransformationEstimationPointToPlane()).transformation
    ev = o3d.pipelines.registration.evaluate_registration(S, R, 5.0, T)
    if best is None or ev.fitness > best[0]: best = (ev.fitness, ev.inlier_rmse, T, (yaw, pit, dy, dz))
f, e, T, init = best; print('best fitness@5mm %.3f rmse %.2f init %s' % (f, e, init))
v = m['v'].astype(float); m['v'] = (v @ T[:3, :3].T + T[:3, 3]).astype('<f4'); m['n'] = (m['n'] @ T[:3, :3].T).astype('<f4')
with open(a.out, 'wb') as fo: fo.write(b'mr2 reg sweep'.ljust(80)); fo.write(struct.pack('<I', len(m))); m.tofile(fo)
json.dump({'T_mm_after_register': T.tolist(), 'fitness_5mm_fenders': f, 'rmse_mm': e, 'init': init}, open(a.outj, 'w'), indent=1)
