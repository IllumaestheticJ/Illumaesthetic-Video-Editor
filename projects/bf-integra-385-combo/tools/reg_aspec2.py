"""A-Spec rear -> Type S (GLB frame): multi-start yaw 20..160 deg (Z up; rear of the A-Spec scan faces ~+X),
target = Type S rear above bumper height (bumpers/diffusers differ between A-Spec and Type S), trimmed ICP."""
import trimesh, numpy as np, json
from scipy.spatial import cKDTree
R = '/home/user/media/bf-integra-385-combo/work/reg'
A = trimesh.load('/home/user/media/bf-integra-385-combo/scan/Integra ASpec Rear.stl', process=False); A.apply_scale(0.001)
Ty = trimesh.load(f'{R}/car_nospoiler.ply', process=False)
tg = Ty.sample(800000); tg = tg[(tg[:, 1] > 1.3) & (tg[:, 2] > 0.62)]
tree = cKDTree(tg)
src = A.sample(15000); src_hi = None
def fit(Pa, Pb):
    ca, cb = Pa.mean(0), Pb.mean(0); Hm = (Pa - ca).T @ (Pb - cb); U, _, Vt = np.linalg.svd(Hm); Rm = Vt.T @ U.T
    if np.linalg.det(Rm) < 0: Vt[-1] *= -1; Rm = Vt.T @ U.T
    return Rm, cb - Rm @ ca
def icp(T, it, trim):
    for _ in range(it):
        X = src @ T[:3, :3].T + T[:3, 3]; k0 = X[:, 2] > 0.62
        d, i = tree.query(X[k0]); k = d < np.quantile(d, trim)
        Rm, t = fit(X[k0][k], tg[i[k]]); D = np.eye(4); D[:3, :3] = Rm; D[:3, 3] = t; T = D @ T
    X = src @ T[:3, :3].T + T[:3, 3]; k0 = X[:, 2] > 0.62; d, _ = tree.query(X[k0]); return T, np.median(d)
# align bbox tops: source top z -> target top z
res = []
for yaw in range(20, 170, 10):
    a = np.radians(yaw); Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    X = src @ Rz.T
    t = np.array([tg[:, 0].mean() - X[:, 0].mean(), tg[:, 1].max() - X[:, 1].max(), tg[:, 2].max() - X[:, 2].max()])
    T = np.eye(4); T[:3, :3] = Rz; T[:3, 3] = t
    T, e = icp(T, 30, 0.5); res.append((e, yaw, T))
res.sort(key=lambda r: r[0]); print([(round(e * 1000, 1), y) for e, y, _ in res[:6]])
src = A.sample(60000)
T, e = icp(res[0][2], 60, 0.6); print('final median mm (above bumper)', round(e * 1000, 2))
json.dump({'matrix': T.tolist(), 'median_mm': e * 1000}, open(f'{R}/aspec_to_glb.json', 'w'))
A.apply_transform(T); A.export(f'{R}/aspec_rear_glbframe.ply')
