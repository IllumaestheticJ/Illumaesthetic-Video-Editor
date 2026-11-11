"""Place a separately captured part scan (own Artec frame, e.g. 'Reverse Light', 'License Plate Light') onto the car frame.
Coarse: PCA-align the part, try all 24 proper axis permutations/sign flips, centroid at --seed (levelled mm).
Fine: trimmed point-to-point ICP against the target (bumper scan in the car frame) cropped to --radius around the seed.
Best = lowest median distance of the closest 80 % after ICP; prints the top hypotheses so a near-tie is visible.
  register_part.py part_lev.stl target.stl --seed x,y,z [--radius 350] out_M.npy
Apply with tools/xform.py out_M.npy part_lev.stl part_car.stl and LOOK at a render before trusting it."""
import argparse, itertools
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
ap = argparse.ArgumentParser(); ap.add_argument("part"); ap.add_argument("target"); ap.add_argument("out")
ap.add_argument("--seed", required=True); ap.add_argument("--radius", type=float, default=350)
ap.add_argument("--axes", default="", help="optional target extents order hint, unused")
a = ap.parse_args()
P = np.fromfile(a.part, dtype=TRI, offset=84)["v"].mean(1).astype(float)
T = np.fromfile(a.target, dtype=TRI, offset=84)["v"].mean(1).astype(float)
seed = np.array([float(v) for v in a.seed.split(",")])
T = T[np.linalg.norm(T - seed, axis=1) < a.radius]
tree = cKDTree(T)
rng = np.random.default_rng(0)
Ps = P[rng.choice(len(P), min(6000, len(P)), replace=False)]
cp = Ps.mean(0); E = np.linalg.svd(Ps - cp, full_matrices=False)[2]   # rows = principal axes (part frame)
mats = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3))
        for i, (p, s) in enumerate(zip(perm, sg)): M[i, p] = s
        if np.linalg.det(M) > 0: mats.append(M)
# target principal axes near the seed (the bumper surface): map part axes onto them
ct = T.mean(0); Et = np.linalg.svd(T - ct, full_matrices=False)[2]
res = []
for M in mats:
    R = Et.T @ M @ E          # part axis k -> target axis
    t = seed - R @ cp
    for it in range(40):
        X = Ps @ R.T + t
        d, j = tree.query(X)
        keep = d < np.percentile(d, 80)
        A, B = X[keep], T[j[keep]]
        ca, cb = A.mean(0), B.mean(0)
        U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb))
        D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
        dR = Vt.T @ D @ U.T
        # new X = dR (X - ca) + cb  =>  R <- dR R,  t <- dR t - dR ca + cb
        R = dR @ R; t = dR @ t - dR @ ca + cb
    X = Ps @ R.T + t
    d, _ = tree.query(X)
    s = np.sort(d)[: int(0.8 * len(d))]
    res.append((float(np.median(s)), float((d < 4).mean()), R, t))
res.sort(key=lambda r: r[0])
for r in res[:5]:
    print(f"median(80%) {r[0]:6.2f} mm  inliers<4mm {100 * r[1]:5.1f} %  centre {(r[2] @ cp + r[3]).round(0)}")
M4 = np.eye(4); M4[:3, :3] = res[0][2]; M4[:3, 3] = res[0][3]
np.save(a.out, M4); print("saved", a.out)
