"""Shots of 'Day in the life of an average track guy'. blender -b --python tl_shots.py -- <shot> <outdir> [anim|f1,f2] [res] [samples]
Reuses the WRX kit (shots.py: rigs, keys, rooms, people, phone) with the FK8 + configurator TC wing (lookdev.py) and gloved hands (hands.py).
Car convention (as WRX): the car faces -Y, centred on the origin; its left (driver, LHD) is +X."""
import bpy, sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots as W
import lookdev as LD
import hands as HD
from ditl_kit import box, plane, R, TEX
from mathutils import Vector, Matrix

mat, imgmat, alphamat, key, vis, swap, shake, rigcam, lookrot = W.mat, W.imgmat, W.alphamat, W.key, W.vis, W.swap, W.shake, W.rigcam, W.lookrot
OPEN, FIST, POINT, FLAT = HD.OPEN, HD.FIST, HD.POINT, HD.FLAT
HALF = 2.28                                   # FK8 length / 2: car frame x (from rear bumper) -> centred
NF = {1: 66, 2: 48, 3: 47, 4: 95, 5: 48, 6: 48, 7: 47, 8: 48, 9: 48, 10: 48, 11: 162, 12: 48, 13: 48, 14: 81, 15: 180}

_G = {}
def kit():
    if not _G:
        _G["glove"] = W._flat_mat("glove", (0.55, 0.04, 0.03), 0.65); _G["suit"] = W._flat_mat("suit", (0.06, 0.1, 0.45), 0.8)
    return _G

def ghand(name, parent, loc, rot, curls=OPEN, thumb=0.3, mirror=False, hold=None):
    g = kit(); return HD.hand(name, parent, loc, rot, curls=curls, thumb=thumb, mirror=mirror, sleeve=g["suit"], glove=g["glove"], hold=hold)

def tofk(v):
    """Centred car space (faces -Y) -> FK8 GLB frame (x fwd from rear bumper, Blender y = car left)."""
    return (HALF - v[1], v[0], v[2])

def fk8car(wing=True, glass_clear=False):
    """FK8 (our scan) + TE37s + configurator TC wing under one root. Returns (veh, wing_group or None)."""
    before = set(bpy.data.objects); LD.fk8(); new = [o for o in bpy.data.objects if o not in before]
    if glass_clear:
        for o in new:
            if o.name == "fk8": seethrough(o.data.materials[0])
    wg = None
    if wing:
        b2 = set(bpy.data.objects); LD.tc_wing(); wparts = [o for o in bpy.data.objects if o not in b2]
        wg = bpy.data.objects.new("wing_grp", None); bpy.context.scene.collection.objects.link(wg); wg.location = (0.13, 0, 1.37)
        bpy.context.view_layer.update()
        for o in wparts:
            if o.parent is None: mw = o.matrix_world.copy(); o.parent = wg; o.matrix_world = mw
        new += [wg]
    root = bpy.data.objects.new("fk8root", None); bpy.context.scene.collection.objects.link(root)
    for o in new:
        if o.parent is None: o.parent = root
    veh = bpy.data.objects.new("veh", None); bpy.context.scene.collection.objects.link(veh)
    root.parent = veh; root.rotation_euler = (0, 0, R(-90)); root.location = (0, HALF, 0)
    return veh, wg

def seethrough(m):
    """Make the body shader's glass see-through (for cabin shots)."""
    nt = m.node_tree; mix = [n for n in nt.nodes if n.type == "MIX_SHADER"][0]
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); gl = nt.nodes.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.05
    m2 = nt.nodes.new("ShaderNodeMixShader"); m2.inputs[0].default_value = 0.12; nt.links.new(tr.outputs[0], m2.inputs[1]); nt.links.new(gl.outputs[0], m2.inputs[2])
    nt.links.new(m2.outputs[0], mix.inputs[2])

def overlay(cam, png, lens, dist=0.03, name="ov"):
    hw = dist * 18.0 / lens * 2.02
    return plane(name, hw, hw, alphamat(name + "m", TEX + png), (0, 0, -dist), parent=cam)

def visor(cam, lens):
    return overlay(cam, "visor.png", lens, 0.03, "visor")

def driveway_set():
    W.world(img="sky_day.png")
    plane("ground", 60, 60, mat("grass_l", (0.12, 0.35, 0.1)), (0, 0, -0.01))
    plane("drive", 6.5, 16, mat("walk_d", (0.62, 0.61, 0.58)), (0, 2.5, 0))
    box("house", (16, 7, 5), mat("sid_h", (0.8, 0.78, 0.7)), (0, -6.5, 0), base="z"); box("roof", (17, 8, 2.4), mat("roof_h", (0.25, 0.22, 0.22)), (0, -6.5, 5), base="z", taper=0.3)
    box("gdoor", (5.2, 0.1, 2.5), mat("door_g", (0.9, 0.9, 0.88)), (0, -2.95, 0), base="z")
    for x in (-6, 6): box(f"win{x}", (1.6, 0.1, 1.3), W._flat_mat(f"winm{x}", (0.1, 0.13, 0.18), 0.2), (x, -2.95, 1.6), base="z")
    box("fence", (0.1, 14, 1.4), mat("wood_f", (0.5, 0.35, 0.2)), (-4.5, 4, 0), base="z")

# ---------------------------------------------------------------- shot 1: alarm, already in the suit, cereal through the visor
def s1():
    W.room((0.42, 0.5, 0.66), (0.33, 0.22, 0.14), w=5, d=5, h=2.7, lamp=70)
    box("bed", (1.6, 2.1, 0.45), mat("blanket_b", (0.16, 0.2, 0.36)), (0, 0.6, 0), base="z"); box("pillow", (0.7, 0.35, 0.14), mat("pil_p", (0.85, 0.85, 0.8)), (0, 1.45, 0.45), base="z")
    box("stand", (0.5, 0.45, 0.55), mat("wood_s", (0.4, 0.25, 0.12)), (1.15, -0.2, 0), base="z")
    clk = box("clock", (0.24, 0.1, 0.12), W._flat_mat("clkb", (0.03, 0.03, 0.03), 0.4), (1.15, -0.2, 0.61), base="z")
    plane("clkface", 0.18, 0.07, W._flat_mat("clkd", (1.0, 0.1, 0.05), 0.5, emit=4), (0, -0.051, 0.06), rot=(R(90), 0, 0), parent=clk)
    poster = plane("poster", 1.0, 0.7, imgmat("posterm", TEX + "screen_signup.png"), (-1.2, 2.48, 1.6), rot=(R(90), 0, R(180)))  # an event flyer on the wall
    E = (0.15, -0.55, 1.22); rig, cam = rigcam(E, (1.15, -0.2, 0.62), lens=20); visor(cam, 20)
    # 1-14: slap the alarm (hand in the clock's space), 15-20: whip down to the bowl
    hs = ghand("hS", clk, (0.0, 0.25, 0.32), (R(-60), 0, R(180)), curls=FLAT, thumb=0.2)
    key(hs, 1, loc=(0.05, 0.35, 0.4), interp="LINEAR"); key(hs, 6, loc=(0.0, 0.02, 0.17), rot=(R(-88), 0, R(180)), interp="LINEAR"); key(hs, 9, loc=(0.0, 0.03, 0.2), interp="LINEAR"); key(hs, 13, loc=(0.1, 0.4, 0.5), interp="LINEAR")
    key(clk, 5, loc=(1.15, -0.2, 0.61), interp="LINEAR"); key(clk, 6, loc=(1.15, -0.2, 0.585), interp="LINEAR"); key(clk, 8, loc=(1.15, -0.2, 0.61), interp="LINEAR")
    vis(hs, 14, False); key(cam, 5, rot=(0, 0, 0), interp="LINEAR"); key(cam, 6, rot=(R(-2), R(1), 0), interp="LINEAR"); key(cam, 8, rot=(0, 0, 0), interp="LINEAR")
    key(rig, 1, rot=lookrot(E, (1.15, -0.2, 0.62)), interp="LINEAR"); key(rig, 13, rot=lookrot(E, (1.15, -0.2, 0.62)), interp="LINEAR"); key(rig, 19, rot=lookrot(E, (0.15, 0.1, 0.75)), interp="LINEAR")
    # bowl in the left hand, spoon in the right; the spoon keeps hitting the closed visor
    bowl = bpy.data.objects.new("bowlroot", None); bpy.context.scene.collection.objects.link(bowl); bowl.parent = cam; bowl.location = (-0.03, -0.1, -0.33); bowl.rotation_euler = (R(62), 0, 0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.08, depth=0.06); b = bpy.context.object; b.parent = bowl; b.data.materials.append(W._flat_mat("bowlm", (0.92, 0.92, 0.9), 0.3))
    plane("milk", 0.15, 0.15, W._flat_mat("milkm", (0.97, 0.96, 0.92), 0.2), (0, 0, 0.031), parent=bowl)
    rnd = random.Random(4); orange = W._flat_mat("loops", (0.95, 0.5, 0.1), 0.6)
    for i in range(14): box(f"loop{i}", (0.014, 0.014, 0.008), orange, (rnd.uniform(-0.05, 0.05), rnd.uniform(-0.05, 0.05), 0.034), rot=(0, 0, rnd.uniform(0, 3)), parent=bowl)
    hl = ghand("hL", bowl, (0.0, -0.07, -0.04), (R(-90), 0, 0), curls=(0.9, 0.9, 0.9, 0.9), thumb=0.4); vis(bowl, 1, False); vis(bowl, 16, True)
    hr = ghand("hR", cam, (0.12, -0.2, -0.36), (R(-50), 0, R(-15)), curls=FIST, thumb=0.9)
    box("spoon", (0.016, 0.16, 0.006), W._flat_mat("spoonm", (0.8, 0.8, 0.82), 0.15), (0.0, 0.13, -0.02), parent=hr)
    vis(hr, 1, False); vis(hr, 16, True)
    down, up = (0.05, -0.12, -0.33), (0.025, -0.02, -0.16)
    hits = [26, 36, 45, 53, 60]; prev = 16; key(hr, 16, loc=down, rot=(R(-50), 0, R(-15)), interp="LINEAR")
    milk = {}
    for i, hf in enumerate(hits):
        dip = max(prev + 2, hf - 5); key(hr, dip, loc=down, rot=(R(-50), 0, R(-15)), interp="LINEAR"); key(hr, hf, loc=up, rot=(R(-20), 0, R(-8)), interp="LINEAR"); key(hr, hf + 2, loc=(0.035, -0.05, -0.2), interp="LINEAR"); prev = hf + 2
        key(cam, hf - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, hf, rot=(R(2.5), R(-1), R(1.5)), interp="LINEAR"); key(cam, hf + 3, rot=(0, 0, 0), interp="LINEAR")
    for k in range(4):
        m = overlay(cam, f"milk_{k}.png", 20, 0.0295, f"milk{k}"); vis(m, 1, False); vis(m, hits[min(k, 4)], True)
        if k < 3: vis(m, hits[k + 1], False)
    for f, ln in ((1, 20), (16, 20), (19, 26)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

# ---------------------------------------------------------------- shot 2: track-day sign-up; thumb hovers, trembles, swipes away
def s2():
    rig, cam = rigcam((0, 0, 1.0), (0, 1.0, 0.47), lens=22); W.bunk(cam)
    ph, d = W.phone(cam, ["signup", "signup_hover", "cart"])
    ghand("hL", cam, (-0.03, -0.1, -0.17), (R(-6), R(180), R(4)), curls=FLAT, thumb=0.2)
    h = ghand("hR", cam, (0.06, -0.125, -0.1), (R(-38), R(4), R(32)), curls=POINT, thumb=0.9)
    rnd = random.Random(7); sched = [(1, "signup")]
    key(h, 1, loc=(0.09, -0.16, -0.09), interp="LINEAR")
    for f in range(6, 34, 2):          # hover and tremble just above REGISTER; the button lights when he nearly commits
        near = (f // 2) % 4 == 0
        key(h, f, loc=(0.058 + rnd.uniform(-0.003, 0.003), -0.124 + rnd.uniform(-0.003, 0.003), -0.098 + (0.006 if near else 0.0)), interp="LINEAR")
        sched.append((f, "signup_hover" if near else "signup"))
    key(h, 34, loc=(0.06, -0.12, -0.104), interp="LINEAR"); key(h, 39, loc=(-0.06, -0.11, -0.104), interp="LINEAR"); key(h, 44, loc=(0.0, -0.17, -0.09), interp="LINEAR")
    sched += [(34, "signup"), (38, "cart")]; swap(d, sched)
    for f, ln in ((1, 24), (30, 30), (36, 24)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

# ---------------------------------------------------------------- shot 3: TC wing in the cart; Confirm hammered ~10 times
def s3():
    rig, cam = rigcam((0, 0, 1.0), (0, 1.0, 0.47), lens=22); W.bunk(cam); ph, d = W.phone(cam, ["cart", "cart_pressed"])
    ghand("hL", cam, (-0.03, -0.1, -0.17), (R(-6), R(180), R(4)), curls=FLAT, thumb=0.2); h = ghand("hR", cam, (0.06, -0.125, -0.1), (R(-38), R(4), R(32)), curls=POINT, thumb=0.9)
    f = 4.0; gap = 6.0; sched = [(1, "cart")]; rnd = random.Random(2)
    while f < 45:
        fi = int(round(f)); sched += [(fi, "cart_pressed"), (fi + 2, "cart")]
        key(h, fi - 2, loc=(0.065, -0.135, -0.085), interp="LINEAR"); key(h, fi, loc=(0.045, -0.105, -0.115), interp="LINEAR"); key(h, fi + 1, loc=(0.06, -0.13, -0.09), interp="LINEAR")
        a = 0.004 + 0.012 * f / 46; key(ph, fi, loc=(-0.012 + rnd.uniform(-a, a), 0.012 - a, -0.135 - a), rot=(R(-6 + rnd.uniform(-4, 4)), R(3), R(4 + rnd.uniform(-5, 5))), interp="LINEAR"); key(ph, fi + 2, loc=(-0.012, 0.012, -0.135), rot=(R(-6), R(3), R(4)), interp="LINEAR")
        f += gap; gap = max(2.6, gap * 0.8)
    swap(d, sched); cam.data.lens = 22; cam.data.keyframe_insert("lens", frame=1); cam.data.lens = 27; cam.data.keyframe_insert("lens", frame=46)

# ---------------------------------------------------------------- shot 4: rips the box, chucks the wing, it lands on the hatch, he kisses the endplate
def s4():
    driveway_set(); veh, wg = fk8car(wing=True)
    card = mat("card_b", (0.55, 0.4, 0.24))
    E0 = Vector((-0.95, 4.05, 1.62)); look0 = Vector((0.0, 2.0, 0.9)); rig, cam = rigcam(tuple(E0), tuple(look0), lens=20)
    bxl = Vector((-0.45, 3.3, 0)); box("bigbox", (0.6, 1.9, 0.32), card, tuple(bxl), rot=(0, 0, R(-8)), base="z")
    box("bigbox_in", (0.52, 1.8, 0.02), W._flat_mat("boxin", (0.05, 0.035, 0.02)), (bxl.x, bxl.y, 0.33), rot=(0, 0, R(-8)))
    hr = ghand("hR", cam, (0.16, -0.36, -0.5), (R(-70), 0, R(-10)), curls=OPEN, thumb=-0.3); hl = ghand("hL", cam, (-0.16, -0.36, -0.5), (R(-70), 0, R(10)), curls=OPEN, thumb=-0.3, mirror=True)
    for i, f in enumerate(range(1, 13, 3)):   # ripping
        o = 0.05 + 0.2 * (i % 2)
        key(hr, f, loc=(0.05 + o, -0.3 + 0.1 * (i % 2), -0.5), rot=(R(-70 + 25 * (i % 2)), 0, R(-10 - 30 * (i % 2))), interp="LINEAR"); key(hl, f, loc=(-0.05 - o, -0.3 + 0.1 * (i % 2), -0.5), rot=(R(-70 + 25 * (i % 2)), 0, R(10 + 30 * (i % 2))), interp="LINEAR")
    rnd = random.Random(9)
    for i in range(12):
        p = plane(f"fl{i}", rnd.uniform(.12, .3), rnd.uniform(.1, .25), card, (0, -0.3, -0.7), parent=cam); a = rnd.uniform(0, 6.28); st = rnd.choice([2, 4, 6, 8])
        vis(p, 1, False); vis(p, st, True); key(p, st, loc=(rnd.uniform(-.1, .1), -0.32, -0.7), rot=(0, 0, 0), interp="LINEAR")
        key(p, st + 12, loc=(math.cos(a) * 0.9, 0.3 + math.sin(a) * 0.5, -rnd.uniform(0.7, 1.4)), rot=(rnd.uniform(0, 9), rnd.uniform(0, 9), rnd.uniform(0, 9)), interp="LINEAR"); vis(p, st + 13, False)
    # the wing group lives in the FK8 frame: its mounted pose is loc (0.13, 0, 1.37), rot 0, scale 1
    home = Vector((0.13, 0, 1.37)); dv = (look0 - E0).normalized()
    inbox = Vector(tofk(bxl + Vector((0, 0, 0.25)))); hold = Vector(tofk(E0 + dv * 0.95 + Vector((0, 0, -0.32)))); wind = Vector(tofk(E0 + dv * 0.7 + Vector((0, 0, -0.15))))
    mid = (wind + home) / 2 + Vector((0, 0, 1.0)); s0, land = 14, 33
    spin = (R(30), R(-720), R(-25))
    key(wg, 1, loc=tuple(inbox), rot=(0, 0, R(-8)), scale=(0.55,) * 3, interp="CONSTANT"); vis(wg, 1, False); vis(wg, s0, True)
    key(wg, s0, loc=tuple(inbox), rot=(0, 0, R(-8)), scale=(0.55,) * 3, interp="LINEAR"); key(wg, s0 + 5, loc=tuple(hold), rot=(R(-10), 0, R(15)), scale=(0.6,) * 3, interp="LINEAR")
    key(wg, s0 + 9, loc=tuple(wind), rot=(R(-15), 0, R(25)), scale=(0.6,) * 3, interp="LINEAR"); key(wg, s0 + 14, loc=tuple(mid), rot=spin, scale=(0.85,) * 3, interp="LINEAR")
    key(wg, land, loc=tuple(home + Vector((0, 0, -0.04))), rot=(0, 0, 0), scale=(1.06, 1.06, 0.9), interp="LINEAR"); key(wg, land + 3, loc=tuple(home), rot=(0, 0, 0), scale=(1, 1, 1), interp="LINEAR")
    key(veh, land - 1, loc=(0, 0, 0), interp="LINEAR"); key(veh, land + 1, loc=(0, 0, -0.035), interp="LINEAR"); key(veh, land + 5, loc=(0, 0, 0), interp="LINEAR")
    for h, sx in ((hr, 1), (hl, -1)):
        key(h, s0 - 1, loc=(0.2 * sx, -0.3, -0.5), rot=(R(-60), 0, R(-20 * sx)), interp="LINEAR"); key(h, s0 + 2, loc=(0.14 * sx, -0.46, -0.6), rot=(R(-95), 0, R(-10 * sx)), interp="LINEAR")
        key(h, s0 + 6, loc=(0.25 * sx, -0.22, -0.5), rot=(R(-50), R(30 * sx), R(-30 * sx)), interp="LINEAR"); key(h, s0 + 9, loc=(0.24 * sx, -0.1, -0.36), rot=(R(-30), R(30 * sx), R(-30 * sx)), interp="LINEAR")
        key(h, s0 + 13, loc=(0.12 * sx, -0.14, -0.72), rot=(R(-75), 0, R(-8 * sx)), interp="LINEAR")
        for j, f in enumerate(range(land + 2, 56, 4)): key(h, f, loc=(0.27 * sx, -0.05 + 0.07 * (j % 2), -0.44), rot=(R(-15), 0, R(-25 * sx)), interp="LINEAR")   # celebrating
    key(cam, land - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, land, rot=(R(1.6), R(-1.2), R(1.5)), interp="LINEAR"); key(cam, land + 3, rot=(0, 0, 0), interp="LINEAR")
    # 58-72: lunge to the right endplate (outside face at car x = -0.848) and kiss it; both hands land flat on it
    epc = Vector((-0.86, 2.15, 1.33)); K = Vector((-1.03, 2.17, 1.36))
    key(rig, 1, loc=tuple(E0), rot=lookrot(tuple(E0), tuple(look0)), interp="LINEAR"); key(rig, 56, loc=tuple(E0), rot=lookrot(tuple(E0), tuple(look0)), interp="BEZIER")
    key(rig, 68, loc=tuple(K), rot=lookrot(tuple(K), tuple(epc)), interp="BEZIER")
    for f, ln in ((1, 20), (56, 20), (68, 17)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    ep = bpy.data.objects.new("ep_space", None); bpy.context.scene.collection.objects.link(ep); ep.location = (-0.875, 2.15, 1.33)
    for nm, dz, mir in (("eR", -0.11, False), ("eL", 0.11, True)):
        fy = Vector((0, 0.35 if not mir else -0.35, 0.94)).normalized(); bz = Vector((-1, 0, 0)); fx = fy.cross(bz) if not mir else bz.cross(fy)
        g = ghand(nm, ep, (0, dz * 0.9, -0.09), Matrix((fx, fy, bz)).transposed().to_euler(), curls=FLAT, thumb=0.2, mirror=mir); vis(g, 1, False); vis(g, 66, True)
    for h in (hr, hl): vis(h, 64, False)
    shake(cam, 70, 95, 0.6, step=3, seed=4)

SHOTS = {1: s1, 2: s2, 3: s3, 4: s4}

if __name__ == "__main__":
    a = sys.argv[sys.argv.index("--") + 1:]; n = int(a[0]); out = a[1]; mode = a[2] if len(a) > 2 else "anim"; res = int(a[3]) if len(a) > 3 else 540; smp = int(a[4]) if len(a) > 4 else 10
    bpy.ops.wm.read_factory_settings(use_empty=True); SHOTS[n]()
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = smp; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 3
    sc.render.resolution_x = sc.render.resolution_y = res; sc.view_settings.view_transform = "Standard"; sc.render.fps = 30; sc.frame_start = 1; sc.frame_end = NF[n]
    sc.render.image_settings.file_format = "PNG"
    if mode == "anim":
        sc.render.filepath = f"{out}/s{n:02d}/"; bpy.ops.render.render(animation=True)
    else:
        for fr in mode.split(","):
            sc.frame_set(int(fr)); sc.render.filepath = f"{out}/s{n:02d}_f{int(fr):03d}.png"; bpy.ops.render.render(write_still=True)
