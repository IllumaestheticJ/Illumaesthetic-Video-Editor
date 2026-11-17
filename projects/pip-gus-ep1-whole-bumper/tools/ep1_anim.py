"""Pip & Gus Ep 1 "Why can't I just print the bumper I want?" - cartoon animation. Runs INSIDE the pilot's scene builder (same
characters, shop, rig, cel look) through its --exec hook, like Ep 0:

  cd projects/scan-tedium-explainer-reel/tools
  blender -b --factory-startup -P partA_scene.py -- --exec ../../pip-gus-ep1-whole-bumper/tools/ep1_anim.py \
      --out /home/user/media/work/ep1/frames --spp 4 --ep1shots E01,E02 [--every N] [--frames 50,120] [--scale 0.5]

Every frame is posed procedurally from ep1_timeline.json (word times of the approved take 2, job fe0cc2e8): reset, anim_<shot>,
render. Frames land in OUT/<shot>/<frame>.png (written via _tmp + rename, existing frames skipped: resumable).

Spine: Gus's "bill" - a receipt hanging from a rolling board (wall clock on top) that collects a picture for every cost and
grows to the floor. The only numbers anywhere are the owner's: 6-7 KG, ~$200, ~250 HRS. No brands. Pip is excited ->
impatient -> deflated -> excited; Gus is dry and matter-of-fact, never angry or sad.
"""
import re as _re

EP = "/home/user/Illumaesthetic-Video-Editor/projects/pip-gus-ep1-whole-bumper"
TL = json.load(open(os.path.join(EP, "ep1_timeline.json")))
FPS = TL["fps"]
LN = {L["n"]: L for L in TL["lines"]}
SF = {s["id"]: (s["f0"], s["f1"]) for s in TL["shots"]}
EVERY = int(arg("--every", "1"))
ONLY = {int(x) for x in arg("--frames", "").split(",") if x}
EP_SHOTS = [s for s in arg("--ep1shots", ",".join(SF)).split(",") if s]
FONT = bpy.data.fonts.load("/home/user/media/work/ep1/fonts/FjallaOne.ttf")


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
    return LN[n]["words"][i]["t0"]


def WE(n, i):
    return LN[n]["words"][i]["t1"]


def win(t, a, b, rin=0.12, rout=0.2):
    if t < a - rin or t > b + rout:
        return 0.0
    if t < a:
        return ease((t - (a - rin)) / rin)
    if t <= b:
        return 1.0
    return 1 - ease((t - b) / rout)


# ----------------------------------------------------------------------------------------------------------------- talk (pilot logic)
_V = _re.compile(r"[aeiouy]+")


def syllables(word):
    w = _re.sub(r"[^a-z]", "", word.lower())
    if w.isdigit() or not w:
        w = {"200": "twohundred", "250": "twohundredfifty", "3d": "threedee"}.get(word.lower().strip(".,?!"), "a")
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
    while x < 60:
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


def talk(spk, t, base_lid=0.0):
    return mouth_at(spk, t), max(base_lid, blink(spk, t), 0.2 * accent(spk, t))


# ----------------------------------------------------------------------------------------------------------------- faces (no brows)
for _ch in (GUS, PIP):
    for _b in _ch.browset:
        for _o in list(_b["piv"].children) + [_b["piv"]]:
            bpy.data.objects.remove(_o, do_unlink=True)
    _ch.browset = []

CUR_T = 0.0
STATES = {   # name: (fL, fR, shape, scale)
    "neutral": (0.0, 0.0, None, 1.0),
    "dry": (0.32, 0.32, None, 1.0),          # Gus: matter-of-fact half-lids
    "curious": (0.0, 0.0, None, 1.15),
    "surprised": (0.0, 0.0, None, 1.3),
    "excited": (0.0, 0.0, "arc", 1.0),
    "deflated": (0.5, 0.5, None, 0.95),
    "squeezed": (1.0, 1.0, "line", 1.0),
}


def expr_state(ch, t):
    st = dict(fL=0.0, fR=0.0, shape=None, scale=1.0)

    def blend(name, k):
        if k <= 0:
            return
        tgt = dict(zip(("fL", "fR", "shape", "scale"), STATES[name]))
        for key in ("fL", "fR", "scale"):
            st[key] = lerp(st[key], tgt[key], k)
        if tgt["shape"] and k > 0.5:
            st["shape"] = tgt["shape"]

    if ch is GUS:
        blend("dry", 1.0)                                                   # dry baseline
        blend("neutral", win(t, LN[1]["t0"], LN[1]["t1"], 0.2, 0.2))        # listening to Pip
        blend("neutral", win(t, LN[11]["t0"], LN[11]["t1"], 0.2, 0.2))
        blend("excited", win(t, W(12, 2), LN[12]["t1"] + 0.4, 0.1, 0.3) * 0.9)   # "We'll show you how." - small warm smile
        blend("neutral", win(t, LN[14]["t0"] - 0.3, LN[14]["t1"] + 0.5, 0.2, 0.2))
    else:
        blend("excited", win(t, LN[1]["t0"], LN[1]["t1"] + 0.2, 0.08, 0.3))
        blend("curious", win(t, LN[2]["t0"], LN[5]["t1"], 0.3, 0.2) * 0.8)
        blend("surprised", win(t, W(3, 9), W(3, 9) + 0.8, 0.06, 0.3))         # "two hundred"
        blend("squeezed", win(t, W(5, 3) + 0.1, W(5, 3) + 0.9, 0.06, 0.15))   # in the sanding cloud
        blend("curious", win(t, LN[7]["t0"], LN[8]["t1"], 0.2, 0.2) * 0.6)
        blend("surprised", win(t, W(7, 3), W(7, 3) + 0.7, 0.06, 0.3))         # "250 hours"
        blend("deflated", win(t, LN[9]["t0"] - 0.2, LN[10]["t1"] - 2.0, 0.3, 0.4))
        blend("curious", win(t, W(10, 9), LN[10]["t1"], 0.2, 0.3))            # the exceptions - Pip perks up
        blend("excited", win(t, LN[11]["t0"], LN[11]["t1"] + 0.2, 0.08, 0.3))
        blend("surprised", win(t, W(12, 3), LN[12]["t1"], 0.1, 0.2))
        blend("excited", win(t, LN[13]["t0"] - 0.1, 60, 0.08, 0.3))
    return st


def apply_expr(ch, lid_call=0.0):
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
    apply_expr(ch, max(ch.S.get("base_lid", 0.0), kw.get("lid", 0.0)))


def gus_pose(t, loc, rz, look_=(0, 0), hips=(0, 0, 0), head=(0, 0, 0), armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12, elbowR=-12):
    m, lid = talk("GUS", t)
    acc = accent("GUS", t)
    pose(GUS, loc=loc, rz=rz, hips=hips, head=(head[0] + 6 * acc, head[1], head[2]), armL=armL, armR=armR, elbowL=elbowL,
         elbowR=elbowR, mouth=0.9 * m, lid=lid, look=look_)


def pip_pose(t, loc, rz, look_=(0, 0), hips=(0, 0, 0), head=(0, 0, 0), armL=(4, 0, 6), armR=(4, 0, -6), elbowL=-12, elbowR=-12,
             hop=0.0):
    m, lid = talk("PIP", t)
    acc = accent("PIP", t)
    pose(PIP, loc=(loc[0], loc[1], loc[2] + hop), rz=rz, hips=hips, head=(head[0] + 6 * acc, head[1], head[2]), armL=armL,
         armR=armR, elbowL=elbowL, elbowR=elbowR, mouth=m, lid=lid, look=look_)


def cam_push(loc, target, lens, k, up=(0, 0, 1)):
    loc, target = Vector(loc), Vector(target)
    look(cam, target + (loc - target) * (1 - k), target, lens, up=up)


# ----------------------------------------------------------------------------------------------------------------- prop helpers
def path_tube(name, pts, rt, m, parent=None, loc=(0, 0, 0), rs=8, ol=0.0):
    bm = bmesh.new()
    pts = [Vector(p) for p in pts]
    rings = []
    for i, p in enumerate(pts):
        tg = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)])
        tg = tg.normalized() if tg.length > 1e-6 else Vector((1, 0, 0))
        a = tg.orthogonal().normalized()
        b = tg.cross(a)
        rings.append([bm.verts.new(p + (a * math.cos(2 * math.pi * k / rs) + b * math.sin(2 * math.pi * k / rs)) * rt)
                      for k in range(rs)])
    for i in range(len(rings) - 1):
        for k in range(rs):
            bm.faces.new((rings[i][k], rings[i + 1][k], rings[i + 1][(k + 1) % rs], rings[i][(k + 1) % rs]))
    for r_ in (rings[0], rings[-1]):
        bm.faces.new(r_)
    ob = new_obj(name, bm, [m, OUTLINE] if ol else [m], parent, loc)
    return add_mods(ob, 0, ol)


def text3d(name, body, size, key, parent=None, loc=(0, 0, 0), rot=(90, 0, 0), extrude=0.004, align="CENTER", glow=1.0):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.font = FONT
    cu.size = size
    cu.extrude = extrude
    cu.align_x = align
    cu.align_y = "CENTER"
    ob = bpy.data.objects.new(name, cu)
    COLL.objects.link(ob)
    ob.data.materials.append(emit(key, glow))
    ob.parent = parent
    ob.location = loc
    ob.rotation_euler = [math.radians(a) for a in rot]
    return ob


# v2 (owner): every bumper is OUR 350Z bumper (part_front_bumper of the epsilon.plus lookbook eps-nissan-350z-z33-v24.glb,
# decimated to 28k faces: /home/user/media/work/ep1/z350/bumper350.obj). Normalised: width 1.48, front at y=0 (wraps +y), z>=0.
from mathutils import Quaternion
from mathutils.bvhtree import BVHTree
BUMP_OBJ = "/home/user/media/work/ep1/z350/bumper350.obj"


def _load_bumper():
    before = set(bpy.data.objects)
    bpy.ops.wm.obj_import(filepath=BUMP_OBJ, forward_axis="Y", up_axis="Z")
    ob = [o for o in bpy.data.objects if o not in before][0]
    me = ob.data
    bpy.data.objects.remove(ob, do_unlink=True)
    xs, ys, zs = ([v.co[i] for v in me.vertices] for i in range(3))
    k = 1.48 / (max(xs) - min(xs))
    cx, y0, z0 = (max(xs) + min(xs)) / 2, min(ys), min(zs)
    for v in me.vertices:
        v.co = Vector(((v.co.x - cx) * k, (v.co.y - y0) * k, (v.co.z - z0) * k))
    bm = bmesh.new()   # drop slivers: they spike the outline shell
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0008)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=0.0008)
    bm.to_mesh(me)
    bm.free()
    me.materials.clear()
    for pg in me.polygons:
        pg.material_index = 0
        pg.use_smooth = True
    try:
        me.set_sharp_from_angle(angle=math.radians(35))
    except Exception:
        pass
    bvh = BVHTree.FromPolygons([v.co.copy() for v in me.vertices], [list(pg.vertices) for pg in me.polygons])
    return me, (max(zs) - z0) * k, bvh


BUMP_ME, BUMP_H, BUMP_BVH = _load_bumper()


def bump_front(x, z):
    """Front-surface point of the (unit) 350Z bumper at (x, z), or None (grille opening / off the part)."""
    hit = BUMP_BVH.ray_cast(Vector((x, -1.0, z)), Vector((0, 1, 0)))
    return hit[0] if hit[0] is not None and hit[0].y < 0.3 else None


def bumper_mesh(name, key, parent=None, loc=(0, 0, 0), s=1.0, seams=True, rz=0.0, flat=False):
    """Our 350Z front bumper (faces -y, width 1.48 s, bottom at z=0). seams: printed-in-sections glue lines."""
    g = empty(name, parent, loc, (0, 0, rz))
    ob = bpy.data.objects.new(name + "_m", BUMP_ME.copy())
    COLL.objects.link(ob)
    ob.parent = g
    ob.scale = (s, s * (0.1 if flat else 1.0), s)   # flat: a printed picture (catalog page, box art) in relief
    if flat:
        ob.location = (0, -0.07 * s, 0)
    ob.data.materials.append(mat(key, hl=True))
    ob.data.materials.append(OUTLINE)
    add_mods(ob, 0, 0.012)
    ob.modifiers["ol"].use_even_offset = False
    if seams:
        for x in (-0.5, -0.17, 0.17, 0.5):
            seg = []
            for j in range(18):
                z = 0.02 + (BUMP_H - 0.04) * j / 17
                hp = bump_front(x, z)
                if hp is None or (seg and (hp - seg[-1]).length > 0.08):
                    if len(seg) > 2:
                        path_tube(f"{name}_seam{x:.2f}_{j}", [q * s for q in seg], 0.006 * s, mat("#5e625e"), g, rs=6)
                    seg = []
                    if hp is None:
                        continue
                seg.append(hp + Vector((0, -0.006, 0)))
            if len(seg) > 2:
                path_tube(f"{name}_seam{x:.2f}", [q * s for q in seg], 0.006 * s, mat("#5e625e"), g, rs=6)
    return g


def spool(name, key, parent=None, loc=(0, 0, 0)):
    g = empty(name, parent, loc)
    cyl(name + "_r", 0.13, 0.11, (0, 0, 0), mat(key, hl=True), g, axis="X", bevel=0.015, ol=0.014)
    cyl(name + "_f0", 0.15, 0.015, (-0.06, 0, 0), mat("#3a3d3a"), g, axis="X", ol=0.01)
    cyl(name + "_f1", 0.15, 0.015, (0.06, 0, 0), mat("#3a3d3a"), g, axis="X", ol=0.01)
    cyl(name + "_h", 0.035, 0.14, (0, 0, 0), mat("dark"), g, axis="X")
    return g


def spaghetti(name, parent=None, loc=(0, 0, 0), s=1.0, seed=3, n=46, key="sage_l", frac=1.0, base=True):
    """v2 (owner: 'doesn't look accurate'): a real failed print = a part that stopped growing a few cm up (a stub of the
    350Z bumper, sliced flat) under an airy nest of thin, tightly curled filament loops. frac 0..1 grows the nest."""
    g = empty(name, parent, loc)
    rng = random.Random(seed)
    m = mat(key, hl=True)
    if base:   # the half-printed section: a slice of the bumper's corner, flat top
        bm = bmesh.new()
        bm.from_mesh(BUMP_ME)
        hz = 0.11
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, hz), plane_no=(0, 0, 1),
                               clear_outer=True)
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0.2, 0, 0), plane_no=(-1, 0, 0),
                               clear_outer=True)
        ob = bpy.data.objects.new(name + "_part", bpy.data.meshes.new(name + "_part"))
        bm.to_mesh(ob.data)
        bm.free()
        COLL.objects.link(ob)
        ob.parent = g
        ob.data.materials.append(m)
        ob.data.materials.append(OUTLINE)
        ob.scale = (0.42 * s,) * 3
        ob.location = (-0.42 * s * 0.25, -0.05 * s, 0)
        add_mods(ob, 0, 0.01)
        ob.modifiers["ol"].use_even_offset = False
        for k in range(4):   # layer lines on the stub
            box(f"{name}_ly{k}", (0.24 * s, 0.002, 0.002), (-0.03 * s, -0.052 * s, (0.012 + 0.009 * k) * s), mat("#7c807c"), g)
    # the nest: a curvature random walk (tight curls 2-4 cm), bounded in an ellipsoid sitting on the stub
    N = max(2, int(900 * cl(frac)))
    p = Vector((0.0, -0.02, 0.05)) * s
    d = Vector((1, 0, 0.2)).normalized()
    ax = Vector((0, 0, 1))
    pts = [p.copy()]
    C = Vector((0, -0.02, 0.1)) * s
    R = Vector((0.17, 0.13, 0.1)) * s
    for i in range(N):
        ax = (ax + Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))) * 0.35).normalized()
        d = (Quaternion(ax, rng.uniform(0.35, 0.6)) @ d).normalized()
        q = Vector(((p.x - C.x) / R.x, (p.y - C.y) / R.y, (p.z - C.z) / R.z))
        if q.length > 1.0:
            d = (d - q.normalized() * 0.5).normalized()
        p = p + d * 0.011 * s
        p.z = max(p.z, 0.006 * s)
        pts.append(p.copy())
    path_tube(name + "_fil", pts, 0.0032 * s, m, g, rs=5)
    return g


# ----------------------------------------------------------------------------------------------------------------- the bill board
BOARD_XY = (0.12, -1.45)
TOP_Z = 1.72
SLOT0, SLOT = 0.12, 0.105   # v2: 13 rows fit on the whiteboard panel
BOARD_S = 1.42   # whole board group scale: icons read at 1080 wide


def build_board():
    g = empty("BOARD", None, (BOARD_XY[0], BOARD_XY[1], 0))
    m = mat("#3a3d3a")
    for x in (-0.42, 0.42):
        box(f"bd_leg{x}", (0.05, 0.05, TOP_Z + 0.05), (x, 0.05, (TOP_Z + 0.05) / 2), m, g, ol=0.01)
        box(f"bd_foot{x}", (0.08, 0.5, 0.05), (x, 0.05, 0.03), m, g, ol=0.01)
        for y in (-0.18, 0.28):
            cyl(f"bd_wheel{x}{y}", 0.035, 0.03, (x, y, 0.035), mat("dark"), g, axis="X")
    box("bd_top", (0.94, 0.06, 0.07), (0, 0.05, TOP_Z), m, g, bevel=0.01, ol=0.012)
    box("bd_clip", (0.62, 0.05, 0.06), (0, -0.0, TOP_Z - 0.06), mat("sage"), g, bevel=0.01, ol=0.01)
    g.scale = (BOARD_S,) * 3
    return g


BOARD = build_board()
# v2 (owner: 'the list comes off the whiteboard'): a fixed whiteboard panel that holds every row; nothing hangs past it.
RECEIPT = empty("RECEIPT", BOARD, (0, 0, 0))
WB_TOP, WB_BOT = TOP_Z - 0.09, 0.14
box("wb_panel", (0.76, 0.012, WB_TOP - WB_BOT), (0, -0.02, (WB_TOP + WB_BOT) / 2), mat("white"), RECEIPT, ol=0.006)
for _n, _sz, _lc in (("t", (0.79, 0.02, 0.025), (0, -0.022, WB_TOP)), ("b", (0.79, 0.02, 0.025), (0, -0.022, WB_BOT)),
                     ("l", (0.025, 0.02, WB_TOP - WB_BOT), (-0.39, -0.022, (WB_TOP + WB_BOT) / 2)),
                     ("r", (0.025, 0.02, WB_TOP - WB_BOT), (0.39, -0.022, (WB_TOP + WB_BOT) / 2))):
    box(f"wb_rim{_n}", _sz, _lc, mat("metal"), RECEIPT, ol=0.005)
box("wb_tray", (0.6, 0.07, 0.02), (0, -0.06, WB_BOT - 0.005), mat("metal"), RECEIPT, ol=0.005)
box("wb_marker", (0.11, 0.022, 0.022), (0.12, -0.07, WB_BOT + 0.015), mat("sage"), RECEIPT, 0.006, 0.004)
# icon pictures (static meshes on the board, revealed in order). Each: (key, builder, label or None)
ICONS = []


def _slot(i):
    return (-0.14, -0.045, TOP_Z - 0.08 - SLOT0 - i * SLOT)


def icon(name, i, build, label=None, lab_size=0.085):
    g = empty(name, BOARD, _slot(i))
    build(g)
    g["s0"] = 1.25
    lab = None
    if label:
        lab = text3d(name + "_lab", label, lab_size, "#0b0c0b", BOARD, (0.1, -0.04, _slot(i)[2]), glow=1.0, align="LEFT")
        lab.location.x = -0.04
    ICONS.append(dict(name=name, g=g, lab=lab))
    return g


def ic_spray(g):
    cyl("i_spray_b", 0.03, 0.09, (0, 0, -0.01), mat("white", hl=True), g, ol=0.006)
    cyl("i_spray_c", 0.018, 0.025, (0, 0, 0.045), mat("sage"), g, ol=0.005)


def build_leo(g, s=1.0):
    """v2 (owner): cartoon Artec Leo - charcoal head with a big black front window (centre lens, two side lenses, a row of
    white flash LEDs), wide touchscreen on the back showing a green scan, rubber pistol grip underneath. Lens faces -y."""
    S = lambda *v: tuple(c * s for c in v)
    box("leo_head", S(0.2, 0.14, 0.13), S(0, 0, 0), mat("#4a4d4a", hl=True), g, 0.03 * s, 0.01 * s)
    box("leo_side", S(0.206, 0.09, 0.06), S(0, 0.01, -0.02), mat("#8d918d"), g, 0.012 * s)
    box("leo_face", S(0.17, 0.012, 0.1), S(0, -0.068, 0.005), mat("#151615"), g, 0.012 * s, 0.004 * s)
    cyl("leo_lens", 0.027 * s, 0.012 * s, S(0, -0.074, 0.01), mat("#2b2e2b"), g, axis="Y", ol=0.003 * s)
    cyl("leo_lensg", 0.013 * s, 0.006 * s, S(0, -0.081, 0.01), emit("sage_l", 1.6), g, axis="Y")
    for _x in (-0.055, 0.055):
        cyl(f"leo_cam{_x}", 0.014 * s, 0.01 * s, S(_x, -0.074, 0.012), mat("#2b2e2b"), g, axis="Y", ol=0.003 * s)
        cyl(f"leo_camg{_x}", 0.006 * s, 0.006 * s, S(_x, -0.08, 0.012), emit("#9fd8ff", 1.3), g, axis="Y")
    for _k in range(6):
        box(f"leo_led{_k}", S(0.012, 0.004, 0.008), S(-0.0625 + 0.025 * _k, -0.076, -0.03), emit("white", 2.0), g)
    scr = empty("leo_scr", g, S(0, 0.072, 0.012), (-18, 0, 0))
    box("leo_bezel", S(0.18, 0.012, 0.115), (0, 0, 0), mat("#151615"), scr, 0.008 * s, 0.004 * s)
    box("leo_disp", S(0.16, 0.004, 0.095), S(0, 0.007, 0), emit("#2e4a36", 1.0), scr)
    for _k in range(5):   # a little green scan mesh on the display
        box(f"leo_ui{_k}", S(0.11 - 0.012 * abs(_k - 2), 0.002, 0.006), S(0, 0.0095, -0.03 + 0.015 * _k), emit("sage_l", 1.4), scr)
    box("leo_grip", S(0.055, 0.07, 0.15), S(0, 0.03, -0.12), mat("#232523"), g, 0.02 * s, 0.008 * s, rot=(-22, 0, 0))
    box("leo_trig", S(0.03, 0.02, 0.03), S(0, -0.008, -0.075), mat("sage"), g, 0.006 * s, 0.003 * s, rot=(-22, 0, 0))
    return g


# replace the pilot's generic scanner prop with the Leo (same object, same -y lens convention)
for _c in list(SCANNER.children):
    for _o in [_c] + list(_c.children_recursive):
        pass
    _stack = [_c]
    while _stack:
        _o = _stack.pop()
        _stack.extend(_o.children)
        bpy.data.objects.remove(_o, do_unlink=True)
build_leo(SCANNER, 0.85)


def ic_scanner(g):
    """Bill picture of the Leo, turned three-quarters from the back so its screen and grip read."""
    sub = empty("i_leo", g, (0, 0, 0.012), (0, 0, 145))
    build_leo(sub, 0.55)


def ic_laptop(g):
    box("i_lap_s", (0.1, 0.008, 0.065), (0, 0, 0.02), mat("#2b2e2b"), g, 0.004, 0.005)
    box("i_lap_scr", (0.085, 0.004, 0.05), (0, -0.006, 0.02), emit("sage_l", 1.0), g)
    box("i_lap_k", (0.11, 0.03, 0.01), (0, -0.01, -0.017), mat("#2b2e2b"), g, 0.003, 0.005)


def ic_spools(g):
    for k, (x, z) in enumerate(((-0.03, -0.02), (0.03, -0.02), (0.0, 0.03))):
        cyl(f"i_sp{k}", 0.028, 0.025, (x, 0, z), mat(("sage", "white", "#555855")[k], hl=True), g, axis="Y", ol=0.005)


def ic_cash(g):
    box("i_cash", (0.11, 0.006, 0.06), (0, 0, 0), mat("#9fc4a8"), g, 0.004, 0.005)
    cyl("i_cash_c", 0.017, 0.008, (0, -0.004, 0), mat("sage"), g, axis="Y")


def ic_spag(g):
    spaghetti("i_spag", g, (0, 0, -0.04), s=0.35, seed=8, n=30)


def ic_glue(g):
    cyl("i_glue", 0.022, 0.07, (0, 0, -0.005), mat("white", hl=True), g, ol=0.005)
    cyl("i_glue_c", 0.014, 0.03, (0, 0, 0.045), mat("sage"), g, r2=0.003, ol=0.004)


def ic_knife(g):
    box("i_kn_b", (0.06, 0.004, 0.05), (0.01, 0, -0.01), mat("metal"), g, ol=0.004, rot=(0, 20, 0))
    box("i_kn_h", (0.02, 0.012, 0.05), (-0.03, 0, 0.03), mat("wood"), g, 0.004, 0.004, rot=(0, 20, 0))


def ic_sand(g):
    box("i_sand", (0.09, 0.03, 0.035), (0, 0, 0), mat("#c9a96e"), g, 0.006, 0.005)
    for k in range(3):
        blob(f"i_dust{k}", (0.015, 0.008, 0.015), (-0.04 + 0.04 * k, -0.01, 0.04 + 0.01 * (k % 2)), mat("#d9dbd8"), g)


def ic_primer(g):
    cyl("i_pr_b", 0.028, 0.085, (0, 0, -0.01), mat("#7c807c", hl=True), g, ol=0.005)
    cyl("i_pr_c", 0.016, 0.02, (0, 0, 0.042), mat("white"), g, ol=0.004)


def ic_clock(g):
    cyl("i_ck", 0.035, 0.01, (0, 0, 0), mat("white"), g, axis="Y", ol=0.005)
    box("i_ck_h", (0.006, 0.004, 0.028), (0, -0.007, 0.012), mat("black"), g)
    box("i_ck_m", (0.022, 0.004, 0.006), (0.009, -0.007, 0), mat("black"), g)


def ic_weight(g):
    hull("i_wt", [(-0.045, 0, -0.03), (0.045, 0, -0.03), (-0.03, 0, 0.03), (0.03, 0, 0.03),
                  (-0.045, 0.02, -0.03), (0.045, 0.02, -0.03), (-0.03, 0.02, 0.03), (0.03, 0.02, 0.03)], mat("#3a3d3a"), g,
         bevel=0.004, ol=0.005)
    torus("i_wt_r", 0.014, 0.004, (0, 0.01, 0.042), mat("#3a3d3a"), g, rot=(90, 0, 0))


def ic_crack(g):
    path_tube("i_crack", [(-0.05, 0, 0.03), (-0.02, 0, 0.0), (-0.01, 0, 0.02), (0.02, 0, -0.01), (0.03, 0, 0.01), (0.05, 0, -0.03)],
              0.005, mat("red"), g, rs=6)


icon("ic_spray", 0, ic_spray)
icon("ic_scanner", 1, ic_scanner)
icon("ic_laptop", 2, ic_laptop)
icon("ic_spools", 3, ic_spools, "6-7 KG")
icon("ic_cash", 4, ic_cash, "~$200")
icon("ic_spag", 5, ic_spag)
icon("ic_glue", 6, ic_glue)
icon("ic_knife", 7, ic_knife)
icon("ic_sand", 8, ic_sand)
icon("ic_primer", 9, ic_primer)
icon("ic_clock", 10, ic_clock, "~250 HRS")
icon("ic_weight", 11, ic_weight)
icon("ic_crack", 12, ic_crack)
ICON_T = {   # when each picture lands on the bill (reel s)
    "ic_spray": W(2, 1), "ic_scanner": W(2, 2) + 0.15, "ic_laptop": W(2, 4), "ic_spools": W(3, 0), "ic_cash": W(3, 9),
    "ic_spag": W(4, 2), "ic_glue": W(5, 1), "ic_knife": W(5, 2), "ic_sand": W(5, 3), "ic_primer": W(5, 4),
    "ic_clock": W(7, 3), "ic_weight": W(8, 3), "ic_crack": W(8, 5),
}


def bill(t, extra=0.0):
    """Reveal icons up to time t (pop with overshoot); receipt length follows the last revealed slot (+ extra)."""
    n = 0
    for k, ic in enumerate(ICONS):
        ta = ICON_T[ic["name"]]
        on = t >= ta
        set_vis(ic["g"], on)
        if ic["lab"]:
            set_vis(ic["lab"], on)
        if on:
            n = k + 1
            s = eback((t - ta) / 0.22, 2.2)
            ic["g"].scale = (s * 1.25,) * 3
            if ic["lab"]:
                ic["lab"].scale = (s, s, s)
    L = n
    return L


def receipt_curl(k):
    """v1 gag (bill curling on the floor) removed in v2: the list stays on the whiteboard."""
    return


# clock rides on top of the board
CLOCK.scale = (0.45, 0.45, 0.45)


def clock_on_board(spin=0.0, fall=0.0):
    CLOCK.parent = BOARD
    CLOCK.location = (0, -0.02 - 0.6 * fall, TOP_Z + 0.26 - 2.3 * fall ** 2)
    CLOCK.rotation_euler = (math.radians(-80 * fall), 0, math.radians(40 * fall))
    a = spin
    HANDS["hour"].rotation_euler = (0, math.radians(300 + a / 12), 0)
    HANDS["minute"].rotation_euler = (0, math.radians(60 + a), 0)
    HANDS["second"].rotation_euler = (0, math.radians(200 + 3 * a), 0)


# ----------------------------------------------------------------------------------------------------------------- other props
DRAW = empty("DRAWING")
DRAW_S = 1.45
box("dr_paper", (0.42, 0.006, 0.3), (0, 0, 0), mat("white"), DRAW, ol=0.006)


def _drawing_mat():
    """Crayon sketch of our 350Z bumper (traced from the lookbook model: z350/drawing.png), on the paper's front face."""
    m = bpy.data.materials.new("m_drawing")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1 / 0.4, 1, 1 / 0.28)
    mp.inputs["Location"].default_value = (0.5, 0, 0.5)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    com = nt.nodes.new("ShaderNodeCombineXYZ")
    im = nt.nodes.new("ShaderNodeTexImage")
    im.image = bpy.data.images.load("/home/user/media/work/ep1/z350/drawing.png")
    im.extension = "CLIP"
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], sep.inputs[0])
    nt.links.new(sep.outputs["X"], com.inputs["X"])
    nt.links.new(sep.outputs["Z"], com.inputs["Y"])
    nt.links.new(com.outputs[0], im.inputs["Vector"])
    nt.links.new(im.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs["Surface"])
    return m


box("dr_art", (0.4, 0.002, 0.28), (0, -0.0045, 0), _drawing_mat(), DRAW)


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
    g.location = (2.75, 3.12, 0.955)
    return g, gantry, head


PRINTER, PR_GANTRY, PR_HEAD = build_printer()
SHELF = empty("SHELF", None, (3.75, 3.4, 1.45))
box("sh_board", (0.9, 0.3, 0.03), (0, 0, 0), mat("wood"), SHELF, bevel=0.005, ol=0.01)
for _i, _x in enumerate((-0.32, -0.12, 0.1)):
    spaghetti(f"sh_spag{_i}", SHELF, (_x, 0, 0.015), s=0.7, seed=20 + _i, key=("sage_l", "white", "#555855")[_i])

SPOOLS = [spool(f"SPOOL{k}", ("sage", "white", "#555855", "sage_l")[k % 4]) for k in range(9)]

BENCH_BUMP = bumper_mesh("BENCH_BUMP", "sage_l", None, (3.55, 3.12, 0.96), s=0.62)
PRIMED_KEY = "#9a9e9a"
GLUE = empty("GLUE")
cyl("gl_body", 0.05, 0.16, (0, 0, 0.08), mat("white", hl=True), GLUE, bevel=0.01, ol=0.012)
cyl("gl_cap", 0.03, 0.06, (0, 0, 0.19), mat("sage"), GLUE, r2=0.006, ol=0.01)
KNIFE = empty("KNIFE")
box("kn_blade", (0.16, 0.008, 0.1), (0, 0, 0), mat("metal"), KNIFE, ol=0.008)
box("kn_handle", (0.05, 0.03, 0.14), (0, 0.0, 0.11), mat("wood"), KNIFE, 0.01, 0.01)
SANDER = empty("SANDER")
box("sd_block", (0.18, 0.08, 0.07), (0, 0, 0), mat("#c9a96e"), SANDER, 0.015, 0.01)
CAN = empty("CAN")
cyl("can_b", 0.055, 0.2, (0, 0, 0), mat("#7c807c", hl=True), CAN, ol=0.01)
cyl("can_c", 0.035, 0.05, (0, 0, 0.12), mat("white"), CAN, ol=0.008)

SCALE_G = empty("SCALE", None, (0.05, -2.05, 0))
box("sc_plat", (0.9, 0.55, 0.08), (0, 0, 0.04), mat("#3a3d3a"), SCALE_G, 0.01, 0.012)
box("sc_top", (0.86, 0.5, 0.012), (0, 0, 0.086), mat("metal"), SCALE_G, ol=0.006)
box("sc_post", (0.06, 0.06, 0.55), (0, 0.24, 0.35), mat("#3a3d3a"), SCALE_G, ol=0.01)
cyl("sc_dial", 0.16, 0.04, (0, 0.2, 0.7), mat("white"), SCALE_G, axis="Y", ol=0.012)
SC_NEEDLE = empty("sc_needle", SCALE_G, (0, 0.17, 0.7))
box("sc_ndl", (0.012, 0.006, 0.13), (0, 0, 0.055), mat("red"), SC_NEEDLE)
for _k in range(7):
    _a = math.radians(-120 + 40 * _k)
    box(f"sc_tick{_k}", (0.01, 0.006, 0.03), (0.13 * math.sin(_a), 0.176, 0.7 + 0.13 * math.cos(_a)), mat("black"), SCALE_G,
        rot=(0, math.degrees(_a), 0))
SC_BUMP = bumper_mesh("SC_BUMP", PRIMED_KEY, None, (0, 0, 0), s=0.72)
CURB = box("CURB", (0.35, 0.3, 0.16), (0, 0, 0.08), mat("#b8bab6"), None, 0.01, 0.012)
CRACK = path_tube("CRACK", [(-0.1, 0, 0.2), (-0.05, 0, 0.12), (-0.07, 0, 0.08), (0.0, 0, 0.03)], 0.008, mat("black"), None, rs=6)

STOREBOX = empty("STOREBOX")
box("sb_box", (0.9, 0.3, 0.45), (0, 0, 0.225), mat("#c49a6c"), STOREBOX, 0.01, 0.012)
box("sb_tape", (0.9, 0.31, 0.04), (0, 0, 0.3), mat("#a07a52"), STOREBOX)
bumper_mesh("sb_pic", "sage", STOREBOX, (0, -0.15, 0.06), s=0.36, seams=False, flat=True)

CATALOG = empty("CATALOG", None, (-3.1, 3.5, 1.55))
box("cat_page", (1.0, 0.01, 1.3), (0, 0, 0), mat("white"), CATALOG, ol=0.008)
bumper_mesh("cat_bump", "#5d718a", CATALOG, (0, 0.0, 0.05), s=0.56, seams=False, flat=True)
for _k in range(3):
    box(f"cat_line{_k}", (0.6 - 0.12 * _k, 0.004, 0.035), (0, -0.012, -0.32 - 0.08 * _k), mat("#c6c8c5"), CATALOG)
STAMP = text3d("STAMP", "DISCONTINUED", 0.2, "red", CATALOG, (0, -0.14, -0.08), rot=(90, 0, 12), extrude=0.01, glow=1.0)
STAMP_BOX = empty("STAMP_BOX", CATALOG, (0, -0.135, -0.08), (0, math.radians(-12), 0))
for _x, _z, _w, _h in ((0, 0.13, 1.05, 0.02), (0, -0.13, 1.05, 0.02), (-0.52, 0, 0.02, 0.28), (0.52, 0, 0.02, 0.28)):
    box(f"stb{_x}{_z}", (_w, 0.006, _h), (_x, 0, _z), emit("red", 1.0), STAMP_BOX)

for _o in [STAMP] + list(STAMP_BOX.children):
    _o.visible_shadow = False
MOLD = empty("MOLD", None, (-3.6, -0.6, 0))
box("mold_b", (0.75, 0.8, 0.6), (0, 0, 0.3), mat("#2b2e2b"), MOLD, 0.02, 0.014)
box("mold_mouth", (0.62, 0.02, 0.3), (0.0, -0.41, 0.3), mat("black"), MOLD)
MOLD_BUMPS = [bumper_mesh(f"MB{k}", "#5d718a", None, (0, 0, 0), s=0.6, seams=False) for k in range(4)]

EXTRA = [BOARD, DRAW, PRINTER, SHELF, BENCH_BUMP, GLUE, KNIFE, SANDER, CAN, SCALE_G, SC_BUMP, CURB, CRACK, STOREBOX, CATALOG,
         MOLD] + SPOOLS + MOLD_BUMPS

# Pip "dusted" after the sanding cloud: per-object material swap (slot 0), eyes/tag faces untouched (Ep 0 method)
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
    return toon(_hexmul(base, 0.85, 0.55), float(mt.group(2)), bool(int(mt.group(3))))


_PIP_DUST = {n: _dusted(m) for n, m in _PIP_ORIG.items()}
DUST_T0, DUST_T1 = W(5, 3) + 0.25, LN[6]["t1"] + 0.9


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
    pip_dust(DUST_T0 <= CUR_T < DUST_T1)
    PIP.root.scale = (1, 1, 1)
    clock_on_board()
    for ob in (DRAW, GLUE, KNIFE, SANDER, CAN):
        ob.parent = None
        ob.scale = (1, 1, 1)
    DRAW.scale = (DRAW_S,) * 3
    BOARD.location = (BOARD_XY[0], BOARD_XY[1], 0)
    RECEIPT.location = (0, 0, 0)
    RECEIPT.rotation_euler = (0, 0, 0)


def cloud(t, t0, center, n=14, size=0.22, seed=4, life_s=1.0, key="#e3e5e2"):
    rng = random.Random(seed)
    for i in range(n):
        d = rng.uniform(0, 0.25)
        a = (t - t0 - d) / 0.25
        if a <= 0:
            continue
        life = eout(a) * (1 - ease((t - t0 - life_s - d) / 0.5))
        if life < 0.02:
            continue
        o = Vector((rng.uniform(-1, 1) * size, rng.uniform(-0.6, 0.6) * size, rng.uniform(-0.4, 1) * size))
        rr = size * rng.uniform(0.35, 0.6) * (0.4 + 0.8 * eout(a))
        temp(blob(f"cl{i}", (rr, rr, rr * 0.9), Vector(center) + o + Vector((0, 0, 0.2 * cl(a / 6))),
                  mat(key, alpha=life, hl=True), None, seg=16, rings=10))


# ----------------------------------------------------------------------------------------------------------------- staging
G_HOME = (-0.48, -2.0, 0)     # Gus left of the board, Pip right
P_HOME = (0.72, -2.2, 0)
CAM_2S = ((0.12, -5.9, 1.35), (0.12, -1.6, 1.3), 30)


def board_on(t, extra=0.0):
    set_vis(BOARD, True)
    return bill(t, extra)


def hold_drawing(k_up=1.0, side="L"):
    """Pip holds his drawing up with one floating hand (face to camera)."""
    bpy.context.view_layer.update()
    hp = PIP.hands[side].matrix_world.translation
    DRAW.parent = None
    DRAW.location = hp + Vector((-0.26, -0.34, -0.2 + 0.04 * k_up))   # v2: held in front of his chest, clear of his head
    DRAW.rotation_euler = (math.radians(-8), math.radians(-6), math.radians(8))
    DRAW.scale = (DRAW_S,) * 3
    set_vis(DRAW, True)


def anim_E01(fr):
    """'Can I 3D print whatever bumper I want?' - Pip bounces in from the right with his crayon dream-bumper drawing."""
    t, u = fr / FPS, prog(fr, "E01")
    board_on(0.0)
    k_in = eback((t - 0.0) / 0.6, 1.6)
    hop = 0.08 * abs(math.sin(math.pi * (t - 0.1) * 2.6)) if t < LN[1]["t1"] else 0.0
    up = win(t, W(1, 3), 60, 0.25, 0.2)
    pip_pose(t, (lerp(1.9, P_HOME[0], k_in), P_HOME[1], 0), -18, look_=(-0.5, 0.6), hop=hop,
             armL=(lerp(-60, -150, up), 0, 14), elbowL=-20, armR=(-30, 0, -14), elbowR=-30)
    hold_drawing(up)
    turn = ease((t - 0.6) / 0.6)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=G_HOME, rz=lerp(0, 24, turn), head=(4, 0, -10 * turn), lid=glid, look=(lerp(0, 0.7, turn), -0.3),
         armL=(4, 0, 6), armR=(4, 0, -6))
    cam_push(*CAM_2S[:2], CAM_2S[2], 0.06 * ease(u))


def anim_E02(fr):
    """'Sure. Scan the car. Design it.' - each step lands on the bill as a picture: spray can + scanner on 'Scan the car',
    laptop on 'Design'. Push in on the board."""
    t, u = fr / FPS, prog(fr, "E02")
    board_on(t)
    pt = win(t, W(2, 1) - 0.1, LN[2]["t1"], 0.2, 0.3)
    gus_pose(t, G_HOME, 22, look_=(0.6, 0.6), head=(-8, 0, -6), armR=(lerp(4, -120, pt), 0, lerp(-6, -40, pt)), elbowR=-10)
    pip_pose(t, P_HOME, -22, look_=(-0.6, 0.8), head=(-14, 0, 6), armL=(-150, 0, 14), elbowL=-20)
    hold_drawing()
    cam_push((0.12, -5.0, 1.75), (0.0, -1.4, 1.75), 32, 0.25 * ease(u))


def anim_E03(fr):
    """'Six or seven kilos of filament. The good stuff's about two hundred bucks.' - spools drop into a stack taller than
    Pip; 6-7 KG and ~$200 land on the bill."""
    t, u = fr / FPS, prog(fr, "E03")
    board_on(t)
    t0 = W(3, 0) - 0.1
    for k, sp in enumerate(SPOOLS[:7]):
        ta = t0 + 0.16 * k
        if t < ta:
            continue
        set_vis(sp, True)
        row, col = divmod(k, 2) if k < 6 else (3, 0.5)
        z_rest = 0.15 + 0.3 * row
        z = z_rest + 2.0 * (1 - eout((t - ta) / 0.3))
        sq = 1 - 0.15 * math.sin(math.pi * cl((t - ta - 0.3) / 0.12))
        sp.location = (1.5 + 0.17 * (col - 0.5), -2.3, z)
        sp.scale = (1, 1, sq)
        sp.rotation_euler = (0, 0, 0)
    gus_pose(t, G_HOME, 20, look_=(0.7, 0.2), armL=(-30, 0, 12), elbowL=-70)
    surpr = win(t, W(3, 9), W(3, 9) + 0.8, 0.06, 0.3)
    pip_pose(t, P_HOME, lerp(-10, 30, ease((t - t0) / 0.6)), look_=(0.5, lerp(0.9, 0.2, surpr)), hop=0.05 * surpr,
             head=(-18, 0, 0), armL=(-60, 0, 14), elbowL=-30)
    hold_drawing(0.3)
    cam_push((0.55, -6.2, 1.4), (0.55, -1.7, 1.2), 30, 0.05 * ease(u))


def anim_E04(fr):
    """'A print fails overnight. Again.' - the printer at the bench; the head runs, the print bursts into spaghetti; on
    'Again.' a second blob. The failed-print shelf above is already full."""
    t, u = fr / FPS, prog(fr, "E04")
    set_vis(PRINTER, True)
    set_vis(SHELF, True)
    set_vis(LAPTOP, False)
    set_vis(UI, False)
    PR_HEAD.location = (0.2 * math.sin(t * 9), 0.12 * math.sin(t * 6.3), 0)
    PR_GANTRY.location = (0, 0, 0.32 + 0.02 * math.sin(t * 2))
    tf = W(4, 2)
    if t >= tf - 0.15:
        k = eout((t - tf + 0.15) / 0.5)   # v2: the nest grows out of the stalled part (no scale pop)
        temp(spaghetti("spag_a", PRINTER, (0, 0, 0.11), s=1.25, seed=5, frac=0.15 + 0.85 * k))
    ta = W(4, 4)
    if t >= ta - 0.1:
        k = eout((t - ta + 0.1) / 0.4)
        temp(spaghetti("spag_b", PRINTER, (0.06, -0.03, 0.2), s=1.0, seed=9, key="white", frac=0.1 + 0.9 * k, base=False))
    cam_push((3.0, 1.15, 1.75), (3.15, 3.15, 1.35), 30, 0.12 * ease(u))


def anim_E05(fr):
    """'Then glue. Filler. Sanding. Primer.' - one beat per word on the printed bumper at the bench: glue bottle squeezes
    along the seams, the filler knife swipes, a sanding cloud (Pip pops into it), the primer can turns it grey."""
    t, u = fr / FPS, prog(fr, "E05")
    set_vis(LAPTOP, False)
    set_vis(UI, False)
    set_vis(SHELF, True)
    set_vis(BENCH_BUMP, True)
    tg, tf, ts, tp = W(5, 1), W(5, 2), W(5, 3), W(5, 4)
    bx, by, bz = 3.55, 3.12, 0.96
    primed = t >= tp + 0.15
    for o in BENCH_BUMP.children:
        if o.name.startswith("BENCH_BUMP_m") and o.data.materials:
            o.data.materials[0] = mat(PRIMED_KEY if primed else "sage_l", hl=True)
    if tg - 0.2 <= t < tf:
        set_vis(GLUE, True)
        k = (t - tg) / max(0.3, tf - tg)
        GLUE.location = (bx - 0.35 + 0.7 * cl(k), by - 0.18, bz + 0.25)
        GLUE.rotation_euler = (math.radians(150), 0, 0)
    if tf - 0.1 <= t < ts:
        set_vis(KNIFE, True)
        k = ease((t - tf) / 0.45)
        KNIFE.location = (bx - 0.3 + 0.6 * k, by - 0.22, bz + 0.22)
        KNIFE.rotation_euler = (math.radians(-25), 0, 0)
    if ts - 0.1 <= t < tp:
        set_vis(SANDER, True)
        SANDER.location = (bx + 0.18 * math.sin(t * 30), by - 0.2, bz + 0.18)
    if t >= ts:
        cloud(t, ts, (bx + 0.25, by - 0.35, bz + 0.05), n=10, size=0.16, seed=6, life_s=max(0.5, tp - ts + 0.2), key="#d9dbd8")
        # Pip pops into the cloud from the right and vanishes in it
        k = eback((t - ts - 0.05) / 0.35, 1.6)
        if t < tp:
            pose(PIP, loc=(bx + lerp(1.0, 0.55, k), by - 0.35, 0), rz=-50, look=(-0.7, 0.4), armL=(-60, 0, 10))
    if t >= tp - 0.1:
        set_vis(CAN, True)
        k = ease((t - tp + 0.1) / 0.6)
        CAN.location = (bx + 0.45 - 0.9 * k, by - 0.5, bz + 0.45)
        CAN.rotation_euler = (math.radians(-35), 0, 0)
        if t >= tp:
            for i in range(8):
                a = ((t - tp) * 3 + i / 8) % 1.0
                p = CAN.location + Vector((0.03 * math.sin(i), 0.15 + 0.35 * a, -0.15 * a))
                temp(blob(f"mist{i}", (0.03 + 0.05 * a,) * 3, p, mat("#9a9e9a", alpha=1 - a, hl=True), None, seg=10, rings=6))
    cam_push((bx - 0.05, 1.05, 1.6), (bx, by, 1.05), 30, 0.08 * ease(u))


def anim_E06(fr):
    """'Is it done yet?' - Pip, dusted grey, pops out of the settling cloud."""
    t, u = fr / FPS, prog(fr, "E06")
    board_on(t)
    imp = win(t, LN[6]["t0"], LN[6]["t1"], 0.1, 0.3)
    pip_pose(t, P_HOME, -20, look_=(-0.6, 0.5), hop=0.05 * abs(math.sin(math.pi * (t - LN[6]["t0"]) * 4)) * imp,
             armL=(-40 - 20 * imp, 0, 14), elbowL=-50, armR=(-40 - 20 * imp, 0, -14), elbowR=-50)
    for i in range(8):
        a = (t * 0.5 + i / 8) % 1.0
        temp(blob(f"dust{i}", (0.02, 0.02, 0.02), (P_HOME[0] + 0.25 * math.sin(i * 2.1), P_HOME[1] - 0.1, 0.5 + 0.7 * a),
                  mat("#d9dbd8", alpha=1 - a, hl=True), None, seg=8, rings=6))
    gm, glid = talk("GUS", t)
    pose(GUS, loc=G_HOME, rz=24, look=(0.7, -0.3), lid=glid)
    cam_push((0.85, -4.1, 1.05), (0.72, -2.2, 0.9), 34, 0.1 * ease(u))


def anim_E07(fr):
    """'...No. That's easily two hundred fifty hours of work.' - the clock on the board spins faster and faster and drops
    off on 'hours'; ~250 HRS lands on the bill."""
    t, u = fr / FPS, prog(fr, "E07")
    board_on(t)
    t0 = SF["E07"][0] / FPS
    th = W(7, 4)
    spin = 360 * 2.2 * max(0.0, t - t0) ** 2
    fall = cl((t - th - 0.1) / 0.45)
    clock_on_board(spin, fall)
    if fall >= 1.0:
        set_vis(CLOCK, False)
    gus_pose(t, G_HOME, 18, look_=(0.5, 0.7), head=(-10, 0, -4), armR=(-60, 0, -20), elbowR=-40)
    pip_pose(t, P_HOME, -20, look_=(-0.4, 0.9), head=(-16, 0, 4))
    # v1.1: after the clock drops, tilt down the bill so ~250 HRS (bottom slot) is on screen when it lands
    kt = ease(cl((t - th) / 0.6))
    cam_push((0.12, -4.6, lerp(2.2, 1.45, kt)), (0.12, -1.3, lerp(2.05, 0.72, kt)), 34, 0.12 * ease(u))


def anim_E08(fr):
    """'And it's still heavier. And weaker.' - the finished bumper thumps onto a floor scale (needle swings hard);
    on 'weaker' a curb taps it and it cracks along a glue seam."""
    t, u = fr / FPS, prog(fr, "E08")
    set_vis(SCALE_G, True)
    set_vis(SC_BUMP, True)
    th, tw = W(8, 3), W(8, 5)
    k = eout((t - th + 0.35) / 0.35)
    SC_BUMP.location = (0.05, -2.12, lerp(1.2, 0.093, k))
    sag = 0.02 * math.sin(math.pi * cl((t - th) / 0.2))
    SC_BUMP.location.z -= sag
    needle = 110 * eback((t - th) / 0.35, 2.0) if t >= th else -110
    SC_NEEDLE.rotation_euler = (0, math.radians(-110 + needle * 1.85 + 4 * math.sin(t * 20) * win(t, th, th + 0.6)), 0)
    if t >= tw - 0.35:
        set_vis(CURB, True)
        kc = eout((t - tw + 0.35) / 0.3)
        CURB.location = (lerp(1.4, 0.58, kc), -2.2, 0.08)
    if t >= tw:
        set_vis(CRACK, True)
        CRACK.location = (0.08, -2.2, 0.1)
        for i in range(5):
            a = (t - tw) / 0.6
            if a < 1:
                temp(box(f"chip{i}", (0.03, 0.02, 0.025), (0.12 + 0.1 * a * math.cos(i), -2.3 - 0.15 * a, 0.25 + 0.2 * a - 0.5 * a * a),
                         mat(PRIMED_KEY), None, ol=0.004, rot=(i * 40 * a, i * 20, 0)))
    gm, glid = talk("GUS", t)
    gus_pose(t, (-0.55, -1.75, 0), 30, look_=(0.6, -0.6), head=(10, 0, -10))
    cam_push((0.25, -4.6, 1.05), (0.0, -2.0, 0.6), 30, 0.08 * ease(u))


def anim_E09(fr):
    """'...So I should just buy one?' - the bill now runs to the floor and curls up; Pip deflates in front of it."""
    t, u = fr / FPS, prog(fr, "E09")
    t0 = SF["E09"][0] / FPS
    k = ease((t - t0) / 0.9)
    board_on(t, extra=k * 2.0)
    receipt_curl(k)
    set_vis(CLOCK, False)
    pip_pose(t, P_HOME, -8, look_=(-0.4, 0.5), hips=(6, 0, 0), head=(10, 0, 4), armL=(10, 0, 8), armR=(10, 0, -8))
    PIP.root.scale = (1.04, 1.04, 0.95)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=G_HOME, rz=24, look=(0.7, -0.2), lid=glid)
    cam_push((0.4, -5.6, 0.95), (0.3, -1.6, 1.2), 28, 0.1 * ease(u))


def anim_E10(fr):
    """'If you can buy it? Yep. Printing a rep doesn't make financial sense...' (store box next to the floor-long bill)
    '...unless it's discontinued,' (DISCONTINUED stamp on a catalog page) 'or you're making them to sell.' (a mold drops
    out identical bumpers in a row)."""
    t, u = fr / FPS, prog(fr, "E10")
    td, ts = W(10, 13) - 0.15, W(10, 16) - 0.1     # "Unless" / "or" cuts
    if t < td:
        board_on(t, extra=2.0)
        receipt_curl(1.0)
        set_vis(CLOCK, False)
        set_vis(STOREBOX, True)
        kb = eback((t - W(10, 0)) / 0.35, 1.6)
        STOREBOX.location = (1.1, -1.75, 0.6 * (1 - kb))
        STOREBOX.rotation_euler = (0, 0, math.radians(-18))
        STOREBOX.scale = (kb, kb, kb)
        pt = win(t, W(10, 6), td, 0.25, 0.1)
        gus_pose(t, G_HOME, 20, look_=(0.6, 0.1), armR=(lerp(4, -80, pt), 0, lerp(-6, -30, pt)), elbowR=-20)
        pip_pose(t, (0.62, -2.45, 0), -30, look_=(-0.7, 0.6), head=(-10, 0, 0))
        cam_push((0.35, -6.0, 1.25), (0.35, -1.7, 1.0), 30, 0.08 * ease((t - SF["E10"][0] / FPS) / (td - SF["E10"][0] / FPS)))
    elif t < ts:
        set_vis(CATALOG, True)
        ks = cl((t - W(10, 15)) / 0.18)    # stamp lands on "discontinued"
        set_vis(STAMP, ks > 0)
        set_vis(STAMP_BOX, ks > 0)
        s = lerp(1.8, 1.0, eout(ks))
        STAMP.scale = (s, s, s)
        STAMP_BOX.scale = (s, s, s)
        shake = 0.01 * math.sin(t * 60) * (1 - cl((t - W(10, 15) - 0.18) / 0.25)) * (ks >= 1)
        k = (t - td) / max(0.2, ts - td)
        look(cam, (-3.1 + shake, 1.0 + 0.2 * ease(k), 1.55), (-3.1, 3.5, 1.5), 34)
    else:
        set_vis(MOLD, True)
        for k, b in enumerate(MOLD_BUMPS):
            ta = ts + 0.18 + 0.32 * k
            if t < ta:
                continue
            set_vis(b, True)
            kk = eout((t - ta) / 0.35)
            zr = 0.27 * k   # v2: 350Z bumper is taller
            b.location = (lerp(-3.6, -2.75, kk), -1.05, zr + 0.6 * (1 - kk) * (kk < 1))
        look(cam, (-3.05, -3.6, 1.15), (-3.1, -0.85, 0.5), 30)


def anim_E11(fr):
    """'But I want a custom one!' - Pip slaps his drawing onto the bill."""
    t, u = fr / FPS, prog(fr, "E11")
    board_on(t, extra=2.0)
    receipt_curl(1.0)
    set_vis(CLOCK, False)
    tsl = W(11, 4)
    k = ease((t - LN[11]["t0"]) / max(0.2, tsl - LN[11]["t0"]))
    if t < tsl:
        pip_pose(t, lerpv(P_HOME, (0.42, -1.65, 0), k), lerp(-20, 30, k), look_=(-0.4, 0.8), hop=0.06 * k,
                 armL=(-150, 0, 14), elbowL=-20)
        hold_drawing()
    else:
        pip_pose(t, (0.42, -1.65, 0), 20, look_=(-0.2, 0.3), armL=(-90, 0, 30), elbowL=-30)
        set_vis(DRAW, True)
        DRAW.parent = BOARD
        DRAW.location = (0.05, -0.08, 0.95)
        DRAW.rotation_euler = (0, math.radians(4), 0)
        sq = 1 + 0.15 * math.sin(math.pi * cl((t - tsl) / 0.15))
        DRAW.scale = (sq * DRAW_S / BOARD_S, DRAW_S / BOARD_S, sq * DRAW_S / BOARD_S)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=G_HOME, rz=24, look=(0.7, 0.0), lid=glid)
    cam_push((0.2, -5.2, 1.4), (0.2, -1.6, 1.25), 30, 0.08 * ease(u))


def anim_E12(fr):
    """'...If you insist. We'll show you how.' - Gus turns from Pip to the camera (to the audience), tiny shrug."""
    t, u = fr / FPS, prog(fr, "E12")
    board_on(t, extra=2.0)
    receipt_curl(1.0)
    set_vis(CLOCK, False)
    set_vis(DRAW, True)
    DRAW.parent = BOARD
    DRAW.location = (0.05, -0.08, 0.95)
    DRAW.rotation_euler = (0, math.radians(4), 0)
    DRAW.scale = (DRAW_S / BOARD_S,) * 3
    kt = ease((t - W(12, 2) + 0.2) / 0.5)
    shrug = win(t, W(12, 0), WE(12, 2), 0.15, 0.3)
    gus_pose(t, (-0.35, -2.3, 0), lerp(30, 0, kt), look_=(lerp(0.7, 0.0, kt), lerp(-0.3, -0.05, kt)),
             armL=(4 - 30 * shrug, 0, 6 + 20 * shrug), armR=(4 - 30 * shrug, 0, -6 - 20 * shrug), elbowL=-40 * shrug,
             elbowR=-40 * shrug, head=(0, 0, 8 * shrug))
    pip_pose(t, (0.6, -1.95, 0), -30, look_=(-0.6, 0.6), head=(-12, 0, 0))
    cam_push((-0.3, -4.6, 1.42), (-0.35, -2.3, 1.3), 38, 0.1 * ease(u))


def anim_E13(fr):
    """'Where do we start?' - Pip, thrilled, wipes the whiteboard clean with one sweep."""
    t, u = fr / FPS, prog(fr, "E13")
    set_vis(BOARD, True)
    tr = W(13, 0) + 0.1
    k = eout((t - tr) / 0.5)
    bill(t)
    for j, ic in enumerate(ICONS):   # v2: his sweep wipes the board clean, top row first
        kw = cl((k - 0.05 * j) / 0.25)
        if kw > 0:
            ic["g"].scale = (1.25 * (1 - kw),) * 3
            if ic["lab"]:
                ic["lab"].scale = ((1 - kw),) * 3
            if kw >= 1:
                set_vis(ic["g"], False)
                if ic["lab"]:
                    set_vis(ic["lab"], False)
    set_vis(CLOCK, False)
    pip_pose(t, (0.42, -1.75, 0), lerp(20, -10, k), look_=(0.3, 0.6), hop=0.1 * abs(math.sin(math.pi * k)),
             armL=(lerp(-150, -60, k), 0, lerp(14, 60, k)), elbowL=-20)
    gm, glid = talk("GUS", t)
    pose(GUS, loc=(-0.48, -2.1, 0), rz=24, look=(0.7, 0.2), lid=glid)
    cam_push((0.2, -5.4, 1.5), (0.2, -1.6, 1.35), 30, 0.06 * ease(u))


def anim_E14(fr):
    """'We scan the car.' - Gus picks up the scanner and turns to the car; Pip hops after him. Hard cut on the beat."""
    t, u = fr / FPS, prog(fr, "E14")
    set_vis(BOARD, True)
    for ic in ICONS:
        set_vis(ic["g"], False)
        if ic["lab"]:
            set_vis(ic["lab"], False)
    set_vis(CLOCK, False)
    BOARD.location = (1.5, -1.0, 0)   # rolled aside
    k = ease((t - LN[14]["t0"] + 0.1) / 0.8)
    attach(SCANNER, GUS.hands["R"], (0, -0.04, 0.05), (0, 0, 0))
    gus_pose(t, (-0.3, lerp(-2.2, -2.0, k), 0), lerp(0, 160, k), look_=(0.0, 0.2), armR=(-70, 0, -10), elbowR=-30)
    pip_pose(t, (0.45, lerp(-2.45, -2.3, k), 0), lerp(-20, 170, k), look_=(0, 0.4), hop=0.08 * abs(math.sin(t * 9)))
    cam_push((0.1, -4.9, 1.35), (0.0, 0.0, 0.85), 30, 0.15 * ease(u))


ANIM = {s: globals()[f"anim_{s}"] for s in SF}

# ----------------------------------------------------------------------------------------------------------------- run
for sh in EP_SHOTS:
    f0, f1 = SF[sh]
    d = os.path.join(OUT, sh)
    os.makedirs(d, exist_ok=True)
    tsum, nr = 0.0, 0
    for fr in range(f0, f1):
        final = os.path.join(d, f"{fr:04d}.png")
        todo = (fr - f0) % EVERY == 0 and not os.path.exists(final) and (not ONLY or fr in ONLY)
        if not todo:
            continue
        CUR_T = fr / FPS
        reset_anim()
        ANIM[sh](fr)
        bpy.context.view_layer.update()
        if os.environ.get("EP1_DEBUG"):   # print world bounds of named objects instead of rendering
            for nm in os.environ["EP1_DEBUG"].split(","):
                o = bpy.data.objects[nm]
                ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
                print(f"[dbg] {fr} {nm} z {min(v.z for v in ws):.2f}..{max(v.z for v in ws):.2f} "
                      f"x {min(v.x for v in ws):.2f}..{max(v.x for v in ws):.2f} vis {not o.hide_render}", flush=True)
            continue
        scn.render.filepath = os.path.join(d, f"{fr:04d}_tmp")
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        os.replace(os.path.join(d, f"{fr:04d}_tmp.png"), final)
        tsum += time.time() - t0
        nr += 1
        print(f"[ep1] {sh} {fr} {time.time() - t0:.1f} s", flush=True)
    if nr:
        print(f"[ep1] {sh} done: {nr} frames, {tsum / nr:.1f} s/frame", flush=True)
