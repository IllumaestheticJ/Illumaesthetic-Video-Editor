"""Rigid transform from Ron's Blender frame (m, nose -Y) to the prepped scan frame (car.blend: m, nose +Y).
No ICP needed: the scan object inside Sentra Review 3.blend still carries its matrix_world from the raw Artec frame
(ron_M.json), and every Artec scan of this car shares that frame. So ron -> artec -> level.json -> prep shift.
(A direct ICP of the bumper-removed scan onto the full car stalled at 20 mm median / 5 deg pitch: open hood, engine bay.)
  ron2car.py ron_M.json level.json car_lvl.stl car_world.npy out.json [check_points.npy]"""
import sys, json, numpy as np
from scipy.spatial import cKDTree
M = np.array(json.load(open(sys.argv[1]))); lv = json.load(open(sys.argv[2]))
Rl, o = np.array(lv['R']), np.array(lv['origin'])
T = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
lvl = np.fromfile(sys.argv[3], dtype=T, offset=84)['v'].reshape(-1, 3)[::40].astype(float) * 0.001
world = np.load(sys.argv[4]).astype(float); tree = cKDTree(world)
S = np.array(json.load(open(sys.argv[4].replace('car_world.npy', 'car.json')))['root_location'])   # seed: prep's shift
for _ in range(30):                               # translation-only fit of the prep shift
    d, i = tree.query(lvl + S, distance_upper_bound=0.5); ok = np.isfinite(d)
    S += np.median(world[i[ok]] - (lvl[ok] + S), axis=0)
d, i = tree.query(lvl + S, distance_upper_bound=0.05)
print('prep shift', S.round(5), 'residual median mm', 1000 * np.median(d[np.isfinite(d)]))
Mi = np.linalg.inv(M[:3, :3]); m = M[:3, 3]
A = 0.001 * Rl @ Mi                               # mine = A @ ron + b
b = S - A @ m - 0.001 * Rl @ o
U, s, Vt = np.linalg.svd(A); print('scale', s.round(5)); R = U @ Vt
print('R', R.round(4).tolist(), 't', b.round(4).tolist())
json.dump({'R': R.tolist(), 't': b.tolist()}, open(sys.argv[5], 'w'), indent=1)
if len(sys.argv) > 6:
    p = np.load(sys.argv[6]).astype(float); p = p[(p[:, 2] > 0.45) & (np.abs(p[:, 0]) < 1.05)] @ R.T + b
    d, _ = tree.query(p, distance_upper_bound=0.05); ok = np.isfinite(d)
    print('check: matched %.0f%%  median %.1f mm' % (100 * ok.mean(), 1000 * np.median(d[ok])))
