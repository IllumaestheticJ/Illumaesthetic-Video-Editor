"""Low-poly copy of the owner's real GT350 original-bumper scan for the cartoon (v3: 'Print my bumper!' must show a bumper).
  blender -b GT350_Lip.blend -P export_bumper_lowpoly.py -- OUT.npz [target_tris]
World coordinates (m): x across the car, front faces -y. Loose scan crumbs dropped."""
import bpy, bmesh, sys
import numpy as np
argv = sys.argv[sys.argv.index("--") + 1:]
out, target = argv[0], int(argv[1]) if len(argv) > 1 else 7000
ob = bpy.data.objects["GT350 (DONE) Front Bumper"]
for o in list(bpy.data.objects):
    if o is not ob:
        me = o.data if o.type == "MESH" else None
        bpy.data.objects.remove(o, do_unlink=True)
        if me is not None and me.users == 0:
            bpy.data.meshes.remove(me)
n0 = len(ob.data.polygons)
m = ob.modifiers.new("d", "DECIMATE")
m.ratio = target / n0
dg = bpy.context.evaluated_depsgraph_get()
me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
me.transform(ob.matrix_world)
bm = bmesh.new(); bm.from_mesh(me)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
# keep the biggest connected island only
seen, best = set(), []
for v in bm.verts:
    if v in seen: continue
    isl, st = [], [v]; seen.add(v)
    while st:
        a = st.pop(); isl.append(a)
        for e in a.link_edges:
            b = e.other_vert(a)
            if b not in seen: seen.add(b); st.append(b)
    if len(isl) > len(best): best = isl
keep = set(best)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v not in keep], context="VERTS")
bm.verts.index_update()
V = np.array([v.co[:] for v in bm.verts], np.float32)
F = np.array([[v.index for v in f.verts] for f in bm.faces], np.int32)
np.savez(out, v=V, f=F)
print("[lowpoly]", n0, "->", len(F), "tris; bbox", V.min(0), V.max(0), flush=True)
