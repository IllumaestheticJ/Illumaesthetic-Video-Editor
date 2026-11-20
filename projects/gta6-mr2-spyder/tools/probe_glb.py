import bpy, sys, numpy as np, bmesh
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=a[0])
o = bpy.data.objects["trim"]; me = o.data
print("uv layers", {ob.name: [u.name for u in ob.data.uv_layers] for ob in bpy.data.objects if ob.type == "MESH"})
bm = bmesh.new(); bm.from_mesh(me); bm.transform(o.matrix_world); bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=2e-4); bm.faces.ensure_lookup_table(); bm.faces.index_update(); uvl = bm.loops.layers.uv.active
mats = [m.name for m in me.materials]
seen = set()
for f in bm.faces:
    if f.index in seen: continue
    stack = [f]; comp = []; seen.add(f.index)
    while stack:
        g = stack.pop(); comp.append(g)
        for e in g.edges:
            for h in e.link_faces:
                if h.index not in seen: seen.add(h.index); stack.append(h)
    v = np.array([vv.co[:] for g in comp for vv in g.verts]); lo, hi = v.min(0), v.max(0)
    ms = sorted({mats[g.material_index] for g in comp})
    rear_low = hi[1] > 1.45 and lo[2] < 0.5 and hi[2] < 0.6 and abs((lo[0] + hi[0]) / 2) > 0.2 and abs((lo[0] + hi[0]) / 2) < 0.62
    lamp = any(m in ("light_red", "light_inner") for m in ms) and lo[1] > 1.2
    if (rear_low or lamp) and len(comp) >= 12:
        uv = np.array([l[uvl].uv[:] for g in comp for l in g.loops])
        print("UV", uv.min(0).round(3), uv.max(0).round(3), end=" ")
        print("LAMP" if lamp else "REARLOW", len(comp), ms, lo.round(3), hi.round(3))
for n in ("part_diffuser", "part_rear_spats", "part_hood_vents"):
    ob = bpy.data.objects[n]; v = np.array([ob.matrix_world @ x.co for x in ob.data.vertices])
    print(n, v.min(0).round(3), v.max(0).round(3))
