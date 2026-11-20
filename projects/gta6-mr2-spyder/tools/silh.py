"""Fast silhouette of the car from a camera JSON (no Blender): geometry from export_geo.py's .npz.
    from silh import Geo; g = Geo(); mask = g.mask(cam_dict, hide=[...], scale=0.25); g.bbox(cam, "part_side_skirts")
"""
import json, numpy as np, cv2
NPZ = "/home/user/media/work/gta6-mr2-spyder/geo/mr2.npz"
STOCK_HIDE = ["part_front_bumper", "part_eyelids", "part_hood_vents", "part_duckbill", "part_side_skirts", "part_rear_spats", "part_diffuser", "part_hardtop", "hardtop_rear_window"]


def mancam(x, y, z, hd, pt, f=1757.0):
    h, p = np.radians(hd), np.radians(pt)
    fwd = np.array([np.cos(h) * np.cos(p), np.sin(h) * np.cos(p), np.sin(p)])
    right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
    return {"image_size": [2560, 1440], "fx_px": f, "focal_mm": 36.0 * f / 2560, "sensor_width_mm": 36.0, "shift_x": 0.0, "shift_y": 0.0,
            "blender": {"location": [x, y, z], "rotation_matrix": np.stack([right, up, -fwd], 1).round(8).tolist()}}


class Geo:
    def __init__(self, npz=NPZ):
        d = np.load(npz); self.tris = {k: d[k] for k in d.files}

    def project(self, cam, pts):
        loc = np.array(cam["blender"]["location"]); M = np.array(cam["blender"]["rotation_matrix"])
        pc = (pts - loc) @ M; z = -pc[..., 2]
        f = cam["fx_px"]; W, H = cam["image_size"]
        return np.stack([W / 2 + f * pc[..., 0] / z, H / 2 - f * pc[..., 1] / z], -1), z

    def mask(self, cam, hide=(), scale=0.25, only=None, drop=0.0):
        W, H = cam["image_size"]; m = np.zeros((int(H * scale), int(W * scale)), np.uint8)
        for k, t in self.tris.items():
            if k in hide or (only and k not in only):
                continue
            if drop and not k.startswith("wheel"):
                t = t - np.array([0, 0, drop], np.float32)
            p, z = self.project(cam, t); ok = (z > 0.05).all(1)
            cv2.fillPoly(m, list((p[ok] * scale).astype(np.int32)), 255)
        return m

    def bbox(self, cam, node):
        p, z = self.project(cam, self.tris[node].reshape(-1, 3)); p = p[z > 0.05]
        if not len(p):
            return [-9e3, -9e3, 9e3, 9e3]
        return [float(v) for v in (p[:, 0].min(), p[:, 1].min(), p[:, 0].max(), p[:, 1].max())]


def overlay(frame, mask, color=(0, 255, 0)):
    m = cv2.resize(mask, (frame.shape[1], frame.shape[0])) > 0
    out = frame.copy(); out[m] = (out[m] * 0.45 + np.array(color) * 0.55).astype(np.uint8)
    return out
