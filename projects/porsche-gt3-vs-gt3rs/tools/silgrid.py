"""Coarse global camera search for a listing/viewer frame: grid over azimuth/elevation/focal, with distance and target
fitted to the mask bbox, scored by silhouette IoU (vertex splat). Writes the best as an ive lookat cam json to seed
silsolve.py --no-global.   python silgrid.py mask.png mesh.npz out.json [--sensor 20.25]"""
import sys, json, itertools
import numpy as np, cv2
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.camera import lookat
mask, mesh, out = sys.argv[1:4]
M0 = cv2.imread(mask, 0); H0, W0 = M0.shape; s = 360 / W0
pm = cv2.resize(M0, (360, int(H0 * s)), interpolation=cv2.INTER_AREA) > 127; h, w = pm.shape
ys, xs = np.nonzero(pm); bb = np.array([xs.min(), ys.min(), xs.max(), ys.max()], float)
V = np.load(mesh)['v'][::4].astype(np.float64)
ker = np.ones((5, 5), np.uint8)
def proj(c):
    r, t = np.array(c['opencv']['rvec']), np.array(c['opencv']['tvec']); f = c['fx_px'] * s
    p, _ = cv2.projectPoints(V, r, t, np.array([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]]), None)
    return p.reshape(-1, 2)
def evalcam(az, el, fmm):
    d = 8.0; tgt = np.array([0, 0, 0.6]); a, e = np.radians(az), np.radians(el)
    dirv = np.array([np.cos(a) * np.cos(e), np.sin(a) * np.cos(e), np.sin(e)])
    for _ in range(4):
        c = lookat(tgt + dirv * d, tgt, fmm, 20.25, (W0, H0), 0); p = proj(c)
        b = np.array([p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max()])
        d *= (b[2] - b[0]) / (bb[2] - bb[0])
        # shift target in the image plane
        R = np.array(c['blender']['rotation_matrix']); px_m = c['fx_px'] * s / d
        dx = ((b[0] + b[2]) - (bb[0] + bb[2])) / 2 / px_m; dy = ((b[1] + b[3]) - (bb[1] + bb[3])) / 2 / px_m
        tgt = tgt + R[:, 0] * dx - R[:, 1] * dy
    c = lookat(tgt + dirv * d, tgt, fmm, 20.25, (W0, H0), 0); p = np.round(proj(c)).astype(int)
    ok = (p[:, 0] >= 0) & (p[:, 0] < w) & (p[:, 1] >= 0) & (p[:, 1] < h)
    mk = np.zeros((h, w), np.uint8); mk[p[ok, 1], p[ok, 0]] = 1
    mk = cv2.morphologyEx(mk, cv2.MORPH_CLOSE, ker) > 0
    return (mk & pm).sum() / max(1, (mk | pm).sum()), c, d
best = (0,)
for az, el, f in itertools.product(range(95, 176, 5), range(5, 56, 5), (22, 30, 40, 55, 80)):
    iou, c, d = evalcam(az, el, f)
    if iou > best[0]: best = (iou, c, az, el, f, d)
iou0, _, az0, el0, f0, _ = best
for az, el, f in itertools.product(np.arange(az0 - 4, az0 + 4.1, 1), np.arange(el0 - 4, el0 + 4.1, 1), (f0 * 0.85, f0, f0 * 1.18)):
    iou, c, d = evalcam(az, el, f)
    if iou > best[0]: best = (iou, c, az, el, f, d)
iou0, _, az0, el0, f0, _ = best
for az, el, f in itertools.product(np.arange(az0 - 1.5, az0 + 1.6, 0.5), np.arange(el0 - 1.5, el0 + 1.6, 0.5), (f0 * 0.88, f0 * 0.94, f0, f0 * 1.06, f0 * 1.12)):
    iou, c, d = evalcam(az, el, f)
    if iou > best[0]: best = (iou, c, az, el, f, d)
best[1]['lookat'] = {'az': float(best[2]), 'el': float(best[3]), 'focal': float(best[4]), 'dist': float(best[5])}
print('best iou %.3f az %.1f el %.1f f %.1f dist %.2f' % (best[0], best[2], best[3], best[4], best[5]), np.round(best[1]['blender']['location'], 2))
json.dump(best[1], open(out, 'w'))
