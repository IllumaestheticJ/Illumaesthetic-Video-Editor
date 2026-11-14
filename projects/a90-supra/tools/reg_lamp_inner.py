"""Seat a lamp part behind an already-placed part (housing behind the lens, insert inside the housing), raw car mm.
Target = the placed part's BOUNDARY (rim) points; the mover must put its own rim on them. Multi-start: mover PCA frame aligned to the
target's PCA frame (all proper sign/axis combos, both handednesses), trimmed ICP (closest 30 %), 30 -> 3 mm.
Score = rim coverage (target rim points with a mover point within 3 mm) minus the share of mover points OUTSIDE the car skin
(in front of the lens = sticking out of the body).
    python projects/a90-supra/tools/reg_lamp_inner.py mover.stl placed.stl --out T.json [--target-all]"""
import argparse, itertools, json
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); D = np.eye(3); D[2, 2] = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ D @ U.T; return R, cb - R @ ca
def rim(m):
    v = np.round(m["v"].reshape(-1, 3), 3); _, inv = np.unique(v, axis=0, return_inverse=True); f = inv.reshape(-1, 3)
    e = np.sort(np.r_[f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]], axis=1); u, c = np.unique(e, axis=0, return_counts=True)
    b = np.unique(u[c == 1]); allv = np.zeros((inv.max() + 1, 3)); allv[inv] = v; return allv[b]
ap = argparse.ArgumentParser(); ap.add_argument("mover"); ap.add_argument("placed"); ap.add_argument("--out"); ap.add_argument("--target-all", action="store_true")
ap.add_argument("--keep", type=float, default=0.3)
a = ap.parse_args(); rng = np.random.default_rng(0)
mv = np.fromfile(a.mover, dtype=TRI, offset=84); P0 = mv["v"].mean(1).astype(np.float64); P0 = P0[rng.choice(len(P0), min(len(P0), 20000), replace=False)]
pl = np.fromfile(a.placed, dtype=TRI, offset=84); Tall = pl["v"].mean(1).astype(np.float64)
T = Tall[rng.choice(len(Tall), min(len(Tall), 30000), replace=False)] if a.target_all else rim(pl)
R_ = rim(pl) if not a.target_all else T
lab = None
print("target points", len(T))
car = np.fromfile("/home/user/media/work/a90/car_2mm.stl", dtype=TRI, offset=84); cc = car["v"].mean(1); cn = car["n"]
box = (cc[:, 0] < Tall[:, 0].max() + 200) & (cc[:, 0] > Tall[:, 0].min() - 200) & (cc[:, 1] > Tall[:, 1].min() - 200) & (cc[:, 1] < Tall[:, 1].max() + 200)
cc, cn = cc[box], cn[box]; ct = cKDTree(cc)
tt = cKDTree(T); rt = cKDTree(R_)
c_t = T.mean(0); _, Vt = np.linalg.eigh(np.cov((T - c_t).T))
best = None
for hand in (1, -1):
    P = P0 * ([1, hand, 1]); cp = P.mean(0); _, Vp = np.linalg.eigh(np.cov((P - cp).T))
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            A = Vp[:, perm] * sg
            if np.linalg.det(A) * np.linalg.det(Vt) < 0: continue
            R = Vt @ A.T; t = c_t - R @ cp
            for ub in (30, 12, 6, 3):
                for _ in range(15):
                    Q = P @ R.T + t; d, i = tt.query(Q, distance_upper_bound=ub * 3, workers=4); ok = np.isfinite(d)
                    if ok.sum() < 50: break
                    m = ok & (d <= np.quantile(d[ok], a.keep)); R, t = kabsch(P[m], T[i[m]])
            Q = P @ R.T + t
            cov = (cKDTree(Q).query(R_, distance_upper_bound=10, workers=4)[0] < 3).mean()
            dc, ic = ct.query(Q, workers=4); outside = (((Q - cc[ic]) * cn[ic]).sum(1) > 2.0) & (dc < 60)
            sc = cov - outside.mean()
            if best is None or sc > best[0]: best = (sc, hand, R, t, cov, outside.mean())
    print("hand", hand, "best score %.2f rim coverage %.2f outside the skin %.2f" % (best[0], best[4], best[5]), flush=True)
sc, hand, R, t, cov, out = best
M = np.eye(4); M[:3, :3] = R @ np.diag([1, hand, 1]); M[:3, 3] = t
print("BEST hand", hand, "rim coverage %.2f outside %.2f" % (cov, out))
if a.out: json.dump(dict(mover=a.mover, placed=a.placed, mirrored=hand < 0, rim_coverage=cov, outside_skin=out, T_part_to_car_mm=M.tolist()), open(a.out, "w"), indent=1)
