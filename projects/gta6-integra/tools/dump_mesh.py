"""blender -b -P tools/dump_mesh.py -- car.glb out.npz : world-space triangles per top-level node (for tools/sil.py)."""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=a[0])
out = {}
for o in bpy.data.objects:
    if o.type != "MESH": continue
    top = o
    while top.parent: top = top.parent
    me = o.data; me.calc_loop_triangles()
    v = np.array([o.matrix_world @ x.co for x in me.vertices], np.float32)
    f = np.array([t.vertices[:] for t in me.loop_triangles], np.int32)
    if top.name in out:
        v0, f0 = out[top.name]; f = f + len(v0); v = np.vstack([v0, v]); f = np.vstack([f0, f])
    out[top.name] = (v, f)
np.savez_compressed(a[1], **{k + "|v": v for k, (v, f) in out.items()}, **{k + "|f": f for k, (v, f) in out.items()})
print("NODES", {k: len(f) for k, (v, f) in out.items()})
