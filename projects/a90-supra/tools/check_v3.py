"""Quick colour-coded diagnostic stills of raw-frame STLs (Workbench, seconds per view).

    flock /home/user/media/work/a90/blender.lock blender -b -P projects/a90-supra/tools/check_v3.py -- \
        --out /path/prefix --mesh body.stl:0.75,0.75,0.78 --mesh fill_fbump.stl:1,0.45,0.1[:dx,dy,dz mm] \
        --view name:az,dist_m,z_m,lookx,looky,lookz[,lens] ...
az = degrees around +Z from +X (nose). Meshes are in car raw mm.
"""
import argparse, math, sys
import bpy
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True); ap.add_argument("--mesh", action="append", default=[])
ap.add_argument("--view", action="append", default=[]); ap.add_argument("--res", default="900x900")
A = ap.parse_args(a)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
for spec in A.mesh:
    f = spec.split(":"); col = [float(x) for x in f[1].split(",")] if len(f) > 1 else [0.8, 0.8, 0.8]
    off = [float(x) for x in f[2].split(",")] if len(f) > 2 else [0, 0, 0]
    bpy.ops.wm.stl_import(filepath=f[0], global_scale=0.001)
    o = bpy.context.selected_objects[0]; o.color = (*col, 1); o.location = Vector(off) * 0.001
    for p in o.data.polygons: p.use_smooth = False
sc.render.engine = "BLENDER_WORKBENCH"
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "OBJECT"; sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.show_backface_culling = False
sc.world = bpy.data.worlds.new("w"); sc.world.color = (0, 0, 0)
W, H = [int(x) for x in A.res.split("x")]
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
sc.render.film_transparent = False
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
cam.data.clip_start, cam.data.clip_end = 0.05, 100
for v in A.view:
    name, nums = v.split(":"); n = [float(x) for x in nums.split(",")]
    az, d, z, lx, ly, lz = n[:6]; cam.data.lens = n[6] if len(n) > 6 else 35
    look = Vector((lx, ly, lz)); cam.location = Vector((look.x + d * math.cos(math.radians(az)), look.y + d * math.sin(math.radians(az)), z))
    cam.rotation_euler = (look - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = f"{A.out}_{name}.png"; bpy.ops.render.render(write_still=True)
