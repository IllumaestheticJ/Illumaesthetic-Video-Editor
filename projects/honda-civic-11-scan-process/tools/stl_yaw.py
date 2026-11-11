"""Rotate a binary STL about Z so the car's long axis is +-Y (PCA of the footprint above wheel-hub height).
usage: stl_yaw.py in.stl out.stl [--deg D]   (prints the angle used)"""
import sys, numpy as np
src, dst = sys.argv[1], sys.argv[2]
hdr = open(src, 'rb').read(84); n = np.frombuffer(hdr[80:84], '<u4')[0]
dt = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
d = np.fromfile(src, dt, count=n, offset=84)
v = d['v'].reshape(-1, 3)
if '--deg' in sys.argv:
    ang = np.radians(float(sys.argv[sys.argv.index('--deg') + 1]))
else:
    z = v[:, 2]; m = z > np.percentile(z, 30)
    xy = v[m, :2] - v[m, :2].mean(0)
    w, e = np.linalg.eigh(np.cov(xy.T)); ax = e[:, -1]
    ang = np.arctan2(ax[0], ax[1])            # rotate long axis onto +Y
    if ang > np.pi / 2: ang -= np.pi
    if ang < -np.pi / 2: ang += np.pi
c, s = np.cos(ang), np.sin(ang)
R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], np.float32)
d['v'] = (d['v'].reshape(-1, 3) @ R.T).reshape(-1, 3, 3); d['n'] = d['n'] @ R.T
with open(dst, 'wb') as f: f.write(hdr); d.tofile(f)
print(f"yaw {np.degrees(ang):.3f} deg, {n} tris")
