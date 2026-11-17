"""BF5 clearance-shelf-drop v0 shots (preview quality, EEVEE).

blender -b --factory-startup -P shots_v0.py -- --shot s2 --out DIR [--res 0.5]

Shots (local frames start at 1, 30 fps):
  s1  warehouse aisle POV push, light banks on, Del & Eps (placeholders)
  s2  Integra trunk lip on a pallet, Eps scan sweep, tag flip  -> ends on the 1:1 frame
  s3  DE4 Integra (lookbook GLB, silver) from the SAME camera, pull back
  s4  GR Corolla V1 lip pallet, Del, tag flip                 -> ends on the 1:1 frame
  s5  GR Corolla (lookbook GLB, silver) from the SAME camera, Eps micro mode, pull back
The 1:1 device: each lip sits on its pallet with the SAME world matrix it has on its car after one rigid transform T
(rotation about Z + translation); the car shot applies T to the whole car and starts from the shelf shot's last camera.
"""
import bpy, sys, math, json, argparse, random
from mathutils import Vector, Matrix, Euler

A = argparse.ArgumentParser()
A.add_argument("--shot", required=True)
A.add_argument("--out", required=True)
A.add_argument("--res", type=float, default=0.5)
A.add_argument("--frames", default="")
A.add_argument("--step", type=int, default=1)
args = A.parse_args(sys.argv[sys.argv.index("--") + 1:])
M = "/home/user/media/bf-clearance-shelf-drop"
GLB = {"integra": f"{M}/glb/eps-acura-integra-de-v29.glb", "grv1": f"{M}/glb/eps-toyota-gr-corolla-v23.glb"}
PART = {"integra": "part_duckbill", "grv1": "part_front_lip"}
LEN = {"s1": 77, "s2": 73, "s3": 73, "s4": 73, "s5": 74}   # frames; cuts on the bar kicks 2.56/5.00/7.44/9.88/12.32 s
FLIP = {"s2": 17, "s4": 18}                                  # local frame of the tag flip (snare 3.11 s / 8.01 s)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = 30
sc.frame_start, sc.frame_end = 1, LEN[args.shot]
sc.render.resolution_x, sc.render.resolution_y = int(1080 * args.res), int(1920 * args.res)
eng = {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}
sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in eng else "BLENDER_EEVEE"
try:
    sc.eevee.taa_render_samples = 24
    sc.eevee.use_shadows = True
except Exception:
    pass
sc.view_settings.view_transform = "AgX"
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = f"{args.out}/f_"


# ------------------------------------------------------------------ materials / world
def mat(name, color, rough=0.5, metal=0.0, emit=None, estr=0.0, alpha=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1)
        p.inputs["Emission Strength"].default_value = estr
    if alpha is not None:
        p.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    return m


SILVER = mat("silver", (0.62, 0.63, 0.66), 0.32, 0.85)
RACK = mat("rack", (0.10, 0.10, 0.11), 0.45, 0.6)
BOX = mat("box", (0.16, 0.16, 0.17), 0.8)
FLOOR = mat("floor", (0.02, 0.02, 0.022), 0.55)
WOOD = mat("pallet", (0.09, 0.09, 0.095), 0.85)
CYAN = mat("beam", (0.43, 0.76, 0.84), 0.5, emit=(0.43, 0.76, 0.84), estr=6.0, alpha=0.35)


ENV = 1.0


def world(bg=0.004):
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    lp = nt.nodes.new("ShaderNodeLightPath")
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    env = nt.nodes.new("ShaderNodeBackground"); env.inputs["Strength"].default_value = ENV
    nt.links.new(ramp.outputs[0], env.inputs["Color"])
    cam = nt.nodes.new("ShaderNodeBackground"); cam.inputs["Color"].default_value = (bg, bg, bg, 1)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(env.outputs[0], mix.inputs[1]); nt.links.new(cam.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])


def light(name, kind, loc, energy, size=2.0, target=None, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, kind); d.energy = energy; d.color = color
    if kind == "AREA":
        d.size = size
    if kind == "SPOT":
        d.spot_size = math.radians(40); d.spot_blend = 0.6
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc
    if target is not None:
        e = bpy.data.objects.new(name + "_t", None); sc.collection.objects.link(e); e.location = target
        c = o.constraints.new("TRACK_TO"); c.target = e
    return o


def box(name, loc, size, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = size; o.data.materials.append(m)
    return o


# ------------------------------------------------------------------ GLB import / 1:1 transform
def import_glb(key, keep):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=GLB[key])
    new = [o for o in bpy.data.objects if o not in before]
    out = {o.name: o for o in new if o.type == "MESH" and (keep is None or o.name in keep)}
    for o in out.values():
        mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
        o.data.materials.clear(); o.data.materials.append(SILVER)
        n = len(o.data.polygons)
        if n > 500000:                       # preview speed: website GLB bodies are 2-5M tris
            md = o.modifiers.new("dec", "DECIMATE"); md.ratio = 500000 / n
            dg = bpy.context.evaluated_depsgraph_get()
            me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
            o.modifiers.clear(); o.data = me
        for p in o.data.polygons:
            p.use_smooth = True
    drop = [o.name for o in new if o.name not in out]
    for nm in drop:
        if nm in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    return out


def bbox(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    return (Vector([min(p[i] for p in pts) for i in range(3)]), Vector([max(p[i] for p in pts) for i in range(3)]))


# per lip: yaw applied to the car, pallet position, final camera offset (from the lip centre) and lens
CFG = {
    "integra": dict(yaw=180 + 28, pallet=Vector((0.0, 6.0, 0.0)), cam=Vector((0.40, -2.05, 1.05)), lens=32),
    "grv1":    dict(yaw=-24,      pallet=Vector((0.0, 6.0, 0.0)), cam=Vector((0.30, -3.30, 1.15)), lens=30),
}
PALLET_TOP = 0.16


def lip_T(key, part):
    """T = translation to the pallet top @ yaw about the lip centre. Same T is used for the whole car."""
    lo, hi = bbox([part])
    c = (lo + hi) / 2
    P = CFG[key]["pallet"] + Vector((0, 0, PALLET_TOP + (c.z - lo.z) + 0.01))
    return Matrix.Translation(P) @ Matrix.Rotation(math.radians(CFG[key]["yaw"]), 4, "Z") @ Matrix.Translation(-c), P


def camera(name="cam", lens=30):
    d = bpy.data.cameras.new(name); d.lens = lens; d.sensor_fit = "VERTICAL"; d.sensor_height = 36
    d.clip_start = 0.02
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); sc.camera = o
    return o


def look(cam, loc, target, f):
    cam.location = loc
    d = (target - loc).normalized()
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f)


def ease_all(obj):
    if obj.animation_data and obj.animation_data.action:
        try:
            for fc in obj.animation_data.action.fcurves:
                for k in fc.keyframe_points:
                    k.interpolation = "BEZIER"; k.easing = "AUTO"
        except AttributeError:
            pass


# ------------------------------------------------------------------ warehouse
def warehouse(lamp_on_frames=None):
    random.seed(5)
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0)); bpy.context.object.data.materials.append(FLOOR)
    for side in (-1, 1):
        x0 = side * 2.4
        for y in [i * 2.7 - 16 for i in range(14)]:
            for dx in (0, side * 1.1):
                box("up", (x0 + dx, y, 3.0), (0.08, 0.08, 6.0), RACK)
            for z in (0.12, 1.6, 3.1, 4.6):
                box("beam", (x0 + side * 0.55, y + 1.35, z), (0.06, 2.7, 0.10), RACK)
                if z > 0.2 or random.random() < 0.5:
                    for k in range(random.randint(1, 3)):
                        s = (random.uniform(0.6, 0.95), random.uniform(0.5, 0.9), random.uniform(0.35, 0.9))
                        box("bx", (x0 + side * 0.55, y + 0.5 + k * 0.85, z + 0.06 + s[2] / 2), s, BOX)
    lamps = []
    for i, y in enumerate([-12, -8, -4, 0, 4, 8, 12, 16]):
        em = mat(f"lamp{i}", (1, 1, 1), emit=(1, 0.97, 0.92), estr=0.0)
        box("lamp", (0, y, 6.2), (0.4, 2.2, 0.05), em)
        L = light(f"L{i}", "AREA", (0, y, 6.0), 0.0, 2.2)
        L.rotation_euler = (0, 0, 0)
        lamps.append((em, L))
    on = lamp_on_frames or {}
    for i, (em, L) in enumerate(lamps):
        f_on = on.get(i, 1)
        p = em.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
        for f, v in ((1, 0.0 if f_on > 1 else 6.0), (max(1, f_on - 1), 0.0 if f_on > 1 else 6.0), (f_on, 6.0)):
            p.default_value = v; p.keyframe_insert("default_value", frame=f)
            L.data.energy = v * 25; L.data.keyframe_insert("energy", frame=f)
    return lamps


def pallet(loc):
    for k in range(5):
        box("slat", (loc.x - 0.5 + k * 0.25, loc.y, loc.z + 0.14), (0.14, 1.2, 0.03), WOOD)
    for k in (-0.5, 0, 0.5):
        box("block", (loc.x, loc.y + k, loc.z + 0.065), (1.2, 0.12, 0.11), WOOD)


def tag(key, loc, yaw, flip_f):
    """Two image planes back to back on a pivot; the pivot spins 180 deg about Z around flip_f."""
    piv = bpy.data.objects.new("tagpiv", None); sc.collection.objects.link(piv)
    piv.location = loc; piv.rotation_euler = (0, 0, yaw)
    for side, rz in (("front", 0), ("back", math.pi)):
        img = bpy.data.images.load(f"{M}/tex/tag_{key}_{side}.png")
        m = bpy.data.materials.new("tag_" + side); m.use_nodes = True
        nt = m.node_tree; p = nt.nodes["Principled BSDF"]
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = img
        nt.links.new(t.outputs["Color"], p.inputs["Base Color"])
        nt.links.new(t.outputs["Color"], p.inputs["Emission Color"]); p.inputs["Emission Strength"].default_value = 0.35
        p.inputs["Roughness"].default_value = 0.7
        bpy.ops.mesh.primitive_plane_add(size=1)
        o = bpy.context.object; o.scale = (0.30, 0.38, 1); o.data.materials.append(m)
        o.rotation_euler = (math.pi / 2, 0, rz); o.location = (0, 0.002 if side == "back" else -0.002, 0)
        o.parent = piv
    # string
    box("string", (loc.x, loc.y, loc.z + 0.19 + 0.6), (0.006, 0.006, 1.2), RACK)
    if flip_f:
        for f, a in ((1, yaw), (flip_f - 3, yaw), (flip_f + 3, yaw + math.pi), (flip_f + 8, yaw + math.pi + 0.08), (flip_f + 14, yaw + math.pi)):
            piv.rotation_euler = (0, 0, a); piv.keyframe_insert("rotation_euler", frame=f)
    return piv


def billboard(name, png, loc, height, cam, emissive=1.0):
    img = bpy.data.images.load(png)
    w, h = img.size
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = img
    nt.links.new(t.outputs["Color"], p.inputs["Base Color"]); nt.links.new(t.outputs["Alpha"], p.inputs["Alpha"])
    nt.links.new(t.outputs["Color"], p.inputs["Emission Color"]); p.inputs["Emission Strength"].default_value = emissive
    try:
        m.surface_render_method = "DITHERED"
    except Exception:
        pass
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    o.scale = (height * w / h, height, 1)
    bpy.ops.object.transform_apply(scale=True)
    for v in o.data.vertices:            # stand the plane up, feet at the origin
        v.co = Vector((v.co.x, 0, v.co.y + height / 2))
    o.location = loc
    c = o.constraints.new("LOCKED_TRACK"); c.target = cam; c.track_axis = "TRACK_NEGATIVE_Y"; c.lock_axis = "LOCK_Z"
    return o


def sweep(part, f0, f1):
    """Cyan scanner line sweeping across the lip before the flip."""
    lo, hi = bbox([part])
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.object; o.data.materials.append(CYAN)
    o.scale = (0.01, (hi.y - lo.y) + 0.25, 1); o.rotation_euler = (0, math.pi / 2, 0)
    o.scale = (hi.z - lo.z + 0.25, (hi.y - lo.y) + 0.25, 1)
    for f, x in ((f0 - 1, None), (f0, lo.x - 0.05), (f1, hi.x + 0.05), (f1 + 1, None)):
        if x is None:
            o.hide_render = True; o.keyframe_insert("hide_render", frame=f)
        else:
            o.hide_render = False; o.keyframe_insert("hide_render", frame=f)
            o.location = (x, (lo.y + hi.y) / 2, (lo.z + hi.z) / 2); o.keyframe_insert("location", frame=f)
    return o


# ------------------------------------------------------------------ shots
def shelf(key, shot):
    global ENV
    ENV = 0.25
    world(0.004)
    parts = import_glb(key, {PART[key]})
    part = parts[PART[key]]
    T, P = lip_T(key, part)
    part.matrix_world = T @ part.matrix_world
    warehouse()
    pallet(CFG[key]["pallet"])
    cam = camera(lens=CFG[key]["lens"])
    end = P + CFG[key]["cam"]
    d = (P - end).normalized()
    n = LEN[shot]
    look(cam, end - d * 3.2 + Vector((0, 0, 0.25)), P, 1)          # POV push in
    look(cam, end - d * 0.15, P, 14)
    look(cam, end, P, n)                                           # final = the 1:1 frame
    ease_all(cam)
    # tag hangs from the pallet's near corner, facing the camera
    side = Vector((d.y, -d.x, 0)).normalized()
    tloc = P + side * 0.30 + d * -0.10 + Vector((0, 0, 0.78))
    yaw = math.atan2(-d.x, d.y)
    tag(key, tloc, yaw, FLIP[shot])
    # key light from the camera side + rim, so the silver part reads in the dark aisle
    light("key", "AREA", end + Vector((0.8, 0.3, 1.6)), 90, 1.5, P)
    light("rim", "AREA", P + Vector((-1.2, 1.8, 1.4)), 160, 1.2, P, (0.85, 0.92, 1.0))
    light("spot", "SPOT", P + Vector((0, 0, 3.5)), 350, target=P)
    lip_c = bbox([part])
    if key == "integra":
        sweep(part, FLIP[shot] - 9, FLIP[shot] - 1)
        billboard("eps", f"{M}/chars/eps_34.png", Vector((*(P - side * 0.45 + d * 2.4).xy, 0)), 1.70, cam)
    else:
        billboard("del", f"{M}/chars/del_34.png", Vector((*(P - side * 0.70 + d * 2.2).xy, 0)), 1.85, cam)
    return cam


def car(key, shot):
    world(0.004)
    keep = None
    objs = import_glb(key, keep)
    for nm in list(objs):
        if nm.startswith("part_") and nm != PART[key] or nm.startswith("livery") or nm in ("underbody",):
            bpy.data.objects.remove(objs.pop(nm), do_unlink=True)
    if key == "integra" and "body_duckbill_stock" in objs:
        bpy.data.objects.remove(objs.pop("body_duckbill_stock"), do_unlink=True)   # the stock lip the part replaces
    for nm in [n for n in objs if n.startswith("glass")]:
        objs[nm].data.materials.clear(); objs[nm].data.materials.append(mat("glass", (0.02, 0.02, 0.025), 0.05, 0.0))
    part = objs[PART[key]]
    T, P = lip_T(key, part)
    for o in objs.values():
        o.matrix_world = T @ o.matrix_world
    cam = camera(lens=CFG[key]["lens"])
    start = P + CFG[key]["cam"]
    d = (P - start).normalized()
    n = LEN[shot]
    lo, hi = bbox(list(objs.values()))
    cc = (lo + hi) / 2
    look(cam, start, P, 1)                                          # identical to the shelf shot's last frame
    look(cam, start - d * 0.25, P + (cc - P) * 0.15, 10)
    pull = 3.4 if key == "integra" else 3.0
    look(cam, start - d * pull + Vector((0, 0, 0.55)), P + (cc - P) * 0.75, n)
    ease_all(cam)
    r = max(hi - lo)
    light("key", "AREA", cc + Vector((r * 0.9, -r * 0.9, r * 0.9)), 90 * r * r * 0.5, r, cc)
    light("rim", "AREA", cc + Vector((-r * 0.8, r * 1.0, r * 0.6)), 120 * r * r * 0.5, r * 0.6, cc, (0.85, 0.92, 1.0))
    light("top", "AREA", cc + Vector((0, 0, r * 1.5)), 70 * r * r * 0.5, r * 1.5, cc)
    light("lipkey", "AREA", start + Vector((0.8, 0.3, 1.6)), 260, 1.5, P)
    if key == "grv1":
        lo_p, hi_p = bbox([part])
        # Eps micro mode (~1:10) standing on the lip's outer end (the end nearer the camera side)
        ends = [Vector((lo_p.x + 0.12, (lo_p.y + hi_p.y) / 2, hi_p.z)), Vector((hi_p.x - 0.12, (lo_p.y + hi_p.y) / 2, hi_p.z))]
        tip = min(ends, key=lambda v: (v - start).length)
        billboard("eps_micro", f"{M}/chars/eps_front.png", tip - Vector((0, 0, 0.005)), 0.19, cam)
    return cam


def aisle():
    global ENV
    ENV = 0.25
    world(0.004)
    lamps = warehouse({0: 1, 1: 1, 2: 20, 3: 20, 4: 37, 5: 37, 6: 56, 7: 56})   # banks snap on with the snares
    cam = camera(lens=26)
    look(cam, Vector((0.0, -13.0, 1.6)), Vector((0, 10, 1.5)), 1)
    look(cam, Vector((0.0, -6.0, 1.6)), Vector((0, 14, 1.4)), LEN["s1"])
    ease_all(cam)
    pallet(Vector((0, 4.0, 0)))
    billboard("del", f"{M}/chars/del_front.png", Vector((-0.75, 2.2, 0)), 1.85, cam)
    billboard("eps", f"{M}/chars/eps_front.png", Vector((0.75, 2.4, 0)), 1.70, cam)
    # BLACK FRIDAY sign (in-world, emissive), hung over the aisle
    bpy.ops.object.text_add(location=(0, 9.5, 4.3), rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object; t.data.body = "BLACK FRIDAY"; t.data.align_x = "CENTER"; t.data.size = 0.75
    try:
        t.data.font = bpy.data.fonts.load("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf")
    except Exception:
        pass
    em = mat("sign", (1, 1, 1), emit=(1, 1, 1), estr=0.0)
    t.data.materials.append(em)
    p = em.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    for f, v in ((1, 0.0), (55, 0.0), (56, 12.0)):
        p.default_value = v; p.keyframe_insert("default_value", frame=f)
    light("fill", "AREA", Vector((0, -2, 3)), 150, 3, Vector((0, 2.3, 1)))
    return cam


if args.shot == "s1":
    aisle()
elif args.shot == "s2":
    shelf("integra", "s2")
elif args.shot == "s3":
    car("integra", "s3")
elif args.shot == "s4":
    shelf("grv1", "s4")
elif args.shot == "s5":
    car("grv1", "s5")
if args.frames:
    a, b = args.frames.split("-"); sc.frame_start, sc.frame_end = int(a), int(b)
sc.frame_step = args.step
sc.render.use_motion_blur = False
bpy.ops.render.render(animation=True)
