"""Ron's finished render at the v0 end pose: his scene, Camera.006(L5) position/direction, portrait 9:16, lens = END_F.
    blender -b 'Honda Civic Sedan 2022-render.blend' -P ron_still_v0.py -- out.png pct spp"""
import sys, bpy
a = sys.argv[sys.argv.index("--") + 1:]
sc = bpy.context.scene
cam = bpy.data.objects["Camera.006(L5)"]; sc.camera = cam
cam.data.sensor_fit = "HORIZONTAL"; cam.data.sensor_width = 20.25; cam.data.lens = 72.0; cam.data.shift_x = cam.data.shift_y = 0
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, int(a[1])
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = int(a[2]); sc.cycles.use_denoising = True
import os
if os.environ.get("GARAGE"):   # v0.11 (user): plain warehouse garage instead of the black studio
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import garage_v0
    for n in ("Circle", "Plane"): bpy.data.objects[n].hide_render = True     # Ron's studio floor discs
    garage_v0.build(cam)
sc.render.filepath = a[0]; sc.render.image_settings.file_format = "PNG"
bpy.ops.render.render(write_still=True)
