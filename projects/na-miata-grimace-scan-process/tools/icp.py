"""Rigid ICP between two STL scans in different Artec frames (PCA coarse + trimmed point-to-point ICP).
usage: icp.py moving.stl fixed.stl out_T.json"""
import sys, json, itertools, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.mesh import TRI
def load(p, n=80000, seed=0):
    v = np.fromfile(p, dtype=TRI, offset=84)['v'].mean(1).astype(np.float64)
    r = np.random.default_rng(seed); return v[r.choice(len(v), min(n, len(v)), replace=False)]
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); H = (A - ca).T @ (B - cb); U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T)); D = np.diag([1, 1, d]); R = Vt.T @ D @ U.T; return R, cb - R @ ca
def icp(M, F, R, t, iters=60, trim=0.7):
    tree = cKDTree(F)
    for i in range(iters):
        X = M @ R.T + t; d, j = tree.query(X)
        k = d <= np.quantile(d, trim); R2, t2 = kabsch(X[k], F[j[k]]); R, t = R2 @ R, R2 @ t + t2
    X = M @ R.T + t; d, _ = tree.query(X); return R, t, float(np.median(d)), float(np.quantile(d, trim))
M = load(sys.argv[1]); F = load(sys.argv[2], seed=1)
cm, cf = M.mean(0), F.mean(0)
_, Vm = np.linalg.eigh(np.cov((M - cm).T)); _, Vf = np.linalg.eigh(np.cov((F - cf).T))
best = None
cands = [np.eye(3)]
for s in itertools.product([1, -1], repeat=3):
    S = np.diag(s)
    if np.linalg.det(Vf @ S @ Vm.T) > 0: cands.append(Vf @ S @ Vm.T)
for R0 in cands:
    t0 = cf - R0 @ cm
    R, t, med, q = icp(M[::4], F, R0, t0, iters=25)
    print('cand med %.1f q70 %.1f' % (med, q))
    if best is None or q < best[3]: best = (R, t, med, q)
R, t, med, q = icp(M, F, best[0], best[1], iters=60, trim=0.6)
R, t, med, q = icp(M, F, R, t, iters=30, trim=0.5)
print('final median %.2f mm' % med)
json.dump({"R": R.tolist(), "t": t.tolist(), "median_mm": med}, open(sys.argv[3], 'w'), indent=1)
