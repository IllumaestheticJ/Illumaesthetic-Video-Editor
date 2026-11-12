"""Register the team's Ronin CAD (Drive 'Nissan Frontier (SEMA 2026)/STL': grille + 4 fenders, design frame) to the
levelled scan frame. Rigid: initial translation from wheel-arch / grille centres, then trimmed point-to-point ICP of the
CAD points against the truck (full car + flares-removed + bumper-off states), keeping the closest --keep fraction (the CAD's
mating faces touch the body; its outer skin does not). Writes projects/nissan-frontier/ronin_T.json (R, t: lev = R@cad + t)."""
import glob, json
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = "/home/user/media/nissan-frontier/lev"
def pts(p, step=1): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)[::step].astype(np.float64)
tgt = np.concatenate([pts(f"{L}/full_4mm.stl", 3), pts(f"{L}/flares_2mm_C.stl", 6), pts(f"{L}/fbrhc_2mm_C.stl", 4)])
tree = cKDTree(tgt)
cad = {f.split("/")[-1][:-4]: pts(f, 25) for f in sorted(glob.glob("/home/user/media/nissan-frontier/ronin/*.stl"))}
P = np.concatenate(list(cad.values()))
best = None
for dz in (60, 120, 180, 240):
    for dy in (-1420, -1390, -1360):
        R = np.eye(3); t = np.array([18.0, dy, dz]); q = P + t
        for it in range(60):
            d, i = tree.query(q); thr = np.percentile(d, 35)
            m = d <= thr; A, B = q[m], tgt[i[m]]
            ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); Ri = Vt.T @ U.T
            if np.linalg.det(Ri) < 0: Vt[-1] *= -1; Ri = Vt.T @ U.T
            q = (q - ca) @ Ri.T + cb; R = Ri @ R; t = Ri @ (t - ca) + cb
        d, _ = tree.query(q); sc = np.percentile(d, 35)
        print(f"init dy {dy} dz {dz}: p35 {sc:.2f} mm, p20 {np.percentile(d,20):.2f}, t {t.round(1)}, rot {np.degrees(np.arccos(np.clip((np.trace(R)-1)/2,-1,1))):.2f} deg")
        if best is None or sc < best[0]: best = (sc, R.copy(), t.copy())
sc, R, t = best
json.dump({"R": R.tolist(), "t": t.tolist(), "p35_mm": float(sc)}, open("projects/nissan-frontier/ronin_T.json", "w"), indent=1)
for k, p in cad.items():
    d, _ = tree.query(p @ R.T + t); print(k, "p10 %.1f p35 %.1f p50 %.1f mm" % tuple(np.percentile(d, [10, 35, 50])))
