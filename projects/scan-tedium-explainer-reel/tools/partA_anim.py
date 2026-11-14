"""Part A animation (stage 3). Executed inside partA_scene.py's globals when it runs with --animate:

  blender -b --factory-startup -P partA_scene.py -- --animate --out FRAMES_DIR --shots S1,S2 [--scale 1] [--spp 8]
          [--timeline partA_timeline.json] [--every N] [--range a:b]

Every frame is posed procedurally from the timeline (no keyframes): reset(), then anim_<shot>(frame), then a still render.
That makes the render resumable frame by frame: FRAMES_DIR/<shot>/<frame>.png is skipped when it exists (written via a
_tmp file and renamed, so a killed render never leaves a half-written frame). Persistent data stays off (lessons).

Talk: mouths are driven by the measured word times in partA_timeline.json (syllables spread over each word, opening fast and
closing slower, leading the sound by one frame); the stressed word of each line gets a small head accent; listeners blink
every 2-3.6 s and look at the speaker. No text anywhere in 3D.
"""
import re as _re

_tl_path = arg("--timeline", os.path.join(os.path.dirname(OUT.rstrip("/")), "partA_timeline.json"))
if not os.path.exists(_tl_path):
    _tl_path = "/home/user/Illumaesthetic-Video-Editor/projects/scan-tedium-explainer-reel/partA_timeline.json"
TL = json.load(open(_tl_path))
FPS = TL["fps"]
SF = {s["id"]: (s["f0"], s["f1"]) for s in TL["shots"]}
LN = {L["n"]: L for L in TL["lines"]}
EVERY = int(arg("--every", "1"))
RANGE = arg("--range", "")
ONLY = {int(x) for x in arg("--frames", "").split(",") if x}   # explicit frame list (lookdev stills)


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
    t += 1.0 / FPS   # mouth shapes lead the sound by a frame
    m = 0.0
    for s0, d, a in SYL[spk]:
        u = (t - s0) / d
        if 0 <= u < 1:
            m = max(m, a * (u / 0.3 if u < 0.3 else 1 - 0.8 * (u - 0.3) / 0.7))
    return m


def accent(spk, t):
    return max([math.exp(-((t - ta - 0.04) / 0.12) ** 2) for ta in STRESS[spk]] + [0.0])


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
    """Face and talk without touching hips/hands (S11/S12: the phone hand must not move): body squash from the talk
    energy, dot-eye blink/squint, eye look."""
    S = ch.S
    talk_squash(ch, mouth)
    f = max(S.get("base_lid", 0.0), lid)
    for e in ch.eyes:
        e.scale = (1, 1, max(0.08, 1 - 0.92 * f))
    ch.eyes_g.location = (look[0] * S["eye_look"], 0, ch.head_c + look[1] * S["eye_look"])


def talk(spk, t, base_lid=0.0):
    """talk energy (drives the body squash and hand lift - no mouths) and lid (blink, plus a squint on the stressed word)."""
    return mouth_at(spk, t), max(base_lid, blink(spk, t), 0.5 * accent(spk, t))


def words_of(n):
    return LN[n]["words"]


def syl_onsets(n):
    out = []
    for w in words_of(n):
        g = syllables(w["w"])
        d = max(0.05, w["t1"] - w["t0"]) / len(g)
        out += [w["t0"] + k * d for k in range(len(g))]
    return out


# ----------------------------------------------------------------------------------------------------------------- shots
def prog(fr, sh):
    f0, f1 = SF[sh]
    return (fr - f0) / max(1, f1 - 1 - f0)


def cam_push(loc, target, lens, k, up=(0, 0, 1)):
    loc, target = Vector(loc), Vector(target)
    look(cam, target + (loc - target) * (1 - k), target, lens, up=up)


def anim_S1(fr):
    t, u = fr / FPS, prog(fr, "S1")
    L = LN[1]
    pip_scanner("hand")   # "how do you scan a whole car?" - gesturing about scanning
    temp(make_dots("dots", []))
    m, lid = talk("PIP", t)
    sp = L["t0"] - 0.05 <= t <= L["t1"] + 0.1
    hop = 0.06 * abs(math.sin(math.pi * (t - L["t0"]) * 2.4)) if sp else 0.0
    wave = math.sin(t * 9.0) * (1 if sp else 0.3)
    acc = accent("PIP", t)
    pose(PIP, loc=(0.85, -2.35, hop), rz=-40, hips=(-6, 0, 0), head=(-20 + 6 * acc, 0, 4 * math.sin(t * 5)),
         armL=(-135 + 18 * wave, 48, 0), armR=(-30 - 15 * wave, 0, -22), elbowL=-25, elbowR=-50,   # wave out to the side: never over the mouth
         legL=(-15 - 25 * (hop / 0.06), 0, 0), legR=(20 * (hop / 0.06), 0, 0), mouth=m, lid=lid, look=(-0.5, 0.9),
         brow=(0.035, -12))
    turn = ease((t - L["t0"] - 0.6) / 1.1)          # GUS's head turns slowly to PIP (he is slow)
    gm, glid = talk("GUS", t, 0.45)
    pose(GUS, loc=(-0.45, -1.95, 0), rz=30, head=(6 * turn, 0, -22 * turn), armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12,
         elbowR=-12, mouth=gm, lid=glid, look=lerpv((0, -0.3), (0.8, -0.4), turn), brow=(0.0, 0))
    cam_push((2.0, -5.5, 1.15), (0.05, -1.4, 0.98), 26, 0.05 * ease(u))


def anim_S2(fr):
    t, u = fr / FPS, prog(fr, "S2")
    L = LN[2]
    t0 = SF["S2"][0] / FPS
    lift = eback((t - t0) / 0.4)
    m, lid = talk("GUS", t, 0.45)
    acc = accent("GUS", t)
    pose(GUS, loc=(0.2, -1.7, 0), rz=10, hips=(-3, 0, 0), head=(lerp(0, -14, lift) + 7 * acc, 0, 10), armL=(lerp(-30, -165, lift), 0, 4),
         armR=(-25, 0, -14), elbowL=lerp(-40, -6, lift), elbowR=-60, mouth=m, lid=lid, look=(0.3, lerp(0, 0.9, lift)), brow=(0.02, 0))
    attach(ROLL, GUS.hands["L"], (0, -0.02, -0.16), (0, 0, 8))
    bpy.context.view_layer.update()
    # the strip unrolls from "Dots." to the end of the line
    wd = [w for w in L["words"] if w["w"].lower().startswith("dots")]
    g = ease((t - wd[0]["t0"]) / max(0.3, L["t1"] - wd[0]["t0"] - 0.05)) if wd else u
    rp = ROLL.matrix_world.translation
    pts = [rp + Vector((0.0, -0.09, -0.02))]
    for i in range(1, 14):
        k = i / 13
        pts.append(rp + Vector((0.03 * math.sin(k * 5), -0.09 - 0.12 * k - 0.05 * math.sin(k * 3.1), -(rp.z - 0.012) * k ** 1.05)))
    last = pts[-1]
    for i in range(1, 9):
        pts.append(Vector((last.x + 0.02 * i, last.y - 0.09 * i, 0.012 + 0.04 * max(0, (i - 6)) ** 1.5)))
    if g > 0.02:
        lens_ = [0.0]
        for a, b in zip(pts, pts[1:]):
            lens_.append(lens_[-1] + (b - a).length)
        want = g * lens_[-1]
        cut = [pts[0]]
        for i in range(1, len(pts)):
            if lens_[i] <= want:
                cut.append(pts[i])
            else:
                f = (want - lens_[i - 1]) / (lens_[i] - lens_[i - 1])
                cut.append(pts[i - 1].lerp(pts[i], f))
                break
        # the hanging end swings a little while it falls
        sw = 0.04 * math.sin(t * 11) * (1 - g)
        cut = [p + Vector((sw * (j / len(cut)), 0, 0)) for j, p in enumerate(cut)]
        if len(cut) >= 2:
            s_, d_ = strip_path("strip", cut, 0.1)
            temp(s_); temp(d_)
    pm, plid = talk("PIP", t)
    pose(PIP, loc=(0.95, -2.45, 0), rz=-30, head=(-26 + 10 * g, 0, 0), mouth=pm, lid=plid, look=(-0.7, lerp(1, -0.2, g)),
         brow=(0.03, -14), armL=(-20, 0, 10), armR=(-20, 0, -10))
    look(cam, (0.95, -5.0, 1.55), (0.3, -1.7, 1.55), 34)


S3_STATE = {}


def anim_S3(fr):
    t = fr / FPS
    near = dots_where(lambda d: d["region"] == "side_n" and -0.5 < d["p"].x < 1.15)
    base = [d for d in near if d["order"] < 0.35]
    T = syl_onsets(3)
    rest = sorted([d for d in near if d["order"] >= 0.35 and 0.02 < d["p"].x < 0.5 and 0.5 < d["p"].z < 0.9],   # in frame
                  key=lambda d: d["order"])
    # spread the slaps across the door (never two neighbours in a row)
    new = []
    for d in rest:
        if all((d["p"] - e["p"]).length > 0.16 for e in new[-2:]):
            new.append(d)
        if len(new) == len(T):
            break
    T = T[:len(new)]
    print(f"[anim] S3 {len(new)} slaps", flush=True) if fr == SF["S3"][0] else None
    shown = list(base)
    k = -1
    for i, (ti, d) in enumerate(zip(T, new)):
        dt = t - ti
        if dt >= -0.02:
            s = 1.25 * cl(dt / 0.067, 0.25) if dt < 0.067 else (1.25 - 0.25 * (dt - 0.067) / 0.066 if dt < 0.133 else 1.0)
            shown.append(dict(d, s=s))
            k = i
    temp(make_dots("dots", shown))
    tgt = [Vector((d["p"].x + 0.12, -0.92, d["p"].z + 0.06)) for d in new]
    if k < 0:
        h = tgt[0] + Vector((0.5, -0.1, 0.12)) * (1 - ease((t - (T[0] - 0.3)) / 0.3))
    elif k < len(T) - 1:
        p = (t - T[k]) / (T[k + 1] - T[k])
        h = tgt[k].lerp(tgt[k + 1], ease((p - 0.2) / 0.6))
        lift = math.sin(math.pi * cl((p - 0.12) / 0.78))
        h = h + Vector((0, -0.09 * lift, 0.06 * lift))
    else:
        p = (t - T[k]) / 0.4
        h = tgt[k] + Vector((0.35, -0.12, 0.08)) * ease(p)
    set_vis(GUS.root, False)
    # GUS's floating mitten (no arm) pressing each dot on
    hr = GUS_SPEC["hand"]
    temp(blob("s3_mitt", (hr[0] * 1.05, hr[1] * 0.8, hr[2] * 1.05), (h.x - 0.02, h.y + 0.01, h.z - 0.06), mat("vinyl", hl=True), None,
              ol=GUS_SPEC["ol"] * 0.8))
    temp(blob("s3_thumb", (hr[0] * 0.42, hr[0] * 0.42, hr[0] * 0.5), (h.x - 0.09, h.y - 0.01, h.z - 0.02), mat("vinyl", hl=True), None,
              ol=GUS_SPEC["ol"] * 0.6))
    shake = Vector((0, 0, 0))
    if k >= 0 and 0 <= t - T[k] < 0.1:
        pd = new[k]["p"]
        for j in range(6):
            a = math.radians(-20 + j * 40)
            temp(box(f"pop{j}", (0.007, 0.004, 0.026), (pd.x + 0.062 * math.cos(a), -0.862, pd.z + 0.062 * math.sin(a)), mat("black"),
                     rot=(0, -math.degrees(a) + 90, 0)))
        shake = Vector((0.004 * (-1) ** fr, 0, 0.003 * (-1) ** (fr // 2)))
    look(cam, Vector((0.3, -2.25, 0.86)) + shake, Vector((0.33, -0.85, 0.7)) + shake, 40)


def anim_S4(fr):
    t, u = fr / FPS, prog(fr, "S4")
    f0, f1 = SF["S4"]
    step = (fr - f0) // 2 * 2 / max(1, f1 - 1 - f0)      # bursts every 2 frames (time-lapse)
    frac = 0.15 + 0.85 * ease(step)
    temp(make_dots("dots", dots_where(lambda d: d["order"] < frac)))
    th = -0.9 + 2 * math.pi * 1.1 * u                  # GUS laps the car
    a, b = 2.7, 1.5
    pos = Vector((a * math.cos(th), b * math.sin(th), 0))
    tan = Vector((-a * math.sin(th), b * math.cos(th), 0)).normalized()
    run = math.sin(fr * 1.4)
    pose(GUS, loc=tuple(pos), rz=math.degrees(math.atan2(tan.x, -tan.y)), hips=(30, 0, 0), head=(-25, 0, 0),
         armL=(-60 * run, 0, 6), armR=(60 * run, 0, -6), elbowL=-60, elbowR=-60, legL=(-45 * run, 0, 0), legR=(45 * run, 0, 0),
         mouth=0.3, lid=0.45)
    for i in range(1, 5):   # motion streaks along his path, on the floor
        q = th - 0.11 * i
        pq = Vector((a * math.cos(q), b * math.sin(q), 0.01))
        tq = Vector((-a * math.sin(q), b * math.cos(q), 0)).normalized()
        temp(box(f"speed{i}", (0.42 - 0.06 * i, 0.03, 0.006), tuple(pq), mat("black"), rot=(0, 0, math.degrees(math.atan2(tq.y, tq.x)))))
    look(cam, (-2.6, -1.2, 6.0), (0.25, -0.2, 0.6), 34, up=(1, 0, 0))


def anim_S5(fr):
    t = fr / FPS
    f0 = SF["S5"][0]
    dots = ALL_DOTS
    cen, lit, radius = pick_four(dots, "side_n", (1.3, 1.65), (0.66, 0.86))
    tc = f0 / FPS + 0.12
    on = ease((t - tc) / 0.13)
    lit = sorted(lit, key=lambda i: dots[i]["p"].x)
    lit_now = {i for j, i in enumerate(lit) if t >= tc + 0.12 + 0.07 * j}
    temp(make_dots("dots", dots, lit=lit_now))
    m, lid = talk("GUS", t, 0.45)
    acc = accent("GUS", t)
    pose(GUS, loc=(1.3, -1.95, 0), rz=180 - 6, hips=(14, 0, 0), head=(24 + 5 * acc, 0, 0), armL=(-70, 0, -4), elbowL=-28,
         armR=(-64, 0, 10), elbowR=-36, mouth=m, lid=lid, look=(0, -1))
    bpy.context.view_layer.update()
    hp = (GUS.hands["L"].matrix_world.translation + GUS.hands["R"].matrix_world.translation) / 2
    set_vis(SCANNER, True)
    SCANNER.location = hp + (cen - hp).normalized() * 0.12 + Vector((0, 0, 0.05))
    SCANNER.rotation_euler = (cen - SCANNER.location).to_track_quat("-Y", "Z").to_euler()
    bpy.context.view_layer.update()
    if on > 0.02:
        lens_ = SCANNER.matrix_world @ Vector((0, -0.12, 0.005))
        temp(light_cone("cone", lens_, cen + Vector((0, -0.004, 0)), radius * (0.3 + 0.7 * on)))
    look(cam, (3.3, -2.55, 1.35), (1.42, -1.05, 0.98), 42)


_PATCH_MESH = {}


def _patch_mesh(name, xr, yr, zr):
    if name in _PATCH_MESH:
        return _PATCH_MESH[name]
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
    bm = bmesh.new()
    bm.from_mesh(tmpme)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=10, use_grid_fill=True)
    for co, no in (((xr[0], 0, 0), (-1, 0, 0)), ((xr[1], 0, 0), (1, 0, 0)), ((0, yr[0], 0), (0, -1, 0)),
                   ((0, yr[1], 0), (0, 1, 0)), ((0, 0, zr[0]), (0, 0, -1)), ((0, 0, zr[1]), (0, 0, 1))):
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no, clear_outer=True)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    bpy.data.meshes.remove(tmpme)
    _PATCH_MESH[name] = me
    return me


PATCHES = [  # word order of line 6: Front. Side. Roof. Back.
    ("front", (0.75, 2.3), (-2, 2), (-1, 2), (0.75, 0.0, 0.15), "#dfe2df"),
    ("side", (-1.55, 1.2), (-2, -0.25), (-1, 1.05), (0.0, -0.75, 0.0), "#c3c8c3"),
    ("roof", (-1.35, 1.15), (-2, 2), (0.92, 2.0), (0.0, 0.0, 0.7), "#eceeec"),
    ("back", (-2.3, -0.8), (-2, 2), (-1, 2), (-0.75, 0.0, 0.12), "#d3d7d3"),
]


def anim_S6(fr):
    t, u = fr / FPS, prog(fr, "S6")
    temp(make_dots("dots", ALL_DOTS))
    W = [w["t0"] for w in words_of(6)][:4]
    while len(W) < 4:
        W.append(W[-1] + 0.35)
    t_lift = W[3] + 0.2
    lift = ease((t - t_lift) / 0.4)
    for k, (nm, xr, yr, zr, off, col) in enumerate(PATCHES):
        al = 0.6 * eout((t - W[k]) / 0.13)
        if al < 0.03:
            continue
        al = round(al * 20) / 20
        me = _patch_mesh(f"patchmesh_{nm}", xr, yr, zr).copy()
        me.materials.clear()
        me.materials.append(scan_patch_mat(al, col))
        me.materials.append(OUTLINE)
        ob = bpy.data.objects.new(f"patch_{nm}", me)
        COLL.objects.link(ob)
        o = Vector(off)
        ob.location = o.normalized() * 0.03 + (o - o.normalized() * 0.03) * lift
        add_mods(ob, 0, 0.016)
        temp(ob)
    # GUS behind the rear-left corner, scanner up; his head follows the section being captured
    heads = [(-10, 0, -40), (-6, 0, -15), (-30, 0, -5), (0, 0, 25)]
    hk = sum(1 for w in W if t >= w - 0.05) - 1
    if hk < 0:
        hd = heads[0]
    elif hk >= 3:
        hd = heads[3]
    else:
        hd = lerpv(heads[hk], heads[hk + 1], ease((t - W[hk]) / max(0.1, W[hk + 1] - W[hk])))
    m, lid = talk("GUS", t, 0.45)
    pose(GUS, loc=(-3.05, 0.55, 0), rz=-115, hips=(-4, 0, 0), head=hd, armL=(-160, 0, -10), elbowL=-15,
         armR=(-10, 0, -15), elbowR=-20, mouth=m, lid=lid, look=(0.3, 1))
    attach(SCANNER, GUS.hands["L"], (0, -0.04, -0.12), (110, 0, 0))
    cam_push((2.5, -4.9, 4.9), (0.1, -0.15, 0.85), 22, 0.04 * ease(u))


DOOR_START, DOOR_NEAR, DOOR_SEAT = (0.16, 0.075, 18.0), (0.085, 0.022, 8.0), (0.0325, -0.04, 0.0)


def anim_S7(fr):
    t, u = fr / FPS, prog(fr, "S7")
    t0 = SF["S7"][0] / FPS
    W = words_of(7)
    t_snap = W[-1]["t0"]                       # snaps on "up"
    if t < t_snap:
        p = ease((t - t0) / max(0.2, t_snap - t0))
        door = lerpv(DOOR_START, DOOR_NEAR, p)
        door = (door[0] + 0.004 * math.sin(t * 13), door[1] + 0.003 * math.sin(t * 17), door[2] + 1.5 * math.sin(t * 9))
        snapped, ps = False, 1.0
    else:
        p = eback((t - t_snap) / 0.12, 2.0)
        door = lerpv(DOOR_NEAR, DOOR_SEAT, p)
        snapped = p >= 0.98
        ps = 1.0 + 0.6 * math.sin(math.pi * cl((t - t_snap - 0.08) / 0.25))
    set_vis(UI, False)
    ui2 = temp(empty("ui_anim", UI.parent, tuple(UI.location), (90, 0, 0)))
    build_screen_ui(ui2, door=door, snapped=snapped, pin_scale=ps)
    m, lid = talk("GUS", t, 0.45)
    pose(GUS, loc=(3.85, 2.3, 0), rz=180 - 22, hips=(16, 0, 0), head=(24 + 5 * accent("GUS", t), 0, 0), armL=(-58, 0, 8),
         elbowL=-40, armR=(-58 + 4 * math.sin(t * 6), 0, -4), elbowR=-40, mouth=m, lid=lid)
    look(cam, (2.72, 1.3, 1.8), (3.32, 3.13, 1.13), lerp(86, 104, ease(u)))


def anim_S8(fr):
    t, u = fr / FPS, prog(fr, "S8")
    f0, f1 = SF["S8"]
    n = f1 - f0
    set_vis(STOOL, True)
    STOOL.location = (-3.7, 2.7, 0)
    am = 150 + 360 * (0.4 * u + 2.4 * u * u)            # spinning up to a blur
    asec = 260 + 360 * (2.0 * u + 8.0 * u * u)
    HANDS["minute"].rotation_euler = (0, math.radians(am), 0)
    HANDS["second"].rotation_euler = (0, math.radians(asec), 0)
    HANDS["hour"].rotation_euler = (0, math.radians(300 + (am - 150) / 12), 0)
    wm = 360 * (0.4 + 4.8 * u) / n                      # degrees per frame
    ws = 360 * (2.0 + 16.0 * u) / n
    for nm, L_, w_, key, y, cnt, wv in (("minute", 0.33, 0.028, "black", -0.07, 8, wm), ("second", 0.36, 0.014, "sage", -0.078, 10, ws)):
        if wv < 6:
            continue
        step = min(wv, 300) / cnt
        for i in range(cnt):
            a = HANDS[nm].rotation_euler.y - math.radians(step * (i + 1))
            al = round(0.5 * (1 - i / cnt) * 20) / 20
            if al <= 0:
                continue
            piv = temp(empty(f"blur_{nm}{i}", CLOCK, (0, y - 0.0005 * i, 0), (0, math.degrees(a), 0)))
            box(f"blur_{nm}{i}m", (w_ * 1.6, 0.004, L_), (0, 0, L_ / 2 - 0.04), mat(key, al), piv)
    if u > 0.3:
        r = 0.42
        for side in (1, -1):
            for j, rr in enumerate((r + 0.14, r + 0.24)):
                for k in range(7):
                    a = math.radians(side * (55 + 6 * k + 8 * j) + 4 * math.sin(fr * 2.1 + j))
                    temp(box(f"whirr{side}{j}{k}", (0.03, 0.01, 0.045), (rr * math.sin(a), -0.03, rr * math.cos(a)), mat("black"), CLOCK,
                             rot=(0, math.degrees(a) + 90, 0)))
    L9 = LN[9]
    m, lid = talk("PIP", t, lerp(0.4, 0.6, ease((t - L9["t1"]) / 0.3)))
    side = ease((t - L9["t0"] + 0.05) / 0.15) * (1 - ease((t - L9["t1"] - 0.15) / 0.3))   # glance toward GUS's "No."
    pose(PIP, loc=(-3.7, 2.68, 0.565), rz=-6, hips=(lerp(14, 28, ease(u)), 0, 0), head=(lerp(4, 14, ease(u)), 0, -8 + 14 * side),
         armL=(-38, 0, 14), elbowL=-50, armR=(-38, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=m, lid=lid,
         look=lerpv((0.3, 1), (1, 0.2), side), brow=(-0.005, -8))
    temp(make_dots("dots", []))
    look(cam, (-3.5, -0.9, 1.6), (-3.82, 2.9, 1.62), 36)


def anim_S9(fr):
    t, u = fr / FPS, prog(fr, "S9")
    f0 = SF["S9"][0]
    peel_zone = [d for d in ALL_DOTS if d["region"] in ("side_n", "front", "hood")]
    order = sorted(peel_zone, key=lambda d: -d["p"].x)          # front to back
    n_end = sum(1 for d in peel_zone if d["p"].x > 0.25)
    n_peeled = int(lerp(n_end * 0.55, n_end, u))
    gone = set(id(d) for d in order[:n_peeled])
    temp(make_dots("dots", [d for d in ALL_DOTS if id(d) not in gone]))
    temp(dot_pile("pile", (1.0, -2.0, 0.0), n=int(lerp(330, 520, u)), radius=lerp(0.36, 0.42, u), height=lerp(0.24, 0.3, u), s=1.5))
    m, lid = talk("GUS", t, 0.45)
    pose(GUS, loc=(0.3, -1.55, 0), rz=-60, hips=(8, 0, 0), head=(12 + 5 * accent("GUS", t), 0, 0), armL=(-78, 0, -15), elbowL=-30,
         armR=(-20, 0, -12), elbowR=-25, mouth=m, lid=lid, look=(0.3, 0))
    # peel cycle (8 frames): reach the next dot, pull it off, flick it toward the pile
    ph = ((fr - f0) % 8) / 8
    cur = order[min(n_peeled, len(order) - 1)]
    reach = cur["p"] + Vector((0, -0.12, 0))
    flick = Vector((0.95, -1.8, 0.7))
    tgt = reach.lerp(flick, ease((ph - 0.35) / 0.4)) if ph >= 0.35 else flick.lerp(reach, ease(ph / 0.3))
    hp = aim_arm(GUS, "L", tgt)
    if 0.35 <= ph < 0.8:
        temp(make_dots("peeled", [dict(p=hp + Vector((0.0, -0.1, -0.05)), n=Vector((0.3, -1, 0.2)), s=1.3)]))
    set_vis(STOOL, True)
    STOOL.location = (2.05, -2.6, 0)
    pm, plid = talk("PIP", t, 0.55)
    pose(PIP, loc=(2.05, -2.58, 0.565), rz=-25, hips=(22, 0, 0), head=(10, 0, 18), armL=(-40, 0, 14), elbowL=-50,
         armR=(-40, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=pm, lid=plid, look=(-1, 0.2), brow=(-0.005, -8))
    look(cam, (2.4, -5.9, 1.55), (0.95, -1.25, 0.95), 28)


def anim_S10(fr):
    t = fr / FPS
    set_vis(PIPSCAN, False)   # never in the phone shots
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.15)))
    L = LN[11]
    tw = L["words"][0]["t0"]
    perk = eback((t - tw + 0.04) / 0.16)
    hop = 0.05 * math.sin(math.pi * cl((t - tw) / 0.25))
    reach = ease((t - tw - 0.3) / 0.4)                         # pulls the phone out after "Wait."
    m, lid = talk("PIP", t, lerp(0.5, 0.0, cl(perk)))
    acc = accent("PIP", t)
    pose(PIP, loc=(1.2, -2.6, hop), rz=-4, hips=(lerp(6, -4, perk), 0, 0), head=(lerp(6, -6, perk) + 5 * acc, 0, lerp(0, 6, perk)),
         armL=lerpv((4, 0, 6), (-62, 0, -8), reach), elbowL=lerp(-10, -80, reach), armR=(4, 0, -6), mouth=m, lid=lid,
         look=lerpv((0, 0), (0.5, 0.7), cl(perk)), brow=lerpv((-0.01, 0), (0.045, -14), cl(perk)))
    pose(GUS, loc=(-0.6, -1.4, 0), rz=30)
    if reach > 0.01:
        bpy.context.view_layer.update()
        # floating hand brings the phone up in front of his chest, a little to his left (in frame)
        rest = PIP.hands["L"].matrix_world.translation.copy()
        chest = PIP.neck.matrix_world.translation + Vector((0.12, -0.3, -0.08))
        hp = aim_arm(PIP, "L", rest.lerp(chest, reach))
        set_vis(PHONE, True)
        n = Vector(lerpv((0.0, 0.3, -1.0), (0.15, 0.8, 0.55), reach)).normalized()
        orient_phone(PHONE, hp + Vector((0.0, -0.03, lerp(-0.12, 0.13, reach))), n, up=lerpv((0, 1, 0), (0, 0, 1), reach))
    look(cam, (1.25, -4.2, 0.98), (1.2, -2.6, 0.86), 42)


def pip_holding(t, look_=(0.6, 0.6), lid_base=0.0):
    set_vis(PIPSCAN, False)
    """S11/S12 base: phone fixed in space (static corners in S11); only PIP's head and face move."""
    c, n, u, r = phone_pose_s11()
    m, lid = talk("PIP", t, lid_base)
    acc = accent("PIP", t)
    PIP.neck.rotation_euler = [math.radians(a) for a in (-12 + 6 * acc, 0, -16 + 3 * math.sin(t * 4))]
    set_face(PIP, m, lid, look_, (0.04, -12))
    return c, n, u, r


def anim_S11(fr):
    t = fr / FPS
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.15)))
    c, n, u, r = pip_holding(t)
    f = -Vector((n.x, n.y, 0)).normalized()
    pose(GUS, loc=(0, 0, 0), rz=math.degrees(math.atan2(f.x, -f.y)) + 25, hips=(6, 0, 0), head=(14, 0, 0), look=(0, -0.6))
    place_head_xy(GUS, c + n * 0.75 + r * 0.62)
    look(cam, c + n * 1.2 - r * 0.16 - u * 0.2, c - r * 0.16 - u * 0.2, 38, up=u)


def anim_S12(fr):
    t, k = fr / FPS, prog(fr, "S12")
    temp(make_dots("dots", dots_where(lambda d: d["order"] < 0.15)))
    c, n, u, r = pip_holding(t, look_=(0.9, 0.7))
    # GUS leans in from the right, his head beside the phone and just BEHIND the screen plane, so nothing of his can ever
    # block the screen during the push; profile toward the phone, face upright; he slides out of frame as the camera pushes
    f = -Vector((r.x, r.y, 0)).normalized()
    rz = math.degrees(math.atan2(f.x, -f.y))
    lean = eout((t - SF["S12"][0] / FPS) / 0.4)
    hx = lerp(14, 32, lean)
    m, lid = talk("GUS", t, 0.0)
    pose(GUS, loc=(0, 0, 0), rz=rz, hips=(hx, 0, 0), head=(-0.85 * hx, 0, 0), armL=(hx, 0, 8), armR=(hx, 0, -8), elbowL=-10,
         elbowR=-10, mouth=m, lid=lid, look=(0, -0.2), brow=(0.025, -4))
    want = c - n * 0.06 + r * lerp(0.62, 0.47, lean)        # head centre beside the screen (inner edge > 0.14 m off axis)
    bpy.context.view_layer.update()
    hc = GUS.neck.matrix_world @ Vector((0, 0, GUS.head_c))
    GUS.root.location += Vector((want.x - hc.x, want.y - hc.y, min(0.0, (c.z + 0.12) - hc.z)))
    s12_cam(c, n, u, k)


ANIM = {k: globals()[f"anim_{k}"] for k in SF}


def reset_anim():
    reset()
    pip_scanner("pouch")
    set_vis(PIPSCAN, True)
    set_vis(UI, True)
    STOOL.location = (-3.7, 2.7, 0)


# ----------------------------------------------------------------------------------------------------------------- run
CORN = os.path.join(OUT, "screen_corners.json")
corners = json.load(open(CORN)) if os.path.exists(CORN) else dict(
    doc="Phone-screen corners for compositing the real IS350 footage (corner-pin), stage 3 timing (partA_timeline.json). Pixels "
        "in the 1080x1920 frame, origin at the top-left corner of the image, x right, y down, floats. Corner order tl, tr, br, bl "
        "= the footage's own upright corners. Frames are reel frames at 30 fps. The screen renders as flat key colour #ff00ff "
        "(camera rays only); use it as the matte where anything overlaps the screen.",
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
        need_c = sh in ("S11", "S12")
        todo = (fr - f0) % EVERY == 0 and lo <= fr < hi and not os.path.exists(final) and (not ONLY or fr in ONLY)
        if not (todo or need_c):
            continue
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
        print(f"[anim] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if per:
        a0, b0 = SF[sh]
        corners["shots"][sh] = dict(frames=[a0, b0], static=(sh == "S11"), per_frame=per)
        if sh == "S12":
            corners["shots"][sh]["note"] = (f"push along the screen normal, lens {S12_LENS} mm, {S12_D0} m -> {S12_DEND:.4f} m; "
                                            f"last frame {b0 - 1} = full frame")
        corners["screen_full_frame"] = TL["screen_full_frame"]
        json.dump(corners, open(CORN, "w"), indent=1)
    if nr:
        print(f"[anim] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
