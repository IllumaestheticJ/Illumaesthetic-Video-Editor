"""Silhouette refinement of a camera solve: scan silhouette vs GrabCut mask of the real car.
usage: refine.py photo cam_in.json mesh.npz cam_out.json [--points points.json --wpts 0.3] [--fix-f]
Cost = truncated symmetric chamfer between silhouette contours (+ optional landmark reprojection)."""
import sys, json, argparse, numpy as np, cv2
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
from scipy.optimize import minimize
ap = argparse.ArgumentParser()
ap.add_argument('photo'); ap.add_argument('cam'); ap.add_argument('mesh'); ap.add_argument('out')
ap.add_argument('--points'); ap.add_argument('--wpts', type=float, default=0.3)
ap.add_argument('--fix-f', action='store_true'); ap.add_argument('--work', type=int, default=1000)
ap.add_argument('--T', type=float, default=12)
ap.add_argument('--bg-thresh', type=float, default=0, help='flat-background photo: mask = colour distance from the border median > this (instead of GrabCut)')
ap.add_argument('--ignore', default='', help='x0,y0,x1,y1;... boxes (full-res px) excluded from photo contour (wing, lip)')
a = ap.parse_args()
img = cv2.imread(a.photo); H0, W0 = img.shape[:2]; s = a.work / W0
small = cv2.resize(img, (a.work, int(H0 * s)), interpolation=cv2.INTER_AREA); h, w = small.shape[:2]
cam = json.load(open(a.cam)); m = np.load(a.mesh); V, F = m['v'], m['f']
r0 = np.array(cam['opencv']['rvec'], float); t0 = np.array(cam['opencv']['tvec'], float); f0 = cam['fx_px'] * s
def sil(r, t, f):
    K = np.array([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]])
    p, _ = cv2.projectPoints(V, r, t, K, None); p = np.round(p.reshape(-1, 2) * 4).astype(np.int32)
    msk = np.zeros((h, w), np.uint8); cv2.fillPoly(msk, list(p[F]), 255, shift=2)
    msk = cv2.morphologyEx(msk, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cs, _ = cv2.findContours(msk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(msk); cv2.drawContours(out, cs, -1, 255, -1); return out
# photo mask by GrabCut seeded with the initial projection
m0 = sil(r0, t0, f0)
gc = np.full((h, w), cv2.GC_BGD, np.uint8)
gc[cv2.dilate(m0, np.ones((61, 61))) > 0] = cv2.GC_PR_BGD
gc[cv2.dilate(m0, np.ones((15, 15))) > 0] = cv2.GC_PR_FGD
gc[cv2.erode(m0, np.ones((31, 31))) > 0] = cv2.GC_FGD
bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
if a.bg_thresh > 0:
    border = np.concatenate([small[:5].reshape(-1, 3), small[-5:].reshape(-1, 3), small[:, :5].reshape(-1, 3), small[:, -5:].reshape(-1, 3)])
    bgc = np.median(border, 0); dist = np.linalg.norm(small.astype(float) - bgc, axis=2)
    pm = np.where(dist > a.bg_thresh, 255, 0).astype(np.uint8); pm = cv2.morphologyEx(pm, cv2.MORPH_OPEN, np.ones((5, 5)))
    for box in filter(None, a.ignore.split(';')):
        x0, y0, x1, y1 = [int(float(v) * s) for v in box.split(',')]; pm[y0:y1, x0:x1] = 0
else:
    cv2.grabCut(small, gc, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
    pm = np.where((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(pm)
if n > 1: pm = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
pm = cv2.morphologyEx(pm, cv2.MORPH_CLOSE, np.ones((9, 9)))
edge = lambda mk: cv2.morphologyEx(mk, cv2.MORPH_GRADIENT, np.ones((3, 3))) > 0
pe = edge(pm)
keep = np.ones((h, w), bool)
for box in filter(None, a.ignore.split(';')):
    x0, y0, x1, y1 = [int(float(v) * s) for v in box.split(',')]; keep[y0:y1, x0:x1] = False
pe &= keep
dt_p = cv2.distanceTransform((~pe).astype(np.uint8), cv2.DIST_L2, 3)
pys, pxs = np.nonzero(pe)
pts = json.load(open(a.points))['points'] if a.points else []
O = np.array([p['xyz'] for p in pts], float); I = np.array([p['px'] for p in pts], float) * s
def unpack(x):
    return r0 + x[:3] * 0.01, t0 + x[3:6] * 0.02, f0 * np.exp(0 if a.fix_f else x[6] * 0.02)
def cost(x, verbose=False):
    r, t, f = unpack(x); mk = sil(r, t, f); re = edge(mk) & keep
    ys, xs = np.nonzero(re)
    if len(xs) < 50: return 1e3
    d1 = np.minimum(dt_p[ys, xs], a.T).mean()
    dt_r = cv2.distanceTransform((~(edge(mk))).astype(np.uint8), cv2.DIST_L2, 3)
    d2 = np.minimum(dt_r[pys, pxs], a.T).mean()
    c = d1 + d2
    if len(pts):
        K = np.array([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1]])
        q, _ = cv2.projectPoints(O, r, t, K, None); e = np.linalg.norm(q.reshape(-1, 2) - I, axis=1)
        c += a.wpts * np.sqrt((e ** 2).mean())
    if verbose: print(f"chamfer r->p {d1:.2f} p->r {d2:.2f} total {c:.2f} (px @ {w})")
    return c
x0 = np.zeros(7)
print("before:"); cost(x0, True)
res = minimize(cost, x0, method='Powell', options={'maxiter': 4000, 'xtol': 1e-3, 'ftol': 1e-4})
res = minimize(cost, res.x, method='Nelder-Mead', options={'maxiter': 1500, 'xatol': 1e-3, 'fatol': 1e-4})
print("after:"); cost(res.x, True)
r, t, f = unpack(res.x); fx = f / s
R, _ = cv2.Rodrigues(r); loc = (-R.T @ t).ravel(); Rb = R.T @ CV_TO_BLENDER_CAM
out = dict(cam); out.update({"fx_px": fx, "focal_mm": fx / W0 * cam['sensor_width_mm'], "image_size": [W0, H0],
    "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rb), "rotation_matrix": Rb.tolist()},
    "opencv": {"rvec": r.tolist(), "tvec": t.tolist()}, "refined": "silhouette chamfer (GrabCut) + landmarks",
    "chamfer_px_at_1000w": float(res.fun)})
json.dump(out, open(a.out, 'w'), indent=2)
# QA image: photo mask (orange edge) vs refined silhouette (cyan)
vis = small.copy(); vis[pe] = (0, 160, 255); vis[edge(sil(r, t, f))] = (255, 255, 0)
cv2.imwrite(a.out.replace('.json', '.refine.jpg'), vis); cv2.imwrite(a.out.replace('.json', '.mask.png'), pm)
print("focal_mm", out['focal_mm'], "loc", loc.round(3))
