"""Align the Epsilon lookbook FG2 game model to the scan frame (= Ecky's / Artec frame, metres).
1) lip part (same CAD as 'FG2 Race Lip.stl') -> exact rigid fit; 2) body+trim vs scan, trimmed ICP (similarity) from there."""
import numpy as np, json, sys
from scipy.spatial import cKDTree
G = np.load('/home/user/media/work/fg2/scan/game_pts.npz'); S = np.load('/home/user/media/work/fg2/scan/fg2_lq_small.npz')['v']
f = open('/home/user/media/fg2/cgi/FG2 Race Lip.stl', 'rb'); f.seek(80); n = np.frombuffer(f.read(4), np.uint32)[0]
dt = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]); L = np.unique(np.fromfile(f, dt, count=n)['v'].reshape(-1, 3).astype(float) / 1000, axis=0)
def umeyama(A, B, scale):
    ma, mb = A.mean(0), B.mean(0); A0, B0 = A - ma, B - mb
    U, D, Vt = np.linalg.svd(B0.T @ A0 / len(A)); Sg = np.eye(3); Sg[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ Sg @ Vt; s = (D * np.diag(Sg)).sum() / A0.var(0).sum() if scale else 1.0
    return s, R, mb - s * R @ ma
def icp(A, B, s, R, t, iters, keep, scale):
    tree = cKDTree(B)
    for k in range(iters):
        P = s * A @ R.T + t; d, j = tree.query(P); m = d <= np.quantile(d, keep)
        s, R, t = umeyama(A[m], B[j[m]], scale)
    P = s * A @ R.T + t; d, _ = tree.query(P)
    return s, R, t, d
R0 = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1.0]])  # game front -Y -> scan front -X
gl = G['part_front_lip'][::4]
t0 = L.mean(0) - R0 @ gl.mean(0)
s1, R1, t1, d1 = icp(gl, L[::2], 1.0, R0, t0, 40, 0.95, False)
print('lip fit: median %.2f mm, p90 %.2f mm' % (np.median(d1) * 1000, np.percentile(d1, 90) * 1000))
body = np.r_[G['body'], G['trim'][::2]]
d_lipT = cKDTree(S).query(s1 * body @ R1.T + t1)[0]
print('body vs scan using lip transform: median %.1f mm, p75 %.1f mm' % (np.median(d_lipT) * 1000, np.percentile(d_lipT, 75) * 1000))
s2, R2, t2, d2 = icp(body, S, s1, R1, t1, 60, 0.7, True)
print('body ICP: scale %.4f, median %.1f mm, p75 %.1f mm' % (s2, np.median(d2) * 1000, np.percentile(d2, 75) * 1000))
dl = cKDTree(L).query(s2 * gl @ R2.T + t2)[0]
print('lip offset after body ICP: median %.1f mm' % (np.median(dl) * 1000))
M = np.eye(4); M[:3, :3] = s2 * R2; M[:3, 3] = t2
Ml = np.eye(4); Ml[:3, :3] = R1; Ml[:3, 3] = t1
json.dump({'body_to_scan': M.tolist(), 'lip_to_scan': Ml.tolist(), 'scale': s2}, open('/home/user/media/work/fg2/scan/game_to_scan.json', 'w'), indent=1)
