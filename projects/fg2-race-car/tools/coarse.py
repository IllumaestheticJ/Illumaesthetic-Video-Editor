import sys, json, numpy as np, cv2, itertools
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.camera import lookat, save
photo, mesh, out, rect = sys.argv[1], sys.argv[2], sys.argv[3], [int(v) for v in sys.argv[4].split(',')]
img = cv2.imread(photo); H0, W0 = img.shape[:2]; w = 240; s = w / W0; h = int(H0 * s)
small = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
m = np.load(mesh); V, F = m["v"], m["f"][::6]
gc = np.zeros((h, w), np.uint8); bg = np.zeros((1, 65)); fg = np.zeros((1, 65))
r = [int(v * s) for v in rect]; cv2.grabCut(small, gc, (r[0], r[1], r[2] - r[0], r[3] - r[1]), bg, fg, 6, cv2.GC_INIT_WITH_RECT)
pm = ((gc == 1) | (gc == 3)).astype(np.uint8)
cv2.imwrite(out + '.mask.png', pm * 255)
def sil(c):
    K = np.array([[c['fx_px'] * s, 0, w / 2], [0, c['fx_px'] * s, h / 2], [0, 0, 1]])
    p, _ = cv2.projectPoints(V, np.array(c['opencv']['rvec']), np.array(c['opencv']['tvec']), K, None)
    if not np.isfinite(p).all(): return None
    p = np.round(p.reshape(-1, 2) * 4).astype(np.int32); mk = np.zeros((h, w), np.uint8)
    cv2.fillPoly(mk, list(p[F]), 1, shift=2); return cv2.morphologyEx(mk, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
best = (-1, None)
tgt = [float(v) for v in sys.argv[5].split(',')]
for x, y, z, f, dt in itertools.product(*[np.linspace(*map(float, a.split(':')[:2]), int(a.split(':')[2])) for a in sys.argv[6:11]]):
    c = lookat([x, y, z], [tgt[0], tgt[1] + dt, tgt[2]], f, 36.0, (W0, H0))
    mk = sil(c)
    if mk is None: continue
    iou = (mk & pm).sum() / max(1, (mk | pm).sum())
    if iou > best[0]: best = (iou, c, (x, y, z, f, dt))
print('best IoU', best[0], best[2]); save(best[1], out)
