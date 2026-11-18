"""Rear-view probe to place the Epsilon plate: prints the car bbox and writes an orthographic rear render with a grid in metres.
blender -b --factory-startup -P plate_probe.py -- <glb> <out.png> <hide,list>"""
import bpy, sys
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.import_scene.gltf(filepath=a[0])
ms = [o for o in bpy.data.objects if o.type == 'MESH']
for o in ms:
    if o.name.split('.')[0] in a[2].split(','): o.hide_render = True
pts = [o.matrix_world @ Vector(c) for o in ms if not o.hide_render for c in o.bound_box]
lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
print('BBOX', [round(v, 3) for v in lo], [round(v, 3) for v in hi], flush=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 8; sc.cycles.use_denoising = True
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
wg = [o for o in ms if 'wing' in o.name and not o.hide_render]
if wg: print('WING_Y', round((wg[0].matrix_world @ Vector(wg[0].bound_box[0])).y, 2), flush=True)
ax = 0 if (hi.x - lo.x) > (hi.y - lo.y) else 1   # length axis
for sgn in (1, -1):
    cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; cam.ortho_scale = 2.2
    co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
    loc = Vector((0, 0, 0.75)); loc[ax] = sgn * 10; co.location = loc
    co.rotation_euler = (Vector((0, 0, 0.75)) - loc).to_track_quat('-Z', 'Y').to_euler()
    sc.render.resolution_x, sc.render.resolution_y = 1100, 750
    sc.render.filepath = a[1].replace('.png', f'_{"p" if sgn > 0 else "n"}.png'); bpy.ops.render.render(write_still=True)
print('AXIS', ax, flush=True)
