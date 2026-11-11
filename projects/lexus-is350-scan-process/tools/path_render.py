"""scan_render.py with a two-camera move: the shot starts EXACTLY on --camera and ends EXACTLY on --cam-b.
  blender -b -P path_render.py -- <all scan_render args incl. --camera A.json> --cam-b B.json [--path-ease ease_in_out]
Position moves on a sphere-ish path around the scan's bbox centre (azimuth / elevation / radius interpolated),
rotation is slerped, lens (log) and lens shift are interpolated - so a close start can swoop out to a solved end pose
(e.g. the listing's 360-viewer angle) while keeping both endpoints pixel-exact."""
import sys, json, math, importlib.util
argv = sys.argv; i = argv.index('--'); rest = argv[i + 1:]
def pop(flag, default=None):
    if flag in rest:
        k = rest.index(flag); v = rest[k + 1]; del rest[k:k + 2]; return v
    return default
cam_b = pop('--cam-b'); path_ease = pop('--path-ease', 'ease_in_out')
sys.argv = argv[:i + 1] + rest
spec = importlib.util.spec_from_file_location('scan_render', '/home/user/Illumaesthetic-Video-Editor/blender/scan_render.py')
sr = importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
from mathutils import Matrix, Vector

def animate(cam, args, lo, hi, f0, f1):
    B = json.load(open(cam_b)); cd = cam.data
    piv = (lo + hi) / 2
    MA = cam.matrix_world.copy(); la, qa = MA.translation.copy(), MA.to_quaternion()
    RB = Matrix(B['blender']['rotation_matrix']); lb = Vector(B['blender']['location']); qb = RB.to_quaternion()
    lensA, lensB = cd.lens, B['focal_mm'] * cd.sensor_width / B['sensor_width_mm']
    sA, sB = (cd.shift_x, cd.shift_y), (B.get('shift_x', 0.0), B.get('shift_y', 0.0))
    def sph(p):
        d = p - piv; r = d.length; return r, math.atan2(d.y, d.x), math.asin(max(-1, min(1, d.z / r)))
    rA, azA, elA = sph(la); rB, azB, elB = sph(lb)
    daz = (azB - azA + math.pi) % (2 * math.pi) - math.pi
    fwd = lambda q: q @ Vector((0, 0, -1))
    ta = la + fwd(qa) * (la - piv).length * 0.75; tb = lb + fwd(qb) * (lb - piv).length
    look = lambda p, tg: (tg - p).to_track_quat('-Z', 'Y')
    ra = look(la, ta).inverted() @ qa; rb = look(lb, tb).inverted() @ qb   # roll/residual at the ends
    if ra.dot(rb) < 0: rb.negate()
    cam.rotation_mode = 'QUATERNION'
    for f in range(f0, f1 + 1):
        t = sr.ease((f - f0) / max(1, f1 - f0), path_ease)
        r = rA * (rB / rA) ** t; az = azA + daz * t; el = elA + (elB - elA) * t
        cam.location = piv + Vector((r * math.cos(el) * math.cos(az), r * math.cos(el) * math.sin(az), r * math.sin(el)))
        tg = ta.lerp(tb, t)
        cam.rotation_quaternion = look(cam.location, tg) @ ra.slerp(rb, t)
        cd.lens = lensA * (lensB / lensA) ** t
        cd.shift_x = sA[0] + (sB[0] - sA[0]) * t; cd.shift_y = sA[1] + (sB[1] - sA[1]) * t
        for k in ('location', 'rotation_quaternion'): cam.keyframe_insert(k, frame=f)
        for k in ('lens', 'shift_x', 'shift_y'): cd.keyframe_insert(k, frame=f)
    bpy_scene = __import__('bpy').context.scene; bpy_scene.frame_set(f0)

sr.animate_camera = animate
sr.main()
