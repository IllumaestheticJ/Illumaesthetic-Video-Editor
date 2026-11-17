import bpy, sys, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=sys.argv[-1])
for o in bpy.data.objects:
    if o.type!='MESH': print('NODE',o.name,o.type,tuple(round(v,3) for v in o.location)); continue
    bb=[o.matrix_world@mathutils.Vector(c) for c in o.bound_box]
    mn=[min(v[i] for v in bb) for i in range(3)]; mx=[max(v[i] for v in bb) for i in range(3)]
    print('MESH',o.name,len(o.data.polygons),[round(x,3) for x in mn],[round(x,3) for x in mx],[m.name for m in o.data.materials][:6])
