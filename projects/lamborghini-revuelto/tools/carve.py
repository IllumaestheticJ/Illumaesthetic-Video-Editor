"""Carve a surround: drop faces of BASE that lie within --d mm of any REF scan (so a state scan can sit inside it
without double surfaces).  carve.py base.stl out.stl --ref a.stl [b.stl ...] --d 15 [--box x0,x1,y0,y1,z0,z1]"""
import argparse, numpy as np
from scipy.spatial import cKDTree
DT = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
ap = argparse.ArgumentParser(); ap.add_argument('base'); ap.add_argument('out'); ap.add_argument('--ref', nargs='+'); ap.add_argument('--d', type=float, default=15); ap.add_argument('--box', help='x0,x1,y0,y1,z0,z1 mm: also drop every base face inside this box')
a = ap.parse_args()
b = np.fromfile(a.base, dtype=DT, offset=84); c = b['v'].mean(1); keep = np.ones(len(b), bool)
for r in a.ref:
    v = np.fromfile(r, dtype=DT, offset=84)['v'].mean(1)[::3]
    lo, hi = v.min(0) - a.d, v.max(0) + a.d; idx = np.where(keep & ((c > lo) & (c < hi)).all(1))[0]
    dist, _ = cKDTree(v).query(c[idx], distance_upper_bound=a.d, workers=-1); keep[idx[np.isfinite(dist)]] = False
if a.box:
    q = [float(x) for x in a.box.split(',')]; keep &= ~((c[:, 0] > q[0]) & (c[:, 0] < q[1]) & (c[:, 1] > q[2]) & (c[:, 1] < q[3]) & (c[:, 2] > q[4]) & (c[:, 2] < q[5]))
out = b[keep]
with open(a.out, 'wb') as f:
    f.write(b'carved'.ljust(80, b' ')); f.write(np.uint32(len(out)).tobytes()); out.tofile(f)
print('faces', len(b), '->', len(out))
