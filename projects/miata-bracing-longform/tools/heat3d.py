"""Animated 3D deviation heat maps from the actual scans (numpy point renderer, no Blender).
  heat3d.py prep <scans_dir> <out_dir>                         -> <state>.npz (points, normals, signed deviation, mm) in the car frame
  heat3d.py frame <out_dir> <left> <right> <yaw> <pitch> out.png   (left/right: control | jacked | fender | strut | both)
  heat3d.py shot  <out_dir> <left> <right> <kind: sides|top> <seconds> out.mp4
Scans are used as exported (they share the reports' alignment). Colours follow the reports: green/yellow/red = outward,
light/dark blue = inward, one +-15 mm scale for every state. Wheels, floor and anything > 25 mm off are shown grey."""
import sys, os, math, subprocess, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
SC = 15.0; BGC = (24, 24, 26); FPS = 24000/1001
def load(p):
    from ive.mesh import TRI
    t = np.fromfile(p, dtype=TRI, offset=84); v = t['v'].astype(np.float64); c = v.mean(1)
    n = np.cross(v[:, 1]-v[:, 0], v[:, 2]-v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12; return c, n
def prep(sd, od):
    C, CN = load(f'{sd}/ext_control.stl'); h, e = np.histogram(C[:, 2], bins=400); zf = e[np.argmax(h[:120])]
    b = C[C[:, 2] > zf + 500]; c0 = b[:, :2].mean(0); w, V = np.linalg.eigh(np.cov((b[:, :2]-c0).T)); ax, lat = V[:, 1], V[:, 0]
    if ((b[b[:, 2] > np.quantile(b[:, 2], .97)][:, :2] - c0) @ ax).mean() < 0: ax = -ax          # +u = rear (the roof sits rear of centre)
    lat = np.array([-ax[1], ax[0]])
    def car(P): return np.stack([-(P[:, :2]-c0) @ ax, (P[:, :2]-c0) @ lat, P[:, 2] - zf], 1)        # x forward, y left, z up from the floor
    def carn(N): return np.stack([-(N[:, :2] @ ax), N[:, :2] @ lat, N[:, 2]], 1)
    P = car(C); keep = (P[:, 2] > 75) & (np.abs(P[:, 1]) < 1000) & (np.abs(P[:, 0]) < 2150); P, N, C2 = P[keep], carn(CN[keep]), C[keep]
    out = N @ np.array([0, 0, 1.]) ; cen = P.mean(0); flip = np.einsum('ij,ij->i', N, P - np.array([0, 0, 600.])) < 0; N[flip] *= -1          # normals point outward
    np.savez_compressed(f'{od}/control.npz', P=P.astype(np.float32), N=N.astype(np.float32), D=np.zeros(len(P), np.float32), ok=np.ones(len(P), bool))
    for k in ('jacked', 'fender', 'strut', 'both'):
        S, _ = load(f'{sd}/ext_{k}.stl'); d, j = cKDTree(S).query(C2, workers=-1); sd_ = np.einsum('ij,ij->i', S[j] - C2, CN[keep]*np.where(flip, -1, 1)[:, None])
        ok = (d < 25) & (np.abs(sd_) < 25); np.savez_compressed(f'{od}/{k}.npz', P=P.astype(np.float32), N=N.astype(np.float32), D=sd_.astype(np.float32), ok=ok)
        print(k, 'covered %.0f%%' % (100*ok.mean()))
def cmap(v):
    x = np.clip(v/SC, -1, 1); st = np.array([[-1, 0, 0, 255], [-.6, 0, 0, 255], [-.35, 0, 140, 255], [-.001, 0, 255, 255], [.001, 0, 255, 0], [.35, 255, 255, 0], [.65, 255, 150, 0], [1, 255, 0, 0]], float)
    return np.stack([np.interp(x, st[:, 0], st[:, i]) for i in (1, 2, 3)], 1)
_cache = {}
def state(od, k):
    if k not in _cache:
        z = np.load(f'{od}/{k}.npz'); P, N, D, ok = z['P'], z['N'], z['D'], z['ok']
        wheel = ((np.abs(P[:, 0]) - 1130)**2 + (P[:, 2] - 300)**2 < 340**2) & (np.abs(P[:, 1]) > 470)           # wheels hang differently on the jack: not body flex
        col = np.full((len(P), 3), 150.) if k == 'control' else np.where((ok & ~wheel)[:, None], cmap(D), 118.)
        if k == 'control': col[:] = (176, 180, 186)
        _cache[k] = (P - np.array([0, 0, 620.], np.float32), N, col.astype(np.float32))
    return _cache[k]
def render(od, k, yaw, pitch, w, h, scale, splat=3):
    P, N, col = state(od, k); cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    R = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]], np.float32); Rp = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]], np.float32)
    M = Rp @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]], np.float32) @ R                        # world -> camera (x right, y up, z toward the viewer)
    Q = P @ M.T; n = N @ M.T; lit = np.clip(n @ np.array([-.35, .55, .76], np.float32), 0, 1); shade = (.42 + .62*lit)[:, None]
    vis = n[:, 2] > -0.15; Q, c = Q[vis], (col*shade)[vis]
    px = (w/2 + Q[:, 0]*scale).astype(np.int32); py = (h/2 - Q[:, 1]*scale).astype(np.int32); o = np.argsort(Q[:, 2]); px, py, c = px[o], py[o], np.clip(c[o], 0, 255).astype(np.uint8)
    im = np.empty((h, w, 3), np.uint8); im[:] = BGC; r = splat//2
    for dx in range(-r, splat - r):
        for dy in range(-r, splat - r):
            x, y = px + dx, py + dy; m = (x >= 0) & (x < w) & (y >= 0) & (y < h); im[y[m], x[m]] = c[m]
    return im
def pair(od, a, b, yaw, pitch):
    """1920x1080 split screen: left = a, right = b, same camera"""
    out = np.empty((1080, 1920, 3), np.uint8); out[:] = BGC
    out[150:1010, 20:950] = render(od, a, yaw, pitch, 930, 860, 0.205); out[150:1010, 970:1900] = render(od, b, yaw, pitch, 930, 860, 0.205); return out
def cam(kind, u):
    e = u*u*(3 - 2*u)
    if kind == 'sides': return math.radians(-25 + 230*e), math.radians(14)                    # right side -> around the rear -> left side
    return math.radians(-20 + 40*e), math.radians(38 + 44*e)                                    # 3/4 from above -> straight down
if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'prep': prep(a[2], a[3])
    elif a[1] == 'frame':
        from PIL import Image; Image.fromarray(pair(a[2], a[3], a[4], math.radians(float(a[5])), math.radians(float(a[6])))).save(a[7])
    elif a[1] == 'shot':
        od, l, r, kind, out = a[2], a[3], a[4], a[5], a[7]; n = int(a[6])                    # a[6] = frame count
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '24000/1001', '-i', '-', '-c:v', 'libx264', '-preset', 'fast', '-crf', '17',
                               '-pix_fmt', 'yuv420p', '-video_track_timescale', '24000', out], stdin=subprocess.PIPE)
        for i in range(n): ff.stdin.write(pair(od, l, r, *cam(kind, i/max(n-1, 1))).tobytes())
        ff.stdin.close(); ff.wait(); print(out, n)
