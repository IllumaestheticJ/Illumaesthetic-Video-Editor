"""Derived cameras. listing: hero-crop solve -> 1080x1920 camera that matches WebZoom frame 0
(screenshot focus = hero centre, startScale s). orbitstart: rotate a camera about a Z pivot by -deg so an
`--move orbit --move-amount deg` render ENDS on it.
usage: cams.py listing cam_hero.json out.json --scale 1.3 | cams.py orbitstart cam.json out.json --deg 40 --pivot 0,0,0.55"""
import sys, json, math, argparse, numpy as np
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
from ive.solve import _matrix_to_euler_xyz, CV_TO_BLENDER_CAM
import cv2
ap = argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--scale', type=float, default=1.3); ap.add_argument('--deg', type=float, default=40)
ap.add_argument('--pivot', default='0,0,0.55')
a = ap.parse_args(); c = json.load(open(a.inp))
def finish(c, loc, R):
    c['blender'] = {'location': list(map(float, loc)), 'rotation_euler': _matrix_to_euler_xyz(R), 'rotation_matrix': R.tolist()}
    Rw2c = (R @ CV_TO_BLENDER_CAM).T; c['opencv'] = {'rvec': cv2.Rodrigues(Rw2c)[0].ravel().tolist(), 'tvec': (-Rw2c @ loc).tolist()}
    return c
if a.mode == 'listing':
    fx = c['fx_px'] * a.scale; c['image_size'] = [1080, 1920]; c['fx_px'] = fx
    c['sensor_width_mm'] = 36.0; c['focal_mm'] = fx / 1080 * 36.0; c['shift_x'] = c['shift_y'] = 0.0
    c['note'] = f'hero-crop solve scaled x{a.scale}; matches WebZoom frame 0 with focus = hero centre'
else:
    p = np.array([float(v) for v in a.pivot.split(',')]); t = math.radians(-a.deg)
    Rz = np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
    loc = np.array(c['blender']['location']); R = np.array(c['blender']['rotation_matrix'])
    c = finish(c, p + Rz @ (loc - p), Rz @ R)
json.dump(c, open(a.out, 'w'), indent=2)
