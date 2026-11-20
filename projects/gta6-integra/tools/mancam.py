"""Camera JSON from a position and a view direction in the car's frame (Z up, nose -Y, left +X), no roll.

    python projects/gta6-integra/tools/mancam.py NAME x y z heading_deg pitch_deg [focal_px]

heading: direction the camera looks, degrees from +X toward +Y (so -90 looks at the nose from behind).
Used for the close-up views of the second capture (exhaust, suspension, wheel), where the camera is set from
the car direction's vanishing point (heading), the wheel's size on screen (distance) and where the wheel or
bumper sits in the frame, then checked by overlay.
"""
import json, sys
from pathlib import Path
import numpy as np

name = sys.argv[1]; x, y, z, hd, pt = map(float, sys.argv[2:7]); f = float(sys.argv[7]) if len(sys.argv) > 7 else 1757.0
h, p = np.radians(hd), np.radians(pt)
fwd = np.array([np.cos(h) * np.cos(p), np.sin(h) * np.cos(p), np.sin(p)])
right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
cam = {"image_size": [2560, 1440], "fx_px": f, "focal_mm": 36.0 * f / 2560, "sensor_width_mm": 36.0, "shift_x": 0.0, "shift_y": 0.0,
       "blender": {"location": [x, y, z], "rotation_matrix": np.stack([right, up, -fwd], 1).round(8).tolist()}}
out = Path(__file__).resolve().parents[1] / f"cam_{name}.json"
json.dump(cam, open(out, "w"), indent=1); print(out)
