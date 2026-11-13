"""Deviation heat map from two decimated state scans (feasibility test for scan-driven heat maps).
usage: heat.py control.stl state.stl out.png [--scale 15] [--T T.json]
ICP-aligns state -> control (whole body, trimmed), then signed distance control surface -> state along the control normal."""
import sys, json, itertools, numpy as np
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.mesh import TRI
a = sys.argv; SC = float(a[a.index('--scale')+1]) if '--scale' in a else 15.0
def load(p):
    t = np.fromfile(p, dtype=TRI, offset=84); v = t['v'].astype(np.float64); c = v.mean(1)
    n = np.cross(v[:, 1]-v[:, 0], v[:, 2]-v[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12; return c, n
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A-ca).T @ (B-cb)); d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T; return R, cb - R @ ca
def icp(M, F, R, t, iters, trim):
    tree = cKDTree(F)
    for _ in range(iters):
        X = M @ R.T + t; d, j = tree.query(X, workers=-1); k = d <= np.quantile(d, trim); R2, t2 = kabsch(X[k], F[j[k]]); R, t = R2 @ R, R2 @ t + t2
    d, _ = tree.query(M @ R.T + t, workers=-1); return R, t, float(np.median(d)), float(np.quantile(d, trim))
C, CN = load(a[1]); S, SN = load(a[2]); rng = np.random.default_rng(0)
def nofloor(P, N):   # floor = densest z slab; keep what is 35 mm above it and inside the car footprint
    h, e = np.histogram(P[:, 2], bins=400); zf = e[np.argmax(h[:120])]; k = (P[:, 2] > zf + 35) & (np.abs(P[:, 1] - np.median(P[:, 1])) < 1000); return P[k], N[k]
if '--asis' in a: C, CN = nofloor(C, CN); S, SN = nofloor(S, SN)
print('control', len(C), C.min(0).round(0), C.max(0).round(0)); print('state  ', len(S), S.min(0).round(0), S.max(0).round(0))
Ms = S[rng.choice(len(S), 120000, replace=False)]; Fs = C[rng.choice(len(C), 400000, replace=False)]
d0, _ = cKDTree(Fs).query(Ms, workers=-1); print('as-exported median distance %.2f mm' % np.median(d0))
if '--asis' in a: R, t = np.eye(3), np.zeros(3)
elif '--T' in a and __import__('os').path.exists(a[a.index('--T')+1]): T = json.load(open(a[a.index('--T')+1])); R, t = np.array(T['R']), np.array(T['t'])
else:
    R, t = np.eye(3), np.zeros(3)
    if np.median(d0) > 30:   # different frames: PCA candidates
        cm, cf = Ms.mean(0), Fs.mean(0); _, Vm = np.linalg.eigh(np.cov((Ms-cm).T)); _, Vf = np.linalg.eigh(np.cov((Fs-cf).T)); best = None
        for s in itertools.product([1, -1], repeat=3):
            R0 = Vf @ np.diag(s) @ Vm.T
            if np.linalg.det(R0) < 0: continue
            r = icp(Ms[::6], Fs, R0, cf - R0 @ cm, 25, .7)
            if best is None or r[3] < best[3]: best = r
        R, t = best[0], best[1]
    for it, tr in ((40, .7), (40, .8), (30, .9)): R, t, med, q = icp(Ms, Fs, R, t, it, tr); print('icp trim %.1f median %.2f mm' % (tr, med))
    if '--T' in a: json.dump({'R': R.tolist(), 't': t.tolist()}, open(a[a.index('--T')+1], 'w'))
S2 = S @ R.T + t; d, j = cKDTree(S2).query(C, workers=-1); sd = np.einsum('ij,ij->i', S2[j] - C, CN)
ok = d < 40; print('covered %.0f%%  |dev| median %.2f  p90 %.2f  p99 %.2f mm' % (100*ok.mean(), np.median(np.abs(sd[ok])), *np.quantile(np.abs(sd[ok]), [.9, .99])))
# car frame from PCA of the control: long axis = x, vertical = smallest extent
P, N = (C, CN) if '--asis' in a else ((C - C.mean(0)) @ np.linalg.eigh(np.cov((C[::20]-C.mean(0)).T))[1][:, ::-1], CN @ np.linalg.eigh(np.cov((C[::20]-C.mean(0)).T))[1][:, ::-1])   # x long, y width, z height
def cmap(v):
    x = np.clip(v / SC, -1, 1); stops = np.array([[-1, 0, 0, 255], [-.6, 0, 0, 255], [-.35, 0, 140, 255], [-.001, 0, 255, 255], [.001, 0, 255, 0], [.35, 255, 255, 0], [.65, 255, 150, 0], [1, 255, 0, 0]], float)
    return np.stack([np.interp(x, stops[:, 0], stops[:, i]) for i in (1, 2, 3)], 1)
def view(u, v, depth, keep, W=1500):
    u, v, depth, col = u[keep], v[keep], depth[keep], cmap(sd[keep]) * np.where(ok[keep], 1, .45)[:, None]
    s = (W-60) / (u.max()-u.min()); H = int((v.max()-v.min())*s) + 60; im = np.full((H, W, 3), 255, np.uint8)
    o = np.argsort(depth); px = ((u[o]-u.min())*s + 30).astype(int); py = (H - 30 - (v[o]-v.min())*s).astype(int)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1): im[np.clip(py+dy, 0, H-1), np.clip(px+dx, 0, W-1)] = col[o]
    return Image.fromarray(im)
x, y, z = P.T; vs = [view(x, z, -y, N[:, 1] < .2), view(-x, z, y, N[:, 1] > -.2), view(x, y, z, np.ones(len(x), bool))]
out = Image.new('RGB', (1500, sum(v.height for v in vs)), 'white'); yy = 0
for v in vs: out.paste(v, (0, yy)); yy += v.height
ImageDraw.Draw(out).text((20, 10), f'{a[2].split("/")[-1]} vs {a[1].split("/")[-1]}  scale +-{SC:g} mm', fill='black'); out.save(a[3]); print(a[3])
