"""Fast silhouette of the car GLB from a camera (no Blender): for scoring how much of the game's car our car covers.

    from sil import Car, cam_from; car = Car(npz from tools/dump_mesh.py); m = car.mask(cam_from(x, y, z, heading, pitch), hide=[...], scale=0.25)
Car frame: Z up, nose -Y, left +X (as tools/mancam.py).
"""
import json
import numpy as np, cv2

F, SIZE = 1757.0, (2560, 1440)


def cam_from(x, y, z, hd, pt):
    h, p = np.radians(hd), np.radians(pt)
    fwd = np.array([np.cos(h) * np.cos(p), np.sin(h) * np.cos(p), np.sin(p)])
    right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
    return np.array([x, y, z], float), np.stack([right, up, -fwd], 1)


def cam_json(path):
    c = json.load(open(path))["blender"]
    return np.array(c["location"]), np.array(c["rotation_matrix"])


class Car:
    def __init__(self, npz):
        d = np.load(npz); self.parts = {}
        for k in d.files:
            if k.endswith("|v"):
                self.parts[k[:-2]] = [(d[k].astype(float), d[k[:-2] + "|f"])]          # already Z up, nose -Y (Blender import)

    def project(self, cam, pts):
        loc, M = cam
        pc = (pts - loc) @ M                                         # camera coords: x right, y up, z back
        z = -pc[:, 2]
        return np.stack([SIZE[0] / 2 + F * pc[:, 0] / z, SIZE[1] / 2 - F * pc[:, 1] / z], 1), z

    def mask(self, cam, hide=(), only=None, scale=0.25, drop=0.0):
        m = np.zeros((int(SIZE[1] * scale), int(SIZE[0] * scale)), np.uint8)
        for name, lst in self.parts.items():
            if name in hide or (only and name not in only):
                continue
            for v, f in lst:
                if drop and not name.startswith("wheel"):
                    v = v - [0, 0, drop]
                p, z = self.project(cam, v)
                ok = (z[f] > 0.05).all(1)
                tri = (p[f[ok]] * scale).round().astype(np.int32)
                tri = tri[(np.abs(tri).max((1, 2)) < 20000)]
                cv2.fillPoly(m, list(tri), 1)
        return m > 0
