"""CGI layer for any car: Epsilon lookbook model in the house CGI scene (Ecky's FG2 scene: his sky light + dark ground,
camera rays see black), only the chosen kit parts visible, paint from the photo car's colour.
blender -b "/home/user/media/fg2/cgi/FG2 Race Lip.blend" -P cgi_render.py -- CAR cam.json out.png [res_scale] [samples]"""
import bpy, json, sys, os
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index('--') + 1:]; car = a[0]; cj = json.load(open(a[1])); out = a[2]
scale = float(a[3]) if len(a) > 3 else 1.0; spp = int(a[4]) if len(a) > 4 else 48
cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cars.json')))[car]
sc = bpy.context.scene
for o in bpy.data.objects:
    if o.name != 'Plane.004': o.hide_render = True
bpy.ops.import_scene.gltf(filepath='/home/user/media/cars/' + cfg['glb'])
keep = set(cfg['kit']); zmin = 1e9
for o in bpy.context.selected_objects:
    base = o.name.split('.')[0]
    if base.startswith('part_') and base not in keep: o.hide_render = True
    if o.type == 'MESH' and not o.hide_render: zmin = min(zmin, min((o.matrix_world @ Vector(c)).z for c in o.bound_box))
bpy.data.objects['Plane.004'].location.z = zmin
def srgb(x): x /= 255; return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
hx = cfg['paint'][1].lstrip('#'); col = tuple(srgb(int(hx[i:i + 2], 16)) for i in (0, 2, 4)) + (1,)
for m in bpy.data.materials:
    if m.name.startswith('paint') and m.node_tree:
        p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if p:
            p.inputs['Base Color'].default_value = col; p.inputs['Roughness'].default_value = 0.2
            p.inputs['Metallic'].default_value = 0.35 if cfg['paint'][2] in ('pearl', 'metallic') else 0.0
            p.inputs['Coat Weight'].default_value = 1.0; p.inputs['Coat Roughness'].default_value = 0.03
cd = bpy.data.cameras.new('ive_cam'); cam = bpy.data.objects.new('ive_cam', cd); sc.collection.objects.link(cam)
cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = cj['sensor_width_mm']; cd.lens = cj['focal_mm']; cd.clip_start = 0.05; cd.clip_end = 500
M = Matrix(cj['blender']['rotation_matrix']).to_4x4(); M.translation = cj['blender']['location']; cam.matrix_world = M; sc.camera = cam
W, H = cj['image_size']; sc.render.resolution_x, sc.render.resolution_y = round(W * scale), round(H * scale); sc.render.resolution_percentage = 100
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = spp; sc.cycles.use_denoising = True
w = sc.world; nt = w.node_tree; o_ = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]; src = o_.inputs[0].links[0].from_socket
lp = nt.nodes.new('ShaderNodeLightPath'); bk = nt.nodes.new('ShaderNodeBackground'); bk.inputs[0].default_value = (0, 0, 0, 1)
mx = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); nt.links.new(src, mx.inputs[1]); nt.links.new(bk.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o_.inputs[0])
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out
bpy.ops.render.render(write_still=True); print('IVE_CGI', out)
