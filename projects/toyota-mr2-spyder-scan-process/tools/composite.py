"""Column-wise state composite (all STLs already aligned/registered, mm):
drop base triangles that sit in an XY column (cell mm) covered by the state scan, within the state's
z-range +-pad, and beyond y_min; then append the state scan as captured.
usage: composite.py base.stl state.stl out.stl --y-min 750 [--cell 25 --pad 60]"""
import sys, struct, argparse, numpy as np
TRI = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
ap = argparse.ArgumentParser(); ap.add_argument('base'); ap.add_argument('state'); ap.add_argument('out')
ap.add_argument('--y-min', type=float, default=-1e9); ap.add_argument('--y-max', type=float, default=1e9)
ap.add_argument('--cell', type=float, default=25); ap.add_argument('--pad', type=float, default=60)
a = ap.parse_args()
B = np.fromfile(a.base, TRI, offset=84); S = np.fromfile(a.state, TRI, offset=84)
cs = S['v'].mean(1); cb = B['v'].mean(1)
sel = (cs[:, 1] > a.y_min) & (cs[:, 1] < a.y_max); S = S[sel]; cs = cs[sel]
key = lambda c: (np.floor(c[:, 0] / a.cell).astype(np.int64) << 32) + np.floor(c[:, 1] / a.cell).astype(np.int64)
ks = key(cs); u, inv = np.unique(ks, return_inverse=True)
zmin = np.full(len(u), np.inf); zmax = np.full(len(u), -np.inf); np.minimum.at(zmin, inv, cs[:, 2]); np.maximum.at(zmax, inv, cs[:, 2])
kb = key(cb); idx = np.searchsorted(u, kb); idx[idx >= len(u)] = 0; hit = u[idx] == kb
zl, zh = zmin[idx], zmax[idx]
drop = hit & (cb[:, 2] > zl - a.pad) & (cb[:, 2] < zh + a.pad) & (cb[:, 1] > a.y_min) & (cb[:, 1] < a.y_max)
out = np.concatenate([B[~drop], S])
with open(a.out, 'wb') as f:
    f.write(b'mr2 composite'.ljust(80)); f.write(struct.pack('<I', len(out))); out.tofile(f)
print('base', len(B), 'dropped', int(drop.sum()), 'state', len(S), 'out', len(out))
