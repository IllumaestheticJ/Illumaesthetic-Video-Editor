"""Arm/hand intersection check. blender -b --python collide.py -- <shot> [step]
Groups: every hand rig (an empty with a *_palm child: palm, fingers, arm, sleeve) and every person (torso, head, arms).
Reports, per sampled frame, which visible groups' meshes overlap (BVH overlap of world-space triangles)."""
import bpy, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index("--") + 1:]; n = int(a[0]); step = int(a[1]) if len(a) > 1 else 3
import tl_shots as T, tl_shots_b as B
bpy.ops.wm.read_factory_settings(use_empty=True)
(T.SHOTS.get(n) or B.SHOTS[n])()
NF = B.NF[n]
roots = [o for o in bpy.data.objects if o.type == "EMPTY" and any(c.name == o.name + "_palm" for c in o.children)]
persons = [o for o in bpy.data.objects if o.type == "EMPTY" and any(c.name == o.name + "_torso" for c in o.children)]
groups = {o.name: o for o in roots + persons}
def tree(root, dg):
    vs, fs = [], []
    for o in [root] + list(root.children_recursive):
        if o.type != "MESH" or o.hide_render: continue
        anc = []; q = o.parent
        while q: anc.append(q); q = q.parent
        if root in persons and any(r in anc for r in roots): continue
        if root in persons and o.name.endswith(("_face", "_fm")) or "_face_" in o.name: continue
        ev = o.evaluated_get(dg); me = ev.to_mesh(); mw = o.matrix_world; base = len(vs)
        vs += [mw @ v.co for v in me.vertices]; fs += [[base + i for i in p.vertices] for p in me.polygons]; ev.to_mesh_clear()
    return BVHTree.FromPolygons(vs, fs) if fs else None
hits = {}
for f in list(range(1, NF + 1, step)) + [NF]:
    bpy.context.scene.frame_set(f); dg = bpy.context.evaluated_depsgraph_get()
    vis = {k: o for k, o in groups.items() if not o.hide_render and not all(c.hide_render for c in o.children_recursive if c.type == "MESH")}
    ts = {k: tree(o, dg) for k, o in vis.items()}
    ks = [k for k in ts if ts[k]]
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            if ts[ks[i]].overlap(ts[ks[j]]): hits.setdefault(f"{ks[i]} x {ks[j]}", []).append(f)
# a person's own forearm/hand (W.arm: *_fa, *_hd) must stay out of their torso and head
def mtree(objs, dg):
    vs, fs = [], []
    for o in objs:
        if o.hide_render: continue
        ev = o.evaluated_get(dg); me = ev.to_mesh(); mw = o.matrix_world; base = len(vs)
        vs += [mw @ v.co for v in me.vertices]; fs += [[base + i for i in p.vertices] for p in me.polygons]; ev.to_mesh_clear()
    return BVHTree.FromPolygons(vs, fs) if fs else None
for pr in persons:
    kids = [c for c in pr.children_recursive if c.type == "MESH"]
    body = [c for c in kids if c.name.endswith(("_torso", "_head"))]; limbs = [c for c in kids if c.name.endswith(("_fa", "_hd"))]
    if not limbs: continue
    for f in list(range(1, NF + 1, step)) + [NF]:
        bpy.context.scene.frame_set(f); dg = bpy.context.evaluated_depsgraph_get(); tb, tl = mtree(body, dg), mtree(limbs, dg)
        if tb and tl and tb.overlap(tl): hits.setdefault(f"{pr.name} arm x body", []).append(f)
print("COLLIDE", n, json.dumps(hits))
