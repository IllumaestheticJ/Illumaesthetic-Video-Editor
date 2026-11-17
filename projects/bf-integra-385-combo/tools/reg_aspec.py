"""Register the DE4 A-Spec rear scan (wingless trunk, same decklid as the Type S) to the Type S scan in the GLB frame.
Rigid ICP (trimmed, multi-start over yaw and the two up-axis choices), target = Type S rear, spoiler zone excluded."""
import trimesh, numpy as np, json
from scipy.spatial import cKDTree
R = '/home/user/media/bf-integra-385-combo/work/reg'
A = trimesh.load('/home/user/media/bf-integra-385-combo/scan/Integra ASpec Rear.stl', process=False)
A.apply_scale(0.001)
T_ = trimesh.load(f'{R}/car_nospoiler.ply', process=False)
rng = np.random.default_rng(0)
src = A.sample(12000)
tgt = T_.sample(500000); tgt = tgt[tgt[:, 1] > 0.6]
tree = cKDTree(tgt)
def fit(Pa, Pb):
    ca, cb = Pa.mean(0), Pb.mean(0); Hm = (Pa - ca).T @ (Pb - cb); U, _, Vt = np.linalg.svd(Hm); Rm = Vt.T @ U.T
    if np.linalg.det(Rm) < 0: Vt[-1] *= -1; Rm = Vt.T @ U.T
    return Rm, cb - Rm @ ca
def icp(T, it=35, trim=0.7):
    for _ in range(it):
        X = src @ T[:3, :3].T + T[:3, 3]; d, i = tree.query(X); k = d < np.quantile(d, trim)
        Rm, t = fit(X[k], tgt[i[k]]); D = np.eye(4); D[:3, :3] = Rm; D[:3, 3] = t; T = D @ T
    X = src @ T[:3, :3].T + T[:3, 3]; d, _ = tree.query(X); return T, np.median(d)
ups = {'z': np.eye(3)}  # bounds: 1.84 m across = car width, Z = height
res = []
for un, U0 in ups.items():
    for yaw in range(0, 360, 30):
        a = np.radians(yaw); Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
        Rr = Rz @ U0; T = np.eye(4); T[:3, :3] = Rr; T[:3, 3] = tgt.mean(0) - Rr @ src.mean(0)
        T, e = icp(T, 20); res.append((e, un, yaw, T))
res.sort(key=lambda r: r[0]); print([(round(e * 1000, 1), u, y) for e, u, y, _ in res[:5]])
T, e = icp(res[0][3], 60, 0.8); print('final median mm', round(e * 1000, 2))
json.dump({'matrix': T.tolist(), 'median_mm': e * 1000}, open(f'{R}/aspec_to_glb.json', 'w'))
A.apply_transform(T); A.export(f'{R}/aspec_rear_glbframe.ply')
