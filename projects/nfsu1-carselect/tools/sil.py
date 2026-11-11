"""Silhouette tools for tracking the game's own car through the NFSU1 car-select animation.

The game's Miata is a blue NB; the Epsilon showroom has an NB GLB in the same frame as every kit car
(metres, Z up, nose -Y, tyres on z=0). Fitting the NB's painted-panel silhouette to the blue pixels of a
capture frame gives the camera relative to the car for that frame; the same camera then renders any kit car.
"""
import cv2, numpy as np

W, H = 2144, 1206
# zones where the menu is drawn over the scene (ignored when comparing silhouettes), capture pixels
UI = [(0, 0, W, 205), (0, 925, W, H), (1340, 250, 1790, 395), (0, 395, 175, 700)]


def size(scale):
    return int(round(W * scale)), int(round(H * scale))


def load_mesh(npz):
    d = np.load(npz)
    return d["V"].astype(np.float64), d["F"], d["C"]


def blue_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = ((h > 108) & (h < 135) & (s > 110) & (v > 22)).astype(np.uint8)
    return cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))


def valid_mask(scale):
    v = np.ones((H, W), np.uint8)
    for x0, y0, x1, y1 in UI:
        v[y0:y1, x0:x1] = 0
    return cv2.resize(v, size(scale), interpolation=cv2.INTER_NEAREST)


def project(V, pose, f):
    R, _ = cv2.Rodrigues(np.asarray(pose[:3], float))
    P = V @ R.T + np.asarray(pose[3:6], float)
    z = P[:, 2]
    zc = np.maximum(z, 0.05)
    return np.stack([f * P[:, 0] / zc + W / 2, f * P[:, 1] / zc + H / 2], 1), z


def render_classes(V, F, C, pose, f, scale):
    """Label image: 2 = painted panel visible, 1 = something else of the car in front of it, 0 = nothing.
    No z-buffer: camera-facing painted triangles are filled, then camera-facing glass / lamps / near-side wheels
    are filled over them. (A painter's sort over decimated triangles put hidden inner panels on top.)
    C: 1 paint, 0 other, -1 ignore; wheel triangles carry 10 + (0 left side, 1 right side)."""
    uv, z = project(V, pose, f)
    w, h = size(scale)
    img = np.zeros((h, w), np.uint8)
    R, _ = cv2.Rodrigues(np.asarray(pose[:3], float))
    cam = -R.T @ np.asarray(pose[3:6], float)
    p = uv[F]
    area2 = (p[:, 1, 0] - p[:, 0, 0]) * (p[:, 2, 1] - p[:, 0, 1]) - (p[:, 1, 1] - p[:, 0, 1]) * (p[:, 2, 0] - p[:, 0, 0])
    front = (area2 < 0) & (z[F].min(1) > 0.1)          # y is down, so CCW meshes come out negative
    pts = np.round(p * scale * 16).astype(np.int32)
    near_side = 10 if cam[0] > 0 else 11
    sel = front & (C == 1)
    if sel.any():
        cv2.fillPoly(img, list(pts[sel]), 2, lineType=cv2.LINE_8, shift=4)
    sel = front & ((C == 0) | (C == near_side))
    if sel.any():
        cv2.fillPoly(img, list(pts[sel]), 1, lineType=cv2.LINE_8, shift=4)
    return img


def cost(pose, V, F, C, f, obs, valid, scale, dt_obs=None, chamfer=0.0):
    """1 - IoU of observed blue pixels vs predicted painted panels; `chamfer` adds a symmetric mean edge distance
    (fraction of the frame diagonal) so the fit still has a slope when the two barely overlap."""
    img = render_classes(V, F, C, pose, f, scale)
    pred = (img == 2) & (valid > 0)
    o = (obs > 0) & (valid > 0)
    inter = (pred & o).sum()
    union = (pred | o).sum()
    if union == 0:
        return 2.0
    c = 1.0 - inter / union
    if not pred.any():
        return 2.0
    if dt_obs is not None and (chamfer > 0 or inter == 0):
        diag = float(np.hypot(*obs.shape))
        d1 = dt_obs[pred].mean() / diag
        d2 = 0.0
        if o.any():
            dt_pred = cv2.distanceTransform((~pred).astype(np.uint8), cv2.DIST_L2, 3)
            d2 = dt_pred[o].mean() / diag
        c += (chamfer if chamfer > 0 else 1.0) * (d1 + d2) * 10
    return c


def lookat_pose(az, el, dist, target, roll=0.0):
    """Camera on a sphere around `target` (car frame: nose -Y, Z up). az 0 = dead front, 90 = car's left."""
    a, e = np.radians(az), np.radians(el)
    d = np.array([np.sin(a) * np.cos(e), -np.cos(a) * np.cos(e), np.sin(e)])
    c = np.asarray(target, float) + d * dist
    fwd = -d
    right = np.cross(fwd, [0, 0, 1.0]); right /= np.linalg.norm(right)
    down = np.cross(fwd, right)
    R = np.stack([right, down, fwd])            # world -> camera (x right, y down, z forward)
    if roll:
        Rz, _ = cv2.Rodrigues(np.array([0, 0, np.radians(roll)])); R = Rz @ R
    t = -R @ c
    return np.concatenate([cv2.Rodrigues(R)[0].ravel(), t])


def cam_json(pose, f, path=None):
    """ive camera schema (Blender camera looks down -Z, Y up)."""
    R, _ = cv2.Rodrigues(np.asarray(pose[:3], float)); t = np.asarray(pose[3:6], float)
    c = -R.T @ t
    Rb = R.T @ np.diag([1.0, -1.0, -1.0])       # camera->world with Blender axes
    d = {"image_size": [W, H], "fx_px": float(f), "focal_mm": float(f * 36.0 / W), "sensor_width_mm": 36.0,
         "shift_x": 0.0, "shift_y": 0.0, "blender": {"location": c.tolist(), "rotation_matrix": Rb.tolist()},
         "opencv": {"rvec": [float(x) for x in pose[:3]], "tvec": t.tolist()}}
    if path:
        import json; json.dump(d, open(path, "w"), indent=1)
    return d


def car_mask(V, F, pose, f, scale):
    """Whole-car silhouette (every triangle in front of the camera, no culling)."""
    uv, z = project(V, pose, f)
    w, h = size(scale)
    img = np.zeros((h, w), np.uint8)
    ok = z[F].min(1) > 0.1
    pts = np.round(uv[F][ok] * scale * 16).astype(np.int32)
    pts = pts[(np.abs(pts).reshape(len(pts), -1).max(1) < 16 * 20000)]
    if len(pts):
        cv2.fillPoly(img, list(pts), 1, lineType=cv2.LINE_8, shift=4)
    return img
