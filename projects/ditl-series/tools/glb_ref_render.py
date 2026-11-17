import bpy, math, sys
from mathutils import Vector
argv=sys.argv[sys.argv.index("--")+1:]
variant, color, az, el, out = argv[0], argv[1], float(argv[2]), float(argv[3]), argv[4]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath="/home/user/Epsilon-Site/showroom/models/eps-subaru-wrx-vb-v3.glb")
kit = variant=="kit"
hide_kit = {"part_front_bumper","part_rear_bumper","part_side_skirts","part_wrc_wing","part_duckbill"}
hide_stock = {"body_front_bumper_stock","body_rear_bumper_stock","trim_side_stock","trim_f1_blank_stock"}
for o in bpy.data.objects:
    if o.type!='MESH': continue
    if (kit and o.name in hide_stock) or (not kit and o.name in hide_kit) or o.name=="part_duckbill":
        o.hide_render=True
cols={"wrblue":(0.02,0.12,0.55),"white":(0.85,0.86,0.86)}
m=bpy.data.materials["paint"]
bsdf=[n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'][0]
bsdf.inputs["Base Color"].default_value=(*cols[color],1)
for l in bsdf.inputs["Base Color"].links: m.node_tree.links.remove(l)
# bounds
mins=Vector((1e9,)*3); maxs=Vector((-1e9,)*3)
for o in bpy.data.objects:
    if o.type=='MESH' and not o.hide_render:
        for c in o.bound_box:
            w=o.matrix_world@Vector(c); mins=Vector(map(min,mins,w)); maxs=Vector(map(max,maxs,w))
ctr=(mins+maxs)/2; print("BOUNDS",mins,maxs)
sc=bpy.context.scene
cam=bpy.data.objects.new("cam",bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera=cam
cam.data.lens=40
d=8.5; a=math.radians(az); e=math.radians(el)
cam.location=ctr+Vector((d*math.cos(e)*math.sin(a), -d*math.cos(e)*math.cos(a), d*math.sin(e)))
cam.rotation_euler=(ctr-cam.location).to_track_quat('-Z','Y').to_euler()
sun=bpy.data.objects.new("sun",bpy.data.lights.new("sun",'SUN')); sun.data.energy=4; sun.rotation_euler=(math.radians(40),0,math.radians(30)); sc.collection.objects.link(sun)
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.55,0.6,0.65,1); w.node_tree.nodes["Background"].inputs[1].default_value=1.0
bpy.ops.mesh.primitive_plane_add(size=60,location=(ctr.x,ctr.y,mins.z)); g=bpy.context.object
gm=bpy.data.materials.new("g"); gm.use_nodes=True; gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(0.25,0.25,0.25,1); g.data.materials.append(gm)
sc.render.engine='CYCLES'; sc.cycles.samples=48; sc.cycles.use_denoising=True; sc.cycles.device='CPU'; sc.render.resolution_x=1024; sc.render.resolution_y=1536
sc.view_settings.view_transform='Standard'
sc.render.filepath=out; bpy.ops.render.render(write_still=True)
