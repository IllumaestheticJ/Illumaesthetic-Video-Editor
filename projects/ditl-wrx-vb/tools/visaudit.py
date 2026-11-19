"""Audit vis(): objects whose first visibility key is 'hidden' at a frame > 1 stay hidden all shot (constant extrapolation).
Also lists which car meshes the POV hands overlap in a shot. blender -b --python visaudit.py -- <shot> [carcheck]"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils.bvhtree import BVHTree
import shots as T
a = sys.argv[sys.argv.index("--") + 1:]; n = int(a[0]); calls = {}
orig = T.vis
def rec(o, f, show): calls.setdefault(o.name, []).append((f, show)); orig(o, f, show)
T.vis = rec
bpy.ops.wm.read_factory_settings(use_empty=True); T.SHOTS[n - 1]()
bad = {k: v[:3] for k, v in calls.items() if min(v)[0] > 1 and not sorted(v)[0][1]}
print("VISAUDIT", n, bad)
if len(a) > 1:
    hands = [o for o in bpy.data.objects if o.type == "EMPTY" and any(c.name == o.name + "_palm" for c in o.children)]
    hm = {m.name for h in hands for m in h.children_recursive}
    car = [o for o in bpy.data.objects if o.type == "MESH" and o.name not in hm and not o.hide_render and not o.name.startswith(("leg", "ap", "mir", "him", "seatpan", "floorpan"))]
    def tr(o, dg):
        ev = o.evaluated_get(dg); me = ev.to_mesh(); t = BVHTree.FromPolygons([o.matrix_world @ v.co for v in me.vertices], [list(p.vertices) for p in me.polygons]) if me.polygons else None; ev.to_mesh_clear(); return t
    hits = {}
    for f in range(1, T.NF[n - 1] + 1, 3):
        bpy.context.scene.frame_set(f); dg = bpy.context.evaluated_depsgraph_get(); ct = [(c.name, tr(c, dg)) for c in car]
        for h in hands:
            for m in h.children_recursive:
                if m.type != "MESH" or m.hide_render: continue
                t = tr(m, dg)
                for cn, c in ct:
                    if c and t and t.overlap(c): hits.setdefault(f"{h.name}:{m.name.split('_')[-1]} x {cn}", []).append(f)
    print("CARHIT", n, {k: (v[0], v[-1], len(v)) for k, v in hits.items()})
