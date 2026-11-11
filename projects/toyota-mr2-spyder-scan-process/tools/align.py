"""Rigidly align MR2 Artec STLs (all states share one frame) so the car's long axis is +Y,
level on its tyres, centred. One transform (align.json) is applied to every state scan, so they
keep lining up. Usage: align.py fit <ref.stl> align.json | align.py apply align.json in.stl out.stl"""
import json, sys, struct
import numpy as np
TRI = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])

def load(p): return np.fromfile(p, dtype=TRI, offset=84)

def save(p, m):
    with open(p, 'wb') as f:
        f.write(b'mr2 aligned'.ljust(80)); f.write(struct.pack('<I', len(m))); m.tofile(f)

def fit(ref, out):
    m = load(ref); c = m['v'].mean(1).astype(np.float64)
    xy = c[:, :2] - c[:, :2].mean(0)
    w, V = np.linalg.eigh(np.cov(xy.T)); ax = V[:, np.argmax(w)]       # long axis
    ang = np.arctan2(ax[0], ax[1])                                      # rotate ax onto +Y
    R = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    p = c @ R.T
    # level: fit plane through the lowest points in 4 tyre quadrants
    yc, xc = np.median(p[:, 1]), np.median(p[:, 0]); pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            q = p[(np.sign(p[:, 0] - xc) == sx) & (np.sign(p[:, 1] - yc) == sy)]
            lo = q[q[:, 2] < np.percentile(q[:, 2], 0.3)]; pts.append(lo.mean(0))
    pts = np.array(pts); A = np.c_[pts[:, 0], pts[:, 1], np.ones(4)]
    a, b, _ = np.linalg.lstsq(A, pts[:, 2], rcond=None)[0]
    n = np.array([-a, -b, 1.0]); n /= np.linalg.norm(n)
    k = np.cross(n, [0, 0, 1.0]); s = np.linalg.norm(k); cth = n[2]
    if s > 1e-9:
        k /= s; K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
        L = np.eye(3) + s * K + (1 - cth) * K @ K
    else: L = np.eye(3)
    M = L @ R; p = c @ M.T
    t = -np.array([(np.percentile(p[:, 0], .5) + np.percentile(p[:, 0], 99.5)) / 2,
                   (np.percentile(p[:, 1], .5) + np.percentile(p[:, 1], 99.5)) / 2,
                   np.percentile(p[:, 2], 0.05)])
    json.dump({'M': M.tolist(), 't': t.tolist(), 'ref': ref, 'level_tilt_deg': float(np.degrees(np.arccos(cth)))}, open(out, 'w'), indent=1)
    q = p + t; print('extent mm', (np.percentile(q, 99.5, 0) - np.percentile(q, .5, 0)).round(0), 'tilt', np.degrees(np.arccos(cth)))

def apply(js, inp, out):
    T = json.load(open(js)); M = np.array(T['M']); t = np.array(T['t'])
    m = load(inp); v = m['v'].astype(np.float64) @ M.T + t
    m['v'] = v.astype('<f4'); m['n'] = (m['n'].astype(np.float64) @ M.T).astype('<f4'); save(out, m)

if __name__ == '__main__':
    if sys.argv[1] == 'fit': fit(sys.argv[2], sys.argv[3])
    else: apply(*sys.argv[2:5])
