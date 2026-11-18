"""Look test for v2: retracing the original bumper on the real GT350 scan (owner's GT350_Lip.blend).
Scan with the original bumper = flat-shaded triangles; section curves traced over it; smooth surface fills in from the centre.
  blender -b GT350_Lip.blend -P retrace_test.py -- OUT_DIR"""
import bpy, bmesh, sys, os, math
from mathutils import Vector, Matrix
OUT = sys.argv[sys.argv.index("--") + 1]; os.makedirs(OUT, exist_ok=True)
scn = bpy.context.scene
SCANS = ["GT350 (DONE) Front End", "GT350 (DONE) Front Bumper"]
NEW = "GT350 Front Bumper"
keep = set(SCANS + [NEW])
for o in list(bpy.data.objects):
    if o.name not in keep:
        me = o.data if o.type == "MESH" else None
        bpy.data.objects.remove(o, do_unlink=True)
        if me is not None and me.users == 0: bpy.data.meshes.remove(me)
scn.render.engine = "BLENDER_WORKBENCH"
sh = scn.display.shading
sh.light, sh.color_type, sh.show_cavity = "STUDIO", "OBJECT", True
sh.cavity_type = "BOTH"
scn.display.render_aa = "8"
scn.render.resolution_x, scn.render.resolution_y, scn.render.resolution_percentage = 1080, 1920, 50
cd = bpy.data.cameras.new("c"); cam = bpy.data.objects.new("c", cd); scn.collection.objects.link(cam); scn.camera = cam
cd.sensor_fit = "VERTICAL"; cd.sensor_height = 36; cd.clip_start = 0.01
def look(loc, tgt, lens):
    loc, tgt = Vector(loc), Vector(tgt); f = (tgt - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    cam.matrix_world = Matrix.Translation(loc) @ Matrix(((r.x, u.x, -f.x), (r.y, u.y, -f.y), (r.z, u.z, -f.z))).to_4x4(); cd.lens = lens
def shot(name):
    scn.render.filepath = os.path.join(OUT, name); bpy.ops.render.render(write_still=True)
nb = bpy.data.objects[NEW]
for s in SCANS:
    bpy.data.objects[s].color = (0.58, 0.59, 0.84, 1)
nb.color = (0.42, 0.72, 0.55, 1)
CAM = ((1.9, -2.3, 1.0), (0.45, -0.1, 0.42), 45)
# which scan state shows the original bumper?
for i, s in enumerate(SCANS):
    for t in SCANS: bpy.data.objects[t].hide_render = (t != s)
    nb.hide_render = True
    look(*CAM); shot(f"state{i}.png")
# real triangles: close-up of the scan, flat shaded
sc = bpy.data.objects[SCANS[1]]
for t in SCANS: bpy.data.objects[t].hide_render = (t != SCANS[1])
for p in sc.data.polygons[:1]: pass
sc.data.polygons.foreach_set("use_smooth", [False] * len(sc.data.polygons))
look((0.72, -0.62, 0.52), (0.6, -0.2, 0.45), 85); shot("tris_close.png")
look((0.68, -0.38, 0.5), (0.62, -0.2, 0.46), 120); shot("tris_macro.png")
# section curves of the reverse-engineered bumper (world space)
dg = bpy.context.evaluated_depsgraph_get()
bm = bmesh.new(); bm.from_mesh(nb.data); bm.transform(nb.matrix_world)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
xs = [v.co.x for v in bm.verts]; zs = [v.co.z for v in bm.verts]
print("bumper bbox x", min(xs), max(xs), "z", min(zs), max(zs), flush=True)
cuts = [("x", x) for x in [k * 0.11 for k in range(-8, 9)]] + [("z", z) for z in (0.26, 0.36, 0.46, 0.56, 0.64)]
edges_all = []
for ax, val in cuts:
    b2 = bm.copy()
    co = (val, 0, 0) if ax == "x" else (0, 0, val); no = (1, 0, 0) if ax == "x" else (0, 0, 1)
    r = bmesh.ops.bisect_plane(b2, geom=b2.verts[:] + b2.edges[:] + b2.faces[:], plane_co=co, plane_no=no, dist=1e-6)
    ce = [e for e in r["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    # keep only the outer skin (front side): y below the local median + margin
    vs = {}
    out = []
    for e in ce:
        a, b = e.verts[0].co.copy(), e.verts[1].co.copy()
        out.append((a, b))
    edges_all.append((ax, val, out)); b2.free()
me = bpy.data.meshes.new("sections"); bmc = bmesh.new()
for ax, val, es in edges_all:
    for a, b in es:
        va, vb = bmc.verts.new(a), bmc.verts.new(b); bmc.edges.new((va, vb))
bmesh.ops.remove_doubles(bmc, verts=bmc.verts, dist=1e-5)
bmc.to_mesh(me); bmc.free()
so = bpy.data.objects.new("sections", me); scn.collection.objects.link(so)
bpy.context.view_layer.objects.active = so; so.select_set(True)
bpy.ops.object.convert(target="CURVE")
so = bpy.context.view_layer.objects.active
so.data.bevel_depth = 0.004; so.data.bevel_resolution = 2
so.color = (0.75, 1.0, 0.85, 1)
# surface grows from the centre: mask by |x|
vg = nb.vertex_groups.new(name="grow")
half = max(abs(min(xs)), abs(max(xs)))
import numpy as np
n = len(nb.data.vertices); co = np.zeros(n * 3, np.float32); nb.data.vertices.foreach_get("co", co)
Mw = np.array(nb.matrix_world); wx = co.reshape(-1, 3) @ Mw[:3, :3].T + Mw[:3, 3]
w = 1.0 - np.clip(np.abs(wx[:, 0]) / half, 0, 1)
for lvl in range(0, 101):
    idx = np.nonzero(np.round(w * 100) == lvl)[0]
    if len(idx): vg.add(idx.tolist(), lvl / 100.0, "REPLACE")
mk = nb.modifiers.new("grow", "MASK"); mk.vertex_group = "grow"
look(*CAM)
for name, thr, curves in (("re_curves.png", 1.01, True), ("re_half.png", 0.55, True), ("re_full.png", 0.0, False)):
    mk.threshold = thr; nb.hide_render = thr > 1.0; so.hide_render = not curves
    shot(name)
