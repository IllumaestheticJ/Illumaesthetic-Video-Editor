"""Landmark camera solve when a silhouette solve gets the outline but not the interior (MR2 cut B: 12 deg roll error).
Pairs are picked by eye on gridded crops: 'real' px in the footage frame, 'rend' px in a render from a KNOWN camera
(--init). Each rend px is ray-cast onto the world-space meshes to get its 3D point; points with known xyz skip that.
Then solvePnP (fixed focal) + LM refine. usage: pnp_landmarks.py pairs.json out.json --init cam.json --mesh a.npz b.npz"""
import sys, json, argparse, numpy as np, cv2, open3d as o3d
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz
ap = argparse.ArgumentParser(); ap.add_argument('pairs'); ap.add_argument('out'); ap.add_argument('--init', required=True)
ap.add_argument('--mesh', nargs='+', required=True); a = ap.parse_args()
cam = json.load(open(a.init)); W, H = cam['image_size']; f = cam['fx_px']; K = np.array([[f, 0, W / 2], [0, f, H / 2], [0, 0, 1.]])
R0, _ = cv2.Rodrigues(np.array(cam['opencv']['rvec'])); t0 = np.array(cam['opencv']['tvec']); C = -R0.T @ t0
sc = o3d.t.geometry.RaycastingScene()
for m in a.mesh:
    d = np.load(m); sc.add_triangles(o3d.core.Tensor(d['v'].astype(np.float32)), o3d.core.Tensor(d['f'].astype(np.uint32)))
P = json.load(open(a.pairs))['points']; obj, img = [], []
for p in P:
    if 'xyz' not in p:
        # corners sit on edges: cast a +-10 px patch and keep the nearest surface (median of hits within 0.1 m of the closest)
        hs = []
        for dx in range(-10, 11, 5):
            for dy in range(-10, 11, 5):
                d = R0.T @ np.linalg.inv(K) @ np.array([p['rend'][0] + dx, p['rend'][1] + dy, 1.]); d /= np.linalg.norm(d)
                h = sc.cast_rays(o3d.core.Tensor(np.r_[C, d][None].astype(np.float32)))['t_hit'].numpy()[0]
                if np.isfinite(h): hs.append(C + d * h)
        assert hs, p['name']; hs = np.array(hs); dist = np.linalg.norm(hs - C, axis=1)
        p['xyz'] = np.median(hs[dist < dist.min() + 0.1], axis=0).round(4).tolist()
    obj.append(p['xyz']); img.append(p['real']); print(p['name'], p['xyz'])
obj, img = np.array(obj, float), np.array(img, float)
ok, r, t = cv2.solvePnP(obj, img, K, None, rvec=np.array(cam['opencv']['rvec']), tvec=t0.copy(), useExtrinsicGuess=True, flags=cv2.SOLVEPNP_ITERATIVE)
r, t = cv2.solvePnPRefineLM(obj, img, K, None, r, t)
q, _ = cv2.projectPoints(obj, r, t, K, None); e = np.linalg.norm(q.reshape(-1, 2) - img, axis=1)
for p, ee in zip(P, e): print(f"  {p['name']:14s} err {ee:6.1f} px")
print('rms', np.sqrt((e ** 2).mean()))
R, _ = cv2.Rodrigues(r); loc = (-R.T @ t.reshape(3)).ravel(); Rb = R.T @ CV_TO_BLENDER_CAM
out = dict(cam); out.update({"blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(Rb), "rotation_matrix": Rb.tolist()},
    "opencv": {"rvec": r.ravel().tolist(), "tvec": t.ravel().tolist()}, "solve": "landmark PnP (tools/pnp_landmarks.py)", "cost": float(np.sqrt((e ** 2).mean()))})
json.dump(out, open(a.out, 'w'), indent=2); json.dump({"points": P}, open(a.pairs, 'w'), indent=1); print('loc', loc.round(3))
