"""Cut exploded-view parts out of the single full-car EK scan (there are no separate part scans).
Regions are in PREPPED metres (ek.json transform); writes mm STLs in the source frame so each part
is prepped with --like ek.json and lines up exactly.
usage: split_parts.py yaw.stl ek.json facelab.npy outdir"""
import sys, json, numpy as np
src, pj, labf, out = sys.argv[1:5]
n = np.fromfile(src, '<u4', 1, offset=80)[0]
dt = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]); d = np.fromfile(src, dt, n, offset=84)
p = json.load(open(pj)); P = d['v'] * p['unit_scale'] + np.array(p['root_location'])   # (n,3,3) prepped metres
c = P.mean(1); x, y, z = c.T
e1 = P[:, 1] - P[:, 0]; e2 = P[:, 2] - P[:, 0]; nn = np.cross(e1, e2); nn /= np.linalg.norm(nn, axis=1, keepdims=True) + 1e-12
lab = np.load(labf); cnt = np.bincount(lab); big = np.argsort(-cnt)[:5]   # body + 4 wheels
wheels = big[1:]
parts = {}
for w in wheels:
    m = lab == w; cx, cy = x[m].mean(), y[m].mean()
    parts[f"wheel_{'F' if cy < 0 else 'R'}{'L' if cx > 0 else 'R'}"] = m
body = lab == big[0]
parts['bumper_F'] = body & (y < -1.48) & (z < 0.575)
parts['bumper_R'] = body & (y > 1.59) & (z < 0.65)
parts['hood'] = body & (x > -0.72) & (x < 0.69) & (y > -2.0) & (y < -0.87) & (z > 0.6) & (nn[:, 2] > 0.45)
used = np.zeros(n, bool)
for k, m in parts.items(): used |= m
parts['base'] = ~used
def write(m, f):
    with open(f, 'wb') as fh:
        fh.write(b'split_parts'.ljust(80, b' ')); fh.write(np.uint32(m.sum()).tobytes()); d[m].tofile(fh)
for k, m in parts.items():
    write(m, f"{out}/part_{k}.stl"); q = P[m].reshape(-1, 3)
    print(k, int(m.sum()), q.min(0).round(3), q.max(0).round(3))
