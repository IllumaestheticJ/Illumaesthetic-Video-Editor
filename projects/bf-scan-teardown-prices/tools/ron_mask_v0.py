"""Car matte for the v0.7 end text (text partly behind the car): Ron's scene through the same Camera.006(L5) portrait
setup as ron_still_v0.py, with a transparent film, so alpha = car (body, wheels, kit).
    blender -b 'Honda Civic Sedan 2022-render.blend' -P ron_mask_v0.py -- out.png pct"""
import sys, bpy
a = sys.argv[sys.argv.index("--") + 1:]
sc = bpy.context.scene
cam = bpy.data.objects["Camera.006(L5)"]; sc.camera = cam
cam.data.sensor_fit = "HORIZONTAL"; cam.data.sensor_width = 20.25; cam.data.lens = 72.0; cam.data.shift_x = cam.data.shift_y = 0
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, int(a[1])
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 4; sc.cycles.use_denoising = False
sc.render.film_transparent = True
for n in ("Circle", "Plane"): bpy.data.objects[n].hide_render = True   # v0.11: matte = car only (no floor glow)
sc.render.filepath = a[0]; sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
bpy.ops.render.render(write_still=True)
