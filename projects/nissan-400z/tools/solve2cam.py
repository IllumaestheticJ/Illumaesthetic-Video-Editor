"""ive solve output (blender rotation matrix) -> shot.py camera {loc, target, focal (sensor 36), roll}.
  python solve2cam.py cam_solve.json out.json"""
import json, math, sys
import numpy as np
c = json.load(open(sys.argv[1])); R = np.array(c["blender"]["rotation_matrix"]); loc = np.array(c["blender"]["location"])
f = -R[:, 2]; up = R[:, 1]
r0 = np.cross(f, [0, 0, 1.0]); r0 /= np.linalg.norm(r0); u0 = np.cross(r0, f)
roll = math.degrees(math.atan2(np.dot(R[:, 0], u0), np.dot(R[:, 0], r0)))
out = {"loc": loc.tolist(), "target": (loc + f * 4.0).tolist(), "roll": roll, "focal": c["fx_px"] / c["image_size"][0] * 36.0}
json.dump(out, open(sys.argv[2], "w"), indent=1); print(out)
