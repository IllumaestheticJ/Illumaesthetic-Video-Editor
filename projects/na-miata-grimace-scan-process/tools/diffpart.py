"""Extract the geometry present in scan A but not in scan B (e.g. the strut brace): A->B rigid transform,
keep A triangles farther than --thr mm from B, then the largest voxel-connected cluster(s).
usage: diffpart.py A.stl B.stl T.json out_part.stl out_A_inB.stl [--thr 12] [--keep 1]"""
import sys, json, argparse, struct, numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.mesh import TRI
ap = argparse.ArgumentParser(); ap.add_argument('A'); ap.add_argument('B'); ap.add_argument('T'); ap.add_argument('out'); ap.add_argument('outA')
ap.add_argument('--thr', type=float, default=12); ap.add_argument('--keep', type=int, default=1); ap.add_argument('--vox', type=float, default=15)
a = ap.parse_args()
T = json.load(open(a.T)); R = np.array(T['R']); t = np.array(T['t'])
A = np.fromfile(a.A, dtype=TRI, offset=84); B = np.fromfile(a.B, dtype=TRI, offset=84)
A['v'] = (A['v'].reshape(-1, 3) @ R.T + t).reshape(-1, 3, 3); A['n'] = A['n'] @ R.T
def save(p, m):
    with open(p, 'wb') as f: f.write(b'ive diffpart'.ljust(80)); f.write(struct.pack('<I', len(m))); m.tofile(f)
save(a.outA, A)
cA = A['v'].mean(1); tree = cKDTree(B['v'].mean(1)); d, _ = tree.query(cA, distance_upper_bound=200)
sel = d > a.thr; P = A[sel]; c = cA[sel]
ijk = np.floor((c - c.min(0)) / a.vox).astype(int); grid = np.zeros(ijk.max(0) + 1, bool); grid[tuple(ijk.T)] = True
lab, n = ndimage.label(grid, structure=np.ones((3, 3, 3))); L = lab[tuple(ijk.T)]
sizes = np.bincount(L)[1:]; order = np.argsort(-sizes)[:a.keep] + 1
print('diff tris', sel.sum(), 'clusters', n, 'top sizes', sorted(sizes)[-6:][::-1])
keep = np.isin(L, order); P = P[keep]
print('kept', len(P), 'bbox mm', P['v'].reshape(-1, 3).min(0).round(), P['v'].reshape(-1, 3).max(0).round())
save(a.out, P)
