"""Camera after scan_render's --move pull/push: translate along the view axis by dist*amount (dist = camera -> look-at)."""
import json, sys
import numpy as np
c = json.load(open(sys.argv[1])); amt = float(sys.argv[3]); look = np.array([float(v) for v in sys.argv[4].split(',')])
R = np.array(c['blender']['rotation_matrix']); L = np.array(c['blender']['location'])
fwd = -R[:, 2]; d = np.linalg.norm(look - L)
c['blender']['location'] = (L - fwd * d * amt).tolist(); c.pop('opencv', None); c['note'] = f'pulled back {amt} x {d:.2f} m from {sys.argv[1]}'
json.dump(c, open(sys.argv[2], 'w'), indent=2)
