"""Refine kit_T.json (dense trimmed ICP from the stored pose) and write every kit/merged/<g>.stl into the levelled scan
frame (lev mm): /home/user/media/nissan-400z/kit/lev/<g>.stl, ready for `ive decimate` + `ive prep --like car.json`."""
import glob, json, os, struct
import numpy as np
from scipy.spatial import cKDTree
TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
L = "/home/user/media/nissan-400z/lev"; K = "/home/user/media/nissan-400z/kit"; J = "projects/nissan-400z/kit_T.json"
def pts(p, step=1): return np.fromfile(p, dtype=TRI, offset=84)["v"].mean(1)[::step].astype(np.float64)
T = json.load(open(J)); R = np.array(T["R"]); t = np.array(T["t"])
tgt = np.concatenate([pts(f"{L}/Full_Car_3mm.stl", 2), pts(f"{L}/Rear_Wing_Removed_3mm.stl", 4)]); tgt = tgt[tgt[:, 2] > -700]
tree = cKDTree(tgt)
FIT = ("front_fender_driver", "front_fender_pass", "rear_fender_driver", "rear_fender_pass", "ducktail", "gas_cap_x")
P = np.concatenate([pts(f"{K}/merged/{g}.stl", max(1, len(np.fromfile(f"{K}/merged/{g}.stl", dtype=TRI, offset=84)) // 30000)) for g in FIT])
q = P @ R.T + t
for it in range(40):
    d, i = tree.query(q); m = d <= np.percentile(d, 35); A, B = q[m], tgt[i[m]]
    ca, cb = A.mean(0), B.mean(0); U, S, Vt = np.linalg.svd((A - ca).T @ (B - cb)); Ri = Vt.T @ U.T
    if np.linalg.det(Ri) < 0: Vt[-1] *= -1; Ri = Vt.T @ U.T
    q = (q - ca) @ Ri.T + cb; R = Ri @ R; t = Ri @ (t - ca) + cb
d, _ = tree.query(q); print("refined p20 %.2f p35 %.2f mm" % (np.percentile(d, 20), np.percentile(d, 35)), "t", t.round(1))
json.dump({**T, "R": R.tolist(), "t": t.tolist(), "refined_p35_mm": float(np.percentile(d, 35))}, open(J, "w"), indent=1)
os.makedirs(f"{K}/lev", exist_ok=True)
for f in sorted(glob.glob(f"{K}/merged/*.stl")):
    m = np.fromfile(f, dtype=TRI, offset=84)
    m["v"] = (m["v"].reshape(-1, 3).astype(np.float64) @ R.T + t).reshape(-1, 3, 3).astype(np.float32)
    m["n"] = (m["n"].astype(np.float64) @ R.T).astype(np.float32)
    o = f"{K}/lev/{os.path.basename(f)}"
    with open(o, "wb") as fo: fo.write(b"bomex kit in lev frame".ljust(80)); fo.write(struct.pack("<I", len(m))); m.tofile(fo)
    print(o, len(m))
