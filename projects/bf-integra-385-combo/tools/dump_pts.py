# dump world-space vertices of mesh objects (optionally filtered) to .npy; usage: blender -b X -P dump_pts.py -- out.npy [glb] [names,...]
import bpy, sys, numpy as np
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]
if len(a)>1 and a[1].endswith('.glb'):
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=a[1]); names=a[2].split(',') if len(a)>2 else None
else: names=None
P=[]
for o in bpy.data.objects:
    if o.type!='MESH' or (names and o.name not in names): continue
    m=o.data; v=np.zeros(len(m.vertices)*3); m.vertices.foreach_get('co',v); v=v.reshape(-1,3)
    M=np.array(o.matrix_world); v=v@M[:3,:3].T+M[:3,3]; P.append(v)
P=np.concatenate(P); rng=np.random.default_rng(0); P=P[rng.choice(len(P),min(len(P),300000),replace=False)]
np.save(out,P); print('DUMP',out,P.shape)
