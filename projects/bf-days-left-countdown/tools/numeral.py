"""BF 9 countdown numeral: a silver numeral built top-to-bottom by a cyan scan sweep.

blender -b -P numeral.py -- --text 3 --out /path/frames/ --frames 149 --drop 80 [--res 1080x1920 --samples 24]

Local frame 0 = the first frame of shot 2. The scan line enters at the top on frame 0, the wireframe appears above it,
the solid silver trails it and finishes exactly on --drop (the music's drop). After the drop the numeral holds with a
slow push-in. The number is geometry from --text, never generated imagery.
"""
import sys, argparse, math
import bpy
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--text", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--frames", type=int, default=149)
ap.add_argument("--drop", type=int, default=80)
ap.add_argument("--res", default="1080x1920")
ap.add_argument("--samples", type=int, default=24)
ap.add_argument("--font", default="/usr/share/fonts/opentype/inter/InterDisplay-Black.otf")
ap.add_argument("--height", type=float, default=1.45, help="numeral height in m")
ap.add_argument("--still", type=int, default=-1, help="render only this local frame (test)")
args = ap.parse_args(a)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
W, H = map(int, args.res.split("x"))
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.fps = 30
sc.frame_start, sc.frame_end = 0, args.frames - 1
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = args.samples
sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"

# ---------------------------------------------------------------- numeral geometry
cu = bpy.data.curves.new("num", "FONT")
cu.body = args.text.replace("\\n", "\n")
cu.font = bpy.data.fonts.load(args.font)
cu.align_x, cu.align_y = "CENTER", "CENTER"
cu.extrude = 0.10
cu.bevel_depth = 0.012
cu.bevel_resolution = 3
cu.space_line = 0.85
o = bpy.data.objects.new("num", cu)
sc.collection.objects.link(o)
o.rotation_euler = (math.radians(90), 0, 0)  # stand up, face -Y
bpy.context.view_layer.objects.active = o
o.select_set(True)
bpy.ops.object.convert(target="MESH")
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
# scale to height and centre on origin
co = [v.co for v in o.data.vertices]
zmin, zmax = min(c.z for c in co), max(c.z for c in co)
xmin, xmax = min(c.x for c in co), max(c.x for c in co)
s = args.height / (zmax - zmin)
o.scale = (s, s, s)
bpy.ops.object.transform_apply(scale=True)
co = [v.co for v in o.data.vertices]
cx = (min(c.x for c in co) + max(c.x for c in co)) / 2
cz = (min(c.z for c in co) + max(c.z for c in co)) / 2
for v in o.data.vertices:
    v.co.x -= cx
    v.co.z -= cz
TOP, BOT = args.height / 2 + 0.05, -args.height / 2 - 0.05
bpy.ops.object.shade_auto_smooth() if hasattr(bpy.ops.object, "shade_auto_smooth") else None

# wireframe twin
w = o.copy(); w.data = o.data.copy(); w.name = "num_wire"
sc.collection.objects.link(w)
tri = w.modifiers.new("tri", "TRIANGULATE")
wm = w.modifiers.new("wire", "WIREFRAME"); wm.thickness = 0.0035; wm.use_replace = True


# ---------------------------------------------------------------- materials
def line_value(nt, name, keys):
    """Value node keyframed over local frames: keys = [(frame, z), ...]."""
    v = nt.nodes.new("ShaderNodeValue"); v.name = name
    for f, z in keys:
        v.outputs[0].default_value = z
        v.outputs[0].keyframe_insert("default_value", frame=f)
    return v


def z_coord(nt):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    return sep.outputs["Z"]


D = args.drop
lag = int(round(D * 0.30))
wire_keys = [(0, TOP), (D - lag, BOT)]          # wire line: top -> bottom, finishes before the drop
solid_keys = [(0, TOP + 0.5), (lag, TOP), (D, BOT)]  # solid trails and lands exactly on the drop

# solid silver (house look: satin metallic silver)
ms = bpy.data.materials.new("silver"); ms.use_nodes = True
nt = ms.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
p = nt.nodes.new("ShaderNodeBsdfPrincipled")
p.inputs["Base Color"].default_value = (0.62, 0.63, 0.66, 1)
p.inputs["Metallic"].default_value = 0.85
p.inputs["Roughness"].default_value = 0.30
tr = nt.nodes.new("ShaderNodeBsdfTransparent")
cmp = nt.nodes.new("ShaderNodeMath"); cmp.operation = "GREATER_THAN"
nt.links.new(z_coord(nt), cmp.inputs[0])
nt.links.new(line_value(nt, "solid_line", solid_keys).outputs[0], cmp.inputs[1])
mix = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(cmp.outputs[0], mix.inputs[0])
nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(p.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], out.inputs[0])
o.data.materials.clear(); o.data.materials.append(ms)

# wireframe: visible between the wire line and the solid line (cyan-white emission)
mw = bpy.data.materials.new("wire"); mw.use_nodes = True
nt = mw.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
em = nt.nodes.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (0.55, 0.85, 0.95, 1)
em.inputs["Strength"].default_value = 3.0
tr = nt.nodes.new("ShaderNodeBsdfTransparent")
z = z_coord(nt)
g1 = nt.nodes.new("ShaderNodeMath"); g1.operation = "GREATER_THAN"
nt.links.new(z, g1.inputs[0]); nt.links.new(line_value(nt, "wire_line", wire_keys).outputs[0], g1.inputs[1])
g2 = nt.nodes.new("ShaderNodeMath"); g2.operation = "LESS_THAN"
nt.links.new(z, g2.inputs[0]); nt.links.new(line_value(nt, "solid_line2", solid_keys).outputs[0], g2.inputs[1])
both = nt.nodes.new("ShaderNodeMath"); both.operation = "MULTIPLY"
nt.links.new(g1.outputs[0], both.inputs[0]); nt.links.new(g2.outputs[0], both.inputs[1])
mix = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(both.outputs[0], mix.inputs[0])
nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], out.inputs[0])
w.data.materials.clear(); w.data.materials.append(mw)

# scan beam: a thin glowing cyan bar riding the wire line, gone after it reaches the bottom
bpy.ops.mesh.primitive_plane_add(size=1)
beam = bpy.context.active_object; beam.name = "beam"
beam.scale = (2.4, 0.006, 1); beam.rotation_euler = (math.radians(90), 0, 0)
beam.location = (0, -0.25, TOP)
mb = bpy.data.materials.new("beam"); mb.use_nodes = True
nt = mb.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
em = nt.nodes.new("ShaderNodeEmission")
em.inputs["Color"].default_value = (0x6f / 255, 0xc3 / 255, 0xd6 / 255, 1)  # scanner light #6fc3d6
em.inputs["Strength"].default_value = 3.5
nt.links.new(em.outputs[0], out.inputs[0])
beam.data.materials.append(mb)
for f, zz in wire_keys:
    beam.location.z = zz; beam.keyframe_insert("location", frame=f)
beam.scale = (2.4, 0.006, 1); beam.keyframe_insert("scale", frame=D - lag)
beam.scale = (2.4, 0.0, 1); beam.keyframe_insert("scale", frame=D - lag + 3)

# ---------------------------------------------------------------- world, lights, camera
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True
nt = wd.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld")
lp = nt.nodes.new("ShaderNodeLightPath")
tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(tc.outputs["Generated"], sep.inputs[0])
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
nt.links.new(sep.outputs["Z"], ramp.inputs[0])
env = nt.nodes.new("ShaderNodeBackground"); env.inputs["Strength"].default_value = 1.2
nt.links.new(ramp.outputs[0], env.inputs["Color"])
bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs["Color"].default_value = (0, 0, 0, 1)
mx = nt.nodes.new("ShaderNodeMixShader")
nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
nt.links.new(env.outputs[0], mx.inputs[1]); nt.links.new(bg.outputs[0], mx.inputs[2])
nt.links.new(mx.outputs[0], out.inputs[0])


def light(name, loc, energy, size, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.size = size; d.color = color
    ob = bpy.data.objects.new(name, d); sc.collection.objects.link(ob); ob.location = loc
    c = ob.constraints.new("TRACK_TO"); c.target = o
    return d


key = light("key", (1.6, -2.2, 1.6), 260, 1.5)
light("rim", (-1.8, 1.2, 1.0), 200, 1.0, (0.85, 0.92, 1.0))
light("top", (0, -0.6, 2.4), 160, 2.0)
# drop accent: the key flares on the drop and settles
for f, e in [(D - 1, 260), (D, 700), (D + 8, 300)]:
    key.energy = e; key.keyframe_insert("energy", frame=f)

cd = bpy.data.cameras.new("cam"); cd.lens = 50
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
tgt = bpy.data.objects.new("tgt", None); sc.collection.objects.link(tgt)
tgt.location = (0.10, 0, -0.30)  # numeral sits in the upper part of the frame, left of centre (Eps on the right)
c = cam.constraints.new("TRACK_TO"); c.target = tgt
for f, d in [(0, 4.4), (D, 4.4), (args.frames - 1, 4.4 * 0.96)]:  # hold, then ~4 % push after the drop
    cam.location = (0.25, -d, -0.55); cam.keyframe_insert("location", frame=f)

sc.render.image_settings.file_format = "PNG"
if args.still >= 0:
    sc.frame_set(args.still)
    sc.render.filepath = args.out.rstrip("/") + f"/still_{args.still:04d}.png"
    bpy.ops.render.render(write_still=True)
else:
    sc.render.filepath = args.out.rstrip("/") + "/f_"
    bpy.ops.render.render(animation=True)
