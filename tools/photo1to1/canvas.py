"""canvas.py CAR ANGLE : zoom-out plan. Start = tight 9:16 window on the Epsilon parts visible in this photo,
end = whole car + 10 %. Writes match/cam_<A>_canvas.json (same focal, wider symmetric sensor) + match/plan_<A>.json."""
import sys, json, numpy as np, cv2
car, A = sys.argv[1], sys.argv[2]; D = f'/home/user/media/cars/{car}'
cam = json.load(open(f'{D}/match/cam_{A}.json')); W, H = cam['image_size']
K = np.array([[cam['fx_px'], 0, W / 2], [0, cam['fx_px'], H / 2], [0, 0, 1]]); r = np.array(cam['opencv']['rvec']); t = np.array(cam['opencv']['tvec'])
def proj(P): p, _ = cv2.projectPoints(np.ascontiguousarray(P, dtype=np.float64), r, t, K, None); return p.reshape(-1, 2)
V = np.load(f'{D}/scan/glb.npz')['v'][::5]; p = proj(V); x0, y0 = np.percentile(p, 0.5, 0); x1, y1 = np.percentile(p, 99.5, 0)
w1 = (x1 - x0) * 1.10; h1 = max(w1 * 16 / 9, (y1 - y0) * 1.15); c1 = [(x0 + x1) / 2, (y0 + y1) / 2 - 0.03 * h1, h1]
f = open(f'{D}/scan/parts_mm.stl', 'rb'); f.seek(80); n = np.frombuffer(f.read(4), np.uint32)[0]
P = np.fromfile(f, np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]), count=n)['v'].reshape(-1, 3)[::9] / 1000
pp = proj(P); inside = (pp[:, 0] > 0) & (pp[:, 0] < W) & (pp[:, 1] > 0) & (pp[:, 1] < H) & (pp[:, 0] > x0) & (pp[:, 0] < x1)
# focus = the nearest (largest on screen) parts: weight by inverse depth
Rm = cv2.Rodrigues(r)[0]; z = (P @ Rm.T + t)[:, 2]
if inside.sum() > 50:
    wgt = (1 / z[inside]) ** 4; fc = (pp[inside] * wgt[:, None]).sum(0) / wgt.sum()
else: fc = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
h0 = min(H * 0.98, h1 / 2.1); h0 = max(h0, (y1 - y0) * 0.7)
c0 = [float(np.clip(fc[0], x0 + h0 * 9 / 32, x1 - h0 * 9 / 32)), float(np.clip(fc[1], h0 / 2, H - h0 / 2)), float(h0)]
wins = [c0, c1]; rs = min(1.0, 2600 / W)
hx = max(W / 2, max(max(abs(c[0] - c[2] * 9 / 32 - W / 2), abs(c[0] + c[2] * 9 / 32 - W / 2)) for c in wins))
hy = max(H / 2, max(max(abs(c[1] - c[2] / 2 - H / 2), abs(c[1] + c[2] / 2 - H / 2)) for c in wins))
Wc, Hc = int(np.ceil(2 * hx)) + 2, int(np.ceil(2 * hy)) + 2
cc = dict(cam); cc['image_size'] = [round(Wc * rs), round(Hc * rs)]; cc['fx_px'] = cam['fx_px'] * rs; cc['sensor_width_mm'] = cam['sensor_width_mm'] * Wc / W
json.dump(cc, open(f'{D}/match/cam_{A}_canvas.json', 'w'), indent=1)
json.dump({'photo': f'{D}/match/{A}.jpg', 'photo_size': [W, H], 'canvas_photo_px': [Wc, Hc], 'origin_photo_px': [W / 2 - Wc / 2, H / 2 - Hc / 2],
           'render_scale': rs, 'win_start': c0, 'win_end': c1}, open(f'{D}/match/plan_{A}.json', 'w'), indent=1)
print(car, A, 'canvas', cc['image_size'], 'zoom %.2f' % (h1 / h0))
