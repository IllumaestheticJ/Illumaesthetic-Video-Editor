"""Front-on mask of a car's grille emblem, taken from its GLB (the real badge artwork, as scanned).

    blender -b -P projects/nfs-carlot/tools/badge_from_glb.py -- <car.glb> <out.png> chrome

Renders an orthographic view of the nose (0.34 m wide, centred 0.66 m up) with the named materials white
and everything else black, and prints which materials have faces there. Clean the mask afterwards
(open, blur, threshold): scans leave rough edges. Used for the Acura plate, which the game does not have.
"""
import bpy, sys, math
from mathutils import Vector
glb, out = sys.argv[sys.argv.index("--")+1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
# find front-centre geometry by material: report bbox of each material's faces near the nose, x in [-0.2,0.2]
import bmesh
info={}
for o in bpy.data.objects:
    if o.type!='MESH': continue
    mw=o.matrix_world
    for p in o.data.polygons:
        c=mw@p.center
        if abs(c.x)<0.16 and c.y<-2.0 and 0.35<c.z<0.95:
            m=o.material_slots[p.material_index].name if o.material_slots else '?'
            b=info.setdefault((o.name,m),[1e9,-1e9,1e9,-1e9,1e9,-1e9,0])
            b[0]=min(b[0],c.x);b[1]=max(b[1],c.x);b[2]=min(b[2],c.y);b[3]=max(b[3],c.y);b[4]=min(b[4],c.z);b[5]=max(b[5],c.z);b[6]+=1
for k,b in info.items(): print("IVE_MAT",k,[round(v,3) for v in b[:6]],b[6])
# flat render: every material black except the ones named on the command line (white)
white=sys.argv[sys.argv.index("--")+3:]
for m in bpy.data.materials:
    m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    e=nt.nodes.new("ShaderNodeEmission"); o_=nt.nodes.new("ShaderNodeOutputMaterial")
    e.inputs[0].default_value=(1,1,1,1) if m.name in white else (0,0,0,1); nt.links.new(e.outputs[0],o_.inputs[0])
cd=bpy.data.cameras.new("c"); cd.type='ORTHO'; cd.ortho_scale=0.34
co=bpy.data.objects.new("c",cd); bpy.context.scene.collection.objects.link(co)
co.location=(0,-6,0.66); co.rotation_euler=(math.radians(90),0,0); bpy.context.scene.camera=co
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.samples=16; sc.cycles.device='CPU'
sc.render.resolution_x=1000; sc.render.resolution_y=1000; sc.view_settings.view_transform='Standard'
sc.render.filepath=out; bpy.ops.render.render(write_still=True)
