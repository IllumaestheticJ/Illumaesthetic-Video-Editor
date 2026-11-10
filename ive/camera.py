"""Hand-made camera JSONs (same schema as `ive solve` output) for reference renders."""
from __future__ import annotations

import json
import math

import numpy as np

from .solve import CV_TO_BLENDER_CAM, _matrix_to_euler_xyz


def lookat(loc, target, focal_mm=26.0, sensor_width_mm=36.0, size=(1080, 1920), roll_deg=0.0) -> dict:
    loc, target = np.array(loc, float), np.array(target, float)
    fwd = target - loc
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0, 0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    r = math.radians(roll_deg)
    right, up = right * math.cos(r) + up * math.sin(r), up * math.cos(r) - right * math.sin(r)
    R_c2w_blender = np.stack([right, up, -fwd], axis=1)  # columns = cam x,y,z in world
    R_w2c_cv = (R_c2w_blender @ CV_TO_BLENDER_CAM).T
    rvec = __import__("cv2").Rodrigues(R_w2c_cv)[0].ravel()
    tvec = -R_w2c_cv @ loc
    w = size[0]
    return {
        "image_size": list(size), "fx_px": focal_mm / sensor_width_mm * w, "focal_mm": focal_mm,
        "sensor_width_mm": sensor_width_mm, "shift_x": 0.0, "shift_y": 0.0,
        "blender": {"location": loc.tolist(), "rotation_euler": _matrix_to_euler_xyz(R_c2w_blender),
                    "rotation_matrix": R_c2w_blender.tolist()},
        "opencv": {"rvec": rvec.tolist(), "tvec": tvec.tolist()},
    }


def save(cam: dict, path: str) -> str:
    with open(path, "w") as f:
        json.dump(cam, f, indent=2)
    return path
