"""Pip & Gus Ep 3 ("AESUB vs the alternatives") - cartoon part. Executed inside the pilot's scene builder, so the shop,
the cartoon sedan, Pip, Gus (row-3 proportions, no brows, nametags) and the cel look are the series' locked assets:

  cd projects/scan-tedium-explainer-reel/tools
  blender -b --factory-startup -P partA_scene.py -- --exec ../../pip-gus-ep3-aesub/tools/ep3_scene.py \
      --out FRAMES_DIR --tl ../../pip-gus-ep3-aesub/ep3_timeline.json [--shots A,B] [--scale 1] [--spp 8]
      [--every N] [--frames 10,20] [--range a:b] [--phonedir DIR --phonef0 N]

The first part of this file is the Ep 2 (spray) session's toolkit, copied unchanged from
projects/pip-gus-ep1-spray-white-light/tools/ep1_scene.py (branch claude/pip-gus-ep1-spray-white-light): talk/lip-sync,
eye-shape expressions, the sedan's extra parts, the generic scanner, spray puffs, dust coats, ray-cast structured light and
the scan patch. Ep 3 state and shots A-L follow. Frames already on disk are skipped (resumable). No text, numbers, logos or
brands in 3D: the vanishing spray is an unlabelled can with an orange cap and band (the owner's AESUB Orange cans); the
captions carry the name.
"""
import re as _re
from mathutils.bvhtree import BVHTree

EP_TL = json.load(open(arg("--tl", "")))
FPS = EP_TL["fps"]
SF = {s["id"]: (s["f0"], s["f1"]) for s in EP_TL["shots"]}
LN = {L["n"]: L for L in EP_TL["lines"] if "t0" in L}
EP_SHOTS = [s for s in arg("--shots", ",".join(SF)).split(",") if s in SF]
EVERY = int(arg("--every", "1"))
RANGE = arg("--range", "")
ONLY = {int(x) for x in arg("--frames", "").split(",") if x}
PAL.update(chrome="#dfe3e6", chrome_d="#9aa2a8", dust="#eeefea", seat="#3e4440", interior="#2c302d", tape="#e9e3cf",
           glass_see="#a9c3d6", beam="#9fd0ae")


# ----------------------------------------------------------------------------------------------------------------- easing / talk
def cl(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = cl(x)
    return x * x * (3 - 2 * x)


def eout(x):
    x = cl(x)
    return 1 - (1 - x) ** 2


def eback(x, s=1.4):
    x = cl(x) - 1
    return 1 + x * x * ((s + 1) * x + s)


def lerp(a, b, t):
    return a + (b - a) * t


def lerpv(a, b, t):
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


_V = _re.compile(r"[aeiouy]+")


def syllables(word):
    w = _re.sub(r"[^a-z]", "", word.lower())
    g = _V.findall(w) or ["a"]
    if len(g) > 1 and w.endswith("e") and not w.endswith(("le", "ee")) and g[-1] == "e":
        g = g[:-1]
    return g


SYL = {"PIP": [], "GUS": []}
STRESS = {"PIP": [], "GUS": []}
for L in LN.values():
    best = None
    for w in L["words"]:
        g = syllables(w["w"])
        d = max(0.05, w["t1"] - w["t0"]) / len(g)
        for k, v in enumerate(g):
            SYL[L["speaker"]].append((w["t0"] + k * d, d, 1.0 if any(c in v for c in "aou") else 0.72))
        key = (len(g), w["t1"] - w["t0"])
        if best is None or key > best[0]:
            best = (key, w["t0"])
    STRESS[L["speaker"]].append(best[1])


def mouth_at(spk, t):
    t += 1.0 / FPS
    m = 0.0
    for s0, d, a in SYL[spk]:
        u = (t - s0) / d
        if 0 <= u < 1:
            m = max(m, a * (u / 0.3 if u < 0.3 else 1 - 0.8 * (u - 0.3) / 0.7))
    return m * (0.9 if spk == "GUS" else 1.0)


def accent(spk, t):
    return 1.8 * max([math.exp(-((t - ta - 0.04) / 0.12) ** 2) for ta in STRESS[spk]] + [0.0])


def _blinks(seed):
    rng = random.Random(seed)
    out, x = [], rng.uniform(0.3, 1.4)
    while x < EP_TL["duration_s"] + 2:
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


def talk(spk, t):
    return mouth_at(spk, t), max(blink(spk, t), 0.28 * accent(spk, t))


def win(t, a, b, rin=0.12, rout=0.2):
    if t < a - rin or t > b + rout:
        return 0.0
    if t < a:
        return ease((t - (a - rin)) / rin)
    if t <= b:
        return 1.0
    return 1 - ease((t - b) / rout)


def wt(n, word):
    """Reel time of the first word in line n starting with `word`."""
    for w in LN[n]["words"]:
        if _re.sub(r"[^a-z]", "", w["w"].lower()).startswith(word):
            return w["t0"]
    raise KeyError((n, word))


# ----------------------------------------------------------------------------------------------------------------- expressions (no brows)
for _ch in (GUS, PIP):
    for _b in _ch.browset:
        for _o in list(_b["piv"].children) + [_b["piv"]]:
            bpy.data.objects.remove(_o, do_unlink=True)
    _ch.browset = []
CUR_T = 0.0
STATES = {   # fL, fR, shape, scale, tilt (deg, > 0 inner side down = annoyed, < 0 inner up = worried)
    "neutral": (0.0, 0.0, None, 1.0, 0),
    "curious": (0.0, 0.0, None, 1.15, 0),
    "impatient": (0.4, 0.4, None, 1.0, 16),
    "squint": (0.0, 0.0, "line", 1.0, 0),
    "thinking": (0.5, 0.0, None, 1.0, 12),
    "surprised": (0.0, 0.0, None, 1.3, 0),
    "excited": (0.0, 0.0, "arc", 1.0, 0),
    "deadpan": (0.55, 0.55, None, 1.0, 6),
    "weary": (0.55, 0.55, None, 1.0, 14),
}
EXPR = {"PIP": [], "GUS": []}   # (name, a, b, rin, rout)


def expr_state(nm, t):
    st = dict(fL=0.0, fR=0.0, shape=None, scale=1.0, tL=0.0, tR=0.0)
    if nm == "GUS":   # matter-of-fact: a subtle flat cut with a small annoyed tilt while he explains (pilot v5/v6 look)
        for L in LN.values():
            if L["speaker"] == "GUS":
                k = win(t, L["t0"] - 0.15, L["t1"], 0.2, 0.4)
                st["fL"] = st["fR"] = max(st["fL"], 0.2 * k)
                st["tL"] = st["tR"] = max(st["tL"], 10 * k)
    for name, a, b, rin, rout in EXPR[nm]:
        k = win(t, a, b, rin, rout)
        if k <= 0:
            continue
        fL, fR, shape, sc, tilt = STATES[name]
        st["fL"], st["fR"] = lerp(st["fL"], fL, k), lerp(st["fR"], fR, k)
        st["scale"] = lerp(st["scale"], sc, k)
        st["tL"], st["tR"] = lerp(st["tL"], tilt, k), lerp(st["tR"], tilt if name != "thinking" else 0, k)
        if shape and k > 0.5:
            st["shape"] = shape
    return st


def apply_expr(ch, lid=0.0):
    nm = "GUS" if ch is GUS else "PIP"
    st = expr_state(nm, CUR_T)
    for key, fk in (("tL", "fL"), ("tR", "fR")):
        if abs(st[key]) > 4 and st[fk] > 0.08:
            st[fk] = max(st[fk], 0.4 * min(1.0, abs(st[key]) / 12.0))
    fl, fr = max(lid, st["fL"]), max(lid, st["fR"])
    shaped = bool(st["shape"]) or max(fl, fr) > 0.08
    sc = st["scale"] * (1.1 if (shaped and st["scale"] < 1.05) else 1.0)
    if st["shape"]:
        set_eyes(ch, 0, 0, shape=st["shape"], scale=sc)
    else:
        set_eyes(ch, fl, fr, scale=sc)
    for e, sx, tl, f in zip(ch.eyeset, (1, -1), (st["tL"], st["tR"]), (fl, fr)):
        ang = max(-24.0, min(24.0, 1.35 * tl)) if (not st["shape"] and 0.08 < f < 0.9) else 0.0
        e["piv"].rotation_euler = (0, math.radians(-sx * ang), 0)


_pose_base = pose


def pose(ch, *a, **kw):
    _pose_base(ch, *a, **kw)
    apply_expr(ch, kw.get("lid", 0.0))


def face_rz(dx, dy):
    """rz (deg) that turns a character (front = -y at rz 0) to face direction (dx, dy)."""
    return math.degrees(math.atan2(dx, -dy))


def char_pose(ch, t, loc, face, **kw):
    """Pose with talk energy, blinks and accents from the timeline; face = world point the character faces (x, y)."""
    nm = "GUS" if ch is GUS else "PIP"
    m, lid = talk(nm, t)
    acc = accent(nm, t)
    rz = face_rz(face[0] - loc[0], face[1] - loc[1]) if face is not None else kw.pop("rz", 0.0)
    kw.pop("rz", None)
    head = kw.pop("head", (0, 0, 0))
    head = (head[0] + 6 * acc, head[1], head[2])
    pose(ch, loc=loc, rz=rz, head=head, mouth=m, lid=max(lid, kw.pop("lid", 0.0)), **kw)


# ----------------------------------------------------------------------------------------------------------------- extra car parts
EP = empty("EP1")
c = CAB
b_ = CAR_BODY


def cab_side(x, z, s=-1, out=0.008):
    t = (z - c["z0"]) / (c["z1"] - c["z0"])
    return Vector((x, s * (c["yb"] + (c["yt"] - c["yb"]) * t + out), z))


CHROME = []
# fender badge: on the front fender between the wheel arch (r 0.45 about x 1.30, z 0.36) and the headlight. It was at
# (1.48, 0.72), inside the arch circle, and read as sitting on the tyre (owner review of ep2_v1).
BX, BZ = 1.80, 0.64
# chrome beltline trim under the near-side windows and a chrome badge on each front fender
for s in (-1, 1):
    pts = [cab_side(x, z, s, 0.0) + Vector((0, s * dy, 0)) for x in (-1.0, 0.86) for z in (0.985, 1.025) for dy in (0.004, 0.022)]
    CHROME.append(hull(f"ep_trim{s}", pts, mat("chrome", hl=True), CAR, ol=0.006))
    bd = cyl(f"ep_badge{s}", 0.075, 0.016, (BX, s * (b_["y"] + 0.008), BZ), mat("chrome", hl=True), CAR, axis="Y", seg=40,
             bevel=0.004, ol=0.008)
    CHROME.append(bd)
    CHROME.append(cyl(f"ep_badge_in{s}", 0.045, 0.02, (BX, s * (b_["y"] + 0.01), BZ), mat("chrome_d"), CAR, axis="Y", seg=32))
BLACK = [bpy.data.objects["grille"]]
BLACK.append(box("ep_lip", (0.05, 1.62, 0.1), (2.01, 0, 0.37), mat("black"), CAR, bevel=0.015))
for s in (-1, 1):
    BLACK.append(box(f"ep_skirt{s}", (3.0, 0.03, 0.06), (0.05, s * (b_["y"] + 0.006), 0.35), mat("black"), CAR, bevel=0.01))
GLASS = [o for o in CAR.children if o.name.startswith(("win_", "windshield", "rearglass"))]
# open cabin for the glass shot: roof, pillars, seats, dark interior (the solid cabin hull hides while it is used)
CABIN_OPEN = empty("CABIN_OPEN", CAR)
_cm = mat("car")


def side_quad(x0, x1, z0, z1, s, name):
    pts = [cab_side(x0, z0, s, 0.0), cab_side(x1, z0, s, 0.0), cab_side(x1, z1, s, 0.0), cab_side(x0, z1, s, 0.0)]
    pts += [p - Vector((0, s * 0.03, 0)) for p in pts]
    return hull(name, pts, _cm, CABIN_OPEN, ol=0.01)


for s in (-1, 1):
    side_quad(-0.12, -0.02, 0.98, 1.5, s, f"bpil{s}")
    side_quad(c["xb0"], -0.98, 0.98, 1.5, s, f"cpil{s}")
    side_quad(0.84, c["xb1"], 0.98, 1.5, s, f"apil{s}")
    side_quad(c["xb0"], c["xb1"], 1.43, 1.5, s, f"rail{s}")
    side_quad(c["xb0"], c["xb1"], 0.98, 1.05, s, f"sill{s}")
hull("roof_open", [(c["xt0"], -c["yt"], c["z1"]), (c["xt1"], -c["yt"], c["z1"]), (c["xt0"], c["yt"], c["z1"]), (c["xt1"], c["yt"], c["z1"]),
                   (c["xt0"], -c["yt"], c["z1"] - 0.04), (c["xt1"], -c["yt"], c["z1"] - 0.04), (c["xt0"], c["yt"], c["z1"] - 0.04),
                   (c["xt1"], c["yt"], c["z1"] - 0.04)], _cm, CABIN_OPEN, ol=0.01)
box("int_back", (2.0, 0.04, 0.5), (-0.07, 0.6, 1.2), mat("interior"), CABIN_OPEN)
box("int_floor", (2.0, 1.3, 0.04), (-0.07, 0, 0.97), mat("interior"), CABIN_OPEN)
SEATS = []
for x in (0.35, -0.62):
    for y in (-0.33, 0.33):
        SEATS.append(box(f"seat_b{x}{y}", (0.12, 0.42, 0.5), (x - 0.12, y, 1.22), mat("seat"), CABIN_OPEN, bevel=0.04, ol=0.01))
        SEATS.append(box(f"seat_s{x}{y}", (0.45, 0.42, 0.1), (x + 0.1, y, 1.02), mat("seat"), CABIN_OPEN, bevel=0.04, ol=0.01))
set_vis(CABIN_OPEN, False)
GLASS_SEE = toon("glass_see", 0.32)
GLASS_MAT = GLASS[0].data.materials[0]
# tape strips on the roof (owner: "sometimes we use tape"); they appear from shot J on
TAPE = empty("TAPE", CAR)
_rng = random.Random(4)
for k in range(5):
    x = lerp(c["xt0"] + 0.15, c["xt1"] - 0.15, k / 4) + _rng.uniform(-0.04, 0.04)
    box(f"tape{k}", (0.05, _rng.uniform(0.28, 0.42), 0.006), (x, _rng.uniform(-0.2, 0.2), c["z1"] + 0.004), mat("tape"), TAPE,
        rot=(0, 0, _rng.uniform(-35, 35)))
set_vis(TAPE, False)


def car_meshes():
    out = []
    st = [CAR]
    while st:
        o = st.pop()
        st.extend(o.children)
        if o.type == "MESH" and not o.hide_render:
            out.append(o)
    return out


def category(o):
    n = o.name
    if o in GLASS:
        return "glass"
    if o in CHROME or n.startswith("ep_badge"):
        return "chrome"
    if o in BLACK or n.startswith(("tyre", "arch", "seam")):
        return "black"
    if n.startswith(("glint", "headl", "taill", "hub", "handle")):
        return "skip"
    return "paint"


def bvhs(objs):
    out = []
    for o in objs:
        me = o.data
        mw = o.matrix_world
        vs = [mw @ v.co for v in me.vertices]
        out.append((o, BVHTree.FromPolygons(vs, [tuple(p.vertices) for p in me.polygons])))
    return out


def cast(p, d, trees, ignore=()):
    best = None
    for o, t in trees:
        if o in ignore:
            continue
        h = t.ray_cast(p, d)
        if h[0] is not None and (best is None or h[3] < best[3]):
            best = (h[0], h[1], o, h[3])
    return best


# ----------------------------------------------------------------------------------------------------------------- scanner
def build_ep_scanner():
    """Generic two-lens structured-light scanner: projector (glowing sage lens) and camera (dark lens) a fixed distance apart
    on one bar, grip below. Not modelled on any real product."""
    g = empty("EPSCAN")
    box("es_bar", (0.36, 0.09, 0.1), (0, 0, 0), mat("metal"), g, 0.025, 0.012)
    box("es_grip", (0.07, 0.07, 0.17), (0, 0.03, -0.12), mat("dark"), g, 0.02, 0.012, rot=(-12, 0, 0))
    cyl("es_proj_r", 0.04, 0.02, (-0.12, -0.048, 0), mat("dark"), g, axis="Y", seg=32)
    cyl("es_proj", 0.03, 0.022, (-0.12, -0.05, 0), emit("sage_l", 2.2), g, axis="Y", seg=32)
    cyl("es_cam_r", 0.04, 0.02, (0.12, -0.048, 0), mat("#6b6d6a"), g, axis="Y", seg=32)
    cyl("es_cam", 0.028, 0.022, (0.12, -0.05, 0), mat("#121312"), g, axis="Y", seg=32)
    blob("es_cam_glint", (0.008, 0.004, 0.008), (0.128, -0.062, 0.009), emit("white", 1.0), g)
    return g


EPSCAN = build_ep_scanner()
set_vis(EPSCAN, False)


def place_scanner(pos, aim):
    """Scanner at pos, lenses facing aim (the bar's -y side faces the car)."""
    pos, aim = Vector(pos), Vector(aim)
    f = (aim - pos).normalized()
    EPSCAN.matrix_world = Matrix.Translation(pos) @ f.to_track_quat("-Y", "Z").to_matrix().to_4x4()
    set_vis(EPSCAN, True)
    bpy.context.view_layer.update()
    mw = EPSCAN.matrix_world
    return mw @ Vector((-0.12, -0.06, 0)), mw @ Vector((0.12, -0.06, 0))   # projector lens, camera lens (world)


def hold_scanner(ch, pos, aim):
    """Gus holds the scanner: right hand on the grip, left hand on the bar's far end (floating hands, arms straight)."""
    pj, cm = place_scanner(pos, aim)
    mw = EPSCAN.matrix_world
    aim_arm(ch, "R", mw @ Vector((0.0, 0.05, -0.16)))
    aim_arm(ch, "L", mw @ Vector((-0.2, 0.02, 0.0)))
    return pj, cm


# ----------------------------------------------------------------------------------------------------------------- spray
def build_can():
    g = empty("CAN")
    cyl("can_body", 0.034, 0.15, (0, 0, 0), mat("white"), g, seg=28, bevel=0.006, ol=0.008)
    cyl("can_band", 0.0345, 0.03, (0, 0, 0.03), mat("sage"), g, seg=28)
    cyl("can_cap", 0.026, 0.035, (0, 0, 0.09), mat("sage"), g, seg=24, bevel=0.006, ol=0.006)
    box("can_nozzle", (0.012, 0.02, 0.012), (0, -0.026, 0.1), mat("dark"), g)
    return g


CAN = build_can()
set_vis(CAN, False)


def hold_can(ch, side, target):
    """Can in a floating hand, nozzle aimed at target; returns the nozzle's world position and spray direction."""
    hand = ch.hands[side]
    bpy.context.view_layer.update()
    hp = hand.matrix_world.translation
    d = (Vector(target) - hp)
    d.z = 0
    d = d.normalized() if d.length > 1e-4 else Vector((0, 1, 0))
    rot = d.to_track_quat("-Y", "Z").to_matrix().to_4x4()
    CAN.matrix_world = Matrix.Translation(hp + Vector((0, 0, 0.04))) @ rot
    set_vis(CAN, True)
    bpy.context.view_layer.update()
    noz = CAN.matrix_world @ Vector((0, -0.04, 0.1))
    return noz, (Vector(target) - noz).normalized()


def puff(noz, d, age, n=16, seed=1, reach=0.4):
    """Spray burst: soft white blobs streaming from the nozzle along d, growing and fading over ~0.5 s."""
    if age < 0 or age > 0.6:
        return
    rng = random.Random(seed)
    g = temp(empty("puff"))
    for k in range(n):
        delay = rng.uniform(0, 0.25)
        a = age - delay
        if a <= 0:
            continue
        u = cl(a / 0.35)
        jit = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))) * 0.06 * u
        p = noz + d * (reach * eout(u)) + jit
        r = lerp(0.015, 0.07, eout(u))
        alpha = 0.55 * (1 - cl((a - 0.2) / 0.3))
        if alpha < 0.03:
            continue
        blob(f"pf{k}", (r, r, r), p, mat("white", round(alpha, 2)), g, seg=12, rings=8)


DUST_CACHE = {}


def dust_spots(key, origin, aim, spread, n, targets, seed=3, size=(0.014, 0.03)):
    """Sprayed coating as overlapping flat white blobs: rays from `origin` within a cone around `aim` onto the target meshes.
    Cached per key; returns a list of (point, normal, radius) in spray order."""
    if key in DUST_CACHE:
        return DUST_CACHE[key]
    trees = bvhs(targets)
    rng = random.Random(seed)
    origin, aim = Vector(origin), Vector(aim)
    f = (aim - origin).normalized()
    r = f.cross(Vector((0, 0, 1))).normalized()
    u = r.cross(f)
    out = []
    tries = 0
    while len(out) < n and tries < n * 20:
        tries += 1
        a, b = rng.gauss(0, spread), rng.gauss(0, spread * 0.8)
        h = cast(origin, (f + r * a + u * b).normalized(), trees)
        if h is None:
            continue
        out.append((h[0], h[1], rng.uniform(*size)))
    DUST_CACHE[key] = out
    return out


def draw_dust(spots, k, name="dust"):
    """First k (0..len) spots as thin white discs on the surface."""
    k = int(k)
    if k <= 0:
        return
    bm = bmesh.new()
    for p, nrm, r in spots[:k]:
        nrm = Vector(nrm).normalized()
        t1 = nrm.orthogonal().normalized()
        t2 = nrm.cross(t1)
        ctr = bm.verts.new(p + nrm * 0.006)
        ring = [bm.verts.new(p + nrm * 0.006 + (t1 * math.cos(2 * math.pi * i / 12) + t2 * math.sin(2 * math.pi * i / 12)) * r)
                for i in range(12)]
        for i in range(12):
            bm.faces.new((ctr, ring[i], ring[(i + 1) % 12]))
    temp(new_obj(name, bm, [mat("dust")]))


# ----------------------------------------------------------------------------------------------------------------- structured light
STRIPE_CACHE = {}


def stripes(key, proj, aim, n=13, half_w=0.32, half_h=0.42, samples=90, see_glass=False, coated=False):
    """Vertical stripe planes from the projector lens, ray-cast onto the car. Returns a list of stripes, each a list of hits
    (point, normal, category) or None. Glass is skipped by rays when see_glass (light goes straight through)."""
    if key in STRIPE_CACHE:
        return STRIPE_CACHE[key]
    objs = car_meshes() + [bpy.data.objects["floor"], bpy.data.objects["wall_back"]]
    trees = bvhs(objs)
    proj, aim = Vector(proj), Vector(aim)
    f = (aim - proj).normalized()
    r = f.cross(Vector((0, 0, 1))).normalized()
    u = r.cross(f)
    out = []
    for i in range(n):
        a = -half_w + 2 * half_w * i / max(1, n - 1)
        row = []
        for j in range(samples):
            bb = half_h - 2 * half_h * j / (samples - 1)
            d = (f + r * a + u * bb).normalized()
            h = cast(proj, d, trees, ignore=GLASS if see_glass else ())
            if h is None:
                row.append(None)
                continue
            cat = category(h[2])
            if h[2].name in ("floor", "wall_back"):
                cat = "bg"
            if coated and cat in ("glass", "chrome", "black"):
                cat = "paint"
            row.append((h[0], h[1], cat, h[2].name))
        out.append(row)
    STRIPE_CACHE[key] = out
    return out


def draw_stripes(rows, grow=1.0, black_alpha=1.0, width=0.022, cats=("paint", "glass", "black"), name="stripes", strength=2.0,
                 grow_axis="down"):
    """Glowing ribbons along each stripe's hits; a stripe breaks at depth jumps or category changes. grow 0..1 reveals the
    stripes top-down (the pattern 'drapes' over the car). Chrome never shows a stripe (it mirrors the light away)."""
    bms = {}
    for row in rows:
        nmax = int(len(row) * cl(grow)) if grow_axis == "down" else len(row)
        seg = []
        for j in range(nmax + 1):
            h = row[j] if j < min(nmax, len(row)) else None
            ok = h is not None and h[2] in cats
            if ok and seg:
                q = seg[-1]
                if (h[0] - q[0]).length > 0.08 or h[2] != q[2]:
                    ok_break = True
                else:
                    ok_break = False
            else:
                ok_break = False
            if (not ok or ok_break) and len(seg) >= 2:
                cat = seg[0][2]
                bm = bms.setdefault(cat, bmesh.new())
                prev = None
                for k, (p, nrm, cc, _) in enumerate(seg):
                    nrm = Vector(nrm)
                    tg = (seg[min(k + 1, len(seg) - 1)][0] - seg[max(k - 1, 0)][0])
                    side = nrm.cross(tg).normalized() * width / 2 if tg.length > 1e-6 else Vector((0.01, 0, 0))
                    pp = Vector(p) + nrm * 0.007
                    v = (bm.verts.new(pp - side), bm.verts.new(pp + side))
                    if prev:
                        bm.faces.new((prev[0], prev[1], v[1], v[0]))
                    prev = v
                seg = []
            elif not ok:
                seg = []
            if ok_break:
                seg = []
            if ok:
                seg.append(h)
    for cat, bm in bms.items():
        if cat == "black":
            if black_alpha < 0.04:
                bm.free()
                continue
            m = emit("beam", strength * black_alpha, round(cl(black_alpha), 2))
        else:
            m = emit("beam", strength)
        temp(new_obj(f"{name}_{cat}", bm, [m]))


def beam_sheet(proj, rows, alpha=0.1, name="beam"):
    """Translucent light from the projector lens to the outline of the lit area (fan of thin triangles per stripe)."""
    bm = bmesh.new()
    pv = None
    for row in rows:
        hs = [h for h in row if h is not None]
        if len(hs) < 2:
            continue
        a, b = Vector(hs[0][0]), Vector(hs[-1][0])
        p0 = bm.verts.new(proj)
        bm.faces.new((p0, bm.verts.new(a), bm.verts.new(b)))
    temp(new_obj(name, bm, [emit("beam", 1.2, alpha)]))


def scan_patch(rows, k, seed_pt, name="patch", cats=("paint",), offset=0.012):
    """Faceted scan mesh from the stripe hits: quads between neighbouring stripes (two tones = triangles that read as a mesh),
    revealed nearest-first from seed_pt; k 0..1. Holes stay wherever the light did not come back."""
    quads = []
    for i in range(len(rows) - 1):
        for j in range(len(rows[i]) - 1):
            hs = (rows[i][j], rows[i + 1][j], rows[i + 1][j + 1], rows[i][j + 1])
            if any(h is None or h[2] not in cats for h in hs):
                continue
            ps = [Vector(h[0]) + Vector(h[1]) * offset for h in hs]
            if max((ps[q] - ps[(q + 1) % 4]).length for q in range(4)) > 0.09:
                continue
            quads.append(ps)
    if not quads or k <= 0:
        return
    sp = Vector(seed_pt)
    quads.sort(key=lambda q: (q[0] - sp).length)
    nshow = int(len(quads) * cl(k))
    bm = bmesh.new()
    for q in quads[:nshow]:
        v = [bm.verts.new(p) for p in q]
        f1 = bm.faces.new((v[0], v[1], v[2]))
        f2 = bm.faces.new((v[0], v[2], v[3]))
        f1.material_index, f2.material_index = 0, 1
    temp(new_obj(name, bm, [emit("#d3d7d3", 1.0), emit("#aeb3ae", 1.0)]))


def dashed(a, b, name, dash=0.05, gap=0.035, r=0.008, key="white"):
    a, b = Vector(a), Vector(b)
    L = (b - a).length
    d = (b - a).normalized()
    g = temp(empty(name))
    s = 0.0
    k = 0
    while s < L:
        e = min(L, s + dash)
        mid = a + d * ((s + e) / 2)
        o = cyl(f"{name}{k}", r, e - s, (0, 0, 0), emit(key, 1.6), g, seg=8)
        o.matrix_world = Matrix.Translation(mid) @ d.to_track_quat("Z", "Y").to_matrix().to_4x4()
        s = e + gap
        k += 1
    return g


def qmark(pos, scale, name="q"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = "?"
    cu.extrude = 0.02
    cu.align_x = "CENTER"
    ob = bpy.data.objects.new(name, cu)
    COLL.objects.link(ob)
    ob.data.materials.append(emit("white", 1.0))
    ob.location = pos
    ob.rotation_euler = (math.radians(90), 0, 0)
    ob.scale = (scale, scale, scale)
    temp(ob)
    back = ob.copy()
    back.data = cu.copy()
    back.data.materials.clear()
    back.data.materials.append(emit("black", 1.0))
    back.data.offset = 0.02
    back.location = Vector(pos) + Vector((0, 0.01, 0))
    COLL.objects.link(back)
    temp(back)
    return ob


def ring(pos, nrm, r, name, key="sage_l", t=0.008):
    o = torus(name, r, t, (0, 0, 0), emit(key, 2.0), None)
    o.matrix_world = Matrix.Translation(pos) @ Vector(nrm).to_track_quat("Z", "Y").to_matrix().to_4x4()
    temp(o)
    return o


# ----------------------------------------------------------------------------------------------------------------- squiggles
SQ_CACHE = {}


def squiggle_paths():
    """Loose hand-sprayed squiggles on the near rear door (x -1.08..-0.12), on its surface plane y = -0.851."""
    if "p" in SQ_CACHE:
        return SQ_CACHE["p"]
    rng = random.Random(9)
    paths = []
    for k in range(5):
        x0 = lerp(-1.02, -0.3, k / 4) + rng.uniform(-0.04, 0.04)
        z0 = rng.uniform(0.5, 0.85)
        pts = []
        for i in range(26):
            s = i / 25
            pts.append(Vector((x0 + 0.17 * s + 0.05 * math.sin(s * 11 + k), -(b_["y"] + 0.004), z0 + 0.09 * math.sin(s * 7.5 + k * 2))))
        paths.append(pts)
    SQ_CACHE["p"] = paths
    return paths


def draw_squiggles(k, name="sq"):
    paths = squiggle_paths()
    tot = len(paths) * 25
    n = int(tot * cl(k))
    bm = bmesh.new()
    for pi_, pts in enumerate(paths):
        m = min(25, max(0, n - pi_ * 25))
        prev = None
        for i in range(m + 1 if m else 0):
            p = pts[i]
            tg = pts[min(i + 1, 25)] - pts[max(i - 1, 0)]
            side = Vector((0, -1, 0)).cross(tg).normalized() * 0.014
            v = (bm.verts.new(p - side), bm.verts.new(p + side))
            if prev:
                bm.faces.new((prev[0], prev[1], v[1], v[0]))
            prev = v
    temp(new_obj(name, bm, [mat("dust")]))




# ================================================================================================================= Ep 3 (AESUB)
# Everything above is the Ep 2 (spray) session's toolkit, unchanged (talk, expressions, car parts, scanner, spray, dust,
# structured light, scan patch). Below: Ep 3 state and shots A-L, timed from ep3_timeline.json.
T = lambda n: LN[n]["t0"]
T1 = lambda n: LN[n]["t1"]
FRONT_WIN = bpy.data.objects["win_-1_-0.02"]
REAR_WIN = bpy.data.objects["win_-1_-0.98"]
PAL.update(powder="#e7e1d3", orange="#e9792b", orange_d="#b9581a", coin="#e3b54a", coin_d="#b38a2c", sun="#ffd34d",
           cloth="#f1f1ec", cloth_dirty="#9c9d97", exo="#26407f", exo_d="#1a2c5a", exo_s="#d9dde2", spark="#ffffff")
T_VANISH = wt(2, "disappears")


def vanish_k(t):
    """AESUB coat (left on the car from Ep 2) sublimating: 0 = full coat, 1 = gone."""
    return ease((t - (T_VANISH - 0.1)) / 1.7)


def win_spots(obj, key, n=900):
    bpy.context.view_layer.update()
    ctr = sum((obj.matrix_world @ v.co for v in obj.data.vertices), Vector()) / len(obj.data.vertices)
    return dust_spots(key, ctr + Vector((0, -0.9, 0.05)), ctr, 0.18, n, [obj], seed=len(key))


def coat_layer(obj, k, out=Vector((0, -0.004, 0))):
    a = round(cl((k - 0.3) / 0.6) * 0.92, 2)
    if a < 0.04:
        return
    o = temp(bpy.data.objects.new(obj.name + "_coat", obj.data.copy()))
    COLL.objects.link(o)
    o.data.materials.clear()
    o.data.materials.append(mat("dust", a) if a < 0.9 else mat("dust"))
    o.matrix_world = Matrix.Translation(out) @ obj.matrix_world


def aesub_coat(t):
    """The Ep 2 end state (windows, trim, grille, badge, squiggles) fading out like frost: spots drop out in random order
    (the spray order is random), the solid skin thins first."""
    k = 1 - vanish_k(t)
    if k <= 0.001:
        return
    for obj, key in ((FRONT_WIN, "fw"), (REAR_WIN, "rw")):
        sp = win_spots(obj, key)
        draw_dust(sp, len(sp) * k ** 0.7, "dust_" + key)
        coat_layer(obj, k ** 1.6)
    tr = bpy.data.objects["ep_trim-1"]
    sp = dust_spots("trim", (-0.07, -1.7, 1.15), (-0.07, -0.75, 1.0), 0.45, 110, [tr], seed=5, size=(0.012, 0.022))
    draw_dust(sp, len(sp) * k ** 0.8, "dust_trim")
    gr = [bpy.data.objects["grille"], bpy.data.objects["ep_lip"]]
    sp = dust_spots("grille", (3.0, -0.4, 0.6), (2.0, 0, 0.5), 0.35, 160, gr, seed=6, size=(0.02, 0.04))
    draw_dust(sp, len(sp) * k ** 0.8, "dust_grille")
    bd = [bpy.data.objects["ep_badge-1"], bpy.data.objects["ep_badge_in-1"]]
    sp = dust_spots("badge", (BX, -1.5, BZ + 0.03), (BX, -0.85, BZ), 0.06, 40, bd, seed=7, size=(0.012, 0.022))
    draw_dust(sp, len(sp) * k ** 0.8, "dust_badge")
    draw_squiggles(k ** 0.8)
    set_vis(TAPE, k > 0.5)


def car_meshes():
    """Ep 2's helper, extended: the visible car (the sedan, or the exotic from shot I on)."""
    root = EXOTIC if (EXOTIC is not None and not EXOTIC.hide_render) else CAR
    out, st = [], [root]
    while st:
        o = st.pop()
        st.extend(o.children)
        if o.type == "MESH" and not o.hide_render:
            out.append(o)
    return out


EXOTIC = None


def paint_meshes():
    return [o for o in car_meshes() if category(o) == "paint" and not o.name.startswith("ep_")]


# ---------------------------------------------------------------------------------------------- the cheap powder (D, E, G)
DOOR_AIM = Vector((0.35, -0.85, 0.8))
POW_ORIGIN = Vector((0.35, -2.1, 1.0))


def powder_spots():
    """Dry shampoo / foot powder on the front door: big chalky blobs, thicker than the AESUB mist."""
    return dust_spots("powder", POW_ORIGIN, DOOR_AIM, 0.28, 650, paint_meshes(), seed=13, size=(0.025, 0.05))


def grille_powder():
    gr = [bpy.data.objects["grille"], bpy.data.objects["ep_lip"]]
    return dust_spots("gpowder", (3.0, -0.4, 0.6), (2.0, 0, 0.5), 0.35, 200, gr, seed=17, size=(0.022, 0.045))


def draw_powder(spots, k_on, wiped_x=None, keep=0.12, name="powder"):
    """Powder spots, first k_on of them sprayed; spots left of wiped_x (the cloth's path, it wipes front to back) are gone
    except a random `keep` share that stays in the gaps."""
    n = int(len(spots) * cl(k_on))
    rng = random.Random(5)
    out = []
    for i, s in enumerate(spots[:n]):
        stuck = rng.random() < keep
        if wiped_x is not None and s[0].x > wiped_x and not stuck:
            continue
        out.append(s)
    if not out:
        return
    bm = bmesh.new()
    for p, nrm, r in out:
        nrm = Vector(nrm).normalized()
        t1 = nrm.orthogonal().normalized()
        t2 = nrm.cross(t1)
        ctr = bm.verts.new(p + nrm * 0.007)
        ring_ = [bm.verts.new(p + nrm * 0.007 + (t1 * math.cos(2 * math.pi * i / 12) + t2 * math.sin(2 * math.pi * i / 12)) * r)
                 for i in range(12)]
        for i in range(12):
            bm.faces.new((ctr, ring_[i], ring_[(i + 1) % 12]))
    temp(new_obj(name, bm, [mat("powder")]))


# ---------------------------------------------------------------------------------------------- props
def build_orange_can():
    """The vanishing spray: same generic can as Ep 2, orange cap and band (the owner's AESUB Orange cans). No text."""
    g = empty("OCAN")
    cyl("oc_body", 0.034, 0.15, (0, 0, 0), mat("white"), g, seg=28, bevel=0.006, ol=0.008)
    cyl("oc_band", 0.0345, 0.04, (0, 0, 0.025), mat("orange"), g, seg=28)
    cyl("oc_cap", 0.026, 0.035, (0, 0, 0.09), mat("orange"), g, seg=24, bevel=0.006, ol=0.006)
    box("oc_nozzle", (0.012, 0.02, 0.012), (0, -0.026, 0.1), mat("dark"), g)
    return g


def build_bottle(name, body, cap, h=0.16, r=0.04):
    """Generic squeeze bottles for the cheap powders (no labels, no brands)."""
    g = empty(name)
    cyl(name + "_b", r, h, (0, 0, 0), mat(body), g, seg=28, bevel=0.012, ol=0.008)
    cyl(name + "_s", r * 0.55, 0.03, (0, 0, h / 2 + 0.012), mat(body), g, seg=20, ol=0.006)
    cyl(name + "_c", r * 0.45, 0.03, (0, 0, h / 2 + 0.04), mat(cap), g, seg=20, bevel=0.004, ol=0.006)
    return g


OCAN = build_orange_can()
SHAMPOO = build_bottle("SHAMPOO", "#f4f1ea", "#7fa3c4")
FOOTP = build_bottle("FOOTP", "#e6dcc8", "#c7b28a", h=0.13, r=0.045)


def coin_stack(pos, n, name):
    g = temp(empty(name))
    for i in range(n):
        cyl(f"{name}{i}", 0.045, 0.014, (pos[0] + 0.004 * math.sin(i * 1.7), pos[1], pos[2] + 0.016 * i), mat("coin"), g, seg=28,
            ol=0.005)
    return g


def build_cloth():
    g = empty("CLOTH")
    box("cloth_m", (0.16, 0.04, 0.12), (0, 0, 0), mat("cloth"), g, bevel=0.02, ol=0.008)
    return g


CLOTH = build_cloth()


def cloth_at(p, dirt):
    CLOTH.matrix_world = Matrix.Translation(Vector(p))
    CLOTH.children[0].data.materials[0] = mat("cloth_dirty") if dirt > 0.5 else mat("cloth")
    set_vis(CLOTH, True)


def hold_prop(prop, ch, side, up=Vector((0, 0, 0.04)), face=None):
    bpy.context.view_layer.update()
    hp = ch.hands[side].matrix_world.translation
    rot = Matrix.Identity(4)
    if face is not None:
        d = Vector(face) - hp
        d.z = 0
        if d.length > 1e-4:
            rot = d.normalized().to_track_quat("-Y", "Z").to_matrix().to_4x4()
    prop.matrix_world = Matrix.Translation(hp + up) @ rot
    set_vis(prop, True)
    bpy.context.view_layer.update()
    return prop.matrix_world @ Vector((0, -0.04, 0.1))


def puff_col(noz, d, age, key, n=16, seed=1, reach=0.4, size=0.07):
    if age < 0 or age > 0.6:
        return
    rng = random.Random(seed)
    g = temp(empty("puff"))
    for k in range(n):
        a = age - rng.uniform(0, 0.25)
        if a <= 0:
            continue
        u = cl(a / 0.35)
        jit = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))) * 0.06 * u
        p = noz + d * (reach * eout(u)) + jit
        r = lerp(0.015, size, eout(u))
        alpha = 0.6 * (1 - cl((a - 0.2) / 0.3))
        if alpha >= 0.03:
            blob(f"pf{k}", (r, r, r), p, mat(key, round(alpha, 2)), g, seg=12, rings=8)


# ---------------------------------------------------------------------------------------------- the exotic (I, J)
def build_exotic():
    """A generic low mid-engine coupe in blue with a pale centre stripe (a nod to the real car, no badges, no brand shape
    details). Same footprint/orientation as the sedan: front = +x."""
    g = empty("EXOTIC")
    body = [(-2.2, -0.95, 0.28), (2.25, -0.88, 0.28), (-2.2, 0.95, 0.28), (2.25, 0.88, 0.28),
            (-2.15, -0.93, 0.78), (-2.15, 0.93, 0.78), (1.0, -0.9, 0.78), (1.0, 0.9, 0.78), (2.3, -0.8, 0.5), (2.3, 0.8, 0.5),
            (0.2, -0.98, 0.7), (0.2, 0.98, 0.7)]
    hull("exo_body", body, mat("exo", hl=True), g, bevel=0.06, ol=0.012)
    cab = [(-1.1, -0.62, 0.76), (0.95, -0.66, 0.76), (-1.1, 0.62, 0.76), (0.95, 0.66, 0.76),
           (-0.65, -0.48, 1.18), (0.25, -0.5, 1.2), (-0.65, 0.48, 1.18), (0.25, 0.5, 1.2)]
    hull("exo_cab", cab, mat("exo_d", hl=True), g, bevel=0.05, ol=0.012)
    hull("exo_glass", [(0.3, -0.5, 1.16), (0.97, -0.64, 0.8), (0.3, 0.5, 1.16), (0.97, 0.64, 0.8),
                       (0.32, -0.5, 1.17), (0.99, -0.64, 0.81), (0.32, 0.5, 1.17), (0.99, 0.64, 0.81)], mat("glass", hl=True), g,
         ol=0.008)
    box("exo_stripe", (2.4, 0.16, 0.012), (0.6, 0, 0.785), mat("exo_s"), g, rot=(0, -6, 0))
    for x in (-1.45, 1.45):
        for s in (-1, 1):
            cyl(f"exo_tyre{x}{s}", 0.35, 0.26, (x, s * 0.83, 0.35), mat("tyre"), g, axis="Y", seg=40, bevel=0.03, ol=0.01)
            cyl(f"exo_rim{x}{s}", 0.24, 0.27, (x, s * 0.83, 0.35), mat("chrome", hl=True), g, axis="Y", seg=40, ol=0.006)
    for s in (-1, 1):
        box(f"exo_lamp{s}", (0.08, 0.32, 0.05), (2.24, s * 0.55, 0.62), emit("white", 1.2), g, rot=(0, 20, 0))
        box(f"exo_intake{s}", (0.5, 0.03, 0.18), (-0.55, s * 0.97, 0.55), mat("black"), g, bevel=0.02)
    return g


EXOTIC = build_exotic()
set_vis(EXOTIC, False)
EXO_HOOD = Vector((1.55, 0, 0.82))


def exo_meshes():
    out, st = [], [EXOTIC]
    while st:
        o = st.pop()
        st.extend(o.children)
        if o.type == "MESH":
            out.append(o)
    return out


def exo_coat_spots():
    return dust_spots("exocoat", (1.6, -1.25, 1.9), (1.55, -0.2, 0.8), 0.33, 900,
                      [bpy.data.objects["exo_body"], bpy.data.objects["exo_stripe"]], seed=23, size=(0.016, 0.03))


def sparkle(p, k, name):
    if k <= 0:
        return
    g = temp(empty(name))
    s = 0.07 * math.sin(math.pi * cl(k))
    box(name + "a", (s, 0.004, s * 0.18), p, emit("spark", 2.5), g, rot=(0, 0, 0))
    box(name + "b", (s * 0.18, 0.004, s), p, emit("spark", 2.5), g, rot=(0, 0, 0))


def sun_icon(k, t):
    """Cartoon sun pinned to the top-left of the frame (in front of the camera), slowly turning."""
    if k <= 0:
        return
    bpy.context.view_layer.update()
    M = cam.matrix_world
    f, r, u = -(M.to_3x3() @ Vector((0, 0, 1))), M.to_3x3() @ Vector((1, 0, 0)), M.to_3x3() @ Vector((0, 1, 0))
    c = M.translation + f * 2.2 - r * 0.38 + u * 0.68
    g = temp(empty("SUN"))
    s = 0.12 * eback(k)
    blob("sun_d", (s, s, s), c, emit("sun", 1.6), g, seg=24, rings=12)
    for i in range(10):
        a = 2 * math.pi * i / 10 + t * 0.8
        p = c + (r * math.cos(a) + u * math.sin(a)) * s * 1.65
        v = r * math.cos(a) + u * math.sin(a)
        o = box(f"sun_r{i}", (0.022, 0.01, s * 0.55), (0, 0, 0), emit("sun", 1.6), g)
        o.matrix_world = Matrix.Translation(p) @ v.to_track_quat("Z", "Y").to_matrix().to_4x4()


# ---------------------------------------------------------------------------------------------- shots
GUS_IDLE = dict(armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12, elbowR=-12)


def prog(fr, sh):
    f0, f1 = SF[sh]
    return (fr - f0) / max(1, f1 - 1 - f0)


def cam_push(loc, target, lens, k):
    loc, target = Vector(loc), Vector(target)
    look(cam, target + (loc - target) * (1 - k), target, lens)


def hand_to(ch, side, p):
    bpy.context.view_layer.update()
    h = ch.hands[side]
    h.matrix_world = Matrix.Translation(Vector(p)) @ h.matrix_world.to_3x3().to_4x4()


# expressions (eye shapes only)
EXPR["PIP"].append(("curious", T(1), T1(1), 0.15, 0.3))
EXPR["PIP"].append(("surprised", T_VANISH + 0.1, T1(2) + 0.6, 0.12, 0.3))
EXPR["PIP"].append(("curious", T(3), T1(3), 0.12, 0.3))
EXPR["PIP"].append(("impatient", T(6) - 0.2, T1(6) + 0.3, 0.1, 0.3))
EXPR["PIP"].append(("excited", T(8), T1(8) + 0.3, 0.1, 0.2))
EXPR["PIP"].append(("surprised", wt(9, "expensive"), T1(9), 0.12, 0.3))
EXPR["PIP"].append(("excited", T(12), T1(12) + 0.4, 0.1, 0.2))
if LN[7].get("sighs"):
    EXPR["GUS"].append(("weary", LN[7]["sighs"][0][0], T(7) + 0.3, 0.15, 0.3))
EXPR["GUS"].append(("weary", wt(5, "wipe"), T1(5), 0.1, 0.3))
EXPR["GUS"].append(("deadpan", T(11) - 0.2, T1(11) + 1.0, 0.1, 0.2))
EXPR["GUS"].append(("deadpan", wt(9, "every") - 0.1, T1(9) + 0.3, 0.1, 0.2))


def anim_A(fr):
    """'Does that spray stay on forever?' The sedan as Ep 2 left it (windows, trim, grille, badge dusted, squiggles, tape).
    Pip pokes the dusted front window; Gus beside him with the orange can."""
    t, u = fr / FPS, prog(fr, "A")
    aesub_coat(t)
    poke = Vector((0.55, -0.757, 1.15))
    char_pose(PIP, t, (0.85, -1.2, 0.02 * abs(math.sin(t * 6))), (0.3, -2.2), head=(-12, 0, 0), look=(-0.6, 0.4))
    k = ease((t - (T(1) + 0.3)) / 0.3)
    hand_to(PIP, "R", poke + Vector((0.0, -0.06 - 0.25 * (1 - k), 0)))
    char_pose(GUS, t, (-0.45, -1.95, 0), (0.7, -1.4), armL=(4, 0, 6), armR=(-30, 0, -10), elbowR=-40)
    hold_prop(OCAN, GUS, "R")
    cam_push((1.9, -3.9, 1.45), (0.2, -1.2, 1.0), 28, 0.05 * ease(u))


def anim_B(fr):
    """'Not this one. AESUB just disappears.' Gus lifts the orange can; on 'disappears' the whole coat fades off like frost
    and Pip's eyes go wide."""
    t, u = fr / FPS, prog(fr, "B")
    aesub_coat(t)
    lift = ease((t - T(2)) / 0.4)
    char_pose(GUS, t, (-0.2, -1.95, 0), (1.2, -3.6), look=(0.2, 0.1), armL=(4, 0, 6), armR=(lerp(-30, -95, lift), 0, -10),
              elbowR=lerp(-40, -20, lift))
    hold_prop(OCAN, GUS, "R")
    # glint on the can when it is up
    gk = win(t, T(2) + 0.45, T(2) + 0.9, 0.05, 0.25)
    if gk > 0:
        bpy.context.view_layer.update()
        p = OCAN.matrix_world @ Vector((0.03, -0.04, 0.06))
        sparkle(p, gk, "cang")
    char_pose(PIP, t, (0.95, -1.75, 0), (-0.2, -1.9), head=(-8, 0, 0), look=(-0.4, 0.3))
    cam_push((2.2, -4.4, 1.45), (0.3, -1.0, 1.0), 26, 0.04 * ease(u))


def anim_C(fr):
    """'Then why use anything else?' Pip, curious, at the clean car; Gus still holding the can."""
    t, u = fr / FPS, prog(fr, "C")
    char_pose(PIP, t, (0.95, -1.75, 0), (-0.2, -1.9), head=(-10, 0, 6 * math.sin(t * 2)), look=(-0.4, 0.4),
              armL=(-25, 0, 10), armR=(-25, 0, -10))
    char_pose(GUS, t, (-0.2, -1.95, 0), (0.95, -1.75), armL=(4, 0, 6), armR=(-35, 0, -10), elbowR=-45)
    hold_prop(OCAN, GUS, "R")
    bpy.context.view_layer.update()
    hc = PIP.neck.matrix_world @ Vector((0, 0, PIP.head_c))
    cam_push(hc + Vector((-1.25, -1.35, 0.12)), hc + Vector((0.0, 0.05, -0.18)), 42, 0.05 * ease(u))


CART_POS = Vector((-1.35, -1.85, 0))


def products(t, show_coins):
    """The cart: orange can (tall coin stack) next to the two cheap bottles (one coin each) - price as a picture."""
    CART.location = CART_POS
    set_vis(CART, True)
    top = CART_POS + Vector((0, 0, 0.92))
    items = [(OCAN, top + Vector((-0.2, -0.05, 0)), 5), (SHAMPOO, top + Vector((0.0, -0.05, 0.005)), 1),
             (FOOTP, top + Vector((0.2, -0.05, -0.01)), 1)]
    for i, (p, pos, n) in enumerate(items):
        p.matrix_world = Matrix.Translation(pos)
        set_vis(p, True)
        if show_coins > 0:
            k = eback(cl((show_coins - 0.15 * i) / 0.5), 2.0)
            if k > 0:
                s = coin_stack(pos + Vector((0, -0.12, 0.3)), n, f"coins{i}")
                s.scale = (k, k, k)
                s.location = (pos + Vector((0, -0.12, 0.3))) * (1 - k)
    return items


def anim_D(fr):
    """'Price. Dry shampoo or foot powder works too...' Over the cart: coins pop over each product on 'Price' (tall stack on
    the orange can, one coin on each cheap bottle). Gus grabs the dry shampoo and puffs it on the front door; a check pops."""
    t, u = fr / FPS, prog(fr, "D")
    tp = wt(4, "price")
    products(t, (t - tp) / 0.6)
    t_go = wt(4, "works")
    if t < t_go - 0.35:
        char_pose(GUS, t, (-1.35, -1.25, 0), (-0.6, -4.0), look=(0, 0.3), armL=(-20, 0, 6), armR=(-20, 0, -6))
        char_pose(PIP, t, (-0.45, -2.05, 0), (-1.35, -1.8), head=(-6, 0, 0), look=(-0.4, 0.3))
        cam_push((-0.7, -3.9, 1.6), (-1.2, -1.7, 1.05), 30, 0.05 * ease(u))
    else:
        k = ease((t - (t_go - 0.35)) / 0.35)
        set_vis(SHAMPOO, False)
        char_pose(GUS, t, (0.4, -1.6, 0), (0.35, -0.8), look=(0, 0.25))
        aim_arm(GUS, "R", DOOR_AIM + Vector((0, -0.5, 0.05)))
        noz = hold_prop(SHAMPOO, GUS, "R", face=DOOR_AIM)
        d = (DOOR_AIM - noz).normalized()
        for j in range(4):
            puff_col(noz, d, t - t_go - 0.25 * j, "powder", seed=40 + j, reach=0.4, size=0.09)
        draw_powder(powder_spots(), ease((t - t_go) / 1.0))
        ck = eback((t - (T1(4) - 0.1)) / 0.3, 2.0)
        if ck > 0:
            g = temp(empty("chk"))
            p = DOOR_AIM + Vector((0.0, -0.25, 0.45))
            box("chk1", (0.03, 0.01, 0.1 * ck), p + Vector((-0.04, 0, -0.02)), emit("sage_l", 1.6), g, rot=(0, 40, 0))
            box("chk2", (0.03, 0.01, 0.2 * ck), p + Vector((0.04, 0, 0.02)), emit("sage_l", 1.6), g, rot=(0, -30, 0))
        char_pose(PIP, t, (1.3, -2.0, 0), (0.4, -1.0), head=(-8, 0, 0), look=(-0.3, 0.3))
        cam_push((1.25, -3.6, 1.35), (0.35, -1.0, 0.85), 30, 0.03 + 0.04 * k)


def anim_E(fr):
    """'...but then you have to wipe it all off.' Gus wipes the door, and wipes; powder left in the gaps; the cloth goes grey.
    Last ~0.9 s: the wall clock spins (running gag)."""
    t, u = fr / FPS, prog(fr, "E")
    f0, f1 = SF["E"]
    t_clock = f1 / FPS - 0.9
    wk = ease((t - f0 / FPS) / max(0.5, t_clock - f0 / FPS + 0.6))
    xw = lerp(1.0, -0.35, wk)
    zw = 0.72 + 0.17 * math.sin(t * 13)
    draw_powder(powder_spots(), 1.0, wiped_x=xw + 0.06, keep=0.14)
    if t < t_clock:
        char_pose(GUS, t, (xw - 0.45, -1.4, 0.01 * abs(math.sin(t * 13))), (xw, -0.8), look=(0, 0.25), head=(-6, 0, 0))
        p = Vector((xw, -0.905, zw))
        aim_arm(GUS, "R", p)
        hand_to(GUS, "R", p + Vector((0, -0.03, 0)))
        cloth_at(p + Vector((0, -0.012, 0)), wk)
        char_pose(PIP, t, (2.35, -1.35, 0), (0.6, -1.0), head=(-6, 0, 0), look=(-0.4, 0.3))
        cam_push((1.9, -3.3, 1.3), (0.25, -0.95, 0.8), 30, 0.04 * ease(u))
    else:
        k = (t - t_clock) / 0.9
        HANDS["minute"].rotation_euler = (0, math.radians(60 + 1500 * k), 0)
        HANDS["hour"].rotation_euler = (0, math.radians(300 + 125 * k), 0)
        HANDS["second"].rotation_euler = (0, math.radians(200 + 6000 * k), 0)
        for o in clock_blur(CLOCK, HANDS):
            temp(o)
        bpy.context.view_layer.update()
        c = CLOCK.matrix_world.translation
        look(cam, c + Vector((0.15, -1.9, -0.05)), c, 45)


def anim_F(fr):
    """'Is it done yet?' Pip bouncing, impatient, in front of the half-wiped door."""
    t, u = fr / FPS, prog(fr, "F")
    draw_powder(powder_spots(), 1.0, wiped_x=-0.35, keep=0.14)
    char_pose(PIP, t, (0.55, -1.75, 0.05 * abs(math.sin(t * 10))), (1.2, -3.6), head=(-12, 0, 0), look=(0.2, 0.4),
              armL=(-40 + 15 * math.sin(t * 10), 0, 14), armR=(-40 - 15 * math.sin(t * 10), 0, -14))
    char_pose(GUS, t, (-0.4, -1.55, 0), (-0.2, -0.8), look=(0, 0.2))
    bpy.context.view_layer.update()
    hc = PIP.neck.matrix_world @ Vector((0, 0, PIP.head_c))
    cam_push(hc + Vector((0.45, -1.6, 0.1)), hc + Vector((-0.1, 0, -0.2)), 42, 0.06 * ease(u))


def anim_G(fr):
    """'...No. Still some in the grille.' Low front 3/4: Gus at the grille with the grey cloth, powder still in the slats."""
    t, u = fr / FPS, prog(fr, "G")
    sp = grille_powder()
    k_left = lerp(1.0, 0.45, ease((t - T(7)) / 1.6))
    draw_powder(sp, k_left, name="gpowder")
    p = Vector((2.06, -0.35 + 0.18 * math.sin(t * 5), 0.52))
    char_pose(GUS, t, (2.75, 0.55, 0), (2.05, -0.1), look=(0, 0.35), head=(-10, 0, 0))
    aim_arm(GUS, "R", p)
    hand_to(GUS, "R", p + Vector((0.03, 0, 0)))
    cloth_at(p + Vector((0.02, 0, 0)), 1.0)
    cam_push((3.75, -2.15, 0.85), (2.0, -0.3, 0.55), 30, 0.05 * ease(u))


EXO_AT = Vector((0.0, 0, 0))


def anim_H(fr):
    """'So vanishing spray wins?' Pip, excited, hands up; Gus with the grey cloth."""
    t, u = fr / FPS, prog(fr, "H")
    up = ease((t - T(8)) / 0.3)
    char_pose(PIP, t, (0.6, -1.9, 0.03 * up * abs(math.sin(t * 9))), (1.2, -3.6), head=(-12, 0, 0), look=(0.2, 0.4),
              armL=(lerp(-25, -150, up), 0, 18), armR=(lerp(-25, -150, up), 0, -18))
    char_pose(GUS, t, (-0.4, -1.65, 0), (0.6, -1.9), armL=(4, 0, 6), armR=(-20, 0, -8), elbowR=-30)
    bpy.context.view_layer.update()
    cloth_at(GUS.hands["R"].matrix_world.translation + Vector((0, 0, 0.02)), 1.0)
    cam_push((1.4, -4.2, 1.2), (0.1, -1.7, 0.8), 30, 0.05 * ease(u))


def anim_I(fr):
    """'On an expensive car you don't want to touch? Every time.' The sedan is gone; a gleaming blue exotic rolls in with
    sparkles. Gus looks at the grey cloth, then hides it behind his back."""
    t, u = fr / FPS, prog(fr, "I")
    set_vis(CAR, False)
    set_vis(EXOTIC, True)
    rk = eout((t - (T(9) - 0.25)) / 1.1)
    EXOTIC.location = (lerp(5.5, 0.0, rk), 0, 0)
    for i, (x, z, ph) in enumerate(((1.6, 0.85, 0.0), (-0.3, 1.2, 0.35), (0.9, 0.62, 0.7), (-1.6, 0.8, 1.05))):
        sk = ((t - wt(9, "expensive") - ph) % 1.4) / 0.45
        if t > wt(9, "expensive") - 0.1:
            sparkle(EXOTIC.matrix_world @ Vector((x, -0.99, z)), sk, f"sp{i}")
    hide = ease((t - wt(9, "every")) / 0.4)
    char_pose(GUS, t, (-0.3, -2.05, 0), (0.6, -1.0), look=(0.1, 0.25), armL=(4, 0, 6),
              armR=(lerp(-25, 40, hide), 0, lerp(-10, -5, hide)), elbowR=lerp(-35, -10, hide))
    bpy.context.view_layer.update()
    hp = GUS.hands["R"].matrix_world.translation
    if hide < 0.8:
        cloth_at(hp + Vector((0, 0, 0.02)), 1.0)
    char_pose(PIP, t, (1.35, -2.15, 0), (0.8, -0.9), head=(-8, 0, 0), look=(-0.2, 0.3))
    cam_push((1.6, -4.5, 1.95), (0.3, -0.8, 0.7), 26, 0.04 * ease(u))


SCAN_EXO = dict(pos=(1.75, -1.15, 1.45), aim=(1.55, -0.25, 0.8))


def anim_J(fr):
    """'But on a hot day, it can vanish mid-scan.' Sun pops up; the coat on the exotic's nose fades in patches while Gus
    scans; the stripes and the scan patch get holes where the coat is gone; Gus re-sprays a panel (orange can)."""
    t, u = fr / FPS, prog(fr, "J")
    set_vis(CAR, False)
    set_vis(EXOTIC, True)
    EXOTIC.location = (0, 0, 0)
    sp = exo_coat_spots()
    tf = wt(10, "vanish")
    fade = ease((t - (tf - 0.2)) / 1.1)
    t_re = T1(10) + 0.15
    re = ease((t - t_re) / 0.5)
    rng = random.Random(9)
    alive = []
    for p, nrm, r in sp:
        # patches: spots on the sun side (-x of the hood) go first, randomly
        thr = 0.15 + 0.85 * rng.random() * (0.55 + 0.45 * cl((p.x - 1.0) / 1.1))
        gone = fade > thr and not (re > 0 and p.x > 1.55 - 1.4 * (1 - re))
        if not gone:
            alive.append((p, nrm, r))
    draw_dust(alive, len(alive), "exocoat")
    char_pose(GUS, t, (1.2, -1.55, 0), (1.6, -0.2), look=(0, 0.35), head=(-10, 0, 0))
    if re <= 0:
        pj, cm = hold_scanner(GUS, SCAN_EXO["pos"], SCAN_EXO["aim"])
        rows = stripes("exo", pj, SCAN_EXO["aim"], n=15, half_w=0.34, half_h=0.3, samples=80)
        tree = KDT(alive)

        def ok(h):
            if h is None or not h[3].startswith("exo_"):
                return None
            _, _, dist = tree.find(Vector(h[0]))
            return (h[0], h[1], "paint", h[3]) if dist is not None and dist < 0.045 else None
        rows2 = [[ok(h) for h in row] for row in rows]
        draw_stripes(rows2, cats=("paint",))
        beam_sheet(pj, rows, 0.06)
        scan_patch(rows2, ease((t - T(10)) / 0.9), SCAN_EXO["aim"], offset=0.016)
    else:
        set_vis(EPSCAN, False)
        aim_arm(GUS, "R", Vector((1.5, -0.3, 0.85)))
        noz = hold_prop(OCAN, GUS, "R", face=(1.5, 0, 0.8))
        d = (Vector((1.5, -0.3, 0.8)) - noz).normalized()
        for j in range(3):
            puff_col(noz, d, t - t_re - 0.25 * j, "white", seed=60 + j, reach=0.45)
    sun_k = ease((t - (T(10) + 0.05)) / 0.35)
    char_pose(PIP, t, (30, 30, 0), None)
    cam_push((2.85, -2.5, 1.65), (1.45, -0.35, 0.85), 30, 0.04 * ease(u))
    sun_icon(sun_k, t)


def KDT(spots):
    from mathutils.kdtree import KDTree
    kd = KDTree(max(1, len(spots)))
    for i, (p, n, r) in enumerate(spots):
        kd.insert(Vector(p), i)
    kd.balance()

    class _W:
        def find(self, p):
            if not spots:
                return None, None, None
            return kd.find(p)
    return _W()


def anim_K(fr):
    """'So you scan fast.' Gus deadpan close-up, scanner up."""
    t, u = fr / FPS, prog(fr, "K")
    set_vis(CAR, False)
    set_vis(EXOTIC, True)
    EXOTIC.location = (0, 0, 0)
    sp = exo_coat_spots()
    draw_dust(sp, len(sp), "exocoat")
    gl = (1.0, -1.85, 0)
    char_pose(GUS, t, gl, (1.4, -4.2), head=(-4, 0, 0), look=(0.2, 0.1))
    bpy.context.view_layer.update()
    hc = GUS.neck.matrix_world @ Vector((0, 0, GUS.head_c))
    hold_scanner(GUS, hc + Vector((0.32, -0.3, -0.2)), hc + Vector((0.4, -1.4, -0.3)))
    cam_push(hc + Vector((0.55, -1.9, 0.0)), hc + Vector((0.0, 0, -0.2)), 46, 0.04 * ease(u))


def phone_pose(t):
    """The pilot's phone_pose_s11 (Pip holds the phone out, screen along PHONE_N, hand behind the screen plane) with the
    mouth, blinks and eye shapes driven by the timeline instead of a fixed open mouth."""
    m, lid = talk("PIP", t)
    pose(PIP, loc=(1.2, -2.6, 0), rz=14, hips=(-6, 0, 0), head=(-12, 0, -16), armR=(-10, 0, -10), mouth=m, lid=lid,
         look=(0.6, 0.6))
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


PHONE_IMG_DIR = arg("--phonedir", "/home/user/media/ep3/phone")
PHONE_SRC_F0 = int(arg("--phonef0", "0"))   # R1 source frame shown on the screen at shot L's first frame


def anim_L(fr):
    """'Scan fast. Like this?' Pip holds the phone up; the camera pushes along the screen normal until the screen fills the
    frame on the last frame. The screen plays the real AESUB footage (R1) frame for frame, so the hard cut continues it."""
    t, u = fr / FPS, prog(fr, "L")
    set_vis(CAR, False)
    set_vis(EXOTIC, True)
    EXOTIC.location = (0, 0, 0)
    pip_scanner("pouch")
    c, n, up, r = phone_pose(t)
    f = fr - SF["L"][0]
    img = os.path.join(PHONE_IMG_DIR, f"{PHONE_SRC_F0 + f + 1:05d}.png")
    if os.path.exists(img):
        SCREEN.data.materials[0] = tex_emit(img)
    char_pose(GUS, t, (2.6, -1.4, 0), (1.2, -2.6), look=(-0.3, 0.2))
    k = ease(cl((t - (T(12) + 0.25)) / max(0.3, SF["L"][1] / FPS - (T(12) + 0.25))))
    s12_cam(c, n, up, k)


ANIM = {k: globals()[f"anim_{k}"] for k in SF}


def build_cart():
    g = empty("CART")
    box("cart_top", (0.7, 0.45, 0.05), (0, 0, 0.82), mat("metal"), g, 0.01, 0.01)
    box("cart_shelf", (0.66, 0.42, 0.03), (0, 0, 0.3), mat("dark"), g, 0.01, 0.01)
    for x in (-0.31, 0.31):
        for y in (-0.19, 0.19):
            box(f"cart_leg{x}{y}", (0.03, 0.03, 0.72), (x, y, 0.47), mat("dark"), g, ol=0.006)
            cyl(f"cart_wh{x}{y}", 0.05, 0.03, (x, y, 0.05), mat("tyre"), g, axis="Y", seg=16, ol=0.006)
    box("cart_handle", (0.04, 0.5, 0.04), (-0.4, 0, 1.0), mat("sage"), g, 0.01, 0.008)
    for y in (-0.22, 0.22):
        box(f"cart_hpost{y}", (0.03, 0.03, 0.2), (-0.36, y, 0.9), mat("dark"), g)
    return g


CART = build_cart()
set_vis(CART, False)
_SCREEN_KEY_MAT = SCREEN.data.materials[0]
# the pilot's screen quad has no UVs (it was a flat key colour); the footage texture needs them (tl, tr, br, bl)
if not SCREEN.data.uv_layers:
    _uv = SCREEN.data.uv_layers.new(name="UVMap")
    for _li, _lp in enumerate(SCREEN.data.loops):
        _uv.data[_li].uv = [(0, 1), (1, 1), (1, 0), (0, 0)][_lp.vertex_index]


def reset_ep():
    reset()
    pip_scanner("pouch")
    set_vis(PIPSCAN, True)
    set_vis(UI, True)
    for o in (EPSCAN, CAN, CART, OCAN, SHAMPOO, FOOTP, CLOTH, EXOTIC):
        set_vis(o, False)
    set_vis(CAR, True)
    set_vis(TAPE, False)
    open_cabin(False)
    SCREEN.data.materials[0] = _SCREEN_KEY_MAT
    STOOL.location = (-3.7, 2.7, 0)


def open_cabin(on):
    set_vis(CABIN_OPEN, on)
    set_vis(bpy.data.objects["car_cabin"], not on)
    for g_ in GLASS:
        g_.data.materials[0] = GLASS_SEE if on else GLASS_MAT


# ----------------------------------------------------------------------------------------------------------------- run
lo, hi = (int(x) for x in RANGE.split(":")) if RANGE else (-10 ** 9, 10 ** 9)
for sh in EP_SHOTS:
    f0, f1 = SF[sh]
    d = os.path.join(OUT, sh)
    os.makedirs(d, exist_ok=True)
    tsum, nr = 0.0, 0
    for fr in range(f0, f1):
        final = os.path.join(d, f"{fr:04d}.png")
        if not ((fr - f0) % EVERY == 0 and lo <= fr < hi and not os.path.exists(final) and (not ONLY or fr in ONLY)):
            continue
        CUR_T = fr / FPS
        reset_ep()
        ANIM[sh](fr)
        bpy.context.view_layer.update()
        scn.render.filepath = os.path.join(d, f"{fr:04d}_tmp")
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        os.replace(os.path.join(d, f"{fr:04d}_tmp.png"), final)
        tsum += time.time() - t0
        nr += 1
        print(f"[ep3] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if nr:
        print(f"[ep3] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
