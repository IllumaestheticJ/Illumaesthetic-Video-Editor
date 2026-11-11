"""solve_angle.py PHOTO.jpg MASK.png glb.npz out_cam.json
Camera for a finished photo in the lookbook-model frame (m, Z up, front -Y): coarse orbit search (IoU of the model
silhouette vs the rembg car mask), then Powell/Nelder-Mead on a truncated symmetric chamfer of the two outlines."""
import sys, json, itertools, numpy as np, cv2
from scipy.optimize import minimize
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.camera import lookat
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
photo, maskp, meshp, out = sys.argv[1:5]
W0, H0 = cv2.imread(photo).shape[1::-1]
mesh = np.load(meshp); V, F = mesh['v'], mesh['f']
def cluster(V, F, cell):   # vertex-cluster decimation for fast silhouettes
    k = np.floor(V / cell).astype(np.int64); _, inv = np.unique(k, axis=0, return_inverse=True); inv = inv.ravel()
    cnt = np.bincount(inv); Vc = np.zeros((cnt.size, 3)); np.add.at(Vc, inv, V); Vc /= cnt[:, None]
    Fc = inv[F]; ok = (Fc[:, 0] != Fc[:, 1]) & (Fc[:, 1] != Fc[:, 2]) & (Fc[:, 0] != Fc[:, 2]); Fc = np.unique(np.sort(Fc[ok], 1), axis=0)
    return Vc, Fc
Vc, Fcc = cluster(V, F, 0.06); Vr, Frr = cluster(V, F, 0.03); Vc = np.ascontiguousarray(Vc); Vr = np.ascontiguousarray(Vr); print('silhouette meshes', len(Fcc), len(Frr))
m0 = cv2.imread(maskp, 0)
def prep(w):
    h = round(H0 * w / W0); m = (cv2.resize(m0, (w, h), interpolation=cv2.INTER_AREA) > 127).astype(np.uint8); return w, h, m
def sil(V, F, r, t, f, w, h):
    K = np.array([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]])
    p, _ = cv2.projectPoints(V, r, t, K, None); p = p.reshape(-1, 2)
    if not np.isfinite(p).all() or (np.c_[V, np.ones(len(V))] @ np.c_[cv2.Rodrigues(r)[0], t.reshape(3, 1)].T)[:, 2].min() < 0.3: return None
    p = np.round(p * 4).astype(np.int32); mk = np.zeros((h, w), np.uint8); cv2.fillPoly(mk, list(p[F]), 1, shift=2)
    mk = cv2.morphologyEx(mk, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(mk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); o = np.zeros_like(mk); cv2.drawContours(o, cs, -1, 1, -1); return o
def cam_rt(c): return np.array(c['opencv']['rvec'], float), np.array(c['opencv']['tvec'], float)
# ---- coarse: for each heading/height/lens, fit distance + aim to the mask bbox, score IoU
w, h, M = prep(200); best = []
ys_, xs_ = np.nonzero(M); mb = np.array([xs_.min(), ys_.min(), xs_.max(), ys_.max()], float); mc = (mb[:2] + mb[2:]) / 2
lo, hi = V.min(0), V.max(0); ctr = (lo + hi) / 2; ctr[2] = (lo[2] + hi[2]) * 0.45
def proj_bbox(V, r, t, f):
    K = np.array([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]]); p, _ = cv2.projectPoints(V, r, t, K, None); p = p.reshape(-1, 2)
    return np.r_[p.min(0), p.max(0)]
Vb = np.ascontiguousarray(Vc[::3], dtype=np.float64)
for az in range(0, 360, 5):
    for el in [2, 6, 11, 18, 28]:
        for foc in [18, 24, 32, 45, 65, 95]:
            a_, e_ = np.radians(az), np.radians(el); dirv = np.array([np.sin(a_) * np.cos(e_), -np.cos(a_) * np.cos(e_), np.sin(e_)])
            d = 6.0; tgt = ctr.copy(); ok = True
            for _ in range(4):
                c = lookat((tgt + d * dirv).tolist(), tgt.tolist(), foc, 36.0, (W0, H0)); r, t = cam_rt(c); f = c['fx_px'] * w / W0
                R_ = cv2.Rodrigues(r)[0]
                if ((Vb @ R_.T + t)[:, 2] < 0.3).any(): ok = False; break
                pb = proj_bbox(Vb, r, t, f); pw = pb[2] - pb[0]; ph = pb[3] - pb[1]
                k = 0.5 * (pw / (mb[2] - mb[0]) + ph / (mb[3] - mb[1])); d = float(np.clip(d * k, 1.5, 40))
                c = lookat((tgt + d * dirv).tolist(), tgt.tolist(), foc, 36.0, (W0, H0)); r, t = cam_rt(c); R_ = cv2.Rodrigues(r)[0]
                if ((Vb @ R_.T + t)[:, 2] < 0.3).any(): ok = False; break
                pb = proj_bbox(Vb, r, t, f); off = mc - (pb[:2] + pb[2:]) / 2
                right = R_[0]; up = -R_[1]; tgt = tgt - (off[0] * right - off[1] * up) * d / f; tgt[2] = np.clip(tgt[2], -0.5, 2.0)
            if not ok or (tgt + d * dirv)[2] < 0.15: continue
            c = lookat((tgt + d * dirv).tolist(), tgt.tolist(), foc, 36.0, (W0, H0)); r, t = cam_rt(c)
            mk = sil(Vc, Fcc, r, t, c['fx_px'] * w / W0, w, h)
            if mk is None: continue
            iou = (mk & M).sum() / max(1, (mk | M).sum()); best.append((iou, az, el, round(d, 2), foc, 0, c))
best.sort(key=lambda x: -x[0]); print('coarse top', [(round(float(b[0]), 3), b[1], b[2], b[3], b[4]) for b in best[:5]])
import os
if os.environ.get('COARSE_ONLY'):
    c = best[0][6]; r, t = cam_rt(c); mk = sil(Vc, Fcc, r, t, c['fx_px'] * w / W0, w, h); img = cv2.resize(cv2.imread(photo), (w, h))
    img[mk > 0] = (img[mk > 0] * 0.4 + np.array([255, 200, 0]) * 0.6).astype(np.uint8); cv2.imwrite(out.replace('.json', '_coarse.jpg'), img); sys.exit()
# ---- refine top-3 starts on outline chamfer, keep best
w, h, M = prep(480); T = 12.0
edge = lambda mk: cv2.morphologyEx(mk, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
pe = edge(M); dt_p = cv2.distanceTransform((~pe).astype(np.uint8), cv2.DIST_L2, 3); pys, pxs = np.nonzero(pe)
def run(c0):
    r0, t0 = cam_rt(c0); f0 = c0['fx_px'] * w / W0
    unpack = lambda x: (r0 + x[:3] * 0.01, t0 + x[3:6] * 0.03, f0 * np.exp(x[6] * 0.03))
    def cost(x):
        r, t, f = unpack(x); mk = sil(Vr, Frr, r, t, f, w, h)
        if mk is None: return 1e3
        re = edge(mk); ys, xs = np.nonzero(re)
        if len(xs) < 50: return 1e3
        d1 = np.minimum(dt_p[ys, xs], T).mean(); d2 = np.minimum(cv2.distanceTransform((~re).astype(np.uint8), cv2.DIST_L2, 3)[pys, pxs], T).mean()
        return d1 + d2
    x = minimize(cost, np.zeros(7), method='Powell', options={'maxiter': 1500, 'xtol': 2e-3, 'ftol': 2e-4}).x
    res = minimize(cost, x, method='Nelder-Mead', options={'maxiter': 500, 'xatol': 2e-3, 'fatol': 2e-4})
    return res.fun, unpack(res.x)
seen = []; results = []
for b in best:
    key = (b[1] // 30,)
    if key in seen: continue
    seen.append(key); results.append(run(b[6]))
    if len(results) == 1: break
fun, (r, t, f) = min(results, key=lambda x: x[0])
fx = f * W0 / w; R, _ = cv2.Rodrigues(r); loc = (-R.T @ t).ravel(); Rb = R.T @ CV_TO_BLENDER_CAM
cam = {'image_size': [W0, H0], 'fx_px': fx, 'focal_mm': fx / W0 * 36.0, 'sensor_width_mm': 36.0, 'shift_x': 0.0, 'shift_y': 0.0,
       'blender': {'location': loc.tolist(), 'rotation_euler': _matrix_to_euler_xyz(Rb), 'rotation_matrix': Rb.tolist()},
       'opencv': {'rvec': r.tolist(), 'tvec': t.tolist()}, 'chamfer_px_at_480w': float(fun), 'method': 'rembg mask + model silhouette (coarse orbit IoU, chamfer refine)'}
json.dump(cam, open(out, 'w'), indent=2)
img = cv2.resize(cv2.imread(photo), (w, h)); mk = sil(Vr, Frr, r, t, f, w, h); vis = (img * 0.55).astype(np.uint8)
vis[mk > 0] = (vis[mk > 0] * 0.5 + np.array([255, 200, 0]) * 0.35).astype(np.uint8); vis[pe] = (0, 160, 255); vis[edge(mk)] = (255, 255, 0)
cv2.imwrite(out.replace('.json', '_check.jpg'), vis)
print('SOLVED', out, 'chamfer %.2f px @480, focal %.1f mm-equiv, cam at' % (fun, cam['focal_mm']), np.round(loc, 2))
