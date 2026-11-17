"""BF civic-parts-rain v0 - the main take (shots 1+2): silver FE1 scan in Ron's design frame, lookbook parts raining like
bills, Ron's production parts seating on the measured hits, Del & Eps placeholders (model-sheet cut-outs on camera-facing
cards, clearly marked), one camera move from a front-left 3/4 to Ron's render-7 view (Camera.006 direction).

    blender -b -P take.py -- --out DIR [--res-pct 50] [--samples 12] [--frames a-b] [--still F] [--engine cycles|workbench]
    blender -b -P take.py -- --end-cam end_cam.json ...   (lens/shift for the 1:1 end pose, from fit_end.py)
Frames are 30 fps from the song start (music at 0). Frame (non-zero) Ron frame: m, front -Y, car's left +X, floor ~0.
"""
import json, math, os, random, sys
import bpy
from mathutils import Vector, Matrix, Euler

sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/blender")
import scan_render as sr  # noqa: E402  (house silver material + studio world)

M = "/home/user/media/bf-civic-parts-rain"
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def arg(k, d=None):
    return argv[argv.index(k) + 1] if k in argv else d
OUT = arg("--out", f"{M}/renders/take"); RES = int(arg("--res-pct", "50")); SPP = int(arg("--samples", "12"))
ENGINE = arg("--engine", "cycles"); STILL = arg("--still"); FR = arg("--frames")
END = json.load(open(arg("--end-cam"))) if arg("--end-cam") else {"lens": 105.0, "shift_x": 0.0, "shift_y": 0.0, "dist_scale": 1.0}

FPS = 30
def fr(t): return round(t * FPS)
# measured hits (decoded track, librosa onset peaks) - see editlog
T_LIP, T_SKIRT, T_REAR, T_WING, T_END = 10.957, 12.365, 14.495, 15.534, 16.251
T_CHARS = 5.622; T_TITLE_OUT = 9.9
F_END = fr(T_END)  # first frame of the next shot

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start = 0; sc.frame_end = F_END - 1
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, RES

def imp(path, name):
    bpy.ops.wm.stl_import(filepath=path)
    o = bpy.context.selected_objects[0]; o.name = name; return o

car = imp(f"{M}/kit/parts/car.stl", "car")
silver = sr.mat_silver(); car.data.materials.append(silver)
m_part = bpy.data.materials.new("part_white"); m_part.use_nodes = True
bs = m_part.node_tree.nodes["Principled BSDF"]
bs.inputs["Base Color"].default_value = (0.82, 0.83, 0.85, 1); bs.inputs["Roughness"].default_value = 0.38
# hero parts: Ron's production files (already in this frame)
SEAT = {"front_lip": (T_LIP, Vector((0, -1.6, 2.2))), "skirt_L": (T_SKIRT, Vector((1.4, 0, 2.0))),
        "skirt_R": (T_SKIRT, Vector((-1.4, 0, 2.0))), "rear_lip": (T_REAR, Vector((0, 1.6, 2.2))),
        "wing": (T_WING, Vector((0, 0.3, 2.6)))}
heroes = {}
for n, (t, off) in SEAT.items():
    o = imp(f"{M}/kit/parts/{n}.stl", n); o.data.materials.append(m_part)
    # origin at the part's centre so it tumbles about itself
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS"); o.select_set(False)
    home = o.location.copy(); heroes[n] = o
    rng = random.Random(hash(n) & 0xffff)
    f_seat = fr(t)
    # fall: from far above (out of frame) tumbling like the rain, straighten in the last 0.35 s, approach from outside
    keys = [(f_seat - 75, home + off + Vector((0, 0, 4.5)), (rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2))),
            (f_seat - 30, home + off, (rng.uniform(-.7, .7), rng.uniform(-.7, .7), rng.uniform(-.7, .7))),
            (f_seat - 10, home + off * 0.25 + Vector((0, 0, 0.05)), (0.05, -0.04, 0.03)),
            (f_seat, home, (0, 0, 0))]
    o.location = keys[0][1] + Vector((0, 0, 30)); o.keyframe_insert("location", frame=0)  # parked far above until its fall
    o.keyframe_insert("location", frame=keys[0][0] - 1)
    for f, loc, rot in keys:
        o.location = loc; o.rotation_euler = rot
        o.keyframe_insert("location", frame=f); o.keyframe_insert("rotation_euler", frame=f)
    o.rotation_euler = keys[0][2]; o.keyframe_insert("rotation_euler", frame=0)
    for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, "fcurves") else []:
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"

# camera: one move, front-left 3/4 -> left side -> Ron's render-7 view
cam_d = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.sensor_fit = "HORIZONTAL"; cam_d.sensor_width = 36.0; cam_d.clip_end = 200
TGT = Vector((0.0, 0.3, 0.62))
r6 = json.load(open(f"{M}/kit/ron_cam006.json")); M6 = Matrix(r6["matrix_world"])
p6 = M6.to_translation(); fwd6 = -(M6.to_3x3() @ Vector((0, 0, 1)))
# Ron's look-at point: closest point on his view ray to our target
t6 = (TGT - p6).dot(fwd6); look6 = p6 + fwd6 * t6
d6 = (p6 - look6).length * END["dist_scale"]
az6 = math.degrees(math.atan2((p6 - look6).x, -(p6 - look6).y)); el6 = math.degrees(math.asin((p6 - look6).z / (p6 - look6).length))
def pose(az, el, d, look):
    a, e = math.radians(az), math.radians(el)
    return look + d * Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
# (frame, az, elevation, lens, look-at, framing width at the car in m)
K = [(0, 24, 10, 35, TGT + Vector((0.1, -0.7, 0.7)), 4.3),
     (fr(T_LIP) - 20, 44, 8, 35, TGT + Vector((0.1, -0.9, 0.45)), 4.0),
     (fr(T_LIP) + 12, 56, 7, 38, TGT + Vector((0.1, -0.5, 0.35)), 4.9),
     (fr(T_SKIRT) + 8, 92, 6, 45, TGT + Vector((0.0, 0.15, 0.3)), 5.9),   # v0 check: car clipped at 5.0
     (fr(T_REAR) + 6, 140, 4, 70, look6, 5.4),
     (F_END - 8, az6, el6, END["lens"], look6, None)]
for f, az, el, lens, look, width in K:
    d = d6 if width is None else width * lens / 36.0
    cam.location = pose(az, el, d, look)
    cam.rotation_euler = (look - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = lens
    cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f); cam_d.keyframe_insert("lens", frame=f)
cam_d.shift_x = END["shift_x"]; cam_d.shift_y = END["shift_y"]
CAM_PATH = []
# exact end: Ron's own rotation (no re-aim), held to the cut
if "matrix" in END:
    cam.matrix_world = Matrix(END["matrix"])
else:
    cam.location = p6 if END["dist_scale"] == 1.0 else look6 + (p6 - look6) * END["dist_scale"]
    cam.rotation_euler = M6.to_euler()
cam_d.lens = END["lens"]
for f in (F_END - 8, F_END):
    cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f); cam_d.keyframe_insert("lens", frame=f)
# shift: 0 until the last approach, then the fitted end shift
for f, v in ((fr(T_REAR) + 6, (0.0, 0.0)), (F_END - 8, (END["shift_x"], END["shift_y"]))):
    cam_d.shift_x, cam_d.shift_y = v; cam_d.keyframe_insert("shift_x", frame=f); cam_d.keyframe_insert("shift_y", frame=f)

for f in range(0, F_END + 1, 6):
    sc.frame_set(f); CAM_PATH.append(cam.matrix_world.to_translation().copy())
# rain: lookbook GLB parts (eps-honda-civic-sedan-fe-facelift-v9), instanced, white satin
rain_src = {}
for n in ("front_lip", "rear_lip", "duckbill", "side_skirts"):
    o = imp(f"{M}/glb/fe_parts/{n}.stl", "src_" + n)
    if n == "side_skirts":  # keep one side only (a pair falling together reads as one odd part)
        import bmesh
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x < 0], context="VERTS"); bm.to_mesh(o.data); bm.free()
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS"); o.select_set(False)
    o.data.materials.append(m_part); o.hide_render = True; o.hide_viewport = True; o.location = (0, 0, -50)
    rain_src[n] = o.data
rng = random.Random(7)
N_RAIN = int(arg("--rain", "56"))
names = list(rain_src)
for i in range(N_RAIN):
    ob = bpy.data.objects.new(f"rain{i}", rain_src[names[i % len(names)]]); sc.collection.objects.link(ob)
    # ring around the car, clear of the body by >= 1 m (parts are up to 1.8 m long, they spin)
    while True:
        a = rng.uniform(0, 2 * math.pi); r = rng.uniform(3.0, 9.0)
        x, y = 0.0 + r * math.sin(a), 0.3 - r * math.cos(a)
        if abs(x) > 2.1 or y < -3.2 or y > 3.7:
            near_cam = min((Vector((x, y)) - Vector((c.x, c.y))).length for c in CAM_PATH)
            if near_cam > 3.4 and not (-3.4 < x < -0.6 and -4.3 < y < -1.9):  # clear of the lens and the mascots
                break
    period = rng.uniform(3.2, 4.6)          # seconds to fall z 7 -> -3
    phase = rng.uniform(0, period)
    spin = Vector((rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5), rng.uniform(-2.5, 2.5)))
    rock = rng.uniform(0.4, 0.9); sway = rng.uniform(0.2, 0.5)
    step = 3
    for f in range(0, F_END + step, step):
        t = f / FPS
        density = 0.55 + 0.45 * min(1, t / 6)   # builds through the intro
        u = ((t + phase) % period) / period
        z = 7.0 - 10.0 * u
        if i > N_RAIN * density and u > 0.02:
            z = 40  # not yet in the rain
        if t > T_REAR:  # the rain falls away after the rear lip lands; the 1:1 end frame is clean
            z -= 7.0 * (t - T_REAR) ** 2
        ob.location = (x + sway * math.sin(2.3 * t + i), y + sway * math.cos(1.9 * t + i), z)
        ob.rotation_euler = (rock * math.sin(3.1 * t + i) + spin.x * t * 0.3, rock * math.cos(2.7 * t + 2 * i) + spin.y * t * 0.3, spin.z * t)
        ob.keyframe_insert("location", frame=f); ob.keyframe_insert("rotation_euler", frame=f)
    ob.animation_data.action  # linear-ish is fine for v0
# thin out the rain after the drop: shrink everything that starts falling after T_LIP
for ob in [o for o in sc.objects if o.name.startswith("rain")]:
    pass

# Del & Eps PLACEHOLDERS: model-sheet cut-outs on cards that face the camera (owner's locked look); 1:1 scale
def card(png, name, height, loc):
    img = bpy.data.images.load(png); w = height * img.size[0] / img.size[1]
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; o.name = name
    o.scale = (w, 1, height); o.rotation_euler = (math.pi / 2, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for v in o.data.vertices: v.co.z += height / 2
    o.location = loc
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img
    em = nt.nodes.new("ShaderNodeEmission"); tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mix = nt.nodes.new("ShaderNodeMixShader")
    # scan-in reveal: visible below an animated height (Generated Z), cyan band at the edge
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    gate = nt.nodes.new("ShaderNodeMath"); gate.operation = "LESS_THAN"; nt.links.new(sep.outputs["Z"], gate.inputs[0])
    alpha = nt.nodes.new("ShaderNodeMath"); alpha.operation = "MULTIPLY"
    nt.links.new(tex.outputs["Alpha"], alpha.inputs[0]); nt.links.new(gate.outputs[0], alpha.inputs[1])
    band = nt.nodes.new("ShaderNodeMath"); band.operation = "COMPARE"; band.inputs[2].default_value = 0.03
    nt.links.new(sep.outputs["Z"], band.inputs[0])
    col = nt.nodes.new("ShaderNodeMix"); col.data_type = "RGBA"; col.inputs["B"].default_value = (0.43, 0.76, 0.84, 1)  # #6fc3d6
    nt.links.new(band.outputs[0], col.inputs["Factor"]); nt.links.new(tex.outputs["Color"], col.inputs["A"])
    nt.links.new(col.outputs["Result"], em.inputs["Color"]); em.inputs["Strength"].default_value = 1.0
    nt.links.new(alpha.outputs[0], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    o.data.materials.append(m)
    for node, f, v in ((gate, 0, -0.05), (gate, fr(T_CHARS), -0.05), (gate, fr(T_CHARS) + 15, 1.05)):
        node.inputs[1].default_value = v; node.inputs[1].keyframe_insert("default_value", frame=f)
    band.inputs[1].default_value = -1
    for f, v in ((0, -0.2), (fr(T_CHARS), -0.05), (fr(T_CHARS) + 15, 1.05), (fr(T_CHARS) + 16, 2.0)):
        band.inputs[1].default_value = v; band.inputs[1].keyframe_insert("default_value", frame=f)
    return o
CH = f"{M}/chars"
NOCH = True  # v0: mascots are 2D composites (see comp.py); the 3D cards stay off
del_ = card(f"{CH}/del_34_ph.png", "DEL_placeholder", 1.85 * 634 / 588, (-2.15, -2.75, 0.0))
eps = card(f"{CH}/eps_34_ph.png", "EPS_placeholder", 1.70 * 562 / 516, (-1.45, -3.45, 0.0))
if NOCH:
    del_.hide_render = eps.hide_render = True

# world + lights (house look: soft top/key, rim, black background)
sr.studio_world((0.004, 0.004, 0.005, 1), False)
root = bpy.data.objects.new("CAR_CENTRE", None); sc.collection.objects.link(root); root.location = TGT
def light(n, loc, e, size, col=(1, 1, 1)):
    d = bpy.data.lights.new(n, "AREA"); d.energy = e; d.size = size; d.color = col
    o = bpy.data.objects.new(n, d); sc.collection.objects.link(o); o.location = loc
    c = o.constraints.new("TRACK_TO"); c.target = root
light("key", (4.2, -4.6, 4.6), 1500, 4.5); light("rim", (-3.8, 5.2, 3.0), 1700, 2.8, (0.85, 0.92, 1.0)); light("top", (0, 0.3, 7.5), 1300, 7)
light("fill_left", (6.0, 3.0, 2.0), 500, 4)

sc.render.engine = "CYCLES" if ENGINE == "cycles" else "BLENDER_WORKBENCH"
if ENGINE == "cycles":
    sc.cycles.samples = SPP; sc.cycles.use_denoising = True; sc.cycles.device = "CPU"
    sc.render.use_persistent_data = False  # lessons: persistent data drops lights / black frames on animated scenes
    sc.cycles.max_bounces = 4
sc.render.use_motion_blur = ENGINE == "cycles" and arg("--mblur", "1") == "1"
sc.render.motion_blur_shutter = 0.35
try:
    sc.view_settings.view_transform = "AgX"
except Exception:
    pass
sc.render.image_settings.file_format = "PNG"
os.makedirs(OUT, exist_ok=True)
if arg("--save"):
    bpy.ops.wm.save_as_mainfile(filepath=arg("--save"))
if STILL is not None:
    for f in [int(x) for x in STILL.split(",")]:
        sc.frame_set(f); sc.render.filepath = f"{OUT}/still_{f:04d}.png"; bpy.ops.render.render(write_still=True)
else:
    a, b = (int(x) for x in FR.split("-")) if FR else (0, F_END - 1)
    sc.frame_start, sc.frame_end = a, b; sc.render.filepath = f"{OUT}/f_"
    bpy.ops.render.render(animation=True)
print("TAKE_DONE", F_END)
