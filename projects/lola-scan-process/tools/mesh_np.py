# export a decimated vertex/face array of the prepared scan for fast numpy silhouettes
import bpy, numpy as np, sys
out=sys.argv[sys.argv.index('--')+1]
o=[o for o in bpy.data.objects if o.type=='MESH'][0]
m=o.modifiers.new('d','DECIMATE'); m.ratio=float(sys.argv[sys.argv.index("--")+2]) if len(sys.argv)>sys.argv.index("--")+2 else 0.03
dg=bpy.context.evaluated_depsgraph_get(); e=o.evaluated_get(dg); me=e.to_mesh()
me.calc_loop_triangles()
v=np.empty(len(me.vertices)*3); me.vertices.foreach_get('co',v); v=v.reshape(-1,3)
mw=np.array(o.matrix_world); v=(np.c_[v,np.ones(len(v))]@mw.T)[:,:3]
t=np.empty(len(me.loop_triangles)*3,np.int32); me.loop_triangles.foreach_get('vertices',t)
np.savez(out,v=v,f=t.reshape(-1,3)); print("EXPORTED",len(v),len(t)//3)
