"""Pip & Gus Ep 7 "Big printer or small printer?" - cartoon part (Blender 5.3, EEVEE cel look, series rig).

Reuses the series library from the pilot (projects/scan-tedium-explainer-reel/tools/partA_scene.py up to its "build all"
block: palette, toon materials + outlines, shop, Pip/Gus rig with the option-3 proportions and nametags, clock, laptop,
phone, EEVEE setup) and the pilot's talk/blink/expression machinery (partA_anim.py up to its shots). Everything
episode-specific lives here: two unbranded printers, the scoreboard, the bumper pieces, the nozzle close-up, 10 shots.

  blender -b --factory-startup -P ep7_scene.py -- --out FRAMES --timeline ../ep7_timeline.json --tagdir TEX
          [--shots S1,S2] [--scale 1] [--spp 8] [--every N] [--frames a,b] [--stills]

--stills renders one lookdev still per shot (its middle frame) to FRAMES/stills/<shot>.png instead of the animation.
Every frame is posed procedurally from the timeline (no keyframes) and written via a _tmp file, so renders resume.
Rules kept: no text/numerals/brands in 3D (scoreboard = icons + tick marks), Pip & Gus locked design, no arms.
"""
import sys, os, json, math, random, time

PILOT = "/home/user/Illumaesthetic-Video-Editor/projects/scan-tedium-explainer-reel/tools"
_src = open(os.path.join(PILOT, "partA_scene.py")).read()
_cut = _src.index("# ----------------------------------------------------------------------------------------------------------------- build all")
exec(compile(_src[:_cut], os.path.join(PILOT, "partA_scene.py"), "exec"), globals())

SHOTS = arg("--shots", "S1,S2,S3,S4,S5,S6,S7,S8,S9,S10").split(",")
STILLS = "--stills" in argv
CLOSE = Vector((30.0, 0.0, 0.0))     # the nozzle close-up set lives far off to the side of the shop

# ----------------------------------------------------------------------------------------------------------------- build
cam, sun = setup_render()
SHOP = build_shop()
for _ob in list(SHOP.children):      # Ep 7 shop: no car bay lines (no car in this episode)
    if _ob.name.startswith("bay"):
        bpy.data.objects.remove(_ob, do_unlink=True)
CLOCK, HANDS = build_clock(SHOP, loc=(-2.95, 3.48, 2.6), r=0.32)
PIP = build_char("PIP", PIP_SPEC)
GUS = build_char("GUS", GUS_SPEC)
PHONE, SCREEN = build_phone()


def build_printer(name, w, d, h, loc, nozzle=0.02, parent=None, enclosed=False):
    """Generic open-frame FDM printer, no brand: dark frame, sage accent rail, black bed, white print head on a gantry,
    a spool of white filament on the side. Origin = floor centre, front faces -y. Returns a dict of the moving parts."""
    s = h / 1.95
    g = empty(name, parent, loc)
    t = 0.05 * max(s, 0.35)
    fr = mat("dark")
    box(f"{name}_plinth", (w, d, 0.12 * h), (0, 0, 0.06 * h), fr, g, 0.01 * s + 0.004, 0.012)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"{name}_post{sx}{sy}", (t, t, h), (sx * (w - t) / 2, sy * (d - t) / 2, h / 2), fr, g, 0.004, 0.01)
    for sy in (-1, 1):
        box(f"{name}_topx{sy}", (w, t, t), (0, sy * (d - t) / 2, h - t / 2), mat("sage") if sy < 0 else fr, g, 0.004, 0.01)
    for sx in (-1, 1):
        box(f"{name}_topy{sx}", (t, d, t), (sx * (w - t) / 2, 0, h - t / 2), fr, g, 0.004, 0.01)
    bed_z = 0.36 * h
    bed = box(f"{name}_bed", (w * 0.78, d * 0.78, 0.035 * s + 0.01), (0, 0, bed_z), mat("#1c1d1c"), g, 0.004, 0.01)
    box(f"{name}_bedrim", (w * 0.8, d * 0.8, 0.012 * s + 0.004), (0, 0, bed_z - 0.02 * s - 0.004), mat("sage_l"), g, 0.002)
    for sx in (-1, 1):   # Z screws
        cyl(f"{name}_zrod{sx}", 0.012 * s + 0.004, h * 0.86, (sx * (w - t) / 2 * 0.86, (d - t) / 2 * 0.85, h * 0.5), mat("metal"), g, seg=12)
    # gantry: X beam spanning the width, moves along y; head carriage moves along x
    gy = empty(f"{name}_gantry", g, (0, 0, 0.8 * h))
    box(f"{name}_xbeam", (w - 2 * t, t * 0.9, t * 0.9), (0, 0, 0), fr, gy, 0.003, 0.01)
    head = empty(f"{name}_head", gy, (0, -t * 0.9, 0))
    hs = 0.16 * s + 0.05
    box(f"{name}_hbody", (hs, hs * 0.75, hs * 1.1), (0, -hs * 0.3, -hs * 0.2), mat("white"), head, hs * 0.12, 0.012)
    box(f"{name}_hstripe", (hs * 1.01, hs * 0.76, hs * 0.16), (0, -hs * 0.3, hs * 0.12), mat("sage"), head, hs * 0.05)
    cyl(f"{name}_fan", hs * 0.28, 0.01, (0, -hs * 0.68, -hs * 0.22), mat("dark"), head, axis="Y", seg=24)
    noz_len = max(0.03, hs * 0.5)
    cyl(f"{name}_noz", nozzle * 1.8, noz_len, (0, -hs * 0.3, -hs * 0.75 - noz_len / 2), mat("metal"), head, seg=16, r2=nozzle * 0.6)
    tip_z = 0.8 * h - hs * 0.75 - noz_len     # nozzle tip height (world, relative to the printer origin)
    if enclosed:   # desktop box: dark side/back/top panels, sage top band, see-through front door with a handle
        for sx in (-1, 1):
            box(f"{name}_side{sx}", (0.012, d, h * 0.9), (sx * w / 2, 0, h * 0.55), mat("#3a3d3a"), g, 0.004, 0.01)
        box(f"{name}_back", (w, 0.012, h * 0.9), (0, d / 2, h * 0.55), mat("#3a3d3a"), g, 0.004, 0.01)
        box(f"{name}_lid", (w + 0.01, d + 0.01, 0.03), (0, 0, h + 0.012), mat("sage"), g, 0.008, 0.012)
        box(f"{name}_door", (w * 0.96, 0.006, h * 0.62), (0, -d / 2 - 0.004, h * 0.6), mat("#cfe3d6", 0.28), g, 0.004)
        box(f"{name}_handle", (0.012, 0.02, h * 0.22), (w * 0.4, -d / 2 - 0.016, h * 0.6), mat("white"), g, 0.004, 0.006)
    # spool + filament
    sp = empty(f"{name}_spoolp", g, (-(w / 2) - 0.11 * s - 0.03, 0.1 * d, 0.62 * h))
    cyl(f"{name}_spool", 0.18 * s + 0.05, 0.1 * s + 0.03, (0, 0, 0), mat("white"), sp, axis="X", seg=32, bevel=0.01, ol=0.01)
    cyl(f"{name}_spoolhub", 0.07 * s + 0.02, 0.1 * s + 0.035, (0, 0, 0), mat("sage"), sp, axis="X", seg=24)
    return dict(g=g, w=w, d=d, h=h, s=s, bed=bed, bed_z=bed_z, gantry=gy, head=head, tip_z=tip_z, top=bed_z + 0.02 * s + 0.01)


BIG = build_printer("BIGP", 1.5, 1.1, 1.95, (-1.6, 2.75, 0), nozzle=0.022)
# long side table for the small printers and the laptop
TABLE = empty("TABLE", None, (1.15, 3.0, 0))
box("tbl_top", (1.9, 0.62, 0.06), (0, 0, 0.82), mat("wood"), TABLE, 0.012, 0.018)
for _sx in (-1, 1):
    for _sy in (-1, 1):
        box(f"tbl_leg{_sx}{_sy}", (0.06, 0.06, 0.8), (_sx * 0.89, _sy * 0.26, 0.4), mat("dark"), TABLE, 0.004, 0.01)
box("tbl_shelf", (1.8, 0.55, 0.035), (0, 0, 0.22), mat("wood_d"), TABLE, 0.004, 0.012)
TABLE_Z = 0.85
SMALLS = [build_printer(f"SMALL{i}", 0.44, 0.44, 0.5, (x, 3.0, TABLE_Z), nozzle=0.006, enclosed=True) for i, x in enumerate((0.5, 0.98, 1.46))]
LAPTOP, UI = build_laptop(None, loc=(1.86, 2.95, TABLE_Z), rz=-12)


def piece_shapes():
    """Exported, cut bumper pieces as flat UI tiles on the laptop screen (no numbers: distinct greys + sage outline)."""
    out = []
    for row in range(2):
        for k in range(5):
            x0 = -0.17 + k * 0.071
            y0 = 0.035 - row * 0.085
            bulge = 0.012 * math.sin(math.pi * (k + 0.5) / 5)
            pts = [(x0, y0 - 0.03), (x0 + 0.056, y0 - 0.03), (x0 + 0.056, y0 + 0.022 + bulge), (x0 + 0.028, y0 + 0.03 + bulge),
                   (x0, y0 + 0.022 + bulge)]
            out.append(pts)
    return out


box("ui_bg", (0.43, 0.28, 0.001), (0, 0, 0.0005), emit("#1d201e", 1.0), UI)
for _i, _pts in enumerate(piece_shapes()):
    poly(f"ui_piece{_i}", [(x * 1.0, y) for x, y in _pts], emit("sage_l", 1.0), UI, z=0.0012)
    poly(f"ui_piecef{_i}", [((x - sum(p[0] for p in _pts) / 5) * 0.86 + sum(p[0] for p in _pts) / 5,
                            (y - sum(p[1] for p in _pts) / 5) * 0.86 + sum(p[1] for p in _pts) / 5) for x, y in _pts],
         emit("ui_piece" if _i % 2 else "ui_piece2", 1.0), UI, z=0.0018)
box("ui_bar", (0.4, 0.022, 0.001), (0, 0.115, 0.0015), emit("#2f3431", 1.0), UI)
cyl("ui_ok", 0.009, 0.001, (0.18, 0.115, 0.0022), emit("sage_l", 1.4), UI, axis="Z", seg=16)

# scoreboard: chalkboard hanging on two chains in front of the roll-up door; icons + tick marks only
BOARD_HOME = Vector((-0.25, 3.3, 2.45))
BOARD = empty("BOARD", None, tuple(BOARD_HOME))
box("brd_frame", (1.0, 0.05, 0.8), (0, 0, 0), mat("wood"), BOARD, 0.012, 0.02)
box("brd_slate", (0.9, 0.055, 0.7), (0, -0.003, 0), mat("#2d312e"), BOARD, 0.006)
box("brd_div", (0.018, 0.06, 0.6), (0, -0.006, -0.02), mat("white"), BOARD)
for _sx in (-1, 1):
    cyl(f"brd_chain{_sx}", 0.008, 2.0, (_sx * 0.38, 0, 0.4 + 1.0), mat("metal"), BOARD, seg=8)


def board_icon(name, cx, size):
    """Printer icon in chalk: outline square frame on legs with a little head - big or small by size."""
    g = empty(name, BOARD, (cx, -0.035, 0.16))
    w = size
    for sx in (-1, 1):
        box(f"{name}_p{sx}", (0.014, 0.004, w), (sx * w / 2, 0, 0), mat("white"), g)
    box(f"{name}_t", (w + 0.014, 0.004, 0.014), (0, 0, w / 2), mat("white"), g)
    box(f"{name}_b", (w + 0.014, 0.004, 0.014), (0, 0, -w / 2), mat("white"), g)
    box(f"{name}_bed", (w * 0.7, 0.004, 0.01), (0, 0, -w * 0.12), mat("sage_l"), g)
    box(f"{name}_hd", (w * 0.22, 0.004, w * 0.18), (w * 0.1, 0, w * 0.22), mat("white"), g)
    return g


board_icon("ico_big", -0.22, 0.26)
board_icon("ico_small", 0.22, 0.12)
TICKS = {"BIG": [], "SMALL": []}
for _side, _cx in (("BIG", -0.22), ("SMALL", 0.22)):
    for _k in range(3):
        _p = empty(f"tick_{_side}{_k}", BOARD, (_cx - 0.11 + _k * 0.11, -0.037, -0.17))
        box(f"tick_{_side}{_k}m", (0.04, 0.004, 0.2), (0, 0, 0), mat("white"), _p, 0.006)
        TICKS[_side].append(_p)


def arc_piece(name, R, th, hgt, a0, a1, m, parent, loc=(0, 0, 0), rot=(0, 0, 0), n=10):
    """A slice of a bumper skin: an annular sector of radius R (outer), thickness th, height hgt, from angle a0 to a1 (deg,
    0 = toward -y), with a rounded lower lip. Origin at the arc centre on the floor."""
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


BUMPER_SPAN = (-55.0, 55.0)


def bumper(name, n_pieces, centre, R=0.8, rz=0.0, gap=1.2, pop=None, seam_glow=0.0, hidden=()):
    """A bumper skin cut into n pieces lying on the floor, open side to the back. pop(i) -> 0..1 scale-in per piece."""
    g = temp(empty(name, None, centre, (0, 0, rz)))
    a0, a1 = BUMPER_SPAN
    step = (a1 - a0) / n_pieces
    for i in range(n_pieces):
        if i in hidden:
            continue
        k = 1.0 if pop is None else pop(i)
        if k <= 0.01:
            continue
        p = empty(f"{name}_p{i}", g, (0, 0, 0))
        mid = a0 + step * (i + 0.5)
        sh = arc_piece(f"{name}_s{i}", R, 0.06, 0.34, a0 + step * i + gap / 2, a0 + step * (i + 1) - gap / 2,
                       mat("white" if i % 2 else "#dfe2df"), p)
        c = Vector((R * math.sin(math.radians(mid)), -R * math.cos(math.radians(mid)), 0.17))
        p.location = c * (1 - k)
        p.scale = (k, k, k)
        if seam_glow > 0.01 and i < n_pieces - 1:   # seam markers: sage strips on each cut
            a = math.radians(a0 + step * (i + 1))
            s = cyl(f"{name}_seam{i}", 0.012 + 0.008 * seam_glow, 0.36, ((R - 0.02) * math.sin(a), -(R - 0.02) * math.cos(a), 0.17),
                    emit("sage_l", 1.6, min(1.0, seam_glow)), g, seg=10)
    return g


# failed-print shelf (running gag): wall shelf left of the big printer with three spaghetti lumps
box("fshelf", (0.7, 0.22, 0.035), (-3.0, 3.45, 1.55), mat("wood"), SHOP, 0.006, 0.012)
for _k, (_x, _c) in enumerate(((-3.22, "white"), (-3.0, "sage_l"), (-2.78, "#dfe2df"))):
    _rng = random.Random(_k + 3)
    for _j in range(9):
        torus(f"spag{_k}_{_j}", 0.04 + 0.02 * _rng.random(), 0.006, (_x + _rng.uniform(-0.05, 0.05), 3.43 + _rng.uniform(-0.04, 0.04),
              1.6 + _rng.uniform(0, 0.08)), mat(_c), SHOP, rot=(_rng.uniform(0, 180), _rng.uniform(0, 180), 0))

# nozzle close-up set (S4): two print heads over one plate, far off to the side; big (left) vs small (right)
CU = empty("CLOSEUP", None, tuple(CLOSE))
box("cu_plate", (1.1, 0.6, 0.04), (0, 0, 0.0), mat("#1c1d1c"), CU, 0.004, 0.01)
box("cu_floor", (8, 8, 0.02), (0, 0, -0.4), mat("floor"), CU)
box("cu_wall", (8, 0.1, 6), (0, 1.2, 2), mat("wall"), CU)
box("cu_band", (8, 0.03, 0.16), (0, 1.14, 0.9), mat("sage"), CU)
box("cu_div", (0.012, 0.6, 0.01), (0, 0, 0.022), mat("sage_l"), CU)
CU_HEADS = {}
for _nm, _x, _hs, _nr in (("big", -0.24, 0.24, 0.032), ("small", 0.24, 0.13, 0.011)):
    _h = empty(f"cu_head_{_nm}", CU, (_x, 0.0, 0.5))
    box(f"cu_hb_{_nm}", (_hs, _hs * 0.8, _hs), (0, 0, _hs * 0.5 + 0.1), mat("white"), _h, _hs * 0.12, 0.012)
    box(f"cu_hs_{_nm}", (_hs * 1.01, _hs * 0.81, _hs * 0.14), (0, 0, _hs * 0.82 + 0.1), mat("sage"), _h, _hs * 0.04)
    for _k in (-1, 0, 1):   # three round vent holes (no symbols)
        cyl(f"cu_vent{_k}_{_nm}", _hs * 0.07, 0.01, (_k * _hs * 0.22, -_hs * 0.41, _hs * 0.36 + 0.1), mat("dark"), _h, axis="Y", seg=16)
    cyl(f"cu_noz_{_nm}", _nr * 1.9, 0.1, (0, 0, 0.05), mat("metal"), _h, seg=24, r2=_nr * 0.55)
    box(f"cu_rail_{_nm}", (0.03, 0.03, 1.4), (0, 0.06, _hs + 0.1 + 0.7), mat("dark"), _h, 0.004, 0.01)   # carriage rail up out of frame
    CU_HEADS[_nm] = dict(piv=_h, x=_x, nr=_nr)


def beads(name, xc, n_layers, r, length, k_cur, parent):
    """Stacked extrusion beads (layer lines): n_layers full beads plus the current one drawn to fraction k_cur."""
    g = temp(empty(name, parent, (xc, 0, 0.02)))
    for i in range(n_layers + 1):
        L = length if i < n_layers else length * k_cur
        if L < 0.01:
            continue
        x0 = -length / 2 if i % 2 == 0 else length / 2 - L
        cyl(f"{name}_{i}", r, L, (x0 + L / 2, 0, r * (2.0 * i + 1)), mat("white" if i % 2 else "#bfc4bf"), g, axis="X", seg=16,
            bevel=0.0, ol=max(0.002, r * 0.1))
    return g


# pieces mountain (S7) + glue bottle
def pieces_mountain(name, centre, n, rng_seed=9, k=1.0):
    g = temp(empty(name, None, centre))
    rng = random.Random(rng_seed)
    for i in range(int(n * k)):
        rr = 0.42 * math.sqrt(rng.random())
        a = rng.uniform(0, 2 * math.pi)
        z = 0.32 * (1 - (rr / 0.42) ** 1.3) * rng.uniform(0.5, 1.0)
        p = empty(f"{name}_{i}", g, (rr * math.cos(a), rr * math.sin(a), z), (rng.uniform(-40, 40), rng.uniform(-40, 40), rng.uniform(0, 360)))
        arc_piece(f"{name}_s{i}", 0.5, 0.04, 0.16, -9, 9, mat("white" if i % 2 else "#dfe2df"), p, loc=(0, 0.5, -0.08))
    return g


def glue_bottle(name, loc):
    g = temp(empty(name, None, loc))
    cyl(f"{name}_b", 0.05, 0.16, (0, 0, 0.08), mat("white"), g, seg=20, bevel=0.012, ol=0.008)
    box(f"{name}_l", (0.075, 0.01, 0.07), (0, -0.05, 0.08), mat("sage"), g, 0.004)
    cyl(f"{name}_n", 0.02, 0.06, (0, 0, 0.19), mat("red"), g, seg=14, r2=0.006, ol=0.006)
    return g


# ----------------------------------------------------------------------------------------------------------------- helpers
_temp = []


def temp(ob):
    _temp.append(ob)
    return ob


def aim_arm(ch, side, target):
    sh = ch.arms[side]
    ch.elbows[side].rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    tl = sh.parent.matrix_world.inverted() @ Vector(target)
    d = tl - sh.location
    sh.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    return ch.hands[side].matrix_world.translation.copy()


def place_head_xy(ch, want):
    bpy.context.view_layer.update()
    h = ch.neck.matrix_world.translation
    ch.root.location.x += want[0] - h.x
    ch.root.location.y += want[1] - h.y
    bpy.context.view_layer.update()


def set_board(big=0, small=0, pops=None, flick=0.0, drop=1.0):
    """Ticks shown per side (pops: {('BIG', i): 0..1} scale-in), flick: tie flicker (alternating dim), drop: 0 up .. 1 hung."""
    pops = pops or {}
    for side, n in (("BIG", big), ("SMALL", small)):
        for i, p in enumerate(TICKS[side]):
            k = pops.get((side, i), 1.0 if i < n else 0.0)
            set_vis(p, k > 0.01)
            p.scale = (max(k, 0.01),) * 3
    yoff = (1 - drop) * 2.2
    BOARD.location = BOARD_HOME + Vector((0, 0, yoff))
    BOARD.rotation_euler = (0, math.radians(4 * math.sin(drop * 9) * (1 - drop) if drop < 1 else 0), 0)
    for nm in ("ico_big", "ico_small"):
        ob = bpy.data.objects[nm]
        on = True
        if flick > 0:
            on = (int(flick * 8) % 2 == 0) == (nm == "ico_big")
        ob.scale = (1.0, 1.0, 1.0) if on else (0.86, 0.86, 0.86)


def run_printer(P, t, speed=1.0, active=True, part_h=0.0, part=(0.5, 0.4)):
    if P is BIG and part_h < 0.002:
        part_h, part = 0.07, (0.62, 0.42)
    """Print head raster on X, gantry steps on Y; a part grows on the bed (a slab of the given footprint fraction)."""
    w, d = P["w"], P["d"]
    if active:
        P["head"].location.x = (w * 0.3) * math.sin(t * 2.2 * speed)
        P["gantry"].location.y = (d * 0.22) * math.sin(t * 0.7 * speed + 1.0)
    if part_h > 0.002:
        temp(box(f"{P['g'].name}_part", (w * part[0], d * part[1], part_h), (0, 0, P["top"] + part_h / 2), mat("white"), P["g"], 0.003, 0.008))


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
    for P in SMALLS[1:]:
        set_vis(P["g"], False)
        P["g"].scale = (1, 1, 1)
    for P in [BIG] + SMALLS:
        P["head"].location.x = 0
        P["gantry"].location.y = 0
    set_board(0, 0)
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
    """Ep 7 expressions (eye shapes only). Gus: dry, slightly annoyed while explaining, weary on 'slower', flat on
    '...This piece is', small sigh droop, skeptical '...Show-off'. Pip: excited 'It's cut!', curious question, excited
    'small ones win!', impatient 'done yet?', curious 'who wins?', surprised pop on 'Wait.', excited 'HUGE'."""
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
        L = L_(3)
        if L:
            blend("weary", 0.8 * win(t, L["t0"], L["t1"], 0.12, 0.3))
        L = L_(8)
        if L:
            k = win(t, L["t0"], L["words"][2]["t1"] + 0.1, 0.06, 0.3)        # flat "...This piece is."
            st["fL"] = st["fR"] = lerp(st["fL"], 0.55, k)
            st["tL"] = st["tR"] = lerp(st["tL"], 16, k)
            for a, b in L.get("sighs", []):                                  # small sigh droop
                ks = win(t, a, b, 0.12, 0.35)
                st["fL"] = st["fR"] = max(st["fL"], 0.62 * ks)
                st["tL"] = st["tR"] = lerp(st["tL"], -4, ks)
        L = L_(7)
        if L:                                                                # eye-roll at "Is it done yet?"
            u = (t - L["t0"]) / max(0.3, L["t1"] - L["t0"])
            if 0 <= u <= 1:
                st["roll"] = (math.cos(math.pi * (1 - u)) * 0.9, math.sin(math.pi * u) * 1.0)
        L = L_(12)
        if L:
            blend("skeptical", win(t, L["t0"] - 0.1, L["t1"] + 1.0, 0.12, 0.2))
    else:
        L = L_(1)
        if L:
            blend("excited", win(t, L["t0"], L["words"][1]["t1"], 0.08, 0.2))
            blend("curious", win(t, L["words"][2]["t0"], L["t1"], 0.12, 0.3))
        L = L_(5)
        if L:
            blend("excited", win(t, L["t0"], L["t1"] + 0.3, 0.08, 0.25))
        L = L_(7)
        if L:
            k = win(t, L["t0"], L["t1"], 0.05, 0.3)
            blend("impatient", k)
            for b0 in (L["t0"], L["t0"] + 0.24):
                bu = (t - b0) / 0.12
                if 0 <= bu < 1:
                    st["fL"] = st["fR"] = max(st["fL"], 1 - abs(2 * bu - 1))
        L = L_(9)
        if L:
            blend("curious", win(t, L["t0"], L["t1"] + 0.4, 0.12, 0.3))
        L = L_(11)
        if L:
            tw = L["words"][0]["t0"]
            if t >= tw - 0.03:
                pop = eback((t - tw + 0.03) / 0.2, 2.2)
                k = win(t, tw, L["words"][0]["t1"] + 0.4, 0.03, 0.3)
                st["scale"] = lerp(1.0, 1.3, k) * (0.92 + 0.08 * pop)
                st["fL"] = st["fR"] = st["fL"] * (1 - k)
            blend("excited", win(t, L["words"][-1]["t0"] - 0.1, L["t1"] + 0.6, 0.08, 0.25))
    return st


def prog(fr, sh):
    f0, f1 = SF[sh]
    return (fr - f0) / max(1, f1 - 1 - f0)


def gus_listen_look(t):
    return (0.6, 0.3) if speaking("PIP", t) else (0.0, 0.0)


def pop_at(t, ta, dur=0.18):
    """0..1 with overshoot, starting at ta."""
    if t < ta:
        return 0.0
    return min(1.15, eback((t - ta) / dur, 2.0)) if t - ta < dur * 1.5 else 1.0


def wt(n, i):
    return LN[n]["words"][i]["t0"]


# ----------------------------------------------------------------------------------------------------------------- shots
def anim_S1(fr):
    """Callback to Ep 6: open close on the laptop (exported cut pieces), pull back to the wide shop; Pip asks; the
    scoreboard drops in at the end."""
    t, u = fr / FPS, prog(fr, "S1")
    set_board(0, 0, drop=cl((u - 0.62) / 0.3))
    run_printer(BIG, t, 0.4, active=False)
    m, lid = talk("PIP", t)
    acc = accent("PIP", t)
    pose(PIP, loc=(0.6, 1.55, 0.04 * math.sin(math.pi * cl((t - wt(1, 1)) / 0.25))), rz=-20, hips=(-4, 0, 0),
         head=(-10 + 6 * acc, 0, lerp(-35, 5, ease(cl((t - wt(1, 2)) / 0.5)))), armL=(-140, 0, -18), elbowL=-25, armR=(-35, 0, -20),
         elbowR=-40, mouth=m, lid=lid, look=lerpv((0.7, -0.2), (-0.6, 0.6), ease(cl((t - wt(1, 2)) / 0.5))))
    gm, glid = talk("GUS", t)
    pose(GUS, loc=(-0.3, 1.85, 0), rz=10, head=(4, 0, -18), armL=(-30, 0, 6), armR=(-20, 0, -6), mouth=gm, lid=glid,
         look=(0.7, 0.2))
    # callback: close on the laptop's exported pieces, then an arc up and back over the characters' heads to the shop
    k = ease(cl(u / 0.85))
    near_loc, near_tgt = Vector((1.72, 2.25, 1.13)), Vector((1.86, 2.98, 1.02))
    far_loc, far_tgt = Vector((-0.05, -2.5, 1.5)), Vector((0.0, 2.3, 1.2))
    loc = near_loc.lerp(far_loc, k) + Vector((0.0, 0.0, 0.95 * math.sin(math.pi * k)))
    look(cam, loc, near_tgt.lerp(far_tgt, k), 28)


BIG_BUMP = (-0.95, 0.75, 0.0)
SMALL_BUMP = (0.55, 0.75, 0.0)
BUMP_R = 0.55


def anim_S2(fr):
    """'Big one? Fewer pieces. Fewer seams.' Both bumpers on the floor: 3 big chunks vs a crowd of 12; seams glow on
    'seams'. BIG +1 on 'pieces', +1 on 'seams'."""
    t = fr / FPS
    tp, ts = wt(2, 3), wt(2, 5)            # "pieces", "seams" (Fewer pieces. Fewer seams.)
    tf = wt(2, 2)                          # first "Fewer"
    bumper("bb", 3, BIG_BUMP, R=BUMP_R, pop=lambda i: pop_at(t, tf - 0.25 + 0.12 * i))
    bumper("sb", 12, SMALL_BUMP, R=BUMP_R, gap=2.0, pop=lambda i: pop_at(t, tf - 0.15 + 0.05 * i, 0.12))
    glow = win(t, ts, ts + 1.0, 0.1, 0.3)
    if glow > 0.01:
        bumper("bbs", 3, BIG_BUMP, R=BUMP_R, seam_glow=glow, pop=lambda i: 0.0)
        bumper("sbs", 12, SMALL_BUMP, R=BUMP_R, gap=2.0, seam_glow=glow, pop=lambda i: 0.0)
    set_board(0, 0, pops={("BIG", 0): pop_at(t, tp + 0.1), ("BIG", 1): pop_at(t, ts + 0.1)})
    run_printer(BIG, t, 0.4, active=False)
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    point = ease(cl((t - wt(2, 0)) / 0.3))
    pose(GUS, loc=(-0.2, 1.7, 0), rz=-10, head=(10 + 5 * acc, 0, -8), armL=(-20, 0, 6), armR=lerpv((-10, 0, -6), (-55, 0, 35), point),
         elbowR=-15, mouth=m, lid=lid, look=(-0.4, -0.6))
    pm, plid = talk("PIP", t)
    pose(PIP, loc=(1.0, 1.55, 0), rz=-35, head=(14, 0, 10), mouth=pm, lid=plid, look=(-0.6, -0.7))
    look(cam, (-0.2, -2.6, 1.55), (-0.2, 1.6, 0.85), 28)


def anim_S3(fr):
    """'But it's slower...': medium on the big printer, its head crawling; the wall clock spins up beside it."""
    t, u = fr / FPS, prog(fr, "S3")
    run_printer(BIG, t, 0.18, part_h=0.06 + 0.01 * u, part=(0.6, 0.45))
    am = 60 + 360 * (1.2 * u + 2.0 * u * u)
    HANDS["minute"].rotation_euler = (0, math.radians(am), 0)
    HANDS["second"].rotation_euler = (0, math.radians(200 + 360 * (5 * u + 8 * u * u)), 0)
    HANDS["hour"].rotation_euler = (0, math.radians(300 + (am - 60) / 12), 0)
    m, lid = talk("GUS", t, 0.2)
    acc = accent("GUS", t)
    pose(GUS, loc=(-0.05, 1.35, 0), rz=-35, head=(8 + 4 * acc, 0, 20), armL=(-15, 0, 4), armR=(-15, 0, -4), mouth=m, lid=lid,
         look=(0.6, 0.0))
    look(cam, (-0.95, -0.9, 1.55), (-1.75, 2.6, 1.45), 30)


def anim_S4(fr):
    """'...and the bigger nozzle means less detail.': close-up, side by side: the fat nozzle lays a few chunky beads, the
    fine one many thin lines - the same wall height, much finer steps on the right."""
    t, u = fr / FPS, prog(fr, "S4")
    for nm, nl, r in (("big", 4, 0.034), ("small", 12, 0.0113)):
        H = CU_HEADS[nm]
        prog_l = 1.0 + u * (nl - 1.0)
        n_full, k = min(int(prog_l), nl), prog_l - int(prog_l)
        beads(f"bd_{nm}", H["x"], n_full, r, 0.34, k if n_full < nl else 0.0, CU)
        x_cur = (-0.17 + 0.34 * k) if n_full % 2 == 0 else (0.17 - 0.34 * k)
        H["piv"].location = (H["x"] + x_cur, 0.0, 0.02 + r * (2.0 * n_full + 2.0))
    look(cam, CLOSE + Vector((0.0, -1.85, 0.62)), CLOSE + Vector((0.0, 0.0, 0.3)), 40)


def anim_S5(fr):
    """'So small ones win!': Pip pats the small printer; the SMALL column takes the two points for 'slower' and 'less
    detail' as he says it."""
    t = fr / FPS
    run_printer(SMALLS[0], t, 2.0, part_h=0.03)
    t0 = LN[5]["t0"]
    set_board(0 + 2, 0, pops={("SMALL", 0): pop_at(t, t0 - 0.05), ("SMALL", 1): pop_at(t, t0 + 0.25)})
    m, lid = talk("PIP", t)
    acc = accent("PIP", t)
    pat = abs(math.sin(t * 9)) * win(t, wt(5, 1), LN[5]["t1"], 0.05, 0.1)
    pose(PIP, loc=(0.05, 2.4, 0.0), rz=-25, hips=(-4, 0, 0), head=(-6 + 6 * acc, 0, 25), armR=(-60, 0, -30), elbowR=-30, mouth=m,
         lid=lid, look=(-0.6, 0.4))
    aim_arm(PIP, "L", Vector((0.27, 2.78, 1.12 + 0.05 * pat)))
    look(cam, (0.45, -0.6, 1.45), (0.4, 2.9, 1.35), 30)


def anim_S6(fr):
    """'Sharper, sure. And you can run a few.': two more small printers pop up beside the first, all three printing.
    SMALL +1 on 'few'."""
    t = fr / FPS
    t_run = wt(6, 2)                          # "And"
    for i, P in enumerate(SMALLS):
        k = 1.0 if i == 0 else pop_at(t, t_run + 0.12 * i, 0.2)
        if k <= 0.01:
            continue
        set_vis(P["g"], True)
        P["g"].scale = (k, k, k)
        run_printer(P, t + i * 0.7, 2.0, part_h=0.03 if i == 0 else 0.0)
    set_board(2, 2, pops={("SMALL", 2): pop_at(t, wt(6, 7) + 0.05)})
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    pose(GUS, loc=(-0.25, 2.2, 0), rz=-30, head=(6 + 4 * acc, 0, 14), armR=(-60, 0, -25), elbowR=-20, mouth=m, lid=lid, look=(0.6, 0.0))
    pm, plid = talk("PIP", t)
    pose(PIP, loc=(1.6, 1.95, 0), rz=10, head=(4, 0, 18), mouth=pm, lid=plid, look=(-0.6, 0.2))
    look(cam, (0.65, -1.6, 1.6), (0.65, 2.9, 1.45), 30)


PILE_C = (1.25, 1.55, 0.0)


def anim_S7(fr):
    """'Is it done yet?' '...This piece is. [sigh] Now glue them all.' A small printer hands Gus one tiny piece; the
    camera drifts down to the mountain of pieces still to glue (sets up the Ep 9 finale). BIG +1 on 'glue'."""
    t = fr / FPS
    for P in SMALLS:
        set_vis(P["g"], True)
        run_printer(P, t, 2.0 if t < LN[8]["t0"] else 0.0, active=t < LN[8]["t0"])
    tg = wt(8, 4)                              # "glue"
    reveal = ease(cl((t - (LN[8]["words"][3]["t0"] - 0.2)) / 0.7))
    temp(pieces_mountain("mtn", PILE_C, 46))
    temp(glue_bottle("glue", (PILE_C[0] - 0.55, PILE_C[1] - 0.25, 0.0)))
    set_board(3 * 0 + 2, 3, pops={("BIG", 2): pop_at(t, tg + 0.1)})
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    take = ease(cl((t - (LN[8]["t0"] - 0.3)) / 0.4))
    pose(GUS, loc=(0.3, 2.15, 0), rz=-10, head=(10 + 4 * acc, 0, 8), mouth=m, lid=lid, look=gus_listen_look(t))
    bpy.context.view_layer.update()
    src = Vector((0.5, 2.85, TABLE_Z + 0.25))
    hold = GUS.neck.matrix_world.translation + Vector((0.18, -0.32, -0.12))
    hp = aim_arm(GUS, "R", src.lerp(hold, take))
    if take > 0.0:
        p = temp(empty("tiny", None, tuple(hp + Vector((0, -0.06, 0.02)))))
        arc_piece("tiny_s", 0.25, 0.03, 0.08, -10, 10, mat("white"), p, loc=(0, 0.25, -0.04))
    pm, plid = talk("PIP", t)
    bounce = 0.03 * abs(math.sin(t * 10)) * win(t, LN[7]["t0"], LN[7]["t1"], 0.05, 0.1)
    pose(PIP, loc=(1.05, 2.0, bounce), rz=20, head=(-4, 0, 20), armL=(-40, 0, 10), armR=(-40, 0, -10), mouth=pm, lid=plid,
         look=(-0.7, 0.4))
    a = (Vector((0.75, -1.4, 1.65)), Vector((0.6, 2.6, 1.45)))
    b = (Vector((0.85, -1.2, 1.5)), Vector((0.9, 1.9, 0.7)))
    look(cam, a[0].lerp(b[0], reveal), a[1].lerp(b[1], reveal), 30)


def anim_S8(fr):
    """'So who wins?' (board flickers 3-3) 'Depends on the part. We run both.': Gus nudges the big bumper skin toward the
    big printer and the small detailed bits toward the small ones."""
    t = fr / FPS
    set_vis(SMALLS[1]["g"], True); set_vis(SMALLS[2]["g"], True)
    for i, P in enumerate([BIG] + SMALLS):
        run_printer(P, t + i, 0.4 if i == 0 else 2.0)
    fl = win(t, LN[9]["t0"], LN[9]["t1"] + 0.3, 0.05, 0.1)
    set_board(3, 3, flick=(t * 1.0 if fl > 0.5 else 0.0))
    nud = ease(cl((t - wt(10, 1)) / 0.6))       # from "on the part"
    bumper("bb", 3, (lerp(-0.6, -1.5, nud), 1.25, 0.0), R=0.55)
    temp(pieces_mountain("bits", (lerp(0.2, 1.15, nud), 1.35, 0.0), 10, rng_seed=4))
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    both = win(t, wt(10, 4), LN[10]["t1"] + 0.5, 0.15, 0.3)
    pose(GUS, loc=(-0.25, 1.9, 0), rz=0, head=(4 + 5 * acc, 0, lerp(-15, 15, nud) * (1 - both)),
         armL=lerpv((-15, 0, 8), (-60, 0, 60), max(nud * (1 - both), both)), armR=lerpv((-15, 0, -8), (-60, 0, -60), max(nud * (1 - both), both)),
         mouth=m, lid=lid, look=gus_listen_look(t))
    pm, plid = talk("PIP", t)
    pose(PIP, loc=(0.55, 1.6, 0), rz=-20, head=(-8, 0, -15), armL=(-20, 0, 8), mouth=pm, lid=plid,
         look=(-0.4, 0.9) if t < LN[9]["t1"] + 0.3 else (-0.7, 0.3))
    look(cam, (-0.2, -2.2, 1.45), (-0.15, 1.9, 1.0), 28)


# phone hand-off (pilot S10-S12 logic, moved to this shop): Pip perks up on "Wait.", pulls out the phone, then holds it
# up to Gus; S10 pushes into the screen until it fills the frame (screen = key colour, corner-pinned with real footage)
PIP_PH = Vector((0.55, 0.9, 0.0))
PHONE_N = (0.28, -1.0, 0.12)
S10_LENS, S10_D0 = 35.0, 1.6
S10_DEND = (PHONE_H / 2) * S10_LENS / 18.0


def phone_pose():
    pose(PIP, loc=tuple(PIP_PH), rz=14, hips=(-6, 0, 0), head=(-12, 0, -16), armR=(-10, 0, -10), mouth=0.0, lid=0.0, look=(0.6, 0.6))
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


def anim_S9(fr):
    """'Wait. Illumaesthetic's big one is HUGE.': Pip perks up on 'Wait.', pulls out his phone (back to camera) and
    beams at it; Gus looks over."""
    t = fr / FPS
    L = LN[11]
    tw = L["words"][0]["t0"]
    perk = eback((t - tw + 0.04) / 0.16)
    hop = 0.05 * math.sin(math.pi * cl((t - tw) / 0.25))
    reach = ease((t - tw - 0.3) / 0.4)
    m, lid = talk("PIP", t, 0.0)
    acc = accent("PIP", t)
    pose(PIP, loc=tuple(PIP_PH + Vector((0, 0, hop))), rz=-4, hips=(lerp(6, -4, cl(perk)), 0, 0),
         head=(lerp(8, -6, cl(perk)) + 5 * acc, 0, lerp(-4, 6, cl(perk))),
         armL=lerpv((4, 0, 6), (-62, 0, -8), reach), elbowL=lerp(-10, -80, reach), armR=(4, 0, -6), mouth=m, lid=lid,
         look=lerpv((0, 0), (0.5, 0.7), cl(perk)))
    pose(GUS, loc=tuple(PIP_PH + Vector((-1.5, 0.8, 0))), rz=30, look=(0.8, -0.2))
    if reach > 0.01:
        bpy.context.view_layer.update()
        rest = PIP.hands["L"].matrix_world.translation.copy()
        chest = PIP.neck.matrix_world.translation + Vector((0.12, -0.3, -0.08))
        hp = aim_arm(PIP, "L", rest.lerp(chest, reach))
        set_vis(PHONE, True)
        n = Vector(lerpv((0.0, 0.3, -1.0), (0.15, 0.8, 0.55), reach)).normalized()
        orient_phone(PHONE, hp + Vector((0.0, -0.03, lerp(-0.12, 0.13, reach))), n, up=lerpv((0, 1, 0), (0, 0, 1), reach))
    look(cam, tuple(PIP_PH + Vector((0.05, -1.6, 0.98))), tuple(PIP_PH + Vector((0.0, 0.0, 0.86))), 42)


def s10_cam(c, n, u, k):
    ke = k ** 1.4
    d = S10_D0 * (S10_DEND / S10_D0) ** ke
    look(cam, c + n * d, c, S10_LENS, up=u)


def anim_S10(fr):
    """'...Show-off.': Pip holds the phone up to Gus, screen to camera; Gus leans in from the side, deadpan; the camera
    pushes along the screen normal until the screen fills the frame on the last frame."""
    t, k = fr / FPS, prog(fr, "S10")
    c, n, u, r = phone_pose()
    pm, plid = talk("PIP", t, 0.0)
    PIP.neck.rotation_euler = [math.radians(a) for a in (-12, 0, -16 + 3 * math.sin(t * 4))]
    set_face(PIP, pm, plid, (0.9, 0.7), (0.04, -12))
    f = -Vector((r.x, r.y, 0)).normalized()
    rz = math.degrees(math.atan2(f.x, -f.y))
    lean = eout((t - SF["S10"][0] / FPS) / 0.4)
    hx = lerp(14, 32, lean)
    m, lid = talk("GUS", t, 0.0)
    pose(GUS, loc=(0, 0, 0), rz=rz, hips=(hx, 0, 0), head=(-0.85 * hx, 0, 0), armL=(hx, 0, 8), armR=(hx, 0, -8), elbowL=-10,
         elbowR=-10, mouth=m, lid=lid, look=(0, -0.2))
    want = c - n * 0.06 + r * lerp(0.62, 0.47, lean)
    bpy.context.view_layer.update()
    hc = GUS.neck.matrix_world @ Vector((0, 0, GUS.head_c))
    GUS.root.location += Vector((want.x - hc.x, want.y - hc.y, min(0.0, (c.z + 0.12) - hc.z)))
    s10_cam(c, n, u, k)


ANIM = {k: globals()[f"anim_{k}"] for k in SF}


def reset_anim():
    reset()


# ----------------------------------------------------------------------------------------------------------------- run
CORN = os.path.join(OUT, "screen_corners.json")
corners = json.load(open(CORN)) if os.path.exists(CORN) else dict(
    doc="Ep 7 phone-screen corners (S10 push) for corner-pinning the real big-printer footage. Pixels in the 1080x1920 frame, "
        "origin top-left, x right, y down. Corner order tl, tr, br, bl = the footage's upright corners. Cartoon frames at 30 fps. "
        "The screen renders as flat key colour #ff00ff (camera rays only); use it as the matte.",
    width=1080, height=1920, fps=FPS, screen_aspect="9:16", key_colour=KEY, corner_order=["tl", "tr", "br", "bl"], shots={})
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
        need_c = sh == "S10" and not STILLS
        todo = ((fr - f0) % EVERY == 0 and not os.path.exists(final) and (not ONLY or fr in ONLY)) or STILLS
        if not (todo or need_c):
            continue
        CUR_T = fr / FPS
        reset_anim()
        ANIM[sh](fr)
        bpy.context.view_layer.update()
        if need_c:
            per[str(fr)] = screen_corners_px()
        if not todo:
            continue
        scn.render.filepath = final[:-4] + "_tmp"
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        os.replace(final[:-4] + "_tmp.png", final)
        tsum += time.time() - t0
        nr += 1
        print(f"[ep7] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if per:
        corners["shots"][sh] = dict(frames=[f0, f1], static=False, per_frame=per,
                                    note=f"push along the screen normal, lens {S10_LENS} mm, {S10_D0} m -> {S10_DEND:.4f} m; last frame {f1 - 1} = full frame")
        corners["screen_full_frame"] = TL["screen_full_frame"]
        json.dump(corners, open(CORN, "w"), indent=1)
    if nr:
        print(f"[ep7] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
