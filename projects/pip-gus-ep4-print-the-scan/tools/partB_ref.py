"""Reference renders + raycasts for the IMG_0770 -> bumper-off scan 1:1 solve (GT350_Lip.blend world coordinates).
  blender -b GT350_Lip.blend -P partB_ref.py -- --out DIR --cam x,y,z:tx,ty,tz:lens [--name ref] [--ray "a:px,py;b:px,py"]
  blender -b GT350_Lip.blend -P partB_ref.py -- --out DIR --camjson cam.json [--name check]
Image 1440x1080, sensor width 36 mm (horizontal fit)."""
import bpy, sys, os, json, math
from mathutils import Vector, Matrix
argv = sys.argv[sys.argv.index("--") + 1:]
arg = lambda n, d=None: argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out"); os.makedirs(OUT, exist_ok=True)
scn = bpy.context.scene
SCAN = "GT350 (DONE) Bumper Off Hood Closed"
for o in bpy.data.objects:
    o.hide_render = o.hide_viewport = (o.name != SCAN)
so = bpy.data.objects[SCAN]
so.color = (0.62, 0.63, 0.80, 1)
scn.render.engine = "BLENDER_WORKBENCH"
sh = scn.display.shading
sh.light, sh.color_type, sh.show_cavity = "STUDIO", "OBJECT", True
scn.render.resolution_x, scn.render.resolution_y, scn.render.resolution_percentage = 1440, 1080, 100
cd = bpy.data.cameras.new("c"); cam = bpy.data.objects.new("c", cd); scn.collection.objects.link(cam); scn.camera = cam
cd.sensor_fit = "HORIZONTAL"; cd.sensor_width = 36.0; cd.clip_start = 0.01
if arg("--camjson"):
    cj = json.load(open(arg("--camjson")))
    cd.sensor_width = cj["sensor_width_mm"]; cd.lens = cj["focal_mm"]
    M = Matrix(cj["blender"]["rotation_matrix"]).to_4x4()
    M.translation = Vector(cj["blender"]["location"])
    cam.matrix_world = M
else:
    a, b, lens = arg("--cam").split(":")
    loc, tgt = Vector([float(x) for x in a.split(",")]), Vector([float(x) for x in b.split(",")])
    f = (tgt - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    cam.matrix_world = Matrix.Translation(loc) @ Matrix(((r.x, u.x, -f.x), (r.y, u.y, -f.y), (r.z, u.z, -f.z))).to_4x4()
    cd.lens = float(lens)
bpy.context.view_layer.update()
scn.render.filepath = os.path.join(OUT, arg("--name", "ref") + ".png")
bpy.ops.render.render(write_still=True)
if arg("--ray"):
    dg = bpy.context.evaluated_depsgraph_get()
    W, H = 1440, 1080
    fx = cd.lens / cd.sensor_width * W
    R = cam.matrix_world.to_3x3(); o = cam.matrix_world.translation
    hits = {}
    for item in arg("--ray").split(";"):
        nm, p = item.split(":"); px, py = [float(v) for v in p.split(",")]
        d = R @ Vector(((px - W / 2) / fx, -(py - H / 2) / fx, -1.0))
        ok, loc, n, i, ob, mtx = scn.ray_cast(dg, o, d.normalized())
        hits[nm] = [round(v, 5) for v in loc] if ok else None
        print("[ray]", nm, px, py, hits[nm], round((loc - o).length, 3) if ok else None, flush=True)
    json.dump(hits, open(os.path.join(OUT, arg("--name", "ref") + "_hits.json"), "w"), indent=1)
