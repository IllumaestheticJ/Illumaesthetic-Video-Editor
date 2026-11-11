"""Silhouette camera fit: find the camera whose projected scan silhouette best matches a target mask.

Used for (a) the end card: solve the listing hero view so the last scan shot ends on it, and
(b) refining a rough landmark solve on footage (lesson from FG2: landmark solve -> silhouette refine).

  python silfit.py --stl car.stl --like car.json --mask target_mask.png --init cam.json --out cam_fit.json
        [--fix-focal] [--ignore x0,y0,x1,y1 ...] [--pp cx,cy]

Mask: white = car. Points are projected (no Blender) with a pinhole; cost = symmetric chamfer
between silhouette edges (in px) at 1/4 resolution, minimised with Powell from --init.
"""
import argparse, json, math, sys
import numpy as np, cv2
from scipy.optimize import minimize

sys.path.insert(0, __file__.rsplit('/projects/', 1)[0])
from ive.camera import lookat

ap = argparse.ArgumentParser()
ap.add_argument('--stl', required=True); ap.add_argument('--like', required=True)
ap.add_argument('--mask', required=True); ap.add_argument('--init', required=True)
ap.add_argument('--out', required=True); ap.add_argument('--fix-focal', action='store_true')
ap.add_argument('--ignore', nargs='*', default=[]); ap.add_argument('--pp', default='')
ap.add_argument('--overlay', default='')
ap.add_argument('--bg', default='', help='image to draw the overlay on')
ap.add_argument('--iters', type=int, default=3)
ap.add_argument('--grid', action='store_true')
a = ap.parse_args()

dt = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
with open(a.stl, 'rb') as fh:
    fh.read(80); n = np.frombuffer(fh.read(4), '<u4')[0]; d = np.fromfile(fh, dt, count=n)
like = json.load(open(a.like))
P = d['v'].reshape(-1, 3)[::7].astype(np.float64) * like['unit_scale'] + np.array(like['root_location'])
rng = np.random.default_rng(0); P = P[rng.choice(len(P), min(len(P), 400000), replace=False)]

tgt = cv2.imread(a.mask, 0) > 127
H, W = tgt.shape
S = 4
ign = np.zeros((H // S, W // S), bool)
for b in a.ignore:
    x0, y0, x1, y1 = (int(v) // S for v in b.split(','))
    ign[y0:y1, x0:x1] = True
tg = cv2.resize(tgt.astype(np.uint8), (W // S, H // S), interpolation=cv2.INTER_NEAREST)
def edges(m):
    e = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    return e & ~ign
te = edges(tg)
tdist = cv2.distanceTransform((~te).astype(np.uint8), cv2.DIST_L2, 3)

init = json.load(open(a.init))
R0 = np.array(init['blender']['rotation_matrix']); L0 = np.array(init['blender']['location'])
fwd0 = -R0[:, 2]
# parametrise: camera location (3), yaw/pitch/roll deltas (3), log focal
x0 = np.zeros(7)
fx0 = init['fx_px'] * W / init['image_size'][0]
if a.pp:
    cx, cy = (float(v) for v in a.pp.split(','))
else:
    L = max(W, H)
    cx = W / 2 - init.get('shift_x', 0) * W; cy = H / 2 + init.get('shift_y', 0) * W  # blender HORIZONTAL fit: shift in units of width

def rot(p):
    yaw, pitch, roll = p[3:6] * 0.1
    def Rz(t): c, s = math.cos(t), math.sin(t); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    def Rx(t): c, s = math.cos(t), math.sin(t); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    # small rotations applied in camera frame (pitch about cam x, roll about cam z) and yaw about world z
    return Rz(yaw) @ R0 @ Rx(pitch) @ np.array([[math.cos(roll), -math.sin(roll), 0], [math.sin(roll), math.cos(roll), 0], [0, 0, 1]])

def cam(p):
    R = rot(p); Lc = L0 + p[:3] * 0.5; fx = fx0 * math.exp(p[6] * 0.1)
    return R, Lc, fx

def project(p, scale=1.0):
    R, Lc, fx = cam(p)
    pc = (P - Lc) @ R  # camera coords (blender: x right, y up, -z forward)
    z = -pc[:, 2]; ok = z > 0.1
    u = cx + fx * pc[ok, 0] / z[ok]; v = cy - fx * pc[ok, 1] / z[ok]
    return u * scale, v * scale

def sil(p):
    u, v = project(p, 1 / S)
    m = np.zeros((H // S, W // S), np.uint8)
    k = (u >= 0) & (u < W // S) & (v >= 0) & (v < H // S)
    m[v[k].astype(int), u[k].astype(int)] = 1
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return m

def cost(p):
    if a.fix_focal: p = p.copy(); p[6] = 0
    m = sil(p); e = edges(m)
    if e.sum() < 10: return 1e3
    d1 = tdist[e].mean()
    md = cv2.distanceTransform((~e).astype(np.uint8), cv2.DIST_L2, 3)
    d2 = md[te].mean()
    return d1 + d2

best = x0; c = cost(best); print('init cost (px@1/4)', round(c, 2))
if a.grid:
    # coarse global search: orbit the init camera about the car centre (az, el, distance)
    ctr = P.mean(0)
    for az in np.radians(np.arange(-40, 41, 8)):
        for el in np.radians([-12, -6, 0, 6, 12]):
            for ds in [0.8, 1.0, 1.25]:
                v = (L0 - ctr) * ds
                ca, sa = math.cos(az), math.sin(az)
                v = np.array([ca * v[0] - sa * v[1], sa * v[0] + ca * v[1], v[2]])
                r = math.hypot(v[0], v[1]); e0 = math.atan2(v[2], r); e1 = e0 + el
                ln = np.linalg.norm(v); v = np.array([v[0] / r * ln * math.cos(e1), v[1] / r * ln * math.cos(e1), ln * math.sin(e1)])
                c2 = lookat((ctr + v).tolist(), ctr.tolist(), 1, 1, (W, H))
                R0, L0n = np.array(c2['blender']['rotation_matrix']), np.array(c2['blender']['location'])
                globals()['R0'] = R0; Ls = L0
                globals()['L0'] = L0n
                cc = cost(x0)
                if cc < c: c, best, keep = cc, x0.copy(), (R0, L0n)
                globals()['L0'] = Ls
                globals()['R0'] = np.array(init['blender']['rotation_matrix'])
    if 'keep' in globals(): R0, L0 = keep
    print('grid best cost', round(c, 2))
for it in range(a.iters):
    r = minimize(cost, best, method='Powell', options={'maxiter': 4000, 'xtol': 1e-3, 'ftol': 1e-4})
    if r.fun < c: best, c = r.x, r.fun
    print('iter', it, 'cost', round(c, 3))
if a.fix_focal: best[6] = 0
R, Lc, fx = cam(best)
fwd = -R[:, 2]
out = lookat(Lc.tolist(), (Lc + fwd).tolist(), 1.0, 1.0, (W, H))
# exact rotation (lookat recomputes up; overwrite with fitted R incl. roll)
from ive.solve import _matrix_to_euler_xyz, CV_TO_BLENDER_CAM
out['blender']['rotation_matrix'] = R.tolist(); out['blender']['rotation_euler'] = _matrix_to_euler_xyz(R)
Rcv = (R @ CV_TO_BLENDER_CAM).T
out['opencv'] = {'rvec': cv2.Rodrigues(Rcv)[0].ravel().tolist(), 'tvec': (-Rcv @ Lc).tolist()}
sw = init.get('sensor_width_mm', 36.0)
out.update({'fx_px': fx, 'sensor_width_mm': sw, 'focal_mm': fx / W * sw,
            'shift_x': (W / 2 - cx) / W, 'shift_y': (cy - H / 2) / W,
            'silfit_cost_px': c * S / 2, 'note': 'silfit: mean symmetric edge distance in full-res px'})
json.dump(json.loads(json.dumps(out, default=float)), open(a.out, 'w'), indent=2)
print('focal_mm', round(out['focal_mm'], 2), 'mean edge err px', round(c * S / 2, 2), '->', a.out)
if a.overlay:
    bg = cv2.imread(a.bg) if a.bg else cv2.cvtColor((tgt * 120).astype(np.uint8), cv2.COLOR_GRAY2BGR)
    m = cv2.resize(sil(best), (W, H), interpolation=cv2.INTER_NEAREST)
    e = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    te_full = cv2.morphologyEx(tgt.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    bg[te_full] = (0, 140, 255); bg[e] = (255, 255, 0)
    cv2.imwrite(a.overlay, bg)
