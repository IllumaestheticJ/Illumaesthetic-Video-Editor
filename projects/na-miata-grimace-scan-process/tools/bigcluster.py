"""Keep the largest voxel-connected cluster(s) of an STL (removes scanned floor shards/debris). usage: in out [vox_mm] [keep]"""
import sys, struct, numpy as np
from scipy import ndimage
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.mesh import TRI
m = np.fromfile(sys.argv[1], dtype=TRI, offset=84); vox = float(sys.argv[3]) if len(sys.argv) > 3 else 20; keep = int(sys.argv[4]) if len(sys.argv) > 4 else 1
c = m['v'].mean(1); ijk = np.floor((c - c.min(0)) / vox).astype(int)
g = np.zeros(ijk.max(0) + 1, bool); g[tuple(ijk.T)] = True
lab, n = ndimage.label(g, structure=np.ones((3, 3, 3))); L = lab[tuple(ijk.T)]; s = np.bincount(L)
top = np.argsort(-s[1:])[:keep] + 1; k = m[np.isin(L, top)]
print('clusters', n, 'kept', len(k), 'of', len(m))
with open(sys.argv[2], 'wb') as f: f.write(b'ive bigcluster'.ljust(80)); f.write(struct.pack('<I', len(k))); k.tofile(f)
