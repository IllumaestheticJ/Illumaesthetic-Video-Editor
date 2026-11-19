"""Ep 4 v2: real Blender scenes of the GT350 job (owner's GT350_Lip.blend) for Gus's phone and for the fast recap.
Owner v1 notes: use the actual Blender scenes on a phone while Gus explains; show RETRACING the bumper (curves over the
scan, then the surface), not parts popping in; a clear scan-vs-surface visual.

  blender -b GT350_Lip.blend -P v2_content.py -- --out DIR [--only tri,retrace,...] [--frames f,f,...] [--scale 0.5]

Phone shots (reel frames, rendered at --scale 0.5 into DIR/phone/<frame>.png):
  tri     247-352  the scanned bumper -> push in until the real triangles show ("A mesh of tiny triangles") -> its thin
                   open edge ("No thickness")
  retrace 570-708  the scan of the original bumper ("the reference") -> section curves traced over it -> the smooth
                   surface grows from the centre over the curves ("remake the original")
  lip     708-778  bumper-off car scan + retraced bumper; the designed lip slides in ("design a new one on it")
  fit     778-912  wipe along the bumper: faceted scan -> smooth surface with clean curves; then the lip seam close-up
  both    912-995  slow orbit of the finished design on the scan
Recap shots (full res, DIR/recap/<name>/<i>.png): r_scan 9 f, r_trace 18 f, r_car 9 f, r_lip 18 f.
Look = the owner's screenshots: Workbench studio light, lavender scan, green bumper, tan lip, dark grey background.
"""
import bpy, bmesh, sys, os, math
import numpy as np
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
arg = lambda n, d=None: argv[argv.index(n) + 1] if n in argv else d
OUT = arg("--out")
ONLY = set((arg("--only", "") or "").split(",")) - {""}
FRAMES = {int(x) for x in (arg("--frames", "") or "").split(",") if x}
SCALE = float(arg("--scale", "0.5"))
scn = bpy.context.scene
S_BUMP, S_OFF, NEW = "GT350 (DONE) Front Bumper", "GT350 (DONE) Bumper Off Hood Closed", "GT350 Front Bumper"
keep = {S_BUMP, S_OFF, NEW} | {o.name for o in bpy.data.objects if o.name.startswith("LipSolid")}
for o in list(bpy.data.objects):
    if o.name not in keep:
        me = o.data if o.type == "MESH" else None
        bpy.data.objects.remove(o, do_unlink=True)
        if me is not None and me.users == 0:
            bpy.data.meshes.remove(me)
sb, so_, nb = bpy.data.objects[S_BUMP], bpy.data.objects[S_OFF], bpy.data.objects[NEW]
LIPS = [o for o in bpy.data.objects if o.name.startswith("LipSolid")]
LAV, GRN, TAN, MINT = (0.58, 0.59, 0.84, 1), (0.42, 0.72, 0.55, 1), (0.80, 0.62, 0.44, 1), (0.82, 1.0, 0.9, 1)
sb.color = so_.color = LAV
nb.color = GRN
for o in LIPS:
    o.color = TAN
sb.data.polygons.foreach_set("use_smooth", [False] * len(sb.data.polygons))   # the scan reads as what it is: facets
scn.render.engine = "BLENDER_WORKBENCH"
sh = scn.display.shading
sh.light, sh.color_type, sh.show_cavity, sh.cavity_type = "STUDIO", "OBJECT", True, "BOTH"
scn.display.render_aa = "8"
scn.render.resolution_x, scn.render.resolution_y = 1080, 1920
scn.view_settings.view_transform = "Standard"
cd = bpy.data.cameras.new("c")
cam = bpy.data.objects.new("c", cd)
scn.collection.objects.link(cam)
scn.camera = cam
cd.sensor_fit, cd.sensor_height, cd.clip_start = "VERTICAL", 36.0, 0.005


def look(loc, tgt, lens):
    loc, tgt = Vector(loc), Vector(tgt)
    f = (tgt - loc).normalized()
    r = f.cross(Vector((0, 0, 1))).normalized()
    u = r.cross(f)
    cam.matrix_world = Matrix.Translation(loc) @ Matrix(((r.x, u.x, -f.x), (r.y, u.y, -f.y), (r.z, u.z, -f.z))).to_4x4()
    cd.lens = lens


def cl(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = cl(x)
    return x * x * (3 - 2 * x)


def eback(x, k=1.2):
    x = cl(x) - 1
    return 1 + x * x * ((k + 1) * x + k)


def lerp(a, b, t):
    return a + (b - a) * t


def lerpv(a, b, t):
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


# ---- the retraced bumper: world-space verts, growth masks, section curves
n = len(nb.data.vertices)
co = np.zeros(n * 3, np.float32)
nb.data.vertices.foreach_get("co", co)
Mw = np.array(nb.matrix_world)
wx = co.reshape(-1, 3) @ Mw[:3, :3].T + Mw[:3, 3]
HALF = float(np.abs(wx[:, 0]).max())


def vgroup(name, w):
    vg = nb.vertex_groups.new(name=name)
    q = np.round(np.clip(w, 0, 1) * 100).astype(int)
    for lvl in range(0, 101):
        idx = np.nonzero(q == lvl)[0]
        if len(idx):
            vg.add(idx.tolist(), lvl / 100.0, "REPLACE")
    return vg


vgroup("centre", 1.0 - np.abs(wx[:, 0]) / HALF)            # 1 at the centreline, 0 at the ends
vgroup("wipe", 1.0 - (wx[:, 0] + HALF) / (2 * HALF))       # 1 at x = -HALF, 0 at x = +HALF
MASK = nb.modifiers.new("grow", "MASK")
NB0 = nb.location.copy()
OFF = Vector((0, -0.004, 0.0015))       # the surface sits a hair proud of the scan (no z-fighting)

bm = bmesh.new()
bm.from_mesh(nb.data)
bm.transform(nb.matrix_world)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
SECTIONS = []                            # (axis, value, curve object)
for ax, val in [("x", k * 0.11) for k in range(-8, 9)] + [("z", z) for z in (0.26, 0.36, 0.46, 0.56, 0.64)]:
    b2 = bm.copy()
    plane_co, plane_no = ((val, 0, 0), (1, 0, 0)) if ax == "x" else ((0, 0, val), (0, 0, 1))
    r = bmesh.ops.bisect_plane(b2, geom=b2.verts[:] + b2.edges[:] + b2.faces[:], plane_co=plane_co, plane_no=plane_no, dist=1e-6)
    bmc = bmesh.new()
    for e in r["geom_cut"]:
        if isinstance(e, bmesh.types.BMEdge):
            bmc.edges.new((bmc.verts.new(e.verts[0].co + OFF), bmc.verts.new(e.verts[1].co + OFF)))
    b2.free()
    if not bmc.edges:
        bmc.free()
        continue
    bmesh.ops.remove_doubles(bmc, verts=bmc.verts, dist=1e-5)
    me = bpy.data.meshes.new(f"sec_{ax}{val:.2f}")
    bmc.to_mesh(me)
    bmc.free()
    ob = bpy.data.objects.new(me.name, me)
    scn.collection.objects.link(ob)
    for o in bpy.context.selected_objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.convert(target="CURVE")
    ob = bpy.context.view_layer.objects.active
    ob.data.bevel_depth, ob.data.bevel_resolution = 0.0035, 2
    try:
        ob.data.bevel_factor_mapping_end = "SPLINE"
    except Exception:
        pass
    ob.color = MINT
    SECTIONS.append((ax, val, ob))
bm.free()
print("[v2] sections", len(SECTIONS), flush=True)
L0 = {o.name: o.location.copy() for o in LIPS}


def state(scan_bump=False, scan_off=False, surf=None, mask=None, curves=0.0, curve_wipe=None, lips=None, lip_k=1.0):
    """surf: None hidden, else mask threshold (0 = whole surface); curves: 0..1 draw-on (centre outward, x then z)."""
    sb.hide_render, so_.hide_render = not scan_bump, not scan_off
    nb.hide_render = surf is None
    nb.location = NB0 + OFF
    if surf is not None:
        MASK.vertex_group = mask or "centre"
        MASK.threshold = surf
        MASK.show_render = surf > 0.0
    order = sorted(SECTIONS, key=lambda s: (s[0] == "z", abs(s[1]) if s[0] == "x" else s[1]))
    for i, (ax, val, ob) in enumerate(order):
        if curve_wipe is not None:      # visible where the wipe has passed (x < wipe position)
            vis = (val < curve_wipe) if ax == "x" else True
            ob.hide_render = not vis or curves <= 0
            ob.data.bevel_factor_end = 1.0
            if ax == "z":
                ob.data.bevel_factor_end = cl((curve_wipe + HALF) / (2 * HALF))
                ob.data.bevel_factor_start = 0.0
        else:
            k = cl(curves * (len(order) + 3) - i) if curves > 0 else 0.0
            ob.hide_render = k <= 0.001
            ob.data.bevel_factor_end = max(0.001, k)
    for o in LIPS:
        o.hide_render = lips is None
        if lips is not None:
            o.location = L0[o.name] + Vector((0.0, -0.45 * (1 - eback(lip_k, 1.1)), -0.06 * (1 - ease(lip_k))))


Q34 = ((1.9, -2.3, 1.0), (0.45, -0.1, 0.42))


def sh_tri(k, fr):
    state(scan_bump=True)
    a = ease((fr - 250) / 40.0)                         # push in until the triangles show (on "triangles." 286)
    if fr < 318:
        loc = lerpv((1.5, -1.7, 0.85), (0.71, -0.48, 0.505), a)
        look(loc, lerpv((0.55, -0.15, 0.45), (0.62, -0.2, 0.46), a), lerp(45, 110, a))
    else:                                               # "No thickness." - the open top edge of the skin, from above/behind
        u = ease((fr - 318) / 34.0)
        look(lerpv((0.95, 0.55, 0.95), (0.8, 0.75, 0.9), u), (0.55, -0.12, 0.6), 60)


def sh_retrace(k, fr=None, fast=False):
    if fast:                                            # recap: curves 0-0.5, surface 0.4-1
        c, s = cl(k / 0.5), cl((k - 0.4) / 0.6)
    else:                                               # "remake" 654 -> curves to 688, surface 684-712
        c, s = cl((fr - 652) / 36.0), cl((fr - 684) / 26.0)
    done = s >= 1.0
    state(scan_bump=not done, surf=(1.0 - ease(s)) if s > 0 else None, mask="centre", curves=c if not done else 1.0)
    u = ease(k)
    ang = math.radians(lerp(-50, -34, u))
    r = 3.0
    look((0.25 + r * math.sin(-ang), -r * math.cos(ang), 0.95), (0.25, -0.1, 0.44), 60)


def sh_lip(k, fr=None, fast=False):
    lk = cl((k - 0.1) / 0.6) if fast else cl((fr - 720) / 26.0)
    state(scan_off=True, surf=0.0, lips=True, lip_k=lk)
    ang = math.radians(lerp(-58, -48, ease(k)))
    r = 2.25
    look((r * math.sin(-ang), -r * math.cos(ang), 0.55), (0.3, -0.1, 0.3), 40)


def sh_fit(k, fr):
    if fr < 858:                                        # wipe: faceted scan -> smooth surface + clean curves
        w = ease((fr - 786) / 68.0)
        xw = lerp(-HALF - 0.02, HALF + 0.02, w)
        state(scan_bump=True, surf=1.0 - cl((xw + HALF) / (2 * HALF)), mask="wipe", curves=1.0, curve_wipe=xw)
        look(lerpv((-0.2, -2.35, 0.7), (0.3, -2.3, 0.72), ease((fr - 778) / 80.0)), (0.05, -0.1, 0.45), 52)
    else:                                               # "Every curve." - glide along the lip / bumper seam
        state(scan_off=True, surf=0.0, lips=True, lip_k=1.0)
        u = ease((fr - 858) / 54.0)
        look(lerpv((1.45, -1.45, 0.3), (0.95, -1.75, 0.28), u), (0.45, -0.25, 0.26), 55)


def sh_both(k, fr):
    state(scan_off=True, surf=0.0, lips=True, lip_k=1.0)
    ang = math.radians(lerp(-30, 20, ease(k)))
    r = 3.3
    look((r * math.sin(-ang), -r * math.cos(ang), 0.95), (0.0, -0.05, 0.45), 52)


def sh_rscan(k, fr=None):
    state(scan_bump=True)
    ang = math.radians(lerp(-50, -46, k))
    look((0.25 + 3.0 * math.sin(-ang), -3.0 * math.cos(ang), 0.95), (0.25, -0.1, 0.44), 60)


def sh_rcar(k, fr=None):
    state(scan_off=True, surf=0.0)
    ang = math.radians(lerp(-40, -44, k))
    look((0.1 + 3.2 * math.sin(-ang), -3.2 * math.cos(ang), 1.0), (0.1, -0.1, 0.5), 40)


PHONE = [("tri", 247, 352, sh_tri), ("retrace", 570, 708, sh_retrace), ("lip", 708, 778, sh_lip), ("fit", 778, 912, sh_fit),
         ("both", 912, 995, sh_both)]
RECAP = [("r_scan", 9, sh_rscan), ("r_trace", 18, lambda k, fr=None: sh_retrace(k, fast=True)), ("r_car", 9, sh_rcar),
         ("r_lip", 18, lambda k, fr=None: sh_lip(k, fast=True))]


def render(path):
    if os.path.exists(path) and not FRAMES:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path[:-4] + "_tmp.png"
    scn.render.filepath = tmp
    bpy.ops.render.render(write_still=True)
    os.replace(tmp, path)


for name, f0, f1, fn in PHONE:
    if ONLY and name not in ONLY:
        continue
    scn.render.resolution_percentage = int(SCALE * 100)
    for fr in range(f0, f1):
        if FRAMES and fr not in FRAMES:
            continue
        fn((fr - f0) / max(1, f1 - 1 - f0), fr)
        render(os.path.join(OUT, "phone", f"{fr:04d}.png"))
        print("[v2]", name, fr, flush=True)
for name, nfr, fn in RECAP:
    if (ONLY and name not in ONLY) or FRAMES:
        continue
    scn.render.resolution_percentage = 100
    for i in range(nfr):
        fn(i / max(1, nfr - 1))
        render(os.path.join(OUT, "recap", name, f"{i:04d}.png"))
        print("[v2]", name, i, flush=True)
print("[v2] DONE", flush=True)
