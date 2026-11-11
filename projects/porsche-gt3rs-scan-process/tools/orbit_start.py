"""Write a camera that, orbited by +deg about pivot (as scan_render --move orbit --look-at does), ENDS on cam_end."""
import json, math, sys
import numpy as np
cam_end, out, deg, pivot = sys.argv[1], sys.argv[2], float(sys.argv[3]), np.array([float(v) for v in sys.argv[4].split(',')])
c = json.load(open(cam_end))
a = math.radians(-deg); Rz = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
R = np.array(c['blender']['rotation_matrix']); L = np.array(c['blender']['location'])
c['blender']['location'] = (pivot + Rz @ (L - pivot)).tolist()
R2 = Rz @ R; c['blender']['rotation_matrix'] = R2.tolist()
sys.path.insert(0, __file__.rsplit('/projects/', 1)[0])
from ive.solve import _matrix_to_euler_xyz
c['blender']['rotation_euler'] = _matrix_to_euler_xyz(R2)
c.pop('opencv', None); c['note'] = f'orbit start: +{deg} deg about {pivot.tolist()} ends on {cam_end}'
json.dump(c, open(out, 'w'), indent=2)
