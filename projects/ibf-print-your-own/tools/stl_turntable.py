# Viewer-style turntable of the real Design Market STL (Workbench, satin grey on near-black).
# blender -b -P stl_turntable.py -- <stl> <outdir> <frames> [res_x res_y]
import bpy, sys, math
from mathutils import Vector
a = sys.argv[sys.argv.index("--")+1:]
stl, out, nf = a[0], a[1], int(a[2])
rx, ry = (int(a[3]), int(a[4])) if len(a) > 4 else (1080, 1920)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath=stl)
ob = bpy.context.selected_objects[0]
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
ob.location = (0, 0, 0)
dims = ob.dimensions; print("DIMS mm", tuple(dims), "tris", len(ob.data.polygons))
s = 1.0 / max(dims); ob.scale = (s, s, s)
bpy.ops.object.transform_apply(scale=True)
pivot = bpy.data.objects.new("pivot", None); bpy.context.scene.collection.objects.link(pivot)
ob.parent = pivot
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading
sh.light = 'STUDIO'; sh.color_type = 'SINGLE'; sh.single_color = (0.62, 0.63, 0.66)
sh.show_specular_highlight = True; sh.show_cavity = True; sh.cavity_type = 'BOTH'
sh.background_type = 'VIEWPORT'; sh.background_color = (0.006, 0.006, 0.008)
sc.display.render_aa = '16'
sc.render.resolution_x, sc.render.resolution_y = rx, ry
sc.render.film_transparent = False
sc.view_settings.view_transform = 'Standard'
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam)
cam.data.lens = 52; cam.data.shift_y = 0.06; cam.data.sensor_fit = 'HORIZONTAL'
cam.location = (0, -1.75, 0.5)
d = Vector((0, 0, 0)) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
sc.camera = cam
sc.frame_start, sc.frame_end = 1, nf
for f, ang in ((1, -70), (nf, -28)):
    pivot.rotation_euler = (0, 0, math.radians(ang)); pivot.keyframe_insert("rotation_euler", frame=f)
for fc in pivot.animation_data.action.fcurves if hasattr(pivot.animation_data.action, "fcurves") else []:
    for k in fc.keyframe_points: k.interpolation = 'LINEAR'
sc.render.filepath = out + "/f####"
sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(animation=True)
