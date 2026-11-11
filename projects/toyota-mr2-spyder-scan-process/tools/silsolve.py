"""Camera solve by silhouette chamfer: scan (npz V,F in prepped Blender metres) vs a frame car mask.
Coarse global search over look-at params, then Powell/NM refine of rvec/tvec/f (+ optional landmarks).
usage: silsolve.py mask.png mesh.npz out.json --init cam.json --sensor 20.25 [--focal-range 16,30]
       [--ignore 'x0,y0,x1,y1;..'] [--points pts.json --wpts 0.5] [--fix-f] [--lock-z 1.4] [--no-global]"""
import sys, json, argparse, numpy as np, cv2
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
from ive.camera import lookat
from scipy.optimize import minimize
ap = argparse.ArgumentParser()
ap.add_argument('mask'); ap.add_argument('mesh'); ap.add_argument('out')
ap.add_argument('--init', required=True); ap.add_argument('--sensor', type=float, default=20.25)
ap.add_argument('--focal-range', default='14,40'); ap.add_argument('--ignore', default='')
ap.add_argument('--points'); ap.add_argument('--wpts', type=float, default=0.5)
ap.add_argument('--fix-f', action='store_true'); ap.add_argument('--work', type=int, default=600)
ap.add_argument('--T', type=float, default=15); ap.add_argument('--no-global', action='store_true')
ap.add_argument('--cx', type=float, default=None, help='principal point x (full-res px) if not centred')
a = ap.parse_args()
M0 = cv2.imread(a.mask, 0); H0, W0 = M0.shape; s = a.work / W0
pm = (cv2.resize(M0, (a.work, int(H0 * s)), interpolation=cv2.INTER_AREA) > 127).astype(np.uint8) * 255; h, w = pm.shape
cx = (a.cx if a.cx is not None else W0 / 2) * s; cy = h / 2
m = np.load(a.mesh); V, F = m['v'].astype(np.float64), m['f']
keep = np.ones((h, w), bool); b = 3; keep[:b] = keep[-b:] = False; keep[:, :b] = keep[:, -b:] = False
for box in filter(None, a.ignore.split(';')):
    x0, y0, x1, y1 = [int(float(v) * s) for v in box.split(',')]; keep[max(0,y0):y1, max(0,x0):x1] = False
edge = lambda mk: cv2.morphologyEx(mk, cv2.MORPH_GRADIENT, np.ones((3, 3))) > 0
pe = edge(pm) & keep; dt_p = cv2.distanceTransform((~pe).astype(np.uint8), cv2.DIST_L2, 3); pys, pxs = np.nonzero(pe)
pts = json.load(open(a.points))['points'] if a.points else []
O = np.array([p['xyz'] for p in pts], float); I = np.array([p['px'] for p in pts], float) * s
def K_(f): return np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]])
def sil(r, t, f):
    p, _ = cv2.projectPoints(V, r, t, K_(f), None); p = p.reshape(-1, 2)
    R, _ = cv2.Rodrigues(r); z = (V @ R.T + t.reshape(1, 3))[:, 2]
    ok = (z[F] > 0.05).all(1) & (np.abs(p[F]) < 4 * w).all((1, 2))
    q = np.round(p * 4).astype(np.int32)
    mk = np.zeros((h, w), np.uint8); cv2.fillPoly(mk, list(q[F[ok]]), 255, shift=2)
    return cv2.morphologyEx(mk, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
def cost_rtf(r, t, f, verbose=False):
    mk = sil(r, t, f); re = edge(mk) & keep; ys, xs = np.nonzero(re)
    if len(xs) < 50: return 1e3
    d1 = np.minimum(dt_p[ys, xs], a.T).mean()
    dt_r = cv2.distanceTransform((~edge(mk)).astype(np.uint8), cv2.DIST_L2, 3)
    d2 = np.minimum(dt_r[pys, pxs], a.T).mean()
    inter = ((mk > 0) & (pm > 0)).sum(); iou = inter / max(1, ((mk > 0) | (pm > 0)).sum())
    c = d1 + d2 + 10 * (1 - iou)
    if len(pts):
        q, _ = cv2.projectPoints(O, r, t, K_(f), None); e = np.linalg.norm(q.reshape(-1, 2) - I, axis=1)
        c += a.wpts * np.sqrt((e ** 2).mean())
    if verbose: print(f"chamfer {d1:.2f}/{d2:.2f} iou {iou:.3f} total {c:.2f} (px @ {w}w)")
    return c
cam = json.load(open(a.init))
def from_cam(c): return np.array(c['opencv']['rvec'], float), np.array(c['opencv']['tvec'], float), c['fx_px'] * s * (W0 / c['image_size'][0])
r0, t0, f0 = from_cam(cam)
if not a.no_global:
    # global: perturb camera location / target / focal around init (look-at param)
    Rb = np.array(cam['blender']['rotation_matrix']); loc = np.array(cam['blender']['location'])
    fwd = -Rb[:, 2]; tgt0 = loc + fwd * 2.0
    best = (cost_rtf(r0, t0, f0), r0, t0, f0); rng = np.random.default_rng(0)
    flo, fhi = map(float, a.focal_range.split(','))
    for it in range(1200):
        sc = 1.0 if it < 600 else 0.4
        if it >= 600: Rb2 = best[4]; loc = best[5]; tgt0 = best[6]
        L = loc + rng.normal(0, [0.35 * sc, 0.35 * sc, 0.25 * sc]); T = tgt0 + rng.normal(0, [0.3 * sc, 0.3 * sc, 0.2 * sc])
        fmm = np.clip((best[3] / s / W0 * a.sensor if it >= 600 else rng.uniform(flo, fhi)) * np.exp(rng.normal(0, 0.08 * sc)), flo, fhi)
        roll = rng.normal(0, 4 * sc)
        c = lookat(L, T, fmm, a.sensor, (W0, H0), roll)
        r, t, f = from_cam(c); cc = cost_rtf(r, t, f)
        if cc < best[0]: best = (cc, r, t, f, None, L, T); print(it, 'global', round(cc, 2), 'f', round(fmm, 1), L.round(2))
        if it == 599 and len(best) < 7: best = best + (None, loc, tgt0)
    r0, t0, f0 = best[1], best[2], best[3]
def unpack(x): return r0 + x[:3] * 0.01, t0 + x[3:6] * 0.02, f0 * np.exp(0 if a.fix_f else x[6] * 0.02)
cost = lambda x: cost_rtf(*unpack(x))
x = np.zeros(7); print('before refine:'); cost_rtf(*unpack(x), True)
res = minimize(cost, x, method='Powell', options={'maxiter': 3000, 'xtol': 1e-3, 'ftol': 1e-4})
res = minimize(cost, res.x, method='Nelder-Mead', options={'maxiter': 1500, 'xatol': 1e-3, 'fatol': 1e-4})
r, t, f = unpack(res.x); print('after:'); cost_rtf(r, t, f, True)
fx = f / s; R, _ = cv2.Rodrigues(r); loc = (-R.T @ t).ravel(); Rb = R.T @ CV_TO_BLENDER_CAM
shift_x = (W0 / 2 - (a.cx if a.cx is not None else W0 / 2)) / max(W0, H0)
out = {"image_size": [W0, H0], "fx_px": fx, "focal_mm": fx / W0 * a.sensor, "sensor_width_mm": a.sensor,
       "shift_x": shift_x, "shift_y": 0.0,
       "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rb), "rotation_matrix": Rb.tolist()},
       "opencv": {"rvec": r.tolist(), "tvec": t.tolist()}, "solve": "silhouette chamfer + IoU (tools/silsolve.py)", "cost": float(res.fun)}
json.dump(out, open(a.out, 'w'), indent=2)
vis = cv2.cvtColor(pm, cv2.COLOR_GRAY2BGR) // 3; vis[pe] = (0, 160, 255); vis[edge(sil(r, t, f))] = (255, 255, 0)
cv2.imwrite(a.out.replace('.json', '.sil.jpg'), vis); print('focal_mm %.2f loc %s' % (out['focal_mm'], loc.round(3)))
