import bpy, sys
from mathutils import Vector
R='/home/user/media/bf-integra-385-combo/work/reg'; out=sys.argv[sys.argv.index('--')+1]
def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
    sc.render.engine='CYCLES'; sc.cycles.samples=8; sc.render.resolution_x=600; sc.render.resolution_y=450
    w=bpy.data.worlds.new('w'); w.use_nodes=True; w.node_tree.nodes['Background'].inputs[1].default_value=3.0; sc.world=w
    cam=bpy.data.cameras.new('c'); cam.lens=50; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
    co.location=Vector((-1.6,3.9,1.9)); co.rotation_euler=(Vector((0,2.1,0.95))-co.location).to_track_quat('-Z','Y').to_euler()
    return sc
def imp(n,col=None):
    bpy.ops.wm.ply_import(filepath=f'{R}/{n}.ply', forward_axis='Y', up_axis='Z')
    o=bpy.context.selected_objects[0]
    if col:
        m=bpy.data.materials.new(n); m.diffuse_color=col; m.use_nodes=True; m.node_tree.nodes['Principled BSDF'].inputs[0].default_value=col; o.data.materials.append(m)
    return o
for name,parts in [('a',[('scan_glbframe',None)]),('b',[('car_nospoiler',None),('deck_patch',(0.9,0.3,0.2,1))]),('c',[('stock_spoiler',(0.2,0.5,0.9,1))])]:
    sc=setup()
    for p,col in parts: imp(p,col)
    sc.render.filepath=f'{out}_{name}.png'; bpy.ops.render.render(write_still=True)
