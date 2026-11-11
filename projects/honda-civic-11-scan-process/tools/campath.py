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
        dist = Vector(c['opencv']['tvec']).length if 'opencv' in c else 5.0
        tgt = loc + (R @ Vector((0, 0, -1))) * dist                       # implied aim point (optical axis at object depth)
        return loc, R.to_quaternion(), c['focal_mm'], c['sensor_width_mm'], c.get('shift_x', 0.0), c.get('shift_y', 0.0), tgt
    loc = Vector(k['loc']); tgt = Vector(k['target']); d = (tgt - loc).normalized()
    q = d.to_track_quat('-Z', 'Y')
    return loc, q, k.get('focal_mm', 28.0), k.get('sensor', 20.25), 0.0, 0.0, tgt
def ease(t, kind):
    return {'ease_in': t * t, 'ease_out': 1 - (1 - t) ** 2, 'ease_in_out': t * t * (3 - 2 * t)}.get(kind, t)
keys = [(k['t'], pose(k), k.get('ease', 'ease_in_out'), k.get('aim', False)) for k in cfg['keys']]
fps, N = cfg['fps'], cfg['frames']
cam.animation_data_clear(); cam.data.animation_data_clear()
cam.data.sensor_fit = 'HORIZONTAL'
for f in range(1, N + 1):
    t = (f - 1) / fps
    i = max(j for j in range(len(keys)) if keys[j][0] <= t + 1e-9) if t >= keys[0][0] else 0
    if i == len(keys) - 1:
        L, Q, F, S, sx, sy, _ = keys[i][1]
    else:
        (t0, p0, _, _), (t1, p1, e, aim) = keys[i], keys[i + 1]
        u = ease(min(1, max(0, (t - t0) / (t1 - t0))), e)
        if aim:   # orbit: interpolate the aim point, slerp the view direction about it, lerp the radius; keep it framed
            T = p0[6].lerp(p1[6], u); o0, o1 = p0[0] - p0[6], p1[0] - p1[6]
            dq = o0.normalized().rotation_difference(o1.normalized())
            dirn = Quaternion().slerp(dq, u) @ o0.normalized()
            L = T + dirn * (o0.length + (o1.length - o0.length) * u)
            qa = (T - L).normalized().to_track_quat('-Z', 'Y')
            r0 = (p0[6] - p0[0]).normalized().to_track_quat('-Z', 'Y'); r1 = (p1[6] - p1[0]).normalized().to_track_quat('-Z', 'Y')
            c0 = r0.inverted() @ p0[1]; c1 = r1.inverted() @ p1[1]          # residual roll vs pure look-at at each key
            Q = qa @ c0.slerp(c1, u)
        else:
            L = p0[0].lerp(p1[0], u); Q = p0[1].slerp(p1[1], u)
        F = p0[2] + (p1[2] - p0[2]) * u; S = p0[3]
        sx = p0[4] + (p1[4] - p0[4]) * u; sy = p0[5] + (p1[5] - p0[5]) * u
    cam.location = L; cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = Q
    cam.data.sensor_width = S; cam.data.lens = F; cam.data.shift_x = sx; cam.data.shift_y = sy
    cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_quaternion', frame=f)
    cam.data.keyframe_insert('lens', frame=f); cam.data.keyframe_insert('shift_x', frame=f); cam.data.keyframe_insert('shift_y', frame=f)
# optional: retime the sweep shader's front (the 'Value' node keys) to finish by frame sweep_end
if cfg.get('sweep_end'):
    e = cfg['sweep_end']
    for m in bpy.data.materials:
        ad = m.node_tree.animation_data if m.node_tree else None
        if not ad or not ad.action: continue
        act = ad.action
        fcs = list(getattr(act, 'fcurves', []) or [])
        for layer in getattr(act, 'layers', []):          # Blender 4.4+/5 layered actions
            for strip in layer.strips:
                for cb in strip.channelbags: fcs += list(cb.fcurves)
        for fc in fcs:
            if 'nodes["Value"]' in fc.data_path:
                ks = fc.keyframe_points; f0, f1 = ks[0].co.x, ks[-1].co.x
                for k in ks:
                    k.co.x = 1 + (k.co.x - f0) / max(1e-6, f1 - f0) * (e - 1); k.handle_left.x = k.co.x; k.handle_right.x = k.co.x
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
