"""Refine the A-Spec -> Type S registration on the TRUNK LID only (same decklid; bumpers/diffusers differ)."""
import trimesh, numpy as np, json
from scipy.spatial import cKDTree
R = '/home/user/media/bf-integra-385-combo/work/reg'
A = trimesh.load('/home/user/media/bf-integra-385-combo/scan/Integra ASpec Rear.stl', process=False); A.apply_scale(0.001)
T0 = np.array(json.load(open(f'{R}/aspec_to_glb.json'))['matrix'])
Ty = trimesh.load(f'{R}/car_nospoiler.ply', process=False)
def deck(P, margin=0.0):
    return (np.abs(P[:, 0]) < 0.62 + margin) & (P[:, 1] > 1.45 - margin) & (P[:, 1] < 2.30 + margin) & (P[:, 2] > 0.86 - margin)
tg = Ty.sample(1500000); tg = tg[deck(tg)]
# exclude the spoiler footprint on the target (no Type S surface there anyway) and the rear window
tg = tg[~((tg[:, 1] > 1.98) & (tg[:, 2] > 0.93))]
tree = cKDTree(tg)
src_all = A.sample(400000)
def fit(Pa, Pb):
    ca, cb = Pa.mean(0), Pb.mean(0); Hm = (Pa - ca).T @ (Pb - cb); U, _, Vt = np.linalg.svd(Hm); Rm = Vt.T @ U.T
    if np.linalg.det(Rm) < 0: Vt[-1] *= -1; Rm = Vt.T @ U.T
    return Rm, cb - Rm @ ca
T = T0.copy()
for it in range(80):
    X = src_all @ T[:3, :3].T + T[:3, 3]
    sel = deck(X, 0.05) & ~((X[:, 1] > 1.98) & (X[:, 2] > 0.93))
    Xs = X[sel]
    d, i = tree.query(Xs); k = d < np.quantile(d, 0.6)
    Rm, t = fit(Xs[k], tg[i[k]]); D = np.eye(4); D[:3, :3] = Rm; D[:3, 3] = t; T = D @ T
    if it % 20 == 0 or it == 79: print(it, sel.sum(), 'median mm', round(np.median(d) * 1000, 2))
json.dump({'matrix': T.tolist()}, open(f'{R}/aspec_to_glb_trunk.json', 'w'))
A.apply_transform(T); A.export(f'{R}/aspec_rear_glbframe.ply')
