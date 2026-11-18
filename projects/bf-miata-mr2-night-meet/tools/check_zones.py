"""v1 check: per zone, 3 stills from one camera: scan with the zone tinted red / zone removed / kit part seated (blue).
    blender -b --factory-startup -P check_zones.py -- mr2|nc outdir"""
import sys, os, bpy
from mathutils import Vector
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/blender"); import scan_render as SR
car, out = sys.argv[sys.argv.index("--") + 1:][:2]
M = "/home/user/media/bf-miata-mr2-night-meet"; D = f"{M}/dec"; K = f"{M}/kit_{car}"
Z = {"mr2": {"skirts": (["part_side_skirts"], (3.0, -1.6, 0.9), (0.8, 0.0, 0.35)), "eyelids": (["part_eyelids"], (1.6, -3.2, 1.3), (0.4, -1.55, 0.62)),
             "hood": (["part_hood_vents"], (1.2, -3.2, 2.0), (0, -1.45, 0.66)), "spats": (["part_rear_spats"], (2.2, 3.6, 0.6), (0.3, 1.7, 0.3)),
             "duck": (["part_duckbill"], (1.6, 3.6, 1.6), (0, 1.75, 0.75))},
     "nc": {"bumper": (["part_front_bumper", "part_front_lip", "part_canards"], (-2.2, -3.6, 1.1), (0, -1.7, 0.4)),
            "fender": (["part_fender_cuts"], (-2.3, -1.6, 0.75), (-0.8, -0.85, 0.42)), "skirts": (["part_side_skirts"], (-3.2, -0.2, 0.7), (-0.8, -0.15, 0.25)),
            "spats": (["part_rear_spats"], (-2.0, 3.6, 0.55), (-0.4, 1.65, 0.35))}}[car]
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.samples = 12; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 640, 480; sc.view_settings.view_transform = "AgX"
SR.studio_world((0.004, 0.004, 0.004, 1), False)
for name, loc, en, size in (("key", (3.5, -4.5, 4.5), 900, 4), ("rim", (-3.5, 4.5, 3.0), 1100, 2.5), ("top", (0, 0, 6), 700, 6), ("fill", (-4, -4, 2), 500, 4)):
    d = bpy.data.lights.new(name, "AREA"); d.energy = en; d.size = size
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector((0, 0, 0.5)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
def mat(name, col):
    m, nt, o = SR.new_mat(name); p = SR.principled(nt, col, 0.4, 0.3); nt.links.new(p.outputs[0], o.inputs[0]); return m
silver, red, blue = SR.mat_silver(), mat("r", (0.8, 0.05, 0.03, 1)), mat("b", (0.05, 0.25, 0.9, 1))
def imp(p, m):
    bpy.ops.wm.stl_import(filepath=p); o = bpy.context.selected_objects[0]; o.data.materials.append(m); return o
imp(f"{D}/{car}_keep.stl", silver)
cuts = {z: imp(f"{D}/{car}_cut_{z}.stl", silver) for z in Z}
parts = {z: [imp(f"{K}/{p}.stl", silver) for p in Z[z][0]] for z in Z}
for z in Z:
    for p in parts[z]: p.hide_render = True
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 40
for z, (pn, loc, tgt) in Z.items():
    cam.location = loc; cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cuts[z].data.materials[0] = red
    sc.render.filepath = f"{out}/{car}_{z}_a"; bpy.ops.render.render(write_still=True)
    cuts[z].hide_render = True
    sc.render.filepath = f"{out}/{car}_{z}_b"; bpy.ops.render.render(write_still=True)
    for p in parts[z]: p.hide_render = False; p.data.materials[0] = blue
    sc.render.filepath = f"{out}/{car}_{z}_c"; bpy.ops.render.render(write_still=True)
    for p in parts[z]: p.data.materials[0] = silver      # stays installed for the next zones
