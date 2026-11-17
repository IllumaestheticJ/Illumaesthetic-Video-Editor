"""BF civic-parts-rain v0 - shots 4a/4b: the website lookbook car, kit paint-matched to the body, slow pan, painted parts
raining behind it (none in front of the text zone).

    blender -b -P cgi.py -- --car fe|fl --out DIR --frames N [--res-pct 50] [--samples 16]
FE = eps-honda-civic-sedan-fe-facelift-v9: front lip, side skirts, rear lip, Si Factory Duckbill wing (owner), Rallye Red R513.
FL = eps-honda-civic-hatch-fl-facelift-v8: front lip, side skirts, Sport Wing; NO rear lip (BF sheet: pre-order, "No deal"),
     Boost Blue Pearl B637P. Paint colours are approximations of the Honda colours (no paint codes -> RGB data in the repo).
"""
import math, os, random, sys
import bpy
from mathutils import Vector
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/blender")
import scan_render as sr  # noqa: E402

M = "/home/user/media/bf-civic-parts-rain"
argv = sys.argv[sys.argv.index("--") + 1:]
def arg(k, d=None): return argv[argv.index(k) + 1] if k in argv else d
CAR = arg("--car", "fe"); OUT = arg("--out"); N = int(arg("--frames", "60")); RES = int(arg("--res-pct", "50")); SPP = int(arg("--samples", "16"))
STILL = arg("--still")
GLB = {"fe": "eps-honda-civic-sedan-fe-facelift-v9", "fl": "eps-honda-civic-hatch-fl-facelift-v8"}[CAR]
PAINT = {"fe": (0.58, 0.004, 0.008, 1), "fl": (0.012, 0.075, 0.50, 1)}[CAR]   # linear RGB: Rallye Red / Boost Blue (approx.)
HIDE = {"fe": ["part_sport_wing", "body_rear_diffuser_stock", "trim_rear_diffuser_stock"],
        "fl": ["part_rear_lip"]}[CAR]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=f"{M}/glb/{GLB}.glb")
for o in list(sc.objects):
    if o.name in HIDE:
        o.hide_render = True
pm = bpy.data.materials["paint"]; b = pm.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = PAINT; b.inputs["Metallic"].default_value = 0.35; b.inputs["Roughness"].default_value = 0.28
try:
    b.inputs["Coat Weight"].default_value = 0.8; b.inputs["Coat Roughness"].default_value = 0.05
except KeyError:
    pass
# painted rain: the same part meshes, instanced
parts = [o for o in sc.objects if o.name.startswith("part_") and not o.hide_render]
cen = Vector((0, 0, 0.6))
cam_d = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.sensor_fit = "HORIZONTAL"; cam_d.sensor_width = 36; cam_d.lens = 40
side = 1 if CAR == "fe" else -1   # FE seen from the front-left (+X), FL from the front-right
az0, az1 = (28, 40) if CAR == "fe" else (-28, -40)
look = cen + Vector((0, -0.75, -0.15))   # v0 check: nose touched the frame edge with -0.2
def campos(az, d=5.6, el=7):
    a, e = math.radians(az), math.radians(el)
    return look + d * Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
for f, az in ((0, az0), (N - 1, az1)):
    cam.location = campos(az); cam.rotation_euler = (look - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f)
cam_d.shift_y = 0.24   # (+ = image content moves DOWN) car low in frame: the offer text sits in the black above it
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rain  # noqa: E402  (v0.2 screen-space rain: no part crosses a frame edge or pops in/out on screen)
srcs = []
for o in parts:   # the same part meshes; origin moved to their centre on copies of the data
    me = o.data.copy(); c = sum((v.co for v in me.vertices), Vector()) / len(me.vertices)
    for v in me.vertices: v.co -= c
    srcs.append(me)
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
n_rain = rain.build(sc, srcs, int(arg("--rain", "12")), N - 1, depth=(9.0, 15.0), xr=0.6,
                    keep_out=((-2.1, -3.4, -1.0), (2.1, 3.4, 2.5)), seed=3 if CAR == "fe" else 5, prefix="prain")
print("RAIN parts", n_rain)
sr.studio_world((0.004, 0.004, 0.005, 1), False)
root = bpy.data.objects.new("C", None); sc.collection.objects.link(root); root.location = cen
def light(n, loc, e, size, col=(1, 1, 1)):
    d = bpy.data.lights.new(n, "AREA"); d.energy = e; d.size = size; d.color = col
    o = bpy.data.objects.new(n, d); sc.collection.objects.link(o); o.location = loc
    c = o.constraints.new("TRACK_TO"); c.target = root
light("key", (4.2 * side, -4.6, 4.6), 1300, 4.5); light("rim", (-3.8 * side, 5.2, 3.0), 1600, 2.8, (0.85, 0.92, 1.0)); light("top", (0, 0, 7.5), 1100, 7)
sc.render.engine = "CYCLES"; sc.cycles.samples = SPP; sc.cycles.use_denoising = True; sc.render.use_persistent_data = False
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, RES
sc.render.fps = 30; sc.frame_start, sc.frame_end = 0, N - 1
sc.view_settings.view_transform = "AgX"
os.makedirs(OUT, exist_ok=True)
if STILL:
    sc.frame_set(int(STILL)); sc.render.filepath = f"{OUT}/still.png"; bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = f"{OUT}/f_"; bpy.ops.render.render(animation=True)
print("CGI_DONE")
