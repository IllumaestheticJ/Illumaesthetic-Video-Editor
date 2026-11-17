"""Pip & Gus Ep 8 ("What plastic should I use for car parts?") - cartoon part, Blender 5.3 EEVEE cel look.

Runs INSIDE the pilot's scene builder (characters, shop, car, phone, cel materials, talk + expression system), so the look and
the locked character spec (v7 proportions, no brows, nametags) are shared with the series:

  cd projects/scan-tedium-explainer-reel/tools
  blender -b --factory-startup -P partA_scene.py -- --exec ../../pip-gus-ep7-materials/tools/ep8_anim.py \
      --timeline ../../pip-gus-ep7-materials/ep8_timeline.json --out FRAMES --ep8shots A1,A2 [--every N] [--frames 10,20]
      [--scale 1] [--spp 8]

Every frame is posed procedurally (no keyframes): reset, pose for the frame, render one still. FRAMES/<shot>/<frame>.png is
skipped when it exists (written via _tmp + rename), so renders resume frame by frame. No text, numbers, logos or brands in 3D.
"""
import re as _re

_HERE8 = os.path.dirname(os.path.abspath(arg("--exec", "")))
_PA = os.path.join(os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1])), "partA_anim.py")
_src = open(_PA).read()
_cut = _src.index("# ----------------------------------------------------------------------------------------------------------------- shots")
exec(compile(_src[:_cut], _PA, "exec"), globals())     # easing, talk, blinks, expression system (brows removed)

EP8_SHOTS = arg("--ep8shots", ",".join(s["id"] for s in TL["shots"])).split(",")
LNO = {L["n"]: L for L in TL["lines"]}


def W(n, k):
    """k-th word (0-based, negative from the end) of line n: dict(w, t0, t1)."""
    return LNO[n]["words"][k]


def word_t(n, needle, default=None):
    for w in LNO[n]["words"]:
        if needle.lower() in w["w"].lower():
            return w["t0"]
    return default if default is not None else LNO[n]["t0"]


# ----------------------------------------------------------------------------------------------------------------- palette
PAL.update(pla="#619f73", petg="#c9cfd1", blk="#262826", asa="#55595a", bed="#2f3230", frame_p="#3a3d3a", head_p="#ecefec",
           sky="#a9d6ea", sky_l="#cfe8f2", sunc="#ffd24a", sunray="#ffe48a", dash="#3b3f3c", dash_l="#4a4f4b",
           cloud="#eef1f2", cloud_d="#b9c1c6", rain="#6f9fd8", asphalt="#6b6e6c", grass="#86b07c", mold_in="#2a2c2a")

# ----------------------------------------------------------------------------------------------------------------- props
set_vis(LAPTOP, False)      # the bench now holds the printer
BENCH_Z = 0.955
PR_X, PR_Y = 3.05, 3.12     # printer centre on the bench


def build_printer():
    """Generic open-frame printer (no brand, no screen text): base, bed, gantry, white toolhead, side spool holder, small
    front screen (shows the bumper pieces in A8)."""
    g = empty("PRINTER", None, (PR_X, PR_Y, BENCH_Z))
    box("pr_base", (0.56, 0.5, 0.09), (0, 0, 0.045), mat("frame_p"), g, 0.015, 0.012)
    box("pr_bed", (0.44, 0.4, 0.018), (0, 0, 0.12), mat("bed"), g, 0.005, 0.008)
    for x in (-0.25, 0.25):
        box(f"pr_up{x}", (0.04, 0.04, 0.56), (x, 0.17, 0.37), mat("frame_p"), g, 0.008, 0.01)
    box("pr_top", (0.54, 0.04, 0.04), (0, 0.17, 0.65), mat("frame_p"), g, 0.008, 0.01)
    box("pr_rail", (0.5, 0.025, 0.025), (0, 0.13, 0.42), mat("metal"), g, 0.005, 0.006)
    head = empty("pr_headp", g, (0.0, 0.1, 0.42))
    box("pr_head", (0.1, 0.08, 0.11), (0, 0, 0), mat("head_p"), head, 0.018, 0.01)
    box("pr_nozzle", (0.02, 0.02, 0.04), (0, -0.005, -0.07), mat("metal"), head, 0.004, 0.005)
    # spool holder on the right side
    arm = empty("pr_holder", g, (0.33, 0.12, 0.42))
    cyl("pr_holder_arm", 0.012, 0.16, (0.06, 0, 0), mat("metal"), arm, axis="X", ol=0.006)
    # front screen
    scr = empty("pr_screen", g, (-0.16, -0.255, 0.05), (0, 0, 0))
    box("pr_scr_bezel", (0.22, 0.012, 0.11), (0, 0, 0), mat("black"), scr, 0.004, 0.006)
    ui = empty("pr_ui", scr, (0, -0.0075, 0), (90, 0, 0))
    return g, head, arm, ui


PRINTER, PR_HEAD, PR_HOLDER, PR_UI = build_printer()


def spool(name, colkey, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), r=0.1, w=0.07):
    """Filament spool: two light flanges, the coloured filament wound between them (axis = local X)."""
    g = empty(name, parent, loc, rot)
    for s in (-1, 1):
        cyl(f"{name}_fl{s}", r, 0.008, (s * w / 2, 0, 0), mat("#d9dcd9"), g, axis="X", bevel=0.002, ol=0.008)
    cyl(f"{name}_fil", r * 0.86, w - 0.004, (0, 0, 0), mat(colkey), g, axis="X", ol=0.006)
    cyl(f"{name}_hub", r * 0.3, w + 0.012, (0, 0, 0), mat("#9da29d"), g, axis="X")
    return g


SPOOL_PLA = spool("SPOOL_PLA", "pla")
SPOOL_BLK = spool("SPOOL_BLK", "blk")
SPOOL_PETG = spool("SPOOL_PETG", "petg")
SPOOL_ASA = spool("SPOOL_ASA", "asa")
SPOOLS = (SPOOL_PLA, SPOOL_BLK, SPOOL_PETG, SPOOL_ASA)


def vent(name, colkey, droop=0.0, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), s=1.0, seed=3):
    """A dash air vent (bezel + 4 slats), melted by `droop` 0..1: the middle sags, the face slumps forward, two drips."""
    g = temp(empty(name, parent, loc, rot))
    hw, d, h = 0.13 * s, 0.05 * s, 0.1 * s
    bm = bmesh.new()

    def bx(cx, cy, cz, sx, sy, sz):
        r = bmesh.ops.create_cube(bm, size=1.0)
        for v in r["verts"]:
            v.co = Vector((cx + v.co.x * sx, cy + v.co.y * sy, cz + v.co.z * sz))
    t = 0.022 * s
    bx(0, 0, t / 2, 2 * hw, d, t)                 # bottom
    bx(0, 0, h - t / 2, 2 * hw, d, t)             # top
    bx(-hw + t / 2, 0, h / 2, t, d, h)            # sides
    bx(hw - t / 2, 0, h / 2, t, d, h)
    for k in range(4):                            # slats, slightly tilted
        z = t + (k + 0.5) * (h - 2 * t) / 4
        bx(0, -0.004 * s, z, 2 * hw - 2 * t, d * 0.7, 0.008 * s)
    bx(0, 0.02 * s, h / 2, 2 * hw - 2 * t, 0.006 * s, h - 2 * t)   # dark back plate
    dd = droop
    if dd > 0:
        for v in bm.verts:
            x, y, z = v.co
            u = 1 - (x / hw) ** 2                       # 1 in the middle, 0 at the ends
            hz = z / h
            v.co.z = z - dd * (0.12 * s * u * (0.35 + hz) + 0.035 * s * hz)
            v.co.y = y - dd * 0.035 * s * hz * (0.4 + u)   # face slumps toward the viewer
            v.co.x = x * (1 + 0.1 * dd * (1 - hz))
    ob = new_obj(name + "_m", bm, [mat(colkey), OUTLINE], g)
    add_mods(ob, 0.0, 0.006 * s, char=True)
    me = ob.data
    for p in me.polygons:   # slats + back plate darker: index by height of the face centre is enough for a toon read
        pass
    if dd > 0.15:           # drips under the sagging middle
        rng = random.Random(seed)
        for k in range(2):
            x = rng.uniform(-0.45, 0.45) * hw
            L = (0.012 + 0.05 * (dd - 0.15)) * s * (1.0 if k == 0 else 0.7)
            zc = -dd * 0.055 * s * (1 - (x / hw) ** 2) * 0.35
            cyl(f"{name}_drip{k}", 0.008 * s, L, (x, -0.01 * s, zc - L / 2 + 0.004), mat(colkey), g, ol=0.004)
            blob(f"{name}_dripb{k}", (0.011 * s, 0.011 * s, 0.013 * s), (x, -0.01 * s, zc - L), mat(colkey), g)
    return g


def build_shelf():
    """The series' growing failed-prints shelf, on the back wall between the roll-up door and the pegboard."""
    g = empty("SHELF", None, (1.25, 3.42, 1.45))
    box("sh_board", (1.05, 0.34, 0.035), (0, 0, 0), mat("wood"), g, 0.008, 0.012)
    for x in (-0.42, 0.42):
        box(f"sh_brk{x}", (0.03, 0.26, 0.16), (x, 0.03, -0.09), mat("dark"), g, 0.004, 0.008)
    # earlier failures (running gag): a spaghetti blob and a warped plate
    rng = random.Random(4)
    for k in range(14):
        a = rng.uniform(0, 2 * math.pi)
        torus(f"sh_spag{k}", rng.uniform(0.03, 0.06), 0.006, (0.33 + rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05),
              0.05 + rng.uniform(0, 0.06)), mat("#d27a4a"), g, rot=(rng.uniform(0, 180), rng.uniform(0, 180), 0))
    w = box("sh_warp", (0.2, 0.15, 0.012), (-0.33, 0, 0.04), mat("#9fb4c9"), g, 0.003, 0.006, rot=(0, -9, 0))
    return g


SHELF = build_shelf()
SHELF_SLOTS = [(-0.08, 0.0), (0.13, 0.02)]   # where droopy vents land (local x, y)


def build_outdoor():
    """Sun-test set, away from the shop (x=60): car dashboard + windscreen frame looking out at a big cartoon sun."""
    g = empty("OUTDOOR", None, (60, 0, 0))
    box("od_sky", (40, 0.2, 24), (0, 14, 6), emit("sky", 1.0), g)
    box("od_ground", (40, 30, 0.02), (0, 6, -0.01), mat("asphalt"), g)
    box("od_grass", (40, 8, 0.03), (0, 12, 0.0), mat("grass"), g)
    sun = empty("od_sun", g, (2.2, 13.5, 5.6))
    cyl("od_sun_disc", 1.1, 0.05, (0, 0, 0), emit("sunc", 1.25), sun, axis="Y", seg=48)
    for k in range(12):
        a = 2 * math.pi * k / 12
        tri = poly(f"od_ray{k}", [(-0.16, 1.35), (0.16, 1.35), (0, 2.05)], emit("sunray", 1.15), sun, rot=(90, 0, 0))
        tri.rotation_euler = (math.radians(90), math.radians(math.degrees(a)), 0)
    # car: dashboard, windscreen frame, hood
    car = empty("od_car", g, (0, 0, 0))
    box("od_dash", (1.9, 0.62, 0.16), (0, 0.05, 0.86), mat("dash"), car, 0.03, 0.014)
    box("od_dash_top", (1.9, 0.5, 0.03), (0, 0.08, 0.955), mat("dash_l"), car, 0.01, 0.01)
    for x in (-0.95, 0.95):
        box(f"od_pillar{x}", (0.09, 0.09, 0.95), (x, 0.55, 1.35), mat("car"), car, 0.02, 0.014, rot=(-32, 0, 0))
    box("od_roof", (2.0, 0.5, 0.08), (0, 0.15, 1.83), mat("car"), car, 0.02, 0.014)
    box("od_hood", (2.1, 1.6, 0.06), (0, 1.25, 0.82), mat("car"), car, 0.03, 0.014, rot=(-6, 0, 0))
    # bumper-piece test stand (A9) to the side
    st = empty("od_stand", g, (3.4, 3.2, 0.0))
    box("od_stand_top", (0.9, 0.5, 0.06), (0, 0, 0.62), mat("wood"), st, 0.01, 0.012)
    for x in (-0.38, 0.38):
        box(f"od_stand_leg{x}", (0.05, 0.4, 0.6), (x, 0, 0.3), mat("dark"), st, 0.005, 0.01)
    return g, sun, st


OUTDOOR, OD_SUN, OD_STAND = build_outdoor()
OD_VENT_LOC = (60.0, -0.04, 0.97)


def bumper_piece(name, parent, loc, colkey="asa"):
    """One cut bumper corner piece (a curved slab with a lip), the kind SeamForge exports."""
    g = temp(empty(name, parent, loc))
    pts = []
    for i in range(9):
        a = math.radians(-60 + 120 * i / 8)
        for z in (0.0, 0.26):
            r = 0.36 + (0.02 if z else 0.0)
            pts.append((r * math.sin(a), -r * math.cos(a) + 0.3, z))
    bm = bmesh.new()
    n = 9
    vs = [[bm.verts.new((x, y, z)) for (x, y, z) in pts[2 * i:2 * i + 2]] for i in range(n)]
    th = 0.03
    inner = [[bm.verts.new((x * (1 - th / 0.37), (y - 0.3) * (1 - th / 0.37) + 0.3, z)) for (x, y, z) in pts[2 * i:2 * i + 2]]
             for i in range(n)]
    for i in range(n - 1):
        bm.faces.new((vs[i][0], vs[i + 1][0], vs[i + 1][1], vs[i][1]))
        bm.faces.new((inner[i][1], inner[i + 1][1], inner[i + 1][0], inner[i][0]))
        bm.faces.new((vs[i][1], vs[i + 1][1], inner[i + 1][1], inner[i][1]))
        bm.faces.new((inner[i][0], inner[i + 1][0], vs[i + 1][0], vs[i][0]))
    bm.faces.new((vs[0][0], vs[0][1], inner[0][1], inner[0][0]))
    bm.faces.new((inner[n - 1][0], inner[n - 1][1], vs[n - 1][1], vs[n - 1][0]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = new_obj(name + "_m", bm, [mat(colkey), OUTLINE], g)
    add_mods(ob, 0.006, 0.008, char=True)
    box(name + "_lip", (0.08, 0.05, 0.035), (0.0, -0.075, 0.02), mat(colkey), g, 0.008, 0.006)
    return g


def mold(name, colkey, parent, loc, lift=0.0):
    """Open-top mold box (outer shell + dark cavity). `lift` raises one corner (warp), in degrees."""
    g = temp(empty(name, parent, loc))
    piv = empty(name + "_piv", g, (-0.16, 0.0, 0.0), (0, -lift, 0))   # hinge on the left edge, right side lifts
    box(name + "_shell", (0.32, 0.24, 0.1), (0.16, 0, 0.05), mat(colkey), piv, 0.01, 0.008)
    box(name + "_cav", (0.25, 0.17, 0.02), (0.16, 0, 0.092), mat("mold_in"), piv, 0.008)
    box(name + "_cav2", (0.18, 0.1, 0.022), (0.16, 0, 0.096), mat("#3b3e3b"), piv, 0.008)
    return g


def screen_pieces(ui, n_lit=4):
    """Printer screen content: the cut bumper pieces as sage silhouettes on near-black (no text)."""
    g = temp(empty("pr_ui_c", ui))
    g.scale = (1.5, 1.5, 1.5)
    poly("pr_ui_bg", [(-0.068, -0.032), (0.068, -0.032), (0.068, 0.032), (-0.068, 0.032)], emit("#151715", 1.0), g, z=0.0)
    shapes = [[(-0.055, -0.02), (-0.03, -0.022), (-0.025, 0.02), (-0.05, 0.022)],
              [(-0.02, -0.022), (0.008, -0.02), (0.01, 0.022), (-0.018, 0.02)],
              [(0.015, -0.02), (0.04, -0.022), (0.042, 0.015), (0.02, 0.022)],
              [(0.046, -0.02), (0.06, -0.02), (0.062, 0.02), (0.048, 0.016)]]
    for k, s in enumerate(shapes[:n_lit]):
        poly(f"pr_ui_p{k}", s, emit("sage_l", 1.2), g, z=0.0006)
    return g


# ----------------------------------------------------------------------------------------------------------------- expressions
def expr_state(ch, t):
    """Ep 8 expressions, keyed from the line/word times (eye shapes only; series spec)."""
    st = dict(fL=0.0, fR=0.0, shape=None, scale=1.0, on=0.0, hL=0.0, hR=0.0, tL=0.0, tR=0.0, roll=None)

    def blend(name, k):
        if k <= 0:
            return
        tgt = dict(zip(("fL", "fR", "shape", "scale", "on", "hL", "hR", "tL", "tR"), STATES[name]))
        for key in ("fL", "fR", "scale", "on", "hL", "hR", "tL", "tR"):
            st[key] = lerp(st[key], tgt[key], k)
        if tgt["shape"] and k > 0.5:
            st["shape"] = tgt["shape"]

    def worried(k):
        st["fL"] = st["fR"] = lerp(st["fL"], 0.45, k)
        st["tL"] = st["tR"] = lerp(st["tL"], -18, k)
        st["on"] = max(st["on"], k)

    L = LNO
    if ch is GUS:
        for Ln in TL["lines"]:
            if Ln["speaker"] == "GUS":                              # matter-of-fact: subtle D-cut while he explains
                k = win(t, Ln["t0"] - 0.15, Ln["t1"], 0.2, 0.4)
                st["fL"] = st["fR"] = max(st["fL"], 0.2 * k)
                st["on"] = max(st["on"], 0.65 * k)
                st["tL"] = st["tR"] = max(st["tL"], 10 * k)
        k = win(t, L[3]["t0"], L[3]["t1"], 0.1, 0.3)                # dry "Sure."
        st["fL"] = st["fR"] = lerp(st["fL"], 0.45, k)
        k = win(t, L[8]["t0"] - 0.2, L[8]["t1"], 0.1, 0.3)          # flat "...Black PETG still melts"
        st["fL"] = st["fR"] = lerp(st["fL"], 0.55, k)
        st["tL"] = st["tR"] = lerp(st["tL"], 14, k)
        blend("skeptical", 0.6 * win(t, L[16]["t0"] - 0.1, L[16]["t1"] + 0.6, 0.12, 0.2))
    else:
        blend("curious", win(t, L[1]["t0"], L[1]["t1"], 0.15, 0.3))
        blend("excited", win(t, W(2, 0)["t0"], L[2]["t1"] + 0.3, 0.08, 0.25))
        worried(win(t, L[4]["t0"] - 0.35, L[5]["t1"] - 0.6, 0.15, 0.4))
        blend("excited", win(t, L[7]["t0"], L[7]["t1"] + 0.1, 0.08, 0.2))
        worried(win(t, word_t(8, "melts") - 0.1, L[8]["t1"] + 0.4, 0.15, 0.3))
        blend("impatient", win(t, L[9]["t0"], L[9]["t1"], 0.08, 0.3))
        blend("excited", win(t, word_t(10, "rain"), L[10]["t1"] + 0.8, 0.1, 0.3))
        blend("curious", win(t, L[14]["t0"], L[14]["t1"], 0.2, 0.3))
        blend("excited", win(t, L[15]["t0"] - 0.05, L[16]["t1"] + 0.3, 0.06, 0.2))
    return st


# ----------------------------------------------------------------------------------------------------------------- helpers
def SFR(sh):
    s = next(x for x in TL["shots"] if x["id"] == sh)
    return s["f0"], s["f1"]


def kshot(fr, sh):
    f0, f1 = SFR(sh)
    return (fr - f0) / max(1, f1 - 1 - f0)


def talker(ch, t):
    nm = "GUS" if ch is GUS else "PIP"
    return talk(nm, t)


def hide_ep8():
    for ob in SPOOLS + (SHELF,):
        set_vis(ob, True)
    for ob in SPOOLS:
        ob.parent = None
        ob.location = (50, 50, 0)
        ob.scale = (1, 1, 1)
    PR_HEAD.location = (0.0, 0.1, 0.42)


def spools_on_bench():
    """Spare spools on the bench, right of the printer (PETG, black, ASA)."""
    for k, sp in enumerate((SPOOL_PETG, SPOOL_BLK, SPOOL_ASA)):
        sp.parent = None
        sp.location = (3.95 + 0.19 * k, 3.2, BENCH_Z + 0.1)
        sp.rotation_euler = (0, 0, math.radians(90))


def shelf_vents(n):
    """Droopy failures already on the shelf: 1 = PLA vent, 2 = + black PETG vent."""
    for k, colkey in enumerate(("pla", "blk")[:n]):
        x, y = SHELF_SLOTS[k]
        vent(f"shv{k}", colkey, 1.0, SHELF, (x, y, 0.018), (0, 0, 8 - 14 * k), 1.0, seed=5 + k)


def printer_head_wiggle(t, on=True):
    if on:
        PR_HEAD.location = (0.12 * math.sin(t * 9.0), 0.1, 0.42)


def cam_look(loc, tgt, lens, dl=(0, 0, 0), k=0.0):
    look(cam, Vector(loc) + Vector(dl) * k, Vector(tgt) + Vector(dl) * k, lens)


def outdoor_light(t):
    """Sun pulses (heat) in the dash shots."""
    s = 1 + 0.05 * math.sin(t * 7.0)
    OD_SUN.scale = (s, s, s)
    OD_SUN.rotation_euler = (0, math.radians(8 * t), 0)


# ----------------------------------------------------------------------------------------------------------------- shots
# shop staging: printer on the bench at (3.05, 3.12); Pip and Gus stand in front of it, facing the camera side.
PIP_SPOT = (2.55, 2.25, 0)
GUS_SPOT = (3.65, 2.3, 0)


def anim_A1(fr):
    """Printer's ready! What do we load in it? - Pip bounces at the empty printer; Gus beside it."""
    t, k = fr / FPS, kshot(fr, "A1")
    spools_on_bench()
    shelf_vents(0)
    m, lid = talk("PIP", t)
    hop = abs(math.sin(t * 6.5)) * 0.03 * win(t, LNO[1]["t0"], LNO[1]["t1"], 0.1, 0.2)
    pose(PIP, loc=(2.45, 2.3, hop), rz=-25, hips=(-4, 0, 0), head=(-10, 0, -18), armL=(-40, 0, -10),
         armR=(-120, 0, -30), elbowL=-20, elbowR=-30, mouth=m, lid=lid, look=(0.7, 0.4))
    m2, lid2 = talk("GUS", t)
    pose(GUS, loc=(3.5, 2.4, 0), rz=18, head=(4, 0, 20), mouth=m2, lid=lid2, look=(-0.7, -0.3))
    cam_look((2.75, -0.35, 1.4), (3.05, 2.7, 1.0), 30, (0.1, 0.3, 0), ease(k))


def anim_A2(fr):
    """This one! PLA! - Pip slides the sage spool onto the empty holder."""
    t, k = fr / FPS, kshot(fr, "A2")
    spools_on_bench()
    m, lid = talk("PIP", t)
    tb = word_t(2, "PLA")
    u = ease((t - (tb - 0.45)) / 0.55)
    pose(PIP, loc=(3.85, 2.72, 0), rz=-100, hips=(-8, 0, 0), head=(-14, 0, 0), armL=(-70, 0, 6), armR=(-95, 0, -18),
         elbowL=-30, elbowR=-24, mouth=m, lid=lid, look=(0.6, 0.6))
    bpy.context.view_layer.update()
    hold = PIP.hands["R"].matrix_world.translation + Vector((0.05, 0.02, 0.06))
    home = PR_HOLDER.matrix_world @ Vector((0.08, 0, 0))
    SPOOL_PLA.parent = None
    SPOOL_PLA.location = hold.lerp(home, u)
    SPOOL_PLA.rotation_euler = (0, 0, 0)
    pose(GUS, loc=(30, 30, 0))
    cam_look((3.6, 0.75, 1.2), (3.6, 3.0, 1.05), 27, (0.0, 0.25, 0), ease(k))


def pla_loaded():
    SPOOL_PLA.parent = None
    SPOOL_PLA.location = PR_HOLDER.matrix_world @ Vector((0.08, 0, 0))
    SPOOL_PLA.rotation_euler = (0, 0, 0)


def anim_A3(fr):
    """Sure. Print a vent and leave it in the sun. - Gus, dry; the printer prints; a sage vent pops up on the bed."""
    t, k = fr / FPS, kshot(fr, "A3")
    spools_on_bench()
    pla_loaded()
    printer_head_wiggle(t)
    tv = word_t(3, "vent")
    if t > tv:
        s = eback((t - tv) / 0.3, 2.0)
        vent("bedvent", "pla", 0.0, PRINTER, (0.0, -0.02, 0.13), (0, 0, 0), max(0.01, s))
    m, lid = talk("GUS", t)
    pose(GUS, loc=(3.8, 2.6, 0), rz=28, hips=(2, 0, 0), head=(2, 0, 14), armL=(-30, 0, 10), armR=(-10, 0, -6),
         elbowL=-40, mouth=m, lid=lid, look=(-0.6, -0.2))
    pose(PIP, loc=(2.3, 2.35, 0), rz=-30, head=(-8, 0, -20), look=(0.8, 0.3))
    cam_look((3.45, 0.15, 1.45), (3.5, 3.0, 1.12), 28, (0.0, 0.2, 0), ease(k))


def dash_cam(t, k, tight=0.0):
    cam_look((60.0, -1.1, 1.38), (60.0, 0.4, 1.12), 30 + 8 * tight, (0, 0.2, -0.04), ease(k))


def anim_A4(fr):
    """...It's melting! - the PLA vent on the dash, in the sun, sags and drips."""
    t, k = fr / FPS, kshot(fr, "A4")
    outdoor_light(t)
    pose(PIP, loc=(30, 30, 0)); pose(GUS, loc=(31, 30, 0))
    d = ease(k * 1.15)
    vent("dashvent", "pla", d, None, OD_VENT_LOC, (0, 0, 0), 1.15)
    dash_cam(t, k, 0.4)


def anim_A5(fr):
    """PLA's easy to print. It just hates heat. - Gus drops the melted vent on the failed-prints shelf."""
    t, k = fr / FPS, kshot(fr, "A5")
    spools_on_bench()
    pla_loaded()
    f0, _ = SFR("A5")
    u = (t - f0 / FPS) / 0.55
    x, y = SHELF_SLOTS[0]
    z = 0.018 + 0.5 * (1 - eback(u, 1.6)) if u < 1 else 0.018
    vent("shv0", "pla", 1.0, SHELF, (x, y, z), (0, 0, 8), 1.0, seed=5)
    m, lid = talk("GUS", t)
    pose(GUS, loc=(1.95, 2.8, 0), rz=-22, hips=(2, 0, 0), head=(4, 0, -16), armL=(-60, 0, 20), armR=(-10, 0, -6),
         elbowL=-50, mouth=m, lid=lid, look=(-0.4, 0.1))
    pose(PIP, loc=(0.85, 2.65, 0), rz=-12, head=(-6, 0, 18), look=(0.6, 0.5))
    cam_look((1.3, 0.55, 1.75), (1.3, 3.3, 1.3), 28, (0.05, 0.25, 0), ease(k))


def anim_A6(fr):
    """Inside the car? PETG. Tougher, handles more heat. - a light PETG vent in the same sun holds its shape."""
    t, k = fr / FPS, kshot(fr, "A6")
    outdoor_light(t)
    pose(PIP, loc=(30, 30, 0)); pose(GUS, loc=(31, 30, 0))
    tp = word_t(6, "PETG", LNO[6]["t0"] + 1.0)
    if t > tp - 0.15:
        s = eback((t - tp + 0.15) / 0.3, 2.0)
        vent("dashvent", "petg", 0.0, None, OD_VENT_LOC, (0, 0, 0), 1.15 * max(0.01, s))
    dash_cam(t, k, 0.2)


def anim_A7(fr):
    """So I'll print it in black! (Pip with the black spool) / ...Black PETG still melts in the sun. (dash: it droops)."""
    t, k = fr / FPS, kshot(fr, "A7")
    tc = LNO[8]["t0"] - 0.25
    if t < tc:
        spools_on_bench()
        pla_loaded()
        shelf_vents(1)
        m, lid = talk("PIP", t)
        pose(PIP, loc=(2.75, 2.3, 0), rz=-6, hips=(-6, 0, 0), head=(-12, 0, 0), armL=(-150, 0, -10), armR=(-150, 0, 10),
             elbowL=-10, elbowR=-10, mouth=m, lid=lid, look=(0.0, 0.2))
        bpy.context.view_layer.update()
        hc = PIP.neck.matrix_world @ Vector((0, 0, PIP.head_c))
        SPOOL_BLK.parent = None
        SPOOL_BLK.location = hc + Vector((0, -0.02, 0.5))
        SPOOL_BLK.rotation_euler = (0, 0, math.radians(20))
        SPOOL_BLK.scale = (1.5, 1.5, 1.5)
        pose(GUS, loc=(30, 30, 0))
        cam_look((2.75, 0.6, 1.25), (2.75, 2.3, 1.15), 32, (0, 0.15, 0), ease((t - SFR("A7")[0] / FPS) / max(0.3, tc - SFR("A7")[0] / FPS)))
    else:
        outdoor_light(t)
        pose(PIP, loc=(30, 30, 0)); pose(GUS, loc=(31, 30, 0))
        tm = word_t(8, "melts")
        d = 0.6 * ease((t - (tc + 0.2)) / max(0.3, tm - tc)) + 0.4 * ease((t - tm) / 1.0)
        vent("dashvent", "blk", d, None, OD_VENT_LOC, (0, 0, 0), 1.15, seed=9)
        dash_cam(t, (t - tc) / max(0.5, SFR("A7")[1] / FPS - tc), 0.4)


def anim_A8(fr):
    """And my bumper? - Pip points at the printer screen: the cut bumper pieces. Two melted vents on the shelf behind."""
    t, k = fr / FPS, kshot(fr, "A8")
    spools_on_bench()
    pla_loaded()
    shelf_vents(2)
    screen_pieces(PR_UI)
    m, lid = talk("PIP", t)
    pose(PIP, loc=(3.7, 2.55, 0), rz=-55, hips=(-6, 0, 0), head=(-14, 0, -6), mouth=m, lid=lid, look=(-0.7, -0.4))
    aim_arm(PIP, "R", PR_UI.matrix_world.translation + Vector((0.05, -0.12, 0.02)))
    pose(GUS, loc=(30, 30, 0))
    cam_look((3.35, 1.15, 1.3), (3.3, 3.0, 1.0), 27, (0.0, 0.2, 0), ease(k))


def anim_A9(fr):
    """Outside? ASA. It's made for sun and rain. - an ASA bumper piece on a stand: sun, then cloud and rain: unchanged."""
    t, k = fr / FPS, kshot(fr, "A9")
    pose(PIP, loc=(30, 30, 0)); pose(GUS, loc=(31, 30, 0))
    bumper_piece("asa_piece", OD_STAND, (0, -0.12, 0.65))
    tr = word_t(10, "rain", LNO[10]["t1"] - 0.6)
    ts = word_t(10, "sun", tr - 0.6)
    c = ease((t - (tr - 0.55)) / 0.5)                          # cloud slides over the sun before "rain"
    s = 1 + 0.05 * math.sin(t * 7.0)
    OD_SUN.scale = (s, s, s)
    cg = temp(empty("cloud", OUTDOOR, (lerp(9.5, 5.6, c), 12.8, 5.9)))
    for j, (dx, dz, r) in enumerate(((-0.9, 0, 0.9), (0, 0.35, 1.15), (0.95, 0.05, 0.85), (0.1, -0.35, 0.9))):
        blob(f"cloud{j}", (r * 1.3, 0.3, r * 0.75), (dx, 0, dz), emit("cloud", 1.0), cg)
    if t > tr - 0.15:                                          # rain streaks over the stand
        rng = random.Random(fr)
        bm = bmesh.new()
        for _ in range(70):
            x, y, z = rng.uniform(-1.4, 1.4), rng.uniform(-0.8, 1.0), rng.uniform(0.2, 2.6)
            for v in bmesh.ops.create_cube(bm, size=1.0)["verts"]:
                v.co = Vector((x + v.co.x * 0.008, y + v.co.y * 0.008, z + v.co.z * 0.16))
        temp(new_obj("rain", bm, [emit("rain", 1.0)], OD_STAND))
    bpy.context.view_layer.update()                             # matrix_world is stale on a process's first frame
    st = OD_STAND.matrix_world.translation
    cam_look((st.x - 0.25, st.y - 1.9, 1.05), (st.x - 0.1, st.y + 0.5, 1.25), 28, (0, 0.3, 0.0), ease(k))


def anim_A10(fr):
    """And it depends what it's for. Molds? PETG or ASA. PETG warps less. - two molds on the bench; the ASA one lifts a corner."""
    t, k = fr / FPS, kshot(fr, "A10")
    spools_on_bench()
    pla_loaded()
    shelf_vents(2)
    tm = word_t(14, "Molds", LNO[14]["t0"] + 1.6)
    tw = word_t(14, "warps", LNO[14]["t1"] - 0.8)
    a = ease((t - (tm - 0.1)) / 0.35)
    if t > tm - 0.1:
        mold("mold_petg", "petg", None, (2.2, 2.95, BENCH_Z + 0.002 + 0.25 * (1 - eback(a, 1.4))), 0.0)
        lift = 12.0 * ease((t - tw) / 0.6)
        mold("mold_asa", "asa", None, (2.58, 2.95, BENCH_Z + 0.002 + 0.25 * (1 - eback(a, 1.4))), lift)
    m, lid = talk("GUS", t)
    pose(GUS, loc=(1.75, 2.3, 0), rz=-25, hips=(2, 0, 0), head=(4, 0, 20), armL=(-45, 0, 12), elbowL=-40, mouth=m, lid=lid,
         look=(0.7, -0.3))
    pose(PIP, loc=(3.4, 2.3, 0), rz=28, head=(-12, 0, 10), look=(-0.7, -0.3))
    # wide two-shot for "it depends what it's for", then push in on the molds as they drop ("Molds?")
    p = ease((t - (tm - 0.25)) / 0.8)
    loc = Vector((2.55, 0.15, 1.5)).lerp(Vector((2.39, 1.55, 1.38)), p)
    tgt = Vector((2.55, 2.6, 1.0)).lerp(Vector((2.39, 2.95, BENCH_Z + 0.02)), p)
    look(cam, loc, tgt, lerp(24, 30, p))


def _pip_holding_ep8(t, look_=(0.6, 0.6)):
    c, n, u, r = phone_pose_s11()
    m, lid = talk("PIP", t)
    acc = accent("PIP", t)
    PIP.neck.rotation_euler = [math.radians(a) for a in (-12 + 6 * acc, 0, -16 + 3 * math.sin(t * 4))]
    set_face(PIP, m, lid, look_, (0.04, -12))
    return c, n, u, r


def anim_A11(fr):
    """Like these?! - Pip holds the phone up to Gus (screen = key colour, the real footage goes in by corner-pin)."""
    t = fr / FPS
    c, n, u, r = _pip_holding_ep8(t)
    f = -Vector((n.x, n.y, 0)).normalized()
    pose(GUS, loc=(0, 0, 0), rz=math.degrees(math.atan2(f.x, -f.y)) + 25, hips=(6, 0, 0), head=(14, 0, 0), look=(0, -0.6))
    place_head_xy(GUS, c + n * 0.75 + r * 0.62)
    look(cam, c + n * 1.2 - r * 0.16 - u * 0.2, c - r * 0.16 - u * 0.2, 38, up=u)


def anim_A12(fr):
    """...Yeah. Like those. - Gus leans in; the camera pushes along the screen normal until the screen fills the frame."""
    t, k = fr / FPS, kshot(fr, "A12")
    c, n, u, r = _pip_holding_ep8(t, look_=(0.9, 0.7))
    f = -Vector((r.x, r.y, 0)).normalized()
    rz = math.degrees(math.atan2(f.x, -f.y))
    lean = eout((t - SFR("A12")[0] / FPS) / 0.4)
    hx = lerp(14, 32, lean)
    m, lid = talk("GUS", t)
    pose(GUS, loc=(0, 0, 0), rz=rz, hips=(hx, 0, 0), head=(-0.85 * hx, 0, 0), armL=(hx, 0, 8), armR=(hx, 0, -8), elbowL=-10,
         elbowR=-10, mouth=m, lid=lid, look=(0, -0.2))
    want = c - n * 0.06 + r * lerp(0.62, 0.47, lean)
    bpy.context.view_layer.update()
    hc = GUS.neck.matrix_world @ Vector((0, 0, GUS.head_c))
    GUS.root.location += Vector((want.x - hc.x, want.y - hc.y, min(0.0, (c.z + 0.12) - hc.z)))
    s12_cam(c, n, u, k)


ANIM8 = {s["id"]: globals()[f"anim_{s['id']}"] for s in TL["shots"]}


def reset8():
    reset()
    pip_scanner("pouch")
    set_vis(PIPSCAN, True)
    set_vis(UI, False)
    set_vis(LAPTOP, False)
    STOOL.location = (-3.7, 2.7, 0)
    hide_ep8()
    OD_SUN.scale = (1, 1, 1)


# ----------------------------------------------------------------------------------------------------------------- run
CORN = os.path.join(OUT, "screen_corners.json")
corners = json.load(open(CORN)) if os.path.exists(CORN) else dict(
    doc="Phone-screen corners for the Ep 8 phone hand-off (corner-pin the real footage). Pixels in the 1080x1920 frame, origin "
        "top-left, x right, y down. Corner order tl, tr, br, bl. Frames are cartoon frames at 30 fps (ep8_timeline.json). The "
        "screen renders as flat key colour #ff00ff.",
    width=1080, height=1920, fps=FPS, key_colour=KEY, corner_order=["tl", "tr", "br", "bl"], shots={})
lo, hi = (int(x) for x in RANGE.split(":")) if RANGE else (0, 10 ** 9)
for sh in EP8_SHOTS:
    f0, f1 = SFR(sh)
    d = os.path.join(OUT, sh)
    os.makedirs(d, exist_ok=True)
    per, tsum, nr = {}, 0.0, 0
    for fr in range(f0, f1):
        final = os.path.join(d, f"{fr:04d}.png")
        need_c = sh in ("A11", "A12") and not ONLY
        todo = (fr - f0) % EVERY == 0 and lo <= fr < hi and not os.path.exists(final) and (not ONLY or fr in ONLY)
        if not (todo or need_c):
            continue
        CUR_T = fr / FPS
        reset8()
        ANIM8[sh](fr)
        bpy.context.view_layer.update()
        if need_c:
            per[str(fr)] = screen_corners_px()
        if not todo:
            continue
        scn.render.filepath = os.path.join(d, f"{fr:04d}_tmp")
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        os.replace(os.path.join(d, f"{fr:04d}_tmp.png"), final)
        tsum += time.time() - t0
        nr += 1
        print(f"[ep8] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if per:
        corners["shots"][sh] = dict(frames=[f0, f1], static=(sh == "A11"), per_frame=per)
        corners["screen_full_frame"] = TL["screen_full_frame"]
        json.dump(corners, open(CORN, "w"), indent=1)
    if nr:
        print(f"[ep8] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
