"""Carve a part that exists only in one state scan: keep state triangles farther than d mm from the base car
(bounded KD-tree query), inside an optional box, largest connected voxel clusters. Also writes the remainder.
usage: diffpart.py base.stl state.stl part.stl [--d 12] [--box x0,x1,y0,y1,z0,z1] [--min-cluster 2000] [--rest rest.stl]"""
import argparse, struct, numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
TRI = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
ap = argparse.ArgumentParser(); ap.add_argument('base'); ap.add_argument('state'); ap.add_argument('out')
ap.add_argument('--d', type=float, default=12); ap.add_argument('--box', default=''); ap.add_argument('--min-cluster', type=int, default=2000)
ap.add_argument('--rest', default=''); ap.add_argument('--vox', type=float, default=15)
a = ap.parse_args()
B = np.fromfile(a.base, TRI, offset=84)['v'].mean(1); S = np.fromfile(a.state, TRI, offset=84); c = S['v'].mean(1)
d, _ = cKDTree(B).query(c, distance_upper_bound=a.d); far = ~np.isfinite(d)
if a.box:
    x0, x1, y0, y1, z0, z1 = map(float, a.box.split(','))
    far &= (c[:, 0] > x0) & (c[:, 0] < x1) & (c[:, 1] > y0) & (c[:, 1] < y1) & (c[:, 2] > z0) & (c[:, 2] < z1)
idx = np.where(far)[0]; q = np.floor((c[idx] - c[idx].min(0)) / a.vox).astype(int)
g = np.zeros(q.max(0) + 1, bool); g[tuple(q.T)] = True
lab, n = ndimage.label(g, structure=np.ones((3, 3, 3))); l = lab[tuple(q.T)]
cnt = np.bincount(l); keepl = np.where(cnt >= a.min_cluster)[0]; keep = np.isin(l, keepl) & (l > 0)
sel = np.zeros(len(S), bool); sel[idx[keep]] = True
def save(p, m):
    with open(p, 'wb') as f: f.write(b'mr2 diffpart'.ljust(80)); f.write(struct.pack('<I', len(m))); m.tofile(f)
save(a.out, S[sel])
if a.rest: save(a.rest, S[~sel])
print('state', len(S), 'far', int(far.sum()), 'part', int(sel.sum()), 'clusters kept', len(keepl), 'bbox', c[sel].min(0).round(), c[sel].max(0).round())
