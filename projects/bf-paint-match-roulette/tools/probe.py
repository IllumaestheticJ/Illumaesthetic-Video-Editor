import bpy, sys
from mathutils import Vector
argv=sys.argv[sys.argv.index('--')+1:]
for p in argv:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=p)
    def bb(objs):
        pts=[o.matrix_world@Vector(c) for o in objs for c in o.bound_box]
        return [round(min(v[i] for v in pts),3) for i in range(3)],[round(max(v[i] for v in pts),3) for i in range(3)]
    ms=[o for o in bpy.data.objects if o.type=='MESH']
    print('##',p.split('/')[-1],'ALL',bb(ms),'nfaces',sum(len(o.data.polygons) for o in ms))
    for o in ms:
        if 'wing' in o.name or 'body'==o.name: print('  ',o.name,bb([o]))
