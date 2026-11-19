"""BF 9 road scene (v1.0): a painted car drives (or drifts) down a road lane, seen from an overhead drone camera,
over road-painted text; the text behind the car has changed from --old to --new. Optionally named kit parts fall
off the car as it passes the text (the low-stock product, e.g. the Corolla hatch side skirts).

blender -b -P drive_road.py -- --glb CAR.glb --paint 0.5,0.005,0.01 --mode drive|drift|none \
    --old "BLACK\\nFRIDAY\\nSALE" --new "3 DAYS\\nLEFT" --out frames/ --frames 154 --hit 74 \
    [--fall part_side_skirts] [--hide a,b] [--res 720x1280 --samples 16 --still N]

User notes (2026-11-18): road background; colored car from the product's GLB; the part falls off when run over;
the car must pass over the WHOLE text (so every text line is narrower than the car); the stock card must be still.
--hit: frame on which the car's nose reaches the top of the text (put it on a beat).
"""
import sys, os, argparse, math
import bpy, bmesh
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "blender")); import ive_gpu  # noqa: E402  (GPU when present, else CPU)
from mathutils import Vector, Matrix

a = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--paint", default="0.012,0.05,0.28", help="linear RGB of the body paint")
ap.add_argument("--mode", choices=["drive", "drift", "none"], default="drive")
ap.add_argument("--old", required=True)
ap.add_argument("--new", default="")
ap.add_argument("--out", required=True)
ap.add_argument("--frames", type=int, default=154)
ap.add_argument("--hit", type=int, default=74)
ap.add_argument("--speed", type=float, default=0.30, help="m per frame (0.30 = 32 km/h)")
ap.add_argument("--fall", default="", help="comma list of part objects that fall off after the car passes the text")
ap.add_argument("--hide", default="", help="comma list of objects to remove (stock parts, unused kit)")
ap.add_argument("--res", default="720x1280")
ap.add_argument("--samples", type=int, default=16)
ap.add_argument("--font", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "../../../assets/fonts/akira/AkiraExpanded-SuperBold.otf"))
ap.add_argument("--text-width", type=float, default=1.70, help="widest text line (m); must stay under the car's width")
ap.add_argument("--stretch", type=float, default=1.9, help="road-marking stretch of the letters along the road")
ap.add_argument("--still", type=int, default=-1)
args = ap.parse_args(a)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
W, H = map(int, args.res.split("x"))
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.fps = 30
sc.frame_start, sc.frame_end = 0, args.frames - 1
sc.render.engine = "CYCLES"; ive_gpu.use(sc)
sc.cycles.samples = args.samples; sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.image_settings.file_format = "PNG"

# ---------------------------------------------------------------- car: the product's GLB, painted
bpy.ops.import_scene.gltf(filepath=args.glb)
for n in [s for s in args.hide.split(",") if s]:
    o = bpy.data.objects.get(n)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)
for o in list(bpy.data.objects):  # drop empties / cameras / lights that came with the GLB
    if o.type not in ("MESH",):
        bpy.data.objects.remove(o, do_unlink=True)


def principled(name, col, rough, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = col
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    p.inputs["Coat Weight"].default_value = coat
    p.inputs["Coat Roughness"].default_value = 0.04
    return m


pc = [float(v) for v in args.paint.split(",")]
paint = principled("car_paint", (*pc, 1), 0.28, 0.55, 1.0)
kit = paint  # parts in the body colour: a falling part reads clearly on the dark road
car_parts = [o for o in bpy.data.objects if o.type == "MESH"]
for o in car_parts:
    for i, ms in enumerate(o.material_slots):
        if ms.material and ms.material.name.startswith("paint"):
            o.material_slots[i].material = kit if o.name.startswith("part_") else paint

root = bpy.data.objects.new("car", None); sc.collection.objects.link(root)
root.rotation_mode = "XYZ"

# parts that fall off: split each into left/right halves, origin at its own centre, NOT parented (keyed in world)
fallers = []
for n in [s for s in args.fall.split(",") if s]:
    o = bpy.data.objects.get(n)
    if not o:
        continue
    car_parts.remove(o)
    halves = []
    for side in (-1, 1):
        h = o.copy(); h.data = o.data.copy(); h.name = f"{n}_{'L' if side > 0 else 'R'}"
        sc.collection.objects.link(h)
        bm = bmesh.new(); bm.from_mesh(h.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if (v.co.x * side) < 0], context="VERTS")
        bm.to_mesh(h.data); bm.free()
        c = sum((h.matrix_world @ v.co for v in h.data.vertices), Vector()) / max(1, len(h.data.vertices))
        h.data.transform(Matrix.Translation(-(h.matrix_world.inverted() @ c)))
        h.matrix_world = Matrix.Translation(c)
        h.rotation_mode = "XYZ"
        halves.append((h, c.copy(), side))
    bpy.data.objects.remove(o, do_unlink=True)
    fallers += halves

for o in car_parts:
    o.parent = root
wheels = {n: bpy.data.objects[n] for n in ("wheel_FL", "wheel_FR", "wheel_RL", "wheel_RR") if n in bpy.data.objects}
for w in wheels.values():
    w.rotation_mode = "XYZ"
R_WHEEL = 0.32

# ---------------------------------------------------------------- road: asphalt, lane edge lines, painted text
def asphalt():
    m = bpy.data.materials.new("asphalt"); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeNewGeometry")  # world position: no stretch from the plane's scale
    fine = nt.nodes.new("ShaderNodeTexNoise"); fine.inputs["Scale"].default_value = 320; fine.inputs["Detail"].default_value = 8
    big = nt.nodes.new("ShaderNodeTexNoise"); big.inputs["Scale"].default_value = 1.6; big.inputs["Detail"].default_value = 3
    for n_ in (fine, big):
        nt.links.new(tc.outputs["Position"], n_.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMath"); mix.operation = "MULTIPLY_ADD"   # fine grain + a faint large variation
    nt.links.new(big.outputs["Fac"], mix.inputs[0]); mix.inputs[1].default_value = 0.08
    nt.links.new(fine.outputs["Fac"], mix.inputs[2])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = (0.005, 0.005, 0.006, 1)
    ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (0.030, 0.030, 0.032, 1)
    nt.links.new(mix.outputs[0], ramp.inputs[0]); nt.links.new(ramp.outputs[0], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = 0.78
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.35; bump.inputs["Distance"].default_value = 0.002
    nt.links.new(fine.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], p.inputs["Normal"])
    return m


bpy.ops.mesh.primitive_plane_add(size=1)
road = bpy.context.active_object; road.scale = (14, 80, 1); road.name = "road"
road.data.materials.append(asphalt())
line_paint = principled("line_paint", (0.62, 0.62, 0.6, 1), 0.55)
for x in (-1.78, 1.78):  # solid lane edge lines: frame the lane at the left/right edges of the shot
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0, 0.0015))
    ln = bpy.context.active_object; ln.scale = (0.11, 80, 1); ln.data.materials.append(line_paint)

AXIS = "Y"


def wipe_material(name, keep_below):
    """Road paint where (world Y < wipe) == keep_below; transparent elsewhere. Wipe value follows the car."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    p = nt.nodes.new("ShaderNodeBsdfPrincipled")
    p.inputs["Base Color"].default_value = (0.8, 0.8, 0.78, 1); p.inputs["Roughness"].default_value = 0.5
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sep.inputs[0])
    v = nt.nodes.new("ShaderNodeValue"); v.name = "wipe"
    cmp = nt.nodes.new("ShaderNodeMath"); cmp.operation = "LESS_THAN" if keep_below else "GREATER_THAN"
    nt.links.new(sep.outputs[AXIS], cmp.inputs[0]); nt.links.new(v.outputs[0], cmp.inputs[1])
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(cmp.outputs[0], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(p.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m, v


def road_text(name, body, mat):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body.replace("\\n", "\n")
    cu.font = bpy.data.fonts.load(args.font)
    cu.align_x, cu.align_y = "CENTER", "CENTER"
    cu.extrude = 0.0025; cu.space_line = 1.05; cu.space_character = 1.15
    ob = bpy.data.objects.new(name, cu); sc.collection.objects.link(ob)
    for o in bpy.context.selected_objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.convert(target="MESH")
    for poly in ob.data.polygons:
        poly.use_smooth = False
    ob.data.materials.clear(); ob.data.materials.append(mat)
    return ob


# the car drives toward -Y: old text survives ahead of it (lower Y), new text appears behind it (higher Y)
m_old, v_old = wipe_material("old_text", keep_below=True)
m_new, v_new = wipe_material("new_text", keep_below=False)
texts = [road_text("t_old", args.old, m_old)]
if args.new:
    texts.append(road_text("t_new", args.new, m_new))
wid = max((max(v.co.x for v in t.data.vertices) - min(v.co.x for v in t.data.vertices)) for t in texts)
s = args.text_width / wid
for i, t in enumerate(texts):
    t.scale = (s, s * args.stretch, s)
    t.location = (0, 0, 0.003 + 0.002 * i)  # new text a hair above the old (no z-fighting)
text_top = max(max((t.matrix_world @ v.co).y for v in t.data.vertices) for t in texts) if texts else 0.6
bpy.context.view_layer.update()
text_top = max(max((t.matrix_world @ v.co).y for v in t.data.vertices) for t in texts)
text_bot = min(min((t.matrix_world @ v.co).y for v in t.data.vertices) for t in texts)
print("TEXT y", round(text_bot, 2), round(text_top, 2), "width", args.text_width)

# ---------------------------------------------------------------- motion
FRONT = 2.25          # car centre -> nose (m)
HIT = args.hit
y_hit = text_top + FRONT          # car centre when the nose touches the top of the text
SP = args.speed


def pose(f):
    """(x, y, yaw_deg, steer_deg) at frame f. yaw 0 = nose toward -Y (down the frame, toward the camera's bottom)."""
    if args.mode == "none":
        return 0.0, 300.0, 0.0, 0.0
    y = y_hit - SP * (f - HIT)
    if args.mode == "drive":
        return 0.0, y, 0.0, 0.0
    # drift: the car slides down the lane tail-out, swings through a flick as it crosses the text, counter-steering;
    # the swept width (~3.8 m at 32 deg) covers the whole text line
    u = (y_hit - y) / max(0.1, (text_top - text_bot) + 2 * FRONT)    # 0 at the text top, 1 when clear of it
    ang = 32.0 * math.sin(math.pi * (0.5 + 1.0 * u)) if -1.5 < u < 2.5 else 32.0 * math.copysign(1, math.sin(math.pi * (0.5 + u)))
    x = 0.35 * math.sin(math.pi * (0.5 + u))
    return x, y, ang, -ang * 0.6


dist = 0.0
prev = None
FALL_F = None
if fallers and args.mode != "none":
    # parts let go once the car's centre is past the bottom of the text (so they land below it, not on it)
    FALL_F = HIT + int(math.ceil((y_hit - text_bot) / SP))
for f in range(args.frames):
    x, y, yaw, steer = pose(f)
    root.location = (x, y, 0); root.rotation_euler = (0, 0, math.radians(yaw))
    root.keyframe_insert("location", frame=f); root.keyframe_insert("rotation_euler", frame=f)
    if prev is not None:
        dist += math.hypot(x - prev[0], y - prev[1])
    prev = (x, y)
    for n, w in wheels.items():
        w.rotation_euler = (dist / R_WHEEL, 0, math.radians(steer) if n.startswith("wheel_F") else 0)
        w.keyframe_insert("rotation_euler", frame=f)
    wv = (y if args.mode != "none" else 50.0)  # none: the wipe sits above everything, so the --old text shows whole
    wv = max(-50.0, min(50.0, wv))
    for v in (v_old, v_new):
        v.outputs[0].default_value = wv
        v.outputs[0].keyframe_insert("default_value", frame=f)

# fallers: ride with the car until FALL_F, then drop (gravity), tip outward flat, slide and stop (friction)
G = 9.81 / 900.0
for h, c, side in fallers:
    st = None
    for f in range(args.frames):
        x, y, yaw, _ = pose(min(f, FALL_F) if FALL_F is not None else f)
        R = Matrix.Rotation(math.radians(yaw), 3, "Z")
        if FALL_F is None or f <= FALL_F:
            loc = Vector((x, y, 0)) + R @ c
            rot = (0.0, 0.0, math.radians(yaw))
            if FALL_F is not None and f == FALL_F:
                x2, y2, _, _ = pose(f + 1)
                vel = Vector((x2 - x, y2 - y, 0)) + (R @ Vector((0.06 * side, 0, 0)))
                st = [loc.copy(), vel, 0.0]
        else:
            t = f - FALL_F
            p0, vel, _ = st
            k = 0.28   # friction decay per frame: ~1 m of slide
            travel = vel * ((1 - math.exp(-k * t)) / k)
            z = max(0.03, p0.z - 0.5 * G * t * t)
            loc = Vector((p0.x + travel.x, p0.y + travel.y, z))
            tip = min(1.0, t / 7.0)
            rot = (0.0, math.radians(-80 * side * tip), math.radians(yaw + 14 * side * (1 - math.exp(-0.08 * t))))
        h.location = loc; h.rotation_euler = rot
        h.keyframe_insert("location", frame=f); h.keyframe_insert("rotation_euler", frame=f)

# drift smoke from the rear wheels (drift only)
if args.mode == "drift":
    def smoke_mat():
        m = bpy.data.materials.new("smoke"); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial"); vol = nt.nodes.new("ShaderNodeVolumePrincipled")
        vol.inputs["Color"].default_value = (0.8, 0.8, 0.82, 1)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"; nt.links.new(tc.outputs["Object"], ln.inputs[0])
        fall = nt.nodes.new("ShaderNodeMapRange")
        fall.inputs["From Min"].default_value = 1.0; fall.inputs["From Max"].default_value = 0.0
        nt.links.new(ln.outputs["Value"], fall.inputs["Value"])
        pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 2.5
        nt.links.new(fall.outputs["Result"], pw.inputs[0])
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.5; nz.inputs["Detail"].default_value = 10.0
        nz.inputs["Distortion"].default_value = 1.5
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
        nt.links.new(pw.outputs[0], m1.inputs[0]); nt.links.new(nz.outputs["Fac"], m1.inputs[1])
        dv = nt.nodes.new("ShaderNodeValue")
        m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
        nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(dv.outputs[0], m2.inputs[1])
        nt.links.new(m2.outputs[0], vol.inputs["Density"]); nt.links.new(vol.outputs[0], out.inputs["Volume"])
        return m, dv
    import random
    rnd = random.Random(7)
    f0 = max(0, HIT - int(5.0 / SP))
    for i in range(12):  # soft tyre smoke: jittered, expands and clears within ~1 s so the new text stays readable
        fb = f0 + i * 3
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=16, ring_count=8)
        pf = bpy.context.active_object
        m, dv = smoke_mat(); pf.data.materials.append(m)
        x0, y0, yaw0, _ = pose(fb)
        R = Matrix.Rotation(math.radians(yaw0), 3, "Z")
        side = (i % 2) * 2 - 1
        pf.location = Vector((x0, y0, 0.25)) + R @ Vector((0.8 * side + rnd.uniform(-0.2, 0.2), 1.5 + rnd.uniform(0, 0.4), 0))
        pf.rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))
        for ff, r, d in ((fb - 1, 0.01, 0.0), (fb, 0.6, 0.9), (fb + 12, 1.3, 0.45), (fb + 28, 1.9, 0.0)):
            pf.scale = (r, r * 1.3, r * 0.5); pf.keyframe_insert("scale", frame=ff)
            dv.outputs[0].default_value = d; dv.outputs[0].keyframe_insert("default_value", frame=ff)
    sc.cycles.volume_step_rate = 4.0

# ---------------------------------------------------------------- world, lights, camera (overhead drone, telephoto)
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True
wd.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.022, 0.03, 1)
wd.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.15


def light(name, loc, energy, size, rot, col=(1, 1, 1), shape="RECTANGLE", size_y=None):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.color = col
    d.shape = shape; d.size = size; d.size_y = size_y or size
    ob = bpy.data.objects.new(name, d); sc.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = [math.radians(v) for v in rot]
    return ob


light("key", (0, -1.0, 9.0), 1500, 3.0, (8, 0, 0), size_y=12.0)                 # long soft strip down the lane
light("rimL", (-4.5, 2.0, 3.0), 900, 1.0, (0, -60, 0), (0.85, 0.9, 1.0), size_y=10.0)  # side strips: paint reflections
light("rimR", (4.5, 2.0, 3.0), 900, 1.0, (0, 60, 0), (1.0, 0.92, 0.85), size_y=10.0)

cd = bpy.data.cameras.new("cam"); cd.lens = 100; cd.sensor_fit = "HORIZONTAL"; cd.sensor_width = 36
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
TILT = 14.0   # degrees off vertical, looking slightly up the road (toward +Y): some depth on the car
DIST = 10.2   # 100 mm lens, 36 mm wide sensor -> ~3.65 m of road across the frame at the text
cam.rotation_euler = (math.radians(TILT), 0, 0)
cam.location = (0, -DIST * math.sin(math.radians(TILT)), DIST * math.cos(math.radians(TILT)))

if args.still >= 0:
    sc.frame_set(args.still)
    sc.render.filepath = args.out.rstrip("/") + f"/still_{args.still:04d}.png"
    bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = args.out.rstrip("/") + "/f_"
    sc.render.use_overwrite = False  # resume after a container restart
    bpy.ops.render.render(animation=True)
