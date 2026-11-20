"""Blender: dump the car GLB's world-space triangles per top-level node to an .npz, for fast silhouette tests (silh.py).
    blender -b -P export_geo.py -- car.glb out.npz
"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a[0])
out = {}
def top(o):
    while o.parent is not None: o = o.parent
    return o.name
dg = bpy.context.evaluated_depsgraph_get()
for o in bpy.context.scene.objects:
    if o.type != "MESH": continue
    me = o.evaluated_get(dg).to_mesh(); me.calc_loop_triangles()
    v = np.array([o.matrix_world @ x.co for x in me.vertices], np.float32)
    t = np.array([lt.vertices[:] for lt in me.loop_triangles], np.int32)
    k = top(o); out.setdefault(k, []).append(v[t])
np.savez_compressed(a[1], **{k: np.concatenate(v) for k, v in out.items()})
for k, v in out.items():
    p = np.concatenate(v).reshape(-1, 3); print(k, len(p) // 3, p.min(0).round(3), p.max(0).round(3))
