"""Fitment check for lookbook parts (lesson from BF6: GLB parts are not always seated on the body).
blender -b --factory-startup -P seat_check.py -- <glb> <part,list> <hide,list>
For each part: distance from every part vertex to the nearest body surface (all shown non-part meshes). Prints the closest gap
and the 5th / 25th percentile in mm. A seated part touches the body (min ~0 mm, a good share of vertices within a few mm)."""
import bpy, sys, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]
PARTS, HIDE = a[1].split(','), a[2].split(',')
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.import_scene.gltf(filepath=a[0])
ms = [o for o in bpy.data.objects if o.type == 'MESH']
base = lambda o: o.name.split('.')[0]
body = [o for o in ms if not base(o).startswith('part_') and base(o) not in HIDE]
def bb(o):
    p = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return Vector([min(q[i] for q in p) for i in range(3)]), Vector([max(q[i] for q in p) for i in range(3)])
trees = {}
def tree(o):
    if o.name not in trees:
        m = o.matrix_world; me = o.data
        trees[o.name] = BVHTree.FromPolygons([m @ v.co for v in me.vertices], [tuple(p.vertices) for p in me.polygons])
    return trees[o.name]
for pn in PARTS:
    for po in [o for o in ms if base(o) == pn]:
        lo, hi = bb(po); lo -= Vector((.05,) * 3); hi += Vector((.05,) * 3)
        near = [o for o in body if all(bb(o)[0][i] <= hi[i] and bb(o)[1][i] >= lo[i] for i in range(3))]
        vs = [po.matrix_world @ v.co for v in po.data.vertices]; vs = vs[::max(1, len(vs) // 4000)]
        d = np.full(len(vs), 9.0)
        for o in near:
            t = tree(o)
            for i, v in enumerate(vs):
                r = t.find_nearest(v, d[i])
                if r[0] is not None: d[i] = min(d[i], r[3])
        d *= 1000
        print(f'SEAT {po.name}: min {d.min():.1f} mm, p5 {np.percentile(d, 5):.1f}, p25 {np.percentile(d, 25):.1f}, within 3 mm {100 * (d < 3).mean():.0f}% (bodies {len(near)})', flush=True)
