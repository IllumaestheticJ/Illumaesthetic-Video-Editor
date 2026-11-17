"""Pip & Gus Ep 4 ("Can't you just 3D print the scan?") - Part A animation. Runs INSIDE the pilot's scene builder
(projects/scan-tedium-explainer-reel/tools/partA_scene.py, the locked characters, shop and render look) via --exec:

  cd projects/scan-tedium-explainer-reel/tools && blender -b --factory-startup -P partA_scene.py -- --exec \
     ../../pip-gus-ep4-print-the-scan/tools/ep4_anim.py --out FRAMES_DIR --timeline ../../pip-gus-ep4-print-the-scan/ep4_timeline.json \
     --shots E1,E2 [--scale 1] [--spp 8] [--frames 40,120] [--range a:b] [--every N]

Same rules as the pilot's partA_anim.py (whose generic talk/blink/expression code is copied below verbatim, marked):
every frame is posed procedurally from the timeline, rendered as FRAMES_DIR/<shot>/<frame>.png (resumable, written via a
_tmp file), persistent data off, no text anywhere in 3D.

Ep 4 additions: an unbranded cartoon printer, Pip's bumper sketch, the failed-print shelf (with Ep 1's spaghetti), a
triangulated scan of the cartoon car (fill + wire sharing one mesh, so a ripple moves both), the stock bumper copy, Pip's
bumper, trace lines (curve bevel draw-on), and two laptop screens (the scan, the slicer's empty plate).
"""
import re as _re

ep4_dir = os.path.dirname(os.path.abspath(arg("--exec", "")))
_tl_path = arg("--timeline", os.path.join(ep4_dir, "..", "ep4_timeline.json"))
TL = json.load(open(_tl_path))
FPS = TL["fps"]
SF = {s["id"]: (s["f0"], s["f1"]) for s in TL["shots"]}
LN = {L["n"]: L for L in TL["lines"]}
EVERY = int(arg("--every", "1"))
RANGE = arg("--range", "")
ONLY = {int(x) for x in arg("--frames", "").split(",") if x}
SHOTS = [s for s in arg("--shots", ",".join(SF)).split(",") if s in SF]

# ======================== copied from partA_anim.py (generic: easing, talk, blinks, expressions engine) ========================
# ----------------------------------------------------------------------------------------------------------------- easing
def cl(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = cl(x)
    return x * x * (3 - 2 * x)


def eout(x):
    x = cl(x)
    return 1 - (1 - x) ** 2


def eback(x, s=1.4):
    """Ease-out with a small overshoot (cartoon settle)."""
    x = cl(x) - 1
    return 1 + x * x * ((s + 1) * x + s)


def lerp(a, b, t):
    return a + (b - a) * t


def lerpv(a, b, t):
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


# ----------------------------------------------------------------------------------------------------------------- talk
_V = _re.compile(r"[aeiouy]+")


def syllables(word):
    w = _re.sub(r"[^a-z]", "", word.lower())
    g = _V.findall(w) or ["a"]
    if len(g) > 1 and w.endswith("e") and not w.endswith(("le", "ee")) and g[-1] == "e":
        g = g[:-1]
    return g


SYL = {"PIP": [], "GUS": []}
STRESS = {"PIP": [], "GUS": []}
for L in TL["lines"]:
    best = None
    for w in L["words"]:
        g = syllables(w["w"])
        d = max(0.05, w["t1"] - w["t0"]) / len(g)
        for k, v in enumerate(g):
            amp = 1.0 if any(c in v for c in "aou") else 0.72
            SYL[L["speaker"]].append((w["t0"] + k * d, d, amp))
        key = (len(g), w["t1"] - w["t0"])
        if best is None or key > best[0]:
            best = (key, w["t0"])
    STRESS[L["speaker"]].append(best[1])


def mouth_at(spk, t):
    if spk == "GUS":   # v5 (owner): normal talk energy, slightly low-key (v4's slow, heavy talk removed)
        return 0.9 * _mouth_raw(spk, t)
    return _mouth_raw(spk, t)


def _mouth_raw(spk, t):
    t += 1.0 / FPS   # talk energy leads the sound by a frame
    m = 0.0
    for s0, d, a in SYL[spk]:
        u = (t - s0) / d
        if 0 <= u < 1:
            m = max(m, a * (u / 0.3 if u < 0.3 else 1 - 0.8 * (u - 0.3) / 0.7))
    return m


def accent(spk, t):
    """Stressed-word accent, 0..1.8 (v2: x1.8 so the head accents read in motion without a mouth)."""
    return 1.8 * max([math.exp(-((t - ta - 0.04) / 0.12) ** 2) for ta in STRESS[spk]] + [0.0])


def speaking(spk, t, pad=0.1):
    return any(L["t0"] - pad <= t <= L["t1"] + pad for L in TL["lines"] if L["speaker"] == spk)


def _blinks(seed):
    rng = random.Random(seed)
    out, x = [], rng.uniform(0.3, 1.4)
    while x < TL["duration_s"] + 2:
        out.append(x)
        x += rng.uniform(2.0, 3.6)
    return out


BLINKS = {"PIP": _blinks(21), "GUS": _blinks(47)}


def blink(spk, t):
    v = 0.0
    for b in BLINKS[spk]:
        u = (t - b) / 0.14
        if 0 <= u < 1:
            v = max(v, 1 - abs(2 * u - 1))
    return v


def set_face(ch, mouth=0.0, lid=0.0, look=(0, 0), brow=(0, 0)):
    """Face and talk without touching hips/hands (S11/S12: the phone hand must not move): body squash, eyes, look."""
    S = ch.S
    talk_squash(ch, mouth)
    f = max(S.get("base_lid", 0.0), lid)
    set_eyes(ch, f, f)
    ch.eyes_g.location = (look[0] * S["eye_look"], 0, ch.head_c + look[1] * S["eye_look"])
    apply_expr(ch, f, look)


def talk(spk, t, base_lid=0.0):
    """talk energy (drives the body squash and hand lift - no mouths) and lid (blink, plus a squint on the stressed word)."""
    return mouth_at(spk, t), max(base_lid, blink(spk, t), 0.28 * accent(spk, t))


def words_of(n):
    return LN[n]["words"]


def syl_onsets(n):
    out = []
    for w in words_of(n):
        g = syllables(w["w"])
        d = max(0.05, w["t1"] - w["t0"]) / len(g)
        out += [w["t0"] + k * d for k in range(len(g))]
    return out


# ----------------------------------------------------------------------------------------------------------------- expressions (v4)
CUR_T = 0.0
NO_BROWS = True          # v6 (owner, concept B): no brows at all - expressions by eye shape (cut depth + tilt) only
if NO_BROWS:
    for _ch in (GUS, PIP):
        for _b in _ch.browset:
            for _o in list(_b["piv"].children) + [_b["piv"]]:
                bpy.data.objects.remove(_o, do_unlink=True)
        _ch.browset = []
SIGH_DEFLATE = False     # v4 had heavy whole-body sigh deflates; v5 (owner): removed
FORCE_EXPR = {}          # expression sheet: {"PIP": "curious", ...}


def win(t, a, b, rin=0.12, rout=0.2):
    """0..1 envelope: ramps in at a, holds, ramps out after b."""
    if t < a - rin or t > b + rout:
        return 0.0
    if t < a:
        return ease((t - (a - rin)) / rin)
    if t <= b:
        return 1.0
    return 1 - ease((t - b) / rout)


def L_(n):
    return LN.get(n)


def sigh_env(t):
    """Gus's sighs/groans (detected in the take: voiced, outside words): droop builds over the sigh, eases out after."""
    v = 0.0
    for L in TL["lines"]:
        if L["speaker"] != "GUS":
            continue
        for a, b in L.get("sighs", []):
            if a - 0.05 <= t <= b:
                v = max(v, ease((t - a) / max(0.1, b - a)))
            elif b < t < b + 0.45:
                v = max(v, 1 - ease((t - b) / 0.45))
    return v


STATES = {   # name: (fL, fR, shape, scale, brow_on, hL, hR, tL, tR)
    "neutral": (0.0, 0.0, None, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
    "weary": (0.55, 0.55, None, 1.0, 1.0, -0.004, -0.004, 18, 18),
    "exasperated": (1.0, 1.0, "line", 1.0, 1.0, -0.008, -0.008, 22, 22),
    "sigh": (0.8, 0.8, None, 1.0, 1.0, -0.006, -0.006, -10, -10),
    "skeptical": (0.55, 0.0, None, 1.0, 1.0, -0.006, 0.022, 18, -8),
    "curious": (0.0, 0.0, None, 1.15, 0.8, 0.012, 0.012, -4, -4),
    "impatient": (0.4, 0.4, None, 1.0, 1.0, -0.004, -0.004, 16, 16),
    "surprised": (0.0, 0.0, None, 1.3, 1.0, 0.03, 0.03, -6, -6),
    "excited": (0.0, 0.0, "arc", 1.0, 1.0, 0.02, 0.02, -6, -6),
}



# ================================================== Ep 4 expressions ==================================================
def expr_state(ch, t):
    """Per-character eye expression for Ep 4 (eye shapes only, no brows): Gus dry and only slightly annoyed, never angry;
    Pip eager -> impatient -> excited (owner's character notes)."""
    nm = "GUS" if ch is GUS else "PIP"
    if nm in FORCE_EXPR:
        st = list(STATES[FORCE_EXPR[nm]])
        return dict(zip(("fL", "fR", "shape", "scale", "on", "hL", "hR", "tL", "tR"), st), roll=None)
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
        for L in TL["lines"]:                       # matter-of-fact while explaining: subtle D-cut, slight inner-down tilt
            if L["speaker"] == "GUS":
                k = win(t, L["t0"] - 0.15, L["t1"], 0.2, 0.4)
                st["fL"] = st["fR"] = max(st["fL"], 0.2 * k)
                st["on"] = max(st["on"], 0.65 * k)
                st["tL"] = st["tR"] = max(st["tL"], 10 * k)
        L = L_(6)                                    # "Sure." - dry half lid, a touch skeptical
        if L:
            blend("skeptical", win(t, L["t0"] - 0.05, L["t1"] + 0.4, 0.08, 0.3))
        L = L_(7)                                    # eye-roll while Pip asks "Is it done yet?" (pilot gag)
        if L:
            u = (t - L["t0"]) / max(0.3, L["t1"] - L["t0"])
            if 0 <= u <= 1:
                st["roll"] = (math.cos(math.pi * (1 - u)) * 0.9, math.sin(math.pi * u) * 1.0)
        L = L_(8)                                    # deadpan "...There's nothing to print."
        if L:
            k = win(t, L["t0"] - 0.1, L["t1"] + 0.5, 0.1, 0.3)
            st["fL"] = st["fR"] = lerp(st["fL"], 0.55, k)
            st["tL"] = st["tR"] = lerp(st["tL"], 12, k)
            st["on"] = max(st["on"], k)
        L = L_(15)                                   # "...Of course they do." - dry, then slightly impressed (eyes open up)
        if L:
            k = win(t, L["t0"] - 0.1, L["t1"] + 1.0, 0.1, 0.2)
            blend("skeptical", k * (1 - cl((t - L["words"][-1]["t0"]) / 0.3)))
            st["scale"] = lerp(st["scale"], 1.12, k * cl((t - L["words"][-1]["t0"]) / 0.3))
    else:
        L = L_(1)
        if L:
            blend("curious", win(t, L["t0"], L["t1"], 0.15, 0.3))
        L = L_(2)                                    # "My bumper!" - excited arcs
        if L:
            blend("excited", win(t, L["t0"], L["t1"], 0.08, 0.25))
        L = L_(5)
        if L:
            blend("impatient", win(t, L["t0"], L["t1"], 0.1, 0.3))
        L = L_(7)                                    # impatient: quick double blink, then narrowed
        if L:
            k = win(t, L["t0"], L["t1"], 0.05, 0.3)
            blend("impatient", k)
            for b0 in (L["t0"], L["t0"] + 0.24):
                bu = (t - b0) / 0.12
                if 0 <= bu < 1:
                    st["fL"] = st["fR"] = max(st["fL"], 1 - abs(2 * bu - 1))
        L = L_(8)                                    # deflated when nothing printed: flat cut
        if L:
            k = win(t, L["t1"] - 0.2, L["t1"] + 0.9, 0.15, 0.3)
            st["fL"] = st["fR"] = lerp(st["fL"], 0.6, k)
        L = L_(12)
        if L:
            blend("curious", win(t, L["t0"], L["t1"] + 0.6, 0.15, 0.3))
        L = L_(14)                                   # pop to surprised on "Ooh!", then excited arcs
        if L:
            tw = L["words"][0]["t0"]
            if t >= tw - 0.03:
                pop = eback((t - tw + 0.03) / 0.2, 2.2)
                k = win(t, tw, L["words"][0]["t1"] + 0.15, 0.03, 0.2)
                st["scale"] = lerp(1.0, 1.3, k) * (0.92 + 0.08 * pop)
            blend("excited", win(t, L["words"][1]["t0"], L["t1"] + 0.3, 0.08, 0.25))
    return st



EYE_TILT_GAIN, EYE_TILT_MAX, CUT_MIN = 1.35, 24.0, 0.4   # v6: annoyed/worried must separate at phone size


def apply_expr(ch, lid_call=0.0, look_call=(0, 0)):
    st = expr_state(ch, CUR_T)
    if NO_BROWS:
        # the brow tilt becomes the tilt of the eye's flat cut: > 0 inner side lower (annoyed), < 0 inner side up (worried);
        # a tilted state always cuts at least CUT_MIN of the dot so the shape reads; shaped eyes 1.1x
        for key, fk in (("tL", "fL"), ("tR", "fR")):
            if abs(st[key]) > 4 and st[fk] > 0.08:
                st[fk] = max(st[fk], CUT_MIN * min(1.0, abs(st[key]) / 12.0))
    fl, fr = max(lid_call, st["fL"]), max(lid_call, st["fR"])
    shaped = bool(st["shape"]) or max(fl, fr) > 0.08
    sc = st["scale"] * (1.1 if (NO_BROWS and shaped and st["scale"] < 1.05) else 1.0)
    if st["shape"]:
        set_eyes(ch, 0, 0, shape=st["shape"], scale=sc)
    else:
        set_eyes(ch, fl, fr, scale=sc)
    for e, sx, t, f in zip(ch.eyeset, (1, -1), (st["tL"], st["tR"]), (fl, fr)):
        ang = 0.0
        if NO_BROWS and not st["shape"] and 0.08 < f < 0.9:
            ang = max(-EYE_TILT_MAX, min(EYE_TILT_MAX, EYE_TILT_GAIN * t))
        e["piv"].rotation_euler = (0, math.radians(-sx * ang), 0)
    hmax = 0.008 if ch is PIP else 0.04      # Pip's cap edge sits just above his brows: keep raised brows in view
    set_brows(ch, st["on"], min(st["hL"], hmax), min(st["hR"], hmax), st["tL"], st["tR"])
    if st["roll"] is not None:
        ch.eyes_g.location = (st["roll"][0] * ch.S["eye_look"] * 1.3, 0, ch.head_c + st["roll"][1] * ch.S["eye_look"] * 1.3)
    if ch is GUS and SIGH_DEFLATE:                                 # v4 only: sighs deflate his whole body
        e = sigh_env(CUR_T)
        if e > 0:
            ch.torso.scale = (ch.torso.scale[0] * (1 + 0.05 * e), ch.torso.scale[1] * (1 + 0.05 * e), ch.torso.scale[2] * (1 - 0.09 * e))
            ch.neck.location.z -= ch.S["body_h"] * 0.09 * e
            rx, ry, rz_ = ch.neck.rotation_euler
            ch.neck.rotation_euler = (rx + math.radians(14 * e), ry, rz_)
            hx, hy, hz_ = ch.hips.rotation_euler
            ch.hips.rotation_euler = (hx + math.radians(5 * e), hy, hz_)
            for sd in ("L", "R"):
                ex_, ey_, ez_ = ch.elbows[sd].rotation_euler
                ch.elbows[sd].rotation_euler = (ex_ + math.radians(22 * e), ey_, ez_)


_pose_base = pose


def pose(ch, *a, **kw):
    _pose_base(ch, *a, **kw)
    apply_expr(ch, max(ch.S.get("base_lid", 0.0), kw.get("lid", 0.0)), kw.get("look", (0, 0)))




# ================================================== Ep 4 props ==================================================
import numpy as _np

PAL.update(plate="#46564b", printer="#2b2e2b", pipb="#619f73", wire="#7d837d", paper="#f4f4ef", ink="#1d201d",
           scan2="#c2c7c2")
EDGE = float(arg("--edge", "0.075"))     # scan triangle edge length (m): "a mesh of tiny triangles"

# the scene's own laptop screen (pilot puzzle UI) is replaced by Ep 4's screens
for _o in list(UI.children_recursive):
    bpy.data.objects.remove(_o, do_unlink=True)
LAPTOP.location = (3.0, 3.05, 0.955)
CLOCK.location = (1.45, 3.56, 2.62)          # wall left of the pegboard, so it sits in the bench shots


def rrect(cy, cz, hy, hz, r, n=6):
    """Rounded rectangle in the (y, z) plane, closed loop starting at the top centre, clockwise seen from +x."""
    pts = [(0.0, cz + hz)]
    for (sy, sz, a0) in ((1, 1, 90), (1, -1, 0), (-1, -1, 270), (-1, 1, 180)):
        ccy, ccz = cy + sy * (hy - r), cz + sz * (hz - r)
        for k in range(n + 1):
            a = math.radians(a0 - 90 * k / n)
            pts.append((ccy + r * math.cos(a), ccz + r * math.sin(a)))
    pts.append((0.0, cz + hz))
    return pts


def curve_obj(name, pts, depth=0.008, m=None, k=1.0):
    """Poly curve with a round bevel, drawn on to fraction k (bevel_factor_end)."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = depth
    cu.bevel_resolution = 3
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p_, q in zip(sp.points, pts):
        p_.co = (q[0], q[1], q[2], 1.0)
    try:
        cu.bevel_factor_mapping_end = "SPLINE"
    except Exception:
        pass
    cu.bevel_factor_end = max(0.001, min(1.0, k))
    ob = bpy.data.objects.new(name, cu)
    COLL.objects.link(ob)
    ob.data.materials.append(m or emit("sage_l", 2.2))
    return ob


def path_len_point(pts, k):
    """Point at fraction k of a polyline's length."""
    P = [Vector(p) for p in pts]
    L = [0.0]
    for a, b in zip(P, P[1:]):
        L.append(L[-1] + (b - a).length)
    want = cl(k) * L[-1]
    for i in range(1, len(P)):
        if L[i] >= want:
            f = (want - L[i - 1]) / max(1e-9, L[i] - L[i - 1])
            return P[i - 1].lerp(P[i], f)
    return P[-1]


# ---------------------------------------------------------------------------------------------------------- printer
def build_printer(loc=(4.05, 3.15, 0.955)):
    g = empty("PRINTER", SHOP, loc)
    box("pr_base", (0.52, 0.46, 0.07), (0, 0, 0.035), mat("printer"), g, 0.012, 0.012)
    box("pr_disp", (0.12, 0.006, 0.035), (0.14, -0.232, 0.036), emit("#3d5d47", 1.0), g, 0.004)
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(f"pr_post{sx}{sy}", (0.035, 0.035, 0.56), (sx * 0.24, sy * 0.21, 0.07 + 0.28), mat("metal"), g, 0.006, 0.01)
    for sy in (-1, 1):
        box(f"pr_topy{sy}", (0.52, 0.035, 0.035), (0, sy * 0.21, 0.645), mat("metal"), g, 0.006, 0.01)
    for sx in (-1, 1):
        box(f"pr_topx{sx}", (0.035, 0.46, 0.035), (sx * 0.24, 0, 0.645), mat("metal"), g, 0.006, 0.01)
    box("pr_gantry", (0.48, 0.03, 0.03), (0, 0.02, 0.47), mat("metal"), g, 0.006, 0.01)
    box("pr_head", (0.085, 0.075, 0.09), (0.05, 0.0, 0.44), mat("sage"), g, 0.012, 0.01)
    cyl("pr_nozzle", 0.014, 0.04, (0.05, 0.0, 0.377), mat("dark"), g, r2=0.004)
    box("pr_carrier", (0.42, 0.4, 0.02), (0, 0, 0.15), mat("printer"), g, 0.004, 0.008)
    cyl("pr_spool", 0.11, 0.065, (0.31, 0.06, 0.42), mat("sage_l"), g, axis="X", bevel=0.01, ol=0.01)
    cyl("pr_spoolhub", 0.035, 0.07, (0.31, 0.06, 0.42), mat("dark"), g, axis="X")
    plate = empty("PLATE", g, (0, 0, 0.166))
    box("pl_plate", (0.38, 0.36, 0.012), (0, 0, 0), mat("plate"), plate, 0.004, 0.01)
    box("pl_tab", (0.08, 0.03, 0.006), (0, -0.19, 0), mat("plate"), plate, 0.004, 0.006)
    return g, plate


PRINTER, PLATE = build_printer()
PLATE_HOME = Vector((0, 0, 0.166))
BED_W = Vector((4.05, 3.15, 0.955)) + PLATE_HOME + Vector((0, 0, 0.007))   # world point on the plate's top


# ---------------------------------------------------------------------------------------------------------- shelf
def build_shelf():
    g = empty("SHELF", SHOP, (5.3, 3.47, 1.12))
    box("sh_plank", (0.9, 0.26, 0.032), (0, 0, 0), mat("wood"), g, 0.006, 0.012)
    for sx in (-1, 1):
        box(f"sh_br{sx}", (0.03, 0.2, 0.14), (sx * 0.33, 0.02, -0.085), mat("dark"), g, 0.004, 0.008)
    # Ep 1's failed print: a tangle of spaghetti filament
    rng = random.Random(9)
    pts, p = [], Vector((0, 0, 0.06))
    d = Vector((1, 0, 0))
    for i in range(90):
        d = (d + Vector((rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9), rng.uniform(-0.7, 0.7)))).normalized()
        p = p + d * 0.022
        p = Vector((cl(p.x, -0.12, 0.12), cl(p.y, -0.09, 0.09), cl(p.z, 0.012, 0.13)))
        pts.append((p.x - 0.18, p.y, p.z + 0.016))
    sp = curve_obj("spaghetti", pts, 0.0055, mat("sage_l"))
    sp.parent = g
    return g


SHELF = build_shelf()
PLATE_SHELF = (Vector((5.52, 3.52, 1.325)), (-74.0, 0.0, 4.0))   # leaning on the wall, next to the spaghetti


# ---------------------------------------------------------------------------------------------------------- Pip's sketch
def build_sketch():
    """Pip's bumper idea (from Ep 1): paper with a front-view line drawing. Lines only, no words."""
    g = empty("SKETCH", None, (2.72, 3.49, 2.02))
    box("sk_paper", (0.44, 0.004, 0.31), (0, 0, 0), mat("paper"), g, 0.0, 0.006)
    ink = emit("ink", 1.0)
    W_, H_ = 0.36, 0.13

    def ln(name, a, b, w=0.006):
        a, b = Vector((a[0], -0.004, a[1])), Vector((b[0], -0.004, b[1]))
        c = (a + b) / 2
        L = (b - a).length
        ang = math.degrees(math.atan2(b.z - a.z, b.x - a.x))
        box(name, (L + w, 0.002, w), c, ink, g, rot=(0, -ang, 0))

    # bumper outline
    cs = [(-W_ / 2, 0.035), (W_ / 2, 0.035), (W_ / 2 + 0.01, -0.05), (W_ / 2 - 0.03, -0.085), (-W_ / 2 + 0.03, -0.085),
          (-W_ / 2 - 0.01, -0.05), (-W_ / 2, 0.035)]
    for i in range(len(cs) - 1):
        ln(f"sk_o{i}", cs[i], cs[i + 1])
    ln("sk_lip", (-W_ / 2 - 0.02, -0.1), (W_ / 2 + 0.02, -0.1), 0.008)          # the splitter lip
    for i, (a, b) in enumerate((((-0.08, -0.02), (0.08, -0.02)), ((0.08, -0.02), (0.08, -0.06)), ((0.08, -0.06), (-0.08, -0.06)),
                                ((-0.08, -0.06), (-0.08, -0.02)))):
        ln(f"sk_in{i}", a, b, 0.005)                                              # centre intake
    for sx in (-1, 1):
        ln(f"sk_v{sx}a", (sx * 0.12, -0.005), (sx * 0.16, -0.055), 0.005)         # side vents
        ln(f"sk_v{sx}b", (sx * 0.145, 0.0), (sx * 0.175, -0.04), 0.005)
    # sage scribbles: an arrow at the lip and a star (excitement, no text)
    ln("sk_ar", (0.12, 0.11), (0.17, -0.07), 0.006)
    box("sk_star", (0.035, 0.002, 0.035), (-0.15, -0.004, 0.105), emit("sage", 1.0), g, rot=(0, 45, 0))
    box("sk_star2", (0.035, 0.002, 0.035), (-0.15, -0.005, 0.105), emit("sage", 1.0), g)
    for sx in (-1, 1):
        box(f"sk_tape{sx}", (0.07, 0.003, 0.025), (sx * 0.2, -0.003, 0.155), mat("#e3dccb"), g, rot=(0, sx * 30, 0))
    return g


SKETCH = build_sketch()
SKETCH_HOME = (Vector((2.72, 3.49, 2.02)), (0, 0, 0))


# ---------------------------------------------------------------------------------------------------------- the scan
def build_scan():
    """Triangulated 'scan' of the cartoon car: the car's own surfaces (outline shells off), merged, subdivided until no edge is
    longer than EDGE, triangulated, with a hair of scanner noise. Fill and wire share one mesh (a ripple moves both)."""
    keep = ("car_body", "car_cabin", "win_", "windshield", "rearglass", "tyre_", "hub_", "headl_", "taill_", "mirror_", "grille")
    obs = [o for o in CAR.children if o.type == "MESH" and o.name.startswith(keep)]
    for o in obs:
        for m in o.modifiers:
            if m.type == "SOLIDIFY":
                m.show_render = m.show_viewport = False
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    for o in obs:
        oe = o.evaluated_get(dg)
        me = bpy.data.meshes.new_from_object(oe)
        me.transform(o.matrix_world)
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)
    for o in obs:
        for m in o.modifiers:
            if m.type == "SOLIDIFY":
                m.show_render = m.show_viewport = True
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    for it in range(10):
        long = [e for e in bm.edges if e.calc_length() > EDGE]
        if not long:
            break
        bmesh.ops.subdivide_edges(bm, edges=long, cuts=1, use_grid_fill=False)
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3])
    rng = random.Random(3)
    bm.normal_update()
    for v in bm.verts:
        v.co += v.normal * rng.uniform(-0.0012, 0.0012)
    g = empty("SCAN")
    fill = new_obj("scan_fill", bm, [mat("scan"), OUTLINE, mat("wire")], g)
    wire = bpy.data.objects.new("scan_wire", fill.data)
    COLL.objects.link(wire)
    wire.parent = g
    wf = wire.modifiers.new("wf", "WIREFRAME")
    wf.thickness = 0.0032
    wf.use_replace = True
    wf.use_even_offset = True
    wf.offset = 1.0
    wf.material_offset = 2
    me = fill.data
    n = len(me.vertices)
    base = _np.zeros(n * 3, _np.float32)
    nrm = _np.zeros(n * 3, _np.float32)
    me.vertices.foreach_get("co", base)
    me.vertices.foreach_get("normal", nrm)
    print(f"[ep4] scan: {len(me.polygons)} triangles, {n} verts", flush=True)
    return g, fill, wire, base.reshape(-1, 3), nrm.reshape(-1, 3)


SCAN, SCAN_FILL, SCAN_WIRE, SCAN_BASE, SCAN_NRM = build_scan()


def scan_ripple(center, t_since, amp=0.035):
    """Cling-film wobble: a decaying ring wave from `center` (world, scan at full size at the origin)."""
    me = SCAN_FILL.data
    if t_since is None or t_since < 0:
        co = SCAN_BASE
    else:
        d = _np.linalg.norm(SCAN_BASE - _np.array(center, _np.float32), axis=1)
        env = _np.exp(-d / 0.45) * math.exp(-t_since / 0.55)
        wave = _np.sin(d * 26.0 - t_since * 34.0) * (d < t_since * 1.35 + 0.02)
        co = SCAN_BASE + SCAN_NRM * (amp * env * wave)[:, None]
    me.vertices.foreach_set("co", co.astype(_np.float32).ravel())
    me.update()


def place_scan(loc=(0, 0, 0), s=1.0, rz=0.0):
    set_vis(SCAN, True)
    SCAN.location = loc
    SCAN.scale = (s, s, s)
    SCAN.rotation_euler = (0, 0, math.radians(rz))


# ---------------------------------------------------------------------------------------------------------- bumpers
def build_stock():
    g = empty("STOCKB")
    box("sb_main", (0.36, 1.74, 0.31), (1.9, 0, 0.455), mat("car"), g, 0.06, 0.02)
    box("sb_slot", (0.02, 0.62, 0.06), (2.082, 0, 0.4), mat("dark"), g, 0.01)
    box("sb_line", (0.02, 1.5, 0.014), (2.082, 0, 0.535), mat("black"), g)
    return g


def build_pipb():
    g = empty("PIPB")
    box("pb_main", (0.44, 1.78, 0.34), (1.93, 0, 0.455), mat("pipb"), g, 0.07, 0.02)
    box("pb_lip", (0.2, 1.74, 0.032), (2.1, 0, 0.29), mat("black"), g, 0.01, 0.014)
    box("pb_intake", (0.03, 0.8, 0.13), (2.143, 0, 0.42), mat("dark"), g, 0.02, 0.01)
    for sx in (-1, 1):
        box(f"pb_vent{sx}", (0.03, 0.22, 0.17), (2.13, sx * 0.62, 0.45), mat("dark"), g, 0.02, 0.01, rot=(sx * 14, 0, 0))
        box(f"pb_canard{sx}", (0.14, 0.05, 0.022), (2.1, sx * 0.84, 0.52), mat("black"), g, 0.006, 0.01, rot=(0, -8, 0))
    return g


STOCKB = build_stock()
PIPB = build_pipb()
STOCK_TRACE = [(2.095, y, z) for y, z in rrect(0.0, 0.455, 0.86, 0.15, 0.06)]
PIPB_TRACE = [(2.16, y, z) for y, z in rrect(0.0, 0.455, 0.88, 0.165, 0.07)] + \
             [(2.2, 0.0, 0.29), (2.2, -0.87, 0.29), (2.2, 0.87, 0.29)]


def pop_group(g, k, base_loc=(0, 0, 0), anchor=(2.0, 0.0, 0.45)):
    """Scale a bumper group in about its front-centre anchor: k 0 -> invisible, 1 -> full; eback overshoot gives the snap."""
    if k <= 0.001:
        set_vis(g, False)
        return
    set_vis(g, True)
    a = Vector(anchor)
    g.scale = (k, k, k)
    g.location = a - a * k + Vector(base_loc)


# ---------------------------------------------------------------------------------------------------------- laptop screens
SW, SH = 0.205, 0.135


def _car_inside(x, z):
    c = CAB
    if -2.0 <= x <= 2.0 and 0.32 <= z <= 0.98:
        return True
    if c["z0"] <= z <= c["z1"]:
        t = (z - c["z0"]) / (c["z1"] - c["z0"])
        return c["xb0"] + (c["xt0"] - c["xb0"]) * t <= x <= c["xb1"] + (c["xt1"] - c["xb1"]) * t
    return any((x - wx) ** 2 + (z - 0.36) ** 2 <= 0.36 ** 2 for wx in (-1.3, 1.3))


def build_ui_scan():
    """Screen 1: the finished scan - a side-view car made of small grey triangles on the dark viewer background."""
    g = empty("UI_SCAN", UI)
    poly("us_bg", [(-SW, -SH), (SW, -SH), (SW, SH), (-SW, SH)], emit("#141614", 1.0), g, loc=(0, 0, 0))
    poly("us_bar", [(-SW, 0.118), (SW, 0.118), (SW, SH), (-SW, SH)], emit("#2a2d2a", 1.0), g, loc=(0, 0, 0.0005))
    bm = bmesh.new()
    s, oz, st = 0.085, -0.075, 0.11
    for i in range(-20, 20):
        for j in range(0, 15):
            x0, z0 = i * st, j * st
            for tri, mi in ((((x0, z0), (x0 + st, z0), (x0, z0 + st)), 0), (((x0 + st, z0), (x0 + st, z0 + st), (x0, z0 + st)), 1)):
                cx = sum(p[0] for p in tri) / 3
                cz = sum(p[1] for p in tri) / 3
                if _car_inside(cx, cz):
                    vs = [bm.verts.new((p[0] * s, p[1] * s + oz, 0.0)) for p in tri]
                    f = bm.faces.new(vs)
                    f.material_index = (mi + (i + j) % 2) % 2
    tri_ob = new_obj("us_tris", bm, [emit("scan", 1.0), emit("scan2", 1.0)], g, loc=(0, 0, 0.001))
    # thin dark gaps between triangles: same triangles, slightly shrunk, over a dark base of the full silhouette
    return g


def build_ui_slicer():
    """Screen 2: a slicer-like view (no brand, no text): a build plate in perspective with a grid, a tiny print head."""
    g = empty("UI_SLICE", UI)
    poly("ul_bg", [(-SW, -SH), (SW, -SH), (SW, SH), (-SW, SH)], emit("#171a18", 1.0), g, loc=(0, 0, 0))
    poly("ul_bar", [(-SW, 0.118), (SW, 0.118), (SW, SH), (-SW, SH)], emit("#2a2d2a", 1.0), g, loc=(0, 0, 0.0005))
    # plate trapezoid
    bl, br, tr, tl = (-0.15, -0.105), (0.15, -0.105), (0.105, 0.0), (-0.105, 0.0)
    poly("ul_plate", [bl, br, tr, tl], emit("plate", 1.0), g, loc=(0, 0, 0.001))
    gm = emit("sage_l", 0.7)
    for k in range(1, 8):
        u = k / 8
        a = (bl[0] + (tl[0] - bl[0]) * u, bl[1] + (tl[1] - bl[1]) * u)
        b = (br[0] + (tr[0] - br[0]) * u, br[1] + (tr[1] - br[1]) * u)
        poly(f"ul_h{k}", [(a[0], a[1] - 0.0008), (b[0], b[1] - 0.0008), (b[0], b[1] + 0.0008), (a[0], a[1] + 0.0008)], gm, g,
             loc=(0, 0, 0.0015))
        a = (bl[0] + (br[0] - bl[0]) * u, bl[1])
        b = (tl[0] + (tr[0] - tl[0]) * u, tl[1])
        poly(f"ul_v{k}", [(a[0] - 0.0009, a[1]), (a[0] + 0.0009, a[1]), (b[0] + 0.0009, b[1]), (b[0] - 0.0009, b[1])], gm, g,
             loc=(0, 0, 0.0015))
    poly("ul_head", [(-0.012, 0.05), (0.012, 0.05), (0.006, 0.03), (-0.006, 0.03)], emit("sage", 1.0), g, loc=(0, 0, 0.0015))
    return g


UI_SCAN = build_ui_scan()
UI_SLICE = build_ui_slicer()


def ui_ghost(k_drop, alpha):
    """The scan dropped into the slicer: a car outline that falls onto the plate and fades away (nothing to slice)."""
    if alpha <= 0.02:
        return
    a = round(alpha * 10) / 10
    m = emit("scan", 1.0, a)
    s = 0.05
    oz = lerp(0.07, -0.06, eout(k_drop))
    sil = [(-2.0, 0.32), (2.0, 0.32), (2.0, 0.98), (1.0, 0.98), (0.48, 1.5), (-0.72, 1.5), (-1.15, 0.98), (-2.0, 0.98), (-2.0, 0.32)]
    for i in range(len(sil) - 1):
        (x0, z0), (x1, z1) = sil[i], sil[i + 1]
        dx, dz = x1 - x0, z1 - z0
        L = math.hypot(dx, dz)
        nx, nz = -dz / L * 0.03, dx / L * 0.03
        temp(poly(f"ug{i}", [((x0 - nx) * s, (z0 - nz) * s + oz), ((x1 - nx) * s, (z1 - nz) * s + oz),
                             ((x1 + nx) * s, (z1 + nz) * s + oz), ((x0 + nx) * s, (z0 + nz) * s + oz)], m, UI, loc=(0, 0, 0.003)))


def screen(name):
    set_vis(UI_SCAN, name == "scan")
    set_vis(UI_SLICE, name == "slicer")


# ---------------------------------------------------------------------------------------------------------- sparkles
def sparkle(name, p, s=1.0, rot=0.0):
    g = temp(empty(name, None, p, (0, 0, 0)))
    m = emit("white", 1.6)
    box(name + "a", (0.075 * s, 0.006, 0.012 * s), (0, 0, 0), m, g, rot=(0, rot, 0))
    box(name + "b", (0.012 * s, 0.006, 0.075 * s), (0, 0, 0), m, g, rot=(0, rot, 0))
    return g


def face_to(g, cam_loc):
    d = Vector(cam_loc) - g.matrix_world.translation
    g.rotation_euler = (-d).to_track_quat("Y", "Z").to_euler()


# ================================================== Ep 4 shots ==================================================
STOOL_TOP = 0.625     # Pip's root z standing on the stool (seat top 0.61 + foot radius)


def prog(fr, sh):
    f0, f1 = SF[sh]
    return (fr - f0) / max(1, f1 - 1 - f0)


def cam_push(loc, target, lens, k, up=(0, 0, 1)):
    loc, target = Vector(loc), Vector(target)
    look(cam, target + (loc - target) * (1 - k), target, lens, up=up)


def talkpose(ch, spk, t, base_lid=0.0, **kw):
    m, lid = talk(spk, t, base_lid)
    acc = accent(spk, t)
    h = kw.pop("head", (0, 0, 0))
    pose(ch, head=(h[0] + 5 * acc, h[1], h[2]), mouth=m, lid=lid, **kw)


def L0(n):
    return LN[n]["t0"]


def L1(n):
    return LN[n]["t1"]


def W(n, i):
    return LN[n]["words"][i]


def pip_on_stool(loc_xy, rz, t, **kw):
    set_vis(STOOL, True)
    STOOL.location = (loc_xy[0], loc_xy[1], 0)
    hop = kw.pop("hop", 0.0)
    talkpose(PIP, "PIP", t, loc=(loc_xy[0], loc_xy[1], STOOL_TOP + hop), rz=rz, **kw)


def anim_E1(fr):
    """'OK, it's scanned. Can we print it now?' - the finished scan on the laptop; Pip bounces on the stool beside it."""
    t, u = fr / FPS, prog(fr, "E1")
    screen("scan")
    sp = L0(1) - 0.05 <= t <= L1(1) + 0.1
    hop = 0.045 * abs(math.sin(math.pi * (t - L0(1)) * 2.2)) if sp else 0.0
    pip_on_stool((2.42, 2.45), 28, t, hop=hop, hips=(-4, 0, 0), head=(-10, 0, 6 * math.sin(t * 4)),
                 armL=(-40, 0, 10), armR=(-115 + 12 * math.sin(t * 9), 30, 0), elbowL=-30, elbowR=-30,
                 look=(0.7, 0.2))
    turn = ease((t - L0(1) - 0.5) / 0.9)
    talkpose(GUS, "GUS", t, 0.0, loc=(3.62, 2.42, 0), rz=lerp(-160, -35, turn), head=(4, 0, 0), armL=(-30, 0, 6),
             armR=(-30, 0, -6), elbowL=-35, elbowR=-35, look=lerpv((0, 0), (-0.7, 0.1), turn))
    cam_push((3.05, -0.45, 1.75), (3.02, 2.8, 1.22), 28, 0.08 * ease(u))


def mini_path_e2(t):
    """Mini scan pops out of the laptop screen on 'Print', arcs onto the printer bed by the end of the line."""
    ta, tb = W(2, 2)["t0"] - 0.05, L1(2) + 0.05
    k = cl((t - ta) / max(0.3, tb - ta))
    a = LAPTOP.matrix_world @ Vector((0, 0.16, 0.2))
    b = BED_W.copy()
    p = a.lerp(b, ease(k)) + Vector((0, -0.12 * math.sin(math.pi * k), 0.32 * math.sin(math.pi * k)))
    s = lerp(0.03, 0.085, eout(k * 1.6)) + 0.04 * math.sin(math.pi * k)
    return k, p, s


def anim_E2(fr):
    """'My bumper! Print my bumper!' - Pip points at her sketch, then shoves the scan from the laptop onto the printer."""
    t, u = fr / FPS, prog(fr, "E2")
    screen("scan")
    k, p, s = mini_path_e2(t)
    if t >= W(2, 2)["t0"] - 0.05:
        place_scan(p, s, rz=-8)
    pt = win(t, L0(2), W(2, 1)["t1"] + 0.1, 0.12, 0.25)          # points up at the sketch on "My bumper!"
    pip_on_stool((2.42, 2.55), lerp(28, 10, pt), t, hop=0.03 * pt, hips=(-6, 0, 0), head=(lerp(-8, -30, pt), 0, lerp(0, -10, pt)),
                 armL=(-30, 0, 10), armR=(-30, 0, -10), elbowL=-30, elbowR=-30, look=lerpv((0.6, 0.1), (-0.2, 1.0), pt))
    bpy.context.view_layer.update()
    if pt > 0.02:
        aim_arm(PIP, "R", Vector((2.72, 3.4, 2.0)).lerp(PIP.hands["R"].matrix_world.translation, 1 - pt))
    if t >= W(2, 2)["t0"] - 0.2 and k < 0.98:                        # the shove follows the mini scan
        aim_arm(PIP, "L", p + Vector((-0.12, -0.15, 0.0)))
    talkpose(GUS, "GUS", t, 0.0, loc=(4.72, 2.5, 0), rz=-40 + 10 * ease(k), head=(8, 0, 0), armL=(-30, 0, 6),
             armR=(-30, 0, -6), elbowL=-35, elbowR=-35, look=lerpv((-0.8, 0.1), (-0.5, 0.3), ease(k)))
    look(cam, (3.45, -0.75, 1.75), (3.45, 3.0, 1.28), 26)


def anim_E3(fr):
    """'That's a scan. It's a skin.' - Gus plucks the scan off the bed and tosses it into the bay, where it grows full size."""
    t, u = fr / FPS, prog(fr, "E3")
    screen("scan")
    ta = L0(3) - 0.1
    tb = W(3, 2)["t1"] + 0.6
    k = cl((t - ta) / (tb - ta))
    a = BED_W.copy()
    b = Vector((0, 0, 0))
    if k < 0.18:
        p, s = a + Vector((0, -0.15, 0.25)) * ease(k / 0.18), 0.085
    else:
        kk = (k - 0.18) / 0.82
        a2 = a + Vector((0, -0.15, 0.25))
        p = a2.lerp(b, ease(kk)) + Vector((0, 0, 1.6 * math.sin(math.pi * kk)))
        s = lerp(0.085, 1.0, eback(kk, 1.2))
    place_scan(p, s, rz=-8 * (1 - ease(k)))
    talkpose(GUS, "GUS", t, 0.0, loc=(3.95, 2.35, 0), rz=lerp(170, -60, ease((k - 0.15) / 0.5)), head=(6, 0, 0),
             armL=(-30, 0, 6), armR=(-30, 0, -6), elbowL=-30, elbowR=-30, look=(-0.6, 0.0))
    bpy.context.view_layer.update()
    if k < 0.3:
        aim_arm(GUS, "R", p + Vector((0.0, -0.08, 0.06)))
    pip_on_stool((2.42, 2.55), lerp(10, -40, ease(k)), t, head=(-10, 0, 0), armL=(-30, 0, 10), armR=(-30, 0, -10),
                 elbowL=-30, elbowR=-30, look=lerpv((0.8, 0.2), (-0.9, -0.1), ease(k)))
    look(cam, (1.6, -4.9, 2.1), (1.7, 1.0, 1.4), 20)


def anim_E4(fr):
    """'A mesh of tiny triangles. No thickness.' - push in on the scan's skin; Gus flicks it and it wobbles like cling film."""
    t, u = fr / FPS, prog(fr, "E4")
    screen("scan")
    place_scan((0, 0, 0), 1.0)
    flick_t = W(4, 5)["t0"] - 0.05                                   # "No thickness."
    centre = Vector((1.15, -0.86, 0.72))
    scan_ripple(centre, t - flick_t)
    m, lid = talk("GUS", t, 0.0)
    pose(GUS, loc=(0.5, -1.4, 0), rz=140, hips=(4, 0, 0), head=(8 + 5 * accent("GUS", t), 0, 0), armL=(-30, 0, 6),
         armR=(-30, 0, -6), elbowL=-30, elbowR=-30, mouth=m, lid=lid, look=(0.3, -0.3))
    bpy.context.view_layer.update()
    # the flick: hand draws back, then snaps to the surface and away
    ph = (t - flick_t) / 0.35
    rest = centre + Vector((0.12, -0.32, 0.05))
    hit = centre + Vector((0.0, -0.03, 0.0))
    if -1.2 <= ph <= 1.5:
        tgt = rest.lerp(hit, ease(ph + 0.6) if ph < 0 else 1 - ease((ph - 0.2) / 1.0)) if ph < 1.5 else rest
        aim_arm(GUS, "L", tgt)
    pose(PIP, loc=(30, 30, 0))
    cam_push((2.25, -2.75, 1.1), (1.22, -0.86, 0.74), 46, 0.45 * ease(u))


def anim_E5(fr):
    """'So... print it anyway?' / 'Sure.' - Pip nudges the printer; Gus drops the scan into the slicer: an empty plate."""
    t, u = fr / FPS, prog(fr, "E5")
    tdrop = W(6, 0)["t1"] + 0.05
    screen("scan" if t < tdrop - 0.1 else "slicer")
    if t >= tdrop - 0.1:
        kd = cl((t - tdrop) / 0.5)
        ui_ghost(kd, 1.0 - cl((t - tdrop - 0.45) / 0.6))
    nudge = math.sin(math.pi * cl((t - W(5, 1)["t0"]) / 0.45)) if t >= W(5, 1)["t0"] else 0.0
    pip_on_stool((4.62, 2.5), -40, t, head=(-6, 0, 0), armL=(-30, 0, 10), armR=(-30, 0, -10), elbowL=-30, elbowR=-30,
                 look=(-0.4, 0.3))
    bpy.context.view_layer.update()
    if nudge > 0.01:
        aim_arm(PIP, "R", Vector((4.3, 3.0, 1.25)) + Vector((-0.04, 0, 0)) * nudge)
        PRINTER.location = (4.05 - 0.008 * nudge, 3.15, 0.955)
    else:
        PRINTER.location = (4.05, 3.15, 0.955)
    shrug = win(t, W(6, 0)["t0"] - 0.1, W(6, 0)["t1"] + 0.1, 0.12, 0.3)
    talkpose(GUS, "GUS", t, 0.0, loc=(2.42, 2.45, 0), rz=lerp(-25, -10, shrug), hips=(0, 0, 0), head=(lerp(4, -6, shrug), 0, 0),
             armL=(lerp(-45, -80, shrug), 0, lerp(6, 40, shrug)), armR=(lerp(-45, -80, shrug), 0, lerp(-6, -40, shrug)),
             elbowL=-40, elbowR=-40, look=lerpv((0.8, 0.0), (0.3, 0.2), shrug))
    if t >= tdrop - 0.4 and shrug < 0.5:
        bpy.context.view_layer.update()
        aim_arm(GUS, "R", LAPTOP.matrix_world @ Vector((0.05, -0.03, 0.05)))   # a tap on the keys
    look(cam, (3.5, -0.55, 1.75), (3.5, 3.0, 1.25), 26)


def anim_E6(fr):
    """'Is it done yet?' - Pip slumped on the stool in front of the (silent) printer; the clock spins like a fan."""
    t, u = fr / FPS, prog(fr, "E6")
    f0, f1 = SF["E6"]
    n = f1 - f0
    screen("slicer")
    am = 150 + 360 * (0.4 * u + 2.4 * u * u)
    asec = 260 + 360 * (2.0 * u + 8.0 * u * u)
    HANDS["minute"].rotation_euler = (0, math.radians(am), 0)
    HANDS["second"].rotation_euler = (0, math.radians(asec), 0)
    HANDS["hour"].rotation_euler = (0, math.radians(300 + (am - 150) / 12), 0)
    wm = 360 * (0.4 + 4.8 * u) / n
    ws = 360 * (2.0 + 16.0 * u) / n
    for nm, L_l, w_, key, y, cnt, wv in (("minute", 0.33, 0.028, "black", -0.07, 8, wm), ("second", 0.36, 0.014, "sage", -0.078, 10, ws)):
        if wv < 6:
            continue
        step = min(wv, 300) / cnt
        for i in range(cnt):
            a = HANDS[nm].rotation_euler.y - math.radians(step * (i + 1))
            al = round(0.5 * (1 - i / cnt) * 20) / 20
            if al <= 0:
                continue
            piv = temp(empty(f"blur_{nm}{i}", CLOCK, (0, y - 0.0005 * i, 0), (0, math.degrees(a), 0)))
            box(f"blur_{nm}{i}m", (w_ * 1.6, 0.004, L_l), (0, 0, L_l / 2 - 0.04), mat(key, al), piv)
    if u > 0.3:
        r = 0.42
        for side in (1, -1):
            for j, rr in enumerate((r + 0.14, r + 0.24)):
                for k in range(7):
                    a = math.radians(side * (55 + 6 * k + 8 * j) + 4 * math.sin(fr * 2.1 + j))
                    temp(box(f"whirr{side}{j}{k}", (0.03, 0.01, 0.045), (rr * math.sin(a), -0.03, rr * math.cos(a)), mat("black"),
                             CLOCK, rot=(0, math.degrees(a) + 90, 0)))
    set_vis(STOOL, True)
    STOOL.location = (2.85, 1.95, 0)
    m, lid = talk("PIP", t, 0.35)
    pose(PIP, loc=(2.85, 1.93, 0.5425), rz=18, hips=(lerp(6, 12, ease(u)), 0, 0), head=(lerp(-8, -4, ease(u)), 0, -10),
         armL=(-38, 0, 14), elbowL=-50, armR=(-38, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=m, lid=lid,
         look=(0.9, 0.5))
    pose(GUS, loc=(30, 30, 0))
    look(cam, (2.7, -1.0, 1.45), (2.45, 3.0, 1.7), 26)


def anim_E7(fr):
    """'...There's nothing to print.' - Gus slides the empty build plate out and stands it on the failed-print shelf, next to
    Ep 1's spaghetti."""
    t, u = fr / FPS, prog(fr, "E7")
    screen("slicer")
    ta, tb = L0(8) - 0.1, L1(8) + 0.75
    k = cl((t - ta) / (tb - ta))
    home = PRINTER.matrix_world @ PLATE_HOME
    out = home + Vector((0.0, -0.32, 0.06))
    up = Vector((5.0, 3.05, 1.5))
    dest, drot = PLATE_SHELF
    if k < 0.3:
        p, rot = home.lerp(out, ease(k / 0.3)), (0, 0, 0)
    elif k < 0.75:
        kk = ease((k - 0.3) / 0.45)
        p = out.lerp(up, kk)
        rot = (lerp(0, -40, kk), 0, lerp(0, 4, kk))
    else:
        kk = eback((k - 0.75) / 0.25, 1.1)
        p = up.lerp(dest, kk)
        rot = (lerp(-40, drot[0], kk), 0, drot[2])
    PLATE.parent = None
    PLATE.location = p
    PLATE.rotation_euler = [math.radians(a) for a in rot]
    kb = ease((k - 0.8) / 0.2)                                    # steps back and turns to camera: deadpan reveal
    gx = lerp(lerp(4.15, 4.95, ease((k - 0.3) / 0.45)), 5.55, kb)
    gy = lerp(2.48, 2.0, kb)
    talkpose(GUS, "GUS", t, 0.0, loc=(gx, gy, 0.03 * math.sin(math.pi * cl((k - 0.3) / 0.45))), rz=lerp(160, 15, kb),
             head=(6, 0, 0), armL=(-30, 0, 6), armR=(-30, 0, -6), elbowL=-30, elbowR=-30, look=lerpv((0.0, 0.2), (-0.3, 0.0), kb))
    bpy.context.view_layer.update()
    if kb < 0.3:
        aim_arm(GUS, "L", p + Vector((-0.17, -0.05, 0.0)))
        aim_arm(GUS, "R", p + Vector((0.17, -0.05, 0.0)))
    # Pip deflates on the stool at the left edge
    set_vis(STOOL, True)
    STOOL.location = (3.55, 1.95, 0)
    m, lid = talk("PIP", t, 0.0)
    pose(PIP, loc=(3.55, 1.93, 0.5425), rz=-25, hips=(18, 0, 0), head=(10, 0, -12), armL=(-38, 0, 14), elbowL=-50,
         armR=(-38, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=m, lid=lid, look=(0.8, 0.5))
    look(cam, (4.95, -0.4, 1.55), (5.05, 3.2, 1.15), 27)


S8CAM = ((4.15, -2.85, 1.3), (2.05, -0.3, 0.62), 26)


def gus_at_front(t, look_=(-0.5, -0.2), **kw):
    talkpose(GUS, "GUS", t, 0.0, loc=(2.72, 0.4, 0), rz=kw.pop("rz", -80), head=(6, 0, 0), armL=(-30, 0, 6),
             armR=(-30, 0, -6), elbowL=-30, elbowR=-30, look=look_)


def anim_E8(fr):
    """'The scan is the reference. You can remake the original from it...' - Gus traces the stock bumper on the scan; a solid
    copy of the original pops out and clicks into place."""
    t, u = fr / FPS, prog(fr, "E8")
    screen("slicer")
    place_scan((0, 0, 0), 1.0)
    gus_at_front(t)
    bpy.context.view_layer.update()
    # 'The scan is the reference': open-hand gesture toward the scan
    g = win(t, L0(9), L1(9), 0.2, 0.3)
    if g > 0.01:
        aim_arm(GUS, "R", GUS.hands["R"].matrix_world.translation.lerp(Vector((2.1, -0.75, 0.8)), g))
    ta, tb = W(10, 2)["t0"], L1(10) - 0.15                              # trace from 'remake' to the end of the line
    k = cl((t - ta) / (tb - ta))
    if k > 0:
        temp(curve_obj("trace_stock", STOCK_TRACE, 0.009, emit("sage_l", 2.4), k))
        aim_arm(GUS, "L", path_len_point(STOCK_TRACE, k) + Vector((0.08, -0.06, 0.0)))
    kp = cl((t - (L1(10) - 0.15)) / 0.3)
    pop_group(STOCKB, eback(kp, 2.0) if kp > 0 else 0.0)
    if 0 < kp:
        sq = 1 + 0.06 * math.sin(math.pi * cl((t - (L1(10) + 0.05)) / 0.18))
        STOCKB.scale = (STOCKB.scale[0] * sq, STOCKB.scale[1], STOCKB.scale[2] / sq)
    pose(PIP, loc=(30, 30, 0))
    cam_push(*S8CAM[:2], S8CAM[2], 0.12 * ease(u))



def anim_E9(fr):
    """'...or design a new one on it.' - the copy slides off; Pip holds up her sketch; Gus draws her bumper over the scan and
    it snaps on ('click')."""
    t, u = fr / FPS, prog(fr, "E9")
    screen("slicer")
    place_scan((0, 0, 0), 1.0)
    ko = cl((t - SF["E9"][0] / FPS) / 0.35)                          # the stock copy slides away
    if ko < 1:
        pop_group(STOCKB, 1 - ease(ko), base_loc=(0.5 * ease(ko), -0.4 * ease(ko), 0))
    else:
        set_vis(STOCKB, False)
    gus_at_front(t, rz=-85)
    m, lid = talk("PIP", t, 0.0)
    pose(PIP, loc=(1.7, -1.5, 0), rz=-30, hips=(-4, 0, 0), head=(-10, 0, 0), armL=(-30, 0, 10), armR=(-30, 0, -10),
         elbowL=-30, elbowR=-30, mouth=m, lid=lid, look=(0.8, 0.2))
    bpy.context.view_layer.update()
    hp = aim_arm(PIP, "L", PIP.neck.matrix_world.translation + Vector((0.3, -0.2, 0.25)))
    attach(SKETCH, PIP.hands["L"], (0.02, -0.05, 0.2), (0, 0, -35))
    ta, tb = W(11, 1)["t0"] - 0.05, L1(11) - 0.05
    k = cl((t - ta) / (tb - ta))
    if k > 0:
        temp(curve_obj("trace_pipb", PIPB_TRACE, 0.01, emit("sage_l", 2.4), k))
        aim_arm(GUS, "L", path_len_point(PIPB_TRACE, k) + Vector((0.08, -0.06, 0.0)))
    tp = L1(11) - 0.05
    kp = cl((t - tp) / 0.28)
    pop_group(PIPB, eback(kp, 2.2) if kp > 0 else 0.0)
    if kp > 0:
        sq = 1 + 0.07 * math.sin(math.pi * cl((t - tp - 0.2) / 0.16))
        PIPB.scale = (PIPB.scale[0] * sq, PIPB.scale[1], PIPB.scale[2] / sq)
        if 0.2 < t - tp < 0.55:
            for i, (yy, zz) in enumerate(((-0.9, 0.62), (0.9, 0.62), (-0.95, 0.3))):
                sparkle(f"click{i}", (2.15, yy, zz), 0.9 + 0.4 * math.sin((t - tp) * 20 + i))
    cam_push(*S8CAM[:2], S8CAM[2], 0.12 + 0.1 * ease(u))


SEAM = [(2.12, y, 0.63) for y in (-0.9, -0.6, -0.3, 0.0, 0.3)]


def anim_E10(fr):
    """'So the scan is what makes it fit?' / 'Every curve.' - Pip peers along the seam; Gus runs a mitten along it, a sparkle
    follows."""
    t, u = fr / FPS, prog(fr, "E10")
    screen("slicer")
    place_scan((0, 0, 0), 1.0)
    pop_group(PIPB, 1.0)
    m, lid = talk("PIP", t, 0.0)
    pose(PIP, loc=(1.62, -1.22, 0), rz=70, hips=(22, 0, 0), head=(14, 0, 0), armL=(-50, 0, 10), armR=(-50, 0, -10),
         elbowL=-40, elbowR=-40, mouth=m, lid=lid, look=(0.6, -0.4))
    ta, tb = W(13, 0)["t0"] - 0.1, L1(13) + 0.2
    k = cl((t - ta) / (tb - ta))
    talkpose(GUS, "GUS", t, 0.0, loc=(2.85, 0.35, 0), rz=-100, head=(10, 0, 0), armL=(-30, 0, 6), armR=(-30, 0, -6),
             elbowL=-30, elbowR=-30, look=(0.0, -0.4))
    bpy.context.view_layer.update()
    if k > 0:
        p = path_len_point(SEAM, k)
        aim_arm(GUS, "R", p + Vector((0.06, 0, 0.07)))
        for i in range(4):
            kk = k - 0.06 * i
            if 0 < kk < 1:
                sparkle(f"seam{i}", path_len_point(SEAM, kk) + Vector((0.01, 0, 0.012)), (1.0 - 0.2 * i) * (0.8 + 0.3 * math.sin(t * 30 + i)), 20 * i)
    look(cam, (3.6, -2.45, 1.0), (1.95, -0.6, 0.62), 26)


def anim_E11(fr):
    """'Ooh! Illumaesthetic does both!' - Pip perks up and pulls out her phone (the pilot's hand-off)."""
    t = fr / FPS
    screen("slicer")
    place_scan((0, 0, 0), 1.0)
    pop_group(PIPB, 1.0)
    L = LN[14]
    tw = L["words"][0]["t0"]
    perk = eback((t - tw + 0.04) / 0.16)
    hop = 0.05 * math.sin(math.pi * cl((t - tw) / 0.25))
    reach = ease((t - L["words"][1]["t0"]) / 0.45)
    m, lid = talk("PIP", t, 0.0)
    acc = accent("PIP", t)
    pose(PIP, loc=(1.2, -2.6, hop), rz=-4, hips=(lerp(6, -4, perk), 0, 0), head=(lerp(6, -6, perk) + 5 * acc, 0, lerp(-4, 6, perk)),
         armL=lerpv((4, 0, 6), (-62, 0, -8), reach), elbowL=lerp(-10, -80, reach), armR=(4, 0, -6), mouth=m, lid=lid,
         look=lerpv((0, 0), (0.5, 0.7), cl(perk)))
    pose(GUS, loc=(-0.6, -1.4, 0), rz=30)
    if reach > 0.01:
        bpy.context.view_layer.update()
        rest = PIP.hands["L"].matrix_world.translation.copy()
        chest = PIP.neck.matrix_world.translation + Vector((0.12, -0.3, -0.08))
        hp = aim_arm(PIP, "L", rest.lerp(chest, reach))
        set_vis(PHONE, True)
        n = Vector(lerpv((0.0, 0.3, -1.0), (0.15, 0.8, 0.55), reach)).normalized()
        orient_phone(PHONE, hp + Vector((0.0, -0.03, lerp(-0.12, 0.13, reach))), n, up=lerpv((0, 1, 0), (0, 0, 1), reach))
    look(cam, (1.25, -4.2, 0.98), (1.2, -2.6, 0.86), 42)


def pip_holding(t, look_=(0.6, 0.6), lid_base=0.0):
    set_vis(PIPSCAN, False)
    c, n, u, r = phone_pose_s11()
    m, lid = talk("PIP", t, lid_base)
    acc = accent("PIP", t)
    PIP.neck.rotation_euler = [math.radians(a) for a in (-12 + 6 * acc, 0, -16 + 3 * math.sin(t * 4))]
    set_face(PIP, m, lid, look_, (0.04, -12))
    return c, n, u, r


def anim_E12(fr):
    """'...Of course they do.' - Gus leans in; the camera pushes along the screen normal until the screen fills the frame."""
    t, k = fr / FPS, prog(fr, "E12")
    screen("slicer")
    place_scan((0, 0, 0), 1.0)
    pop_group(PIPB, 1.0)
    c, n, u, r = pip_holding(t, look_=(0.9, 0.7))
    f = -Vector((r.x, r.y, 0)).normalized()
    rz = math.degrees(math.atan2(f.x, -f.y))
    lean = eout((t - SF["E12"][0] / FPS) / 0.4)
    hx = lerp(14, 32, lean)
    m, lid = talk("GUS", t, 0.0)
    pose(GUS, loc=(0, 0, 0), rz=rz, hips=(hx, 0, 0), head=(-0.85 * hx, 0, 0), armL=(hx, 0, 8), armR=(hx, 0, -8), elbowL=-10,
         elbowR=-10, mouth=m, lid=lid, look=(0, -0.2), brow=(0.025, -4))
    want = c - n * 0.06 + r * lerp(0.62, 0.47, lean)
    bpy.context.view_layer.update()
    hc = GUS.neck.matrix_world @ Vector((0, 0, GUS.head_c))
    GUS.root.location += Vector((want.x - hc.x, want.y - hc.y, min(0.0, (c.z + 0.12) - hc.z)))
    # hold the wide-ish framing for the first half of the line, then push (lands full-screen on the last frame)
    kk = cl((k - 0.35) / 0.65)
    s12_cam(c, n, u, kk)


ANIM = {k: globals()[f"anim_{k}"] for k in SF}


def reset_anim():
    reset()
    pip_scanner("pouch")
    set_vis(PIPSCAN, True)
    set_vis(CAR, False)
    set_vis(UI, True)
    set_vis(SCAN, False)
    scan_ripple(None, None)
    set_vis(STOCKB, False)
    set_vis(PIPB, False)
    STOCKB.location = PIPB.location = (0, 0, 0)
    STOCKB.scale = PIPB.scale = (1, 1, 1)
    SKETCH.parent = None
    SKETCH.location, SKETCH.rotation_euler = SKETCH_HOME[0], (0, 0, 0)
    set_vis(SKETCH, True)
    PLATE.parent = PRINTER
    PLATE.location, PLATE.rotation_euler = PLATE_HOME, (0, 0, 0)
    PRINTER.location = (4.05, 3.15, 0.955)
    STOOL.location = (2.42, 2.55, 0)


# ================================================== run ==================================================
CORN = os.path.join(OUT, "screen_corners.json")
corners = json.load(open(CORN)) if os.path.exists(CORN) else dict(
    doc="Phone-screen corners for compositing the real footage (corner-pin), Ep 4 timing (ep4_timeline.json). Pixels in the "
        "1080x1920 frame, origin top-left, x right, y down. Corner order tl, tr, br, bl. The screen renders as flat key colour "
        "#ff00ff (camera rays only).",
    width=1080, height=1920, fps=FPS, screen_aspect="9:16", key_colour=KEY, corner_order=["tl", "tr", "br", "bl"], shots={})
lo, hi = (int(x) for x in RANGE.split(":")) if RANGE else (0, 10 ** 9)
for sh in SHOTS:
    f0, f1 = SF[sh]
    d = os.path.join(OUT, sh)
    os.makedirs(d, exist_ok=True)
    per = {}
    tsum, nr = 0.0, 0
    for fr in range(f0, f1):
        final = os.path.join(d, f"{fr:04d}.png")
        need_c = sh == "E12" and not ONLY
        todo = (fr - f0) % EVERY == 0 and lo <= fr < hi and not os.path.exists(final) and (not ONLY or fr in ONLY)
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
        scn.render.filepath = os.path.join(d, f"{fr:04d}_tmp")
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        os.replace(os.path.join(d, f"{fr:04d}_tmp.png"), final)
        tsum += time.time() - t0
        nr += 1
        print(f"[ep4] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if per:
        corners["shots"][sh] = dict(frames=[f0, f1], static=False, per_frame=per,
                                    note="push along the screen normal; last frame = full frame")
        corners["screen_full_frame"] = TL["screen_full_frame"]
        json.dump(corners, open(CORN, "w"), indent=1)
    if nr:
        print(f"[ep4] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
