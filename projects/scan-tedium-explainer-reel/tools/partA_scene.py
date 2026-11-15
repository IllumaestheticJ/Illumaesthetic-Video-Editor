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
ENGINE = arg("--engine", "EEVEE").upper()   # EEVEE = cel-shaded look (owner, stage 3); CYCLES = stage 1-2 look
TOON = ENGINE == "EEVEE"
TOON_T = (float(arg("--t0", "0.33")), float(arg("--t1", "0.77")))   # measured lit range ~0.27 (ambient) .. ~0.82 (facing the sun), --lumdebug   # lit-luminance band edges: shadow|base, base|highlight
OL_BG = 0.45          # background/prop outline scale (characters keep theirs: thicker lines on characters)
ANIMATE = "--animate" in argv   # stage 3: per-frame animation driven by partA_timeline.json (tools/partA_anim.py)
SHOTS = arg("--shots", "S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12").split(",")
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
    # revised ending (owner, 2026-11-14): PIP points at the Illumaesthetic video, the phone hands over to the real footage
    ("PIP", 14.1, 15.3, "Wait. I saw an Illumaesthetic video..."),
    ("PIP", 15.3, 16.6, "...they did a whole car way faster."),
    ("GUS", 16.6, 17.3, "...Show me."),
]
# Storyboard shot grid (reel frames at 30 fps, version A). Cuts get snapped to measured kicks later.
SHOT_FRAMES = {"S1": (0, 57), "S2": (57, 110), "S3": (110, 162), "S4": (162, 200), "S5": (200, 237),
               "S6": (237, 283), "S7": (283, 330), "S8": (330, 375), "S9": (375, 423), "S10": (423, 459),
               "S11": (459, 498), "S12": (498, 519)}   # Part A ends at 17.3 s (frame 519), P2 follows

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
    car="#5d718a", glass="#1b2333", tyre="#1c1d1c", hub="#c3c7c3", trim="#3a3d3a",
    floor="#8e908d", wall="#abadaa", base="#7f817e", door="#c6c8c5", rib="#b0b2af", peg="#a1a3a0", hole="#5e605d",
    wood="#9b8a76", wood_d="#77695b",
    vinyl="#d2d0cf", foot="#4c4d4c", vest="#3c3e3d", capg="#545655", gog="#3d3e3d", string="#f2f3f2",
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


def _hexmul(h, f, mix_white=0.0):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [min(1.0, v * f) * (1 - mix_white) + mix_white for v in c]
    return "#" + "".join(f"{int(round(v * 255)):02x}" for v in c)


def _set_blend(m):
    for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        try:
            setattr(m, attr, val)
            return
        except Exception:
            pass


def toon(key, alpha=1.0, hl=False):
    """Cel shading: lit diffuse -> Shader to RGB -> luminance -> constant ramp (shadow / base / highlight) -> emission."""
    name = f"t_{key}_{alpha:.2f}_{int(hl)}"
    if name in _MATS:
        return _MATS[name]
    base = PAL.get(key, key)
    m, nt, out = _new_mat(name)
    d = nt.nodes.new("ShaderNodeBsdfDiffuse")
    d.inputs["Color"].default_value = (1, 1, 1, 1)
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    nt.links.new(d.outputs[0], s2r.inputs[0])
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    nt.links.new(s2r.outputs["Color"], bw.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "CONSTANT"
    cr.elements[0].position = 0.0
    cr.elements[0].color = hexcol(_hexmul(base, 0.82))   # shadow close to the base value: a thin, light crescent
    cr.elements[1].position = TOON_T[0]
    cr.elements[1].color = hexcol(base)
    if hl:
        e3 = cr.elements.new(TOON_T[1])
        e3.color = hexcol(_hexmul(base, 1.0, 0.35))
    nt.links.new(bw.outputs[0], ramp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission")
    if "--lumdebug" in argv:   # calibration: emit the raw lit luminance / 3 instead of the bands
        dv = nt.nodes.new("ShaderNodeMath")
        dv.operation = "DIVIDE"
        dv.inputs[1].default_value = 3.0
        nt.links.new(bw.outputs[0], dv.inputs[0])
        nt.links.new(dv.outputs[0], em.inputs["Color"])
    else:
        nt.links.new(ramp.outputs[0], em.inputs["Color"])
    sh = em.outputs[0]
    if alpha < 1.0:
        t = nt.nodes.new("ShaderNodeBsdfTransparent")
        mx = nt.nodes.new("ShaderNodeMixShader")
        mx.inputs[0].default_value = alpha
        nt.links.new(t.outputs[0], mx.inputs[1])
        nt.links.new(sh, mx.inputs[2])
        sh = mx.outputs[0]
        _set_blend(m)
    nt.links.new(sh, out.inputs["Surface"])
    m.diffuse_color = hexcol(base)
    _MATS[name] = m
    return m


def mat(key, alpha=1.0, hl=False):
    """Flat diffuse material from the palette (optionally see-through); cel-shaded when TOON."""
    if TOON:
        return toon(key, alpha, hl)
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
        _set_blend(m)
    nt.links.new(sh, out.inputs["Surface"])
    _MATS[name] = m
    return m


def outline_mat_toon():
    """EEVEE inverted hull: black emission with back-face culling (the shell's near side faces away and is culled); the
    shell is transparent to shadow rays so it never shades the object inside it."""
    m, nt, out = _new_mat("outline_toon")
    lp = nt.nodes.new("ShaderNodeLightPath")
    t = nt.nodes.new("ShaderNodeBsdfTransparent")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = hexcol(PAL["black"])
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Shadow Ray"], mx.inputs[0])
    nt.links.new(e.outputs[0], mx.inputs[1])
    nt.links.new(t.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    m.use_backface_culling = True
    for attr, val in (("use_backface_culling_shadow", True), ("use_transparent_shadow", True)):
        try:
            setattr(m, attr, val)
        except Exception:
            pass
    _MATS["outline"] = m
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


OUTLINE = outline_mat_toon() if TOON else outline_mat()


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


def add_mods(ob, bevel=0.0, ol=0.0, seg=3, char=False):
    if bevel:
        b = ob.modifiers.new("bev", "BEVEL")
        b.width = bevel
        b.segments = seg
        b.limit_method = "ANGLE"
    if ol:
        s = ob.modifiers.new("ol", "SOLIDIFY")
        s.thickness = ol if (char or not TOON) else ol * OL_BG
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
DOT_SPACING = 0.07 * math.sqrt(2)   # v5 (owner): half the dot density -> min distance x sqrt(2) (v1-v4: 0.07, typical ~8 cm)


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


def make_dots(name, dots, lit=(), pop=None, parent=None, seg=14, r_in=R_IN):
    """One mesh for many marker dots: black ring disc + white centre (material 2 = lit sage ring)."""
    bm = bmesh.new()
    for i, d in enumerate(dots):
        p, n = Vector(d["p"]), Vector(d["n"]).normalized()
        s = d.get("s", 1.0) * (1.25 if pop == i else 1.0) * (1.3 if i in lit else 1.0)
        t = n.orthogonal().normalized()
        t2 = n.cross(t)
        rot = d.get("spin", 0.0)
        for layer, (r, off, mi) in enumerate(((R_OUT, 0.003, 2 if i in lit else 0), (r_in, 0.0055, 1))):
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


def _smooth(bm):
    for f in bm.faces:
        f.smooth = True


def blob(name, radii, loc, m, parent, taper=0.0, ol=0.0, seg=40, rings=24, half=False):
    """Ellipsoid (egg when taper > 0: narrower toward +z). half=True keeps the upper half (cap dome)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=1.0)
    if half:
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.02], context="VERTS")
    for v in bm.verts:
        k = 1 - taper * v.co.z
        v.co = Vector((v.co.x * radii[0] * k, v.co.y * radii[1] * k, v.co.z * radii[2]))
    _smooth(bm)
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent, loc)
    return add_mods(ob, 0, ol, char=True)


def capsule(name, r, z0, z1, m, parent, ol=0.0):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=24, radius=r)
    L = z1 - z0 - 2 * r
    for v in bm.verts:
        v.co.z += (L / 2 if v.co.z > 0 else -L / 2) + (z0 + z1) / 2
    _smooth(bm)
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent)
    return add_mods(ob, 0, ol, char=True)


def tube(name, r, z0, z1, m, parent, ol=0.0, bevel=0.02, r_top=None):
    """Straight clothing tube (closed, so it reads solid from above): no sleeves, no shoulder bulges."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=48, radius1=r, radius2=r_top or r, depth=z1 - z0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(0, 0, (z0 + z1) / 2))
    _smooth(bm)
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent)
    if bevel:
        b = ob.modifiers.new("bev", "BEVEL")
        b.width = bevel
        b.segments = 4
        b.limit_method = "ANGLE"
        b.harden_normals = False
    return add_mods(ob, 0, ol, char=True)


def torus(name, R, r, loc, m, parent, rot=(0, 0, 0), ol=0.0, scale=(1, 1, 1)):
    bm = bmesh.new()
    segs, rs = 48, 12
    rings = []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        ring = []
        for k in range(rs):
            b = 2 * math.pi * k / rs
            p = Vector(((R + r * math.cos(b)) * math.cos(a), (R + r * math.cos(b)) * math.sin(a), r * math.sin(b)))
            ring.append(bm.verts.new(Vector((p.x * scale[0], p.y * scale[1], p.z * scale[2]))))
        rings.append(ring)
    for i in range(segs):
        for k in range(rs):
            a, b = rings[i], rings[(i + 1) % segs]
            bm.faces.new((a[k], b[k], b[(k + 1) % rs], a[(k + 1) % rs]))
    _smooth(bm)
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent, loc, rot)
    return add_mods(ob, 0, ol, char=True)


def arc_tube(name, R, rt, m, parent, loc, a0=25.0, a1=155.0, n=14, rs=8):
    """Upward arc (^-style closed happy eye): a tube along a circular arc in the XZ plane."""
    bm = bmesh.new()
    rings = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        c = Vector((R * math.cos(a), 0, R * math.sin(a)))
        t = Vector((-math.sin(a), 0, math.cos(a)))
        nrm = c.normalized()
        b2 = Vector((0, 1, 0))
        ring = []
        for k in range(rs):
            q = 2 * math.pi * k / rs
            ring.append(bm.verts.new(c + (nrm * math.cos(q) + b2 * math.sin(q)) * rt))
        rings.append(ring)
    for i in range(n):
        for k in range(rs):
            a_, b_ = rings[i], rings[i + 1]
            bm.faces.new((a_[k], b_[k], b_[(k + 1) % rs], a_[(k + 1) % rs]))
    for ring in (rings[0], rings[-1]):
        bm.faces.new(ring)
    _smooth(bm)
    return new_obj(name, bm, [m], parent, loc)


def set_eyes(ch, fL, fR=None, shape=None, scale=1.0):
    """Dot-eye expression: f 0 round .. 1 shut (flat-topped half dot in between, a short line when shut); shape 'line' / 'arc'
    overrides both eyes; scale pops the dots (curious 1.15, surprised 1.3)."""
    fR = fL if fR is None else fR
    for e, f in zip(ch.eyeset, (fL, fR)):
        for k in ("round", "half", "line", "arc"):
            e[k].hide_render = True
        e["piv"].scale = (scale, scale, scale)
        if shape in ("line", "arc"):
            e[shape].hide_render = False
        elif f < 0.08:
            e["round"].hide_render = False
        elif f > 0.9:
            e["line"].hide_render = False
        else:
            h = e["half"]
            h.hide_render = False
            h.scale = (1, 1, 2 * (1 - f))
            h.location = (0, 0, e["rz"] * (1 - 2 * f))


def set_brows(ch, on=0.0, hL=0.0, hR=None, tL=0.0, tR=None):
    """Brows: on 0 hidden .. 1 full length; h raise (m); t tilt deg, > 0 = inner end down (annoyed), < 0 = inner up (worried)."""
    hR = hL if hR is None else hR
    tR = tL if tR is None else tR
    for b, h, tl in zip(ch.browset, (hL, hR), (tL, tR)):
        b["piv"].hide_render = on < 0.05
        for c in b["piv"].children:
            c.hide_render = on < 0.05
        b["piv"].scale = (max(0.05, on), 1, 1)
        b["piv"].location.z = b["z"] + h
        b["piv"].rotation_euler = (0, math.radians(-b["sx"] * tl), 0)


def head_surface_y(S, x, z):
    """Front surface y of the egg head (local to the head centre) at (x, z)."""
    rx, ry, rz = S["head"][0] / 2, S["head"][1] / 2, S["head"][2] / 2
    k = 1 - S["taper"] * (z / rz)
    q = 1 - (x / (rx * k)) ** 2 - (z / rz) ** 2
    return -ry * k * math.sqrt(max(0.0, q))


def build_char(name, S):
    """Locked 2026-11-14 design (characters/design.md + turnarounds): light-grey egg head on a light-grey pill body, two
    black dot eyes and nothing else on the face, NO arms or shoulders - mitten hands float detached about a hand-width
    from the body - two dark-grey stubby feet, clothes as straight tubes. Rig keeps the old names (arms/elbows/hands are
    invisible pivots that place the floating hands), so the stage-3 animation drives it unchanged."""
    ch = Char()
    ch.S = S
    ol = S["ol"]
    V = mat("vinyl", hl=True)
    ch.root = empty(name)
    ch.hips = empty(f"{name}_hips", ch.root, (0, 0, S["hip_z"]))
    ch.torso = empty(f"{name}_torso", ch.hips)
    ch.legs, ch.arms, ch.elbows, ch.hands = {}, {}, {}, {}
    fr = S["foot"]
    for side, sx in (("L", 1), ("R", -1)):
        lp = empty(f"{name}_leg{side}", ch.hips, (sx * S["foot_x"], 0, 0))
        blob(f"{name}_foot{side}", fr, (0, -fr[1] * 0.25, -S["hip_z"] + fr[2] * 0.75), mat("foot"), lp, ol=ol)
        ch.legs[side] = lp
        sh = empty(f"{name}_arm{side}", ch.hips, (sx * S["hand_x"], 0, S["shoulder_z"]))
        el = empty(f"{name}_elbow{side}", sh, (0, 0, -S["reach"] / 2))
        hd_ = empty(f"{name}_hand{side}", el, (0, 0, -S["reach"] / 2))
        hr = S["hand"]
        blob(f"{name}_mitt{side}", hr, (0, 0, 0), mat("vinyl", hl=True), hd_, ol=ol * 0.8)
        blob(f"{name}_thumb{side}", (hr[0] * 0.42, hr[0] * 0.42, hr[0] * 0.5), (-sx * hr[0] * 0.55, -hr[1] * 0.55, hr[2] * 0.35),
             mat("vinyl", hl=True), hd_, ol=ol * 0.6)
        ch.arms[side], ch.elbows[side], ch.hands[side] = sh, el, hd_
    # pill ends just under the head (the egg is narrow at the bottom): no grey body band can show between collar and head
    capsule(f"{name}_body", S["body_r"], 0.0, min(S["body_h"], S["neck_z"] + 0.03), V, ch.torso, ol=ol)
    S["dress"](name, ch, S)
    ch.neck = empty(f"{name}_head", ch.hips, (0, 0, S["neck_z"]))
    hw, hd, hh = S["head"]
    hz = hh / 2 - S["head_sink"]
    ch.head_c = hz
    blob(f"{name}_headm", (hw / 2, hd / 2, hh / 2), (0, 0, hz), V, ch.neck, taper=S["taper"], ol=ol)
    ch.eyes_g = empty(f"{name}_eyes", ch.neck, (0, 0, hz))
    ch.eyes, ch.eyeset, ch.browset = [], [], []
    er, ex, ez = S["eye_r"], S["eye_x"], S["eye_z"]
    blk = mat("black")
    for sx in (1, -1):
        # v4 expressions: each dot eye has four shapes - round dot, flat-topped half dot (lid level), squeezed line, ^ arc
        y = head_surface_y(S, sx * ex, ez) + er * 0.45
        piv = empty(f"{name}_eyep{sx}", ch.eyes_g, (sx * ex, y, ez))
        rnd = blob(f"{name}_eye{sx}", (er, er * 0.8, er * 1.15), (0, 0, 0), blk, piv)
        half = blob(f"{name}_eyeh{sx}", (er, er * 0.8, er * 1.15), (0, 0, 0), blk, piv, half=True)
        half.rotation_euler = (math.pi, 0, 0)      # lower half: flat top
        line = blob(f"{name}_eyel{sx}", (er * 1.55, er * 0.7, er * 0.45), (0, 0, -er * 0.15), blk, piv)
        arc = arc_tube(f"{name}_eyea{sx}", er * 1.3, er * 0.45, blk, piv, (0, 0, -er * 0.75), a0=15.0, a1=165.0)
        ch.eyes.append(rnd)
        ch.eyeset.append(dict(piv=piv, round=rnd, half=half, line=line, arc=arc, rz=er * 1.15))
        # floating brow: small dark rounded dash above the eye, tilts for emotion, fades out when neutral
        bz = ez + er * 1.15 + S.get("brow_gap", 0.04)
        by = head_surface_y(S, sx * ex, bz) - 0.008
        bp = empty(f"{name}_browp{sx}", ch.neck, (sx * ex, by, hz + bz))
        blob(f"{name}_brow{sx}", (S["brow_len"] / 2, 0.012, S.get("brow_t", 0.012)), (0, 0, 0), mat("#2a2a2a"), bp)
        ch.browset.append(dict(piv=bp, z=hz + bz, sx=sx))
    S["hat"](name, ch, S)
    # compatibility stubs for the old face API
    ch.pupils, ch.lids, ch.brows = [], [], []
    pose(ch)
    return ch


def dress_gus(name, ch, S):
    """Sleeveless charcoal work vest: a straight tube hugging the pill, collar, two snap pockets, zip. No shoulders."""
    r = S["body_r"]
    vm = mat("vest", hl=False)
    # v2 (owner): the vest reaches the neck - straight tube up to just under the head, a thick collar ring meeting the head
    top = S["neck_z"] - 0.06
    tube(f"{name}_vest", r + 0.018, S["body_h"] * 0.38, top, vm, ch.torso, ol=S["ol"], bevel=0.03)
    torus(f"{name}_collar", r * 0.66, 0.06, (0, 0, top + 0.035), vm, ch.torso, ol=S["ol"] * 0.7, scale=(1, 1, 0.95))
    fy = -(r + 0.018)
    for sx in (1, -1):   # shirt-collar flaps
        box(f"{name}_cflap{sx}", (0.1, 0.022, 0.075), (sx * 0.06, -r * 0.72, top + 0.0), vm, ch.torso, 0.012,
            S["ol"] * 0.5, rot=(-35, 0, -sx * 28))
    for sx in (1, -1):
        box(f"{name}_pocket{sx}", (0.12, 0.025, 0.11), (sx * 0.1, fy + 0.002, S["body_h"] * 0.70), vm, ch.torso, 0.012,
            S["ol"] * 0.5)
        box(f"{name}_flap{sx}", (0.13, 0.03, 0.035), (sx * 0.1, fy - 0.004, S["body_h"] * 0.70 + 0.06), vm, ch.torso, 0.01,
            S["ol"] * 0.5)
        blob(f"{name}_snap{sx}", (0.011, 0.008, 0.011), (sx * 0.1, fy - 0.02, S["body_h"] * 0.70 + 0.06), mat("#b9bbb8"), ch.torso)
        box(f"{name}_lpocket{sx}", (0.13, 0.025, 0.1), (sx * 0.11, fy + 0.004, S["body_h"] * 0.48), vm, ch.torso, 0.012,
            S["ol"] * 0.5)
    box(f"{name}_zip", (0.014, 0.012, S["body_h"] * 0.47), (0, fy - 0.004, S["body_h"] * 0.62), mat("#c8cac7"), ch.torso)


def hat_gus(name, ch, S):
    """Welding goggles with sage lenses pushed up on his head: strap round the head, two lens cups on top-front."""
    hz = ch.head_c
    hw, hd, hh = S["head"]
    g = mat("gog")
    torus(f"{name}_strap", hw / 2 * 0.9, 0.022, (0, 0.01, hz + hh * 0.2), g, ch.neck, rot=(-24, 0, 0), ol=S["ol"] * 0.6,
          scale=(1, 0.97, 1.25))
    for sx in (1, -1):
        cup = empty(f"{name}_cupp{sx}", ch.neck, (sx * 0.1, -hd * 0.26, hz + hh * 0.4), (55, 0, -sx * 10))   # lenses face forward-up
        cyl(f"{name}_cup{sx}", 0.078, 0.075, (0, 0, 0), g, cup, seg=32, bevel=0.012, ol=S["ol"] * 0.7)
        cyl(f"{name}_rim{sx}", 0.082, 0.02, (0, 0, 0.038), mat("#6b6d6a"), cup, seg=32, bevel=0.006)
        cyl(f"{name}_lens{sx}", 0.06, 0.012, (0, 0, 0.045), mat("sage", hl=True), cup, seg=32)
    box(f"{name}_bridge", (0.05, 0.03, 0.03), (0, -hd * 0.26, hz + hh * 0.42), g, ch.neck, 0.008)


def dress_pip(name, ch, S):
    """Sleeveless oversized sage hoodie as a straight tube: hood collar ring, white drawstrings, kangaroo pocket."""
    r = S["body_r"]
    sm = mat("sage")
    bh = S["body_h"]
    tube(f"{name}_hoodie", r + 0.02, bh * 0.2, bh * 0.9, sm, ch.torso, ol=S["ol"], bevel=0.035)
    torus(f"{name}_hood", r * 0.8, 0.05, (0, 0.015, bh * 0.9 + 0.01), sm, ch.torso, ol=S["ol"] * 0.8, scale=(1, 1, 0.9))
    fy = -(r + 0.02)
    for sx in (1, -1):
        cyl(f"{name}_string{sx}", 0.008, 0.13, (sx * 0.04, fy - 0.006, bh * 0.84 - 0.065), mat("string"), ch.torso, seg=10)
        blob(f"{name}_tip{sx}", (0.014, 0.014, 0.018), (sx * 0.04, fy - 0.008, bh * 0.84 - 0.135), mat("string"), ch.torso)
    box(f"{name}_pouch", (0.2, 0.022, 0.085), (0, fy + 0.002, bh * 0.36), sm, ch.torso, 0.02, S["ol"] * 0.5)


def hat_pip(name, ch, S):
    """Backwards dark-grey cap: dome over the top of the head, brim to the back, button on top."""
    hz = ch.head_c
    hw, hd, hh = S["head"]
    cm = mat("capg")
    cap = empty(f"{name}_capp", ch.neck, (0, 0.015, hz + hh * 0.22), (8, 0, 0))   # sits high: band above the eyes
    k = 1 - S["taper"] * 0.44                                                       # head width at the cap line (egg)
    blob(f"{name}_cap", (hw / 2 * 1.02 * k, hd / 2 * 1.03 * k, hh * 0.36), (0, 0, 0), cm, cap, half=True, ol=S["ol"])
    brim = empty(f"{name}_brimp", cap, (0, hd / 2 * 0.9, 0.01), (-12, 0, 0))
    cyl(f"{name}_brim", 0.12, 0.018, (0, 0.06, 0), cm, brim, seg=32, ol=S["ol"] * 0.7, rot=(0, 0, 0))
    ch_brim = bpy.data.objects[f"{name}_brim"]
    ch_brim.scale = (1.15, 1.0, 1.0)
    blob(f"{name}_button", (0.018, 0.018, 0.012), (0, 0, hh * 0.42), cm, cap)
    # backwards cap: the adjustment opening faces front, as a plain darker band - no holes or arch (they read as a second
    # pair of eyes above the real ones)
    fy = -hd / 2 * 1.03 * k - 0.004
    box(f"{name}_strapband", (0.15, 0.012, 0.03), (0, fy - 0.002, 0.016), mat("#3f403f"), cap, 0.006, S["ol"] * 0.4)


def pose(ch, loc=None, rz=0.0, hips=(0, 0, 0), head=(0, 0, 0), armL=(0, 0, 4), armR=(0, 0, -4), elbowL=-10, elbowR=-10,
         legL=(0, 0, 0), legR=(0, 0, 0), mouth=0.0, lid=0.0, look=(0, 0), brow=(0, 0)):
    """Angles in degrees. x>0 leans/nods forward; armX<0 swings a (floating) hand forward/up.
    No mouths: `mouth` (0..1 talk energy from the word times) squashes and stretches the body and lifts the hands a little;
    `lid` 0 open..1 shut squashes the dot eyes (blink / squint); `look` shifts the dot eyes; `brow` is ignored."""
    S = ch.S
    if loc is not None:
        ch.root.location = loc
    ch.root.rotation_euler = (0, 0, math.radians(rz))
    R = lambda t: [math.radians(a) for a in t]
    ch.hips.rotation_euler = R(hips)
    ch.neck.rotation_euler = R(head)
    ch.arms["L"].rotation_euler = R(armL)
    ch.arms["R"].rotation_euler = R(armR)
    ch.elbows["L"].rotation_euler = R((elbowL - 75 * mouth, 0, 0))   # v2: hand lifts read in motion
    ch.elbows["R"].rotation_euler = R((elbowR - 45 * mouth, 0, 0))
    ch.neck.rotation_euler = R((head[0] + 7 * mouth, head[1], head[2] + 3 * mouth))   # head bobs with the talk energy
    ch.legs["L"].rotation_euler = R(legL)
    ch.legs["R"].rotation_euler = R(legR)
    talk_squash(ch, mouth)
    f = max(S.get("base_lid", 0.0), lid)
    set_eyes(ch, f, f)
    set_brows(ch, 0.0)
    ch.eyes_g.location = (look[0] * S["eye_look"], 0, ch.head_c + look[1] * S["eye_look"])


def talk_squash(ch, m):
    S = ch.S
    sz = 1 + 0.12 * m      # v2: squash/stretch up to 12 % (owner: 7 % barely read in motion)
    sxy = 1 - 0.06 * m
    ch.torso.scale = (sxy, sxy, sz)
    ch.neck.location.z = S["neck_z"] + S["body_h"] * (sz - 1)


GUS_SPEC = dict(hip_z=0.06, foot=(0.12, 0.16, 0.075), foot_x=0.12, body_r=0.2, body_h=1.2, neck_z=1.13,
                head=(0.62, 0.57, 0.72), taper=-0.13, head_sink=0.0, eye_r=0.024, eye_x=0.085, eye_z=0.05, eye_look=0.03,
                hand=(0.085, 0.075, 0.09), hand_x=0.47, shoulder_z=1.0, reach=0.36, ol=0.024,
                brow_len=0.075, brow_t=0.013, brow_gap=0.045, dress=dress_gus, hat=hat_gus)
PIP_SPEC = dict(hip_z=0.045, foot=(0.085, 0.115, 0.055), foot_x=0.075, body_r=0.15, body_h=0.66, neck_z=0.61,
                head=(0.5, 0.46, 0.55), taper=-0.13, head_sink=0.0, eye_r=0.02, eye_x=0.072, eye_z=0.03, eye_look=0.025,
                hand=(0.06, 0.055, 0.065), hand_x=0.36, shoulder_z=0.55, reach=0.24, ol=0.019,
                brow_len=0.065, brow_t=0.012, brow_gap=0.016, dress=dress_pip, hat=hat_pip)


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
                           ("second", 0.36, 0.012, mat("sage"), -0.076)):
        piv = empty(f"clock_{nm}", g, (0, y, 0))
        box(f"clock_{nm}_m", (w, 0.006, L), (0, 0, L / 2 - 0.04), m, piv, 0.002)
        hands[nm] = piv
    cyl("clock_pin", 0.03, 0.02, (0, -0.082, 0), mat("sage"), g, axis="Y")
    return g, hands


def clock_blur(clock_g, hands, r=0.42):
    """Hands spinning 'like a fan': trailing ghost copies (see-through) + whirr strokes beside the clock."""
    objs = []
    for nm, L, w, key, y, n, step in (("minute", 0.33, 0.028, "black", -0.07, 9, 14), ("second", 0.36, 0.014, "sage", -0.078, 12, 11)):
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


def strip_path(name, pts, width, dots_every=0.14, rng=None):   # v5: half density on the dot roll too
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


def build_screen_ui(ui, door=(0.085, 0.022, 8.0), snapped=False, pin_scale=1.0):
    """Laptop screen: a side-view car assembled from scan pieces with recognisable silhouettes (rear quarter, roof, front
    bumper/fender); the DOOR is being dragged into its slot with three colour-coded pin pairs (no numerals) about to snap."""
    objs = []

    def P(name, pts, col, loc=(0, 0, 0.001), rot=0.0, z=0.0):
        o = poly(name, pts, emit(col, 1.0), ui, loc=loc, rot=(0, 0, rot), z=z)
        objs.append(o)
        return o

    P("ui_bg", [(-0.205, -0.135), (0.205, -0.135), (0.205, 0.135), (-0.205, 0.135)], "#141614", loc=(0, 0, 0))
    P("ui_bar", [(-0.205, 0.118), (0.205, 0.118), (0.205, 0.135), (-0.205, 0.135)], "#2a2d2a", loc=(0, 0, 0.0005))
    for i, c in enumerate(("#8c918c", "sage_l", "white")):
        objs.append(cyl(f"ui_dot{i}", 0.0045, 0.0005, (-0.19 + i * 0.013, 0.1265, 0.001), emit(c, 1.0), ui, seg=12))
    oy = -0.01   # lift the whole car a little on the screen
    sh = lambda pts: [(x, y + oy) for x, y in pts]
    # empty slot where the door goes (dark ghost of the car's side)
    P("ui_ghost", sh([(-0.04, -0.097), (0.105, -0.097), (0.105, 0.05), (-0.04, 0.05)]), "#2e322e", loc=(0, 0, 0.0008))
    P("ui_rear", sh([(-0.182, -0.095), (-0.035, -0.095), (-0.035, 0.047), (-0.078, 0.05), (-0.118, -0.012), (-0.176, -0.024),
                     (-0.188, -0.06)]), "ui_piece2")
    P("ui_roof", sh([(-0.08, 0.046), (0.07, 0.046), (0.062, 0.06), (0.035, 0.07), (-0.042, 0.072), (-0.072, 0.064)]), "ui_piece")
    P("ui_front", sh([(0.10, -0.095), (0.178, -0.095), (0.188, -0.07), (0.186, -0.03), (0.17, -0.02), (0.10, -0.012)]), "ui_piece2")
    P("ui_headl", sh([(0.17, -0.042), (0.185, -0.042), (0.184, -0.03), (0.17, -0.03)]), "white", loc=(0, 0, 0.0015))
    P("ui_lip", sh([(0.10, -0.078), (0.186, -0.078), (0.186, -0.074), (0.10, -0.074)]), "#6b706b", loc=(0, 0, 0.0015))
    P("ui_taill", sh([(-0.186, -0.045), (-0.176, -0.045), (-0.176, -0.033), (-0.184, -0.033)]), "#6b706b", loc=(0, 0, 0.0015))
    for nm, x in (("r", -0.118), ("f", 0.135)):
        objs.append(cyl(f"ui_wheel{nm}", 0.029, 0.0005, (x, -0.095 + oy, 0.002), emit("black", 1.0), ui, seg=32))
        objs.append(cyl(f"ui_hub{nm}", 0.012, 0.0005, (x, -0.095 + oy, 0.0025), emit("#8c918c", 1.0), ui, seg=24))
    # the door (local coords, seated centre would be (0.0325, -0.04)): outline, window, handle; dragged up-right, tilted
    door_c = Vector((0.0325, -0.04 + oy))
    loc = Vector((door[0], door[1] + oy))
    rot = math.radians(door[2])
    outer = [(-0.0675, -0.055), (0.0675, -0.055), (0.0675, 0.025), (0.033, 0.083), (-0.0675, 0.087)]
    win = [(-0.058, 0.03), (0.058, 0.03), (0.031, 0.075), (-0.058, 0.077)]
    handle = [(0.03, 0.004), (0.056, 0.004), (0.056, 0.011), (0.03, 0.011)]
    P("ui_door", outer, "#d4d8d4", loc=(loc.x, loc.y, 0.003), rot=rot)
    P("ui_door_win", win, "#141614", loc=(loc.x, loc.y, 0.0034), rot=rot)
    P("ui_door_handle", handle, "#6b706b", loc=(loc.x, loc.y, 0.0034), rot=rot)
    # pins: where the door meets the rear piece, the front fender and the roof
    tgt = [Vector((-0.03, -0.035 + oy)), Vector((0.098, -0.06 + oy)), Vector((0.005, 0.047 + oy))]
    pin_cols = ["sage_l", "white", "pin_blue"]
    for i, (tg, c) in enumerate(zip(tgt, pin_cols)):
        lp = tg - door_c
        lp = Vector((max(-0.06, min(0.06, lp.x)), min(0.078, lp.y)))
        src = loc + Vector((lp.x * math.cos(rot) - lp.y * math.sin(rot), lp.x * math.sin(rot) + lp.y * math.cos(rot)))
        for nm, pt in ((("t", tg),) if snapped else (("s", src), ("t", tg))):
            ps = pin_scale
            objs.append(cyl(f"pin_{nm}{i}", 0.0065 * ps, 0.0006, (pt.x, pt.y, 0.0045), emit(c, 1.3), ui, axis="Z", seg=16))
            objs.append(cyl(f"pin_{nm}r{i}", 0.0085 * ps, 0.0005, (pt.x, pt.y, 0.004), emit("black", 1.0), ui, axis="Z", seg=16))
        if snapped:
            continue
        d = tg - src
        for k in range(0, 6, 2):
            p0, p1 = src + d * (k / 6), src + d * ((k + 1) / 6)
            nrm = Vector((-d.y, d.x)).normalized() * 0.0012
            P(f"pin_l{i}{k}", [tuple(p0 - nrm), tuple(p1 - nrm), tuple(p1 + nrm), tuple(p0 + nrm)], c, loc=(0, 0, 0.0042))
    cur = [(0, 0), (0, -0.03), (0.008, -0.022), (0.014, -0.034), (0.019, -0.031), (0.013, -0.02), (0.024, -0.02)]
    P("ui_cursor", cur, "white", loc=(loc.x + 0.03, loc.y + 0.02, 0.006))
    P("ui_cursor_o", [(x * 1.25 - 0.002, y * 1.18 + 0.002) for x, y in cur], "black", loc=(loc.x + 0.03, loc.y + 0.02, 0.0055))
    return objs


def build_stool(loc):
    g = empty("STOOL", None, loc)
    cyl("stool_seat", 0.24, 0.06, (0, 0, 0.58), mat("wood"), g, bevel=0.015, ol=0.015)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.4
        box(f"stool_leg{k}", (0.045, 0.045, 0.6), (0.15 * math.cos(a), 0.15 * math.sin(a), 0.28), mat("dark"), g, ol=0.01,
            rot=(math.degrees(-0.14 * math.sin(a)), math.degrees(0.14 * math.cos(a)), 0))
    return g


# ----------------------------------------------------------------------------------------------------------------- phone
PHONE_W, PHONE_H = 0.153, 0.272   # screen 9:16 (cartoon-sized), so vertical footage drops in with no crop change
KEY = "#ff00ff"                   # screen key colour: appears nowhere else in the scene
SCREEN_LOCAL = [(-PHONE_W / 2, -0.0076, PHONE_H / 2), (PHONE_W / 2, -0.0076, PHONE_H / 2),
                (PHONE_W / 2, -0.0076, -PHONE_H / 2), (-PHONE_W / 2, -0.0076, -PHONE_H / 2)]   # tl, tr, br, bl (upright)


def build_phone():
    """Generic phone: rounded near-black slab, no brand, no logo. The screen is a flat emissive key-colour quad that only
    the camera sees (no light spill, no shadow), to be replaced by the real IS350 footage by corner-pin + key."""
    g = empty("PHONE")
    box("phone_body", (PHONE_W + 0.022, 0.014, PHONE_H + 0.042), (0, 0, 0), mat("#202320"), g, bevel=0.012, ol=0.008)
    bm = bmesh.new()
    vs = [bm.verts.new(c) for c in SCREEN_LOCAL]
    bm.faces.new(vs)
    scr = new_obj("phone_screen", bm, [emit(KEY, 1.0)], g)
    for attr in ("visible_diffuse", "visible_glossy", "visible_shadow", "visible_transmission", "visible_volume_scatter"):
        if hasattr(scr, attr):
            setattr(scr, attr, False)
    return g, scr


def orient_phone(phone, centre, n, up=(0, 0, 1)):
    """Place the phone so its screen centre is at `centre`, facing direction n, with the screen's up as close to `up` as possible."""
    n = Vector(n).normalized()
    u = Vector(up) - Vector(up).dot(n) * n
    u.normalize()
    ycol = -n
    xcol = ycol.cross(u)
    M = Matrix(((xcol.x, ycol.x, u.x), (xcol.y, ycol.y, u.y), (xcol.z, ycol.z, u.z)))
    phone.matrix_world = Matrix.Translation(Vector(centre) - n * 0.0076) @ M.to_4x4()
    return n, u, xcol


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
    # peeled markers read as white stickers: thin black ring, big white face; a third lie face-down (plain white backing)
    face_up = [d for k, d in enumerate(dl) if k % 3]
    backs = [d for k, d in enumerate(dl) if not k % 3]
    g = make_dots(name, face_up, r_in=R_OUT * 0.8)
    bm = bmesh.new()
    for d in backs:
        p, n = Vector(d["p"]), Vector(d["n"]).normalized()
        t = n.orthogonal().normalized()
        t2 = n.cross(t)
        vs = [bm.verts.new(p + n * 0.003 + (t * math.cos(2 * math.pi * k / 14) + t2 * math.sin(2 * math.pi * k / 14)) * R_OUT * d["s"] * 1.05)
              for k in range(14)]
        bm.faces.new(vs)
    new_obj(name + "_backs", bm, [mat("white")], g)
    return g


# ----------------------------------------------------------------------------------------------------------------- render setup
def setup_render():
    if TOON:
        return setup_render_eevee()
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


def setup_render_eevee():
    """Cel-shaded look: EEVEE (software GL here: Mesa llvmpipe via EGL, no GPU), toon emission materials, hard sun shadow."""
    scn.render.engine = "BLENDER_EEVEE"
    ee = scn.eevee
    ee.taa_render_samples = SPP
    for attr, val in (("use_shadows", True), ("use_raytracing", False), ("use_gtao", False), ("use_bloom", False),
                      ("shadow_ray_count", 1), ("shadow_step_count", 4)):
        try:
            setattr(ee, attr, val)
        except Exception:
            pass
    scn.render.resolution_x = 1080
    scn.render.resolution_y = 1920
    scn.render.resolution_percentage = int(round(SCALE * 100))
    scn.render.film_transparent = False
    scn.render.use_motion_blur = False
    scn.view_settings.view_transform = "Standard"
    scn.view_settings.look = "None"
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
    bg.inputs["Color"].default_value = hexcol("#c9cbc8")
    bg.inputs["Strength"].default_value = 0.45
    out = [n for n in w.node_tree.nodes if n.type == "OUTPUT_WORLD"]
    out = out[0] if out else w.node_tree.nodes.new("ShaderNodeOutputWorld")
    w.node_tree.links.new(bg.outputs[0], out.inputs["Surface"])
    sun_d = bpy.data.lights.new("sun", "SUN")
    sun_d.energy = 2.2
    sun_d.angle = math.radians(1.5)
    sun = bpy.data.objects.new("sun", sun_d)
    COLL.objects.link(sun)
    # key light from front-left-above (camera side, like the cel reference): faces read mostly lit with a narrow shadow side
    d_from = Vector((-0.55, -1.0, 1.1)).normalized()
    sun.rotation_euler = (-d_from).to_track_quat("-Z", "Y").to_euler()
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
PHONE, SCREEN = build_phone()
# Pip's own small handheld 3D scanner (character design): dark-grey head with three green lights on a sage grip, in his free hand
PIPSCAN = empty("PIPSCAN", PIP.hands["R"], (0, -0.01, 0.02))


def pip_scanner(where):
    """Pip's scanner: in his right hand ('hand') only while he scans or gestures about scanning, else clipped in the hoodie
    pouch ('pouch'); never in the phone shots."""
    if where == "hand":
        PIPSCAN.parent = PIP.hands["R"]
        PIPSCAN.location, PIPSCAN.rotation_euler = (0, -0.01, 0.02), (0, 0, 0)
    else:
        PIPSCAN.parent = PIP.torso
        r, bh = PIP_SPEC["body_r"], PIP_SPEC["body_h"]
        PIPSCAN.location, PIPSCAN.rotation_euler = (0.045, -(r + 0.035), bh * 0.36 + 0.02), (math.radians(-8), 0, math.radians(8))
box("ps_grip", (0.04, 0.045, 0.1), (0, 0.0, 0.0), mat("sage"), PIPSCAN, 0.012, 0.006)
box("ps_head", (0.075, 0.06, 0.05), (0, -0.01, 0.07), mat("gog"), PIPSCAN, 0.014, 0.006)
for _k in (-1, 0, 1):
    cyl(f"ps_led{_k}", 0.008, 0.004, (_k * 0.021, -0.041, 0.07), emit("sage_l", 1.8), PIPSCAN, axis="Y", seg=12)
ALL_DOTS = gen_car_dots()
print(f"[partA] {len(ALL_DOTS)} marker dots on the car", flush=True)
if "--dotstat" in argv:
    exec(open(arg("--dotstat", "")).read())

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
    for ob in (SCANNER, ROLL, STOOL, PHONE):
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
    """See-through 'scan data' grey, front faces only (back faces fully transparent so the colour doesn't stack).
    Cel look: flat colour (emission) with blended transparency (EEVEE's default dithered alpha speckles at low samples)."""
    name = f"scanpatch_{key}_{alpha:.2f}"
    if name in _MATS:
        return _MATS[name]
    m, nt, out = _new_mat(name)
    if TOON:
        d = nt.nodes.new("ShaderNodeEmission")
        _set_blend(m)
    else:
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
    pose(PIP, loc=(-3.7, 2.68, 0.565), rz=-6, hips=(24, 0, 0), head=(10, 0, -8), armL=(-38, 0, 14), elbowL=-50,
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
    pose(PIP, loc=(2.05, -2.58, 0.565), rz=-25, hips=(22, 0, 0), head=(10, 0, 18), armL=(-40, 0, 14), elbowL=-50,
         armR=(-40, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=0.0, lid=0.55, look=(-1, 0.2),
         brow=(-0.005, -8))
    look(cam, (2.4, -5.9, 1.55), (0.95, -1.25, 0.95), 28)


def shot_S10():
    """Close on PIP: 'Wait. I saw an Illumaesthetic video...' - he perks up and pulls out a phone (back to camera)."""
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.15)))
    pose(PIP, loc=(1.2, -2.6, 0), rz=-4, hips=(-4, 0, 0), head=(-6, 0, 6), armL=(-62, 0, -8), elbowL=-80, armR=(4, 0, -6),
         mouth=0.8, lid=0.0, look=(0.5, 0.7), brow=(0.045, -14))
    pose(GUS, loc=(-0.6, -1.4, 0), rz=30)
    bpy.context.view_layer.update()
    hp = PIP.hands["L"].matrix_world.translation
    set_vis(PHONE, True)
    orient_phone(PHONE, hp + Vector((0.0, -0.03, 0.13)), (0.15, 0.8, 0.55))   # screen toward PIP's face, back to camera
    look(cam, (1.25, -4.2, 0.98), (1.2, -2.6, 0.86), 42)


# S11 and S12 share the phone pose: PIP holds it up to GUS, screen facing GUS and the camera along PHONE_N.
PHONE_N = (0.28, -1.0, 0.12)
S12_LENS, S12_D0 = 35.0, 1.6
S12_DEND = (PHONE_H / 2) * S12_LENS / 18.0   # sensor 36 mm vertical: screen height == frame height at the last frame


def aim_arm(ch, side, target):
    """Point an arm (elbow straight) from its shoulder toward a world target; returns the hand's world position."""
    sh = ch.arms[side]
    ch.elbows[side].rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    tl = sh.parent.matrix_world.inverted() @ Vector(target)
    d = tl - sh.location
    sh.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    return ch.hands[side].matrix_world.translation.copy()


def place_head_xy(ch, want):
    """Shift a character on the floor so its head pivot lands over `want` (x, y)."""
    bpy.context.view_layer.update()
    h = ch.neck.matrix_world.translation
    ch.root.location.x += want[0] - h.x
    ch.root.location.y += want[1] - h.y
    bpy.context.view_layer.update()


def phone_pose_s11():
    """PIP holds the phone out in front of his face, off to GUS's side, screen along PHONE_N; the hand stays behind the
    phone plane so nothing ever crosses the screen."""
    pose(PIP, loc=(1.2, -2.6, 0), rz=14, hips=(-6, 0, 0), head=(-12, 0, -16), armR=(-10, 0, -10), mouth=0.75, lid=0.0,
         look=(0.6, 0.6), brow=(0.04, -12))
    bpy.context.view_layer.update()
    n = Vector(PHONE_N).normalized()
    u = Vector((0, 0, 1)) - n.z * n
    u.normalize()
    r = (-n).cross(u)
    head = PIP.neck.matrix_world @ Vector((0, 0, PIP.S["head"][2] / 2))
    hand = aim_arm(PIP, "L", head + r * 0.24 + n * 0.4 - u * 0.14)
    set_vis(PHONE, True)
    c = hand + u * (PHONE_H / 2 + 0.06) + n * 0.14
    n, u, r = orient_phone(PHONE, c, n)
    bpy.context.view_layer.update()
    c = SCREEN.matrix_world @ Vector((0, -0.0076, 0))
    return c, n, u, r


def screen_corners_px():
    from bpy_extras.object_utils import world_to_camera_view
    bpy.context.view_layer.update()
    out = []
    for lc in SCREEN_LOCAL:
        v = world_to_camera_view(scn, cam, SCREEN.matrix_world @ Vector(lc))
        out.append([round(v.x * 1080, 2), round((1 - v.y) * 1920, 2)])
    return out


def s12_cam(c, n, u, k):
    """Push along the screen normal; k = 0..1 over S12. Distance is eased exponentially (constant zoom rate, accelerating
    slightly into the cut) and lands exactly on S12_DEND at the last frame."""
    ke = k ** 1.4
    d = S12_D0 * (S12_DEND / S12_D0) ** ke
    look(cam, c + n * d, c, S12_LENS, up=u)


def shot_S11():
    """PIP holds the phone up to GUS, screen to camera: '...they did a whole car way faster.' GUS's shoulder in the foreground."""
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.15)))
    c, n, u, r = phone_pose_s11()
    f = -Vector((n.x, n.y, 0)).normalized()
    pose(GUS, loc=(0, 0, 0), rz=math.degrees(math.atan2(f.x, -f.y)) + 25, hips=(6, 0, 0), head=(14, 0, 0), look=(0, -0.6))
    place_head_xy(GUS, c + n * 0.75 + r * 0.62)   # shoulder in the right edge of frame, clear of the screen
    # camera parallel to the screen normal, shifted so PIP's face sits below-left of the phone: screen stays a true rectangle
    look(cam, c + n * 1.2 - r * 0.16 - u * 0.2, c - r * 0.16 - u * 0.2, 38, up=u)


def shot_S12():
    """GUS leans in ('...Show me.'); the camera pushes along the screen normal until the screen fills the frame (start frame)."""
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.15)))
    c, n, u, r = phone_pose_s11()
    # GUS peeks in from the right in profile: faces the phone sideways (-r), head beside the screen just in front of its
    # plane, body behind it - nothing of his can enter the cone between camera and screen during the push
    f = -Vector((r.x, r.y, 0)).normalized()
    pose(GUS, loc=(0, 0, 0), rz=math.degrees(math.atan2(f.x, -f.y)), hips=(42, 0, 0), head=(-8, 0, 0),
         armL=(42, 0, 8), armR=(42, 0, -8), elbowL=-10, elbowR=-10, look=(0, 0), mouth=0.5, brow=(0.02, 0))
    place_head_xy(GUS, c + n * 0.1 + r * 0.33)
    s12_cam(c, n, u, 0.0)
    return c, n, u


def shot_S12end():
    """Check render: the last frame of the S12 push must be all screen (key colour edge to edge)."""
    c, n, u = shot_S12()
    s12_cam(c, n, u, 1.0)


# ----------------------------------------------------------------------------------------------------------------- run
SHOT_FUNCS = {k: globals()[f"shot_{k}"] for k in list(SHOT_FRAMES) + ["S12end"]}
CORNERS_PATH = os.path.join(OUT, "screen_corners.json")
corners = json.load(open(CORNERS_PATH)) if os.path.exists(CORNERS_PATH) else dict(
    doc="Phone-screen corners for compositing the real IS350 footage (corner-pin). Pixels in the 1080x1920 frame, origin at the "
        "top-left corner of the image, x right, y down, floats. Corner order tl, tr, br, bl = the footage's own upright corners. "
        "Frames are reel frames at 30 fps (Part A version A, revised ending). The screen renders as flat key colour; use the key "
        "as the matte where a hand or head overlaps it.",
    width=1080, height=1920, fps=30, screen_aspect="9:16", key_colour=KEY, corner_order=["tl", "tr", "br", "bl"], shots={})
timings = {}
tpath = os.path.join(OUT, "timings.json")
if os.path.exists(tpath):
    timings = json.load(open(tpath))
for sh in ([] if ANIMATE else SHOTS):
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
    if sh == "S11":
        a0, b0 = SHOT_FRAMES["S11"]
        corners["shots"]["S11"] = dict(frames=[a0, b0], static=True, corners=screen_corners_px())
    if sh == "S12":
        a0, b0 = SHOT_FRAMES["S12"]
        c, n, u, r = phone_pose_s11()
        per = {}
        for f in range(a0, b0):
            s12_cam(c, n, u, (f - a0) / (b0 - 1 - a0))
            per[str(f)] = screen_corners_px()
        corners["shots"]["S12"] = dict(frames=[a0, b0], static=False, per_frame=per,
                                       note=f"push along the screen normal, lens {S12_LENS} mm, {S12_D0} m -> {S12_DEND:.4f} m; "
                                            f"last frame {b0 - 1} = full frame")
        s12_cam(c, n, u, 0.0)
    if sh in ("S11", "S12"):
        json.dump(corners, open(CORNERS_PATH, "w"), indent=1)
    scn.render.filepath = os.path.join(OUT, f"{sh}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t0
    timings[sh] = dict(seconds=round(dt, 1), spp=SPP, scale=SCALE, threads=THREADS)
    print(f"[partA] {sh}: {dt:.1f} s ({SPP} spp, {SCALE:.2f} scale)", flush=True)
    json.dump(timings, open(tpath, "w"), indent=1)

if ANIMATE:
    _here = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1])) if "-P" in sys.argv else os.getcwd()
    _anim = os.path.join(_here, "partA_anim.py")
    exec(compile(open(_anim).read(), _anim, "exec"), globals())
