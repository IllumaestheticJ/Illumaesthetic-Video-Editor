"""CGI layer = Epsilon lookbook FG2 game model (eps-honda-civic-fg2-v10.glb) in Ecky's FG2 scene (his sky light + dark ground),
placed in the scan frame (game_to_scan.json), rendered from a solved camera JSON.
blender -b "FG2 Race Lip.blend" -P cgi_game_render.py -- cam.json out.png [res_scale] [samples]"""
import bpy, json, sys, os
from mathutils import Matrix
a = sys.argv[sys.argv.index('--') + 1:]; cj = json.load(open(a[0])); out = a[1]
scale = float(a[2]) if len(a) > 2 else 1.0; spp = int(a[3]) if len(a) > 3 else 64
GLB = '/home/user/media/fg2/cgi/epsilon/eps-honda-civic-fg2-v10.glb'
T = json.load(open('/home/user/media/work/fg2/scan/game_to_scan.json'))['body_to_scan']
sc = bpy.context.scene
# Ecky's scene keeps: world (sky), ground plane 'Plane.004'. Everything else (painted scan, his lip, tyres, scraps) off.
for o in bpy.data.objects:
    if o.name != 'Plane.004': o.hide_render = True
bpy.ops.import_scene.gltf(filepath=GLB)
imp = [o for o in bpy.context.selected_objects]
root = bpy.data.objects.new('eps_game_root', None); sc.collection.objects.link(root)
for o in imp:
    if o.parent is None: o.parent = root
    if o.name.startswith('part_tc_wing_kit'): o.hide_render = True   # rule: no wing unless configurator-exact
root.matrix_world = Matrix(T)
# paint: lookbook default for this car = Rallye Red R513 #c8102e gloss (also matches #806); lip finish = paint
def srgb(c): return ((c / 255) / 12.92) if c / 255 <= 0.04045 else (((c / 255) + 0.055) / 1.055) ** 2.4
red = (srgb(0xc8), srgb(0x10), srgb(0x2e), 1)
for m in bpy.data.materials:
    if not m.node_tree: continue
    p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if p is None: continue
    if m.name.startswith('paint'):
        p.inputs['Base Color'].default_value = red; p.inputs['Metallic'].default_value = 0.0; p.inputs['Roughness'].default_value = 0.18
        p.inputs['Coat Weight'].default_value = 1.0; p.inputs['Coat Roughness'].default_value = 0.03
    if m.name == 'rim_dark' and os.environ.get('IVE_SILVER_RIMS', '1') == '1':   # #806 runs silver Enkei RPF1s (photos, Ecky's CGI)
        p.inputs['Base Color'].default_value = (0.72, 0.73, 0.75, 1); p.inputs['Metallic'].default_value = 1.0; p.inputs['Roughness'].default_value = 0.28
# camera from solve
cd = bpy.data.cameras.new('ive_cam'); cam = bpy.data.objects.new('ive_cam', cd); sc.collection.objects.link(cam)
cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = cj['sensor_width_mm']; cd.lens = cj['focal_mm']; cd.clip_start = 0.05; cd.clip_end = 500
M = Matrix(cj['blender']['rotation_matrix']).to_4x4(); M.translation = cj['blender']['location']; cam.matrix_world = M; sc.camera = cam
W, H = cj['image_size']; sc.render.resolution_x, sc.render.resolution_y = round(W * scale), round(H * scale); sc.render.resolution_percentage = 100
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = spp; sc.cycles.use_denoising = True
sc.view_settings.view_transform = 'AgX' if 'AgX' in [i.identifier for i in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else sc.view_settings.view_transform
# camera rays see black behind the car; his sky still lights it (same as his CGI->real reference)
w = sc.world; nt = w.node_tree; o_ = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]; src = o_.inputs[0].links[0].from_socket
lp = nt.nodes.new('ShaderNodeLightPath'); bk = nt.nodes.new('ShaderNodeBackground'); bk.inputs[0].default_value = (0, 0, 0, 1)
mx = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); nt.links.new(src, mx.inputs[1]); nt.links.new(bk.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o_.inputs[0])
sc.render.image_settings.file_format = 'PNG'; sc.render.filepath = out
bpy.ops.render.render(write_still=True); print('IVE_CGI', out)
