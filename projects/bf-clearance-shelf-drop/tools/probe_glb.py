import bpy, sys
from mathutils import Vector
p = sys.argv[sys.argv.index("--")+1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=p)
def bb(o):
    pts=[o.matrix_world @ Vector(c) for c in o.bound_box]
    lo=Vector([min(q[i] for q in pts) for i in range(3)]); hi=Vector([max(q[i] for q in pts) for i in range(3)])
    return lo,hi
for o in bpy.context.scene.objects:
    if o.type=='MESH':
        lo,hi=bb(o); print(f"{o.name:40s} {len(o.data.polygons):7d} lo={tuple(round(x,3) for x in lo)} hi={tuple(round(x,3) for x in hi)} mats={[m.name for m in o.data.materials][:3]}")
