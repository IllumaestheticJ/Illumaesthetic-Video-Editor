"""Blender: import the Epsilon lookbook GLB and write one binary STL per part group (GLB->Blender frame, metres).

    blender -b -P glb_export.py -- eps-honda-civic-sedan-fe-facelift-v9.glb outdir
Groups: body, trim, glass, front_lip, side_skirts, rear_lip, sport_wing, duckbill, wheel_FL/FR/RL/RR (+ rim/tyre split).
"""
import os, sys, struct
import bpy, numpy as np

glb, out = sys.argv[sys.argv.index("--") + 1:][:2]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
dg = bpy.context.evaluated_depsgraph_get()
groups = {}
for o in bpy.context.scene.objects:
    if o.type != "MESH":
        continue
    n = o.name
    mats = [s.material.name if s.material else "" for s in o.material_slots]
    if n.startswith("part_sport_wing_duckbill"): g = "duckbill"
    elif n.startswith("part_sport_wing"): g = "sport_wing"
    elif n.startswith("part_rear_lip"): g = "rear_lip"
    elif n.startswith("part_side_skirts"): g = "side_skirts"
    elif n.startswith("part_front_lip"): g = "front_lip"
    elif n.startswith("wheel_"): g = n[:8]
    elif n.startswith("body"): g = "body"
    elif n.startswith("trim"): g = "trim"
    elif n.startswith("glass"): g = "glass"
    else: g = None
    print("OBJ", n, mats, len(o.data.polygons), g)
    if not g:
        continue
    me = o.evaluated_get(dg).to_mesh()
    me.calc_loop_triangles()
    co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co)
    M = np.array(o.matrix_world, np.float64)
    co = co.reshape(-1, 3).astype(np.float64) @ M[:3, :3].T + M[:3, 3]
    tri = np.empty(len(me.loop_triangles) * 3, np.int32); me.loop_triangles.foreach_get("vertices", tri)
    mi = np.empty(len(me.loop_triangles), np.int32); me.loop_triangles.foreach_get("material_index", mi)
    v = co[tri.reshape(-1, 3)]
    groups.setdefault(g, []).append(v)
    if g.startswith("wheel_"):
        for k, m in enumerate(mats):
            sub = "rim" if m.startswith("rim") else "tyre" if m == "rubber" else "brake"
            groups.setdefault(f"{g}_{sub}", []).append(v[mi == k])
for g, parts in groups.items():
    v = np.concatenate(parts).astype(np.float32)
    if not len(v):
        continue
    n = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    rec = np.zeros(len(v), np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])); rec["n"] = n; rec["v"] = v
    with open(f"{out}/{g}.stl", "wb") as f:
        f.write(b"\0" * 80 + struct.pack("<I", len(v))); rec.tofile(f)
    print("GROUP", g, len(v), v.reshape(-1, 3).min(0).round(3), v.reshape(-1, 3).max(0).round(3))
