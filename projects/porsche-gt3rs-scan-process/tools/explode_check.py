"""Check an exploded-view layout without Blender: project the car and each moved part with a shot camera and report
(a) how much of each part lands on top of the car silhouette (hard to read - reviewer rule: parts must move into clear
background) and (b) whether it stays inside the frame. Writes a silhouette board (car grey, parts coloured).

  python explode_check.py cam.json out.png "part:dx,dy,dz" ...   [--car car.stl] [--pull amt,lookx,looky,lookz]
"""
import argparse, json, sys
import numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('cam'); ap.add_argument('out'); ap.add_argument('parts', nargs='+')
ap.add_argument('--car', default='/home/user/media/gt3rs/scan/car_carved_noFW.stl'); ap.add_argument('--pull', default='')
ap.add_argument('--orbit', default='', help='deg,px,py,pz')
a = ap.parse_args()
like = json.load(open('/home/user/media/work/gt3rs/car.json')); off = np.array(like['root_location'])
dt = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
def load(f, step):
    with open(f, 'rb') as fh:
        fh.read(80); n = np.frombuffer(fh.read(4), '<u4')[0]; d = np.fromfile(fh, dt, count=n)
    return d['v'].reshape(-1, 3)[::step].astype(float) * 0.001 + off
c = json.load(open(a.cam)); R = np.array(c['blender']['rotation_matrix']); L = np.array(c['blender']['location'])
if a.pull:
    amt, *lk = (float(v) for v in a.pull.split(',')); fwd = -R[:, 2]; L = L - fwd * np.linalg.norm(np.array(lk) - L) * amt
if a.orbit:
    deg, *pv = (float(v) for v in a.orbit.split(',')); t = np.radians(deg); Rz = np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
    pv = np.array(pv); L = pv + Rz @ (L - pv); R = Rz @ R
W, H = c['image_size']; fx = c['fx_px']; cx = W / 2 - c.get('shift_x', 0) * W; cy = H / 2 + c.get('shift_y', 0) * W
def proj(P):
    pc = (P - L) @ R; z = -pc[:, 2]; ok = z > 0.05
    return np.stack([cx + fx * pc[ok, 0] / z[ok], cy - fx * pc[ok, 1] / z[ok]], 1)
def mask(P, k=5):
    m = np.zeros((H, W), np.uint8); uv = proj(P).astype(int); s = (uv[:, 0] >= 0) & (uv[:, 0] < W) & (uv[:, 1] >= 0) & (uv[:, 1] < H)
    m[uv[s, 1], uv[s, 0]] = 1; return cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8)), (~s).mean() if len(s) else 1
car, _ = mask(load(a.car, 5), 7)
board = cv2.cvtColor(car * 90, cv2.COLOR_GRAY2BGR)
cols = [(0, 140, 255), (255, 200, 0), (0, 255, 0), (255, 0, 255), (0, 0, 255), (255, 255, 0), (128, 255, 128)]
for i, spec in enumerate(a.parts):
    name, o = spec.split(':'); o = np.array([float(v) for v in o.split(',')])
    P = load(f'/home/user/media/gt3rs/scan/parts2mm/{name}.stl', 3) + o
    m, outside = mask(P)
    area = m.sum(); over = (m & car).sum() / max(area, 1)
    uv = proj(P); x0, y0 = uv.min(0); x1, y1 = uv.max(0)
    print(f'{name:26s} on-car {over*100:5.1f}%  out-of-frame {outside*100:5.1f}%  bbox x {x0:.0f}..{x1:.0f} y {y0:.0f}..{y1:.0f}')
    board[m > 0] = cols[i % len(cols)]
cv2.rectangle(board, (0, int(H * 0.8)), (W - 1, H - 1), (60, 60, 60), 2)
cv2.imwrite(a.out, cv2.resize(board, (W // 3, H // 3)))
