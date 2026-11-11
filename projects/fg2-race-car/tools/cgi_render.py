"""Render Ecky's CGI .blend from a solved camera JSON, keeping his materials, world and ground.
blender -b "FG2 Race Lip.blend" -P cgi_render.py -- cam.json out.png [res_scale] [samples] [extra.blend:Object,...]"""
import bpy, json, sys
from mathutils import Matrix
a = sys.argv[sys.argv.index('--') + 1:]
cj = json.load(open(a[0])); out = a[1]
scale = float(a[2]) if len(a) > 2 else 1.0
spp = int(a[3]) if len(a) > 3 else 64
sc = bpy.context.scene
cd = bpy.data.cameras.new('ive_cam'); cam = bpy.data.objects.new('ive_cam', cd); sc.collection.objects.link(cam)
cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = cj['sensor_width_mm']; cd.lens = cj['focal_mm']
cd.shift_x = cj.get('shift_x', 0.0); cd.shift_y = cj.get('shift_y', 0.0); cd.clip_start = 0.05; cd.clip_end = 500
R = Matrix(cj['blender']['rotation_matrix']).to_4x4(); R.translation = cj['blender']['location']; cam.matrix_world = R
sc.camera = cam
W, H = cj['image_size']
sc.render.resolution_x, sc.render.resolution_y = round(W * scale), round(H * scale)
sc.render.resolution_percentage = 100
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = spp
sc.cycles.use_denoising = True; sc.cycles.use_adaptive_sampling = True
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out
# the 'scrap' collection is hidden in Ecky's viewport (old lip iterations): keep it out of the render too
for o in bpy.data.collections['scrap'].objects: o.hide_render = True
for o in bpy.data.objects:
    if o.type == 'MESH' and o.modifiers: print('MODS', o.name, [m.type for m in o.modifiers])
import os
# --- look fixes (logged in editlog): match Ecky's CGI->real reference
# 1) camera sees black behind the car, lighting/reflections still come from his sky
w = sc.world; nt = w.node_tree
outn = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]; src = outn.inputs[0].links[0].from_socket
lp = nt.nodes.new('ShaderNodeLightPath'); blk = nt.nodes.new('ShaderNodeBackground'); blk.inputs[0].default_value = (0, 0, 0, 1)
mix = nt.nodes.new('ShaderNodeMixShader')
nt.links.new(lp.outputs['Is Camera Ray'], mix.inputs[0]); nt.links.new(src, mix.inputs[1]); nt.links.new(blk.outputs[0], mix.inputs[2])
nt.links.new(mix.outputs[0], outn.inputs[0])
# 2) the lip is black on the real car: give it a black satin plastic
lipm = bpy.data.materials.new('ive_lip_black'); lipm.use_nodes = True
pb = lipm.node_tree.nodes['Principled BSDF']; pb.inputs['Base Color'].default_value = (0.012, 0.012, 0.013, 1); pb.inputs['Roughness'].default_value = 0.35
if os.environ.get('IVE_BLACK_LIP'): bpy.data.objects['Front Lip'].data.materials.clear(); bpy.data.objects['Front Lip'].data.materials.append(lipm)
# 3) missing image textures render magenta: drop them (tyre falls back to its dark base colour)
for m in bpy.data.materials:
    if m.node_tree:
        for n in list(m.node_tree.nodes):
            if n.type == 'TEX_IMAGE' and (n.image is None or not n.image.has_data):
                try:
                    n.image.reload() if n.image else None
                except Exception: pass
                if n.image is None or not n.image.has_data: m.node_tree.nodes.remove(n)
# 4) optional extra parts in the scan frame (mm STL): EXTRA=path.stl
import os
for x in filter(None, os.environ.get('IVE_EXTRA_STL', '').split(';')):
    bpy.ops.wm.stl_import(filepath=x); ob = bpy.context.selected_objects[0]; ob.scale = (0.001,) * 3
    ob.data.materials.clear(); ob.data.materials.append(lipm)
    for p in ob.data.polygons: p.use_smooth = True
for yv in filter(None, os.environ.get('IVE_UPRIGHTS', '').split(';')):
    # simple swan-neck stand-in: 8 mm plate from the trunk lid up into the blade (x 1.72-1.92 m, z 0.50-0.80 m)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1.82, float(yv), 0.68)); up = bpy.context.active_object
    up.scale = (0.16, 0.008, 0.36); up.data.materials.append(lipm)
if os.environ.get('IVE_TRANSPARENT'):
    sc.render.film_transparent = True
bpy.ops.render.render(write_still=True)
print('IVE_CGI', out)
