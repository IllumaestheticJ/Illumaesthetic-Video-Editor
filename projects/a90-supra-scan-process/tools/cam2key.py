"""Convert an `ive solve` camera JSON to a shots.py cam key {pos, look, lens, roll} that reproduces it exactly.
usage: python cam2key.py cam.json [look_dist_m]"""
import json, math, sys
import numpy as np
c = json.load(open(sys.argv[1])); d = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
R = np.array(c["blender"]["rotation_matrix"]); p = np.array(c["blender"]["location"])
f = -R[:, 2]; u_true = R[:, 1]
look = p + f * d
up = np.array([0, 0, 1.0]); r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
# shots.py applies rotate_axis("Z", roll) after building (r, u, -f). Sign verified by rendering: the silhouette
# bbox of shots.py frame 0 equals `ive render --camera` exactly (cam_A, A90 scan-process reel).
roll = math.degrees(math.atan2(np.dot(np.cross(u, u_true), -f), np.dot(u, u_true)))
print(json.dumps({"pos": p.round(5).tolist(), "look": look.round(5).tolist(), "lens": c["focal_mm"], "roll": round(roll, 4),
                  "sensor": c["sensor_width_mm"], "shift": [c.get("shift_x", 0), c.get("shift_y", 0)]}))
