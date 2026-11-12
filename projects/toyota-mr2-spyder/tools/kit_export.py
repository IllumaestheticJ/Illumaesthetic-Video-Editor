"""Blender: import the Epsilon lookbook GLB (eps-toyota-mr2-spyder-v19.glb) and write one binary STL per mesh object
(GLB->Blender frame: metres, nose -Y, z up). Wheels are also split by material (rim / tyre / brake).

    blender -b -P kit_export.py -- model.glb outdir
"""
import os, sys
import bpy, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stlio import DT, write  # noqa: E402

glb, out = sys.argv[sys.argv.index("--") + 1:][:2]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
dg = bpy.context.evaluated_depsgraph_get()
groups = {}
for o in bpy.context.scene.objects:
    if o.type != "MESH":
        continue
    mats = [s.material.name if s.material else "" for s in o.material_slots]
    me = o.evaluated_get(dg).to_mesh(); me.calc_loop_triangles()
    co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co)
    M = np.array(o.matrix_world, np.float64)
    co = co.reshape(-1, 3).astype(np.float64) @ M[:3, :3].T + M[:3, 3]
    tri = np.empty(len(me.loop_triangles) * 3, np.int32); me.loop_triangles.foreach_get("vertices", tri)
    mi = np.empty(len(me.loop_triangles), np.int32); me.loop_triangles.foreach_get("material_index", mi)
    v = co[tri.reshape(-1, 3)]
    g = "hardtop_window" if o.name == "hardtop_rear_window" else o.name
    groups.setdefault(g, []).append(v)
    if o.name.startswith("wheel_"):
        for k, m in enumerate(mats):
            sub = "rim" if m.startswith("rim") else "tyre" if m == "rubber" else "brake"
            groups.setdefault(f"{o.name}_{sub}", []).append(v[mi == k])
    print("OBJ", o.name, mats, len(v))
for g, vs in groups.items():
    v = np.concatenate(vs).astype(np.float32)
    if not len(v):
        continue
    d = np.zeros(len(v), DT); d["v"] = v
    n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); d["n"] = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    write(os.path.join(out, g + ".stl"), d)
