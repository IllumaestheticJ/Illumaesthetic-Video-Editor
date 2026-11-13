"""MR2 v3 shot renderer (Blender, Cycles CPU): keyframed camera between arbitrary poses (solved cam JSONs or
loc/look-at keys) + per-part translate keys, house silver or clay look, persistent data OFF (lighting dropouts).

  blender -b -P tools/shot.py -- shot.json [--res-pct 25 --samples 6 --frames 0,32,64 --out DIR]

shot.json: {"objects": {"car": ".../topdown.blend", "ht": ".../ht_rear.blend"}, "out_frames": 129, "out": "/dir",
  "pivot": [x,y,z] (optional: camera location interpolates on a sphere about it, else straight line),
  "camera": [{"f": 0, "cam": "match/camB.json"}, {"f": 129, "loc": [..], "look": [..], "lens36": 39.1, "ease": "out"}],
  "parts": {"ht": [{"f": 0, "off": [0,0,0.08]}, {"f": 40, "off": [0,0,0.45], "ease": "out"}]},
  "look": "silver" | "clay", "clay": [r,g,b], "bg": [r,g,b]}
Key times are OUTPUT frames (30 fps); source frame i (rendered at 15 fps, file f_%04d = i+1) shows output frame 2i.
Renders ceil(out_frames/2)+3 source frames so minterpolate's dropped tail never reaches the cut."""
import json, math, os, sys
import bpy
from mathutils import Matrix, Vector, Quaternion

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "blender"))
import scan_render as sr  # noqa: E402

a = sys.argv[sys.argv.index("--") + 1:]
spec = json.load(open(a[0]))
opt = {a[i][2:]: a[i + 1] for i in range(1, len(a) - 1, 2)}
root = os.path.dirname(os.path.dirname(os.path.abspath(a[0]))) if not os.path.isabs(spec.get("base", "/")) else ""

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
objs = {}
for name, path in spec["objects"].items():
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = list(src.objects)
    grp = bpy.data.objects.new("grp_" + name, None); sc.collection.objects.link(grp)
    for o in dst.objects:
        if o is None: continue
        sc.collection.objects.link(o)
        if o.parent is None: o.parent = grp
    objs[name] = (grp, [o for o in dst.objects if o is not None and o.type == "MESH"])
bpy.context.view_layer.update()
car = objs[spec.get("light_on", list(objs)[0])][1]
lo, hi = sr.bbox(car)

look = spec.get("look", "silver")
bg = tuple(spec.get("bg", [0.004, 0.004, 0.005])) + (1.0,)
sr.studio_world(bg, False); sr.studio_lights(lo, hi)
if look == "clay":
    wb = sc.world.node_tree.nodes
    mat = sr.mat_clay()
    try:
        p = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"); c = spec.get("clay", [0.075, 0.078, 0.075])
        p.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1)
        for l in list(mat.node_tree.links):
            if l.to_socket == p.inputs["Base Color"]: mat.node_tree.links.remove(l)
    except StopIteration:
        pass
else:
    mat = sr.mat_silver()
for grp, meshes in objs.values():
    for o in meshes:
        o.data.materials.clear(); o.data.materials.append(mat)

cd = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.sensor_fit = "HORIZONTAL"; cd.sensor_width = 36; cd.clip_start = 0.01; cd.clip_end = 1000


def key_pose(k):
    if "cam" in k:
        cj = json.load(open(k["cam"]))
        R = Matrix(cj["blender"]["rotation_matrix"]); L = Vector(cj["blender"]["location"])
        return L, R.to_quaternion(), cj["focal_mm"] * 36.0 / cj["sensor_width_mm"]
    L = Vector(k["loc"]); fwd = (Vector(k["look"]) - L).normalized()
    right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd)
    R = Matrix((right, up, -fwd)).transposed()
    return L, R.to_quaternion(), k["lens36"]


def ease(u, kind):
    if kind == "lin": return u
    if kind == "out": return 1 - (1 - u) ** 2
    if kind == "in": return u * u
    return u * u * (3 - 2 * u)


def interp(keys, f, fn):
    if f <= keys[0]["f"]: return fn(keys[0], keys[0], 0)
    for k0, k1 in zip(keys, keys[1:]):
        if f <= k1["f"]:
            return fn(k0, k1, ease((f - k0["f"]) / (k1["f"] - k0["f"]), k1.get("ease", "inout")))
    return fn(keys[-1], keys[-1], 0)


piv = Vector(spec["pivot"]) if spec.get("pivot") else None
poses = {id(k): key_pose(k) for k in spec["camera"]}


def cam_at(k0, k1, u):
    L0, q0, f0 = poses[id(k0)]; L1, q1, f1 = poses[id(k1)]
    if piv is not None:
        d0, d1 = L0 - piv, L1 - piv
        r = d0.length + (d1.length - d0.length) * u
        L = piv + d0.normalized().slerp(d1.normalized(), u) * r
    else:
        L = L0.lerp(L1, u)
    return L, q0.slerp(q1, u), f0 + (f1 - f0) * u


W, H = spec.get("res", [1080, 1920])
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.resolution_percentage = int(opt.get("res-pct", spec.get("res_pct", 75)))
nout = spec["out_frames"]; nsrc = math.ceil(nout / 2) + 3
sc.frame_start, sc.frame_end = 1, nsrc
for i in range(nsrc):
    f = min(2 * i, nout) if spec.get("clamp", True) else 2 * i
    L, q, lens = interp(spec["camera"], f, cam_at)
    cam.matrix_world = Matrix.Translation(L) @ q.to_matrix().to_4x4(); cd.lens = lens
    cam.keyframe_insert("location", frame=i + 1); cam.rotation_mode = "QUATERNION"
    cam.rotation_quaternion = q; cam.keyframe_insert("rotation_quaternion", frame=i + 1)
    cd.keyframe_insert("lens", frame=i + 1)
    for name, keys in spec.get("parts", {}).items():
        off = interp(keys, f, lambda k0, k1, u: Vector(k0["off"]).lerp(Vector(k1["off"]), u))
        objs[name][0].location = off; objs[name][0].keyframe_insert("location", frame=i + 1)

sc.render.engine = "CYCLES"; sc.cycles.samples = int(opt.get("samples", spec.get("samples", 12)))
sc.cycles.use_denoising = True; sc.cycles.use_adaptive_sampling = True; sc.cycles.device = "CPU"
sc.render.use_persistent_data = False
try: sc.view_settings.view_transform = "AgX"
except TypeError: sc.view_settings.view_transform = "Filmic"
sc.view_settings.look = "None"
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"
out = opt.get("out", spec["out"]); os.makedirs(out, exist_ok=True)
frames = [int(v) for v in opt["frames"].split(",")] if "frames" in opt else None   # source indices (0-based)
rng = opt.get("range")
todo = frames if frames is not None else (range(*[int(v) for v in rng.split(",")]) if rng else range(nsrc))
for i in todo:
    fp = os.path.join(out, "f_%04d.png" % (i + 1))
    if os.path.exists(fp) and "force" not in opt: continue
    sc.frame_set(i + 1); sc.render.filepath = fp; bpy.ops.render.render(write_still=True)
print("IVE_SHOT_DONE", out, nsrc)
