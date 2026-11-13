"""Trimmed point-to-point ICP of A onto B (mm). ticp.py A.stl B.stl [keep_frac] [out.json] [zmin]
Prints the rigid motion and residuals per iteration; out.json gets R,t (apply as x' = R x + t)."""
import sys, json, numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = lambda p: np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1).astype(np.float64)
a, b = L(sys.argv[1]), L(sys.argv[2])
keep = float(sys.argv[3]) if len(sys.argv) > 3 else 0.4
zmin = float(sys.argv[5]) if len(sys.argv) > 5 else 150
rng = np.random.default_rng(1)
a = a[a[:, 2] > zmin]; a = a[rng.choice(len(a), min(80000, len(a)), replace=False)]
tb = cKDTree(b[b[:, 2] > zmin - 50])
R, t = np.eye(3), np.zeros(3)
for it in range(40):
    p = a @ R.T + t
    d, i = tb.query(p, distance_upper_bound=150)
    ok = np.isfinite(d); thr = np.quantile(d[ok], keep); m = ok & (d <= thr)
    q = tb.data[i[m]]; pm = p[m]
    cp, cq = pm.mean(0), q.mean(0)
    U, S, Vt = np.linalg.svd((pm - cp).T @ (q - cq))
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
    dR = Vt.T @ D @ U.T; dt = cq - dR @ cp
    R, t = dR @ R, dR @ t + dt
    if it % 8 == 0 or it == 39:
        print(it, "trim-median %.2f  all-p50 %.2f  within5 %.0f%%" % (np.median(d[m]), np.median(d[ok]), 100 * (d[ok] < 5).mean()))
ang = np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
print("rot deg %.3f  t mm" % ang, t.round(2))
if len(sys.argv) > 4: json.dump({"R": R.tolist(), "t": t.tolist()}, open(sys.argv[4], "w"))
