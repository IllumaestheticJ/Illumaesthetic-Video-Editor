"""Re-render a scene saved by `ive render ... --save-blend` with a keyframed camera path.
Run: blender -b scene.blend --python campath.py -- path.json
path.json: {"out": dir, "fps": 15, "frames": N, "res_pct": 75, "samples": 12, "size": [1080,1920],
            "frames_only": [optional list of frame numbers for framing tests],
            "keys": [{"t": 0.0, "cam": "cam_B.json"} | {"t": 0.4, "loc": [x,y,z], "target": [x,y,z], "focal_mm": 28, "sensor": 20.25},
                     ... each key may carry "ease": "linear|ease_in|ease_out|ease_in_out" for the segment ENDING at it]}
Location/focal are interpolated per segment with that segment's ease, rotation by quaternion slerp."""
import sys, json, math, os
import bpy
from mathutils import Vector, Matrix, Quaternion
cfg = json.load(open(sys.argv[sys.argv.index('--') + 1]))
sc = bpy.context.scene; cam = sc.camera
W, H = cfg.get('size', [1080, 1920])
def pose(k):
    if 'cam' in k:
        c = json.load(open(k['cam'])); b = c['blender']
        R = Matrix(b['rotation_matrix']); loc = Vector(b['location'])
        loc = loc + Vector(k.get('offset', [0, 0, 0]))   # translate only: keeps the matched rotation
        return loc, R.to_quaternion(), c['focal_mm'], c['sensor_width_mm'], c.get('shift_x', 0.0), c.get('shift_y', 0.0)
    loc = Vector(k['loc']); d = (Vector(k['target']) - loc).normalized()
    q = d.to_track_quat('-Z', 'Y')
    return loc, q, k.get('focal_mm', 28.0), k.get('sensor', 20.25), 0.0, 0.0
def ease(t, kind):
    return {'ease_in': t * t, 'ease_out': 1 - (1 - t) ** 2, 'ease_in_out': t * t * (3 - 2 * t)}.get(kind, t)
keys = [(k['t'], pose(k), k.get('ease', 'ease_in_out')) for k in cfg['keys']]
fps, N = cfg['fps'], cfg['frames']
cam.animation_data_clear(); cam.data.animation_data_clear()
cam.data.sensor_fit = 'HORIZONTAL'
for f in range(1, N + 1):
    t = (f - 1) / fps
    i = max(j for j in range(len(keys)) if keys[j][0] <= t + 1e-9) if t >= keys[0][0] else 0
    if i == len(keys) - 1:
        L, Q, F, S, sx, sy = keys[i][1]
    else:
        (t0, p0, _), (t1, p1, e) = keys[i], keys[i + 1]
        u = ease(min(1, max(0, (t - t0) / (t1 - t0))), e)
        L = p0[0].lerp(p1[0], u); Q = p0[1].slerp(p1[1], u); F = p0[2] + (p1[2] - p0[2]) * u; S = p0[3]
        sx = p0[4] + (p1[4] - p0[4]) * u; sy = p0[5] + (p1[5] - p0[5]) * u
    cam.location = L; cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = Q
    cam.data.sensor_width = S; cam.data.lens = F; cam.data.shift_x = sx; cam.data.shift_y = sy
    cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_quaternion', frame=f)
    cam.data.keyframe_insert('lens', frame=f); cam.data.keyframe_insert('shift_x', frame=f); cam.data.keyframe_insert('shift_y', frame=f)
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.resolution_percentage = cfg.get('res_pct', 75)
sc.render.engine = 'CYCLES'; sc.cycles.samples = cfg.get('samples', 12); sc.cycles.use_denoising = True
sc.cycles.use_adaptive_sampling = True; sc.cycles.device = 'CPU'; sc.render.use_persistent_data = True
sc.render.fps = int(fps); sc.frame_start, sc.frame_end = 1, N
out = cfg['out']; os.makedirs(out, exist_ok=True)
only = cfg.get('frames_only')
if only:
    for f in only:
        sc.frame_set(f); sc.render.filepath = os.path.join(out, f"f_{f:04d}.png"); bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = os.path.join(out, 'f_'); bpy.ops.render.render(animation=True)
print('CAMPATH_DONE', out)
