"""BF 9 shot 1 plate (v0 stand-in for the BF 2/3 reuse): the website Integra DE GLB with the Epsilon kit, house silver
on black, low rear 3/4. One still; the push-in is done in the edit.

blender -b -P plate_integra.py -- --glb eps-acura-integra-de-v29.glb --out plate.png [--res 1080x1920 --samples 64]
"""
import sys, argparse, math
import bpy
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--glb", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--res", default="1080x1920")
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--az", type=float, default=215, help="camera azimuth deg around the car (0 = front)")
args = ap.parse_args(a)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=args.glb)

# kit as sold in BF 2: lip, skirts, spats, Sport Wing + trunk lip (duckbill). Flares are a separate product: hidden.
HIDE = {"body_duckbill_stock", "part_fender_flares", "interior"}
for o in list(bpy.data.objects):
    if o.name in HIDE:
        bpy.data.objects.remove(o, do_unlink=True)


def mat(name, col, rough, metal):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = col
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    return m


silver = mat("silver", (0.62, 0.63, 0.66, 1), 0.32, 0.85)
glass = mat("glass", (0.02, 0.02, 0.025, 1), 0.08, 0.0)
tyre = mat("tyre", (0.03, 0.03, 0.03, 1), 0.7, 0.0)
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
for o in meshes:
    m = glass if o.name == "glass" else silver
    o.data.materials.clear()
    o.data.materials.append(m)

# bbox in world
pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
c = (lo + hi) / 2
wing = bpy.data.objects["part_sport_wing"]
rear_sign = 1 if (wing.matrix_world.translation.y - c.y) > 0 else -1
print("REAR_SIGN", rear_sign, "bbox", lo, hi)

# world: black to camera, studio gradient in reflections
wd = bpy.data.worlds.new("w"); sc.world = wd; wd.use_nodes = True
nt = wd.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputWorld"); lp = nt.nodes.new("ShaderNodeLightPath")
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

tgt = bpy.data.objects.new("tgt", None); sc.collection.objects.link(tgt)
tgt.location = c + Vector((0, 0, -0.15))
r = max(hi - lo)


def light(name, off, energy, size, col=(1, 1, 1)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = energy; d.size = size; d.color = col
    ob = bpy.data.objects.new(name, d); sc.collection.objects.link(ob); ob.location = c + Vector(off)
    k = ob.constraints.new("TRACK_TO"); k.target = tgt


light("key", (r * 0.9, rear_sign * r * 0.9, r * 0.9), 90 * r * r, r)
light("rim", (-r * 0.8, -rear_sign * r * 1.0, r * 0.6), 120 * r * r, r * 0.6, (0.85, 0.92, 1.0))
light("top", (0, 0, r * 1.5), 70 * r * r, r * 1.5)

# camera: low rear 3/4 (az measured from the car's front direction)
front = Vector((0, -rear_sign, 0))
az = math.radians(args.az)
d = Vector((front.x * math.cos(az) - front.y * math.sin(az), front.x * math.sin(az) + front.y * math.cos(az), 0))
cd = bpy.data.cameras.new("cam"); cd.lens = 28; cd.shift_x = 0.04
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = c + d * 8.2 + Vector((0, 0, -c.z + 0.65))
k = cam.constraints.new("TRACK_TO"); k.target = tgt

W, H = map(int, args.res.split("x"))
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = args.samples; sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.filepath = args.out
bpy.ops.render.render(write_still=True)
