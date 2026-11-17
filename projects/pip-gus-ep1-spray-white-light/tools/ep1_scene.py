"""Pip & Gus Ep 1 ("why we spray the windows white") - cartoon part. Executed inside the pilot's scene builder, so the shop,
the cartoon sedan, Pip, Gus (v7 proportions, no brows, nametags) and the cel look are exactly the series' locked assets:

  cd projects/scan-tedium-explainer-reel/tools
  blender -b --factory-startup -P partA_scene.py -- --exec ../../pip-gus-ep1-spray-white-light/tools/ep1_scene.py \
      --out FRAMES_DIR --tl ../../pip-gus-ep1-spray-white-light/ep1_timeline.json [--shots A,B] [--scale 1] [--spp 8]
      [--every N] [--frames 10,20] [--range a:b]

Every frame is posed procedurally from ep1_timeline.json (no keyframes) and written as FRAMES_DIR/<shot>/<frame>.png; frames
already on disk are skipped (written via _tmp + rename), so the render is resumable. Persistent data stays off (lessons).

The structured-light pattern is real geometry: stripes are ray-cast from the scanner's projector lens onto the car's own meshes
(BVH per object), so they bend over the body's creases, pass through see-through glass onto the seats, skip chrome (which
throws a reflected beam instead) and fade on black. The scan patch is built from the same ray hits.
No text, numbers, logos or brands in 3D (the "?" glyph is the only symbol).
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
# chrome beltline trim under the near-side windows and a chrome badge on each front fender
for s in (-1, 1):
    pts = [cab_side(x, z, s, 0.0) + Vector((0, s * dy, 0)) for x in (-1.0, 0.86) for z in (0.985, 1.025) for dy in (0.004, 0.022)]
    CHROME.append(hull(f"ep_trim{s}", pts, mat("chrome", hl=True), CAR, ol=0.006))
    bd = cyl(f"ep_badge{s}", 0.075, 0.016, (1.48, s * (b_["y"] + 0.008), 0.72), mat("chrome", hl=True), CAR, axis="Y", seg=40,
             bevel=0.004, ol=0.008)
    CHROME.append(bd)
    CHROME.append(cyl(f"ep_badge_in{s}", 0.045, 0.02, (1.48, s * (b_["y"] + 0.01), 0.72), mat("chrome_d"), CAR, axis="Y", seg=32))
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


# ----------------------------------------------------------------------------------------------------------------- state over time
T = lambda n: LN[n]["t0"]
T1 = lambda n: LN[n]["t1"]
FRONT_WIN = bpy.data.objects["win_-1_-0.02"]
REAR_WIN = bpy.data.objects["win_-1_-0.98"]


def coat_state(t):
    """What has been sprayed by time t (0..1 each)."""
    s = {}
    s["front_win"] = (lerp(0.35, 0.6, ease((t - 0.2) / 2.2)) if t < wt(10, "glass") else 1.0) if t >= 0 else 0.0
    s["rear_win"] = ease((t - wt(10, "glass")) / 0.45)
    s["trim"] = ease((t - wt(10, "chrome")) / 0.4)
    s["grille"] = ease((t - wt(10, "black")) / 0.4)
    s["badge"] = ease((t - wt(10, "badges")) / 0.4)
    s["squig"] = ease((t - (SF["J"][0] / FPS + 0.1)) / 1.6)
    s["tape"] = t >= SF["J"][0] / FPS
    return s


def win_spots(obj, key, n=900):
    bpy.context.view_layer.update()
    ctr = sum((obj.matrix_world @ v.co for v in obj.data.vertices), Vector()) / len(obj.data.vertices)
    return dust_spots(key, ctr + Vector((0, -0.9, 0.05)), ctr, 0.18, n, [obj], seed=len(key))


def coat_layer(obj, k, out=Vector((0, -0.004, 0))):
    """A matte white skin over a sprayed part that thickens with coverage k (blobs carry the edge, this the solid coat)."""
    a = round(cl((k - 0.3) / 0.6) * 0.92, 2)
    if a < 0.04:
        return
    o = temp(bpy.data.objects.new(obj.name + "_coat", obj.data.copy()))
    COLL.objects.link(o)
    o.data.materials.clear()
    o.data.materials.append(mat("dust", a) if a < 0.9 else mat("dust"))
    o.matrix_world = Matrix.Translation(out) @ obj.matrix_world


def apply_coats(t, skip=()):
    s = coat_state(t)
    if "front_win" not in skip:
        sp = win_spots(FRONT_WIN, "fw")
        draw_dust(sp, len(sp) * s["front_win"], "dust_fw")
        coat_layer(FRONT_WIN, s["front_win"])
    if s["rear_win"] > 0 and "rear_win" not in skip:
        sp = win_spots(REAR_WIN, "rw")
        draw_dust(sp, len(sp) * s["rear_win"], "dust_rw")
        coat_layer(REAR_WIN, s["rear_win"])
    if s["trim"] > 0:
        tr = bpy.data.objects["ep_trim-1"]
        sp = dust_spots("trim", (-0.07, -1.7, 1.15), (-0.07, -0.75, 1.0), 0.45, 110, [tr], seed=5, size=(0.012, 0.022))
        draw_dust(sp, len(sp) * s["trim"], "dust_trim")
    if s["grille"] > 0:
        gr = [bpy.data.objects["grille"], bpy.data.objects["ep_lip"]]
        sp = dust_spots("grille", (3.0, -0.4, 0.6), (2.0, 0, 0.5), 0.35, 160, gr, seed=6, size=(0.02, 0.04))
        draw_dust(sp, len(sp) * s["grille"], "dust_grille")
    if s["badge"] > 0:
        bd = [bpy.data.objects["ep_badge-1"], bpy.data.objects["ep_badge_in-1"]]
        sp = dust_spots("badge", (1.48, -1.5, 0.75), (1.48, -0.85, 0.72), 0.06, 40, bd, seed=7, size=(0.012, 0.022))
        draw_dust(sp, len(sp) * s["badge"], "dust_badge")
    if s["squig"] > 0:
        draw_squiggles(s["squig"])
    set_vis(TAPE, s["tape"])
    return s


# ----------------------------------------------------------------------------------------------------------------- shots
GUS_IDLE = dict(armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12, elbowR=-12)


def prog(fr, sh):
    f0, f1 = SF[sh]
    return (fr - f0) / max(1, f1 - 1 - f0)


def cam_push(loc, target, lens, k):
    loc, target = Vector(loc), Vector(target)
    look(cam, target + (loc - target) * (1 - k), target, lens)


def spray_at(t, ch, target, start, dur=0.5, seed=1, side="R", reach=0.35):
    """Gus sprays target: arm out, can aimed, puff from `start` for `dur`."""
    aim_arm(ch, side, Vector(target) + Vector((0, -0.5, 0.05)))
    noz, d = hold_can(ch, side, target)
    for k in range(int(dur / 0.25) + 1):
        puff(noz, d, t - start - k * 0.25, seed=seed + k, reach=reach)


def anim_A(fr):
    """Hook: front 3/4 of the shop car; Gus dusting the front side window (half done), Pip at his side asks."""
    t, u = fr / FPS, prog(fr, "A")
    apply_coats(t)
    gl = (0.35, -1.58, 0)
    char_pose(GUS, t, gl, (0.4, -0.7), head=(-6, 0, 0), look=(0, 0.3))
    spray_at(t, GUS, (0.45, -0.75, 1.22 + 0.06 * math.sin(t * 3)), 0.0, dur=2.6, seed=int(t * 4))
    char_pose(PIP, t, (-0.55, -2.1, 0.02 * abs(math.sin(t * 7))), (0.35, -1.65), head=(-14, 0, 0), look=(0.3, 0.6),
              armL=(-25, 0, 10), armR=(-25, 0, -10))
    cam_push((3.3, -3.15, 1.35), (-0.05, -1.4, 1.0), 27, 0.06 * ease(u))


EXPR["PIP"].append(("curious", T(1), T1(1), 0.15, 0.3))
EXPR["PIP"].append(("impatient", T(5), T1(5), 0.1, 0.3))
EXPR["PIP"].append(("squint", wt(7, "it"), T1(7) + 0.3, 0.06, 0.25))
EXPR["PIP"].append(("thinking", T(9) - 0.2, T1(9) - 0.5, 0.2, 0.15))
EXPR["PIP"].append(("excited", T1(9) - 0.45, T1(9) + 0.2, 0.08, 0.2))
EXPR["PIP"].append(("curious", T(11), T1(11), 0.12, 0.3))
EXPR["PIP"].append(("excited", T(13), T1(13) + 0.3, 0.1, 0.2))
EXPR["PIP"].append(("excited", T1(4) - 0.6, T1(4) + 0.4, 0.1, 0.2))
EXPR["GUS"].append(("weary", LN[12]["sighs"][0][0], T(12) + 0.3, 0.15, 0.3))
EXPR["GUS"].append(("deadpan", T(14) - 0.2, T1(14) + 1.0, 0.1, 0.2))
EXPR["GUS"].append(("weary", wt(8, "black"), T1(8), 0.1, 0.3))

SCAN_DOOR = dict(pos=(-0.55, -2.05, 0.95), aim=(-0.55, -0.85, 0.85))


def anim_B(fr):
    """'The scanner shines a pattern of light on the car.' Gus aims the scanner at the rear door; the stripes drape over it."""
    t, u = fr / FPS, prog(fr, "B")
    apply_coats(t)
    gl = (-0.55, -2.55, 0)
    char_pose(GUS, t, gl, (-0.55, 0), head=(-4, 0, 0), look=(0, 0.2))
    pj, cm = hold_scanner(GUS, SCAN_DOOR["pos"], SCAN_DOOR["aim"])
    rows = stripes("door", pj, SCAN_DOOR["aim"], n=15, half_w=0.36, half_h=0.36)
    on = ease((t - wt(2, "shines")) / 0.25)
    if on > 0:
        g = ease((t - wt(2, "pattern")) / 0.9)
        draw_stripes(rows, grow=max(0.05, g))
        beam_sheet(pj, rows, 0.08 * on)
    char_pose(PIP, t, (30, 30, 0), None)
    cam_push((1.9, -3.6, 1.35), (-0.6, -1.4, 0.9), 26, 0.08 * ease(u))


def anim_C(fr):
    """'A camera watches the lines bend. From that angle, it knows where every point is.' Close on the door: the stripes kink
    over the beltline crease; the camera lens glints; projector -> point -> camera triangle flashes; the scan patch knits."""
    t, u = fr / FPS, prog(fr, "C")
    apply_coats(t)
    gl = (-0.55, -2.55, 0)
    char_pose(GUS, t, gl, (-0.55, 0), head=(-4, 0, 0), look=(0, 0.2))
    pj, cm = hold_scanner(GUS, SCAN_DOOR["pos"], SCAN_DOOR["aim"])
    rows = stripes("door", pj, SCAN_DOOR["aim"], n=15, half_w=0.36, half_h=0.36)
    draw_stripes(rows)
    beam_sheet(pj, rows, 0.06)
    # camera lens glint on "camera"
    gk = win(t, wt(3, "camera"), wt(3, "camera") + 0.35, 0.05, 0.25)
    if gk > 0:
        ring(cm + Vector((0, -0.02, 0)), (EPSCAN.matrix_world.to_3x3() @ Vector((0, -1, 0))), 0.05 + 0.03 * gk, "camglow", "white")
    # triangle on "angle": dashed projector -> point -> camera
    ta = wt(4, "angle")
    tk = win(t, ta - 0.1, T1(4) - 0.2, 0.15, 0.3)
    hit = rows[9][40] or rows[9][45]
    if tk > 0 and hit:
        p = Vector(hit[0]) + Vector(hit[1]) * 0.01
        dashed(pj, p, "tri_a", key="sage_l")
        dashed(p, cm, "tri_b", key="white")
        dashed(pj, cm, "tri_c", key="white", r=0.006)
        blob("tri_pt", (0.02 * (1 + 0.5 * tk),) * 3, p, emit("white", 2.0), temp(empty("tp")))
    # scan patch knits from "knows" to the end of the line
    kk = ease((t - wt(4, "knows")) / max(0.6, T1(4) - wt(4, "knows") + 0.3))
    if hit:
        scan_patch(rows, kk, hit[0])
    # Pip pops in at the right edge for the ^ ^ at the end of line 4
    pk = ease((t - (T1(4) - 0.7)) / 0.35)
    char_pose(PIP, t, (lerp(0.75, 0.45, pk), -2.1, 0), (-0.55, -0.85), head=(-6, 0, 0), look=(-0.5, 0.2))
    cam_push((0.25, -2.4, 1.15), (-0.6, -1.15, 0.85), 26, 0.05 * ease(u))


def anim_D(fr):
    """'So what's wrong with windows?' Pip points at the bare rear window, impatient."""
    t, u = fr / FPS, prog(fr, "D")
    apply_coats(t)
    pl = (0.05, -1.8, 0)
    char_pose(PIP, t, pl, (0.9, -3.6), head=(-12, 0, 0), look=(0.2, 0.2))
    aim_arm(PIP, "R", (-0.55, -0.75, 1.25))
    char_pose(GUS, t, (-1.15, -2.35, 0), (0.05, -1.8), **GUS_IDLE)
    cam_push((0.95, -3.75, 1.05), (-0.35, -1.35, 1.0), 30, 0.05 * ease(u))


def open_cabin(on):
    set_vis(CABIN_OPEN, on)
    set_vis(bpy.data.objects["car_cabin"], not on)
    for g in GLASS:
        g.data.materials[0] = GLASS_SEE if on else GLASS_MAT


SCAN_WIN = dict(pos=(-0.5, -2.1, 1.25), aim=(-0.55, -0.7, 1.2))


def anim_E(fr):
    """'Light goes straight through glass.' The window is see-through: the stripes skip the glass and land on the seat inside;
    the scan patch has a window-shaped hole."""
    t, u = fr / FPS, prog(fr, "E")
    open_cabin(True)
    apply_coats(t)
    char_pose(GUS, t, (-0.5, -2.6, 0), (-0.5, 0), look=(0, 0.3))
    pj, cm = hold_scanner(GUS, SCAN_WIN["pos"], SCAN_WIN["aim"])
    rows = stripes("win", pj, SCAN_WIN["aim"], n=17, half_w=0.36, half_h=0.3, see_glass=True)
    draw_stripes(rows, cats=("paint",))
    beam_sheet(pj, rows, 0.07)
    # the light through the glass: a separate, brighter set that only shows on the interior (seat) hits
    inner = [[h if (h and (h[3].startswith(("seat", "int_")))) else None for h in row] for row in rows]
    k = ease((t - wt(6, "straight")) / 0.4)
    if k > 0:
        draw_stripes(inner, grow=k, cats=("paint",), name="inner", strength=2.6)
    kk = ease((t - T(6)) / 1.2)
    scan_patch([[h if (h and not h[3].startswith(("seat", "int_"))) else None for h in row] for row in rows], kk,
               Vector(SCAN_WIN["aim"]) + Vector((0.5, 0, -0.35)), offset=0.014)
    cam_push((0.35, -3.05, 1.42), (-0.55, -1.0, 1.15), 34, 0.05 * ease(u))


def anim_F(fr):
    """'Chrome's a mirror. It throws the light away.' The pattern hits the chrome fender badge: no stripes on it, a reflected
    beam flies off and lands on Pip's face; Pip squints."""
    t, u = fr / FPS, prog(fr, "F")
    apply_coats(t)
    open_cabin(False)
    badge = Vector((1.48, -(b_["y"] + 0.02), 0.72))
    spos = (1.05, -1.75, 0.86)
    char_pose(GUS, t, (0.95, -2.3, 0), (1.48, -0.85), look=(0, 0.2))
    pj, cm = hold_scanner(GUS, spos, badge)
    rows = stripes("badge", pj, badge, n=13, half_w=0.2, half_h=0.2, samples=60)
    draw_stripes(rows)
    beam_sheet(pj, rows, 0.06)
    pl = (2.3, -1.55, 0)
    char_pose(PIP, t, pl, (1.3, -2.4), head=(-8, 0, 0), look=(-0.2, 0.3))
    bpy.context.view_layer.update()
    face = PIP.neck.matrix_world @ Vector((0, -0.2, PIP.head_c + 0.02))
    k = ease((t - wt(7, "it")) / 0.35)
    if k > 0:
        tip = badge.lerp(face, k)
        dashed(badge, tip, "refl", dash=0.06, gap=0.02, r=0.016, key="sage_l")
        if k >= 1:
            ring(face + Vector((0, -0.02, 0)), (0, -1, 0), 0.07, "facespot", "sage_l", 0.02)
    # chrome glint pulses on "mirror"
    gk = win(t, wt(7, "mirror"), wt(7, "mirror") + 0.4, 0.05, 0.3)
    if gk > 0:
        blob("glint", (0.03 * gk, 0.005, 0.03 * gk), badge + Vector((0.02, -0.015, 0.03)), emit("white", 2.0), temp(empty("gl")))
    cam_push((1.75, -3.9, 1.0), (1.8, -1.2, 0.85), 30, 0.05 * ease(u))


def anim_G(fr):
    """'And black just swallows it.' Front 3/4 low on the black grille and lip: the stripes there fade to nothing; the patch
    stays empty over the black."""
    t, u = fr / FPS, prog(fr, "G")
    apply_coats(t)
    spos = (3.0, -0.55, 0.95)
    aim = (2.0, -0.05, 0.55)
    char_pose(GUS, t, (3.5, -0.6, 0), (2.0, -0.2), look=(0, 0.3))
    pj, cm = hold_scanner(GUS, spos, aim)
    rows = stripes("grille", pj, aim, n=15, half_w=0.34, half_h=0.26, samples=80)
    fade = 1 - ease((t - wt(8, "swallows")) / 0.6)
    draw_stripes(rows, black_alpha=fade)
    beam_sheet(pj, rows, 0.06)
    scan_patch(rows, ease((t - T(8)) / 1.0), aim)
    cam_push((3.6, -2.4, 0.75), (2.0, -0.25, 0.6), 30, 0.05 * ease(u))


def anim_H(fr):
    """'So you only spray the tricky bits?' Close on Pip working it out (one eye narrows), then ^ ^ as it clicks."""
    t, u = fr / FPS, prog(fr, "H")
    apply_coats(t)
    pl = (1.0, -2.1, 0)
    char_pose(PIP, t, pl, (1.6, -3.6), head=(-10, 0, 8 * math.sin(t * 2)), look=(-0.3, 0.4))
    char_pose(GUS, t, (-0.2, -1.75, 0), (1.0, -2.1), **GUS_IDLE)
    bpy.context.view_layer.update()
    hc = PIP.neck.matrix_world @ Vector((0, 0, PIP.head_c))
    cam_push(hc + Vector((0.55, -1.75, 0.1)), hc + Vector((-0.05, 0, -0.12)), 50, 0.06 * ease(u))


I_SPOTS = None


def anim_I(fr):
    """'Glass. Chrome. Black. Badges. Now the light comes back.' One puff per word (rear window, beltline trim, grille,
    badge), Gus zipping between them; then the pattern sweeps the whole side and reads crisp everywhere, the patch fills."""
    t, u = fr / FPS, prog(fr, "I")
    apply_coats(t)
    marks = [("glass", (-0.55, -1.85, 0), (-0.55, -0.74, 1.22)), ("chrome", (0.1, -1.8, 0), (0.1, -0.76, 1.0)),
             ("black", (2.75, -0.95, 0), (2.02, -0.2, 0.55)), ("badges", (1.5, -1.65, 0), (1.48, -0.86, 0.72))]
    times = [wt(10, w) for w, _, _ in marks]
    # Gus position: slides to each mark just before its word
    k = 0
    for i, tm in enumerate(times):
        if t >= tm - 0.28:
            k = i
    tm = times[k]
    prev = marks[max(0, k - 1)][1]
    mv = ease((t - (tm - 0.28)) / 0.22) if k > 0 else 1.0
    gl = lerpv(prev, marks[k][1], mv)
    after = t > times[-1] + 0.55
    if not after:
        char_pose(GUS, t, gl, marks[k][2][:2], look=(0, 0.3), hips=(-6 * (1 - mv), 0, 0))
        spray_at(t, GUS, marks[k][2], tm - 0.05, dur=0.3, seed=11 + k, reach=0.3)
    else:
        char_pose(GUS, t, (1.15, -2.35, 0), (0.6, -0.8), look=(0, 0.2))
        spos = (0.25, -2.45, 1.05)
        aim = (0.4, -0.7, 0.85)
        pj, cm = hold_scanner(GUS, spos, aim)
        rows = stripes("side", pj, aim, n=25, half_w=0.75, half_h=0.32, samples=110, coated=True)
        sw = ease((t - wt(10, "light")) / 0.8)
        keep = int(len(rows) * sw)
        draw_stripes(rows[:max(1, keep)])
        beam_sheet(pj, rows[:max(1, keep)], 0.06)
        scan_patch(rows, ease((t - wt(10, "comes")) / 1.0), aim)
    char_pose(PIP, t, (1.6, -2.4, 0), (2.4, -1.2), look=(0.0, 0.3), armL=(-25, 0, 10), armR=(-25, 0, -10))
    cam_push((4.3, -3.9, 1.5), (1.35, -1.0, 0.8), 24, 0.04 * ease(u))


def anim_J(fr):
    """'Why the squiggles?' Gus sprays loose squiggles on the plain rear door; tape strips already sit on the roof."""
    t, u = fr / FPS, prog(fr, "J")
    s = apply_coats(t)
    paths = squiggle_paths()
    tot = len(paths) * 25
    n = int(tot * s["squig"])
    pi_ = min(len(paths) - 1, n // 25)
    tip = paths[pi_][min(25, n - pi_ * 25)]
    char_pose(GUS, t, (tip.x - 0.4, -1.45, 0), (tip.x, -0.85), look=(0, 0.2))
    spray_at(t, GUS, tip, SF["J"][0] / FPS, dur=2.0, seed=31, reach=0.25)
    char_pose(PIP, t, (0.85, -1.45, 0), (-0.5, -1.45), head=(-8, 0, 0), look=(0.3, 0.3))
    cam_push((1.6, -3.0, 1.4), (-0.55, -0.95, 0.78), 27, 0.05 * ease(u))


def anim_K(fr):
    """'Smooth panels all look the same. It needs something to track.' Over the scanner: the plain front door gets a '?'; the
    view pans to the squiggled rear door and the taped roof, and sage tracking rings lock onto them."""
    t, u = fr / FPS, prog(fr, "K")
    apply_coats(t)
    t_track = wt(12, "it")
    pan = ease((t - (t_track - 0.35)) / 0.7)
    tgt = lerpv((0.45, -0.85, 0.7), (-0.55, -0.85, 0.82), pan)
    spos = Vector(lerpv((0.45, -2.0, 0.9), (-0.55, -2.0, 0.95), pan))
    char_pose(GUS, t, (30, 31, 0), None)
    pj, cm = hold_scanner(GUS, spos, tgt)
    q = win(t, wt(12, "smooth") + 0.2, t_track - 0.4, 0.12, 0.2)
    if q > 0:
        qmark(Vector((0.45, -1.55, 1.25 + 0.03 * math.sin(t * 6))), 0.38 * eback(q), "qm")
    if t >= t_track - 0.1:
        rows = stripes("rear", pj, (-0.55, -0.85, 0.82), n=15, half_w=0.36, half_h=0.36)
        draw_stripes(rows)
        paths = squiggle_paths()
        for i, pts in enumerate(paths):
            lk = eback((t - (wt(12, "something") + 0.12 * i)) / 0.25, 2.0)
            if lk > 0:
                ring(pts[12] + Vector((0, -0.012, 0)), (0, -1, 0), lerp(0.12, 0.05, cl(lk)), f"rk{i}", "sage_l", 0.007)
        tk = eback((t - wt(12, "track")) / 0.25, 2.0)
        if tk > 0:
            for i in range(3):
                tp = bpy.data.objects[f"tape{i + 1}"].matrix_world.translation + Vector((0, 0, 0.01))
                ring(tp, (0, 0, 1), lerp(0.12, 0.06, cl(tk)), f"rt{i}", "sage_l", 0.007)
    else:
        rows = stripes("front", pj, (0.45, -0.85, 0.7), n=15, half_w=0.36, half_h=0.36)
        draw_stripes(rows)
    look(cam, spos + Vector((0.25, -0.75, 0.55)), Vector(tgt) + Vector((0, 0, 0.1)), 30)


def hand_to(ch, side, p):
    """Floating hands: put a hand exactly at world point p."""
    bpy.context.view_layer.update()
    h = ch.hands[side]
    h.matrix_world = Matrix.Translation(Vector(p)) @ h.matrix_world.to_3x3().to_4x4()


def anim_L(fr):
    """'Does it come off?' Pip pokes the dusted front window: a fingertip print in the coat."""
    t, u = fr / FPS, prog(fr, "L")
    apply_coats(t)
    pl = (0.85, -1.15, 0)
    poke = Vector((0.55, -0.757, 1.15))
    char_pose(PIP, t, pl, (0.3, -2.2), head=(-10, 0, 0), look=(-0.6, 0.4))
    k = ease((t - (T(13) - 0.15)) / 0.25)
    hand_to(PIP, "R", poke + Vector((0.0, -0.06 - 0.25 * (1 - k), 0)))
    if t >= T(13) + 0.1:
        blob("print", (0.022, 0.004, 0.03), poke + Vector((0, -0.009, 0)), mat("glass"), temp(empty("pr")))
    char_pose(GUS, t, (-0.55, -1.9, 0), (0.6, -1.45), **GUS_IDLE)
    cam_push((1.4, -3.0, 1.35), (0.65, -1.0, 1.1), 34, 0.05 * ease(u))


def anim_M(fr):
    """'...Depends on the spray.' Gus deadpan close-up, can in hand."""
    t, u = fr / FPS, prog(fr, "M")
    apply_coats(t)
    gl = (-0.2, -1.9, 0)
    char_pose(GUS, t, gl, (1.0, -3.5), head=(-4, 0, 0), look=(0.2, 0.1), armL=(4, 0, 6), armR=(-35, 0, -10), elbowR=-50)
    bpy.context.view_layer.update()
    hp = GUS.hands["R"].matrix_world.translation
    CAN.matrix_world = Matrix.Translation(hp + Vector((0, 0, 0.05)))
    set_vis(CAN, True)
    char_pose(PIP, t, (30, 30, 0), None)
    hc = GUS.neck.matrix_world @ Vector((0, 0, GUS.head_c))
    cam_push(hc + Vector((0.6, -1.9, 0.0)), hc + Vector((0.0, 0, -0.18)), 48, 0.04 * ease(u))


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


def anim_O(fr):
    """Series callback (v0.4): 'We scan the car.' Gus wheels the scanner over on a cart, Pip trots behind; the car waits."""
    t, u = fr / FPS, prog(fr, "O")
    k = eout(u * 1.15)
    cx = lerp(-3.1, -1.25, k)
    CART.location = (cx, -1.75, 0)
    set_vis(CART, True)
    bob = 0.015 * abs(math.sin(t * 9)) * (1 - k)
    char_pose(GUS, t, (cx - 0.75, -1.75, bob), (cx + 2, -1.75), look=(0.3, 0.1), hips=(-8 * (1 - k), 0, 0))
    aim_arm(GUS, "L", (cx - 0.4, -1.55, 1.0))
    aim_arm(GUS, "R", (cx - 0.4, -1.95, 1.0))
    place_scanner((cx + 0.05, -1.75, 0.92), (cx + 0.05, -0.8, 0.9))
    char_pose(PIP, t, (cx - 1.35, -2.05, 0.04 * abs(math.sin(t * 11))), (cx, -1.6), head=(-12, 0, 0), look=(0.4, 0.4))
    cam_push((1.3, -4.0, 1.0), (-1.6, -1.6, 0.62), 28, 0.03 * ease(u))


ANIM = {k: globals()[f"anim_{k}"] for k in SF}


def reset_ep():
    reset()
    pip_scanner("pouch")
    set_vis(PIPSCAN, True)
    set_vis(UI, True)
    set_vis(EPSCAN, False)
    set_vis(CAN, False)
    set_vis(CART, False)
    open_cabin(False)
    STOOL.location = (-3.7, 2.7, 0)


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
        print(f"[ep1] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if nr:
        print(f"[ep1] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
