"""Register a loose PART scan (own frame) to the same part on the car by PCA frames + trimmed ICP:
all 24 proper axis rotations between the part's and the target zone's principal axes are tried (brute-force rotation
search in globalreg.py stalls on thin smooth shells like a bumper skin).
    pcareg.py target_L.stl part.stl out_T.json --box x0,x1,y0,y1,z0,z1     (box = where the part sits on the car, mm)"""
import argparse, itertools, json, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("car"); ap.add_argument("part"); ap.add_argument("out"); ap.add_argument("--box", required=True)
a = ap.parse_args(); b = list(map(float, a.box.split(",")))
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
C = L(a.car); C = C[(C[:, 0] > b[0]) & (C[:, 0] < b[1]) & (C[:, 1] > b[2]) & (C[:, 1] < b[3]) & (C[:, 2] > b[4]) & (C[:, 2] < b[5])]
P = L(a.part); rng = np.random.default_rng(0)
Cs = C[rng.choice(len(C), min(len(C), 60000), False)]; Ps = P[rng.choice(len(P), min(len(P), 30000), False)]
def frame(X):
    m = X.mean(0); w, V = np.linalg.eigh(np.cov((X - m).T)); V = V[:, ::-1]
    if np.linalg.det(V) < 0: V[:, 2] *= -1
    return m, V
mc, Vc = frame(Cs); mp, Vp = frame(Ps); tree = cKDTree(Cs)
def icp(R, t, iters, keep, X=Ps, tr=tree):
    for _ in range(iters):
        Q = X @ R.T + t; d, j = tr.query(Q); m = d <= np.quantile(d, keep)
        A, B = X[m], tr.data[j[m]]; ma, mb = A.mean(0), B.mean(0)
        U, _, Vt = np.linalg.svd((B - mb).T @ (A - ma)); S = np.eye(3); S[2, 2] = np.sign(np.linalg.det(U @ Vt))
        R = U @ S @ Vt; t = mb - R @ ma
    d, _ = tr.query(X @ R.T + t); return R, t, d
res = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        Mx = np.zeros((3, 3))
        for i, p in enumerate(perm): Mx[i, p] = sg[i]
        if np.linalg.det(Mx) < 0: continue
        R = Vc @ Mx @ Vp.T; t = mc - R @ mp
        R, t, d = icp(R, t, 25, 0.6)
        res.append(((d < 6).mean(), np.median(d), R, t))
res.sort(key=lambda r: -r[0])
for f, md, R, t in res[:4]: print(f"coarse fit6 {f:.3f} median {md:.1f}")
treeF = cKDTree(C); best = None
for f, md, R, t in res[:3]:
    R, t, d = icp(R, t, 40, 0.8, P[::2], treeF)
    print(f"refined fit6 {(d<6).mean():.3f} fit3 {(d<3).mean():.3f} median {np.median(d):.2f} mm")
    if best is None or (d < 6).mean() > best[0]: best = ((d < 6).mean(), np.median(d), R, t)
T = np.eye(4); T[:3, :3] = best[2]; T[:3, 3] = best[3]
json.dump({"T": T.tolist(), "fitness6": best[0], "median_mm": best[1]}, open(a.out, "w")); print("BEST", best[0], best[1])
