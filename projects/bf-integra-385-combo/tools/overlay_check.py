import bpy, sys
from mathutils import Vector
R='/home/user/media/bf-integra-385-combo/work/reg'; out=sys.argv[sys.argv.index('--')+1]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=6; sc.render.resolution_x=700; sc.render.resolution_y=450
w=bpy.data.worlds.new('w'); w.use_nodes=True; w.node_tree.nodes['Background'].inputs[1].default_value=2.5; sc.world=w
for n,col in [('car_nospoiler',(0.8,0.8,0.8,1)),('aspec_rear_glbframe',(0.9,0.3,0.2,1))]:
    bpy.ops.wm.ply_import(filepath=f'{R}/{n}.ply', forward_axis='Y', up_axis='Z'); o=bpy.context.selected_objects[0]
    m=bpy.data.materials.new(n); m.use_nodes=True; m.node_tree.nodes['Principled BSDF'].inputs[0].default_value=col; o.data.materials.append(m)
cam=bpy.data.cameras.new('c'); cam.lens=45; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
for nm,loc in [('a',(-2.2,4.6,2.2)),('b',(3.5,1.9,1.1))]:
    co.location=Vector(loc); co.rotation_euler=(Vector((0,1.9,0.85))-co.location).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f'{out}_{nm}.png'; bpy.ops.render.render(write_still=True)
