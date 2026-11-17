"""Pip & Gus Ep 9 (glue, finale): cartoon shots, run INSIDE the pilot scene (its shop, characters, phone, clock, render setup).

  cd projects/scan-tedium-explainer-reel/tools
  blender -b --factory-startup -P partA_scene.py -- --out OUT --exec ../../pip-gus-ep9-glue/tools/ep9_scene.py \
          [--ep9 stills|anim] [--ep9shots E1,E2] [--scale 0.5] [--spp 8] [--range a:b] [--every N]

Every shot is a function of reel time t (seconds = time in the approved voice take, voice_lines.json), so the same code
renders the lookdev stills (one t per shot) and the animation (every frame). Frames are posed procedurally, written via a
_tmp file and renamed, and skipped when they exist (resumable). Persistent data stays off (lessons).

Rules kept: no brands, no numbers, no text in 3D except the approved cartoon "ASA / ABS" stamp; dot eyes only; no arms.
"""
import json as _json

EP9 = os.path.dirname(os.path.abspath(arg("--exec", "")))
EPROOT = os.path.dirname(EP9)
VL = _json.load(open(os.path.join(EPROOT, "voice_lines.json")))
LINES9 = {L["n"]: L for L in VL["lines"]}
TEX9 = arg("--tex9", "/home/user/media/work/pip-gus-ep9/tex")
MODE9 = arg("--ep9", "stills")
FPS9 = 30

# hide the pilot-only props
for _ob in (SCANNER, ROLL, LAPTOP):
    set_vis(_ob, False)
pip_scanner("pouch")

WHITE_PRINT = "#e9eae6"
GLOW = "#f2a04a"


# ----------------------------------------------------------------------------------------------------------------- helpers
def cl9(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sm(x):
    x = cl9(x)
    return x * x * (3 - 2 * x)


def seg(t, a, b):
    """0..1 progress of t through [a, b] (smoothstep)."""
    return sm((t - a) / max(1e-6, b - a))


def lerp(a, b, k):
    return a + (b - a) * k


def lerpv(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def talk(who, t):
    """Talk energy 0..1 from the measured word times: a syllable-ish bump every ~0.17 s inside each word."""
    e = 0.0
    for L in VL["lines"]:
        if L["who"] != who or not (L["t0"] - 0.1 <= t <= L["t1"] + 0.1):
            continue
        for w in L["words"]:
            a, b = w["t0"] - 0.033, w["t1"]          # lead the sound by one frame
            if a <= t <= b:
                n = max(1, round((b - a) / 0.17))
                ph = (t - a) / (b - a) * n
                e = max(e, 0.35 + 0.65 * math.sin(math.pi * (ph % 1.0)))
    return e


def blink(t, seed):
    """Blink lid 0..1: a 4-frame blink every 2.4-3.6 s (deterministic per character)."""
    rng = random.Random(seed)
    s = rng.uniform(0.5, 1.5)
    while s < t + 1:
        if 0 <= t - s < 0.13:
            return math.sin(math.pi * (t - s) / 0.13)
        s += rng.uniform(2.4, 3.6)
    return 0.0


def face(ch, expr, lid=0.0):
    """Eye-shape expression (design.md option B): neutral, annoyed (flat D-cut), excited (^ ^), surprised (1.3 pop),
    curious (1.15), squint (lines), skeptical (one cut + one round)."""
    if expr == "excited":
        set_eyes(ch, 0, 0, shape="arc", scale=1.1)
    elif expr == "squint":
        set_eyes(ch, 0, 0, shape="line", scale=1.1)
    elif expr == "surprised":
        set_eyes(ch, lid, lid, scale=1.3)
    elif expr == "curious":
        set_eyes(ch, lid, lid, scale=1.15)
    elif expr == "annoyed":
        set_eyes(ch, max(0.45, lid), max(0.45, lid), scale=1.1)
    elif expr == "skeptical":
        set_eyes(ch, 0.5, lid, scale=1.1)
    else:
        set_eyes(ch, lid, lid)


def P(ch, who, t, expr="neutral", seed=1, **kw):
    """pose() + talk energy + blink + expression."""
    lid = blink(t, seed)
    pose(ch, mouth=talk(who, t), lid=lid, **kw)
    face(ch, expr, lid)


def mark(ob, k=True):
    set_vis(ob, k)
    return ob


# ----------------------------------------------------------------------------------------------------------------- props
def curved_piece(name, w, h, th, bend, m, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    """A printed bumper piece: a thin slab bent around Z (curvature `bend` rad over its width), bevelled, outlined."""
    bm = bmesh.new()
    nx = 10
    rows = []
    for zi, z in enumerate((-h / 2, h / 2)):
        for side in (-1, 1):
            row = []
            for i in range(nx + 1):
                u = (i / nx - 0.5)
                a = u * bend
                if abs(bend) > 1e-4:
                    R = w / bend
                    x, y = R * math.sin(a), R * (1 - math.cos(a))
                else:
                    x, y = u * w, 0.0
                y += side * th / 2
                row.append(bm.verts.new((x, y, z)))
            rows.append(row)
    lo_f, lo_b, hi_f, hi_b = rows
    for i in range(nx):
        bm.faces.new((lo_f[i], lo_f[i + 1], hi_f[i + 1], hi_f[i]))
        bm.faces.new((lo_b[i + 1], lo_b[i], hi_b[i], hi_b[i + 1]))
        bm.faces.new((lo_b[i], lo_b[i + 1], lo_f[i + 1], lo_f[i]))
        bm.faces.new((hi_f[i], hi_f[i + 1], hi_b[i + 1], hi_b[i]))
    for r0, r1 in ((0, nx),):
        pass
    bm.faces.new((lo_f[0], hi_f[0], hi_b[0], lo_b[0]))
    bm.faces.new((lo_b[nx], hi_b[nx], hi_f[nx], lo_f[nx]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = new_obj(name, bm, [m, OUTLINE], parent, loc, rot)
    return add_mods(ob, 0.004, 0.006)


def build_pile(parent=None, loc=(1.15, 2.05, 0), seed=9, n=26):
    """Pile of printed white bumper pieces (the Ep 8 hand-off: 'Now I've got a pile of pieces')."""
    g = empty("PILE", parent, loc)
    rng = random.Random(seed)
    pieces = []
    for i in range(n):
        rr = 0.42 * math.sqrt(rng.random())
        a = rng.uniform(0, 2 * math.pi)
        hgt = 0.34 * (1 - (rr / 0.45) ** 1.3) * rng.uniform(0.5, 1.0)
        w, h = rng.uniform(0.22, 0.42), rng.uniform(0.12, 0.24)
        p = curved_piece(f"pile{i}", w, h, 0.03, rng.uniform(0.2, 0.9), mat(WHITE_PRINT), g,
                         (rr * math.cos(a), rr * math.sin(a), 0.03 + hgt),
                         (rng.uniform(-70, 70), rng.uniform(-60, 60), rng.uniform(0, 360)))
        pieces.append(p)
    return g, pieces


def build_glue_bottle(parent=None):
    g = empty("CA_BOTTLE", parent)
    cyl("ca_body", 0.03, 0.09, (0, 0, 0.045), mat("white"), g, bevel=0.01, ol=0.006)
    cyl("ca_cap", 0.018, 0.03, (0, 0, 0.105), mat("sage"), g, bevel=0.004, ol=0.005)
    cyl("ca_nozzle", 0.008, 0.035, (0, 0, 0.135), mat("sage"), g, r2=0.003, ol=0.004)
    return g


def build_mold_box(parent=None, loc=(2.9, 3.05, 0.955)):
    """Open mold box (a master gets dropped in to make a mold)."""
    g = empty("MOLDBOX", parent, loc)
    L, W, H, T = 0.5, 0.36, 0.2, 0.03
    box("mb_floor", (L, W, T), (0, 0, T / 2), mat("metal"), g, bevel=0.006, ol=0.01)
    for nm, sz, lc in (("n", (L, T, H), (0, W / 2, H / 2)), ("s", (L, T, H), (0, -W / 2, H / 2)),
                       ("e", (T, W, H), (L / 2, 0, H / 2)), ("w", (T, W, H), (-L / 2, 0, H / 2))):
        box(f"mb_{nm}", sz, lc, mat("sage"), g, bevel=0.006, ol=0.01)
    return g


def build_epoxy(parent=None, loc=(3.6, 2.95, 0.955)):
    """Mixing card with two blobs (resin + hardener) and a stir stick; no labels."""
    g = empty("EPOXY", parent, loc)
    box("ep_card", (0.3, 0.22, 0.006), (0, 0, 0.003), mat("white"), g, ol=0.006)
    blobs = []
    for i, (x, key) in enumerate(((-0.06, "#d9b25a"), (0.06, "#e3e5e1"))):
        b = blob(f"ep_blob{i}", (0.05, 0.045, 0.022), (x, 0, 0.012), mat(key), g, ol=0.006, seg=24, rings=12, half=True)
        blobs.append(b)
    stick = box("ep_stick", (0.02, 0.2, 0.006), (0, -0.05, 0.03), mat("wood"), g, bevel=0.003, ol=0.004, rot=(0, 0, 25))
    return g, blobs, stick


def build_hot_stapler(parent=None):
    """Hot stapler: dark body, sage grip, two glowing prongs (staple held in the tip)."""
    g = empty("HSTAPLER", parent)
    box("hs_body", (0.07, 0.22, 0.08), (0, -0.06, 0.0), mat("dark"), g, bevel=0.02, ol=0.008)
    box("hs_grip", (0.05, 0.06, 0.15), (0, 0.04, -0.1), mat("sage"), g, bevel=0.015, ol=0.008, rot=(-15, 0, 0))
    box("hs_neck", (0.04, 0.06, 0.04), (0, -0.19, -0.01), mat("metal"), g, bevel=0.008, ol=0.006)
    glow = []
    for s in (-1, 1):
        glow.append(box(f"hs_prong{s}", (0.008, 0.012, 0.04), (s * 0.014, -0.215, -0.035), emit(GLOW, 1.6), g, ol=0.004))
    return g, glow


def build_office_stapler(parent=None):
    g = empty("OSTAPLER", parent)
    box("os_base", (0.06, 0.24, 0.025), (0, 0, 0.0125), mat("dark"), g, bevel=0.008, ol=0.006)
    box("os_top", (0.055, 0.23, 0.035), (0, -0.005, 0.05), mat("red"), g, bevel=0.012, ol=0.006, rot=(-6, 0, 0))
    return g


def build_thought(parent=None, loc=(0, 0, 0), r=0.26):
    """Thought bubble: white puff cloud + two trailing puffs, holds an office stapler."""
    g = empty("THOUGHT", parent, loc)
    rng = random.Random(4)
    for i in range(9):
        a = 2 * math.pi * i / 9
        blob(f"th_puff{i}", (r * 0.42, r * 0.3, r * 0.42), (r * 0.78 * math.cos(a), 0, r * 0.62 * math.sin(a)), mat("white"), g,
             ol=0.008, seg=20, rings=10)
    blob("th_core", (r * 0.95, r * 0.25, r * 0.75), (0, 0.02, 0), mat("white"), g, seg=24, rings=12)
    blob("th_t1", (0.05, 0.04, 0.05), (-r * 0.8, 0, -r * 1.05), mat("white"), g, ol=0.006, seg=16, rings=8)
    blob("th_t2", (0.03, 0.025, 0.03), (-r * 1.05, 0, -r * 1.4), mat("white"), g, ol=0.005, seg=12, rings=6)
    st = build_office_stapler(g)
    st.location = (0, -0.2, -0.05)
    st.rotation_euler = (math.radians(70), 0, math.radians(90))
    return g


def build_weld_pen(parent=None):
    g = empty("WELDPEN", parent)
    cyl("wp_body", 0.022, 0.2, (0, 0, 0), mat("dark"), g, axis="Y", bevel=0.006, ol=0.006)
    cyl("wp_grip", 0.025, 0.07, (0, 0.04, 0), mat("sage"), g, axis="Y", bevel=0.006, ol=0.006)
    cyl("wp_tip", 0.014, 0.05, (0, -0.125, 0), mat("metal"), g, axis="Y", r2=0.004, ol=0.004)
    tip = cyl("wp_glow", 0.006, 0.012, (0, -0.155, 0), emit(GLOW, 1.8), g, axis="Y")
    return g, tip


def build_acetone(parent=None, loc=(4.25, 3.1, 0.955)):
    g = empty("ACETONE", parent, loc)
    cyl("ac_jar", 0.05, 0.1, (0, 0, 0.05), mat("#c9dcd0", 0.55), g, bevel=0.01, ol=0.006)
    cyl("ac_liq", 0.046, 0.06, (0, 0, 0.032), mat("#b9d6c4", 0.6), g)
    cyl("ac_lid", 0.053, 0.02, (0.11, 0.0, 0.01), mat("sage"), g, bevel=0.005, ol=0.005)
    return g


def build_brush(parent=None):
    g = empty("BRUSH", parent)
    cyl("br_handle", 0.01, 0.16, (0, 0, 0.08), mat("wood"), g, ol=0.004)
    cyl("br_ferrule", 0.012, 0.03, (0, 0, 0.17), mat("metal"), g, ol=0.004)
    cyl("br_tip", 0.012, 0.04, (0, 0, 0.205), mat("#e6dcc4"), g, r2=0.002, ol=0.004)
    return g


def build_shelf(parent=None, loc=(5.45, 3.48, 1.55)):
    """The running gag: the failed-print shelf, fuller every episode (spaghetti nest, a flopped paper-thin print, a cracked
    piece). Snapped superglue pieces land on it in E3."""
    g = empty("SHELF", parent, loc)
    box("sh_board", (1.1, 0.3, 0.035), (0, -0.15, 0), mat("wood"), g, bevel=0.008, ol=0.012)
    for x in (-0.45, 0.45):
        box(f"sh_brk{x}", (0.03, 0.22, 0.12), (x, -0.11, -0.07), mat("dark"), g, ol=0.008)
    rng = random.Random(3)
    for i in range(14):   # spaghetti nest: tangled thin loops
        a = rng.uniform(0, math.pi)
        torus(f"sh_spag{i}", rng.uniform(0.04, 0.08), 0.004, (-0.3 + rng.uniform(-0.06, 0.06), -0.15 + rng.uniform(-0.05, 0.05),
              0.06 + rng.uniform(0, 0.06)), mat("#8a8f8a"), g, rot=(math.degrees(a), rng.uniform(0, 90), rng.uniform(0, 90)))
    curved_piece("sh_flop", 0.3, 0.16, 0.006, 1.6, mat(WHITE_PRINT, 0.9), g, (0.05, -0.13, 0.1), (70, 0, 10))
    curved_piece("sh_crack", 0.22, 0.12, 0.025, 0.5, mat(WHITE_PRINT), g, (0.33, -0.15, 0.08), (15, 20, -30))
    return g


def build_board(parent=None, loc=(1.32, 3.56, 1.82)):
    """Tier board (icons only): one row per method -> method icon | rating icon | 'what it's for' icon. Rows appear as
    Gus covers them (vis set per shot)."""
    g = empty("BOARD", parent, loc)
    box("bd_frame", (1.04, 0.04, 1.08), (0, 0, 0), mat("dark"), g, bevel=0.01, ol=0.012)
    box("bd_face", (0.96, 0.02, 1.0), (0, -0.022, 0), mat("white"), g)
    rows = {}
    ys = -0.035
    for i, key in enumerate(("ca", "epoxy", "staple", "weld")):
        z = 0.36 - i * 0.24
        r = empty(f"bd_row_{key}", g, (0, ys, z))
        box(f"bd_line{i}", (0.9, 0.004, 0.006), (0, 0, -0.11), mat("#c7c9c6"), r)
        rows[key] = r
    # method icons (col x = -0.32)
    ca = rows["ca"]
    cyl("bdi_ca", 0.035, 0.1, (-0.32, 0, -0.02), mat("white"), ca, axis="Z", ol=0.005)
    cyl("bdi_ca_c", 0.02, 0.04, (-0.32, 0, 0.05), mat("sage"), ca, ol=0.004)
    ep = rows["epoxy"]
    for x, k in ((-0.36, "#d9b25a"), (-0.28, "#cfd1cd")):
        blob(f"bdi_ep{x}", (0.04, 0.012, 0.035), (x, 0, 0), mat(k), ep, ol=0.005, seg=16, rings=8)
    stp = rows["staple"]
    box("bdi_st", (0.14, 0.012, 0.03), (-0.32, 0, 0.025), mat("dark"), stp, ol=0.004)
    for s in (-1, 1):
        box(f"bdi_stp{s}", (0.012, 0.012, 0.05), (-0.32 + s * 0.04, 0, -0.02), emit(GLOW, 1.4), stp, ol=0.003)
    wd = rows["weld"]
    box("bdi_wd", (0.16, 0.012, 0.03), (-0.32, 0, 0), mat("dark"), wd, ol=0.004, rot=(0, -25, 0))
    box("bdi_wdt", (0.03, 0.012, 0.02), (-0.4, 0, -0.04), emit(GLOW, 1.4), wd, rot=(0, -25, 0))
    # rating icons (col x = 0.0): dot-eye faces
    def face_icon(r, kind, x=0.0):
        cyl(f"{r.name}_fc", 0.07, 0.01, (x, 0, 0), mat("vinyl"), r, axis="Y", ol=0.005)
        for s in (-1, 1):
            if kind == "squint":
                box(f"{r.name}_e{s}", (0.03, 0.006, 0.008), (x + s * 0.025, -0.008, 0.01), mat("black"), r)
            elif kind == "happy":
                torus(f"{r.name}_e{s}", 0.013, 0.004, (x + s * 0.025, -0.008, 0.0), mat("black"), r, rot=(90, 0, 0),
                      scale=(1, 1, 1))
            else:
                cyl(f"{r.name}_e{s}", 0.008, 0.006, (x + s * 0.025, -0.008, 0.01), mat("black"), r, axis="Y")
    face_icon(rows["ca"], "squint")
    face_icon(rows["epoxy"], "happy")
    face_icon(rows["staple"], "happy")
    face_icon(rows["weld"], "happy")
    # small clock next to epoxy's face (slow)
    cyl("bdi_clk", 0.035, 0.01, (0.1, 0, 0), mat("white"), rows["epoxy"], axis="Y", ol=0.004)
    box("bdi_clkh", (0.006, 0.004, 0.03), (0.1, -0.008, 0.012), mat("black"), rows["epoxy"])
    # use icons (col x = 0.3): mold box for superglue, a little bumper for staples + weld
    box("bdi_mold", (0.12, 0.012, 0.07), (0.3, 0, -0.01), mat("sage"), rows["ca"], ol=0.004)
    box("bdi_moldi", (0.09, 0.008, 0.05), (0.3, -0.006, 0.0), mat("metal"), rows["ca"])
    for key in ("staple", "weld"):
        curved_piece(f"bdi_bump_{key}", 0.16, 0.05, 0.012, 1.2, mat(WHITE_PRINT), rows[key], (0.3, 0, 0), (90, 0, 180))
    return g, rows


def build_stamp(parent=None):
    """Approved cartoon-only label: 'ASA / ABS' stamp mark (texture from tools/stamp_tex.py)."""
    g = empty("STAMP", parent)
    bm = bmesh.new()
    w, h = 0.36, 0.168
    vs = [bm.verts.new(c) for c in ((-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2))]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new()
    for lp, c in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        lp[uv].uv = c
    new_obj("stamp_face", bm, [tex_emit(os.path.join(TEX9, "stamp_asa_abs.png"))], g)
    return g


def build_bumper_on_car(parent):
    """Finale: the glued printed bumper on Pip's car: white shell over the front, filled seams still faintly visible,
    lower intake, a couple of staple glints underneath (no claim about paint)."""
    g = empty("NEWBUMPER", parent, (2.05, 0, 0.5))
    box("nb_shell", (0.16, 1.78, 0.34), (0, 0, 0), mat(WHITE_PRINT), g, bevel=0.06, ol=0.022)
    box("nb_intake", (0.03, 0.8, 0.1), (0.075, 0, -0.06), mat("black"), g, bevel=0.02)
    for y in (-0.62, -0.2, 0.22, 0.6):
        box(f"nb_seam{y}", (0.02, 0.006, 0.3), (0.075, y, 0), mat("#c8cac5"), g)
    for s in (-1, 1):
        box(f"nb_lip{s}", (0.2, 0.5, 0.03), (0.04, s * 0.55, -0.17), mat(WHITE_PRINT), g, bevel=0.01, ol=0.012)
    return g


# build -- layout: the glue table stands free on the floor right of Pip's car (car spans x -2..2), Gus works behind it
# facing the camera; board + failed-print shelf on the back wall behind; pile of pieces on the floor left of the table.
TX, TY, TZ = 4.0, 1.6, 0.66         # table centre (top height)


def build_table(loc=(TX, TY, 0)):
    g = empty("GTABLE", SHOP, loc)
    box("gt_top", (1.7, 0.8, 0.06), (0, 0, TZ - 0.03), mat("wood"), g, bevel=0.015, ol=0.02)
    for x in (-0.78, 0.78):
        for y in (-0.33, 0.33):
            box(f"gt_leg{x}{y}", (0.06, 0.06, TZ - 0.06), (x, y, (TZ - 0.06) / 2), mat("dark"), g, ol=0.012)
    return g


GTABLE = build_table()
PILE, PILE_PIECES = build_pile(loc=(2.75, 1.85, 0))
BOTTLE = build_glue_bottle()
MOLDBOX = build_mold_box(SHOP, loc=(TX + 0.55, TY + 0.05, TZ))
EPOXY, EP_BLOBS, EP_STICK = build_epoxy(SHOP, loc=(TX - 0.5, TY - 0.12, TZ))
HSTAPLER, HS_GLOW = build_hot_stapler()
THOUGHT = build_thought()
WELDPEN, WP_TIP = build_weld_pen()
WELDPEN.scale = (1.6, 1.6, 1.6)
BRUSH_SCALE = 1.6
ACETONE = build_acetone(SHOP, loc=(TX + 0.45, TY + 0.25, TZ))
BRUSH = build_brush()
BRUSH.scale = (1.6, 1.6, 1.6)
SHELF = build_shelf(SHOP, loc=(6.55, 3.48, 1.5))
BOARD, ROWS = build_board(SHOP, loc=(5.4, 3.56, 1.8))
STAMP = build_stamp(BOARD)
STAMP.location = (0.0, -0.05, -0.42)
STAMP.rotation_euler = (0, math.radians(-8), 0)
NEWBUMPER = build_bumper_on_car(CAR)
# seam workpiece lying flat on the table: two printed halves meeting at a seam along y (x = TX)
WORK = empty("WORK", SHOP, (TX, TY - 0.08, TZ))
WORK_L = curved_piece("work_l", 0.34, 0.26, 0.035, 0.3, mat(WHITE_PRINT), WORK, (-0.172, 0, 0.03), (90, 0, 0))
WORK_R = curved_piece("work_r", 0.34, 0.26, 0.035, 0.3, mat(WHITE_PRINT), WORK, (0.172, 0, 0.03), (90, 0, 0))
SEAM_FILL = box("work_seamfill", (0.026, 0.26, 0.012), (0, 0, 0.052), mat("#d9b25a"), WORK)   # bead, grows along y
STAPLES = [box(f"work_staple{i}", (0.07, 0.012, 0.006), (0, -0.08 + i * 0.08, 0.055), emit(GLOW, 1.4), WORK, ol=0.003)
           for i in range(3)]
# a glued test part on the floor for Pip to hop on (E3); its two halves split when it snaps
TEST = empty("TESTPART", SHOP, (5.35, 1.55, 0))
TEST_L = curved_piece("test_l", 0.3, 0.22, 0.04, 0.2, mat(WHITE_PRINT), TEST, (-0.15, 0, 0.13), (0, 0, 0))
TEST_R = curved_piece("test_r", 0.3, 0.22, 0.04, 0.2, mat(WHITE_PRINT), TEST, (0.15, 0, 0.13), (0, 0, 0))


def reset9():
    reset()
    for ob in (BOTTLE, HSTAPLER, THOUGHT, WELDPEN, BRUSH, NEWBUMPER, STAMP):
        set_vis(ob, False)
    for r in ROWS.values():
        set_vis(r, False)
    set_vis(PILE, True)
    set_vis(TEST, True)
    set_vis(SEAM_FILL, False)
    for st in STAPLES:
        set_vis(st, False)
    for ob in (BOTTLE, HSTAPLER, WELDPEN, BRUSH, THOUGHT):
        ob.parent = None
    TEST_L.location, TEST_L.rotation_euler = (-0.15, 0, 0.13), (0, 0, 0)
    TEST_R.location, TEST_R.rotation_euler = (0.15, 0, 0.13), (0, 0, 0)
    SEAM_FILL.scale = (1, 1, 1)
    WORK.location = (TX, TY - 0.08, TZ)
    pip_scanner("pouch")


def board_rows(*keys):
    for k, r in ROWS.items():
        set_vis(r, k in keys)


SEAM = Vector((TX, TY - 0.08, TZ + 0.06))


def gus_at_table(t, expr="neutral", head=(8, 0, 0), tool=None, target=None, trot=(0, 0, 0), tloc=(0, 0, 0), **kw):
    """Gus behind the table, facing the camera, leaning over the workpiece; the right hand aims at `target` (default the
    seam) holding `tool`, the left hand steadies the piece."""
    P(GUS, "GUS", t, expr, seed=5, loc=(TX, TY + 0.6, 0), rz=0, hips=(6, 0, 0), head=head, look=(0, -0.8), **kw)
    aim_arm(GUS, "L", SEAM + Vector((-0.28, 0.05, 0.0)))
    aim_arm(GUS, "R", Vector(target) if target is not None else SEAM + Vector((0.02, 0, 0.12)))
    if tool is not None:
        set_vis(tool, True)
        attach(tool, GUS.hands["R"], tloc, trot)


# ----------------------------------------------------------------------------------------------------------------- shots
# Reel time = take time for Part A (0 .. 37.96 s); the finale tag plays the take's 37.97 .. 41.6 s after Part B.
L = LINES9


def shot_E1(t):
    """'Now I've got a pile of pieces. How do we stick them together?' Pip sits on top of the pile, two pieces held up;
    Gus behind the glue table turns to him. Pip's car (no bumper yet) at the left edge."""
    k = seg(t, 0.0, 1.2)
    P(PIP, "PIP", t, "curious", seed=2, loc=(2.75, 1.85, 0.3), rz=-15, hips=(-8, 0, 0), head=(-10, 0, 0),
      armL=(-120, 0, -15), armR=(-120, 0, 15), elbowL=-20, elbowR=-20, look=(0.3, 0.4))
    P(GUS, "GUS", t, "neutral", seed=5, loc=(TX + 0.2, TY + 0.62, 0), rz=lerp(0, 40, k), head=(4, 0, -10), look=(-0.6, -0.2))
    look(cam, (3.4, -1.15, 1.15), (3.45, 1.9, 0.72), 30)


def shot_E2(t):
    """'Superglue. Fast. Perfect for mold masters.' Gus dabs glue on the seam; the joined master drops into the mold box."""
    # dab on 'Superglue', joined master lifted and dropped into the mold box on 'mold masters'
    drop = seg(t, 6.9, 7.8)
    gus_at_table(t, tool=BOTTLE if drop < 0.05 else None, tloc=(0, -0.03, -0.05), trot=(180, 0, 0))
    WORK.location = (lerp(TX, TX + 0.55, drop), lerp(TY - 0.08, TY + 0.05, drop), TZ + 0.35 * math.sin(math.pi * drop) + 0.02 * drop)
    P(PIP, "PIP", t, "curious", seed=2, loc=(TX - 1.05, TY + 0.2, 0), rz=-50, head=(-6, 0, 10), look=(0.6, 0.2))
    look(cam, (TX + 0.1, TY - 1.55, 1.25), (TX + 0.05, TY + 0.3, 0.85), 30)


def shot_E3(t):
    """'Strong enough to hang on?' / '...Not that.' Pip hops up onto a glued test part; it snaps; Gus deadpan."""
    t_snap = L[4]["t0"] - 0.05
    snap = seg(t, t_snap - 0.1, t_snap + 0.15)
    hop = math.sin(math.pi * seg(t, L[3]["t1"] - 0.2, t_snap)) * 0.25
    P(PIP, "PIP", t, "surprised" if snap > 0.3 else "excited", seed=2,
      loc=(5.35, 1.55, lerp(0.17 + hop, 0.0, snap)), rz=-10, armL=(-150, 0, -20), armR=(-150, 0, 20))
    TEST_L.rotation_euler = (0, math.radians(-25 * snap), 0)
    TEST_R.rotation_euler = (0, math.radians(25 * snap), 0)
    TEST_L.location = (-0.15 - 0.12 * snap, 0, 0.13 - 0.04 * snap)
    TEST_R.location = (0.15 + 0.12 * snap, 0, 0.13 - 0.04 * snap)
    P(GUS, "GUS", t, "annoyed", seed=5, loc=(TX + 0.4, TY + 0.62, 0), rz=-30, head=(6, 0, 0), look=(0.6, -0.2))
    look(cam, (5.0, -1.2, 1.25), (5.25, 2.3, 0.9), 30)


def shot_E4(t):
    """'Epoxy. Fills gaps.' Close on the table: blobs on the mixing card, the seam fills with the bead."""
    gus_at_table(t, tool=None, target=SEAM + Vector((-0.45, -0.05, 0.1)))
    set_vis(SEAM_FILL, True)
    SEAM_FILL.scale = (1, max(0.02, seg(t, L[5]["t0"] + 0.5, L[5]["t1"] + 0.3)), 1)
    EP_STICK.location = (0.0 + 0.03 * math.sin(t * 12), -0.05 + 0.03 * math.cos(t * 12), 0.03)
    look(cam, (TX + 0.35, TY - 0.85, 1.15), (TX - 0.32, TY + 0.0, 0.7), 30)


def shot_E5(t):
    """'Is it done yet?' / '...No.' Pip slumped on the stool under the spinning wall clock (pilot S8 framing)."""
    set_vis(STOOL, True)
    P(PIP, "PIP", t, "annoyed", seed=2, loc=(-3.7, 2.7, 0.61), rz=-15, hips=(10, 0, 0), head=(14, 0, 0), look=(0.3, -0.3))
    P(GUS, "GUS", t, "annoyed", seed=5, loc=(-2.6, 2.3, 0), rz=-40, head=(4, 0, 15), look=(-0.6, 0.2))
    spin = t * 900
    HANDS["minute"].rotation_euler = (0, math.radians(spin), 0)
    HANDS["second"].rotation_euler = (0, math.radians(spin * 6), 0)
    HANDS["hour"].rotation_euler = (0, math.radians(spin / 12), 0)
    for ob in clock_blur(CLOCK, HANDS):
        temp(ob)
    look(cam, (-3.2, -0.6, 1.75), (-3.45, 3.0, 1.6), 30)


def shot_E6(t):
    """'Need it strong? Staples.' Gus raises the hot stapler, prongs glowing; Pip at the table's end."""
    up = seg(t, L[8]["t0"] - 0.3, L[8]["t0"] + 0.3)
    P(GUS, "GUS", t, "neutral", seed=5, loc=(TX, TY + 0.62, 0), rz=0, head=(-4, 0, 0), armL=(-40, 0, 10),
      armR=(lerp(-50, -160, up), 0, -10), elbowR=-15, look=(0.3, 0.3))
    set_vis(HSTAPLER, True)
    attach(HSTAPLER, GUS.hands["R"], (0, 0, 0.05), (90, 0, 0))
    P(PIP, "PIP", t, "curious", seed=2, loc=(TX - 1.05, TY + 0.2, 0), rz=-50, head=(-12, 0, 10), look=(0.6, 0.5))
    look(cam, (TX - 0.4, -1.4, 1.45), (TX - 0.4, TY + 0.3, 1.2), 30)


def shot_E7(t):
    """'Staples?!' Pip, eyes popped; thought bubble with an office stapler."""
    pop = seg(t, L[9]["t0"] - 0.1, L[9]["t0"] + 0.1)
    P(PIP, "PIP", t, "surprised", seed=2, loc=(TX - 1.05, TY + 0.2, 0), rz=-25, head=(-14, 0, 0),
      armL=(-90, 0, -30), armR=(-90, 0, 30), look=(0.0, 0.5))
    set_vis(THOUGHT, True)
    THOUGHT.parent = None
    THOUGHT.location = (TX - 0.7, TY + 0.05, 1.62)
    THOUGHT.rotation_euler = (0, 0, math.radians(-10))
    sc = max(0.01, pop)
    THOUGHT.scale = (sc, sc, sc)
    look(cam, (TX - 1.05, TY - 1.45, 1.2), (TX - 0.95, TY + 0.2, 1.1), 32)


def shot_E8(t):
    """'Hot ones. Melted in across the seam.' Close: glowing staples sink across the seam one by one."""
    k = seg(t, L[10]["t0"], L[10]["t1"])
    yk = -0.08 + 0.08 * min(2, int(k * 3))
    gus_at_table(t, tool=HSTAPLER, target=SEAM + Vector((0, yk, 0.2)), tloc=(0, 0, -0.02), trot=(-90, 0, 0))
    for i, st in enumerate(STAPLES):
        set_vis(st, k > (i + 0.5) / 3)
    look(cam, (TX + 0.6, TY - 0.7, 1.12), (TX, TY + 0.05, 0.72), 32)


def shot_E9(t):
    """'Or weld it. Melt plastic into the seam.' Welding pen runs filament into the seam; the bead grows."""
    k = seg(t, L[11]["t0"] + 0.5, L[11]["t1"])
    gus_at_table(t, tool=WELDPEN, target=SEAM + Vector((0, 0.13 - 0.26 * k, 0.16)), tloc=(0, 0, -0.03), trot=(-60, 0, 0))
    set_vis(SEAM_FILL, True)
    SEAM_FILL.scale = (1, max(0.02, k), 1)
    SEAM_FILL.location = (0, 0.13 * (1 - k), 0.052)
    look(cam, (TX - 0.6, TY - 0.7, 1.12), (TX, TY + 0.05, 0.72), 32)


def shot_E10(t):
    """'ASA or ABS? Acetone welds those. Only those.' Brush wipes the seam; the stamp thumps onto the board behind."""
    gus_at_table(t, head=(4, 0, 0), tool=BRUSH, target=SEAM + Vector((0, 0.1 * math.sin(t * 5), 0.18)), tloc=(0, 0, -0.02),
                 trot=(180, 0, 0))
    board_rows("ca", "epoxy", "staple", "weld")
    set_vis(STAMP, t > L[12]["t1"] - 0.6)
    look(cam, (TX - 0.25, TY - 1.25, 1.3), (TX + 0.6, 2.9, 1.15), 28)


def shot_E11(t):
    """'So which one's best?' / 'Depends what it's for.' Both at the board; Gus nods at it, each method beside its use."""
    board_rows("ca", "epoxy", "staple", "weld")
    set_vis(STAMP, True)
    P(PIP, "PIP", t, "curious", seed=2, loc=(4.7, 2.85, 0), rz=-25, head=(-14, 0, 0), look=(0.5, 0.6))
    P(GUS, "GUS", t, "neutral", seed=5, loc=(6.15, 2.85, 0), rz=30, head=(0, 0, -15), look=(-0.5, 0.2))
    look(cam, (5.4, 0.2, 1.5), (5.4, 3.0, 1.45), 30)


def shot_E12(t):
    """'Wait. Show me you guys doing it!' Phone hand-off: the pilot's S11/S12 phone set-up and push into the screen."""
    c, n, u, r = phone_pose_s11()
    face(PIP, "excited")
    k = seg(t, L[15]["t1"] - 0.45, 37.96)
    s12_cam(c, n, u, k)


def shot_E13(t):
    """Finale tag: the glued printed bumper on Pip's car. 'I printed the bumper I wanted.' / 'You insisted.'"""
    set_vis(NEWBUMPER, True)
    set_vis(PILE, False)
    # presentation shot, straight at the car's new front: Pip one side (thrilled), Gus the other (dry, to camera)
    P(PIP, "PIP", t, "excited", seed=2, loc=(3.15, -1.08, 0), rz=70, head=(-12, 0, 0), armL=(-150, 0, -20),
      armR=(-150, 0, 20), look=(-0.3, 0.6))
    P(GUS, "GUS", t, "annoyed" if t > L[17]["t0"] - 0.2 else "neutral", seed=5, loc=(2.8, 0.6, 0),
      rz=lerp(130, 100, seg(t, L[17]["t0"] - 0.3, L[17]["t0"] + 0.2)), head=(0, 0, 0), look=(0.0, 0.0))
    look(cam, (5.9, -1.35, 1.55), (2.45, 0.05, 0.55), 30)


SHOTS9 = [  # id, t0, t1 (reel/take seconds), still time
    ("E1", 0.0, 4.29, 2.2), ("E2", 4.29, 8.01, 6.2), ("E3", 8.01, 11.42, 10.6), ("E4", 11.42, 13.63, 12.9),
    ("E5", 13.63, 16.13, 14.2), ("E6", 16.13, 18.24, 17.4), ("E7", 18.24, 19.64, 18.8), ("E8", 19.64, 23.19, 22.0),
    ("E9", 23.19, 26.44, 25.4), ("E10", 26.44, 31.55, 31.0), ("E11", 31.55, 35.42, 34.2), ("E12", 35.42, 37.96, 36.4),
    ("E13", 37.96, 41.75, 40.8)]
FUNCS9 = {s: globals()[f"shot_{s}"] for s, *_ in SHOTS9}

if MODE9 == "stills":
    want = arg("--ep9shots", ",".join(s for s, *_ in SHOTS9)).split(",")
    os.makedirs(OUT, exist_ok=True)
    for sid, a, b, ts in SHOTS9:
        if sid not in want:
            continue
        reset9()
        FUNCS9[sid](ts)
        bpy.context.view_layer.update()
        scn.render.filepath = os.path.join(OUT, f"{sid}.png")
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        print(f"[ep9] {sid} t={ts}: {time.time() - t0:.1f} s", flush=True)

if MODE9 == "anim":
    # Take-time frames at 30 fps: 0..1138 = Part A (ends on the phone full-frame), 1139..1252 = finale tag.
    FR = os.path.join(OUT, "frames")
    os.makedirs(FR, exist_ok=True)
    rng_ = arg("--range", "0:1253").split(":")
    f0, f1 = int(rng_[0]), int(rng_[1])
    every = int(arg("--every", "1"))
    t_start = time.time()
    n = 0
    for f in range(f0, f1, every):
        t = f / FPS9
        sid = next(sid for sid, a, b, _ in SHOTS9 if a <= t < b or sid == "E13")
        dst = os.path.join(FR, f"{f:05d}.png")
        if os.path.exists(dst) and not (sid == "E12" and "--corners" in argv):
            continue
        reset9()
        FUNCS9[sid](t)
        bpy.context.view_layer.update()
        tmp = os.path.join(FR, f"_tmp_{f:05d}.png")
        scn.render.filepath = tmp
        bpy.ops.render.render(write_still=True)
        os.replace(tmp, dst)
        if sid == "E12":   # phone-screen corners (px, tl tr br bl) for corner-pinning Part B's first frames into the phone
            cp = os.path.join(OUT, "screen_corners.json")
            cj = _json.load(open(cp)) if os.path.exists(cp) else {}
            cj[str(f)] = screen_corners_px()
            _json.dump(cj, open(cp, "w"), indent=0)
        n += 1
        print(f"[ep9] frame {f} {sid} ({(time.time() - t_start) / n:.1f} s/frame avg)", flush=True)
