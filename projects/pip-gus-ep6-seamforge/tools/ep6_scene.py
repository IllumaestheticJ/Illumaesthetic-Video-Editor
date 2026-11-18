"""Pip & Gus Ep 6 "What does SeamForged do?" - cartoon part (Blender 5.3, EEVEE cel look, series rig).

Reuses the series library from the pilot (projects/scan-tedium-explainer-reel/tools/partA_scene.py up to its "build all"
block: palette, toon materials + outlines, shop, Pip/Gus rig with the option-3 proportions and nametags, clock, laptop,
phone, stool, EEVEE setup) and the pilot's talk/blink/expression machinery (partA_anim.py up to its shots). Props and
layout follow Ep 7 (tools/ep7_scene.py on claude/pip-gus-ep6-printer-size): unbranded printer, side table, bumper skins.
Everything episode-specific lives here: the bumper hanging off the small printer, the hand-numbering, the row of build
plates, Gus's phone hand-off, 7 shots.

  blender -b --factory-startup -P ep6_scene.py -- --out FRAMES --timeline ../ep6_timeline.json --tagdir TEX
          [--shots S1,S2] [--scale 1] [--spp 8] [--every N] [--frames a,b] [--stills]

Screens: the laptop screen (S1, S2) and the phone screen (S7) render as flat key colour #ff00ff seen by camera rays only;
their corners go to FRAMES/screen_corners.json for corner-pinning the real footage (slicer clip on the laptop, the
SeamForged capture on the phone). Rules kept: no text, numerals or brands in 3D ("numbers" are sage marker scribbles),
Pip & Gus locked design, no arms.
"""
import sys, os, json, math, random, time

PILOT = "/home/user/Illumaesthetic-Video-Editor/projects/scan-tedium-explainer-reel/tools"
_src = open(os.path.join(PILOT, "partA_scene.py")).read()
_cut = _src.index("# ----------------------------------------------------------------------------------------------------------------- build all")
exec(compile(_src[:_cut], os.path.join(PILOT, "partA_scene.py"), "exec"), globals())

SHOTS = arg("--shots", "S1,S2,S3,S4,S5,S6,S7").split(",")
STILLS = "--stills" in argv

# ----------------------------------------------------------------------------------------------------------------- build
cam, sun = setup_render()
SHOP = build_shop()
for _ob in list(SHOP.children):      # no car in this episode
    if _ob.name.startswith("bay"):
        bpy.data.objects.remove(_ob, do_unlink=True)
for _ob in list(SHOP.children):
    if _ob.name.startswith(("bench", "toolbox")):
        _ob.location.x += 0.4
CLOCK, HANDS = build_clock(SHOP, loc=(-2.25, 3.48, 2.55), r=0.32)
PIP = build_char("PIP", PIP_SPEC)
GUS = build_char("GUS", GUS_SPEC)
PHONE, SCREEN = build_phone()
STOOL = build_stool((-0.6, 0.0, 0))


def build_printer(name, w, d, h, loc, nozzle=0.006):
    """Small enclosed desktop FDM printer, no brand (Ep 7's design): dark frame, sage lid band, black bed, white head,
    see-through door, white spool. Origin = base centre, front faces -y."""
    s = h / 1.95
    g = empty(name, None, loc)
    t = 0.05 * max(s, 0.35)
    fr = mat("dark")
    box(f"{name}_plinth", (w, d, 0.12 * h), (0, 0, 0.06 * h), fr, g, 0.01 * s + 0.004, 0.012)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"{name}_post{sx}{sy}", (t, t, h), (sx * (w - t) / 2, sy * (d - t) / 2, h / 2), fr, g, 0.004, 0.01)
    bed_z = 0.36 * h
    bed = box(f"{name}_bed", (w * 0.78, d * 0.78, 0.035 * s + 0.01), (0, 0, bed_z), mat("#1c1d1c"), g, 0.004, 0.01)
    box(f"{name}_bedrim", (w * 0.8, d * 0.8, 0.012 * s + 0.004), (0, 0, bed_z - 0.02 * s - 0.004), mat("sage_l"), g, 0.002)
    hs = 0.16 * s + 0.05
    head = empty(f"{name}_head", g, (0, -t * 0.9, 0.8 * h))
    box(f"{name}_hbody", (hs, hs * 0.75, hs * 1.1), (0, -hs * 0.3, -hs * 0.2), mat("white"), head, hs * 0.12, 0.012)
    box(f"{name}_hstripe", (hs * 1.01, hs * 0.76, hs * 0.16), (0, -hs * 0.3, hs * 0.12), mat("sage"), head, hs * 0.05)
    for sx in (-1, 1):
        box(f"{name}_side{sx}", (0.012, d, h * 0.9), (sx * w / 2, 0, h * 0.55), mat("#3a3d3a"), g, 0.004, 0.01)
    box(f"{name}_back", (w, 0.012, h * 0.9), (0, d / 2, h * 0.55), mat("#3a3d3a"), g, 0.004, 0.01)
    box(f"{name}_lid", (w + 0.01, d + 0.01, 0.03), (0, 0, h + 0.012), mat("sage"), g, 0.008, 0.012)
    box(f"{name}_door", (w * 0.96, 0.006, h * 0.62), (0, -d / 2 - 0.004, h * 0.6), mat("#cfe3d6", 0.28), g, 0.004)
    box(f"{name}_handle", (0.012, 0.02, h * 0.22), (w * 0.4, -d / 2 - 0.016, h * 0.6), mat("white"), g, 0.004, 0.006)
    sp = empty(f"{name}_spoolp", g, (-(w / 2) - 0.11 * s - 0.03, 0.1 * d, 0.62 * h))
    cyl(f"{name}_spool", 0.18 * s + 0.05, 0.1 * s + 0.03, (0, 0, 0), mat("white"), sp, axis="X", seg=32, bevel=0.01, ol=0.01)
    cyl(f"{name}_spoolhub", 0.07 * s + 0.02, 0.1 * s + 0.035, (0, 0, 0), mat("sage"), sp, axis="X", seg=24)
    return dict(g=g, w=w, d=d, h=h, s=s, bed=bed, bed_z=bed_z, head=head, top=bed_z + 0.02 * s + 0.01)


# back table: the small printer and the laptop (Ep 7's side table)
TABLE = empty("TABLE", None, (0.9, 3.0, 0))
box("tbl_top", (1.9, 0.62, 0.06), (0, 0, 0.82), mat("wood"), TABLE, 0.012, 0.018)
for _sx in (-1, 1):
    for _sy in (-1, 1):
        box(f"tbl_leg{_sx}{_sy}", (0.06, 0.06, 0.8), (_sx * 0.89, _sy * 0.26, 0.4), mat("dark"), TABLE, 0.004, 0.01)
box("tbl_shelf", (1.8, 0.55, 0.035), (0, 0, 0.22), mat("wood_d"), TABLE, 0.004, 0.012)
TABLE_Z = 0.85
SMALL = build_printer("SMALL", 0.44, 0.44, 0.5, (0.35, 3.0, TABLE_Z))
LAPTOP, UI = build_laptop(None, loc=(1.3, 2.9, TABLE_Z), rz=-8)
LAP_W, LAP_H = 0.42, 0.27
LAP_LOCAL = [(-LAP_W / 2, LAP_H / 2, 0.0012), (LAP_W / 2, LAP_H / 2, 0.0012), (LAP_W / 2, -LAP_H / 2, 0.0012),
             (-LAP_W / 2, -LAP_H / 2, 0.0012)]    # tl, tr, br, bl (upright on the lid)
_bm = bmesh.new()
_bm.faces.new([_bm.verts.new(c) for c in LAP_LOCAL])
LAP_SCREEN = new_obj("lap_key", _bm, [emit(KEY, 1.0)], UI)
for _attr in ("visible_diffuse", "visible_glossy", "visible_shadow", "visible_transmission", "visible_volume_scatter"):
    if hasattr(LAP_SCREEN, _attr):
        setattr(LAP_SCREEN, _attr, False)

# front work table: where the cut pieces get numbered and laid on the plates; a long row of build plates runs off to the right
WT = empty("WTABLE", None, (0.9, 0.9, 0))
WT_LEN = 4.6
box("wt_top", (WT_LEN, 0.7, 0.06), (0, 0, 0.78), mat("wood"), WT, 0.012, 0.018)
for _sx in (-1, 1):
    for _sy in (-1, 1):
        box(f"wt_leg{_sx}{_sy}", (0.06, 0.06, 0.76), (_sx * (WT_LEN / 2 - 0.05), _sy * 0.3, 0.38), mat("dark"), WT, 0.004, 0.01)
WT_Z = 0.81
PLATE_S = 0.34
PLATES = []
for _i in range(10):
    _x = -1.6 + _i * 0.42
    _p = empty(f"plate{_i}", WT, (_x, -0.15, WT_Z - 0.002))
    box(f"plate{_i}_b", (PLATE_S, PLATE_S, 0.014), (0, 0, 0.007), mat("#1c1d1c"), _p, 0.003, 0.008)
    box(f"plate{_i}_r", (PLATE_S + 0.016, PLATE_S + 0.016, 0.008), (0, 0, 0.003), mat("sage_l"), _p, 0.002)
    PLATES.append(_p)

# failed-print shelf (running gag): wall shelf with spaghetti lumps
box("fshelf", (0.7, 0.22, 0.035), (-3.0, 3.45, 1.55), mat("wood"), SHOP, 0.006, 0.012)
for _k, (_x, _c) in enumerate(((-3.22, "white"), (-3.0, "sage_l"), (-2.78, "#dfe2df"))):
    _rng = random.Random(_k + 3)
    for _j in range(9):
        torus(f"spag{_k}_{_j}", 0.04 + 0.02 * _rng.random(), 0.006, (_x + _rng.uniform(-0.05, 0.05), 3.43 + _rng.uniform(-0.04, 0.04),
              1.6 + _rng.uniform(0, 0.08)), mat(_c), SHOP, rot=(_rng.uniform(0, 180), _rng.uniform(0, 180), 0))


def arc_piece(name, R, th, hgt, a0, a1, m, parent, loc=(0, 0, 0), rot=(0, 0, 0), n=10):
    """A slice of a bumper skin (Ep 7): annular sector of outer radius R, thickness th, height hgt, angles a0..a1 (deg,
    0 = toward -y), rounded lower lip. Origin at the arc centre."""
    bm = bmesh.new()
    ring = []
    steps = max(2, int(n * (a1 - a0) / 100) + 2)
    prof = [(R, 0.0), (R + 0.02, hgt * 0.15), (R, hgt * 0.75), (R - th * 0.4, hgt), (R - th, hgt), (R - th, 0.0)]
    for i in range(steps):
        a = math.radians(a0 + (a1 - a0) * i / (steps - 1))
        ring.append([bm.verts.new((r * math.sin(a), -r * math.cos(a), z)) for r, z in prof])
    for i in range(steps - 1):
        for j in range(len(prof)):
            bm.faces.new((ring[i][j], ring[i + 1][j], ring[i + 1][(j + 1) % len(prof)], ring[i][(j + 1) % len(prof)]))
    bm.faces.new(list(reversed(ring[0])))
    bm.faces.new(ring[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = new_obj(name, bm, [m, OUTLINE], parent, loc, rot)
    return add_mods(ob, 0.0, 0.008)


bpy.context.view_layer.update()     # matrix_world of the props is used below and in the shots

# ----------------------------------------------------------------------------------------------------------------- helpers
_temp = []


def temp(ob):
    _temp.append(ob)
    return ob


def whole_bumper(name, loc, R=0.5, rz=0.0, scale=1.0):
    """The finished bumper design in one piece (white skin), open side to the back."""
    g = temp(empty(name, None, loc, (0, 0, rz)))
    g.scale = (scale,) * 3
    arc_piece(f"{name}_s", R, 0.05, 0.26, -58, 58, mat("white"), g)
    return g


def piece(name, loc, rot=(0, 0, 0), k=1.0, mark=0.0, parent=None, col=None):
    """One cut bumper piece (a short curved slab) lying flat; mark 0..1 = sage marker scribble drawn on it (a squiggle,
    never a numeral)."""
    g = temp(empty(name, parent, loc, rot)) if parent is None else empty(name, parent, loc, rot)
    g.scale = (max(k, 0.01),) * 3
    arc_piece(f"{name}_s", 0.42, 0.035, 0.12, -11, 11, mat(col or "white"), g, loc=(0, 0.06, 0.42), rot=(90, 0, 0))
    if mark > 0.01:   # squiggle: three short strokes in a zig-zag, drawn left to right
        n = max(1, int(round(3 * cl(mark))))
        for j in range(n):
            a = math.radians(-30 if j % 2 == 0 else 30)
            box(f"{name}_m{j}", (0.035, 0.008, 0.004), (-0.03 + j * 0.03, -0.03, 0.04), emit("sage", 1.2), g, rot=(0, 0, math.degrees(a)))
    return g


def marker(name, loc, rot=(0, 0, 0)):
    g = temp(empty(name, None, loc, rot))
    cyl(f"{name}_b", 0.014, 0.12, (0, 0, 0), mat("white"), g, seg=14, ol=0.005)
    cyl(f"{name}_c", 0.015, 0.035, (0, 0, 0.07), mat("sage"), g, seg=14, ol=0.005)
    cyl(f"{name}_t", 0.006, 0.02, (0, 0, -0.068), mat("dark"), g, seg=10, r2=0.003)
    return g


def aim_arm(ch, side, target):
    sh = ch.arms[side]
    ch.elbows[side].rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    tl = sh.parent.matrix_world.inverted() @ Vector(target)
    d = tl - sh.location
    sh.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    return ch.hands[side].matrix_world.translation.copy()


def clock_spin(u, rate=1.0):
    am = 60 + 360 * rate * (1.2 * u + 2.0 * u * u)
    HANDS["minute"].rotation_euler = (0, math.radians(am), 0)
    HANDS["second"].rotation_euler = (0, math.radians(200 + 360 * rate * (5 * u + 8 * u * u)), 0)
    HANDS["hour"].rotation_euler = (0, math.radians(300 + (am - 60) / 12), 0)


def reset():
    for ob in _temp:
        stack = [ob]
        while stack:
            o = stack.pop()
            try:
                stack.extend(o.children)
                bpy.data.objects.remove(o, do_unlink=True)
            except ReferenceError:
                pass
    _temp.clear()
    set_vis(PHONE, False)
    set_vis(STOOL, True)
    SMALL["head"].location.x = 0
    set_vis(PIP.root, True)
    set_vis(GUS.root, True)
    pose(PIP, loc=(30, 30, 0))
    pose(GUS, loc=(31, 30, 0))
    HANDS["hour"].rotation_euler = (0, math.radians(300), 0)
    HANDS["minute"].rotation_euler = (0, math.radians(60), 0)
    HANDS["second"].rotation_euler = (0, math.radians(200), 0)


# ----------------------------------------------------------------------------------------------------------------- animation lib
_asrc = open(os.path.join(PILOT, "partA_anim.py")).read()
_acut = _asrc.index("# ----------------------------------------------------------------------------------------------------------------- shots")
exec(compile(_asrc[:_acut], os.path.join(PILOT, "partA_anim.py"), "exec"), globals())


def expr_state(ch, t):
    """Ep 6 expressions (eye shapes only). Pip: worried 'bigger than the printer', impatient 'done yet?' and 'better way',
    excited 'Show me!'. Gus: flat and only slightly weary while explaining, eyes down on his work for '...No.', a little
    proud half-lid on '...We made one.'"""
    nm = "GUS" if ch is GUS else "PIP"
    st = dict(fL=0.0, fR=0.0, shape=None, scale=1.0, on=0.0, hL=0.0, hR=0.0, tL=0.0, tR=0.0, roll=None)

    def blend(name, k):
        if k <= 0:
            return
        tgt = dict(zip(("fL", "fR", "shape", "scale", "on", "hL", "hR", "tL", "tR"), STATES[name]))
        for key in ("fL", "fR", "scale", "on", "hL", "hR", "tL", "tR"):
            st[key] = lerp(st[key], tgt[key], k)
        if tgt["shape"] and k > 0.5:
            st["shape"] = tgt["shape"]

    if nm == "GUS":
        for L in TL["lines"]:
            if L["speaker"] == "GUS":
                k = win(t, L["t0"] - 0.15, L["t1"], 0.2, 0.4)
                st["fL"] = st["fR"] = max(st["fL"], 0.2 * k)
                st["on"] = max(st["on"], 0.65 * k)
                st["tL"] = st["tR"] = max(st["tL"], 10 * k)
        for n in (3, 4):
            L = L_(n)
            if L:
                blend("weary", 0.55 * win(t, L["t0"], L["t1"], 0.15, 0.3))
        L = L_(6)
        if L:
            blend("weary", 0.8 * win(t, L["t0"] - 0.2, L["t1"] + 0.4, 0.1, 0.3))
        L = L_(8)
        if L:
            k = win(t, L["t0"] - 0.1, L["t1"] + 0.6, 0.1, 0.3)
            st["fL"] = st["fR"] = lerp(st["fL"], 0.45, k)
            st["tL"] = st["tR"] = lerp(st["tL"], -2, k)
    else:
        L = L_(1)
        if L:
            blend("curious", win(t, L["t0"] - 0.1, L["words"][1]["t1"], 0.08, 0.2))
            k = win(t, L["words"][2]["t0"], L["t1"] + 0.4, 0.15, 0.3)
            st["fL"] = st["fR"] = lerp(st["fL"], 0.35, k)          # worried half-moon, inner corners up
            st["tL"] = st["tR"] = lerp(st["tL"], -18, k)
        L = L_(5)
        if L:
            k = win(t, L["t0"], L["t1"] + 0.4, 0.05, 0.3)
            blend("impatient", k)
        L = L_(7)
        if L:
            blend("impatient", win(t, L["t0"] - 0.1, L["t1"] + 0.3, 0.08, 0.3))
        L = L_(9)
        if L:
            blend("excited", win(t, L["t0"] - 0.05, L["t1"] + 1.0, 0.05, 0.2))
    return st


def prog(fr, sh):
    f0, f1 = SF[sh]
    return (fr - f0) / max(1, f1 - 1 - f0)


def pop_at(t, ta, dur=0.18):
    if t < ta:
        return 0.0
    return min(1.15, eback((t - ta) / dur, 2.0)) if t - ta < dur * 1.5 else 1.0


def wt(n, i):
    return LN[n]["words"][i]["t0"]


def wt1(n, i):
    return LN[n]["words"][i]["t1"]


# ----------------------------------------------------------------------------------------------------------------- layout
GUS_LAP = Vector((1.85, 2.42, 0.0))      # Gus at the laptop (back table), right of it, turned toward the screen
PIP_LAP = Vector((-0.05, 2.35, 0.0))      # Pip in front-left of the small printer (portrait frame: stacked in depth)
GUS_BEHIND = 0.55                        # Gus stands this far behind the front table centre line, facing the camera (-y)
PILE_X = -2.0                           # unnumbered pile at the left end of the front table (table-local x)
PLATE_PERIOD = 0.75                      # seconds per piece placed (S4/S5 loop)


def placed_count(t, t_start):
    return max(0, int((t - t_start) / PLATE_PERIOD))


def fill_plates(n_done, t, t_start, gus):
    """Pieces already on plates (two per plate); Gus stands at the current plate with a small stack of numbered pieces at
    his left and carries the next one over. Returns (hand target or None, Gus x)."""
    for i in range(min(n_done, 2 * len(PLATES))):
        p = PLATES[i // 2]
        sx = -0.07 if i % 2 == 0 else 0.07
        piece(f"onp{i}", (0, 0, 0), (0, 0, 15 + 25 * (i % 3)), mark=1.0, parent=temp(empty(f"onpp{i}", p, (sx, 0.0, 0.016))))
    i = min(n_done, 2 * len(PLATES) - 1)
    cur = PLATES[i // 2].matrix_world.translation
    stack = cur + Vector((-0.3, -0.12, 0.0))
    for j in range(4):
        piece(f"stk{j}", tuple(stack + Vector((0, 0, 0.022 + 0.026 * j))), (0, 0, 8 * j), mark=1.0, col="white" if j % 2 else "#dfe2df")
    u = ((t - t_start) / PLATE_PERIOD) % 1.0
    tgt = cur + Vector((-0.07 if i % 2 == 0 else 0.07, 0.0, 0.03))
    src = stack + Vector((0, 0, 0.13))
    if u < 0.45:
        k = ease(u / 0.45)
        pos = src.lerp(tgt, k) + Vector((0, 0, 0.12 * math.sin(math.pi * k)))
        piece("carry", tuple(pos - Vector((0, 0, 0.02))), (0, 0, 20), mark=1.0)
    else:
        k = ease((u - 0.45) / 0.55)
        pos = tgt.lerp(src, k) + Vector((0, 0, 0.1 * math.sin(math.pi * k)))
    return pos, cur.x - 0.15


def numbered_pile(n, k_last=1.0):
    """Pieces at the left end of the front table: the numbered ones (with scribbles) stacked, and a loose unnumbered heap."""
    rng = random.Random(11)
    base = WT.matrix_world @ Vector((PILE_X, 0.0, WT_Z))
    for i in range(14):
        off = Vector((rng.uniform(-0.22, 0.22), rng.uniform(-0.18, 0.18), 0.012 + 0.028 * (i // 4)))
        piece(f"heap{i}", tuple(base + off), (rng.uniform(-8, 8), rng.uniform(-8, 8), rng.uniform(0, 360)),
              col="white" if i % 2 else "#dfe2df")
    return base


# ----------------------------------------------------------------------------------------------------------------- shots
def anim_S1(fr):
    """'It's bigger than the printer...': open close on the laptop (the bumper file, far bigger than the bed - real slicer
    clip pinned on the key screen), pull back: the whole bumper skin in front of the tiny printer, hanging off both sides;
    Pip looks from the bumper to the printer, worried; Gus at the laptop."""
    t, u = fr / FPS, prog(fr, "S1")
    whole_bumper("bump", (0.35, 3.45, TABLE_Z + 0.53), R=0.5, rz=0, scale=1.6)   # on the printer lid, hanging off both sides
    m, lid = talk("PIP", t)
    acc = accent("PIP", t)
    lk = ease(cl((t - wt(1, 2)) / 0.4))
    pose(PIP, loc=tuple(PIP_LAP), rz=-28, hips=(-3, 0, 0), head=(-4 + 5 * acc, 0, lerp(-10, 25, lk)),
         armL=(-35, 0, 10), armR=(-35, 0, -10), mouth=m, lid=lid, look=lerpv((0.4, 0.1), (0.7, 0.4), lk))
    gm, glid = talk("GUS", t)
    pose(GUS, loc=tuple(GUS_LAP), rz=35, hips=(6, 0, 0), head=(10, 0, 0), armL=(-50, 0, 8), armR=(-50, 0, -8), mouth=gm, lid=glid,
         look=(-0.3, -0.4))
    k = ease(cl(u / 0.8))
    near_loc, near_tgt = Vector((1.25, 2.45, 1.1)), Vector((1.31, 2.98, 1.02))
    far_loc, far_tgt = Vector((0.3, 1.3, 1.3)), Vector((0.22, 2.9, 0.95))
    loc = near_loc.lerp(far_loc, k) + Vector((0.0, 0.0, 0.2 * math.sin(math.pi * k)))
    look(cam, loc, near_tgt.lerp(far_tgt, k), lerp(32, 18, k))


def anim_S2(fr):
    """'So we cut it up. By hand.': over Gus's shoulder onto the laptop (the real manual-cut clip on the key screen); a
    stack of cut pieces grows beside the laptop; the wall clock starts to turn."""
    t, u = fr / FPS, prog(fr, "S2")
    clock_spin(u * 0.25)
    n_cut = int(cl((t - wt(2, 2)) / (LN[2]["t1"] - wt(2, 2) + 0.4)) * 7)
    base = Vector((2.0, 2.9, TABLE_Z))
    for i in range(n_cut):
        piece(f"cut{i}", tuple(base + Vector((0.03 * (i % 2), 0.0, 0.025 * i))), (0, 0, 10 * i), col="white" if i % 2 else "#dfe2df")
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    tap = 0.03 * abs(math.sin(t * 13))
    pose(GUS, loc=tuple(GUS_LAP), rz=35, hips=(8, 0, 0), head=(12 + 4 * acc, 0, -4), mouth=m, lid=lid, look=(-0.3, -0.5))
    bpy.context.view_layer.update()
    kb = LAPTOP.matrix_world @ Vector((0.0, -0.05, 0.05))
    aim_arm(GUS, "L", kb + Vector((-0.1, 0.0, tap)))
    aim_arm(GUS, "R", kb + Vector((0.1, 0.0, 0.03 - tap)))
    look(cam, (0.85 + 0.06 * u, 1.55, 1.42), (1.55, 2.85, 1.12), 24)


def anim_S3(fr):
    """'Number every piece...': front table, close: Gus marks each piece with a marker; sage scribbles pop on one after
    another (never numerals)."""
    t, u = fr / FPS, prog(fr, "S3")
    clock_spin(0.25 + u * 0.25)
    numbered_pile(0)
    rng = random.Random(4)
    row0 = WT.matrix_world @ Vector((-0.5, 0.2, WT_Z + 0.012))
    t_s = LN[3]["t0"] - 0.1
    per = 0.32
    cur = int(max(0, t - t_s) / per)
    for i in range(7):
        k = cl((t - t_s - i * per) / per)
        pos = row0 + Vector((0.2 * i, 0.06 * (i % 2), 0.0))
        piece(f"row{i}", tuple(pos), (0, 0, rng.uniform(-20, 20)), mark=k * 1.2, col="white" if i % 2 else "#dfe2df")
    ci = min(cur, 6)
    tip = row0 + Vector((0.2 * ci - 0.03 + 0.06 * cl((t - t_s - ci * per) / per), 0.06 * (ci % 2) - 0.03, 0.06 + 0.02 * abs(math.sin(t * 20))))
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    pose(GUS, loc=tuple(WT.matrix_world @ Vector((-0.2 + 0.2 * ci * 0.6, GUS_BEHIND, 0.0))), rz=0, hips=(14, 0, 0),
         head=(20 + 3 * acc, 0, 0), mouth=m, lid=lid, look=(0.0, -0.7))
    hp = aim_arm(GUS, "R", tip + Vector((0.02, 0.05, 0.08)))
    marker("mk", tuple(hp + Vector((0.0, -0.02, -0.03))), (25, 0, 0))
    aim_arm(GUS, "L", row0 + Vector((0.2 * ci - 0.12, 0.08, 0.06)))
    look(cam, tuple(WT.matrix_world @ Vector((0.05 + 0.2 * u, -1.55, 1.4))), tuple(WT.matrix_world @ Vector((0.05 + 0.2 * u, 0.25, 0.95))), 26)


def gus_placing(t, t_start, gus_x_follow=True, head_down=True):
    """Gus at the front table laying pieces on the plates one at a time (S4, S5)."""
    n_done = placed_count(t, t_start)
    numbered_pile(0)
    hand, gx = fill_plates(n_done, t, t_start, GUS)
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    pose(GUS, loc=(gx, WT.location.y + GUS_BEHIND, 0.0), rz=0, hips=(12, 0, 0), head=(18 + 3 * acc, 0, 0) if head_down else (6, 0, 0),
         mouth=m, lid=lid, look=(0.0, -0.7) if head_down else (0.0, 0.0))
    if hand is not None:
        aim_arm(GUS, "R", hand + Vector((0, 0.04, 0.05)))
    return gx


def anim_S4(fr):
    """'...then lay each one flat on the print bed.': Gus lays numbered pieces on the build plates one by one; the camera
    trucks right along the row of plates, which runs out of frame - there are a lot more to go."""
    t, u = fr / FPS, prog(fr, "S4")
    set_vis(STOOL, False)          # it sits between the camera and the table on this truck
    clock_spin(0.5 + u * 0.3)
    gx = gus_placing(t, SF["S4"][0] / FPS - 2.4)
    xc = gx + 0.1 + 0.1 * u
    look(cam, (xc, WT.location.y - 1.75, 1.5), (xc + 0.2, WT.location.y + 0.3, 1.0), 24)


def anim_S5(fr):
    """'Is it done yet?' '...No.': wide: Pip slumped on the stool in front; behind, Gus keeps laying pieces on plates and
    answers without looking up; the clock spins like a fan."""
    t, u = fr / FPS, prog(fr, "S5")
    clock_spin(0.8 + 2.5 * u, rate=2.0)
    gus_placing(t, SF["S4"][0] / FPS - 2.4, head_down=True)
    pm, plid = talk("PIP", t)
    acc = accent("PIP", t)
    slump = 1 - 0.6 * win(t, LN[5]["t0"] - 0.1, LN[5]["t1"] + 0.1, 0.1, 0.4)
    pose(PIP, loc=(STOOL.location.x, STOOL.location.y, 0.6), rz=25, hips=(16 * slump, 0, 0), head=(14 * slump - 10 * (1 - slump) + 4 * acc, 0, 22),
         armL=(-20, 0, 15), armR=(-20, 0, -15), legL=(-80, 0, 0), legR=(-80, 0, 0), mouth=pm, lid=plid, look=(0.6, 0.5))
    look(cam, (-0.5, -1.6, 1.3), (0.15, 1.4, 0.9), 20)


def anim_S6(fr):
    """'There has to be a better way.': Pip to camera, close, impatient; Gus out of focus behind, still placing."""
    t, u = fr / FPS, prog(fr, "S6")
    clock_spin(3.3 + 2.0 * u, rate=2.0)
    gus_placing(t, SF["S4"][0] / FPS - 2.4)
    pm, plid = talk("PIP", t)
    acc = accent("PIP", t)
    pose(PIP, loc=(STOOL.location.x, STOOL.location.y, 0.6), rz=0, hips=(-4, 0, 0), head=(-4 + 6 * acc, 0, 0),
         armL=(-25, 0, 15), armR=(-25, 0, -15), legL=(-80, 0, 0), legR=(-80, 0, 0), mouth=pm, lid=plid, look=(0.0, -0.1))
    bpy.context.view_layer.update()
    hc = PIP.neck.matrix_world @ Vector((0, 0, PIP.head_c))
    look(cam, tuple(hc + Vector((0.05 - 0.04 * u, -1.15 + 0.12 * u, 0.0))), tuple(hc + Vector((0.0, 0.0, -0.1))), 40)


# phone hand-off, reversed: Gus pulls out the phone this time and holds it up to Pip (and us); the camera pushes along the
# screen normal until the screen fills the frame on the last frame (screen = key colour, corner-pinned with the capture)
PHONE_N = (0.0, -1.0, 0.1)
S7_LENS, S7_D0 = 35.0, 1.5
S7_DEND = (PHONE_H / 2) * S7_LENS / 18.0


def screen_corners_px(scr=None, local=None):
    from bpy_extras.object_utils import world_to_camera_view
    scr, local = scr or SCREEN, local or SCREEN_LOCAL
    bpy.context.view_layer.update()
    out = []
    for lc in local:
        v = world_to_camera_view(scn, cam, scr.matrix_world @ Vector(lc))
        out.append([round(v.x * 1080, 2), round((1 - v.y) * 1920, 2)])
    return out


def anim_S7(fr):
    """'...We made one.' 'Show me!': Gus turns from the plates, pulls a phone out of his vest pocket and holds it up,
    screen to us; Pip pops up beside it, excited; the camera pushes into the screen."""
    t, u = fr / FPS, prog(fr, "S7")
    clock_spin(5.3, rate=2.0)
    numbered_pile(0)
    for i in range(20):
        p = PLATES[i // 2]
        piece(f"onp{i}", (0, 0, 0), (0, 0, 15 + 25 * (i % 3)), mark=1.0,
              parent=temp(empty(f"onpp{i}", p, (-0.07 if i % 2 == 0 else 0.07, 0.0, 0.016))))
    G = Vector((-0.1, 0.25, 0.0))
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    turn = ease(cl((t - SF["S7"][0] / FPS) / 0.35))
    pose(GUS, loc=tuple(G), rz=lerp(150, 0, turn), hips=(4, 0, 0), head=(-2 + 3 * acc, 0, -6), mouth=m, lid=lid, look=(0.2, -0.1))
    bpy.context.view_layer.update()
    reach = ease(cl((t - (LN[8]["t0"] - 0.1)) / 0.45))
    chest = GUS.neck.matrix_world.translation + Vector((0.0, -0.12, -0.32))
    up_pt = GUS.neck.matrix_world.translation + Vector((0.16, -0.42, 0.02))
    hp = aim_arm(GUS, "R", chest.lerp(up_pt, reach))
    set_vis(PHONE, reach > 0.02)
    n = Vector(lerpv((0.3, 0.2, -1.0), PHONE_N, reach)).normalized()
    c = hp + Vector((0.0, -0.06, lerp(0.0, PHONE_H / 2 + 0.09, reach)))
    orient_phone(PHONE, c, n, up=lerpv((0, 1, 0), (0, 0, 1), reach))
    bpy.context.view_layer.update()
    pm, plid = talk("PIP", t)
    pop = eback(cl((t - (LN[9]["t0"] - 0.15)) / 0.22), 2.0)
    pose(PIP, loc=tuple(G + Vector((0.55, -0.12, 0.06 * math.sin(math.pi * cl((t - LN[9]["t0"]) / 0.3))))), rz=-30,
         hips=(-6 * pop, 0, 0), head=(-8, 0, 20 * pop), armL=(-40, 0, 10), armR=(-40, 0, -10), mouth=pm, lid=plid, look=(-0.6, 0.3))
    sc = SCREEN.matrix_world @ Vector((0, -0.0076, 0))
    ns = (SCREEN.matrix_world.to_3x3() @ Vector((0, -1, 0))).normalized()
    us = (SCREEN.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()
    kpush = cl((t - LN[9]["t0"]) / max(0.2, SF["S7"][1] / FPS - 1 / FPS - LN[9]["t0"]))
    wide_loc, wide_tgt = G + Vector((0.3, -2.2, 1.35)), G + Vector((0.25, 0.0, 1.1))
    if kpush <= 0.0:
        look(cam, tuple(wide_loc), tuple(wide_tgt), 32)
    else:
        ke = kpush ** 1.4
        d = S7_D0 * (S7_DEND / S7_D0) ** ke
        a = cl(kpush * 3)
        loc = wide_loc.lerp(sc + ns * d, a)
        tgt = wide_tgt.lerp(sc, a)
        look(cam, tuple(loc), tuple(tgt), lerp(32, S7_LENS, a), up=tuple(Vector((0, 0, 1)).lerp(us, a)))


ANIM = {k: globals()[f"anim_{k}"] for k in SF}


# ----------------------------------------------------------------------------------------------------------------- run
CORN = os.path.join(OUT, "screen_corners.json")
corners = json.load(open(CORN)) if os.path.exists(CORN) else dict(
    doc="Ep 6 screen corners for corner-pinning real footage. Pixels in the 1080x1920 frame, origin top-left, x right, y down. "
        "Corner order tl, tr, br, bl = the footage's upright corners. Cartoon frames at 30 fps. Screens render as flat key "
        "colour #ff00ff (camera rays only); use it as the matte. 'laptop' = S1/S2 (slicer clip), 'phone' = S7 (SeamForged).",
    width=1080, height=1920, fps=FPS, key_colour=KEY, corner_order=["tl", "tr", "br", "bl"], shots={})
CORNER_SHOTS = {**{k: ("laptop", LAP_SCREEN, LAP_LOCAL) for k in ("S1", "S2", "S3", "S4", "S5", "S6")}, "S7": ("phone", None, None)}
# The laptop is in the background of S3-S6 too (v1 review: its key screen showed magenta there).
ONLY = {int(x) for x in arg("--frames", "").split(",") if x}
EVERY = int(arg("--every", "1"))
for sh in SHOTS:
    f0, f1 = SF[sh]
    d = os.path.join(OUT, "stills" if STILLS else sh)
    os.makedirs(d, exist_ok=True)
    frames = [(f0 + f1) // 2] if STILLS else list(range(f0, f1))
    per, tsum, nr = {}, 0.0, 0
    for fr in frames:
        final = os.path.join(d, f"{sh}.png" if STILLS else f"{fr:04d}.png")
        need_c = sh in CORNER_SHOTS and not STILLS
        todo = ((fr - f0) % EVERY == 0 and not os.path.exists(final) and (not ONLY or fr in ONLY)) or STILLS
        if not (todo or need_c):
            continue
        CUR_T = fr / FPS
        reset()
        ANIM[sh](fr)
        bpy.context.view_layer.update()
        if need_c:
            kind, scr, loc_ = CORNER_SHOTS[sh]
            vis = scr is None and not PHONE.hide_render or scr is not None
            if vis:
                per[str(fr)] = screen_corners_px(scr, loc_)
        if not todo:
            continue
        scn.render.filepath = final[:-4] + "_tmp"
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        os.replace(final[:-4] + "_tmp.png", final)
        tsum += time.time() - t0
        nr += 1
        print(f"[ep6] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if per:
        corners["shots"][sh] = dict(frames=[f0, f1], screen=CORNER_SHOTS[sh][0], per_frame=per)
        if sh == "S7":
            corners["screen_full_frame"] = f1 - 1
        json.dump(corners, open(CORN, "w"), indent=1)
    if nr:
        print(f"[ep6] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
