import bpy, sys, math
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; ply,out=a
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=4; sc.render.resolution_x=500; sc.render.resolution_y=400
w=bpy.data.worlds.new('w'); w.use_nodes=True; w.node_tree.nodes['Background'].inputs[1].default_value=2.0; sc.world=w
bpy.ops.wm.ply_import(filepath=ply, forward_axis='Y', up_axis='Z')
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; cam.ortho_scale=2.6; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
for n,loc in [('x',(8,0,0)),('y',(0,8,0)),('z',(0,0,8)),('iso',(5,5,4))]:
    co.location=loc; co.rotation_euler=(Vector((0,0,0))-Vector(loc)).to_track_quat('-Z','Y' if n!='z' else 'Y').to_euler()
    sc.render.filepath=f'{out}_{n}.png'; bpy.ops.render.render(write_still=True)
