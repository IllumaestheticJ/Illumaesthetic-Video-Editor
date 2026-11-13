"""Register the Bomex x Kaido House CAD (kit/merged/*.stl, design frame mm, nose -Y, driver +X, ground ~z 0) to the levelled
scan frame (lev mm). Rigid trimmed ICP of the CAD parts whose mating faces lie on the stock body (front/rear fenders, side
skirts, ducktail) against Full Car + Rear Wing Removed, keeping the closest --keep fraction; grid of initial offsets.
Writes projects/nissan-400z/kit_T.json (lev = R @ cad + t) and per-part residuals."""
import glob, json, sys
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = "/home/user/media/nissan-400z/lev"; K = "/home/user/media/nissan-400z/kit/merged"
KEEP = float(sys.argv[sys.argv.index("--keep") + 1]) if "--keep" in sys.argv else 0.35
def pts(p, step=1): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)[::step].astype(np.float64)
tgt = np.concatenate([pts(f"{L}/Full_Car_3mm.stl", 6), pts(f"{L}/Rear_Wing_Removed_3mm.stl", 12)])
tgt = tgt[tgt[:, 2] > -700]  # body only (no ground/tyre contact)
tree = cKDTree(tgt)
FIT = ("front_fender_driver", "front_fender_pass", "rear_fender_driver", "rear_fender_pass", "side_skirts_driver", "side_skirts_pass", "ducktail")
cad = {g: pts(f"{K}/{g}.stl", max(1, len(np.fromfile(f"{K}/{g}.stl", dtype=TRI, offset=84)) // 12000)) for g in FIT}
P = np.concatenate(list(cad.values()))
best = None
for dz in (-640, -590, -540):  # kit skirt bottom (z -8) just below the scan sill (lev z -559)
    for dy in (-500, -460, -420):  # kit arch gap (skirt y -631..1174) centred on the scan wheelbase
        R = np.eye(3); t = np.array([9.0, dy, dz]); q = P + t
        for it in range(50):
            d, i = tree.query(q); m = d <= np.percentile(d, KEEP * 100); A, B = q[m], tgt[i[m]]
            ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); Ri = Vt.T @ U.T
            if np.linalg.det(Ri) < 0: Vt[-1] *= -1; Ri = Vt.T @ U.T
            q = (q - ca) @ Ri.T + cb; R = Ri @ R; t = Ri @ (t - ca) + cb
        d, _ = tree.query(q); sc = np.percentile(d, KEEP * 100)
        ang = np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1)))
        print(f"init dy {dy} dz {dz}: p{int(KEEP*100)} {sc:.2f} mm p20 {np.percentile(d,20):.2f} t {t.round(1)} rot {ang:.2f} deg", flush=True)
        if best is None or sc < best[0]: best = (sc, R.copy(), t.copy())
sc, R, t = best
json.dump({"R": R.tolist(), "t": t.tolist(), "score_mm": float(sc), "keep": KEEP}, open("projects/nissan-400z/kit_T.json", "w"), indent=1)
for g in sorted(glob.glob(f"{K}/*.stl")):
    n = g.split("/")[-1][:-4]; p = pts(g, 50)
    d, _ = tree.query(p @ R.T + t); print(f"{n:28s} p10 {np.percentile(d,10):6.1f} p35 {np.percentile(d,35):6.1f} p50 {np.percentile(d,50):6.1f} mm")
