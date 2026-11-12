"""Fit the Epsilon lookbook model (kit/glb/*.stl, model frame: front -Y, m) to the prepped scan frame (front +Y, floor z=0).

Trimmed similarity ICP of the model's painted body onto the FE1 scan (after fg2-race-car/tools/align_game.py), started
from a 180 deg turn about Z. Writes kit/model_to_scan.json and kit/scan/<part>.stl in RAW scan units (mm, minus root) so
`ive prep --like car4.json` puts them exactly on the car.
"""
import glob, json, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stlio import read, write  # noqa: E402

M = "/home/user/media/honda-civic-11"
pj = json.load(open(f"{M}/prep/car4.json")); s0 = pj["unit_scale"]; root = np.array(pj["root_location"])
S = read(f"{M}/dec/fe1_final_4mm.stl")["v"].reshape(-1, 3).astype(np.float64) * s0 + root
S = np.unique(S.round(4), axis=0)
B = np.unique(read(f"{M}/kit/glb/body.stl")["v"].reshape(-1, 3).astype(np.float64).round(4), axis=0)


def umeyama(A, Bp, scale):
    ma, mb = A.mean(0), Bp.mean(0); A0, B0 = A - ma, Bp - mb
    U, D, Vt = np.linalg.svd(B0.T @ A0 / len(A)); Sg = np.eye(3); Sg[2, 2] = np.sign(np.linalg.det(U @ Vt))
    R = U @ Sg @ Vt; s = (D * np.diag(Sg)).sum() / A0.var(0).sum() if scale else 1.0
    return s, R, mb - s * R @ ma


tree = cKDTree(S)
# free similarity fit. It pitches the model ~3 deg nose-down: correct, the scanned car sits that way in the prepped
# frame (front tyres bottom z 0.07-0.09, rear 0.19-0.28); a yaw-only fit floated the model 26 cm (median 31 mm).
R = np.diag([-1.0, -1.0, 1.0]); s = 1.0
t = np.array([0.0, (S[:, 1].min() + S[:, 1].max()) / 2 + (B[:, 1].min() + B[:, 1].max()) / 2, 0.0])
t[2] = np.percentile(S[:, 2], 99.9) - B[:, 2].max()


def fit4(A, Bp, scale):
    s2, R2, t2 = umeyama(np.c_[A[:, :2], np.zeros(len(A))], np.c_[Bp[:, :2], np.zeros(len(A))], False)
    Rz = np.eye(3); Rz[:2, :2] = R2[:2, :2]
    a0, b0 = A - A.mean(0), Bp - Bp.mean(0)
    sc = float((b0 * (a0 @ Rz.T)).sum() / (a0 ** 2).sum()) if scale else 1.0
    return sc, Rz, Bp.mean(0) - sc * Rz @ A.mean(0)


for scale, keep, it in ((False, 0.6, 40), (True, 0.7, 60), (True, 0.8, 40)):
    for _ in range(it):
        P = s * B @ R.T + t; d, j = tree.query(P); m = d <= np.quantile(d, keep)
        s, R, t = umeyama(B[m], S[j[m]], scale)
    P = s * B @ R.T + t; d, _ = tree.query(P)
    print(f"scale={scale} keep={keep}: s={s:.4f} median {np.median(d)*1000:.1f} mm p75 {np.percentile(d,75)*1000:.1f} p90 {np.percentile(d,90)*1000:.1f}")
print("R\n", R.round(4), "\nt", t.round(4))
json.dump({"scale": s, "R": R.tolist(), "t": t.tolist()}, open(f"{M}/kit/model_to_scan.json", "w"), indent=1)
os.makedirs(f"{M}/kit/scan", exist_ok=True)
for f in sorted(glob.glob(f"{M}/kit/glb/*.stl")):
    d = read(f); v = d["v"].reshape(-1, 3).astype(np.float64)
    p = s * v @ R.T + t
    d["v"] = ((p - root) / s0).reshape(-1, 3, 3).astype(np.float32)
    n = d["n"].astype(np.float64) @ R.T; d["n"] = n.astype(np.float32)
    write(f"{M}/kit/scan/{os.path.basename(f)}", d)
    print(os.path.basename(f), p.min(0).round(3), p.max(0).round(3))
