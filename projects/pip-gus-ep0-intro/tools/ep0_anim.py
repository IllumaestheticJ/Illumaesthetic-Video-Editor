"""Pip & Gus Ep 0 "Meet Pip & Gus" - cartoon animation. Runs INSIDE the pilot's scene builder (same characters, shop, rig,
cel look), via its --exec hook:

  cd projects/scan-tedium-explainer-reel/tools
  blender -b --factory-startup -P partA_scene.py -- --exec ../../pip-gus-ep0-intro/tools/ep0_anim.py \
      --out /home/user/media/work/pip-gus-ep0/frames --spp 4 --ep0shots A,B [--every N] [--frames 50,120] [--scale 0.5]

Every frame is posed procedurally from ep0_timeline.json (word times of the approved take 2): reset, anim_<shot>(frame),
render. Frames land in OUT/<shot>/<frame>.png (written via _tmp + rename, existing frames skipped: resumable).
The phone shot (E) writes OUT/screen_corners.json for compositing the Lola / C5 / MR2 1:1 cuts into the key-colour screen.

Owner rules honoured here: Gus is warm (never sad / never annoyed in this episode), Pip curious -> excited; dot eyes, no
brows (eye shapes only), no arms, nametags; no text in 3D except the Illumaesthetic logo on the banner (owner asset).
"""
import re as _re

EP = "/home/user/Illumaesthetic-Video-Editor/projects/pip-gus-ep0-intro"
TL = json.load(open(os.path.join(EP, "ep0_timeline.json")))
FPS = TL["fps"]
LN = {L["n"]: L for L in TL["lines"]}
EVERY = int(arg("--every", "1"))
ONLY = {int(x) for x in arg("--frames", "").split(",") if x}
TEX = "/home/user/media/work/scan-tedium/tex"

# shot grid (reel frames, f1 exclusive). Cuts on the music beats (2.4203 s + 0.6 k) except H1-H4, cut on Gus's words.
SHOT_LIST = [("A", 0, 109), ("B", 109, 199), ("C", 199, 289), ("D", 289, 397), ("E", 397, 505), ("F", 505, 649),
             ("G", 649, 752), ("H1", 752, 778), ("H2", 778, 814), ("H3", 814, 842), ("H4", 842, 865), ("I", 865, 973),
             ("J", 973, 1027), ("K", 1027, 1135)]
SF = {s: (a, b) for s, a, b in SHOT_LIST}
EP_SHOTS = [s for s in arg("--ep0shots", ",".join(SF)).split(",") if s]


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
    x = cl(x) - 1
    return 1 + x * x * ((s + 1) * x + s)


def lerp(a, b, t):
    return a + (b - a) * t


def lerpv(a, b, t):
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


def prog(fr, sh):
    f0, f1 = SF[sh]
    return (fr - f0) / max(1, f1 - 1 - f0)


def W(n, i):
    """time of word i of line n"""
    return LN[n]["words"][i]["t0"]


# ----------------------------------------------------------------------------------------------------------------- talk (pilot logic)
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
    return m


def accent(spk, t):
    return 1.8 * max([math.exp(-((t - ta - 0.04) / 0.12) ** 2) for ta in STRESS[spk]] + [0.0])


def _blinks(seed):
    rng = random.Random(seed)
    out, x = [], rng.uniform(0.3, 1.4)
    while x < 45:
        out.append(x)
        x += rng.uniform(2.0, 3.6)
    return out


BLINKS = {"PIP": _blinks(21), "GUS": _blinks(47)}
# owner rule "never sad": a blink on Gus's "..." pause before "There's a lot to cover" read as weary - keep his eyes open there
BLINKS["GUS"] = [b for b in BLINKS["GUS"] if not (LN[10]["t0"] - 0.6 <= b <= LN[10]["t1"])]


def blink(spk, t):
    v = 0.0
    for b in BLINKS[spk]:
        u = (t - b) / 0.14
        if 0 <= u < 1:
            v = max(v, 1 - abs(2 * u - 1))
    return v


def talk(spk, t, base_lid=0.0):
    return mouth_at(spk, t), max(base_lid, blink(spk, t), 0.2 * accent(spk, t))


def win(t, a, b, rin=0.12, rout=0.2):
    if t < a - rin or t > b + rout:
        return 0.0
    if t < a:
        return ease((t - (a - rin)) / rin)
    if t <= b:
        return 1.0
    return 1 - ease((t - b) / rout)


# ----------------------------------------------------------------------------------------------------------------- faces (no brows)
for _ch in (GUS, PIP):
    for _b in _ch.browset:
        for _o in list(_b["piv"].children) + [_b["piv"]]:
            bpy.data.objects.remove(_o, do_unlink=True)
    _ch.browset = []

CUR_T = 0.0
STATES = {   # name: (fL, fR, shape, scale, tL, tR)
    "neutral": (0.0, 0.0, None, 1.0, 0, 0),
    "curious": (0.0, 0.0, None, 1.15, 0, 0),
    "surprised": (0.0, 0.0, None, 1.3, 0, 0),
    "excited": (0.0, 0.0, "arc", 1.0, 0, 0),
    "squeezed": (1.0, 1.0, "line", 1.0, 0, 0),
}
PUFF_T = W(9, 3)   # "spray" - the powder puff lands on Pip


def expr_state(ch, t):
    nm = "GUS" if ch is GUS else "PIP"
    st = dict(fL=0.0, fR=0.0, shape=None, scale=1.0, tL=0.0, tR=0.0)

    def blend(name, k):
        if k <= 0:
            return
        tgt = dict(zip(("fL", "fR", "shape", "scale", "tL", "tR"), STATES[name]))
        for key in ("fL", "fR", "scale", "tL", "tR"):
            st[key] = lerp(st[key], tgt[key], k)
        if tgt["shape"] and k > 0.5:
            st["shape"] = tgt["shape"]

    if nm == "GUS":
        # warm and friendly (owner: never sad): round dots, happy arcs on "Hi", on "so long" and while amused at white Pip
        blend("excited", win(t, W(1, 0) + 0.05, LN[1]["t1"], 0.08, 0.25))
        blend("excited", win(t, W(4, 21), LN[4]["t1"] + 0.3, 0.1, 0.3))      # "so long." - proud smile
        blend("curious", win(t, W(6, 0), LN[6]["t1"], 0.15, 0.3) * 0.6)
        blend("excited", win(t, W(10, 2), LN[10]["t1"] + 0.6, 0.1, 0.3))    # "...a lot to cover."
    else:
        blend("excited", win(t, W(2, 0), LN[3]["t1"] + 0.2, 0.08, 0.3))
        blend("curious", win(t, LN[4]["t0"], LN[4]["t1"], 0.2, 0.2))
        blend("curious", win(t, LN[5]["t0"], LN[5]["t1"], 0.1, 0.2))
        blend("excited", win(t, W(7, 2), LN[7]["t1"] + 0.3, 0.08, 0.3))
        blend("excited", win(t, LN[9]["t0"], PUFF_T - 0.12, 0.08, 0.06))     # giggly "And why..."
        # puff: pop on impact, squeezed shut inside the cloud, then round blinking eyes
        if PUFF_T - 0.06 <= t < PUFF_T + 0.12:
            blend("surprised", 1.0)
        elif PUFF_T + 0.12 <= t < PUFF_T + 1.05:
            blend("squeezed", 1.0)
        blend("curious", win(t, LN[11]["t0"] - 0.2, LN[11]["t1"] + 1.4, 0.2, 0.2))
    return st


def apply_expr(ch, lid_call=0.0, look_call=(0, 0)):
    st = expr_state(ch, CUR_T)
    fl, fr = max(lid_call, st["fL"]), max(lid_call, st["fR"])
    shaped = bool(st["shape"]) or max(fl, fr) > 0.08
    sc = st["scale"] * (1.1 if (shaped and st["scale"] < 1.05) else 1.0)
    if st["shape"]:
        set_eyes(ch, 0, 0, shape=st["shape"], scale=sc)
    else:
        set_eyes(ch, fl, fr, scale=sc)
    for e in ch.eyeset:
        e["piv"].rotation_euler = (0, 0, 0)


_pose_base = pose


def pose(ch, *a, **kw):
    _pose_base(ch, *a, **kw)
    apply_expr(ch, max(ch.S.get("base_lid", 0.0), kw.get("lid", 0.0)), kw.get("look", (0, 0)))


def cam_push(loc, target, lens, k, up=(0, 0, 1)):
    loc, target = Vector(loc), Vector(target)
    look(cam, target + (loc - target) * (1 - k), target, lens, up=up)


# ----------------------------------------------------------------------------------------------------------------- props
def path_tube(name, pts, rt, m, parent=None, loc=(0, 0, 0), rs=10):
    """Closed tube along a polyline (the cartoon question mark)."""
    bm = bmesh.new()
    pts = [Vector(p) for p in pts]
    rings = []
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        a = t.orthogonal().normalized()
        b = t.cross(a)
        rings.append([bm.verts.new(p + (a * math.cos(2 * math.pi * k / rs) + b * math.sin(2 * math.pi * k / rs)) * rt)
                      for k in range(rs)])
    for i in range(len(rings) - 1):
        for k in range(rs):
            bm.faces.new((rings[i][k], rings[i + 1][k], rings[i + 1][(k + 1) % rs], rings[i][(k + 1) % rs]))
    for r_ in (rings[0], rings[-1]):
        bm.faces.new(r_)
    _smooth(bm)
    return new_obj(name, bm, [m], parent, loc)


def qmark(name, s=1.0, key="sage"):
    """Cartoon '?' in the XZ plane (faces -y), height ~0.36 s, outlined."""
    g = empty(name)
    pts = []
    for i in range(19):   # hook: from the left, over the top, down the right, curling back to the centre
        a = math.radians(160 - 250 * i / 18)
        pts.append((0.085 * s * math.cos(a), 0, 0.12 * s + 0.085 * s * math.sin(a)))
    pts += [(0.0, 0, 0.0), (0.0, 0, -0.045 * s)]
    ob = path_tube(name + "_hook", pts, 0.026 * s, mat(key, hl=True), g)
    add_mods(ob, 0, 0.012 * s, char=True)
    ob.data.materials.append(OUTLINE)
    blob(name + "_dot", (0.03 * s, 0.03 * s, 0.03 * s), (0, 0, -0.12 * s), mat(key, hl=True), g, ol=0.012 * s)
    for o in g.children_recursive:   # falling '?' shadows swept across Gus's face in G - no shadows from them
        o.visible_shadow = False
    return g


def build_banner():
    """Sage banner with the Illumaesthetic logo panel (owner's logo asset), hung over the car; unrolls from the top bar."""
    g = empty("BANNER")
    w, h = 2.0, 0.6
    cyl("ban_bar", 0.045, w + 0.25, (0, 0, 0), mat("dark"), g, axis="X", ol=0.015)
    cloth = empty("ban_cloth", g)
    bm = bmesh.new()
    vs = [bm.verts.new(c) for c in ((-w / 2, 0, -h), (w / 2, 0, -h), (w / 2, 0, 0), (-w / 2, 0, 0))]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new("UVMap")
    for lp, co in zip(f.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        lp[uv].uv = co
    face = new_obj("ban_face", bm, [tex_emit(os.path.join(TEX, "banner_logo.png"))], cloth)
    roll = cyl("ban_roll", 0.04, w + 0.04, (0, 0, -h), mat("sage"), cloth, axis="X", ol=0.015)
    g.location = (0.05, -0.6, 2.62)
    return g, cloth, face, roll


BANNER, BAN_CLOTH, BAN_FACE, BAN_ROLL = build_banner()


def banner_unroll(k):
    """k 0 rolled up .. 1 fully down: the face scales from the top bar, the roll rides its bottom edge."""
    k = max(0.02, k)
    BAN_FACE.scale = (1, 1, k)
    BAN_ROLL.location = (0, 0, -0.6 * k)
    BAN_ROLL.rotation_euler = (k * 12.0, 0, 0)


def mini_scan(name):
    """Small silver 'scan file' of the cartoon sedan (same body + cabin, scan material), 1/7 scale."""
    g = empty(name)
    b = CAR_BODY
    box(name + "_b", (b["x1"] - b["x0"], 2 * b["y"], b["z1"] - b["z0"]), (0, 0, (b["z0"] + b["z1"]) / 2), mat("scan", hl=True), g,
        bevel=0.07, ol=0.02)
    hull(name + "_c", cabin_pts(), mat("scan", hl=True), g, bevel=0.05, ol=0.02)
    for x in (-1.25, 1.25):
        for s in (-1, 1):
            cyl(f"{name}_w{x}{s}", 0.33, 0.24, (x, s * 0.78, 0.33), mat("#9ea39e"), g, axis="Y", ol=0.02)
    g.scale = (1 / 7,) * 3
    return g


def lip_part(name):
    """Front lip / splitter for the cartoon sedan (front face at x = 2.0): a sage wedge under the bumper."""
    g = empty(name)
    hull(name + "_m", [(0, -0.84, 0.0), (0, 0.84, 0.0), (0.3, -0.76, -0.03), (0.3, 0.76, -0.03),
                       (0, -0.84, 0.1), (0, 0.84, 0.1), (0.18, -0.8, 0.07), (0.18, 0.8, 0.07)], mat("sage", hl=True), g,
         bevel=0.01, ol=0.02)
    return g


LIP_HOME = Vector((1.96, 0, 0.27))


def build_printer():
    g = empty("PRINTER")
    m = mat("#3a3d3a")
    for x in (-0.28, 0.28):
        for y in (-0.22, 0.22):
            box(f"pr_post{x}{y}", (0.04, 0.04, 0.62), (x, y, 0.31), m, g, ol=0.01)
    box("pr_top", (0.6, 0.48, 0.05), (0, 0, 0.62), m, g, bevel=0.01, ol=0.012)
    box("pr_base", (0.62, 0.5, 0.06), (0, 0, 0.03), m, g, bevel=0.01, ol=0.012)
    box("pr_bed", (0.46, 0.36, 0.02), (0, 0, 0.1), mat("#c8cac7"), g, ol=0.008)
    gantry = empty("pr_gantry", g, (0, 0, 0.32))
    box("pr_rail", (0.56, 0.03, 0.03), (0, 0.02, 0), mat("metal"), gantry, ol=0.008)
    head = empty("pr_head", gantry, (0, 0, 0))
    box("pr_hbody", (0.08, 0.07, 0.09), (0, -0.02, 0), mat("sage"), head, bevel=0.01, ol=0.01)
    cyl("pr_nozzle", 0.012, 0.04, (0, -0.02, -0.065), mat("#c9a14a"), head, r2=0.003)
    cyl("pr_spool", 0.11, 0.06, (0.36, 0.0, 0.5), mat("sage_l"), g, axis="X", bevel=0.01, ol=0.012)
    return g, gantry, head


PRINTER, PR_GANTRY, PR_HEAD = build_printer()


def build_spool(name, key):
    g = empty(name)
    cyl(name + "_r", 0.13, 0.11, (0, 0, 0), mat(key, hl=True), g, axis="X", bevel=0.015, ol=0.014)
    cyl(name + "_f0", 0.15, 0.015, (-0.06, 0, 0), mat("#3a3d3a"), g, axis="X", ol=0.01)
    cyl(name + "_f1", 0.15, 0.015, (0.06, 0, 0), mat("#3a3d3a"), g, axis="X", ol=0.01)
    cyl(name + "_h", 0.035, 0.14, (0, 0, 0), mat("dark"), g, axis="X")
    return g


SPOOLS = [build_spool("SPOOL0", "sage"), build_spool("SPOOL1", "white"), build_spool("SPOOL2", "#555855")]


def build_glue():
    g = empty("GLUE")
    cyl("gl_body", 0.05, 0.16, (0, 0, 0.08), mat("white", hl=True), g, bevel=0.01, ol=0.012)
    cyl("gl_cap", 0.03, 0.06, (0, 0, 0.19), mat("sage"), g, r2=0.006, ol=0.01)
    box("gl_label", (0.07, 0.006, 0.06), (0, -0.05, 0.08), mat("sage_l"), g)
    return g


GLUE = build_glue()


def build_puff():
    g = empty("PUFF")
    blob("pf_pad", (0.17, 0.17, 0.07), (0, 0, 0), mat("#f6f0ee", hl=True), g, ol=0.015)
    torus("pf_ring", 0.07, 0.018, (0, 0, 0.07), mat("sage"), g, ol=0.01)
    return g


PUFF = build_puff()
EXTRA = [BANNER, PRINTER, GLUE, PUFF] + SPOOLS

# Pip "dusted white" after the puff: per-object material swap (slot 0), eyes/tag faces untouched
_PIP_ORIG = {}


def _walk(ob):
    yield ob
    for c in ob.children:
        yield from _walk(c)


for _o in _walk(PIP.root):
    if _o.type == "MESH" and _o.data.materials and not any(k in _o.name for k in ("_eye", "_tagface")):
        _PIP_ORIG[_o.name] = _o.data.materials[0]


def _dusted(m):
    mt = _re.match(r"t_(.+)_(\d\.\d\d)_(\d)$", m.name)
    if not mt:
        return m
    base = PAL.get(mt.group(1), mt.group(1))
    return toon(_hexmul(base, 1.0, 0.72), float(mt.group(2)), bool(int(mt.group(3))))


_PIP_DUST = {n: _dusted(m) for n, m in _PIP_ORIG.items()}


def pip_dust(on):
    for n, m in (_PIP_DUST if on else _PIP_ORIG).items():
        bpy.data.objects[n].data.materials[0] = m


def reset_anim():
    reset()
    for ob in EXTRA:
        set_vis(ob, False)
    set_vis(LAPTOP, True)
    set_vis(UI, True)
    set_vis(PIPSCAN, True)
    pip_scanner("pouch")
    pip_dust(CUR_T >= PUFF_T + 0.5)
    banner_unroll(1.0)
    PRINTER.parent = None


# ----------------------------------------------------------------------------------------------------------------- shots
def gus_talk_pose(t, loc, rz, look_=(0, 0), hips=(0, 0, 0), head=(0, 0, 0), armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12, elbowR=-12):
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    pose(GUS, loc=loc, rz=rz, hips=hips, head=(head[0] + 6 * acc, head[1], head[2]), armL=armL, armR=armR, elbowL=elbowL,
         elbowR=elbowR, mouth=0.9 * m, lid=lid, look=look_)


def pip_talk_pose(t, loc, rz, look_=(0, 0), hips=(0, 0, 0), head=(0, 0, 0), armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12, elbowR=-12,
                  hop=0.0):
    m, lid = talk("PIP", t)
    acc = accent("PIP", t)
    loc = (loc[0], loc[1], loc[2] + hop)
    pose(PIP, loc=loc, rz=rz, hips=hips, head=(head[0] + 6 * acc, head[1], head[2]), armL=armL, armR=armR, elbowL=elbowL,
         elbowR=elbowR, mouth=m, lid=lid, look=look_)


def anim_A(fr):
    """'Hi, I'm Gus.' / 'And I'm Pip!' - Gus steps in and waves; Pip pops up beside him."""
    t = fr / FPS
    k_in = eback((t - 0.0) / 0.55)
    wave = math.sin((t - W(1, 0)) * 11) if LN[1]["t0"] - 0.1 < t < LN[1]["t1"] + 0.3 else 0.0
    wv = win(t, LN[1]["t0"] - 0.1, LN[1]["t1"] + 0.2, 0.15, 0.3)
    gus_talk_pose(t, (lerp(-1.4, -0.45, k_in), -2.0, 0), lerp(20, 8, k_in), look_=(0.1, 0.1),
                  armL=(lerp(4, -158, wv), -16 * wave * wv, 6), elbowL=lerp(-12, -6, wv))
    # Pip pops up from below frame on his line: a hop with overshoot
    tp = W(2, 0) - 0.25
    pk = eback((t - tp) / 0.35, 2.0)
    hop = 0.12 * max(0.0, math.sin(math.pi * cl((t - tp - 0.3) / 0.45)))
    ar = win(t, W(2, 0), LN[2]["t1"] + 0.2, 0.1, 0.3)
    pip_talk_pose(t, (0.55, -2.25, lerp(-1.3, 0, pk)), -14, look_=(-0.2, 0.3), hop=hop,
                  armL=(lerp(4, -155, ar), 0, 10), armR=(lerp(4, -155, ar), 0, -10), elbowL=-8, elbowR=-8)
    look(cam, (0.05, -5.1, 1.12), (0.05, -2.0, 0.92), 34)


def anim_B(fr):
    """'We are the Illumaesthetic mascots!' - banner unrolls over the car on 'Illumaesthetic', push in on the nametags."""
    t, u = fr / FPS, prog(fr, "B")
    set_vis(BANNER, True)
    banner_unroll(eback((t - W(3, 3)) / 0.5, 1.2))
    pr = win(t, W(3, 3), LN[3]["t1"] + 0.5, 0.15, 0.3)
    pip_talk_pose(t, (0.55, -2.25, 0), -10, look_=(-0.1, 0.4), hips=(-4 * pr, 0, 0),
                  armL=(lerp(4, -155, pr), 0, 8), armR=(-20, 0, -10), elbowL=-8)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=(-0.45, -2.0, 0), rz=8 - 10 * ease(u), head=(-6, 0, -12 * ease(u)), armL=(4, 0, 6), armR=(-20, 0, -12),
         elbowR=-70, lid=glid, look=(0.5, 0.2))
    cam_push((0.05, -5.6, 1.4), (0.05, -2.0, 1.55), 30, 0.22 * ease(u))


VOX = []
_rv = random.Random(3)
for _i in range(46):
    VOX.append(dict(p=Vector((_rv.uniform(-1.8, 1.8), _rv.uniform(-2.8, -0.8), _rv.uniform(0.2, 2.3))), s=_rv.uniform(0.04, 0.09),
                    d=_rv.uniform(0.0, 0.45), key=("sage_l", "sage", "white")[_i % 3]))


def anim_C(fr):
    """'Here in the digital world to explain to you the tips and tricks...' - sage voxels pop in on 'digital world';
    on 'tips and tricks' Pip lifts his scanner and Gus points at it."""
    t, u = fr / FPS, prog(fr, "C")
    tv = W(4, 3)
    for i, v in enumerate(VOX):
        a = (t - tv - v["d"]) / 0.25
        life = eback(a, 2.0) * (1 - ease((t - tv - v["d"] - 1.1) / 0.35))
        if life > 0.02:
            s = v["s"] * life
            ob = box(f"vox{i}", (s, s, s), v["p"] + Vector((0, 0, 0.25 * cl(a / 6))), emit(v["key"], 1.0), None, ol=0.0)
            ob.rotation_euler = (0.3 * i, 0.7 * i + t, 0.2 * i)
            temp(ob)
    tt = W(4, 10)
    k = win(t, tt - 0.1, LN[4]["t1"], 0.25, 0.3)
    pip_scanner("hand" if k > 0.3 else "pouch")
    pip_talk_pose(t, (0.6, -2.25, 0), -18, look_=(lerp(-0.6, 0.3, k), lerp(0.7, 0.3, k)),
                  armR=(lerp(4, -95, k), 0, lerp(-6, -20, k)), elbowR=lerp(-12, -40, k))
    gus_talk_pose(t, (-0.4, -2.0, 0), lerp(4, 22, k), look_=(lerp(0.0, 0.6, k), lerp(0.1, -0.3, k)),
                  armR=(lerp(-20, -80, k), 0, lerp(-10, -35, k)), elbowR=lerp(-50, -10, k), armL=(-15, 0, 10), elbowL=-60)
    cam_push((0.6, -4.6, 1.35), (0.0, -2.0, 1.12), 32, 0.12 * ease(u))


def anim_D(fr):
    """'...we've learned along the way... from doing this for so long.' - a slow move across the tool wall down to the two
    of them at the workbench; Gus proud on 'so long', Pip looking up at him."""
    t, u = fr / FPS, prog(fr, "D")
    k = ease(u * 1.25)
    gus_talk_pose(t, (2.75, 2.15, 0), 12, look_=(0.15, 0.2), armL=(-35, 0, 12), elbowL=-80, armR=(4, 0, -8))
    pip_talk_pose(t, (3.6, 2.05, 0), 32, look_=(-0.8, 0.8), head=(-14, 0, 6))
    tgt = (lerpv((3.35, 3.5, 2.15), (3.15, 2.1, 1.05), k))
    look(cam, (lerp(3.9, 3.25, k), lerp(0.3, -0.75, k), lerp(1.9, 1.35, k)), tgt, lerp(40, 30, k))


PHONE_SEG = SF["E"]


def anim_E(fr):
    """'Illumaesthetic scans whole cars in 3D...' - Pip shows the phone (real Lola / C5 / MR2 1:1 cuts composited later)."""
    t, u = fr / FPS, prog(fr, "E")
    set_vis(PIPSCAN, False)
    c, n, uu, r = phone_pose_s11()
    m, lid = talk("PIP", t)
    acc = accent("PIP", t)
    PIP.neck.rotation_euler = [math.radians(a) for a in (-12 + 6 * acc, 0, -16 + 3 * math.sin(t * 4))]
    talk_squash(PIP, m)
    apply_expr(PIP, max(lid, blink("PIP", t)), (0.6, 0.6))
    PIP.eyes_g.location = (0.6 * PIP.S["eye_look"], 0, PIP.head_c + 0.6 * PIP.S["eye_look"])
    f = -Vector((n.x, n.y, 0)).normalized()
    pose(GUS, loc=(0, 0, 0), rz=math.degrees(math.atan2(f.x, -f.y)) + 25, hips=(6, 0, 0), head=(14, 0, 0), look=(0, -0.6))
    place_head_xy(GUS, c + n * 0.75 + r * 0.62)
    d = lerp(1.55, 1.3, ease(u))
    look(cam, c + n * d - r * 0.2 - uu * 0.06, c - r * 0.2 - uu * 0.06, 38, up=uu)


def anim_F(fr):
    """'...sells the scans, designs the parts, prints them... and everything in between.' - a silver mini scan pops over
    Gus's mitten; a sage lip outline appears at the car's nose; it prints (fills from one side); it snaps on."""
    t, u = fr / FPS, prog(fr, "F")
    t_sell, t_des, t_pr, t_ev = W(6, 0), W(6, 3), W(6, 6), W(6, 8)
    hold = win(t, t_sell - 0.1, t_ev + 0.2, 0.2, 0.3)
    gus_talk_pose(t, (1.5, -1.65, 0), 28, look_=(lerp(0.0, 0.5, hold), 0.3), armL=(lerp(4, -85, hold), 0, 12),
                  elbowL=lerp(-12, -25, hold), armR=(-25, 0, -14), elbowR=-55)
    pip_talk_pose(t, (3.2, 1.05, 0), 112, look_=(-0.7, 0.2))
    bpy.context.view_layer.update()
    # mini scan over the right mitten
    ks = eback((t - t_sell) / 0.3, 2.0) * (1 - ease((t - t_ev - 0.3) / 0.3))
    if ks > 0.02:
        ms = temp(mini_scan("MS"))
        hp = GUS.hands["L"].matrix_world.translation
        ms.location = hp + Vector((0, 0, 0.12))
        ms.scale = (ks / 7,) * 3
        ms.rotation_euler = (0, 0, t * 1.6)
    # the lip: outline (designs) -> printing fill (prints) -> snap on (everything in between)
    if t >= t_des - 0.05:
        kd = eback((t - t_des) / 0.25)
        kp = ease((t - t_pr) / max(0.3, t_ev - t_pr))
        ksn = eback((t - t_ev - 0.1) / 0.45, 1.8)
        off = Vector((0.75, 0, 0.3)) * (1 - ksn)
        ghost = temp(lip_part("LIPG"))
        for o in ghost.children:
            o.data.materials[0] = emit("sage_l", 1.2, 0.35)
            if len(o.data.materials) > 1:
                o.data.materials[1] = emit("sage_l", 1.0, 0.0)
        ghost.location = LIP_HOME + off
        ghost.scale = (1, kd, 1)
        set_vis(ghost, ksn < 0.98)
        if kp > 0.01:
            solid = temp(lip_part("LIPS"))
            solid.location = LIP_HOME + off + Vector((0, -0.82 * (1 - kp), 0))
            solid.scale = (1, max(0.01, kp), 1)
    look(cam, (3.55, -3.9, 0.95), (1.85, -0.75, 0.9), 28)


QM = [dict(x=-0.95, y=-2.6, z0=3.0, d=0.0, s=2.0, key="sage"), dict(x=1.15, y=-2.5, z0=3.0, d=0.12, s=1.8, key="white"),
      dict(x=0.05, y=-1.5, z0=3.2, d=0.24, s=2.4, key="sage_l"), dict(x=0.75, y=-3.2, z0=3.0, d=0.36, s=1.4, key="sage"),
      dict(x=-0.5, y=-3.35, z0=3.0, d=0.5, s=1.3, key="white")]


def anim_G(fr):
    """'And we'll answer all the questions you keep asking us!' - cartoon question marks drop in and bounce."""
    t, u = fr / FPS, prog(fr, "G")
    tq = W(7, 5) - 0.3
    for i, q in enumerate(QM):
        a = cl((t - tq - q["d"]) / 0.55)
        if a <= 0:
            continue
        z = lerp(q["z0"], 0.25 * q["s"], a * a) if a < 1 else 0.25 * q["s"] + 0.08 * abs(math.sin((t - tq - q["d"] - 0.55) * 7)) * math.exp(-(t - tq - q["d"] - 0.55) * 3)
        g = temp(qmark(f"QM{i}", q["s"], q["key"]))
        g.location = (q["x"], q["y"], z + 0.15 * q["s"])
        g.rotation_euler = (0, math.radians(8 * math.sin(t * 3 + i)), math.radians(-10 + 20 * (i % 2)))
    ex = win(t, W(7, 0), LN[7]["t1"], 0.12, 0.3)
    hop = 0.07 * abs(math.sin(math.pi * (t - W(7, 0)) * 2.2)) * ex
    pip_talk_pose(t, (0.45, -2.3, 0), -8, look_=(-0.2, 0.5), hop=hop, armL=(lerp(4, -155, ex), 0, 10),
                  armR=(lerp(4, -155, ex), 0, -10), elbowL=-8, elbowR=-8)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=(-0.5, -1.95, 0), rz=14, head=(-8, 0, -14), lid=glid, look=(0.6, 0.6), armL=(4, 0, 6), armR=(4, 0, -6))
    cam_push((0.0, -5.6, 1.15), (0.0, -2.0, 1.05), 30, 0.1 * ease(u))


def anim_H1(fr):
    """'Scanning.' - Pip sweeps his scanner along the car's side; a sage light cone hits the door."""
    t, u = fr / FPS, prog(fr, "H1")
    pip_scanner("hand")
    pose(PIP, loc=(0.2 + 0.5 * ease(u), -1.75, 0), rz=-178, armR=(-95, 0, 0), elbowR=-10, look=(0, 0.2))
    bpy.context.view_layer.update()
    ap = PIPSCAN.matrix_world @ Vector((0, -0.045, 0.07))
    cone = temp(light_cone("cone", ap, Vector((ap.x + 0.05, -0.86, ap.z + 0.05)), 0.33))
    cone.data.materials[0] = emit("sage_l", 1.3, 0.38)
    for ch_ in cone.children:
        ch_.data.materials[0] = emit("sage_l", 1.6, 0.6)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=(-1.6, -2.2, 0), rz=-30, mouth=0.9 * gm, lid=glid, look=(0.5, 0.3))
    look(cam, (2.5, -2.9, 1.05), (0.35, -1.35, 0.85), 28)


def anim_H2(fr):
    """'Printing.' - a printer on the workbench: the head shuttles, the part grows layer by layer."""
    t, u = fr / FPS, prog(fr, "H2")
    set_vis(LAPTOP, False); set_vis(UI, False)
    set_vis(PRINTER, True)
    PRINTER.location = (3.35, 3.1, 0.955)
    hgt = 0.02 + 0.16 * ease(u * 1.1)
    PR_GANTRY.location = (0, 0, 0.11 + hgt + 0.07)
    PR_HEAD.location = (0.14 * math.sin(t * 22), 0, 0)
    part = temp(box("prpart", (0.22, 0.12, hgt), (0, 0, 0.11 + hgt / 2), mat("sage", hl=True), PRINTER, ol=0.012))
    for i in range(int(hgt / 0.025)):
        temp(box(f"prl{i}", (0.222, 0.122, 0.004), (0, 0, 0.11 + 0.025 * (i + 1)), mat("#4f8a60"), PRINTER))
    look(cam, (3.35, 1.85, 1.55), (3.35, 3.1, 1.2), 34)


def anim_H3(fr):
    """'Materials.' - three filament spools drop onto the bench one by one."""
    t, u = fr / FPS, prog(fr, "H3")
    t0 = SF["H3"][0] / FPS
    for i, sp in enumerate(SPOOLS):
        a = cl((t - t0 - 0.12 * i) / 0.32)
        if a <= 0:
            continue
        set_vis(sp, True)
        z = lerp(1.9, 1.105, a * a) + (0.04 * abs(math.sin((t - t0 - 0.12 * i - 0.32) * 12)) * math.exp(-(t - t0) * 4) if a >= 1 else 0)
        sp.location = (2.75 + 0.42 * i, 2.95, z)
        sp.rotation_euler = (0, 0, math.radians(-8 + 8 * i))
    set_vis(LAPTOP, False); set_vis(UI, False)
    look(cam, (3.15, 1.25, 1.55), (3.17, 2.95, 1.1), 32)


def anim_H4(fr):
    """'Glue.' - the glue bottle tips and runs a bead along the seam of two printed pieces, which slide together."""
    t, u = fr / FPS, prog(fr, "H4")
    set_vis(LAPTOP, False); set_vis(UI, False)
    set_vis(GLUE, True)
    gap = 0.06 * (1 - ease((u - 0.55) / 0.4))
    temp(box("gp0", (0.3, 0.16, 0.08), (3.2 - gap, 3.0, 0.995), mat("sage", hl=True), None, bevel=0.01, ol=0.012))
    temp(box("gp1", (0.3, 0.16, 0.08), (3.5 + gap, 3.0, 0.995), mat("sage", hl=True), None, bevel=0.01, ol=0.012))
    k = ease(u / 0.6)
    GLUE.location = (3.35 + 0.05, 3.0 - 0.08 + 0.16 * k, 1.13)
    GLUE.rotation_euler = (math.radians(150), 0, 0)
    if k > 0.02:
        temp(box("bead", (0.03, 0.16 * k, 0.02), (3.35, 2.92 + 0.08 * k, 1.04), mat("white", hl=True), None, bevel=0.008))
    look(cam, (3.35, 2.15, 1.45), (3.35, 3.0, 1.02), 40)


CLOUD = []
_rc = random.Random(9)
for _i in range(28):
    CLOUD.append(dict(o=Vector((_rc.uniform(-0.35, 0.35), _rc.uniform(-0.3, 0.2), _rc.uniform(0.3, 1.25))), r=_rc.uniform(0.12, 0.26),
                      d=_rc.uniform(0, 0.12)))


def anim_I(fr):
    """'And why we spray everything white!' - Pip giggles; Gus bops him with a giant powder puff: white cloud; Pip comes
    out dusted white and blinks."""
    t, u = fr / FPS, prog(fr, "I")
    pip_loc = Vector((0.5, -2.2, 0))
    g = ease((t - (LN[9]["t0"] - 0.2)) / 0.5)
    wind = ease((t - (PUFF_T - 0.45)) / 0.35)
    bop = eout((t - (PUFF_T - 0.1)) / 0.1) * (1 - ease((t - PUFF_T - 0.15) / 0.35))
    set_vis(PUFF, True)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=(-0.4, -2.0, 0), rz=lerp(10, 40, g), hips=(8 * bop, 0, 0), head=(-6, 0, -10), lid=glid, look=(0.7, 0.4),
         armR=(lerp(4, -60, g) - 90 * wind + 70 * bop, 0, -20), elbowR=-20, armL=(4, 0, 6))
    bpy.context.view_layer.update()
    PUFF.parent = None
    PUFF.matrix_world = Matrix.Translation(GUS.hands["R"].matrix_world.translation + Vector((0.05, -0.05, 0.08)))
    PUFF.rotation_euler = (math.radians(70), 0, math.radians(-30))
    giggle = 0.02 * abs(math.sin(t * 18)) * win(t, LN[9]["t0"], PUFF_T - 0.1, 0.05, 0.05)
    squish = 1 - 0.12 * eback((t - PUFF_T) / 0.12) * (1 - ease((t - PUFF_T - 0.2) / 0.5))
    pip_talk_pose(t, (pip_loc.x, pip_loc.y, giggle), -20, look_=(-0.5, 0.4), hips=(-3, 0, 0))
    PIP.root.scale = (1 / max(0.6, squish) ** 0.3, 1, squish)
    # the cloud
    for i, c in enumerate(CLOUD):
        a = (t - PUFF_T - c["d"]) / 0.25
        if a <= 0:
            continue
        life = eout(a) * (1 - ease((t - PUFF_T - 0.85 - c["d"]) / 0.5))
        if life < 0.02:
            continue
        rr = c["r"] * (0.4 + 0.8 * eout(a))
        drift = Vector((0, 0, 0.25 * cl(a / 6)))
        temp(blob(f"cl{i}", (rr, rr, rr * 0.9), pip_loc + c["o"] + drift, mat("#f7f8f7", alpha=life, hl=True), None, seg=16, rings=10))
    cam_push((0.1, -5.0, 1.15), (0.05, -2.05, 0.95), 32, 0.08 * ease(u))


def anim_J(fr):
    """'...There's a lot to cover.' - Gus looks over at the dusted-white Pip, amused; a little powder still drifting."""
    t, u = fr / FPS, prog(fr, "J")
    gus_talk_pose(t, (-0.4, -2.0, 0), 34, look_=(0.8, -0.2), head=(6, 0, -14), armL=(-25, 0, 14), elbowL=-60)
    pip_talk_pose(t, (0.45, -2.2, 0), -24, look_=(-0.6, 0.6))
    for i in range(8):
        a = (t * 0.35 + i / 8) % 1.0
        temp(blob(f"dust{i}", (0.02, 0.02, 0.02), (0.45 + 0.25 * math.sin(i * 2.1), -2.3, 0.6 + 0.7 * a), mat("#f7f8f7", alpha=1 - a, hl=True),
                  None, seg=8, rings=6))
    cam_push((-0.1, -4.4, 1.3), (0.0, -2.05, 1.0), 34, 0.1 * ease(u))


def anim_K(fr):
    """'What questions do you have?' - Pip leans into the lens; Gus behind him, smiling."""
    t, u = fr / FPS, prog(fr, "K")
    lean = eback((t - (LN[11]["t0"] - 0.3)) / 0.5)
    pip_talk_pose(t, (0.2, lerp(-2.3, -2.55, lean), 0), -4, look_=(0, -0.1), hips=(14 * lean, 0, 0), head=(-12 * lean, 0, 6),
                  armL=(-40, 0, 10), armR=(-40, 0, -10))
    gm, glid = talk("GUS", t)
    pose(GUS, loc=(-0.6, -1.7, 0), rz=10, head=(-4, 0, -6), lid=glid, look=(0.3, 0.0), armL=(4, 0, 6), armR=(4, 0, -6))
    look(cam, (0.15, -4.05, 0.98), (0.05, -2.2, 0.92), 30)


ANIM = {s: globals()[f"anim_{s}"] for s in SF}

# ----------------------------------------------------------------------------------------------------------------- run
CORN = os.path.join(OUT, "screen_corners.json")
corners = json.load(open(CORN)) if os.path.exists(CORN) else dict(
    doc="Ep 0 phone screen corners (shot E) for compositing the real footage: pixels in 1080x1920, tl,tr,br,bl. Key #ff00ff.",
    width=1080, height=1920, fps=FPS, key_colour=KEY, shots={})
for sh in EP_SHOTS:
    f0, f1 = SF[sh]
    d = os.path.join(OUT, sh)
    os.makedirs(d, exist_ok=True)
    per, tsum, nr = {}, 0.0, 0
    for fr in range(f0, f1):
        final = os.path.join(d, f"{fr:04d}.png")
        need_c = sh == "E"
        todo = (fr - f0) % EVERY == 0 and not os.path.exists(final) and (not ONLY or fr in ONLY)
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
        print(f"[ep0] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if per:
        corners["shots"][sh] = dict(frames=[f0, f1], per_frame=per)
        json.dump(corners, open(CORN, "w"), indent=1)
    if nr:
        print(f"[ep0] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
