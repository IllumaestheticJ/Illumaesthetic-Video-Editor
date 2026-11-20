"""All 14 shots of the DITL GR Corolla short. blender -b --python gr_shots.py -- <shot 1-14> <outdir> [f1,f2,..|anim] [res] [samples] [start]
Built on the WRX kit (shots.py: hands, people, rooms, road, keying helpers) and cars.py."""
import bpy, sys, math, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots as W, cars as C
from shots import mat, imgmat, procmat, box, plane, R, TEX, key, vis, swap, lookrot, rigcam, shake, hand, person, arm, alphamat, texmat, OPEN, FIST, POINT, FLAT
from mathutils import Vector
k = W.k
NF = [65, 48, 47, 95, 47, 48, 47, 47, 95, 48, 47, 48, 95, 213]
WHITE = (0.62, 0.02, 0.025)   # his car: red (owner, 2026-11-19); the name is kept from the first build
_SK = {}
def _skin():   # light skin on the POV hands (owner: "skin tone doesn't matter maybe white")
    if "s" not in _SK: _SK["s"] = W.skinmat("skin_him", (0.74, 0.52, 0.4), (0.82, 0.6, 0.47)); _SK["n"] = W._flat_mat("nail", (0.86, 0.7, 0.64), 0.3); _SK["p"] = W._flat_mat("palmskin", (0.85, 0.62, 0.52), 0.55)
    return _SK
W.S = _skin

def empty(name, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.location = loc; e.rotation_euler = rot; e.parent = parent; return e

def cap(name, head, col=(0.015, 0.015, 0.018)):
    m = W._flat_mat(name + "_cap", col); box(name + "_capc", (0.25, 0.26, 0.09), m, loc=(0, 0.005, 0.25), parent=head, base="z", taper=0.85)
    box(name + "_brim", (0.2, 0.16, 0.018), m, loc=(0, -0.18, 0.262), parent=head); box(name + "_capl", (0.07, 0.004, 0.04), W._flat_mat(name + "_capr", (0.8, 0.05, 0.06)), loc=(0, -0.118, 0.305), parent=head)

def guy(name, who, loc, rz, faces, skin, shirt, hat=True, hair=(0.05, 0.04, 0.03), **kw):
    sk = mat(name + "_skin", skin, 0.7); p, head, fd = person(name, who, loc, rz, sk, mat("polo_" + name, shirt), mat(name + "_hair", hair), faces, hair_h=0.04 if hat else 0.1, **kw)
    if hat: cap(name, head)
    return p, head, fd, sk

def lamp(parent, loc, energy=8, size=0.4):
    l = bpy.data.objects.new("lamp", bpy.data.lights.new("lamp", "POINT")); l.data.energy = energy; l.data.shadow_soft_size = size; bpy.context.scene.collection.objects.link(l); l.parent = parent; l.location = loc; return l

def aim(h, f, tgt, sh, reach=0.2, interp="LINEAR", roll=0.0):
    """Key hand h (in its parent's space, parent unrotated) so the fingertips sit on tgt and the forearm runs back toward the shoulder point sh."""
    d = (Vector(tgt) - Vector(sh)).normalized(); e = d.to_track_quat("Y", "Z").to_euler(); e.rotate_axis("Y", roll)
    key(h, f, loc=tuple(Vector(tgt) - d * reach), rot=tuple(e), interp=interp)

# ---------------- 1: phone, "which one should I buy?" ----------------
def s1():
    rig, cam = rigcam((0, 0, 1.0), (0, 1.0, 0.47), lens=22); W.bunk(cam)
    names = ["tr", "sw1_0", "sw1_1", "wrx", "sw2_0", "sw2_1", "grc", "liked", "typed0", "typed1", "typed2"]
    ph, d = W.phone(cam, names); sw = [(1, "tr"), (15, "sw1_0"), (17, "sw1_1"), (19, "wrx"), (33, "sw2_0"), (35, "sw2_1"), (37, "grc"), (53, "liked"), (57, "typed0"), (60, "typed1"), (63, "typed2")]; swap(d, sw)
    hand("hL", cam, (-0.035, -0.17, -0.185), (R(-6), R(180), R(4)), curls=FLAT, thumb=0.2)
    rest = (0.105, -0.26, -0.095); h = hand("hR", cam, rest, (R(-8), R(4), R(12)), curls=POINT, thumb=0.9)
    for f in (15, 33):   # press right of centre, drag left, lift
        key(h, f - 5, loc=rest, interp="LINEAR"); key(h, f - 2, loc=(0.1, -0.225, -0.096), interp="LINEAR"); key(h, f + 2, loc=(0.068, -0.225, -0.096), interp="LINEAR"); key(h, f + 6, loc=rest, interp="LINEAR")
    like = (0.045, -0.262, -0.093); key(h, 46, loc=rest, interp="LINEAR"); key(h, 50, loc=(0.07, -0.3, -0.06), interp="LINEAR"); key(h, 53, loc=like, interp="LINEAR"); key(h, 56, loc=(0.09, -0.3, -0.08), interp="LINEAR")
    for f in (57, 60, 63): key(h, f - 1, loc=(0.085, -0.292, -0.085), interp="LINEAR"); key(h, f, loc=(0.07, -0.275, -0.093), interp="LINEAR")
    P0 = (-0.012, 0.012, -0.135); key(ph, 52, loc=P0, rot=(R(-6), R(3), R(4)), interp="LINEAR"); key(ph, 53, loc=(-0.012, 0.0, -0.15), rot=(R(-12), R(3), R(-3)), interp="LINEAR"); key(ph, 57, loc=P0, rot=(R(-6), R(3), R(4)), interp="LINEAR")
    cam.data.lens = 22; cam.data.keyframe_insert("lens", frame=1); cam.data.lens = 26; cam.data.keyframe_insert("lens", frame=65)

# ---------------- 2-3: the dealer ----------------
def dealer(faces):
    W.room((0.8, 0.8, 0.82), (0.3, 0.3, 0.33)); wood = procmat("wood", "noise", (0.22, 0.12, 0.06), (0.33, 0.19, 0.09), 6); box("desk", (1.8, 0.9, 0.78), wood, (0, 0.1, 0), base="z")
    plane("sign_t", 1.4, 0.36, imgmat("signtm", TEX + "sign_toyota.png"), (-1.9, 2.94, 2.35), rot=(R(90), 0, 0)); plane("sign_n", 2.3, 0.44, imgmat("signnm", TEX + "sign_notest.png"), (1.3, 2.94, 2.0), rot=(R(90), 0, 0))
    dk = empty("deskspace", (0, 0.02, 0.783), (0, 0, R(-4)))
    sh = {i: plane(f"sheet{i}", 0.3, 0.4, imgmat(f"sheetm{i}", f"{TEX}sheet{i}.png"), (0, 0, i * 0.0004), parent=dk) for i in range(4)}
    p, head, fd, sk = guy("sales", "sales", (0, 0.95, 0.45), 0, faces, (0.8, 0.6, 0.48), (0.75, 0.1, 0.1), hat=False, hair=(0.3, 0.2, 0.08)); p.rotation_euler = (R(-24), 0, 0)
    return dk, sh, p, head, fd, sk

def pen_at(h, f, tgt, jit=0.0, rnd=None, lift=0.0):
    """Hand root so the pen tip sits on desk-space point tgt (x, y on the sheet)."""
    j = (rnd.uniform(-jit, jit), rnd.uniform(-jit, jit)) if rnd else (0, 0)
    key(h, f, loc=(tgt[0] + 0.012 + j[0], tgt[1] - 0.12 + j[1], 0.125 + lift), interp="LINEAR")

def s2():
    dk, sh, p, head, fd, sk = dealer(["flat", "grin", "proud"]); swap(sh, [(1, 0), (11, 1), (24, 2)]); swap(fd, [(1, "flat"), (24, "grin"), (42, "proud")])
    L0 = (0, -0.42, 1.42); fl = (0.0, 0.0, 0.783); ll = (0, 0.8, 1.2); rig, cam = rigcam(L0, fl, lens=40)
    key(rig, 1, rot=lookrot(L0, fl, -3), interp="LINEAR"); key(rig, 37, rot=lookrot(L0, fl, -1), interp="LINEAR"); key(rig, 42, rot=lookrot(L0, ll), interp="LINEAR")
    for f, ln in ((1, 38), (23, 42), (24, 37), (37, 40), (42, 38)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    h = hand("hR", dk, (0, 0, 0.2), (R(-22), 0, R(14)), curls=FIST, thumb=0.9, hold="pen"); rnd = random.Random(5); GRP = (-0.101, 0.087)
    pen_at(h, 1, (0.1, -0.2), lift=0.1)
    for f in range(3, 12): pen_at(h, f, GRP, 0.03, rnd)
    for f in range(14, 40, 3): pen_at(h, f, (0.24, -0.2), 0.02, rnd, lift=0.05)   # off the paper, pen still twitching
    hl = hand("hL", dk, (-0.22, -0.16, 0.03), (R(-4), 0, R(-20)), curls=FLAT, mirror=True)
    # the salesman's stamp: arm + block come down on the sheet at 30
    st = empty("stamp", (0.2, 0.5, 0.5), parent=dk); st.scale = (0.7, 0.7, 0.7); rm = W._flat_mat("stampm", (0.6, 0.05, 0.05)); box("st_blk", (0.2, 0.07, 0.05), rm, (0, 0, 0.025), parent=st); box("st_hdl", (0.05, 0.05, 0.09), W._flat_mat("sth", (0.2, 0.12, 0.06)), (0, 0, 0.09), parent=st)
    box("st_hand", (0.1, 0.1, 0.07), sk, (0, 0.03, 0.14), parent=st); box("st_arm", (0.09, 0.75, 0.09), mat("polo_st", (0.75, 0.1, 0.1)), (0, 0.08, 0.14), rot=(R(22), 0, 0), parent=st, base="y")
    SP = (-0.05, -0.105, 0.0); key(st, 1, loc=(0.25, 0.6, 0.5), interp="LINEAR"); key(st, 19, loc=(0.1, 0.25, 0.4), interp="LINEAR"); key(st, 24, loc=SP, interp="LINEAR"); key(st, 26, loc=SP, interp="LINEAR"); key(st, 31, loc=(0.3, 0.45, 0.3), interp="LINEAR")
    key(cam, 23, rot=(0, 0, 0), interp="LINEAR"); key(cam, 24, rot=(R(-2.5), R(1), R(2)), interp="LINEAR"); key(cam, 28, rot=(0, 0, 0), interp="LINEAR")
    for f, rz in ((1, 0), (24, 6), (40, -6), (44, 6)): key(head, f, rot=(R(-16), 0, R(rz)), interp="CONSTANT")

def s3():
    dk, sh, p, head, fd, sk = dealer(["grin", "proud", "horror"]); swap(sh, [(1, 2), (14, 3)]); swap(fd, [(1, "grin"), (16, "proud"), (28, "horror")])
    L0 = (0, -0.45, 1.27); rig, cam = rigcam(L0, (0, 0.3, 0.95), lens=17)
    for f, ln in ((1, 17), (27, 17), (30, 19), (47, 22)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    rnd = random.Random(7); hr = hand("hR", dk, (0, 0, 0.2), (R(-22), 0, R(14)), curls=FIST, thumb=0.9, hold="pen"); hl = hand("hL", dk, (0, 0, 0.2), (R(-22), 0, R(-14)), curls=FIST, thumb=0.9, hold="pen", mirror=True)
    for f in range(1, 48, 2):
        u = (f % 24) / 24; pen_at(hr, f, (0.04 + 0.09 * u, -0.168), 0.01, rnd); pen_at(hl, f, (-0.2 + 0.08 * u, -0.19), 0.01, rnd)
    for f, rz in ((1, -4), (16, 5), (28, -8), (34, 6), (40, -6), (46, 5)): key(head, f, rot=(R(-12 if f < 28 else -4), 0, R(rz)), interp="CONSTANT")
    shake(cam, 28, 47, 0.5, seed=3)

# ---------------- 4: unboxing, the full kit gets thrown on ----------------
def s4():
    k.world(); k.lot_set(); card = mat("card", (0.55, 0.4, 0.24)); rnd = random.Random(4)
    for i in range(5): box(f"bx{i}", (rnd.uniform(.5, 1.1), rnd.uniform(.4, .9), rnd.uniform(.25, .6)), card, (rnd.uniform(1.6, 4.6), rnd.uniform(-5.2, -3.6), 0), rot=(0, 0, rnd.uniform(0, 3)), base="z")
    root, by = C.grc(kit=False); bpy.context.view_layer.update()
    cl = (4.0, -3.4, 1.7); look = (0.0, 0.2, 0.6); rig, cam = rigcam(cl, look, lens=21); dv = (Vector(look) - Vector(cl)).normalized()
    bxl = Vector(cl) + dv * 1.4; bxl.z = 0; box("bigbox", (0.95, 0.75, 0.55), card, tuple(bxl), rot=(0, 0, R(48)), base="z"); box("bigbox_in", (0.85, 0.65, 0.02), W._flat_mat("boxin", (0.05, 0.035, 0.02)), (bxl.x, bxl.y, 0.56), rot=(0, 0, R(48)))
    hold = Vector(cl) + dv * 0.8 + Vector((0, 0, -0.28)); wind = hold - dv * 0.2 + Vector((0, 0, 0.12))
    hr = hand("hR", cam, (0.16, -0.36, -0.5), (R(-70), 0, R(-10)), curls=OPEN, thumb=-0.3); hl = hand("hL", cam, (-0.16, -0.36, -0.5), (R(-70), 0, R(10)), curls=OPEN, thumb=-0.3, mirror=True)
    for i, f in enumerate(range(1, 11, 3)):
        o = 0.1 + 0.2 * (i % 2); key(hr, f, loc=(0.05 + o, -0.3 + 0.1 * (i % 2), -0.5), rot=(R(-70 + 25 * (i % 2)), 0, R(-10 - 30 * (i % 2))), interp="LINEAR"); key(hl, f, loc=(-0.05 - o, -0.3 + 0.1 * (i % 2), -0.5), rot=(R(-70 + 25 * (i % 2)), 0, R(10 + 30 * (i % 2))), interp="LINEAR")
    for i in range(12):
        p = plane(f"fl{i}", rnd.uniform(.12, .3), rnd.uniform(.1, .25), card, (0, -0.3, -0.7), parent=cam); a = rnd.uniform(0, 6.28); st = rnd.choice([2, 4, 6, 8])
        vis(p, 1, False); vis(p, st, True); key(p, st, loc=(rnd.uniform(-.1, .1), -0.32, -0.7), rot=(0, 0, 0), interp="LINEAR")
        key(p, st + 12, loc=(math.cos(a) * 0.9, 0.3 + math.sin(a) * 0.5, -rnd.uniform(0.7, 1.4)), rot=(rnd.uniform(0, 9), rnd.uniform(0, 9), rnd.uniform(0, 9)), interp="LINEAR"); vis(p, st + 13, False)
    PARTS = [(["part_front_lip_v2"], [], 0.42), (["part_canards"], [], 0.9), (["part_side_skirts_v2"], [], 0.3), (["part_rear_spats_v2"], [], 0.42), (["part_wrc_wing", "part_wing_strakes"], ["body_roof_spoiler_stock"], 0.5)]
    for i, (pns, stock, hs) in enumerate(PARTS):
        s0 = 11 + i * 16; land = s0 + 12; ms = [by[n] for n in pns]
        pts = [m.matrix_world @ Vector(c) for m in ms for c in m.bound_box]; c = sum(pts, Vector()) / len(pts)
        hd = empty("thrown_" + pns[0], c); bpy.context.view_layer.update()
        for m in ms:
            d = m.copy(); bpy.context.scene.collection.objects.link(d); d.parent = hd; d.matrix_parent_inverse = hd.matrix_world.inverted(); d.matrix_basis = m.matrix_world.copy(); d.hide_render = False
        for sn in stock: vis(by[sn], 1, True); vis(by[sn], land, False)
        spin = (6.2832 * (1 if i % 2 else -1), 6.2832, 6.2832 * (2 if i < 2 else -1)); inbox = (bxl.x, bxl.y, 0.4)
        vis(hd, 1, False); vis(hd, s0, True)
        key(hd, s0, loc=inbox, rot=spin, scale=(hs * 0.5,) * 3, interp="LINEAR"); key(hd, s0 + 5, loc=tuple(hold), rot=spin, scale=(hs,) * 3, interp="LINEAR"); key(hd, s0 + 7, loc=tuple(wind), rot=tuple(v * 0.97 for v in spin), scale=(hs,) * 3, interp="LINEAR")
        mid = (Vector(wind) + c) / 2 + Vector((0, 0, 0.9)); key(hd, s0 + 9, loc=tuple(mid), rot=tuple(v * 0.5 for v in spin), scale=((hs + 1) / 2,) * 3, interp="LINEAR")
        key(hd, land, loc=tuple(c), rot=(0, 0, 0), scale=(1.14,) * 3, interp="LINEAR"); key(hd, land + 3, loc=tuple(c), rot=(0, 0, 0), scale=(1, 1, 1), interp="LINEAR")
        for h, sx in ((hr, 1), (hl, -1)):
            key(h, s0 - 1, loc=(0.2 * sx, -0.3, -0.5), rot=(R(-60), 0, R(-20 * sx)), interp="LINEAR"); key(h, s0 + 1, loc=(0.18 * sx, -0.46, -0.6), rot=(R(-95), 0, R(-10 * sx)), interp="LINEAR")
        key(cam, land - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, land, rot=(R(1.6), R(-1.2), 0), interp="LINEAR"); key(cam, land + 3, rot=(0, 0, 0), interp="LINEAR")

# ---------------- 5: hood up, counting cylinders ----------------
def s5():
    k.world(); k.lot_set(); wh = W._flat_mat("wh", WHITE, 0.25); dk = W._flat_mat("bay", (0.02, 0.02, 0.024), 0.6); al = W._flat_mat("alu", (0.5, 0.5, 0.53), 0.35); rd = W._flat_mat("rd", (0.75, 0.04, 0.05), 0.4)
    eb = empty("bay", (0, 0, 0.75))
    box("bayfloor", (1.5, 1.2, 0.5), dk, (0, 0, -0.25), parent=eb); box("fenL", (0.3, 1.5, 0.3), wh, (0.9, 0, 0.0), parent=eb); box("fenR", (0.3, 1.5, 0.3), wh, (-0.9, 0, 0.0), parent=eb); box("bump", (2.1, 0.3, 0.5), wh, (0, -0.85, -0.2), parent=eb)
    box("cowl", (2.1, 0.2, 0.3), dk, (0, 0.72, 0.1), parent=eb); box("hood", (1.7, 1.4, 0.04), wh, (0, 0.95, 0.85), rot=(R(58), 0, 0), parent=eb); box("prop", (0.02, 0.02, 0.8), al, (0.6, 0.3, 0.45), rot=(R(-20), 0, 0), parent=eb)
    box("block", (0.86, 0.5, 0.2), al, (0, 0.05, 0.1), parent=eb); box("cover", (0.86, 0.26, 0.05), dk, (0, 0.22, 0.225), parent=eb); plane("coverl", 0.36, 0.18, imgmat("coverm", TEX + "cover.png"), (0, 0.22, 0.252), parent=eb)
    X = (0.24, 0.0, -0.24)
    for i, x in enumerate(X): box(f"coil{i}", (0.11, 0.11, 0.09), dk, (x, -0.08, 0.245), parent=eb); box(f"coilt{i}", (0.07, 0.07, 0.02), rd, (x, -0.08, 0.3), parent=eb)
    box("batt", (0.3, 0.2, 0.2), dk, (-0.52, -0.38, 0.05), parent=eb); box("airbox", (0.3, 0.3, 0.16), dk, (0.5, -0.36, 0.05), parent=eb); box("turbo", (0.16, 0.16, 0.16), al, (-0.5, 0.34, 0.12), parent=eb)
    L0 = (0, -1.0, 1.62); rig, cam = rigcam(L0, (0, 0.0, 0.98), lens=18); SH = (0.34, -1.0, 0.45)
    h = hand("hR", eb, (0.3, -0.5, 0.6), (0, 0, 0), curls=POINT, thumb=0.9)
    tip = lambda x, up=0.0: (x, -0.08, 0.315 + up)
    aim(h, 1, (0.5, -0.4, 0.6), SH)
    for i, f in enumerate((6, 13, 20)):
        aim(h, f - 3, tip(X[i], 0.1), SH); aim(h, f, tip(X[i]), SH); aim(h, f + 2, tip(X[i], 0.08), SH)
        key(cam, f - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, f, rot=(R(-1.2), 0, 0), interp="LINEAR"); key(cam, f + 2, rot=(0, 0, 0), interp="LINEAR")
    for f, x in ((25, -0.46), (28, -0.38), (31, -0.5), (33, -0.42), (34, -0.46)): aim(h, f, tip(x, 0.07), SH)   # looking for a fourth
    vis(h, 1, True); vis(h, 35, False)
    # shrug: both palms up, then pat the cover
    sr = hand("sR", cam, (0.26, -0.2, -0.5), (R(-60), R(170), R(-30)), curls=OPEN, thumb=-0.2); sl = hand("sL", cam, (-0.26, -0.2, -0.5), (R(-60), R(-170), R(30)), curls=OPEN, thumb=-0.2, mirror=True)
    for s_, sx in ((sr, 1), (sl, -1)):
        vis(s_, 1, False); vis(s_, 35, True); key(s_, 35, loc=(0.22 * sx, -0.3, -0.5), interp="LINEAR"); key(s_, 38, loc=(0.3 * sx, -0.14, -0.46), interp="LINEAR"); key(s_, 40, loc=(0.3 * sx, -0.17, -0.47), interp="LINEAR"); vis(s_, 41, False)
    pt = hand("pat", eb, (0.05, 0.1, 0.5), (R(-10), 0, R(8)), curls=FLAT, thumb=0.2); vis(pt, 1, False); vis(pt, 41, True)
    for f, z in ((41, 0.42), (43, 0.285), (45, 0.36), (47, 0.285)): key(pt, f, loc=(0.04, 0.08, z), interp="LINEAR")

# ---------------- cabin helpers ----------------
EYE = (0.36, 0.14, 1.25)
def cabin(look=(0.1, -0.8, 1.0), lens=19, loc=EYE, kit=True):
    root, by = C.grc(kit=kit, hide_glass=True); rig, cam = rigcam(loc, look, lens=lens, parent=root); W.cablight(root)
    dk = W._flat_mat("cab_dk", (0.035, 0.035, 0.04), 0.6)
    box("cab_dash", (1.5, 0.34, 0.2), dk, (0, -0.52, 0.98), parent=root); box("cab_cons", (0.24, 0.9, 0.2), dk, (0, 0.0, 0.62), parent=root); box("cab_bin", (0.5, 0.06, 0.16), dk, (0.36, -0.42, 1.08), parent=root)
    wh = W.wheel(root, (0.36, -0.3, 1.02)); plane("cab_grb", 0.05, 0.035, imgmat("cab_grm", TEX + "cover.png"), (0, 0, 0.017), parent=wh)
    return root, by, rig, cam

def limb(name, root, side, skin, shirt, rx=-100, bend=-10, rz=12):
    """Arm from the shoulder by explicit angles: rx -100 hangs down slightly forward, 160 reaches forward; bend folds the forearm."""
    a = box(name + "_ua", (0.1, 0.3, 0.1), shirt, loc=(side * 0.35, 0, 0.47), rot=(R(rx), 0, R(rz) * side), parent=root, base="y", taper=0.85)
    f = box(name + "_fa", (0.085, 0.28, 0.085), skin, loc=(0, 0.3, 0), rot=(R(bend), 0, 0), parent=a, base="y", taper=0.9)
    box(name + "_hd", (0.1, 0.11, 0.04), skin, loc=(0, 0.28, 0), parent=f, base="y"); return a, f

def legs(name, root, col=(0.08, 0.1, 0.2)):
    m = W._flat_mat(name + "_legm", col)
    for sx in (-1, 1): box(f"{name}_leg{sx}", (0.19, 0.2, 0.8), m, (sx * 0.12, 0, -0.8), parent=root, base="z")

def sillw(cam, side=1, col=WHITE, pillar=False):
    wh = W._flat_mat("ourdoor", col, 0.25); dk = W._flat_mat("ourtrim", (0.03, 0.03, 0.035), 0.5); e = empty("sill", parent=cam)
    box("sill1", (1.3, 0.09, 0.2), wh, (0.0, -0.37, -0.75), rot=(R(8), 0, R(-3) * side), parent=e); box("sill2", (1.3, 0.06, 0.04), dk, (0.0, -0.275, -0.74), rot=(R(8), 0, R(-3) * side), parent=e)
    if pillar: box("apill", (0.07, 0.9, 0.07), dk, (-0.5 * side, 0.05, -0.7), rot=(0, 0, R(-24) * side), parent=e)
    box("hdr", (1.4, 0.07, 0.1), dk, (0, 0.34, -0.72), rot=(R(-6), 0, R(-3) * side), parent=e); return e

def bubble(name, parent, loc, rot, w=0.9):
    return plane(name, w, w / 3, alphamat(name + "_m", f"{TEX}{name}.png"), loc, rot=rot, parent=parent)

def superlot():
    k.world(); k.lot_set(); plane("sign_s", 9, 1.35, imgmat("sign_sm", TEX + "sign_super.png", emit=0.3), (0, 6.95, 4.3), rot=(R(90), 0, 0))
    for i, x in enumerate((-5.4, -2.7, 2.7, 5.4)): k.lowcar(f"pk{i}", (x, 3.6, 0), 0, W._flat_mat(f"pk{i}m", [(0.5, 0.1, 0.1), (0.3, 0.32, 0.35), (0.1, 0.25, 0.4), (0.6, 0.6, 0.55)][i], 0.3), W._flat_mat(f"pk{i}g", (0.03, 0.04, 0.05), 0.1), W._flat_mat(f"pk{i}t", (0.02, 0.02, 0.02)), L=4.4)

# ---------------- 6: the AWD dial, in a supermarket car park ----------------
def s6():
    superlot(); root, by, rig, cam = cabin(look=(0.12, -0.8, 1.04), lens=17); lamp(root, (0.2, 0.0, 1.3), 16)
    KN = Vector((0.04, -0.33, 1.0)); ax = Vector((0.1, 0.9, 0.42)).normalized(); tilt = empty("knob_tilt", tuple(KN), parent=root); tilt.rotation_euler = ax.to_track_quat("Z", "Y").to_euler(); kb = empty("knob", parent=tilt)
    bpy.ops.mesh.primitive_cylinder_add(vertices=18, radius=0.05, depth=0.05); kn = bpy.context.object; kn.data.materials.append(W._flat_mat("knm", (0.5, 0.5, 0.53), 0.3)); kn.parent = kb; kn.location = (0, 0, 0.025)
    box("kn_mark", (0.014, 0.045, 0.006), W._flat_mat("knr", (0.9, 0.05, 0.05), emit=1), (0, 0.024, 0.052), parent=kb)
    d = {m: plane("awd_" + m, 0.26, 0.162, imgmat("awdm_" + m, f"{TEX}awd_{m}.png", emit=1.2), (0.04, -0.4, 1.19), rot=(R(74), 0, R(180)), parent=root) for m in ("6040", "3070", "5050")}
    box("awd_bez", (0.28, 0.18, 0.03), W._flat_mat("bez", (0.02, 0.02, 0.02)), (0.04, -0.418, 1.185), rot=(R(74), 0, R(180)), parent=root); box("awd_stand", (0.06, 0.05, 0.12), W._flat_mat("bez2", (0.02, 0.02, 0.02)), (0.04, -0.44, 1.1), parent=root)
    bpy.context.view_layer.update(); SH = Vector((0.3, 0.3, 0.98)); dv = (KN - SH).normalized(); grip = KN + ax * 0.085 - dv * 0.075
    h = hand("hR", None, (0, 0, 0), (0, 0, 0), curls=(0.8, 0.85, 0.9, 0.95), thumb=0.5); h.rotation_euler = dv.to_track_quat("Y", "Z").to_euler(); h.location = grip; bpy.context.view_layer.update()
    mw = h.matrix_world.copy(); h.parent = kb; h.matrix_parent_inverse = kb.matrix_world.inverted(); h.matrix_basis.identity(); h.matrix_world = mw
    seq = ["6040", "3070", "5050", "3070", "6040", "5050", "3070", "5050", "6040", "3070", "5050"]; sched = []
    for i, m in enumerate(seq):
        f = 1 + i * 4; sched.append((f, m)); key(kb, f, rot=(0, 0, R(32 if i % 2 else -32)), interp="LINEAR")
    swap(d, sched)
    hl = hand("hL", root, (0.52, -0.2, 1.1), (R(12), 0, R(172)), curls=FIST, thumb=0.9, mirror=True)
    A = lookrot(EYE, (0.12, -0.8, 1.02)); B = lookrot(EYE, (0.0, -8, 1.32)); key(rig, 1, rot=A, interp="LINEAR"); key(rig, 27, rot=A, interp="LINEAR"); key(rig, 33, rot=B, interp="LINEAR")
    for f, ln in ((1, 19), (27, 21), (33, 20)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    root.rotation_euler = (0, 0, R(180)); key(root, 1, loc=(1.35, -9.5, 0), interp="LINEAR"); key(root, 48, loc=(1.35, -8.6, 0), interp="LINEAR")
    # a shopper with a trolley overtakes him
    t = empty("trolley", (3.0, -10, 0), (0, 0, R(180))); gm = W._flat_mat("trm", (0.6, 0.62, 0.65), 0.3); box("tr_b", (0.55, 0.9, 0.45), gm, (0, 0, 0.55), parent=t, base="z"); box("tr_h", (0.55, 0.04, 0.04), W._flat_mat("trh", (0.8, 0.1, 0.1)), (0, 0.5, 1.05), parent=t)
    for sx in (-1, 1): box(f"tr_l{sx}", (0.04, 0.8, 0.5), gm, (sx * 0.25, 0, 0.05), parent=t, base="z")
    p, head, fd, sk = guy("shop", "pump", (0, 0.95, 0.85), 0, ["flat"], (0.8, 0.6, 0.48), (0.2, 0.45, 0.3), hat=False); p.parent = t; legs("shop", p); arm("sha", p, 1, sk, mat("polo_sh", (0.2, 0.45, 0.3)), up=-25, fwd=85, bend=10); arm("shb", p, -1, sk, mat("polo_sh2", (0.2, 0.45, 0.3)), up=-25, fwd=85, bend=10)
    key(t, 1, loc=(2.9, -12.5, 0), interp="LINEAR"); key(t, 30, loc=(2.9, -9.0, 0), interp="LINEAR"); key(t, 48, loc=(2.9, -4.5, 0), interp="LINEAR")

# ---------------- 7: "Corolla for Kevin?" ----------------
def s7():
    W.road(); root, by, rig, cam = cabin(look=(0.1, -3, 1.1), lens=17)
    p, head, fd, sk = guy("kevin", "kevin", (-0.36, 1.0, 0.48), 0, ["flat", "blink", "talk"], (0.33, 0.2, 0.12), (0.85, 0.75, 0.2), hat=False); p.parent = root
    box("case", (0.3, 0.42, 0.55), W._flat_mat("casem", (0.1, 0.3, 0.6), 0.4), (0.2, 1.0, 0.55), parent=root, base="z"); box("case_h", (0.14, 0.03, 0.06), W._flat_mat("caseh", (0.05, 0.05, 0.05)), (0.2, 1.0, 1.13), parent=root)
    arm("ka", p, 1, sk, mat("polo_ka", (0.85, 0.75, 0.2)), up=-50, fwd=75, bend=100)
    lamp(root, (0.0, 0.7, 1.3), 10)
    bb = bubble("bubble_kevin", root, (0.2, 0.8, 1.24), (R(90), 0, R(22)), w=0.62); vis(bb, 1, False); vis(bb, 11, True)
    for f, sc_ in ((11, 0.2), (14, 1.12), (16, 1.0)): key(bb, f, scale=(0.62 * sc_, 0.62 / 3 * sc_, 1), interp="LINEAR")
    BK = (-0.25, 1.0, 1.08); A = lookrot(EYE, (0.1, -3, 1.1)); B = lookrot(EYE, BK, 4)
    key(rig, 1, rot=A, interp="LINEAR"); key(rig, 3, rot=A, interp="LINEAR"); key(rig, 9, rot=B, interp="LINEAR"); key(rig, 47, rot=lookrot(EYE, BK, 2), interp="LINEAR")
    for f, ln in ((1, 17), (9, 20), (47, 24)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    swap(fd, [(1, "flat"), (11, "talk"), (15, "flat"), (18, "talk"), (22, "flat"), (30, "blink"), (33, "flat")])
    for f, rz in ((1, 0), (11, 6), (18, -5), (26, 0)): key(head, f, rot=(R(8), 0, R(rz)), interp="CONSTANT")
    h = hand("hR", cam, (0.2, -0.3, -0.45), (R(-75), R(10), R(-15)), curls=POINT, thumb=0.9)
    key(h, 1, loc=(0.4, -0.5, -0.4), interp="LINEAR"); key(h, 22, loc=(0.4, -0.5, -0.4), interp="LINEAR")
    for i, f in enumerate(range(26, 47, 4)): key(h, f, loc=(0.16 + 0.05 * (i % 2), -0.2, -0.45), rot=(R(-80 + 22 * (i % 2)), R(10), R(-15)), interp="LINEAR")
    shake(cam, 24, 47, 0.5, seed=7)

# ---------------- 8: grandma ----------------
def s8():
    superlot(); loc = (-0.5, 0.25, 1.22); TG = (-2.35, 0.2, 1.1); rig, cam = rigcam(loc, TG, lens=30); sillw(cam, side=-1)
    h_, hb = C.hatch(); h_.location = (-2.75, 0.0, 0); hb["glass"].hide_render = True; hb["interior"].hide_render = True
    box("gseat", (0.5, 0.14, 0.8), W._flat_mat("gseatm", (0.45, 0.4, 0.32)), (0.38, 0.42, 0.4), parent=h_, base="z"); box("gfloor", (1.5, 2.2, 0.3), W._flat_mat("gfl", (0.05, 0.05, 0.05)), (0, 0.3, 0.3), parent=h_, base="z")
    p, head, fd, sk = guy("gran", "gran", (0.38, 0.2, 0.4), R(84), ["grin", "proud"], (0.86, 0.72, 0.64), (0.75, 0.55, 0.75), hat=False, hair=(0.75, 0.75, 0.78)); p.parent = h_
    a, f_ = limb("ga", p, 1, sk, mat("polo_ga", (0.75, 0.55, 0.75)), rx=160, bend=-70, rz=0)
    for f in range(9, 47, 4): key(f_, f, rot=(R(-70), R(-22), 0), interp="LINEAR"); key(f_, f + 2, rot=(R(-70), R(22), 0), interp="LINEAR")
    swap(fd, [(1, "grin"), (13, "proud"), (20, "grin"), (30, "proud")])
    key(h_, 1, loc=(-2.75, 3.2, 0), interp="LINEAR"); key(h_, 7, loc=(-2.75, 0.06, 0), interp="LINEAR"); key(h_, 9, loc=(-2.75, 0.0, 0), interp="LINEAR")
    for f, ln in ((1, 30), (9, 30), (22, 36)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    # he slides down in his seat and hides behind both hands
    key(rig, 26, loc=loc, interp="LINEAR"); key(rig, 42, loc=(loc[0], loc[1], 1.0), interp="LINEAR")
    for nm, sx in (("hR", 1), ("hL", -1)):
        h = hand(nm, cam, (sx * 0.1, -0.6, -0.34), (R(-12), R(180), R(8 * sx)), curls=FLAT, thumb=0.2, mirror=sx < 0)
        key(h, 24, loc=(sx * 0.16, -0.62, -0.36), interp="LINEAR"); key(h, 34, loc=(sx * 0.085, -0.16, -0.34), interp="LINEAR"); key(h, 47, loc=(sx * 0.075, -0.1, -0.3), interp="LINEAR")

# ---------------- 9-10: red light, Type R on the right, WRX on the left ----------------
def lights():
    W.road(); root = None
    tr, trb = C.fl5(); tr.location = (-3.05, -0.1, 0)
    p1, h1, f1, s1_ = guy("typer", "typer", (0.38, 0.1, 0.3), R(72), ["smug", "talk", "grin", "horror"], (0.74, 0.52, 0.38), (0.93, 0.93, 0.96)); p1.parent = tr
    a1, fa1 = arm("ta", p1, -1, s1_, mat("polo_ta", (0.93, 0.93, 0.96)), up=20, fwd=-50, bend=30); box("t_vape", (0.035, 0.035, 0.14), W._flat_mat("tvape", (0.75, 0.08, 0.5), 0.3), loc=(0, 0.3, 0.05), parent=fa1)
    wx, wb = C.wrx(); wx.location = (3.25, -0.1, 0); wb["glass"].hide_render = True
    p2, h2, f2, s2_ = guy("wrxguy", "wrxguy", (-0.42, -0.05, 0.3), R(-78), ["smug", "talk", "grin", "horror"], (0.33, 0.19, 0.11), (0.25, 0.28, 0.2)); p2.parent = wx; p2.rotation_euler = (0, R(-14), R(-78))
    a2, fa2 = arm("wa", p2, 1, s2_, mat("polo_wa", (0.25, 0.28, 0.2)), up=20, fwd=-50, bend=30); box("w_vape", (0.035, 0.035, 0.14), W._flat_mat("wvape", (0.75, 0.08, 0.5), 0.3), loc=(0, 0.3, 0.05), parent=fa2)
    box("pole", (0.15, 0.15, 5), W._flat_mat("pole", (0.2, 0.2, 0.2)), (5.6, -9, 0), base="z"); box("lightbox", (0.4, 0.3, 1.1), W._flat_mat("lb", (0.08, 0.08, 0.08)), (4.6, -9, 4.3), base="z"); box("red", (0.26, 0.05, 0.26), W._flat_mat("redl", (1, 0.08, 0.05), emit=6), (4.6, -8.84, 5.0), base="z")
    loc = (0.36, 0.2, 1.22); rig, cam = rigcam(loc, (-2.63, -0.1, 1.06), lens=30); sillw(cam)
    RT = lookrot(loc, (-2.63, -0.05, 1.08), 2); LT = lookrot(loc, (2.75, -0.15, 1.1), -2)
    return dict(rig=rig, cam=cam, RT=RT, LT=LT, tr=tr, wx=wx, h1=h1, f1=f1, a1=a1, h2=h2, f2=f2, a2=a2, root=root)

def s9():
    L = lights(); rig, cam = L["rig"], L["cam"]
    key(rig, 1, rot=L["RT"], interp="LINEAR"); key(rig, 50, rot=L["RT"], interp="LINEAR"); key(rig, 55, rot=L["LT"], interp="LINEAR"); key(rig, 76, rot=L["LT"], interp="LINEAR"); key(rig, 81, rot=L["RT"], interp="LINEAR")
    for f, ln in ((1, 44), (50, 50), (55, 40), (76, 44), (81, 54), (95, 60)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    swap(L["f1"], [(1, "smug"), (60, "talk"), (63, "smug"), (66, "talk"), (70, "grin")]); swap(L["f2"], [(1, "smug"), (60, "talk"), (63, "smug"), (66, "talk"), (70, "grin")])
    for f, rx, rz in ((1, 0, -6), (8, 12, -6), (14, -4, -6), (20, 10, -6), (26, 0, -6), (81, -6, 4), (88, 4, -6)): key(L["h1"], f, rot=(R(rx), R(-6), R(rz)), interp="LINEAR" if f < 30 else "CONSTANT")
    for f, rx, rz in ((1, 0, 6), (56, 8, 6), (60, -6, -4), (66, 6, 8), (70, 0, 0)): key(L["h2"], f, rot=(R(rx), R(6), R(rz)), interp="CONSTANT")
    h = hand("hR", cam, (0.16, -0.2, -0.42), (R(-66), R(10), R(-22)), curls=POINT, thumb=0.9)
    key(h, 1, loc=(0.3, -0.4, -0.4), interp="LINEAR"); key(h, 10, loc=(0.16, -0.2, -0.42), rot=(R(-66), R(10), R(-22)), interp="LINEAR")
    for f in range(14, 44, 6): key(h, f, loc=(0.1, -0.24, -0.4), rot=(R(-110), R(10), R(10)), interp="LINEAR"); key(h, f + 3, loc=(0.1, -0.27, -0.42), rot=(R(-120), R(10), R(10)), interp="LINEAR")
    key(h, 48, loc=(0.3, -0.45, -0.4), interp="LINEAR"); vis(h, 1, True); vis(h, 50, False)
    shake(cam, 1, 48, 0.3, step=3, seed=11)

def s10():
    L = lights(); rig, cam = L["rig"], L["cam"]
    key(rig, 1, rot=L["RT"], interp="LINEAR"); key(rig, 12, rot=L["RT"], interp="LINEAR"); key(rig, 16, rot=L["LT"], interp="LINEAR"); key(rig, 36, rot=L["LT"], interp="LINEAR"); key(rig, 40, rot=L["RT"], interp="LINEAR")
    for f, ln in ((1, 46), (12, 46), (16, 40), (36, 44), (40, 54), (48, 62)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    for fd in (L["f1"], L["f2"]): swap(fd, [(1, "grin"), (14, "smug"), (26, "grin"), (33, "horror")])
    for i, rf in enumerate((4, 17, 30)):
        for a, sg in ((L["a1"], -1), (L["a2"], 1)):
            key(a, rf - 3, rot=(R(-10), 0, R(140) * sg), interp="LINEAR"); key(a, rf + 2, rot=(R(20), 0, R(140) * sg), interp="LINEAR"); key(a, rf + 9, rot=(R(-10), 0, R(140) * sg), interp="LINEAR")
        for hd, sg in ((L["h1"], -1), (L["h2"], 1)): key(hd, rf, rot=(R(-10), R(-6 * -sg), R(6 * sg)), interp="CONSTANT"); key(hd, rf + 6, rot=(R(6), R(-6 * -sg), R(-4 * sg)), interp="CONSTANT")
        shake(cam, rf, rf + 9, 1.3, seed=20 + i)
    h = hand("hR", cam, (0.2, -0.16, -0.42), (R(-50), R(10), R(-20)), curls=FIST, thumb=0.9)
    for rf in (4, 17, 30): key(h, rf - 3, loc=(0.2, -0.24, -0.42), interp="LINEAR"); key(h, rf + 2, loc=(0.2, 0.0, -0.4), interp="LINEAR"); key(h, rf + 9, loc=(0.2, -0.24, -0.42), interp="LINEAR")

# ---------------- 11: "Is that the hybrid?" ----------------
def s11():
    k.world(); k.lot_set(); root, by = C.grc(kit=True)
    cn = W._flat_mat("canopy", (0.85, 0.1, 0.1), 0.4); box("canopy", (9, 7, 0.4), cn, (-3, 1, 4.6), base="z")
    for x in (-6.5, -1.9): box(f"col{x}", (0.3, 0.3, 4.6), W._flat_mat(f"colm{x}", (0.8, 0.8, 0.8)), (x, 1.2, 0), base="z")
    plane("sign_g", 1.6, 0.6, imgmat("sign_gm", TEX + "sign_gas.png", emit=0.4), (-3, -2.49, 4.8), rot=(R(90), 0, 0))
    pb = box("pumpb", (0.7, 0.45, 1.7), W._flat_mat("pumpm", (0.85, 0.86, 0.88), 0.4), (-2.6, 1.25, 0.15), base="z"); box("pump_is", (1.6, 1.0, 0.15), W._flat_mat("isl", (0.5, 0.5, 0.5)), (-2.6, 1.25, 0), base="z")
    plane("pump_face", 0.5, 0.66, imgmat("pump_fm", TEX + "pump.png", emit=0.4), (-2.24, 1.25, 1.35), rot=(R(90), 0, R(90)))
    loc = (-2.0, 3.05, 1.62); rig, cam = rigcam(loc, (-1.2, 1.3, 1.05), lens=19)
    # nozzle in the filler, hand on it (car space, so it stays on the car)
    FL = Vector((-0.93, 1.45, 0.93)); nz = empty("nozzle", tuple(FL + Vector((-0.02, 0, 0))), (0, 0, R(-116)), parent=root); bk = W._flat_mat("nzm", (0.03, 0.03, 0.03), 0.4)
    box("nz_spout", (0.03, 0.2, 0.03), W._flat_mat("nzs", (0.6, 0.6, 0.62), 0.3), (0, 0.1, 0), parent=nz, base="y"); box("nz_body", (0.07, 0.24, 0.1), bk, (0, -0.22, 0.01), parent=nz, base="y"); box("nz_grip", (0.05, 0.08, 0.2), bk, (0, -0.2, -0.1), parent=nz)
    box("nz_hose", (0.035, 0.035, 0.9), bk, (0, -0.26, -0.5), rot=(R(-20), 0, 0), parent=nz)
    box("flap", (0.02, 0.16, 0.16), W._flat_mat("flapm", WHITE, 0.25), (-0.97, 1.6, 0.93), rot=(0, 0, R(50)), parent=root)
    bpy.context.view_layer.update(); gp = nz.matrix_world @ Vector((0, -0.12, 0.07)); SH = Vector((-1.75, 2.95, 1.2)); dv = (gp - SH).normalized()
    h = hand("hR", None, (0, 0, 0), (0, 0, 0), curls=(1.0, 1.05, 1.1, 1.15), thumb=0.8); h.rotation_euler = dv.to_track_quat("Y", "Z").to_euler(); h.location = gp - dv * 0.1; bpy.context.view_layer.update()
    mw = h.matrix_world.copy(); h.parent = nz; h.matrix_parent_inverse = nz.matrix_world.inverted(); h.matrix_basis.identity(); h.matrix_world = mw
    hl = hand("hL", cam, (-0.3, -0.36, -0.42), (R(-60), 0, R(20)), curls=OPEN, mirror=True)
    p, head, fd, sk = guy("pump", "pump", (-3.3, 2.0, 0.84), R(140), ["grin", "talk"], (0.8, 0.6, 0.48), (0.3, 0.35, 0.6), hat=False, hair=(0.6, 0.5, 0.3)); legs("pump", p)
    psh = mat("polo_pa", (0.3, 0.35, 0.6)); limb("pa", p, 1, sk, psh); pa2, pf2 = limb("pb", p, -1, sk, psh, rx=-130, bend=-60)
    for f in range(9, 47, 5): key(pa2, f, rot=(R(-130), 0, R(-6)), interp="LINEAR"); key(pa2, f + 2, rot=(R(-142), 0, R(-6)), interp="LINEAR")
    key(p, 1, loc=(-4.6, 2.3, 0.84), interp="LINEAR"); key(p, 6, loc=(-3.0, 1.95, 0.84), rot=(0, 0, R(140)), interp="LINEAR"); key(p, 9, loc=(-2.95, 1.95, 0.84), rot=(R(-10), 0, R(140)), interp="LINEAR")
    swap(fd, [(1, "grin"), (9, "talk"), (12, "grin"), (15, "talk"), (18, "grin"), (21, "talk"), (24, "grin")])
    bb = bubble("bubble_hybrid", None, (-2.75, 1.95, 2.0), lookrot((-2.75, 1.95, 2.0), loc), w=1.25); bb.rotation_euler = lookrot(loc, (-2.75, 1.95, 2.0)); vis(bb, 1, False); vis(bb, 9, True)
    for f, sc_ in ((9, 0.2), (12, 1.12), (14, 1.0)): key(bb, f, scale=(1.25 * sc_, 1.25 / 3 * sc_, 1), interp="LINEAR")
    A = lookrot(loc, (-1.2, 1.3, 1.05)); B = lookrot(loc, (-2.5, 1.8, 1.5), 3); key(rig, 1, rot=A, interp="LINEAR"); key(rig, 5, rot=A, interp="LINEAR"); key(rig, 10, rot=B, interp="LINEAR"); key(rig, 26, rot=B, interp="LINEAR"); key(rig, 31, rot=lookrot(loc, (-1.1, 1.4, 0.95)), interp="LINEAR")
    for f, ln in ((1, 19), (26, 19), (31, 24), (47, 34)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    rnd = random.Random(3)
    for f in range(30, 48): a = 0.004 + 0.012 * (f - 30) / 17; key(nz, f, loc=tuple(FL + Vector((-0.02 + rnd.uniform(-a, a), rnd.uniform(-a, a), rnd.uniform(-a, a)))), interp="LINEAR")
    shake(cam, 30, 47, 0.8, seed=5)

# ---------------- 12: more GR stickers ----------------
def s12():
    k.world(); k.lot_set(); root, by = C.grc(kit=True); bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    loc = (0.3, 3.3, 1.38); rig, cam = rigcam(loc, (0.0, 2.1, 1.02), lens=20); sm = alphamat("stk", TEX + "sticker_gr.png"); slaps = [9, 22, 35]; spots = [("body", 0.36, 0.86), ("body", -0.36, 0.86), ("glass", 0.0, 1.24)]
    SH = (0.62, 3.25, 1.0); h = hand("hR", root, (0.5, 2.9, 0.9), (0, 0, 0), curls=FLAT, thumb=0.2); aim(h, 1, (0.85, 2.8, 0.95), SH)
    for i, ((obn, x, z), sf) in enumerate(zip(spots, slaps)):
        ob = by[obn]; inv = ob.matrix_world.inverted(); ok, hit, nrm, _ = ob.ray_cast(inv @ Vector((x, 4.0, z)), inv.to_3x3() @ Vector((0, -1, 0)), depsgraph=dg)
        hit = ob.matrix_world @ hit; nrm = (ob.matrix_world.to_3x3() @ nrm).normalized()
        st = plane(f"stk{i}", 0.34, 0.2125, sm, tuple(hit + nrm * 0.004), parent=root); st.rotation_euler = nrm.to_track_quat("Z", "Y").to_euler(); vis(st, 1, False); vis(st, sf, True)
        on = hit + nrm * 0.012; back = hit + nrm * 0.4 + Vector((0.1, 0, 0.05))
        aim(h, sf - 5, tuple(back), SH); aim(h, sf, tuple(on), SH, reach=0.17); aim(h, sf + 2, tuple(on), SH, reach=0.17); aim(h, sf + 6, tuple(back), SH)
        key(cam, sf - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, sf, rot=(R(-1.8), R(0.8), 0), interp="LINEAR"); key(cam, sf + 3, rot=(0, 0, 0), interp="LINEAR")
    hl = hand("hL", cam, (-0.24, -0.34, -0.42), (R(-60), 0, R(20)), curls=FIST, thumb=0.9, mirror=True)
    for f in range(1, 48, 6): key(hl, f, loc=(-0.24, -0.34 + 0.03 * ((f // 6) % 2), -0.42), interp="LINEAR")
    for f, ln in ((1, 20), (48, 24)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

# ---------------- 13-14: the meet ----------------
def dup(root, loc):
    m = {}
    def rec(o, par):
        d = o.copy(); bpy.context.scene.collection.objects.link(d); d.parent = par; m[o] = d
        for c in o.children: rec(c, d)
        return d
    d = rec(root, None); d.location = loc; return d

def meet(n=6, gran=False, thumbs=False):
    k.world(img="sky_dawn.png", sun=(2.2, 72, 60)); k.lot_set()
    root, by = C.grc(kit=True); cars = [root] + [dup(root, (i * 2.7, 0, 0)) for i in range(1, n)]
    for i, c in enumerate(cars): c.location = ((i - (n - 1) / 2) * 2.7, 0, 0)
    sk = mat("clone_skin", (0.74, 0.55, 0.42), 0.7); sh = mat("polo_clone", (0.1, 0.1, 0.12)); cl = []
    for i, c in enumerate(cars):
        p, head, fd = person(f"cl{i}", "clone", (c.location.x + 1.25, -1.9, 0.84), R(180), sk, sh, mat(f"cl{i}_hair", (0.05, 0.04, 0.03)), ["flat", "blank"], hair_h=0.04); cap(f"cl{i}", head); legs(f"cl{i}", p)
        a, fa = arm(f"cl{i}a", p, 1, sk, sh, up=30, fwd=60, bend=95); box(f"cl{i}_vape", (0.035, 0.035, 0.14), W._flat_mat(f"cl{i}v", (0.75, 0.08, 0.5), 0.3), loc=(0, 0.3, 0.05), parent=fa); cl.append((p, head, fd))
    g = None
    if gran:
        h_, hb = C.hatch(); h_.location = (cars[0].location.x - 2.7, 0, 0); h_.rotation_euler = (0, 0, R(180))   # backed in, so the spoiler extension faces us
        se = by["part_spoiler_extension"].copy(); bpy.context.scene.collection.objects.link(se); se.parent = h_; se.hide_render = False; se.location = (0, 0, -0.04)   # Spoiler Extension (listing: Corolla Hatchback / GR Corolla); hatch roof is 40 mm lower
        gs = mat("gran_skin", (0.86, 0.72, 0.64), 0.7); gsh = mat("polo_gr", (0.75, 0.55, 0.75)); p, head, fd = person("gran", "gran", (h_.location.x + 1.25, -2.6, 0.84), 0, gs, gsh, mat("gran_hair", (0.75, 0.75, 0.78)), ["grin"], bun=True); legs("gran", p, (0.3, 0.3, 0.4))
        if thumbs:
            a, fa = arm("gra", p, -1, gs, gsh, up=40, fwd=70, bend=80); box("gr_thumb", (0.035, 0.035, 0.1), gs, (0, 0.33, 0.07), parent=fa)
        g = (h_, p, head)
    return cars, cl, g

def s13():
    cars, cl, g = meet(6); A = (-9.2, -4.6, 1.62); B = (-6.6, -4.4, 1.62); rig, cam = rigcam(A, (-3.5, -1.2, 1.1), lens=24)
    key(rig, 1, loc=A, rot=lookrot(A, (-5.0, -1.5, 1.15)), interp="LINEAR"); key(rig, 95, loc=B, rot=lookrot(B, (-1.0, -1.5, 1.15)), interp="LINEAR")
    for i, (p, head, fd) in enumerate(cl):
        swap(fd, [(1, "flat"), (52, "blank")]); toc = math.atan2(-(B[0] - p.location.x), (B[1] - p.location.y))
        key(p, 1, rot=(0, 0, R(180)), interp="CONSTANT"); key(p, 52, rot=(0, 0, R(180) + toc), interp="CONSTANT")
    for nm, sx in (("hR", 1), ("hL", -1)):
        h = hand(nm, cam, (sx * 0.3, -0.3, -0.5), (R(20), 0, R(-10 * sx)), curls=OPEN, mirror=sx < 0)
        for f in range(1, 50, 6): key(h, f, loc=(sx * 0.3, -0.3, -0.5), rot=(R(20), 0, R((-10 + 16 * ((f // 6) % 2)) * sx)), interp="LINEAR")
        key(h, 54, loc=(sx * 0.3, -0.3, -0.5), rot=(R(20), 0, R(-10 * sx)), interp="LINEAR"); key(h, 92, loc=(sx * 0.3, -0.5, -0.5), rot=(R(-30), 0, R(-10 * sx)), interp="LINEAR")

def mirrorbg(thumbs):
    cars, cl, g = meet(4, gran=True, thumbs=thumbs)
    for (p, head, fd) in cl: swap(fd, [(1, "blank")]); p.rotation_euler = (0, 0, 0)
    gx = g[0].location.x; rig, cam = rigcam((gx + 1.55, -8.0, 0.95), (gx + 1.55, 0, 1.2), lens=46); sc = bpy.context.scene; sc.render.resolution_x = 720; sc.render.resolution_y = 250

def s14():
    k.world(img="sky_dawn.png", sun=(2.2, 72, 60)); k.lot_set(); root, by, rig0, cam0 = cabin(); bpy.data.objects.remove(cam0); bpy.data.objects.remove(rig0)
    # the mirror is yawed toward the driver (owner: it was angled away from him)
    mc = Vector((0.03, -0.25, 1.268)); fr = empty("mir", mc, (R(-5), 0, R(-20))); MW, MH = 0.36, 0.125; blk = W._flat_mat("mirf", (0.02, 0.02, 0.02))
    bg = {i: plane(f"mir_bg{i}", MW, MH, imgmat(f"mirbg{i}", f"{TEX}mirror_bg{i}.png", emit=0.9), (0, 0, 0), rot=(R(90), 0, R(180)), parent=fr) for i in (0, 1)}; swap(bg, [(1, 0), (104, 1)])
    for nm, sz, lc in (("rt", (MW + 0.02, 0.03, 0.012), (0, 0.004, MH / 2 + 0.004)), ("rb", (MW + 0.02, 0.03, 0.012), (0, 0.004, -MH / 2 - 0.004)), ("rl", (0.012, 0.03, MH + 0.02), (-MW / 2 - 0.004, 0.004, 0)), ("rr", (0.012, 0.03, MH + 0.02), (MW / 2 + 0.004, 0.004, 0))): box("mir_" + nm, sz, blk, lc, parent=fr)
    box("mir_house", (MW + 0.02, 0.03, MH + 0.02), blk, (0, -0.018, 0), parent=fr); box("mir_stalk", (0.03, 0.03, 0.1), blk, (0, -0.03, 0.1), parent=fr)
    hs = W._flat_mat("skin_face", (0.74, 0.55, 0.42), 0.6, emit=0.25); sc_ = 0.2
    p, head, fd = person("him", "him", (0, 0, 0), 0, hs, W._flat_mat("htee", (0.1, 0.1, 0.12), emit=0.2), W._flat_mat("hhair", (0.02, 0.02, 0.02)), ["blank", "twitch", "pinpoint", "horror"], hair_h=0.04)
    p.parent = fr; p.rotation_euler = (0, 0, R(180)); p.scale = (sc_, sc_ * 0.06, sc_); p.location = (-0.085, 0.006, -(0.62 + 0.15) * sc_)
    for o in p.children:
        if o.name.endswith("_torso"): o.hide_render = True
    box("him_sh", (0.15, 0.004, 0.022), W._flat_mat("htee2", (0.1, 0.1, 0.12), emit=0.2), (-0.085, 0.004, -MH / 2 + 0.011), parent=fr)
    swap(fd, [(1, "blank"), (112, "twitch"), (118, "blank"), (134, "twitch"), (150, "pinpoint"), (186, "horror")])
    for f, rz in ((1, 0), (112, 5), (118, 0), (134, -6), (150, 3), (186, -4), (198, 5), (206, -5)): key(head, f, rot=(0, R(rz), 0), interp="CONSTANT")
    a = EYE; b = (0.3, 0.1, 1.26); rig, cam = rigcam(a, (0.1, -0.75, 1.06), lens=19, parent=root)
    # he looks up, then down, and sighs (owner: no dash slap), then his eyes go to the mirror
    FW = (0.2, -0.9, 1.08); UP = (0.2, -0.8, 1.75); DN = (0.34, -0.45, 0.72)
    for f, tg in ((1, FW), (16, UP), (22, UP), (36, DN), (44, DN), (56, tuple(mc))): key(rig, f, loc=a, rot=lookrot(a, tg), interp="BEZIER")
    key(rig, 213, loc=b, rot=lookrot(b, tuple(mc), -2), interp="LINEAR")
    for f, ln in ((1, 19), (44, 20), (56, 30), (213, 62)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    hr = hand("hR", root, (0.2, -0.22, 1.1), (R(12), 0, R(188)), curls=FIST, thumb=0.9); hl = hand("hL", root, (0.52, -0.2, 1.1), (R(12), 0, R(172)), curls=FIST, thumb=0.9, mirror=True)
    for h, x in ((hr, 0.2), (hl, 0.52)):   # the sigh: both hands sag on the wheel and come back
        key(h, 20, loc=(x, -0.22 if h is hr else -0.2, 1.1), interp="BEZIER"); key(h, 34, loc=(x, -0.2, 1.065), interp="BEZIER"); key(h, 50, loc=(x, -0.22 if h is hr else -0.2, 1.1), interp="BEZIER")

SHOTS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]
if __name__ == "__main__":
    a = sys.argv[sys.argv.index("--") + 1:]; n = int(a[0]) if a[0].isdigit() else 14; out = a[1]; mode = a[2] if len(a) > 2 else "anim"; res = int(a[3]) if len(a) > 3 else 540; smp = int(a[4]) if len(a) > 4 else 14
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if a[0].startswith("mirror"): n = 14; mirrorbg(a[0].endswith("1"))
    else: SHOTS[n - 1]()
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = smp; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 3
    sc.render.resolution_x = sc.render.resolution_y = res
    if a[0].startswith("mirror"): sc.render.resolution_x = 720; sc.render.resolution_y = 250; sc.render.filepath = f"{TEX}mirror_bg{a[0][-1]}.png"; bpy.ops.render.render(write_still=True); sys.exit()
    sc.render.resolution_y = res; sc.view_settings.view_transform = "Standard"; sc.render.fps = 30; sc.frame_start = int(a[5]) if len(a) > 5 else 1; sc.frame_end = NF[n - 1]
    sc.render.image_settings.file_format = "PNG"
    if mode == "anim":
        sc.render.filepath = f"{out}/s{n:02d}/"; bpy.ops.render.render(animation=True)
    else:
        for fr in mode.split(","):
            sc.frame_set(int(fr)); sc.render.filepath = f"{out}/s{n:02d}_f{int(fr):03d}.png"; bpy.ops.render.render(write_still=True)
