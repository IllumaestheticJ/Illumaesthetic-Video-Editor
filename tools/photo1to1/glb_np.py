"""blender -b -P glb_np.py -- model.glb out.npz parts_out_mm.stl 'part_a,part_b,...'
Exports the lookbook model (body + chosen kit parts, other part_* hidden) as triangles in the GLB frame (m),
and the chosen kit parts alone as an STL in mm (to overlay on the scan render)."""
import bpy, sys, numpy as np, bmesh
a = sys.argv[sys.argv.index('--') + 1:]; glb, out, parts_stl = a[0], a[1], a[2]; keep = set(filter(None, a[3].split(',')))
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=glb)
dg = bpy.context.evaluated_depsgraph_get(); V = []; F = []; PV = []; n = 0
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    base = o.name.split('.')[0]
    is_part = base.startswith('part_')
    if is_part and base not in keep: continue
    me = o.evaluated_get(dg).to_mesh(); bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.triangulate(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    v = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', v); v = v.reshape(-1, 3)
    M = np.array(o.matrix_world); v = (np.c_[v, np.ones(len(v))] @ M.T)[:, :3]
    t = np.empty(len(me.polygons) * 3, np.int64); me.polygons.foreach_get('vertices', t); t = t.reshape(-1, 3)
    V.append(v); F.append(t + n); n += len(v)
    if is_part: PV.append(v[t])
V = np.concatenate(V); F = np.concatenate(F); np.savez(out, v=V, f=F)
if PV:
    T = np.concatenate(PV) * 1000.0; rec = np.zeros(len(T), np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])); rec['v'] = T
    with open(parts_stl, 'wb') as fh: fh.write(b'\0' * 80); fh.write(np.uint32(len(T)).tobytes()); rec.tofile(fh)
print('GLBNP', len(V), len(F), 'parts tris', sum(len(p) for p in PV))
