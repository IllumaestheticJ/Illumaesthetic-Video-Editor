"""v1: refine a GLB-frame scan against the lookbook body, MODEL -> SCAN (the scan's interior/roll bar no longer count).
Trimmed similarity ICP of the painted GLB body onto the scan; the inverse is applied to the scan in place.
    python refine_fit.py scan_glbframe.stl body.stl [more_body.stl ...]"""
import sys, json
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl, write_stl, umeyama

scan_p, bodies = sys.argv[1], sys.argv[2:]
T = read_stl(scan_p); C = T.mean(1)
B = np.concatenate([read_stl(b).reshape(-1, 3) for b in bodies]); B = np.unique(B.round(3), axis=0)
B = B[B[:, 2] > 0.30]
rng = np.random.default_rng(0)
if len(B) > 120000: B = B[rng.choice(len(B), 120000, replace=False)]
tree = cKDTree(C)
s, R, t = 1.0, np.eye(3), np.zeros(3)
def rep(tag):
    d, _ = tree.query(s * B @ R.T + t); print(f"{tag}: model->scan median {np.median(d)*1000:.1f} mm p75 {np.percentile(d,75)*1000:.1f} p90 {np.percentile(d,90)*1000:.1f} scale {s:.4f}")
rep("before")
for scale, keep, it in ((False, 0.6, 25), (True, 0.7, 25), (True, 0.8, 20)):
    for _ in range(it):
        P = s * B @ R.T + t; d, j = tree.query(P); m = d <= np.quantile(d, keep)
        s, R, t = umeyama(B[m], C[j[m]], scale)
rep("after")
V = ((T.reshape(-1, 3) - t) @ R) / s          # inverse: scan -> model frame
write_stl(scan_p, V.reshape(-1, 3, 3))
json.dump({"s": s, "R": R.tolist(), "t": t.tolist()}, open(scan_p.replace(".stl", "_refine.json"), "w"))
