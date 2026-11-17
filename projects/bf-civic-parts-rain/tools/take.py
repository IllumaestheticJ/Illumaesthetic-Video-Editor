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
# v0.4 (owner: first scene too long; parts snap on the beat): the song now starts at MUSIC_START s, so these are VIDEO times.
# Kit parts land on four consecutive measured hits of the post-drop grid (song 11.320, 12.365, 13.436, 14.495; ~1.06 s apart),
# the 1:1 cut to render 7 is the next hit (song 15.534).
MUSIC_START = 9.25
T_LIP, T_SKIRT, T_REAR, T_WING, T_END = (t - MUSIC_START for t in (11.320, 12.365, 13.436, 14.495, 15.534))
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
# hero parts: Ron's production files (already in this frame). Animated after the camera exists (falls are checked
# against the frame and the scan): owner on v0 - no "homing", they must just fall onto the car as if that was the plan.
SEAT = {"front_lip": (T_LIP, Vector((0, -1, 0))), "skirt_L": (T_SKIRT, Vector((1, 0, 0))), "skirt_R": (T_SKIRT, Vector((-1, 0, 0))),
        "rear_lip": (T_REAR, Vector((0, 1, 0))), "wing": (T_WING, Vector((0, 0, 0)))}
heroes = {}
for n in SEAT:
    o = imp(f"{M}/kit/parts/{n}.stl", n); o.data.materials.append(m_part); heroes[n] = o

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
     (max(fr(T_LIP) - 20, 30), 16, 9, 35, TGT + Vector((0.0, -0.9, 0.45)), 4.3),   # v0.2: near-frontal so the lip drops in from the top
     (fr(T_LIP) + 12, 22, 8, 38, TGT + Vector((0.0, -0.6, 0.35)), 4.7),
     ((fr(T_LIP) + 12 + fr(T_SKIRT) + 8) // 2, 57, 7, 42, TGT + Vector((0.0, -0.2, 0.3)), 5.8),   # arc key: a 22->92 deg chord cropped the nose
     (fr(T_SKIRT) + 8, 92, 6, 45, TGT + Vector((0.0, 0.15, 0.3)), 5.9),
     (fr(T_SKIRT) + 8 + (fr(T_REAR) - fr(T_SKIRT) - 2) // 3, 118, 6, 50, TGT + Vector((0.0, 0.3, 0.25)), 6.0),   # arc keys (a straight
     (fr(T_SKIRT) + 8 + 2 * (fr(T_REAR) - fr(T_SKIRT) - 2) // 3, 142, 5, 55, TGT + Vector((0.0, 0.45, 0.2)), 5.7),   # chord cut the tail)
     (fr(T_REAR) + 6, 165, 5, 60, TGT + Vector((0.0, 0.6, 0.2)), 5.2),   # v0.2: nearly behind so the rear lip drops in from the top
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rain, falls  # noqa: E402
# rain: lookbook GLB parts (eps-honda-civic-sedan-fe-facelift-v9), white satin, screen-space falls behind the car
rain_src = []
for n in ("front_lip", "rear_lip", "duckbill", "side_skirts"):
    o = imp(f"{M}/glb/fe_parts/{n}.stl", "src_" + n)
    if n == "side_skirts":  # keep one side only (a pair falling together reads as one odd part)
        import bmesh
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.x < 0], context="VERTS"); bm.to_mesh(o.data); bm.free()
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS"); o.select_set(False)
    o.data.materials.append(m_part); o.hide_render = True; o.hide_viewport = True; o.location = (0, 0, -50)
    rain_src.append(o.data)
KEEP = ((-2.9, -3.9, -1.8), (2.9, 4.5, 3.3))   # Ron-frame car bbox + 1.8 m (bigger parts)
n_rain = rain.build(sc, rain_src, int(arg("--rain", "30")), F_END - 1, depth=(8.0, 14.0), xr=0.5, fall=(2.2, 3.2),
                    gap=(0.1, 0.8), y_edge=1.42, keep_out=KEEP, t_last_end=T_END - 0.05, seed=7, scale=1.6)
print("RAIN parts", n_rain)
# hero falls (tools/falls.py): straight line, constant orientation, gravity, steepest line that clears the scan
for n, (t, side) in SEAT.items():
    info = falls.animate(sc, heroes[n], car, fr(t), side, F_END - 1, name=n)
    print("FALL", n, info)

# v0.4 layers (owner: falling parts a bit blurred): --layer car = no rain; --layer rain = rain only, car + kit as
# holdout on a transparent film (blurred and laid over the car layer in comp.py)
LAYER = arg("--layer", "both")
RAIN_OBS = [o for o in sc.objects if o.name.startswith("rain")]
if LAYER == "car":
    for o in RAIN_OBS: o.hide_render = True
elif LAYER == "rain":
    for o in [car] + list(heroes.values()): o.is_holdout = True
    sc.render.film_transparent = True

# world + lights (house look: soft top/key, rim, black background)
sr.studio_world((0.004, 0.004, 0.005, 1), LAYER == "rain")
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
