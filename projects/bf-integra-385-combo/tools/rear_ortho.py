import bpy, sys, math
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; which=a[1]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=8; sc.render.resolution_x=800; sc.render.resolution_y=500
w=bpy.data.worlds.new('w'); w.use_nodes=True; w.node_tree.nodes['Background'].inputs[1].default_value=2.0; sc.world=w
if which=='glb': bpy.ops.import_scene.gltf(filepath='/home/user/media/bf-integra-385-combo/glb/eps-acura-integra-type-s-de5-v19.glb')
else: bpy.ops.wm.ply_import(filepath='/home/user/media/bf-integra-385-combo/work/reg/car_nospoiler_filled.ply', forward_axis='Y', up_axis='Z')
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; cam.ortho_scale=1.6; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
co.location=(0,8,0.6); co.rotation_euler=(Vector((0,0,0.6))-co.location).to_track_quat('-Z','Y').to_euler()
sc.render.filepath=out; bpy.ops.render.render(write_still=True)
