"""Project wrapper around blender/scan_render.py (shared code left untouched).
Adds lights inside enclosed scans (the SW20 Interior scan has sprayed glass + doors, so the cabin is a closed box
and the studio lights never reach it). Run:
  IVE_EXTRA_LIGHTS='[{"loc":[0,-0.2,0.9],"energy":150,"kind":"POINT","size":0.3}]' \
  blender -b -P tools/render_plus.py -- <scan_render args>
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "blender"))
import scan_render as sr
from mathutils import Vector

_orig = sr.studio_lights
_done = [False]
def studio_lights(lo, hi):
    _orig(lo, hi)
    if _done[0]:
        return
    _done[0] = True
    for i, L in enumerate(json.loads(os.environ.get("IVE_EXTRA_LIGHTS", "[]"))):
        d = sr.bpy.data.lights.new(f"extra{i}", L.get("kind", "POINT"))
        d.energy = L["energy"]; d.color = L.get("color", (1, 1, 1))
        if hasattr(d, "shadow_soft_size"): d.shadow_soft_size = L.get("size", 0.3)
        if L.get("kind") == "AREA": d.size = L.get("size", 0.5)
        o = sr.bpy.data.objects.new(f"extra{i}", d); sr.bpy.context.scene.collection.objects.link(o)
        o.location = Vector(L["loc"])
        if "target" in L:
            t = sr.bpy.data.objects.new(f"extra_t{i}", None); sr.bpy.context.scene.collection.objects.link(t); t.location = Vector(L["target"])
            c = o.constraints.new("TRACK_TO"); c.target = t; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
sr.studio_lights = studio_lights

_orig_anim = sr.animate_camera
def animate_camera(cam, args, lo, hi, f0, f1):
    """IVE_END_CAM=cam.json: ease from the (matched) start camera to this end camera - location lerp,
    rotation slerp (combined orbit + pull + rise in one move). IVE_EASE overrides the ease kind."""
    end = os.environ.get("IVE_END_CAM")
    if not end or f1 <= f0:
        return _orig_anim(cam, args, lo, hi, f0, f1)
    from mathutils import Matrix
    cj = json.load(open(end))
    M0 = cam.matrix_world.copy(); M1 = Matrix.Translation(Vector(cj["blender"]["location"])) @ Matrix(cj["blender"]["rotation_matrix"]).to_4x4()
    q0, q1 = M0.to_quaternion(), M1.to_quaternion(); p0, p1 = M0.translation.copy(), M1.translation.copy()
    kind = os.environ.get("IVE_EASE", args.ease)
    import math
    orbit = os.environ.get("IVE_PATH") == "orbit"  # cylindrical path about the car's Z axis (no cutting through it)
    lens0, lens1 = cam.data.lens, float(cj.get("focal_mm", cam.data.lens))
    if orbit:
        a0, a1 = math.atan2(p0.y, p0.x), math.atan2(p1.y, p1.x)
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        r0, r1 = math.hypot(p0.x, p0.y), math.hypot(p1.x, p1.y)
    for f in range(f0, f1 + 1):
        t = sr.ease((f - f0) / (f1 - f0), kind)
        if orbit:
            a = a0 + da * t; r = r0 + (r1 - r0) * t
            p = Vector((r * math.cos(a), r * math.sin(a), p0.z + (p1.z - p0.z) * t))
            # orientation: slerp, then yaw by the orbit angle offset so the car stays framed
            q = q0.slerp(q1, t)
        else:
            p = p0.lerp(p1, t); q = q0.slerp(q1, t)
        cam.matrix_world = Matrix.Translation(p) @ q.to_matrix().to_4x4()
        cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f)
        if abs(lens1 - lens0) > 1e-3:
            cam.data.lens = lens0 * (lens1 / lens0) ** t; cam.data.keyframe_insert("lens", frame=f)
    cam.matrix_world = M0; cam.data.lens = lens0
sr.animate_camera = animate_camera
sr.main()
