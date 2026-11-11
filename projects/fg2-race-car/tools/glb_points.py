import bpy, sys, numpy as np
bpy.ops.wm.read_factory_settings(use_empty=True)
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.import_scene.gltf(filepath=a[0])
out={}
for o in bpy.data.objects:
    if o.type!='MESH': continue
    me=o.data; v=np.empty(len(me.vertices)*3); me.vertices.foreach_get('co',v); v=v.reshape(-1,3)
    M=np.array(o.matrix_world); out[o.name]=(np.c_[v,np.ones(len(v))]@M.T)[:,:3]
np.savez(a[1],**out); print('SAVED',{k:len(v) for k,v in out.items()})
