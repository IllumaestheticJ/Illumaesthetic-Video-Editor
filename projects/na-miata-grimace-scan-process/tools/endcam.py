"""End-on-listing camera: map a camera solved on the listing photo (W0xH0) into the 1080x1920 frame where
WebZoom shows that photo `box_w` px wide, centred; optionally pre-rotate it about Z through `pivot` by -deg
so an `--move orbit --move-amount deg` render ENDS exactly on the listing view.
usage: endcam.py cam_listing.json out.json --box-w 1078 --deg 25 --pivot x,y,z"""
import json, math, argparse, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('cam'); ap.add_argument('out'); ap.add_argument('--box-w', type=float, default=1078)
ap.add_argument('--deg', type=float, default=0); ap.add_argument('--pivot', default='0,0,0'); ap.add_argument('--box-cy', type=float, default=960)
a = ap.parse_args(); c = json.load(open(a.cam)); W0, H0 = c['image_size']; k = a.box_w / W0
out = dict(c); fx = c['fx_px'] * k
out.update({"image_size": [1080, 1920], "fx_px": fx, "focal_mm": fx * c['sensor_width_mm'] / 1080, "shift_x": 0.0,
            "shift_y": (a.box_cy - 960) / 1080})
if a.deg:
    th = math.radians(-a.deg); Rz = np.array([[math.cos(th), -math.sin(th), 0], [math.sin(th), math.cos(th), 0], [0, 0, 1]])
    p = np.array([float(v) for v in a.pivot.split(',')]); L = np.array(c['blender']['location']); M = np.array(c['blender']['rotation_matrix'])
    L2 = p + Rz @ (L - p); M2 = Rz @ M
    out['blender'] = {"location": L2.tolist(), "rotation_matrix": M2.tolist(), "rotation_euler": c['blender']['rotation_euler']}
json.dump(out, open(a.out, 'w'), indent=2); print('focal', out['focal_mm'])
