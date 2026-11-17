# export the registered scan (GLB frame) and GLB body/trim as PLY for analysis
import bpy, sys, json
from mathutils import Matrix
a=sys.argv[sys.argv.index('--')+1:]; scan_blend, reg, glb, out_scan, out_glb = a[:5]
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(scan_blend) as (src,dst): dst.objects=list(src.objects)
for o in dst.objects: bpy.context.scene.collection.objects.link(o)
bpy.context.view_layer.update()
T=Matrix(json.load(open(reg))['matrix'])
for o in dst.objects:
    if o.parent is None: o.matrix_world = T @ o.matrix_world
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in dst.objects:
    if o.type=='MESH': o.select_set(True)
bpy.ops.wm.ply_export(filepath=out_scan, export_selected_objects=True, export_normals=False, export_uv=False, ascii_format=False, apply_modifiers=False, forward_axis='Y', up_axis='Z')
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.import_scene.gltf(filepath=glb)
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
    if o.type=='MESH' and o.name in tuple(a[5].split(',')) : o.select_set(True)
bpy.ops.wm.ply_export(filepath=out_glb, export_selected_objects=True, export_normals=False, export_uv=False, ascii_format=False, forward_axis='Y', up_axis='Z')
print('EXPORTED')
