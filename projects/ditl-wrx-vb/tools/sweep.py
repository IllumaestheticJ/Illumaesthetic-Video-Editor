"""Pose sweep for a person's arm. blender -b --python sweep.py -- <shot> <person> <armname> <ups> <rzs> <bends>"""
import bpy, sys, os, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils.bvhtree import BVHTree
import shots as T
R = math.radians; A = sys.argv[sys.argv.index("--") + 1:]; L = lambda s: [float(x) for x in s.split(",")]
bpy.ops.wm.read_factory_settings(use_empty=True); T.SHOTS[int(A[0]) - 1](); bpy.context.scene.frame_set(5)
a = bpy.data.objects[A[2] + "_ua"]; f = bpy.data.objects[A[2] + "_fa"]
for o in (a, f): o.animation_data_clear()
body = [bpy.data.objects[A[1] + s] for s in ("_torso", "_head", "_neck")]; limb = [f] + [c for c in f.children_recursive if c.type == "MESH"]
def tr(objs, dg):
    vs, fs = [], []
    for o in objs:
        ev = o.evaluated_get(dg); me = ev.to_mesh(); b = len(vs); vs += [o.matrix_world @ v.co for v in me.vertices]; fs += [[b + i for i in p.vertices] for p in me.polygons]; ev.to_mesh_clear()
    return BVHTree.FromPolygons(vs, fs)
print("ORIG", [round(math.degrees(x)) for x in a.rotation_euler], [round(math.degrees(x)) for x in f.rotation_euler])
out = []
for up, rz, bend in itertools.product(L(A[3]), L(A[4]), L(A[5])):
    a.rotation_euler = (R(up), 0, R(rz)); f.rotation_euler = (R(bend), 0, 0); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    out.append(f"{up:.0f}/{rz:.0f}/{bend:.0f}:" + ("HIT" if tr(body, dg).overlap(tr(limb, dg)) else "ok"))
print("SW", " ".join(out))
