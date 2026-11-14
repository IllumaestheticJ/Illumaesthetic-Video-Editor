"""blender -b preview.blend -P export_wheels.py -- out_dir
Re-export the 'wheels' collection of the designer's preview.blend (design frame, mm) WITHOUT the generic
'Brembo_GTS_*' brake models (v7: replaced by the scanned GT-R brakes), and write each wheel's hub from its
Brembo_GTS_disc_001 rotor (bbox centre; the rotor is thin along design X) to hubs.json."""
import bpy, numpy as np, struct, sys, os, json
out = sys.argv[sys.argv.index('--') + 1]; os.makedirs(out, exist_ok=True)
dg = bpy.context.evaluated_depsgraph_get(); tris = []; hubs = {}
for o in bpy.data.objects:
    if o.type != 'MESH' or 'wheels' not in [c.name for c in o.users_collection] or o.name.startswith('Cylinder'):
        continue
    oe = o.evaluated_get(dg); me = oe.to_mesh(); me.calc_loop_triangles(); n = len(me.loop_triangles)
    if not n: oe.to_mesh_clear(); continue
    co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    M = np.array(o.matrix_world); w = (co @ M[:3, :3].T + M[:3, 3]) * 1000.0
    if o.name.startswith('Brembo_GTS'):
        if o.name.startswith('Brembo_GTS_disc_001'):
            lo, hi = w.min(0), w.max(0); hubs[o.name] = {'centre': ((lo + hi) / 2).tolist(), 'size': (hi - lo).tolist()}
        oe.to_mesh_clear(); continue
    idx = np.empty(n * 3, np.int32); me.loop_triangles.foreach_get('vertices', idx)
    tris.append(w[idx.reshape(-1, 3)].astype(np.float32)); oe.to_mesh_clear()
T = np.concatenate(tris)
a = np.zeros(len(T), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])); a['v'] = T
with open(f'{out}/wheels_nobrake.stl', 'wb') as f:
    f.write(b'preview.blend wheels without Brembo_GTS'.ljust(80)); f.write(struct.pack('<I', len(a))); a.tofile(f)
json.dump(hubs, open(f'{out}/hubs.json', 'w'), indent=1)
print('WHEELS', len(a), 'HUBS', json.dumps(hubs))
