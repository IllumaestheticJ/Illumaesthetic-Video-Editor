"""Turn a full-frame camera solve into a 9:16 crop camera for 1080x1920 renders.
Optionally absorb a 2D similarity (scale s about the principal point + translation) fitted on
landmarks inside the crop window, as focal scale + Blender lens shift (lens distortion / drift).
usage: cropcam.py cam.json points.json out.json --x0 1312 [--fit name,name,...] [--k1 0]"""
import json, argparse, numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('cam'); ap.add_argument('points'); ap.add_argument('out')
ap.add_argument('--x0', type=float, required=True); ap.add_argument('--fit', default='')
ap.add_argument('--out-size', default='1080x1920')
ap.add_argument('--sim', default='', help='manual s,tx,ty (full-res px) instead of --fit')
a = ap.parse_args()
c = json.load(open(a.cam)); d = json.load(open(a.points))
W0, H0 = c['image_size']; f = c['fx_px']; cx, cy = W0 / 2, H0 / 2
K = np.array([[f, 0, cx], [0, f, cy], [0, 0, 1]])
pts = d['points']; O = np.array([p['xyz'] for p in pts]); I = np.array([p['px'] for p in pts], float)
q, _ = cv2.projectPoints(O, np.array(c['opencv']['rvec']), np.array(c['opencv']['tvec']), K, None); q = q.reshape(-1, 2)
s, tx, ty = 1.0, 0.0, 0.0
names = [n for n in a.fit.split(',') if n]
if a.sim: s, tx, ty = [float(v) for v in a.sim.split(',')]
if names:
    idx = [i for i, p in enumerate(pts) if p['name'] in names]
    A = []; b = []
    for i in idx:
        A.append([q[i, 0] - cx, 1, 0]); b.append(I[i, 0] - cx)
        A.append([q[i, 1] - cy, 0, 1]); b.append(I[i, 1] - cy)
    s, tx, ty = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)[0]
    qq = np.c_[cx + s * (q[:, 0] - cx) + tx, cy + s * (q[:, 1] - cy) + ty]
    for i, p in enumerate(pts):
        print(f"{p['name']:10s} before {np.linalg.norm(q[i]-I[i]):6.1f}  after {np.linalg.norm(qq[i]-I[i]):6.1f}" + ("  *" if i in idx else ""))
OW, OH = [int(v) for v in a.out_size.split('x')]; cw = H0 * OW / OH; k = OH / H0
fn = f * s * k
offU = k * (cx + tx - a.x0) - OW / 2; offV = k * (cy + ty) - OH / 2
md = OW  # Blender shift is in units of the sensor-fit dimension (HORIZONTAL -> width)
out = dict(c); out.update({"image_size": [OW, OH], "fx_px": fn, "focal_mm": fn * c['sensor_width_mm'] / OW,
    "shift_x": -offU / OW, "shift_y": offV / OW,
    "crop": {"src_size": [W0, H0], "x0": a.x0, "width": cw, "similarity": [float(s), float(tx), float(ty)]}})
json.dump(out, open(a.out, 'w'), indent=2)
print("s %.4f tx %.1f ty %.1f -> focal %.2f mm shift %.4f %.4f" % (s, tx, ty, out['focal_mm'], out['shift_x'], out['shift_y']))
