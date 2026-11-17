"""v1: NC stock fender zone. The lookbook NC body already has the fender-cut opening, so the stock panel on the scan =
footprint of the lookbook stock piece + kit part, PLUS the scan skin behind the front wheel that the lookbook body does
not have (the closed stock fender). Writes dec/nc_fender_idx.npy (triangle indices of nc_glbframe.stl)."""
import sys, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from scan_to_glb import read_stl
M = "/home/user/media/bf-miata-mr2-night-meet"; D = f"{M}/dec"; K = f"{M}/kit_nc"
T = read_stl(f"{D}/nc_glbframe.stl"); C = T.mean(1)
def pts(p):
    X = read_stl(p); return np.concatenate([X.reshape(-1, 3), X.mean(1)])
P = np.concatenate([pts(f"{K}/body_fender_cuts_stock.stl"), pts(f"{K}/part_fender_cuts.stl")])
lo, hi = P.min(0), P.max(0)
box = (np.abs(C[:, 0]) > 0.60) & (C[:, 1] > lo[1] - 0.01) & (C[:, 1] < hi[1] + 0.01) & (C[:, 2] > lo[2] - 0.01) & (C[:, 2] < hi[2] + 0.01)
idx = np.where(box)[0]
B = pts(f"{K}/body.stl"); B = B[(np.abs(B[:, 0]) > 0.5) & (B[:, 1] > lo[1] - 0.1) & (B[:, 1] < hi[1] + 0.1) & (B[:, 2] < hi[2] + 0.1)]
db, _ = cKDTree(B).query(C[idx]); dp, _ = cKDTree(P).query(C[idx])
sel = idx[(db > 0.006) | (dp < 0.006)]
# outer skin only: nothing deeper than 60 mm inboard of the outermost scan surface at that (y, z)
key = np.round(C[sel][:, 1:] / 0.02).astype(int); side = np.sign(C[sel][:, 0])
out = {}
for k, s, x in zip(map(tuple, key), side, np.abs(C[sel][:, 0])): out[(k, s)] = max(out.get((k, s), 0), x)
keep = np.array([abs(x) > out[(tuple(k), s)] - 0.06 for k, s, x in zip(key, side, C[sel][:, 0])])
sel = sel[keep]; np.save(f"{D}/nc_fender_idx.npy", sel); print("fender zone tris", len(sel))
