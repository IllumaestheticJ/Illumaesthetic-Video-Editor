"""Which mesh pairs overlap between two groups at a frame. blender -b --python probe.py -- <shot> <frame> <groupA> <groupB>"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index("--") + 1:]; n = int(a[0]); fr = int(a[1])
import gr_shots as T
bpy.ops.wm.read_factory_settings(use_empty=True); T.SHOTS[n - 1](); bpy.context.scene.frame_set(fr); dg = bpy.context.evaluated_depsgraph_get()
def ms(name):
    if name == "legs": return [o for o in bpy.data.objects if o.name in ("leg-1", "leg1")]
    r = bpy.data.objects[name]; return [o for o in [r] + list(r.children_recursive) if o.type == "MESH" and not o.hide_render]
def tr(o):
    ev = o.evaluated_get(dg); me = ev.to_mesh(); mw = o.matrix_world
    t = BVHTree.FromPolygons([mw @ v.co for v in me.vertices], [list(p.vertices) for p in me.polygons]); ev.to_mesh_clear(); return t
A = [(o.name, tr(o)) for o in ms(a[2])]; B = [(o.name, tr(o)) for o in ms(a[3])]
print("PROBE", n, fr, sorted({(x, y) for x, tx in A for y, ty in B if x != y and tx.overlap(ty)}))
