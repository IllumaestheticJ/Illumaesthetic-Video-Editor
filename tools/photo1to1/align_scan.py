"""Align a raw scan (decimated STL, mm, arbitrary frame) to its lookbook model frame (m, Z up, front -Y).
usage: align_scan.py scan_mm.stl glb.npz out_scan_mm_in_glb_frame.stl out_transform.json
Search 24 axis-aligned rotations + scale, trimmed similarity ICP (scan has ground / missing kit, model has kit)."""
import sys, json, itertools, numpy as np
from scipy.spatial import cKDTree
def read_stl(p):
    f = open(p, 'rb'); f.seek(80); n = np.frombuffer(f.read(4), np.uint32)[0]
    return np.fromfile(f, np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]), count=n)
def umeyama(A, B):
    ma, mb = A.mean(0), B.mean(0); A0, B0 = A - ma, B - mb
    U, D, Vt = np.linalg.svd(B0.T @ A0 / len(A)); S = np.eye(3); S[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ S @ Vt; s = 1.0; return s, R, mb - s * R @ ma   # both frames are metric: rigid only
def icp(A, tree, B, s, R, t, it, keep):
    for _ in range(it):
        P = s * A @ R.T + t; d, j = tree.query(P); m = d <= np.quantile(d, keep); s, R, t = umeyama(A[m], B[j[m]])
    d, _ = tree.query(s * A @ R.T + t); return s, R, t, d
rec = read_stl(sys.argv[1]); g = np.load(sys.argv[2]); G = g['v']
Sv = rec['v'].reshape(-1, 3).astype(float) / 1000.0
rng = np.random.default_rng(0); A = Sv[rng.choice(len(Sv), 30000, replace=False)]
B = G[rng.choice(len(G), min(60000, len(G)), replace=False)]; tree = cKDTree(B)
rots = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product([1, -1], repeat=3):
        R = np.zeros((3, 3)); R[range(3), perm] = sg
        if np.linalg.det(R) > 0: rots.append(R)
# Z is up after the floor pre-crop: also sweep heading every 10 deg (scans can sit at any yaw)
for yaw in range(0, 360, 10):
    c_, s_ = np.cos(np.radians(yaw)), np.sin(np.radians(yaw)); rots.append(np.array([[c_, -s_, 0], [s_, c_, 0], [0, 0, 1.0]]))
best = None
# robust centre: scan bbox centre of the 5..95 percentile, model bbox centre
ca = (np.percentile(A, 5, 0) + np.percentile(A, 95, 0)) / 2; cb = (B.min(0) + B.max(0)) / 2
for R0 in rots:
    t0 = cb - R0 @ ca
    s, R, t, d = icp(A, tree, B, 1.0, R0, t0, 25, 0.6)
    sc = np.quantile(d, 0.6)
    if best is None or sc < best[0]: best = (sc, s, R, t)
sc, s, R, t = best
s, R, t, d = icp(A, tree, B, s, R, t, 60, 0.7)
print('ALIGN scale %.4f  median %.1f mm  p70 %.1f mm' % (s, np.median(d) * 1000, np.quantile(d, 0.7) * 1000))
T = (s * Sv @ R.T + t) * 1000.0
out = rec.copy(); out['v'] = T.reshape(-1, 3, 3).astype('<f4')
with open(sys.argv[3], 'wb') as fh: fh.write(b'\0' * 80); fh.write(np.uint32(len(out)).tobytes()); out.tofile(fh)
json.dump({'scale': s, 'R': R.tolist(), 't_m': t.tolist(), 'median_mm': float(np.median(d) * 1000), 'note': 'p_glb_m = scale*R@(p_scan_mm/1000)+t'}, open(sys.argv[4], 'w'), indent=1)
