"""Part A ("the usual way") cartoon scene for the scan-tedium explainer reel - Blender 5.3, Cycles CPU.

Builds a cartoon shop, a blocky blue sedan, two cuboid characters (PIP, GUS) and the storyboard props from primitives,
then renders one look-development still per storyboard shot (S1-S10, script version A).

Usage (one Blender process at a time, in the background):
  blender -b --factory-startup -P partA_scene.py -- --out DIR [--shots S1,S3] [--scale 1.0] [--spp 8] [--threads 4]
Writes DIR/<shot>.png and DIR/timings.json (seconds per still).

Design notes
- Palette: illumaesthetic.com theme (#0b0c0b near-black, #619f73 / #77ac87 sage, #ecefec off-white), the car's blue, warm
  neutral shop. Red only where it should read as pain (the clock's second hand).
- Toon look: diffuse-only materials, bright warm world + one soft sun, Standard view transform (brand hexes land as authored),
  inverted-hull outlines (solidify shell, flipped normals, a backface-switched black material: no Freestyle cost).
- Persistent data stays OFF (lessons: Cycles dropped lights mid-animation with persistent data and keyed parts).
- No text, numerals, logos or brands anywhere in 3D: the clock has ticks only; pins on the laptop are colour-coded, not numbered.
- Characters are generic cuboid people of our own design (bevelled toy-block parts, protruding block eyes, no textures).
"""
import bpy, bmesh, math, random, sys, time, json, os
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default


OUT = arg("--out", "/home/user/media/work/scan-tedium/stills")
SHOTS = arg("--shots", "S1,S2,S3,S4,S5,S6,S7,S8,S9,S10").split(",")
SCALE = float(arg("--scale", "1.0"))
SPP = int(arg("--spp", "8"))
THREADS = int(arg("--threads", "4"))
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------------------------------------------- timing
# Script A line windows (seconds, reel time) from script.md; drives mouth flaps in the animation pass (not audio amplitude).
LINES_A = [
    ("PIP", 0.2, 1.9, "So... how do you scan a whole car?"),
    ("GUS", 1.9, 3.6, "The usual way? Dots. Lots of dots."),
    ("GUS", 3.7, 5.3, "One every few inches. Never in a row."),
    ("PIP", 5.5, 6.6, "Then you scan it?"),
    ("GUS", 6.7, 7.9, "In pieces."),
    ("GUS", 7.9, 9.4, "Front. Side. Roof. Back."),
    ("GUS", 9.5, 11.0, "Then I line them all up."),
    ("PIP", 11.1, 12.1, "Is it done yet?"),
    ("GUS", 12.1, 12.5, "No."),
    ("GUS", 12.6, 14.1, "Now we peel the dots off."),
    ("PIP", 14.1, 15.4, "There's got to be a faster way."),
]
# Storyboard shot grid (reel frames at 30 fps, version A). Cuts get snapped to measured kicks later.
SHOT_FRAMES = {"S1": (0, 57), "S2": (57, 110), "S3": (110, 162), "S4": (162, 200), "S5": (200, 237),
               "S6": (237, 283), "S7": (283, 330), "S8": (330, 375), "S9": (375, 423), "S10": (423, 465)}

# ----------------------------------------------------------------------------------------------------------------- scene
scn = bpy.context.scene
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
COLL = scn.collection


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexcol(h, a=1.0):
    h = h.lstrip("#")
    return (lin(int(h[0:2], 16) / 255), lin(int(h[2:4], 16) / 255), lin(int(h[4:6], 16) / 255), a)


PAL = dict(
    black="#0b0c0b", sage="#619f73", sage_l="#77ac87", white="#ecefec",
    car="#2a4fb5", glass="#1b2333", tyre="#1c1d1c", hub="#c3c7c3", trim="#3a3d3a",
    floor="#978a7a", wall="#dccbb3", base="#b49f83", door="#d6d8d2", rib="#bcc0b9", peg="#c2ad8f", hole="#6e5f4c",
    wood="#a57b55", wood_d="#7d5a3d",
    skin="#e2ad83", pip_top="#77ac87", pip_pants="#2b2e2b", shoe="#ecefec",
    gus_suit="#2d312e", gus_cap="#619f73", patch="#ecefec",
    red="#d43c2c", scan="#d3d7d3", ui_piece="#aeb3ae", ui_piece2="#8c918c", pin_blue="#6f93ee",
    metal="#8e938e", dark="#232523",
)

_MATS = {}


def _new_mat(name):
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, out


def mat(key, alpha=1.0):
    """Flat diffuse material from the palette (optionally see-through)."""
    name = f"m_{key}_{alpha:.2f}"
    if name in _MATS:
        return _MATS[name]
    m, nt, out = _new_mat(name)
    d = nt.nodes.new("ShaderNodeBsdfDiffuse")
    d.inputs["Color"].default_value = hexcol(PAL.get(key, key))
    sh = d.outputs[0]
    if alpha < 1.0:
        t = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        mx.inputs[0].default_value = alpha
        nt.links.new(t.outputs[0], mx.inputs[1])
        nt.links.new(sh, mx.inputs[2])
        sh = mx.outputs[0]
    nt.links.new(sh, out.inputs["Surface"])
    m.diffuse_color = hexcol(PAL.get(key, key))
    _MATS[name] = m
    return m


def emit(key, strength=1.0, alpha=1.0):
    name = f"e_{key}_{strength:.2f}_{alpha:.2f}"
    if name in _MATS:
        return _MATS[name]
    m, nt, out = _new_mat(name)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = hexcol(PAL.get(key, key))
    e.inputs["Strength"].default_value = strength
    sh = e.outputs[0]
    if alpha < 1.0:
        t = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        mx.inputs[0].default_value = alpha
        nt.links.new(t.outputs[0], mx.inputs[1])
        nt.links.new(sh, mx.inputs[2])
        sh = mx.outputs[0]
    nt.links.new(sh, out.inputs["Surface"])
    _MATS[name] = m
    return m


def outline_mat():
    """Inverted hull: the solidify shell has inward normals, so its near side is back-facing to the camera (see-through)
    and only the far side peeking out around the silhouette renders flat near-black. Non-camera rays (shadow, ambient)
    pass straight through the shell, otherwise it would shade the object inside it."""
    if "outline" in _MATS:
        return _MATS["outline"]
    m, nt, out = _new_mat("outline")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    lp = nt.nodes.new("ShaderNodeLightPath")
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(lp.outputs["Is Camera Ray"], inv.inputs[1])
    mxv = nt.nodes.new("ShaderNodeMath")
    mxv.operation = "MAXIMUM"
    nt.links.new(geo.outputs["Backfacing"], mxv.inputs[0])
    nt.links.new(inv.outputs[0], mxv.inputs[1])
    t = nt.nodes.new("ShaderNodeBsdfTransparent")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = hexcol(PAL["black"])
    e.inputs["Strength"].default_value = 1.0
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mxv.outputs[0], mx.inputs[0])
    nt.links.new(e.outputs[0], mx.inputs[1])   # fac 0: camera ray on the shell's far side (silhouette rim) -> black
    nt.links.new(t.outputs[0], mx.inputs[2])   # fac 1: near side of the shell, or any non-camera ray -> see-through
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    _MATS["outline"] = m
    return m


OUTLINE = outline_mat()


def empty(name, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None)
    COLL.objects.link(ob)
    ob.parent = parent
    ob.location = loc
    ob.rotation_euler = [math.radians(a) for a in rot]
    return ob


def new_obj(name, bm, mats, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    COLL.objects.link(ob)
    for m in mats:
        me.materials.append(m)
    ob.parent = parent
    ob.location = loc
    ob.rotation_euler = [math.radians(a) for a in rot]
    return ob


def add_mods(ob, bevel=0.0, ol=0.0, seg=3):
    if bevel:
        b = ob.modifiers.new("bev", "BEVEL")
        b.width = bevel
        b.segments = seg
        b.limit_method = "ANGLE"
    if ol:
        s = ob.modifiers.new("ol", "SOLIDIFY")
        s.thickness = ol
        s.offset = 1.0
        s.use_flip_normals = True
        s.use_rim = False
        s.use_even_offset = True
        s.material_offset = 1
    return ob


def box(name, size, loc=(0, 0, 0), m=None, parent=None, bevel=0.0, ol=0.0, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent, loc, rot)
    return add_mods(ob, bevel, ol)


def cyl(name, r, depth, loc=(0, 0, 0), m=None, parent=None, axis="Z", seg=32, bevel=0.0, ol=0.0, r2=None, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r,
                          radius2=r if r2 is None else r2, depth=depth)
    if axis == "X":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"))
    elif axis == "Y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent, loc, rot)
    return add_mods(ob, bevel, ol)


def hull(name, pts, m=None, parent=None, bevel=0.0, ol=0.0, loc=(0, 0, 0)):
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in pts]
    res = bmesh.ops.convex_hull(bm, input=vs)
    bmesh.ops.delete(bm, geom=res["geom_interior"], context="VERTS")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent, loc)
    return add_mods(ob, bevel, ol)


def poly(name, pts2d, m, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), z=0.0):
    """Flat n-gon in local XY (used for screen UI and 2D-ish props)."""
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, z)) for x, y in pts2d]
    bm.faces.new(vs)
    return new_obj(name, bm, [m], parent, loc, rot)


def set_vis(ob, vis):
    ob.hide_render = not vis
    ob.hide_viewport = not vis
    for c in ob.children:
        set_vis(c, vis)


# ----------------------------------------------------------------------------------------------------------------- shop
def build_shop():
    g = empty("SHOP")
    floor = box("floor", (40, 40, 0.02), (0, 0, -0.01), mat("floor"), g)
    box("wall_back", (30, 0.2, 6), (0, 3.7, 3), mat("wall"), g)
    box("wall_left", (0.2, 20, 6), (-7.0, -6, 3), mat("wall"), g)
    box("base_back", (30, 0.06, 0.16), (0, 3.58, 0.08), mat("base"), g)
    box("band_back", (30, 0.03, 0.16), (0, 3.595, 1.12), mat("sage"), g)       # brand-sage wall band
    box("band_left", (0.03, 20, 0.16), (-6.895, -6, 1.12), mat("sage"), g)
    for y in (-1.3, 1.3):                                                       # painted bay lines either side of the car
        box(f"bay{y}", (6.4, 0.08, 0.004), (0, y, 0.002), mat("#c9c2b2"), g)
    box("base_left", (0.06, 20, 0.16), (-6.88, -6, 0.08), mat("base"), g)
    # roll-up door behind the car
    door = box("rollup", (3.6, 0.08, 3.1), (-1.2, 3.58, 1.55), mat("door"), g, bevel=0.02, ol=0.02)
    for i in range(1, 12):
        box(f"rib{i}", (3.56, 0.02, 0.035), (-1.2, 3.53, 0.26 * i), mat("rib"), g)
    box("rollup_box", (3.9, 0.3, 0.32), (-1.2, 3.5, 3.25), mat("rib"), g, bevel=0.03, ol=0.02)
    # pegboard + tools over the workbench
    box("pegboard", (2.7, 0.04, 1.3), (3.35, 3.58, 1.95), mat("peg"), g, bevel=0.01, ol=0.015)
    bm = bmesh.new()
    for ix in range(26):
        for iz in range(12):
            x, z = 2.1 + ix * 0.1, 1.38 + iz * 0.1
            s = 0.013
            vs = [bm.verts.new((x - s, 3.555, z - s)), bm.verts.new((x + s, 3.555, z - s)),
                  bm.verts.new((x + s, 3.555, z + s)), bm.verts.new((x - s, 3.555, z + s))]
            bm.faces.new(vs)
    new_obj("peg_holes", bm, [mat("hole")], g)
    # tools: wrench, hammer, screwdriver, tape (generic silhouettes)
    box("wrench_h", (0.06, 0.03, 0.5), (2.35, 3.53, 1.95), mat("metal"), g, bevel=0.01, ol=0.012)
    cyl("wrench_r", 0.07, 0.03, (2.35, 3.53, 2.24), mat("metal"), g, axis="Y", bevel=0.005, ol=0.012)
    box("hammer_h", (0.05, 0.03, 0.55), (2.75, 3.53, 1.9), mat("wood"), g, bevel=0.01, ol=0.012)
    box("hammer_hd", (0.24, 0.05, 0.08), (2.75, 3.52, 2.2), mat("dark"), g, bevel=0.01, ol=0.012)
    box("sd_h", (0.07, 0.04, 0.2), (3.1, 3.53, 2.25), mat("sage"), g, bevel=0.015, ol=0.012)
    box("sd_s", (0.02, 0.02, 0.3), (3.1, 3.53, 2.0), mat("metal"), g, ol=0.008)
    cyl("tape", 0.11, 0.06, (3.55, 3.52, 2.15), mat("sage_l"), g, axis="Y", bevel=0.01, ol=0.012)
    cyl("tape_c", 0.05, 0.065, (3.55, 3.52, 2.15), mat("peg"), g, axis="Y")
    box("level", (0.6, 0.04, 0.07), (4.1, 3.53, 2.35), mat("sage"), g, bevel=0.01, ol=0.012)
    # workbench
    box("bench_top", (2.7, 0.75, 0.07), (3.35, 3.17, 0.92), mat("wood"), g, bevel=0.015, ol=0.02)
    for x in (2.1, 4.6):
        for y in (2.88, 3.48):
            box(f"bench_leg{x}{y}", (0.07, 0.07, 0.88), (x, y, 0.44), mat("dark"), g, ol=0.012)
    box("bench_shelf", (2.6, 0.65, 0.04), (3.35, 3.17, 0.25), mat("wood_d"), g, ol=0.015)
    box("toolbox", (0.55, 0.3, 0.25), (2.6, 3.2, 0.395), mat("sage"), g, bevel=0.02, ol=0.015)
    # tyre stack (set dressing, left)
    for i in range(3):
        cyl(f"tyre_stack{i}", 0.36, 0.25, (-5.6, 2.6, 0.13 + i * 0.26), mat("tyre"), g, bevel=0.04, ol=0.02)
        cyl(f"tyre_stack_c{i}", 0.2, 0.255, (-5.6, 2.6, 0.13 + i * 0.26), mat("dark"), g)
    return g


# ----------------------------------------------------------------------------------------------------------------- car
CAR_BODY = dict(x0=-2.0, x1=2.0, y=0.85, z0=0.32, z1=0.98)
CAB = dict(xb0=-1.15, xb1=1.0, xt0=-0.72, xt1=0.48, yb=0.74, yt=0.62, z0=0.98, z1=1.5)


def cabin_pts(grow=0.0):
    c = CAB
    return [(c["xb0"] - grow, s * (c["yb"] + grow), c["z0"]) for s in (-1, 1)] + \
           [(c["xb1"] + grow, s * (c["yb"] + grow), c["z0"]) for s in (-1, 1)] + \
           [(c["xt0"] - grow, s * (c["yt"] + grow), c["z1"] + grow) for s in (-1, 1)] + \
           [(c["xt1"] + grow, s * (c["yt"] + grow), c["z1"] + grow) for s in (-1, 1)]


def build_car():
    g = empty("CAR")
    b = CAR_BODY
    box("car_body", (b["x1"] - b["x0"], 2 * b["y"], b["z1"] - b["z0"]), (0, 0, (b["z0"] + b["z1"]) / 2), mat("car"), g,
        bevel=0.07, ol=0.025)
    hull("car_cabin", cabin_pts(), mat("car"), g, bevel=0.05, ol=0.025)
    c = CAB
    # side windows (two per side, split by the B-pillar), windshield, rear glass
    for s in (-1, 1):
        y = s * 0.0
        for (xa, xb) in ((-0.98, -0.12), (-0.02, 0.84)):
            # trapezoid inset on the slanted-in cabin side: interpolate the side plane
            def side_pt(x, z):
                t = (z - c["z0"]) / (c["z1"] - c["z0"])
                yy = c["yb"] + (c["yt"] - c["yb"]) * t
                return (x, s * (yy + 0.008), z)
            zb, zt = 1.05, 1.43
            # clip x to the trapezoid at that height
            def xlim(z, lo):
                t = (z - c["z0"]) / (c["z1"] - c["z0"])
                return (c["xb0"] + (c["xt0"] - c["xb0"]) * t + 0.1) if lo else (c["xb1"] + (c["xt1"] - c["xb1"]) * t - 0.1)
            pts = [side_pt(max(xa, xlim(zb, True)), zb), side_pt(min(xb, xlim(zb, False)), zb),
                   side_pt(min(xb, xlim(zt, False)), zt), side_pt(max(xa, xlim(zt, True)), zt)]
            pts2 = [(p[0], p[1] + s * 0.012, p[2]) for p in pts]
            hull(f"win_{s}_{xa}", pts + pts2, mat("glass"), g, ol=0.008)
    # windshield (front slope) and rear glass
    def slope_pts(front):
        xb, xt = (c["xb1"], c["xt1"]) if front else (c["xb0"], c["xt0"])
        f = 1 if front else -1
        out = []
        for t in (0.12, 0.9):
            x = xb + (xt - xb) * t
            z = c["z0"] + (c["z1"] - c["z0"]) * t
            yy = (c["yb"] + (c["yt"] - c["yb"]) * t) - 0.1
            out += [(x + f * 0.012, -yy, z), (x + f * 0.012, yy, z), (x + f * 0.03, -yy, z), (x + f * 0.03, yy, z)]
        return out
    hull("windshield", slope_pts(True), mat("glass"), g, ol=0.008)
    hull("rearglass", slope_pts(False), mat("glass"), g, ol=0.008)
    # cartoon glints on the windshield
    for i, (t0, w) in enumerate(((0.3, 0.07), (0.52, 0.035))):
        x = c["xb1"] + (c["xt1"] - c["xb1"]) * 0.5 + 0.035
        box(f"glint{i}", (0.01, w, 0.42), (x, -0.25 + i * 0.16, 1.24), emit("white", 0.9), g,
            rot=(28, -math.degrees(math.atan2(c["xb1"] - c["xt1"], c["z1"] - c["z0"])), 0))
    # wheels + dark arches
    for x in (-1.3, 1.3):
        for s in (-1, 1):
            cyl(f"arch_{x}_{s}", 0.45, 0.02, (x, s * (b["y"] + 0.004), 0.36), mat("dark"), g, axis="Y", seg=40)
            cyl(f"tyre_{x}_{s}", 0.36, 0.28, (x, s * 0.78, 0.36), mat("tyre"), g, axis="Y", bevel=0.05, ol=0.02)
            cyl(f"hub_{x}_{s}", 0.19, 0.04, (x, s * 0.925, 0.36), mat("hub"), g, axis="Y", bevel=0.01, ol=0.012)
    # lights, grille, seams, handles, mirrors
    for s in (-1, 1):
        box(f"headl_{s}", (0.04, 0.36, 0.13), (2.0, s * 0.56, 0.84), emit("white", 1.0), g, bevel=0.02, ol=0.012)
        box(f"taill_{s}", (0.04, 0.36, 0.12), (-2.0, s * 0.56, 0.84), mat("trim"), g, bevel=0.02, ol=0.012)
        box(f"mirror_{s}", (0.16, 0.14, 0.1), (0.92, s * 0.86, 1.06), mat("car"), g, bevel=0.03, ol=0.015)
        for x in (0.98, -0.07, -1.13):
            box(f"seam_{s}_{x}", (0.014, 0.01, 0.56), (x, s * (b["y"] + 0.003), 0.69), mat("black"), g)
        for x in (0.55, -0.55):
            box(f"handle_{s}_{x}", (0.16, 0.02, 0.035), (x, s * (b["y"] + 0.008), 0.86), mat("trim"), g, bevel=0.008)
    box("grille", (0.04, 0.62, 0.16), (2.0, 0, 0.62), mat("black"), g, bevel=0.02)
    box("bumper_line_f", (0.03, 1.64, 0.02), (2.005, 0, 0.47), mat("black"), g)
    box("bumper_line_r", (0.03, 1.64, 0.02), (-2.005, 0, 0.47), mat("black"), g)
    return g


# ----------------------------------------------------------------------------------------------------------------- dots
R_OUT, R_IN = 0.022, 0.012
DOT_SPACING = 0.07   # min centre distance -> typical nearest neighbour ~8 cm, matching the on-screen "~8 CM"


def poisson(w, h, r, rng, mask=lambda u, v: True):
    cell = r / math.sqrt(2)
    grid = {}
    pts = []
    tries = int(w * h / (r * r) * 6)
    for _ in range(tries):
        u, v = rng.uniform(0, w), rng.uniform(0, h)
        if not mask(u, v):
            continue
        gi, gj = int(u / cell), int(v / cell)
        ok = True
        for di in range(-2, 3):
            for dj in range(-2, 3):
                q = grid.get((gi + di, gj + dj))
                if q and (q[0] - u) ** 2 + (q[1] - v) ** 2 < r * r:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            grid[(gi, gj)] = (u, v)
            pts.append((u, v))
    return pts


def gen_car_dots(seed=7):
    """Marker dots scattered randomly (never in rows) over the painted body: hood, trunk, roof, sides, front, rear."""
    rng = random.Random(seed)
    b, c = CAR_BODY, CAB
    dots = []

    def add(region, origin, U, V, w, h, n, mask=lambda u, v: True):
        O, U, V, N = Vector(origin), Vector(U), Vector(V), Vector(n)
        for u, v in poisson(w, h, DOT_SPACING, rng, mask):
            dots.append(dict(p=O + U * u + V * v, n=N, region=region))

    def wheel_ok(x, z):
        return all((x - wx) ** 2 + (z - 0.36) ** 2 > 0.5 ** 2 for wx in (-1.3, 1.3))

    # hood / trunk tops
    add("hood", (1.05, -0.78, b["z1"]), (1, 0, 0), (0, 1, 0), 0.88, 1.56, (0, 0, 1))
    add("trunk", (-1.92, -0.78, b["z1"]), (1, 0, 0), (0, 1, 0), 0.72, 1.56, (0, 0, 1))
    # roof
    add("roof", (c["xt0"] + 0.03, -c["yt"] + 0.04, c["z1"]), (1, 0, 0), (0, 1, 0), c["xt1"] - c["xt0"] - 0.06,
        2 * c["yt"] - 0.08, (0, 0, 1))
    # sides (door panels, fenders, quarters) - not over the wheel arches, seams are fine
    for s in (-1, 1):
        add("side_n" if s < 0 else "side_f", (-1.94, s * b["y"], 0.42), (1, 0, 0), (0, 0, 1), 3.88, 0.5, (0, s, 0),
            mask=lambda u, v: wheel_ok(-1.94 + u, 0.42 + v))
    # front and rear faces, avoiding lights and grille
    def front_ok(u, v):
        y, z = -0.78 + u, 0.42 + v
        if z > 0.76 and abs(abs(y) - 0.56) < 0.22:
            return False
        if abs(y) < 0.36 and 0.52 < z < 0.72:
            return False
        return abs(z - 0.47) > 0.025
    add("front", (b["x1"], -0.78, 0.42), (0, 1, 0), (0, 0, 1), 1.56, 0.5, (1, 0, 0), mask=front_ok)
    add("rear", (b["x0"], -0.78, 0.42), (0, 1, 0), (0, 0, 1), 1.56, 0.5, (-1, 0, 0), mask=front_ok)
    order = list(range(len(dots)))
    rng.shuffle(order)
    for rank, i in enumerate(order):
        dots[i]["order"] = rank / max(1, len(dots) - 1)
    return dots


def make_dots(name, dots, lit=(), pop=None, parent=None, seg=14):
    """One mesh for many marker dots: black ring disc + white centre (material 2 = lit sage ring)."""
    bm = bmesh.new()
    for i, d in enumerate(dots):
        p, n = Vector(d["p"]), Vector(d["n"]).normalized()
        s = d.get("s", 1.0) * (1.25 if pop == i else 1.0) * (1.3 if i in lit else 1.0)
        t = n.orthogonal().normalized()
        t2 = n.cross(t)
        rot = d.get("spin", 0.0)
        for layer, (r, off, mi) in enumerate(((R_OUT, 0.003, 2 if i in lit else 0), (R_IN, 0.0055, 1))):
            vs = []
            for k in range(seg):
                a = 2 * math.pi * k / seg + rot
                vs.append(bm.verts.new(p + n * off + (t * math.cos(a) + t2 * math.sin(a)) * r * s))
            f = bm.faces.new(vs)
            f.material_index = mi
    return new_obj(name, bm, [mat("black"), mat("white"), emit("sage_l", 2.2)], parent)


# ----------------------------------------------------------------------------------------------------------------- characters
class Char:
    pass


def build_char(name, S):
    ch = Char()
    ch.S = S
    ch.root = empty(name)
    ch.hips = empty(f"{name}_hips", ch.root, (0, 0, S["leg"][2]))
    bev, ol = S["bevel"], S["ol"]
    lw, ld, lh = S["leg"]
    bw, bd, bh = S["body"]
    hw, hd, hh = S["head"]
    ch.legs, ch.arms, ch.elbows, ch.hands = {}, {}, {}, {}
    for side, sx in (("L", 1), ("R", -1)):
        lp = empty(f"{name}_leg{side}", ch.hips, (sx * S["leg_x"], 0, 0))
        box(f"{name}_legm{side}", (lw, ld, lh), (0, 0, -lh / 2), mat(S["pants"]), lp, bev, ol)
        box(f"{name}_shoe{side}", (lw * 1.08, ld * 1.35, 0.08), (0, -ld * 0.18, -lh + 0.04), mat(S["shoe"]), lp, bev, ol)
        ch.legs[side] = lp
        aw, ad, au = S["arm_up"]
        al = S["arm_lo"]
        sh = empty(f"{name}_arm{side}", ch.hips, (sx * (bw / 2 + aw / 2 + 0.01), 0, bh - aw * 0.55))
        box(f"{name}_up{side}", (aw, ad, au), (0, 0, -au / 2 + aw * 0.3), mat(S["top"]), sh, bev, ol)
        el = empty(f"{name}_elbow{side}", sh, (0, 0, -au + aw * 0.3))
        box(f"{name}_lo{side}", (aw * 0.94, ad * 0.94, al), (0, 0, -al / 2), mat(S["sleeve"]), el, bev, ol)
        hd_ = empty(f"{name}_hand{side}", el, (0, 0, -al))
        hs = S["hand"]
        box(f"{name}_handm{side}", (hs, hs, hs * 0.85), (0, 0, -hs * 0.4), mat("skin"), hd_, bev, ol)
        ch.arms[side], ch.elbows[side], ch.hands[side] = sh, el, hd_
    box(f"{name}_body", (bw, bd, bh), (0, 0, bh / 2), mat(S["top"]), ch.hips, bev * 1.4, ol)
    if S.get("patch"):
        box(f"{name}_patch", (0.17, 0.01, 0.1), (bw * 0.22, -bd / 2 - 0.004, bh * 0.72), mat("patch"), ch.hips, 0.004)
    if S.get("belt"):
        box(f"{name}_belt", (bw * 1.01, bd * 1.01, 0.06), (0, 0, 0.08), mat("dark"), ch.hips, 0.01)
    if S.get("pocket"):
        box(f"{name}_pocket", (bw * 0.5, 0.012, bh * 0.22), (0, -bd / 2 - 0.004, bh * 0.28), mat(S["pocket"]), ch.hips, 0.01)
    ch.neck = empty(f"{name}_head", ch.hips, (0, 0, bh + 0.005))
    box(f"{name}_headm", (hw, hd, hh), (0, 0, hh / 2), mat("skin"), ch.neck, bev * 1.6, ol)
    fy = -hd / 2
    ew, eh = S["eye"]
    ch.eyes, ch.pupils, ch.lids, ch.brows = [], [], [], []
    for sx in (1, -1):
        # round disc eyes on block heads (our own face design): white disc, round pupil, a skin-coloured block lid
        e = cyl(f"{name}_eye{sx}", ew / 2, 0.03, (sx * S["eye_x"], fy - 0.012, S["eye_z"]), mat("white"), ch.neck, axis="Y",
                seg=32, ol=S["ol"] * 0.6)
        e.scale = (1, 1, eh / ew)
        pw = ew * S["pupil"]
        p = cyl(f"{name}_pupil{sx}", pw / 2, 0.02, (0, -0.018, 0), mat("black"), e, axis="Y", seg=24)
        cyl(f"{name}_glint{sx}", pw * 0.14, 0.004, (pw * 0.18, -0.011, pw * 0.2), emit("white", 1.0), p, axis="Y", seg=12)
        lid_piv = empty(f"{name}_lidp{sx}", e, (0, -0.022, ew / 2 + 0.002))
        lid = box(f"{name}_lid{sx}", (ew * 1.08, 0.03, ew * 1.04), (0, 0, -ew * 0.52), mat(S["lid"]), lid_piv, 0.004)
        br = box(f"{name}_brow{sx}", (ew * 1.15, 0.03, S["brow_h"]), (sx * S["eye_x"], fy - 0.02, S["eye_z"] + eh / 2 + 0.035),
                 mat(S["brow"]), ch.neck, 0.006)
        ch.eyes.append(e)
        ch.pupils.append(p)
        ch.lids.append(lid_piv)
        ch.brows.append(br)
    mw, mh = S["mouth"]
    ch.mouth = box(f"{name}_mouth", (mw, 0.03, mh), (0, fy - 0.01, S["mouth_z"]), mat("black"), ch.neck, 0.006)
    ch.mouth_in = box(f"{name}_tongue", (mw * 0.6, 0.02, mh * 0.35), (0, -0.003, -mh * 0.22), mat("#b2534a"), ch.mouth, 0.004)
    if S.get("hair"):
        box(f"{name}_hair", (hw * 1.03, hd * 1.03, 0.06), (0, 0.0, hh + 0.005), mat("dark"), ch.neck, 0.02, ol)
        box(f"{name}_fringe", (hw * 0.55, 0.06, 0.1), (-hw * 0.2, -hd / 2 - 0.0, hh - 0.03), mat("dark"), ch.neck, 0.02, ol,
            rot=(0, -12, 0))
        box(f"{name}_tuft", (0.07, 0.11, 0.15), (0.06, 0.0, hh + 0.09), mat("dark"), ch.neck, 0.02, ol, rot=(0, 30, 0))
    if S.get("cap"):
        box(f"{name}_cap", (hw * 1.08, hd * 1.08, 0.11), (0, 0.0, hh + 0.04), mat(S["cap"]), ch.neck, 0.025, ol)
        box(f"{name}_brim", (hw * 1.0, hd * 0.55, 0.03), (0, -hd * 0.7, hh + 0.005), mat(S["cap"]), ch.neck, 0.01, ol)
    pose(ch)
    return ch


def pose(ch, loc=None, rz=0.0, hips=(0, 0, 0), head=(0, 0, 0), armL=(0, 0, 8), armR=(0, 0, -8), elbowL=-10, elbowR=-10,
         legL=(0, 0, 0), legR=(0, 0, 0), mouth=0.0, lid=0.0, look=(0, 0), brow=(0, 0)):
    """Angles in degrees. x>0 leans/nods forward; armX<0 swings an arm forward/up; mouth 0 closed..1 open;
    lid 0 open..1 shut; look = pupil offset (-1..1 screen x, -1..1 up); brow = (raise in m, tilt deg, inner up > 0)."""
    S = ch.S
    if loc is not None:
        ch.root.location = loc
    ch.root.rotation_euler = (0, 0, math.radians(rz))
    R = lambda t: [math.radians(a) for a in t]
    ch.hips.rotation_euler = R(hips)
    ch.neck.rotation_euler = R(head)
    ch.arms["L"].rotation_euler = R(armL)
    ch.arms["R"].rotation_euler = R(armR)
    ch.elbows["L"].rotation_euler = R((elbowL, 0, 0))
    ch.elbows["R"].rotation_euler = R((elbowR, 0, 0))
    ch.legs["L"].rotation_euler = R(legL)
    ch.legs["R"].rotation_euler = R(legR)
    mw, mh = S["mouth"]
    ch.mouth.scale = (1.0 - 0.25 * mouth, 1, 0.22 + 0.78 * mouth)
    ch.mouth_in.hide_render = mouth < 0.4
    ew, eh = S["eye"]
    pw = ew * S["pupil"]
    for i, p in enumerate(ch.pupils):
        p.location = (look[0] * (ew - pw) * 0.45, -0.018, look[1] * (ew - pw) * 0.45)
    base_lid = S.get("base_lid", 0.0)
    for lp in ch.lids:
        f = max(base_lid, lid)
        lp.scale = (1, 1, max(0.001, f))
        lp.children[0].hide_render = f < 0.02
    for i, br in enumerate(ch.brows):
        sx = 1 if i == 0 else -1
        br.location.z = S["eye_z"] + eh / 2 + 0.035 + brow[0]
        br.rotation_euler = (0, math.radians(-sx * brow[1]), 0)


PIP_SPEC = dict(leg=(0.13, 0.15, 0.26), leg_x=0.095, body=(0.44, 0.3, 0.36), head=(0.54, 0.46, 0.48),
                arm_up=(0.11, 0.13, 0.2), arm_lo=0.17, hand=0.11, eye=(0.15, 0.17), eye_x=0.13, eye_z=0.27, pupil=0.5,
                mouth=(0.15, 0.1), mouth_z=0.1, brow_h=0.03, top="pip_top", sleeve="pip_top", pants="pip_pants",
                shoe="shoe", lid="skin", brow="dark", hair=True, pocket="#69997a", bevel=0.025, ol=0.014)
GUS_SPEC = dict(leg=(0.24, 0.26, 0.84), leg_x=0.17, body=(0.78, 0.44, 0.82), head=(0.36, 0.34, 0.36),
                arm_up=(0.17, 0.19, 0.4), arm_lo=0.36, hand=0.17, eye=(0.085, 0.09), eye_x=0.08, eye_z=0.19, pupil=0.55,
                mouth=(0.12, 0.07), mouth_z=0.07, brow_h=0.025, top="gus_suit", sleeve="gus_suit", pants="gus_suit",
                shoe="dark", lid="skin", brow="dark", cap="gus_cap", patch=True, belt=True, base_lid=0.45,
                bevel=0.03, ol=0.018)


# ----------------------------------------------------------------------------------------------------------------- props
def build_clock(parent=None, loc=(-4.0, 3.56, 2.75), r=0.42):
    g = empty("CLOCK", parent, loc)
    cyl("clock_rim", r + 0.05, 0.08, (0, 0, 0), mat("black"), g, axis="Y", seg=48, bevel=0.02)
    cyl("clock_face", r, 0.09, (0, -0.005, 0), mat("white"), g, axis="Y", seg=48)
    for k in range(12):
        a = 2 * math.pi * k / 12
        L = 0.09 if k % 3 == 0 else 0.05
        rr = r - 0.03 - L / 2
        box(f"tick{k}", (0.025 if k % 3 == 0 else 0.016, 0.01, L), (rr * math.sin(a), -0.055, rr * math.cos(a)), mat("black"), g,
            rot=(0, math.degrees(a), 0))
    hands = {}
    for nm, L, w, m, y in (("hour", 0.22, 0.04, mat("black"), -0.06), ("minute", 0.33, 0.028, mat("black"), -0.068),
                           ("second", 0.36, 0.012, mat("red"), -0.076)):
        piv = empty(f"clock_{nm}", g, (0, y, 0))
        box(f"clock_{nm}_m", (w, 0.006, L), (0, 0, L / 2 - 0.04), m, piv, 0.002)
        hands[nm] = piv
    cyl("clock_pin", 0.03, 0.02, (0, -0.082, 0), mat("red"), g, axis="Y")
    return g, hands


def clock_blur(clock_g, hands, r=0.42):
    """Hands spinning 'like a fan': trailing ghost copies (see-through) + whirr strokes beside the clock."""
    objs = []
    for nm, L, w, key, y, n, step in (("minute", 0.33, 0.028, "black", -0.07, 9, 14), ("second", 0.36, 0.014, "red", -0.078, 12, 11)):
        for i in range(n):
            a = hands[nm].rotation_euler.y - math.radians(step * (i + 1))
            alpha = 0.55 * (1 - i / n)
            piv = empty(f"blur_{nm}{i}", clock_g, (0, y - 0.0005 * i, 0), (0, math.degrees(a), 0))
            objs.append(piv)
            box(f"blur_{nm}{i}m", (w * 1.6, 0.004, L), (0, 0, L / 2 - 0.04), mat(key, alpha), piv)
    # whirr strokes: short arcs outside the rim
    for side in (1, -1):
        for j, rr in enumerate((r + 0.14, r + 0.24)):
            for k in range(7):
                a = math.radians(side * (55 + 6 * k + 8 * j))
                o = box(f"whirr{side}{j}{k}", (0.03, 0.01, 0.045), (rr * math.sin(a), -0.03, rr * math.cos(a)), mat("black"), clock_g,
                        rot=(0, math.degrees(a) + 90, 0))
                objs.append(o)
    return objs


def build_scanner(parent=None):
    """Generic handheld scanner: a grey body, grip, sage lens window. No brand, no screen text."""
    g = empty("SCANNER", parent)
    box("scn_body", (0.12, 0.22, 0.13), (0, 0, 0), mat("metal"), g, 0.025, 0.012)
    box("scn_grip", (0.07, 0.08, 0.17), (0, 0.07, -0.13), mat("dark"), g, 0.02, 0.012, rot=(-15, 0, 0))
    box("scn_lens", (0.09, 0.01, 0.08), (0, -0.112, 0.005), emit("sage_l", 1.6), g, 0.005)
    box("scn_screen", (0.08, 0.06, 0.005), (0, 0.04, 0.067), emit("#3d5d47", 1.0), g, 0.003)
    return g


def light_cone(name, apex, target, radius):
    """Translucent sage light cone from the scanner lens to the panel."""
    apex, target = Vector(apex), Vector(target)
    L = (target - apex).length
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=False, segments=40, radius1=radius, radius2=0.01, depth=L)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, -L / 2))   # apex at origin, base at -L along local Z
    ob = new_obj(name, bm, [emit("sage_l", 1.3, 0.16)])
    ob.location = apex
    ob.rotation_euler = (target - apex).to_track_quat("-Z", "Y").to_euler()
    ring = cyl(name + "_spot", radius, 0.003, (0, 0, -L + 0.004), emit("sage_l", 1.0, 0.16), ob, seg=48)
    return ob


def build_roll(parent=None):
    g = empty("ROLL", parent)
    cyl("roll_tape", 0.085, 0.11, (0, 0, 0), mat("white"), g, axis="X", bevel=0.01, ol=0.012)
    cyl("roll_core", 0.04, 0.115, (0, 0, 0), mat("sage"), g, axis="X")
    return g


def strip_path(name, pts, width, dots_every=0.07, rng=None):
    """A ribbon (the unrolled dot strip) through 3D points, with marker dots printed on it."""
    rng = rng or random.Random(3)
    bm = bmesh.new()
    left, right = [], []
    for i, p in enumerate(pts):
        p = Vector(p)
        q = Vector(pts[min(i + 1, len(pts) - 1)]) - Vector(pts[max(i - 1, 0)])
        side = Vector((1, 0, 0))
        left.append(bm.verts.new(p - side * width / 2))
        right.append(bm.verts.new(p + side * width / 2))
    for i in range(len(pts) - 1):
        bm.faces.new((left[i], right[i], right[i + 1], left[i + 1]))
    ob = new_obj(name, bm, [mat("white")])
    # dots along the strip (staggered, a strip of markers as sold on a roll)
    dl = []
    acc = 0.0
    for i in range(len(pts) - 1):
        a, b = Vector(pts[i]), Vector(pts[i + 1])
        seg = (b - a).length
        while acc < seg:
            p = a + (b - a) * (acc / seg)
            t = (b - a).normalized()
            n = t.cross(Vector((1, 0, 0))).normalized()
            if n.y > 0:
                n = -n
            dl.append(dict(p=p + Vector((rng.uniform(-0.02, 0.02), 0, 0)) + n * 0.001, n=n, s=0.8))
            acc += dots_every
        acc -= seg
    d = make_dots(name + "_dots", dl)
    return ob, d


def build_laptop(parent=None, loc=(3.35, 3.05, 0.955), rz=0):
    g = empty("LAPTOP", parent, loc, (0, 0, rz))
    box("lap_base", (0.46, 0.32, 0.025), (0, 0, 0.0125), mat("metal"), g, 0.01, 0.01)
    box("lap_keys", (0.4, 0.15, 0.003), (0, 0.03, 0.026), mat("dark"), g)
    box("lap_pad", (0.12, 0.07, 0.003), (0, -0.1, 0.026), mat("#7c817c"), g)
    hinge = empty("lap_hinge", g, (0, 0.16, 0.025), (-12, 0, 0))   # screen leans back 12 deg past vertical
    box("lap_lid", (0.46, 0.018, 0.31), (0, 0.009, 0.155), mat("metal"), hinge, 0.01, 0.01)
    scr = empty("lap_screen", hinge, (0, -0.0015, 0.16))
    box("lap_bezel", (0.44, 0.003, 0.29), (0, 0, 0), mat("black"), scr)
    ui = empty("lap_ui", scr, (0, -0.002, 0), (90, 0, 0))   # local XY = screen plane, +Z toward the viewer
    return g, ui


def jigsaw(w, h, tabs, r=None, n=10):
    """Rectangle polygon (centred) with round tabs: tabs = dict(edge -> +1 out / -1 in) for 'top','right','bottom','left'."""
    r = r or min(w, h) * 0.16
    pts = []
    corners = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    edges = ["bottom", "right", "top", "left"]
    for k in range(4):
        a, b = Vector(corners[k]), Vector(corners[(k + 1) % 4])
        pts.append(tuple(a))
        t = tabs.get(edges[k], 0)
        if t:
            d = (b - a)
            mid = a + d * 0.5
            nrm = Vector((d.y, -d.x)).normalized() * t   # outward normal for CCW polygon is (dy, -dx)
            ux = d.normalized()
            pts.append(tuple(mid - ux * r * 0.7))
            for i in range(n + 1):
                ang = math.pi * (1 - i / n)
                c = mid + nrm * r * 0.85
                p = c + ux * math.cos(ang) * r + nrm * math.sin(ang) * r * 0.9
                pts.append(tuple(p))
            pts.append(tuple(mid + ux * r * 0.7))
    return pts


def build_screen_ui(ui):
    """Laptop screen: car-section mesh pieces as jigsaw pieces; the roof piece is being dragged in; 3 colour-coded pin pairs."""
    objs = []
    bg = poly("ui_bg", [(-0.205, -0.135), (0.205, -0.135), (0.205, 0.135), (-0.205, 0.135)], emit("#141614", 1.0), ui, z=0.0)
    objs.append(bg)
    # window chrome strip (no text)
    objs.append(poly("ui_bar", [(-0.205, 0.118), (0.205, 0.118), (0.205, 0.135), (-0.205, 0.135)], emit("#2a2d2a", 1.0), ui, z=0.0005))
    for i, c in enumerate(("red", "sage_l", "white")):
        objs.append(cyl(f"ui_dot{i}", 0.0045, 0.0005, (-0.19 + i * 0.013, 0.1265, 0.001), emit(c, 1.0), ui, seg=12))
    W, H = 0.105, 0.07
    base_y = -0.06
    pieces = [("rear", -0.105, base_y, {"right": 1}, "ui_piece2"),
              ("mid", 0.0, base_y, {"left": -1, "right": 1, "top": -1}, "ui_piece"),
              ("front", 0.105, base_y, {"left": -1}, "ui_piece2")]
    for nm, x, y, tabs, col in pieces:
        objs.append(poly(f"ui_{nm}", jigsaw(W * 0.97, H * 0.97, tabs), emit(col, 1.0), ui, loc=(x, y, 0.001)))
    # the dragged roof piece: offset up-right, slightly rotated
    roof_loc = (0.045, 0.045, 0.002)
    roof = poly("ui_roof", jigsaw(W * 1.25, H * 0.8, {"bottom": 1}), emit("#c9cec9", 1.0), ui, loc=roof_loc, rot=(0, 0, 9))
    objs.append(roof)
    # pins: three on the roof piece, three targets on the middle piece; joined by lines
    pin_cols = ["sage_l", "white", "pin_blue"]
    src_local = [(-0.045, -0.012), (0.0, 0.018), (0.045, -0.01)]
    ang = math.radians(9)
    tgt = [(-0.04, base_y + 0.032), (0.005, base_y + 0.05), (0.048, base_y + 0.034)]
    for i, (sl, tg, c) in enumerate(zip(src_local, tgt, pin_cols)):
        sx = roof_loc[0] + sl[0] * math.cos(ang) - sl[1] * math.sin(ang)
        sy = roof_loc[1] + sl[0] * math.sin(ang) + sl[1] * math.cos(ang)
        objs.append(cyl(f"pin_s{i}", 0.0065, 0.0006, (sx, sy, 0.004), emit(c, 1.3), ui, axis="Z", seg=16))
        objs.append(cyl(f"pin_sr{i}", 0.0085, 0.0005, (sx, sy, 0.0035), emit("black", 1.0), ui, axis="Z", seg=16))
        objs.append(cyl(f"pin_t{i}", 0.0065, 0.0006, (tg[0], tg[1], 0.004), emit(c, 1.3), ui, axis="Z", seg=16))
        objs.append(cyl(f"pin_tr{i}", 0.0085, 0.0005, (tg[0], tg[1], 0.0035), emit("black", 1.0), ui, axis="Z", seg=16))
        # dashed line source -> target
        a, b = Vector((sx, sy)), Vector(tg)
        d = b - a
        nseg = 6
        for k in range(nseg):
            if k % 2:
                continue
            p0 = a + d * (k / nseg)
            p1 = a + d * ((k + 1) / nseg)
            nrm = Vector((-d.y, d.x)).normalized() * 0.0012
            objs.append(poly(f"pin_l{i}{k}", [tuple(p0 - nrm), tuple(p1 - nrm), tuple(p1 + nrm), tuple(p0 + nrm)], emit(c, 1.2), ui,
                             z=0.003))
    # cursor arrow (generic) grabbing the roof piece
    cur = [(0, 0), (0, -0.03), (0.008, -0.022), (0.014, -0.034), (0.019, -0.031), (0.013, -0.02), (0.024, -0.02)]
    objs.append(poly("ui_cursor", cur, emit("white", 1.2), ui, loc=(0.085, 0.06, 0.006)))
    curo = [(x * 1.25 - 0.002, y * 1.18 + 0.002) for x, y in cur]
    objs.append(poly("ui_cursor_o", curo, emit("black", 1.0), ui, loc=(0.085, 0.06, 0.0055)))
    return objs


def build_stool(loc):
    g = empty("STOOL", None, loc)
    cyl("stool_seat", 0.24, 0.06, (0, 0, 0.58), mat("wood"), g, bevel=0.015, ol=0.015)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.4
        box(f"stool_leg{k}", (0.045, 0.045, 0.6), (0.15 * math.cos(a), 0.15 * math.sin(a), 0.28), mat("dark"), g, ol=0.01,
            rot=(math.degrees(-0.14 * math.sin(a)), math.degrees(0.14 * math.cos(a)), 0))
    return g


def dot_pile(name, center, n=170, radius=0.3, height=0.16, seed=5, s=1.0):
    rng = random.Random(seed)
    dl = []
    for _ in range(n):
        rr = radius * math.sqrt(rng.random())
        a = rng.uniform(0, 2 * math.pi)
        h = height * (1 - (rr / radius) ** 1.5) * rng.uniform(0.6, 1.0)
        nrm = Vector((rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5), rng.uniform(0.6, 1))).normalized()
        dl.append(dict(p=Vector(center) + Vector((rr * math.cos(a), rr * math.sin(a), h + 0.006)), n=nrm, s=s,
                       spin=rng.uniform(0, 6.3)))
    return make_dots(name, dl)


# ----------------------------------------------------------------------------------------------------------------- render setup
def setup_render():
    scn.render.engine = "CYCLES"
    cy = scn.cycles
    cy.device = "CPU"
    cy.samples = SPP
    cy.use_adaptive_sampling = False
    cy.use_denoising = True
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    cy.max_bounces = 4
    cy.diffuse_bounces = 2
    cy.glossy_bounces = 1
    cy.transmission_bounces = 1
    cy.volume_bounces = 0
    cy.transparent_max_bounces = 16
    cy.caustics_reflective = False
    cy.caustics_refractive = False
    cy.blur_glossy = 1.0
    scn.render.use_persistent_data = False
    scn.render.threads_mode = "FIXED"
    scn.render.threads = THREADS
    scn.render.resolution_x = 1080
    scn.render.resolution_y = 1920
    scn.render.resolution_percentage = int(round(SCALE * 100))
    scn.render.film_transparent = False
    scn.render.use_motion_blur = False
    scn.view_settings.view_transform = "Standard"
    scn.view_settings.look = "None"
    scn.view_settings.exposure = 0.0
    scn.render.image_settings.file_format = "PNG"
    scn.render.image_settings.color_mode = "RGB"
    scn.render.image_settings.compression = 15
    w = bpy.data.worlds.new("W")
    scn.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = w.node_tree.nodes.get("Background") or w.node_tree.nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = hexcol("#f4ece0")
    bg.inputs["Strength"].default_value = 0.55
    out = [n for n in w.node_tree.nodes if n.type == "OUTPUT_WORLD"]
    out = out[0] if out else w.node_tree.nodes.new("ShaderNodeOutputWorld")
    w.node_tree.links.new(bg.outputs[0], out.inputs["Surface"])
    sun_d = bpy.data.lights.new("sun", "SUN")
    sun_d.energy = 1.9
    sun_d.angle = math.radians(9)
    sun_d.color = hexcol("#fff6ea")[:3]
    sun = bpy.data.objects.new("sun", sun_d)
    COLL.objects.link(sun)
    sun.rotation_euler = (math.radians(42), math.radians(-18), math.radians(-28))
    cam_d = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cam_d)
    COLL.objects.link(cam)
    scn.camera = cam
    cam_d.sensor_fit = "VERTICAL"
    cam_d.sensor_height = 36.0
    cam_d.clip_start = 0.02
    cam_d.clip_end = 100
    return cam, sun


def look(cam, loc, target, lens, up=(0, 0, 1)):
    loc, target, up = Vector(loc), Vector(target), Vector(up)
    f = (target - loc).normalized()
    r = f.cross(up).normalized()
    u = r.cross(f)
    M = Matrix(((r.x, u.x, -f.x), (r.y, u.y, -f.y), (r.z, u.z, -f.z)))
    cam.matrix_world = Matrix.Translation(loc) @ M.to_4x4()
    cam.data.lens = lens
    cam.data.dof.use_dof = False


# ----------------------------------------------------------------------------------------------------------------- build all
cam, sun = setup_render()
SHOP = build_shop()
CAR = build_car()
CLOCK, HANDS = build_clock(SHOP)
PIP = build_char("PIP", PIP_SPEC)
GUS = build_char("GUS", GUS_SPEC)
SCANNER = build_scanner()
ROLL = build_roll()
LAPTOP, UI = build_laptop(SHOP)
build_screen_ui(UI)
STOOL = build_stool((-3.7, 2.7, 0))
ALL_DOTS = gen_car_dots()
print(f"[partA] {len(ALL_DOTS)} marker dots on the car", flush=True)

_temp = []


def temp(ob):
    _temp.append(ob)
    return ob


def reset():
    for ob in _temp:
        stack = [ob]
        while stack:
            o = stack.pop()
            stack.extend(o.children)
            try:
                bpy.data.objects.remove(o, do_unlink=True)
            except ReferenceError:
                pass
    _temp.clear()
    for ob in (SCANNER, ROLL, STOOL):
        set_vis(ob, False)
    set_vis(PIP.root, True)
    set_vis(GUS.root, True)
    pose(PIP, loc=(30, 30, 0))
    pose(GUS, loc=(31, 30, 0))
    HANDS["hour"].rotation_euler = (0, math.radians(300), 0)
    HANDS["minute"].rotation_euler = (0, math.radians(60), 0)
    HANDS["second"].rotation_euler = (0, math.radians(200), 0)
    SCANNER.parent = None
    ROLL.parent = None


def dots_where(pred):
    return [d for d in ALL_DOTS if pred(d)]


def attach(prop, hand, loc=(0, 0, 0), rot=(0, 0, 0)):
    prop.parent = hand
    prop.location = loc
    prop.rotation_euler = [math.radians(a) for a in rot]
    set_vis(prop, True)


# ----------------------------------------------------------------------------------------------------------------- shots
def shot_S1():
    """Hook: 3/4 of the shop, sedan behind, PIP hops up at GUS and asks."""
    temp(make_dots("dots", []))
    pose(PIP, loc=(0.85, -2.35, 0.07), rz=-40, hips=(-6, 0, 0), head=(-20, 0, 0), armL=(-150, 0, -20), armR=(-30, 0, -22),
         elbowL=-20, elbowR=-50, legL=(-15, 0, 0), legR=(20, 0, 0), mouth=0.85, look=(-0.5, 0.9), brow=(0.035, -12))
    pose(GUS, loc=(-0.45, -1.95, 0), rz=30, head=(6, 0, -22), armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12, elbowR=-12,
         mouth=0.0, look=(0.8, -0.4), brow=(0.0, 0))
    look(cam, (2.0, -5.5, 1.15), (0.05, -1.4, 0.98), 26)


def shot_S2():
    """GUS holds up the dot roll; the strip unrolls to the floor. PIP's head at the frame edge."""
    pose(GUS, loc=(0.2, -1.7, 0), rz=10, hips=(-3, 0, 0), head=(-14, 0, 10), armL=(-165, 0, 4), armR=(-25, 0, -14), elbowL=-6,
         elbowR=-60, mouth=0.75, look=(0.3, 0.9), brow=(0.02, 0))
    attach(ROLL, GUS.hands["L"], (0, -0.02, -0.16), (0, 0, 8))
    bpy.context.view_layer.update()
    rp = ROLL.matrix_world.translation
    pts = [rp + Vector((0.0, -0.09, -0.02))]
    for i in range(1, 14):
        t = i / 13
        pts.append(rp + Vector((0.03 * math.sin(t * 5), -0.09 - 0.12 * t - 0.05 * math.sin(t * 3.1), -(rp.z - 0.012) * t ** 1.05)))
    last = pts[-1]
    for i in range(1, 9):   # curl along the floor toward the camera
        pts.append(Vector((last.x + 0.02 * i, last.y - 0.09 * i, 0.012 + 0.04 * max(0, (i - 6)) ** 1.5)))
    s, d = strip_path("strip", pts, 0.1)
    temp(s); temp(d)
    pose(PIP, loc=(0.95, -2.45, 0), rz=-30, head=(-26, 0, 0), mouth=0.0, look=(-0.7, 1), brow=(0.03, -14),
         armL=(-20, 0, 10), armR=(-20, 0, -10))
    look(cam, (0.95, -5.0, 1.55), (0.3, -1.7, 1.55), 34)


def shot_S3():
    """Close on the front door: GUS's block hand slaps dots on, randomly spaced (~8 cm), one popping in."""
    near = dots_where(lambda d: d["region"] == "side_n" and -0.5 < d["p"].x < 1.15)
    shown = [d for d in near if d["order"] < 0.55]
    pop_i = min(range(len(shown)), key=lambda i: (shown[i]["p"].x - 0.5) ** 2 + (shown[i]["p"].z - 0.66) ** 2)
    temp(make_dots("dots", shown, pop=pop_i))
    pd = shown[pop_i]["p"]
    for k in range(6):   # impact dashes around the dot that just went on
        a = math.radians(-20 + k * 40)
        r0 = 0.062
        temp(box(f"pop{k}", (0.007, 0.004, 0.026), (pd.x + r0 * math.cos(a), -0.862, pd.z + r0 * math.sin(a)), mat("black"),
                 rot=(0, -math.degrees(a) + 90, 0)))
    set_vis(GUS.root, False)
    hx, hz = pd.x + 0.17, pd.z + 0.06   # palm just right of the new dot, flat on the panel
    temp(box("s3_arm", (0.55, 0.2, 0.2), (hx + 0.38, -1.0, hz + 0.1), mat("gus_suit"), None, 0.03, 0.018, rot=(0, -14, 20)))
    temp(box("s3_cuff", (0.06, 0.21, 0.21), (hx + 0.11, -0.97, hz + 0.03), mat("dark"), None, 0.02, 0.016, rot=(0, -14, 20)))
    temp(box("s3_hand", (0.17, 0.1, 0.18), (hx, -0.92, hz), mat("skin"), None, 0.035, 0.016, rot=(0, -14, 8)))
    temp(box("s3_thumb", (0.08, 0.06, 0.05), (hx - 0.06, -0.915, hz + 0.075), mat("skin"), None, 0.015, 0.012, rot=(0, 30, 8)))
    look(cam, (0.3, -2.25, 0.86), (0.33, -0.85, 0.7), 40)


def shot_S4():
    """High-angle time-lapse (car's length up the frame): dots spreading over the car, GUS zipping round its nose."""
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.72)))
    pose(GUS, loc=(2.55, -0.95, 0), rz=-140, hips=(32, 0, 0), head=(-25, 0, 0), armL=(-70, 0, 0), armR=(50, 0, 0),
         elbowL=-60, elbowR=-60, legL=(-45, 0, 0), legR=(40, 0, 0), mouth=0.3)
    for i in range(4):   # motion streaks on the floor behind him
        temp(box(f"speed{i}", (0.75 - 0.12 * i, 0.03, 0.006), (2.0 - 0.1 * i, -1.35 - 0.16 * i, 0.01), mat("black"), rot=(0, 0, 40)))
    look(cam, (-2.6, -1.2, 6.0), (0.25, -0.2, 0.6), 34, up=(1, 0, 0))


def pick_four(dots, region, x_rng, z_rng, want=(1.5, 0.8), seed=11):
    """Find a spot on the panel where a cone lights exactly 4 dots with clear margins (never a 5th)."""
    rng = random.Random(seed)
    idx = [i for i, d in enumerate(dots) if d["region"] == region]
    best = None
    for _ in range(4000):
        c = Vector((rng.uniform(*x_rng), dots[idx[0]]["p"].y, rng.uniform(*z_rng)))
        ds = sorted(((dots[i]["p"] - c).length, i) for i in idx)
        inner, outer = ds[3][0] + R_IN + 0.004, ds[4][0] - R_IN - 0.004   # 4 white centres inside, the 5th's outside
        if inner < outer:
            score = (c.x - want[0]) ** 2 + (c.z - want[1]) ** 2 - (outer - inner) * 0.5
            if best is None or score < best[0]:
                best = (score, c, [i for _, i in ds[:4]], (inner + outer) / 2)
    return best[1], best[2], best[3]


def shot_S5():
    """GUS in profile at the front fender (over-the-shoulder hid the cone at phone size): the cone lights exactly 4 dots."""
    dots = ALL_DOTS
    cen, lit, radius = pick_four(dots, "side_n", (1.3, 1.65), (0.66, 0.86))
    temp(make_dots("dots", dots, lit=set(lit)))
    pose(GUS, loc=(1.3, -1.95, 0), rz=180 - 6, hips=(14, 0, 0), head=(24, 0, 0), armL=(-70, 0, -4), elbowL=-28,
         armR=(-64, 0, 10), elbowR=-36, mouth=0.6, look=(0, -1))
    bpy.context.view_layer.update()
    hp = (GUS.hands["L"].matrix_world.translation + GUS.hands["R"].matrix_world.translation) / 2
    set_vis(SCANNER, True)
    SCANNER.location = hp + (cen - hp).normalized() * 0.12 + Vector((0, 0, 0.05))
    SCANNER.rotation_euler = (cen - SCANNER.location).to_track_quat("-Y", "Z").to_euler()
    bpy.context.view_layer.update()
    lens = SCANNER.matrix_world @ Vector((0, -0.12, 0.005))
    temp(light_cone("cone", lens, cen + Vector((0, -0.004, 0)), radius))
    print(f"[partA] S5 cone: {len(lit)} dots lit, radius {radius:.3f} m, centre {tuple(round(v, 2) for v in cen)}", flush=True)
    look(cam, (3.3, -2.55, 1.35), (1.42, -1.05, 0.98), 42)


def scan_patch_mat(alpha, key="scan"):
    """See-through 'scan data' grey, front faces only (back faces fully transparent so the colour doesn't stack)."""
    name = f"scanpatch_{key}_{alpha:.2f}"
    if name in _MATS:
        return _MATS[name]
    m, nt, out = _new_mat(name)
    d = nt.nodes.new("ShaderNodeBsdfDiffuse")
    d.inputs["Color"].default_value = hexcol(PAL.get(key, key))
    t = nt.nodes.new("ShaderNodeBsdfTransparent")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(geo.outputs["Backfacing"], inv.inputs[1])
    nt.links.new(inv.outputs[0], mul.inputs[0])
    mul.inputs[1].default_value = alpha
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mul.outputs[0], mx.inputs[0])
    nt.links.new(t.outputs[0], mx.inputs[1])
    nt.links.new(d.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    _MATS[name] = m
    return m


def shot_S6():
    """The car in overlapping scan sections: front, side and roof patches captured (lifted off slightly), rear not yet."""
    temp(make_dots("dots", ALL_DOTS))
    b = CAR_BODY
    tmpme = bpy.data.meshes.new("tmp")
    base = bmesh.new()
    bmesh.ops.create_cube(base, size=1.0)
    for v in base.verts:
        v.co = Vector((v.co.x * (b["x1"] - b["x0"]) * 1.012, v.co.y * 2 * b["y"] * 1.03,
                       (b["z0"] + b["z1"]) / 2 + v.co.z * (b["z1"] - b["z0"]) * 1.03))
    vs = [base.verts.new(p) for p in cabin_pts(0.025)]
    res = bmesh.ops.convex_hull(base, input=vs)
    bmesh.ops.delete(base, geom=res["geom_interior"], context="VERTS")
    base.to_mesh(tmpme)
    base.free()

    def patch(name, xr, yr, zr, offset, alpha, key="scan"):
        bm = bmesh.new()
        bm.from_mesh(tmpme)
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=10, use_grid_fill=True)
        for co, no in (((xr[0], 0, 0), (-1, 0, 0)), ((xr[1], 0, 0), (1, 0, 0)), ((0, yr[0], 0), (0, -1, 0)),
                       ((0, yr[1], 0), (0, 1, 0)), ((0, 0, zr[0]), (0, 0, -1)), ((0, 0, zr[1]), (0, 0, 1))):
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no, clear_outer=True)
        bmesh.ops.translate(bm, verts=bm.verts, vec=offset)
        ob = new_obj(name, bm, [scan_patch_mat(alpha, key), OUTLINE])
        add_mods(ob, 0, 0.016)
        return temp(ob)

    # each captured section lifts off the car in its own direction; neighbours share an overlap band
    patch("patch_front", (0.75, 2.3), (-2, 2), (-1, 2), (0.75, 0.0, 0.15), 0.6, "#dfe2df")
    patch("patch_side", (-1.55, 1.2), (-2, -0.25), (-1, 1.05), (0.0, -0.75, 0.0), 0.6, "#c3c8c3")
    patch("patch_roof", (-1.35, 1.15), (-2, 2), (0.92, 2.0), (0.0, 0.0, 0.7), 0.6, "#eceeec")
    bpy.data.meshes.remove(tmpme)
    pose(GUS, loc=(-3.05, 0.55, 0), rz=-115, hips=(-4, 0, 0), head=(-22, 0, 20), armL=(-160, 0, -10), elbowL=-15,
         armR=(-10, 0, -15), elbowR=-20, mouth=0.65, look=(0.3, 1))
    attach(SCANNER, GUS.hands["L"], (0, -0.04, -0.12), (110, 0, 0))
    look(cam, (2.5, -4.9, 4.9), (0.1, -0.15, 0.85), 22)


def shot_S7():
    """Over GUS's shoulder onto the laptop: dragging the roof piece, three colour-coded pin pairs about to snap."""
    pose(GUS, loc=(3.85, 2.3, 0), rz=180 - 22, hips=(16, 0, 0), head=(24, 0, 0), armL=(-58, 0, 8), elbowL=-40,
         armR=(-58, 0, -4), elbowR=-40)
    look(cam, (2.72, 1.3, 1.8), (3.32, 3.13, 1.13), 86)


def shot_S8():
    """Wall clock spinning like a fan; PIP slumped on a stool underneath asks 'Is it done yet?'."""
    set_vis(STOOL, True)
    HANDS["minute"].rotation_euler = (0, math.radians(150), 0)
    HANDS["second"].rotation_euler = (0, math.radians(260), 0)
    for o in clock_blur(CLOCK, HANDS):
        temp(o)
    pose(PIP, loc=(-3.7, 2.68, 0.61), rz=-6, hips=(24, 0, 0), head=(10, 0, -8), armL=(-38, 0, 14), elbowL=-50,
         armR=(-38, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=0.55, lid=0.5, look=(0.3, 1),
         brow=(-0.005, -8))
    temp(make_dots("dots", []))
    look(cam, (-3.5, -0.9, 1.6), (-3.82, 2.9, 1.62), 36)


def shot_S9():
    """GUS peels the dots off one by one; a pile grows on the floor; PIP slumped on the stool in the foreground."""
    keep = dots_where(lambda d: not (d["region"] in ("side_n", "front", "hood") and (d["p"].x > 0.25 or d["order"] < 0.35)))
    temp(make_dots("dots", keep))
    temp(dot_pile("pile", (1.0, -2.0, 0.0), n=520, radius=0.42, height=0.3, s=1.5))
    pose(GUS, loc=(0.3, -1.55, 0), rz=-60, hips=(8, 0, 0), head=(12, 0, 0), armL=(-78, 0, -15), elbowL=-30,
         armR=(-20, 0, -12), elbowR=-25, mouth=0.6, look=(0.3, 0))
    bpy.context.view_layer.update()
    hp = GUS.hands["L"].matrix_world.translation
    temp(make_dots("peeled", [dict(p=hp + Vector((0.04, -0.1, -0.06)), n=Vector((0.3, -1, 0.2)), s=1.3)]))
    set_vis(STOOL, True)
    STOOL.location = (2.05, -2.6, 0)
    pose(PIP, loc=(2.05, -2.58, 0.61), rz=-25, hips=(22, 0, 0), head=(10, 0, 18), armL=(-40, 0, 14), elbowL=-50,
         armR=(-40, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=0.0, lid=0.55, look=(-1, 0.2),
         brow=(-0.005, -8))
    look(cam, (2.4, -5.9, 1.55), (0.95, -1.25, 0.95), 28)


def shot_S10():
    """Close on PIP, deadpan to camera: 'There's got to be a faster way.'"""
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.15)))
    pose(PIP, loc=(1.2, -2.6, 0), rz=-4, head=(2, 0, 0), armL=(4, 0, 6), armR=(4, 0, -6), mouth=0.55, lid=0.5,
         look=(0, 0), brow=(-0.01, 0))
    pose(GUS, loc=(-0.6, -1.4, 0), rz=30)
    look(cam, (1.25, -4.2, 0.98), (1.2, -2.6, 0.84), 42)


# ----------------------------------------------------------------------------------------------------------------- run
SHOT_FUNCS = {k: globals()[f"shot_{k}"] for k in SHOT_FRAMES}
timings = {}
tpath = os.path.join(OUT, "timings.json")
if os.path.exists(tpath):
    timings = json.load(open(tpath))
for sh in SHOTS:
    reset()
    SHOT_FUNCS[sh]()
    bpy.context.view_layer.update()
    if sh == "S8":   # where the clock lands on screen (for the S4 wall-clock inset in the animatic)
        from bpy_extras.object_utils import world_to_camera_view
        c = CLOCK.matrix_world.translation
        p0 = world_to_camera_view(scn, cam, c)
        p1 = world_to_camera_view(scn, cam, c + Vector((0.6, 0, 0)))
        cx, cy = p0.x * 1080, (1 - p0.y) * 1920
        json.dump(dict(cx=round(cx), cy=round(cy), r=round(abs(p1.x - p0.x) * 1080)), open(os.path.join(OUT, "clock_px.json"), "w"))
    scn.render.filepath = os.path.join(OUT, f"{sh}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t0
    timings[sh] = dict(seconds=round(dt, 1), spp=SPP, scale=SCALE, threads=THREADS)
    print(f"[partA] {sh}: {dt:.1f} s ({SPP} spp, {SCALE:.2f} scale)", flush=True)
    json.dump(timings, open(tpath, "w"), indent=1)
