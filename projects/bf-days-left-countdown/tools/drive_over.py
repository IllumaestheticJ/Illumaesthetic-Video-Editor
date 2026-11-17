"""BF 9 drive-over countdown: silver text lies on a black floor; the Epsilon-kitted Integra drives (or drifts) over it,
and the text behind the car has changed from --old to --new. The swap finishes on --drop (the music's drop).

blender -b -P drive_over.py -- --glb eps-acura-integra-de-v29.glb --mode drive|drift --old "BLACK FRIDAY\\nSALE" \
    --new "3 DAYS\\nLEFT" --out frames/ [--frames 208 --drop 139 --res 1080x1920 --samples 16 --still N]
The new text is geometry built from --new (computed from days_left by the caller), never generated imagery.
"""
import sys, argparse, math
import bpy
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--mode", choices=["drive", "drift"], default="drive")
ap.add_argument("--old", default="BLACK FRIDAY\\nSALE")
ap.add_argument("--new", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--frames", type=int, default=208)
ap.add_argument("--drop", type=int, default=139)
ap.add_argument("--res", default="1080x1920")
ap.add_argument("--samples", type=int, default=16)
ap.add_argument("--font", default="/usr/share/fonts/opentype/inter/InterDisplay-Black.otf")
ap.add_argument("--text-width", type=float, default=4.6, help="width of the wider text block on the floor (m)")
ap.add_argument("--still", type=int, default=-1)
args = ap.parse_args(a)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
W, H = map(int, args.res.split("x"))
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.fps = 30
sc.frame_start, sc.frame_end = 0, args.frames - 1
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
sc.cycles.samples = args.samples; sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
D = args.drop

# ---------------------------------------------------------------- the car (website GLB, Epsilon kit, house silver)
bpy.ops.import_scene.gltf(filepath=args.glb)
for n in ("body_duckbill_stock", "part_fender_flares", "interior"):
    o = bpy.data.objects.get(n)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)


def principled(name, col, rough, metal):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = col
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    return m


silver = principled("silver", (0.62, 0.63, 0.66, 1), 0.32, 0.85)
glass = principled("glass", (0.02, 0.02, 0.025, 1), 0.08, 0.0)
car_parts = [o for o in bpy.data.objects if o.type == "MESH"]
for o in car_parts:
    o.data.materials.clear(); o.data.materials.append(glass if o.name == "glass" else silver)

root = bpy.data.objects.new("car", None); sc.collection.objects.link(root)
for o in car_parts:
    o.parent = root
wheels = {n: bpy.data.objects[n] for n in ("wheel_FL", "wheel_FR", "wheel_RL", "wheel_RR")}
for w in wheels.values():
    w.rotation_mode = "XYZ"
R_WHEEL = 0.32
# GLB: front is -Y. Heading yaw h (deg) about Z: travel direction +X world when h = 90 (car nose to +X).


# ---------------------------------------------------------------- floor text: old and new, swapped by a wipe that follows the car
def floor_text(name, body, mat):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body.replace("\\n", "\n")
    cu.font = bpy.data.fonts.load(args.font)
    cu.align_x, cu.align_y = "CENTER", "CENTER"
    cu.extrude = 0.035; cu.bevel_depth = 0.006; cu.bevel_resolution = 2; cu.space_line = 0.9
    ob = bpy.data.objects.new(name, cu); sc.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.ops.object.convert(target="MESH")
    return ob


def wipe_material(name, keep_left):
    """Silver where (world X < wipe) == keep_left; transparent elsewhere. Wipe value is keyframed with the car."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    p = nt.nodes.new("ShaderNodeBsdfPrincipled")
    p.inputs["Base Color"].default_value = (0.72, 0.73, 0.76, 1)
    p.inputs["Metallic"].default_value = 0.85; p.inputs["Roughness"].default_value = 0.28
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(geo.outputs["Position"], sep.inputs[0])
    v = nt.nodes.new("ShaderNodeValue"); v.name = "wipe"
    cmp = nt.nodes.new("ShaderNodeMath"); cmp.operation = "LESS_THAN" if keep_left else "GREATER_THAN"
    nt.links.new(sep.outputs["X"], cmp.inputs[0]); nt.links.new(v.outputs[0], cmp.inputs[1])
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(cmp.outputs[0], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(p.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m, v


m_old, v_old = wipe_material("old_text", keep_left=False)   # old text survives ahead of (right of) the car
m_new, v_new = wipe_material("new_text", keep_left=True)    # new text appears behind (left of) the car
t_old = floor_text("t_old", args.old, m_old)
t_new = floor_text("t_new", args.new, m_new)
# both blocks share one scale (the wider sets it) so the type size matches
wid = []
for t in (t_old, t_new):
    xs = [v.co.x for v in t.data.vertices]; wid.append(max(xs) - min(xs))
s = args.text_width / max(wid)
for t, mat in ((t_old, m_old), (t_new, m_new)):
    t.scale = (s, s, s)
    bpy.context.view_layer.objects.active = t
    for o in bpy.context.selected_objects:
        o.select_set(False)
    t.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    t.data.materials.clear(); t.data.materials.append(mat)
    t.location = (0, 0, 0.001)  # lying flat on the floor, reading toward the camera (-Y)

# floor: black, a little gloss so the car sits on it
bpy.ops.mesh.primitive_plane_add(size=80)
floor = bpy.context.active_object
fm = principled("floor", (0.0, 0.0, 0.0, 1), 0.22, 0.0)
fm.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.12  # faint sharp reflection, black floor
floor.data.materials.append(fm)

# ---------------------------------------------------------------- car motion (path, heading, wheel spin), keyed per frame
x_in, x_drop = -9.5, 4.6     # car centre x: enters off-frame left, clears the text by the drop
f_in = D - 48 if args.mode == "drive" else D - 60
speed = (x_drop - x_in) / (D - f_in)  # m per frame (constant)


def pose(f):
    """returns (x, y, yaw_deg, steer_deg) for frame f."""
    x = x_in + speed * (f - f_in)
    if args.mode == "drive":
        return x, 0.0, 90.0, 0.0
    # drift: the car swings its tail out as it crosses: yaw builds to ~38 deg past travel, nose toward camera,
    # holds through the text, and partly recovers; front wheels counter-steer; slight arc in y.
    u = (f - f_in) / (D - f_in)  # 0 at entry, 1 at the drop
    ang = 38.0 * min(1.0, max(0.0, u / 0.35)) * (1 - 0.35 * max(0.0, u - 1.0))
    y = -0.35 * math.sin(math.pi * min(max(u, 0), 1.3) / 1.3)
    return x, y, 90.0 - ang, ang * 0.55


wipe_lag = 0.0  # the swap edge sits at the car's centre (hidden under the body)
dist = 0.0
prev = None
for f in range(args.frames):
    x, y, yaw, steer = pose(f)
    root.location = (x, y, 0); root.rotation_euler = (0, 0, math.radians(yaw))
    root.keyframe_insert("location", frame=f); root.keyframe_insert("rotation_euler", frame=f)
    if prev is not None:
        dist += math.hypot(x - prev[0], y - prev[1])
    prev = (x, y)
    spin = -dist / R_WHEEL
    for n, w in wheels.items():
        w.rotation_euler = (spin, 0, math.radians(-steer) if n.startswith("wheel_F") else 0)
        w.keyframe_insert("rotation_euler", frame=f)
    wv = max(-50.0, x - wipe_lag) if f >= f_in else -50.0
    for v in (v_old, v_new):
        v.outputs[0].default_value = wv
        v.outputs[0].keyframe_insert("default_value", frame=f)

# drift smoke (drift mode only): soft puffs behind the rear wheels, radial falloff x noise, low density
if args.mode == "drift":
    def smoke_mat():
        m = bpy.data.materials.new("smoke"); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        vol = nt.nodes.new("ShaderNodeVolumePrincipled")
        vol.inputs["Color"].default_value = (0.85, 0.87, 0.9, 1)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
        nt.links.new(tc.outputs["Object"], ln.inputs[0])
        fall = nt.nodes.new("ShaderNodeMapRange")
        fall.inputs["From Min"].default_value = 1.0; fall.inputs["From Max"].default_value = 0.0
        nt.links.new(ln.outputs["Value"], fall.inputs["Value"])
        pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 3.0
        nt.links.new(fall.outputs["Result"], pw.inputs[0])
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.2; nz.inputs["Detail"].default_value = 8.0
        nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        m1 = nt.nodes.new("ShaderNodeMath"); m1.operation = "MULTIPLY"
        nt.links.new(pw.outputs[0], m1.inputs[0]); nt.links.new(nz.outputs["Fac"], m1.inputs[1])
        dv = nt.nodes.new("ShaderNodeValue"); dv.name = "dens"
        m2 = nt.nodes.new("ShaderNodeMath"); m2.operation = "MULTIPLY"
        nt.links.new(m1.outputs[0], m2.inputs[0]); nt.links.new(dv.outputs[0], m2.inputs[1])
        nt.links.new(m2.outputs[0], vol.inputs["Density"])
        nt.links.new(vol.outputs[0], out.inputs["Volume"])
        return m, dv
    for i in range(12):
        fb = f_in + 6 + i * 4
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=16, ring_count=8)
        pf = bpy.context.active_object
        m, dv = smoke_mat(); pf.data.materials.append(m)
        x0, y0, yaw0, _ = pose(fb)
        hd = math.radians(yaw0 - 90)  # car forward (+X when yaw = 90)
        fwd = Vector((math.cos(hd), math.sin(hd), 0))
        side = (i % 2) * 2 - 1
        lat = Vector((-fwd.y, fwd.x, 0)) * 0.8 * side
        pf.location = Vector((x0, y0, 0.35)) - fwd * 1.5 + lat
        for ff, r, d in ((fb - 1, 0.01, 0.0), (fb, 0.5, 0.9), (fb + 20, 1.1, 0.45), (fb + 45, 1.6, 0.0)):
            pf.scale = (r, r, r * 0.7); pf.keyframe_insert("scale", frame=ff)
            dv.outputs[0].default_value = d; dv.outputs[0].keyframe_insert("default_value", frame=ff)
    sc.cycles.volume_step_rate = 4.0

# ---------------------------------------------------------------- world, lights, camera
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True
nt = wd.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld"); lp = nt.nodes.new("ShaderNodeLightPath")
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tc.outputs["Generated"], sep.inputs[0])
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
nt.links.new(sep.outputs["Z"], ramp.inputs[0])
env = nt.nodes.new("ShaderNodeBackground"); env.inputs["Strength"].default_value = 1.0
nt.links.new(ramp.outputs[0], env.inputs["Color"])
bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs["Color"].default_value = (0, 0, 0, 1)
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
nt.links.new(env.outputs[0], mx.inputs[1]); nt.links.new(bg.outputs[0], mx.inputs[2])
nt.links.new(mx.outputs[0], out.inputs[0])

tgt = bpy.data.objects.new("tgt", None); sc.collection.objects.link(tgt); tgt.location = (0, 0.2, 0.2)


def light(name, loc, energy, size, col=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.size = size; d.color = col
    ob = bpy.data.objects.new(name, d); sc.collection.objects.link(ob); ob.location = loc
    c = ob.constraints.new("TRACK_TO"); c.target = tgt
    return d


# light linking: the lights hit only the car and the text, so the black floor shows no light reflections
lit = bpy.data.collections.new("lit")
for o in car_parts + [t_old, t_new]:
    lit.objects.link(o)


def link(d):
    for ob in bpy.data.objects:
        if ob.data == d:
            ob.light_linking.receiver_collection = lit


light("key", (3.5, -4.0, 6.0), 1800, 4.0)
light("rim", (-4.0, 5.0, 3.5), 1500, 3.0, (0.85, 0.92, 1.0))
light("top", (0, 0, 8.0), 900, 6.0)
for d in bpy.data.lights:
    link(d)

cd = bpy.data.cameras.new("cam"); cd.lens = 32; cd.shift_x = 0.015  # centre the text on the safe box (x 484)
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
c = cam.constraints.new("TRACK_TO"); c.target = tgt
# high front angle (not straight overhead), slow push over the shot; a small kick on the drop
for f, (yy, zz) in ((0, (-6.2, 7.4)), (args.frames - 1, (-5.6, 6.7))):
    cam.location = (0, yy, zz); cam.keyframe_insert("location", frame=f)

sc.render.image_settings.file_format = "PNG"
if args.still >= 0:
    sc.frame_set(args.still)
    sc.render.filepath = args.out.rstrip("/") + f"/still_{args.still:04d}.png"
    bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = args.out.rstrip("/") + "/f_"
    bpy.ops.render.render(animation=True)
