"""Product thumbnails for the cart cards: each Epsilon part alone. blender -b --python thumbs.py -- <outdir>"""
import bpy, sys, math
from mathutils import Vector
out = sys.argv[sys.argv.index("--") + 1]
PARTS = {"part_front_bumper": 200, "part_rear_bumper": 20, "part_side_skirts": 250, "part_wrc_wing": 30}
for part, az in PARTS.items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath="/home/user/epsilon-site/showroom/models/eps-subaru-wrx-vb-v3.glb")
    m = bpy.data.materials["paint"]; b = [n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
    for l in list(b.inputs["Base Color"].links): m.node_tree.links.remove(l)
    b.inputs["Base Color"].default_value = (0.02, 0.12, 0.55, 1)
    mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
    for o in bpy.data.objects:
        if o.type != "MESH": continue
        if o.name != part: o.hide_render = True; continue
        for v in o.data.vertices:
            w = o.matrix_world @ v.co; mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
    c = (mn + mx) / 2; d = (mx - mn).length * 1.25
    sc = bpy.context.scene; cam = bpy.data.objects.new("c", bpy.data.cameras.new("c")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 50
    a = math.radians(az); cam.location = c + Vector((d * math.sin(a), -d * math.cos(a), d * 0.35)); cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.91, 0.93, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 1.2
    s = bpy.data.objects.new("s", bpy.data.lights.new("s", "SUN")); s.data.energy = 3; s.rotation_euler = (math.radians(50), 0, a + 0.5); sc.collection.objects.link(s)
    sc.render.engine = "CYCLES"; sc.cycles.samples = 24; sc.cycles.use_denoising = True; sc.render.resolution_x = sc.render.resolution_y = 256; sc.view_settings.view_transform = "Standard"
    sc.render.filepath = f"{out}/thumb_{part}.png"; bpy.ops.render.render(write_still=True)
