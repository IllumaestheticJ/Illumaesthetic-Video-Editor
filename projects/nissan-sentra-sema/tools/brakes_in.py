"""Import the designer's brake OBJ (GT-R calipers/rotors, hubs, Sentra adapters) and dump each object's world triangles
(raw OBJ frame, as Blender imports it with axis forward=Y up=Z so numbers equal the file's) to an npz + bbox report.
  blender -b -P brakes_in.py -- in.obj out.npz"""
import sys, bpy, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=a[0], forward_axis='Y', up_axis='Z')
out = {}
for o in bpy.context.scene.objects:
    if o.type != 'MESH': continue
    me = o.data; me.calc_loop_triangles(); n = len(me.vertices)
    co = np.empty(n * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    M = np.array(o.matrix_world); co = co @ M[:3, :3].T + M[:3, 3]
    tri = np.empty(len(me.loop_triangles) * 3, np.int32); me.loop_triangles.foreach_get('vertices', tri)
    out[o.name] = co[tri.reshape(-1, 3)].astype(np.float32)
    print('OBJ', o.name, len(tri) // 3, co.min(0).round(1), co.max(0).round(1))
np.savez(a[1], **out)
