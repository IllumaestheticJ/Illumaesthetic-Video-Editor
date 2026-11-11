"""Zoom-out plan for one angle: car extent in the photo (projected scan+lip), a window path from a tight start
to the whole car, and an extended canvas (symmetric about the principal point, so no lens shift) that the
scan/CGI are rendered on.  usage: canvas.py NAME photo cam.json mesh.npz 'cx,cy,h' margin render_scale"""
import sys, json, numpy as np, cv2
name, photo, camp, mesh = sys.argv[1:5]; c0 = [float(v) for v in sys.argv[5].split(',')]
margin = float(sys.argv[6]); rs = float(sys.argv[7])
W, H = cv2.imread(photo).shape[1::-1]; cam = json.load(open(camp)); m = np.load(mesh)
K = np.array([[cam['fx_px'], 0, W / 2], [0, cam['fx_px'], H / 2], [0, 0, 1]])
p, _ = cv2.projectPoints(m['v'], np.array(cam['opencv']['rvec']), np.array(cam['opencv']['tvec']), K, None); p = p.reshape(-1, 2)
x0, y0 = np.percentile(p, 0.5, axis=0); x1, y1 = np.percentile(p, 99.5, axis=0)
w1 = (x1 - x0) * (1 + margin); h1 = w1 * 16 / 9; c1 = [(x0 + x1) / 2, (y0 + y1) / 2 - 0.04 * h1, h1]
wins = [c0, c1]
hx = max(max(abs(c[0] - c[2] * 9 / 32 - W / 2), abs(c[0] + c[2] * 9 / 32 - W / 2)) for c in wins); hx = max(hx, W / 2)
hy = max(max(abs(c[1] - c[2] / 2 - H / 2), abs(c[1] + c[2] / 2 - H / 2)) for c in wins); hy = max(hy, H / 2)
Wc, Hc = int(np.ceil(2 * hx)) + 2, int(np.ceil(2 * hy)) + 2; ox, oy = W / 2 - Wc / 2, H / 2 - Hc / 2  # canvas origin in photo px
cc = dict(cam); cc['image_size'] = [round(Wc * rs), round(Hc * rs)]; cc['fx_px'] = cam['fx_px'] * rs
cc['sensor_width_mm'] = cam['sensor_width_mm'] * Wc / W  # same focal, wider sensor = same pixels per degree
plan = {'photo': photo, 'photo_size': [W, H], 'canvas_photo_px': [Wc, Hc], 'origin_photo_px': [ox, oy], 'render_scale': rs,
        'car_bbox_photo_px': [x0, y0, x1, y1], 'win_start': c0, 'win_end': c1}
json.dump(cc, open(f'/home/user/media/work/fg2/match/cam_{name}_canvas.json', 'w'), indent=1)
json.dump(plan, open(f'/home/user/media/work/fg2/match/plan_{name}.json', 'w'), indent=1)
print(name, 'canvas', cc['image_size'], 'car w', round(x1 - x0), 'end win h', round(h1), 'zoom', round(h1 / c0[2], 2))
