"""Ep 4 Part B scan shots from the owner's GT350_Lip.blend (Drive, Ron's 'GT350 Bumper' folder): the bumper-off car scan,
the reverse-engineered bumper ('GT350 Front Bumper') and the designed lip ('LipSolid.*') are already aligned there.
Look = the owner's Blender screenshots (IMG_0774-0781): Workbench solid, studio light, lavender scan, green bumper, tan lip,
dark grey background.

  blender -b GT350_Lip.blend -P partB_render.py -- --out DIR --shot test|bumper|lip [--frames a:b] [--scale s]
"""
import bpy, sys, math, os
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
arg = lambda n, d: argv[argv.index(n) + 1] if n in argv else d
OUT, SHOT = arg("--out", "/tmp/partB"), arg("--shot", "test")
SCALE = float(arg("--scale", "1.0"))
os.makedirs(OUT, exist_ok=True)
scn = bpy.context.scene
KEEP = {"GT350 (DONE) Bumper Off Hood Closed": (0.58, 0.59, 0.84), "GT350 Front Bumper": (0.42, 0.72, 0.55)}
for o in bpy.data.objects:
    if o.name.startswith("LipSolid"):
        KEEP[o.name] = (0.80, 0.62, 0.44)
for o in bpy.data.objects:
    vis = o.name in KEEP
    o.hide_render = not vis
    o.hide_viewport = not vis
    if vis:
        o.color = (*KEEP[o.name], 1.0)
scn.render.engine = "BLENDER_WORKBENCH"
sh = scn.display.shading
sh.light = "STUDIO"
sh.color_type = "OBJECT"
sh.show_cavity = True
sh.cavity_type = "WORLD"
sh.curvature_ridge_factor = 0.6
sh.show_specular_highlight = True
scn.render.film_transparent = False
scn.world.color = (0.045, 0.045, 0.045) if scn.world else None
sh.background_type = "VIEWPORT" if hasattr(sh, "background_type") else None
try:
    sh.background_type = "WORLD"
except Exception:
    pass
scn.display.render_aa = "8"
scn.render.resolution_x, scn.render.resolution_y = 1080, 1920
scn.render.resolution_percentage = int(SCALE * 100)
scn.view_settings.view_transform = "Standard"
cam_d = bpy.data.cameras.new("pbcam")
cam = bpy.data.objects.new("pbcam", cam_d)
scn.collection.objects.link(cam)
scn.camera = cam
cam_d.sensor_fit = "VERTICAL"
cam_d.sensor_height = 36.0
cam_d.clip_start = 0.01


def look(loc, tgt, lens):
    loc, tgt = Vector(loc), Vector(tgt)
    f = (tgt - loc).normalized()
    r = f.cross(Vector((0, 0, 1))).normalized()
    u = r.cross(f)
    cam.matrix_world = Matrix.Translation(loc) @ Matrix(((r.x, u.x, -f.x), (r.y, u.y, -f.y), (r.z, u.z, -f.z))).to_4x4()
    cam_d.lens = lens



def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def eback(x, k=1.3):
    x = max(0.0, min(1.0, x)) - 1; return 1 + x * x * ((k + 1) * x + k)


BUMP = bpy.data.objects["GT350 Front Bumper"]
LIPS = [o for o in bpy.data.objects if o.name.startswith("LipSolid")]
B0 = BUMP.location.copy()
L0 = {o.name: o.location.copy() for o in LIPS}
lo, hi = (int(x) for x in arg("--frames", "0:36").split(":"))
ONLY = [int(x) for x in arg("--only", "").split(",") if x]
for fr in (ONLY or range(lo, hi)):
    if SHOT == "scan":      # bumper-off scan of the corner, then the reverse-engineered bumper slides on and settles
        k = (fr - 10) / 16.0
        BUMP.hide_render = fr < 10
        BUMP.location = B0 + Vector((0.0, -0.75 * (1 - eback(k)), 0.0))
        for o in LIPS:
            o.hide_render = True
        u = fr / 40.0
        look(Vector((1.75, -2.25, 1.15)).lerp(Vector((1.55, -1.95, 1.08)), ease(u)), (0.5, -0.08, 0.42), 50)
    elif SHOT == "lip":     # low three-quarter: the designed lip slides in under the bumper and hugs the curve
        k = (fr - 6) / 14.0
        for o in LIPS:
            o.hide_render = fr < 6
            o.location = L0[o.name] + Vector((0.0, -0.45 * (1 - eback(k, 1.1)), -0.06 * (1 - ease(k))))
        u = fr / 40.0
        a = math.radians(-58 + 10 * ease(u))
        r = 2.25
        look((r * math.sin(-a) * -1 + 0.0, -r * math.cos(a), 0.55), (0.3, -0.1, 0.3), 40)
    scn.render.filepath = os.path.join(OUT, SHOT, f"{fr:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("[partB]", SHOT, fr, flush=True)
