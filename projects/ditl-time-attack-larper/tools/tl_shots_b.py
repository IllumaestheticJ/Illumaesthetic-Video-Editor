"""Shots 5-15 of the track-guy short. blender -b --python tl_shots_b.py -- <shot> <outdir> [anim|f1,f2] [res] [samples]
Car faces -Y, centred; driver (LHD) on +X; driver eye EYE in car space."""
import bpy, sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tl_shots as T
import shots as W
from ditl_kit import box, plane, R, TEX, lowcar
from mathutils import Vector, Matrix

mat, imgmat, alphamat, key, vis, swap, shake, rigcam, lookrot, ghand, tofk = T.mat, T.imgmat, T.alphamat, T.key, T.vis, T.swap, T.shake, T.rigcam, T.lookrot, T.ghand, T.tofk
fm = W._flat_mat
OPEN, FIST, POINT, FLAT = T.OPEN, T.FIST, T.POINT, T.FLAT
EYE = (0.37, 0.23, 1.17)
NF = dict(T.NF); NF[8] = 72

def skin(name="s"): return fm(name, (0.84, 0.62, 0.48), 0.6)

def interior(m):
    """Cabin shots: see-through glass, and the shell's inside faces dark grey except where it is glass (the scan has no trim)."""
    nt = m.node_tree; body = nt.nodes["bodymix"]; fac = body.inputs[0].links[0].from_socket
    T.seethrough(m); out = nt.nodes["Material Output"]; src = out.inputs["Surface"].links[0].from_socket
    geo = nt.nodes.new("ShaderNodeNewGeometry"); dk = nt.nodes.new("ShaderNodeBsdfDiffuse"); dk.inputs["Color"].default_value = (0.035, 0.035, 0.04, 1)
    inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0; nt.links.new(fac, inv.inputs[1])
    bf = nt.nodes.new("ShaderNodeMath"); bf.operation = "MULTIPLY"; nt.links.new(geo.outputs["Backfacing"], bf.inputs[0]); nt.links.new(inv.outputs[0], bf.inputs[1])
    mx = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(bf.outputs[0], mx.inputs[0]); nt.links.new(src, mx.inputs[1]); nt.links.new(dk.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs["Surface"])

def car_in(wing=True):
    veh, wg = T.fk8car(wing=wing)
    interior(bpy.data.objects["fk8"].data.materials[0]); return veh, wg

def cabin(veh, screens=("timer_000",)):
    """Simple game cabin in car space: dash, door cards, wheel, shifter (6-speed manual), phone mount with the lap timer."""
    dk = fm("dash", (0.03, 0.03, 0.035), 0.6); gr = fm("trimg", (0.08, 0.08, 0.09), 0.7); red = fm("redstitch", (0.6, 0.03, 0.03), 0.6)
    box("dash", (1.5, 0.42, 0.24), dk, (0, -0.68, 0.8), base="z", parent=veh); box("hood_in", (1.5, 0.3, 0.02), dk, (0, -0.95, 1.03), parent=veh)
    for sx in (-1, 1): box(f"door{sx}", (0.06, 1.5, 0.45), gr, (sx * 0.72, 0.1, 0.55), base="z", parent=veh)
    box("tunnel", (0.26, 1.0, 0.25), dk, (0.0, 0.05, 0.42), base="z", parent=veh); box("floorin", (1.4, 2.2, 0.03), dk, (0, 0.2, 0.33), parent=veh)
    box("seatL", (0.5, 0.15, 0.7), red, (0.37, 0.55, 0.55), base="z", parent=veh); box("seatR", (0.5, 0.15, 0.7), red, (-0.37, 0.55, 0.55), base="z", parent=veh)
    col = box("column", (0.08, 0.32, 0.08), dk, (0.37, -0.42, 0.86), rot=(R(-22), 0, 0), parent=veh)
    whl = bpy.data.objects.new("wheelpivot", None); bpy.context.scene.collection.objects.link(whl); whl.parent = veh; whl.location = (0.37, -0.28, 0.93); whl.rotation_mode = "ZXY"; whl.rotation_euler = (R(68), 0, 0)   # Z spins the wheel on its own column (applied before the 68 deg tilt); + = right turn as the driver sees it
    bpy.ops.mesh.primitive_torus_add(major_radius=0.185, minor_radius=0.022, major_segments=28, minor_segments=8); tr = bpy.context.object; tr.parent = whl; tr.data.materials.append(dk)
    for a in (0, 120, 240): box(f"spoke{a}", (0.03, 0.17, 0.015), gr, (0, 0, 0), rot=(0, 0, R(a)), base="y", parent=whl)
    box("hubpad", (0.11, 0.08, 0.03), red, (0, 0, 0.005), parent=whl)
    stalk = box("stalk", (0.16, 0.02, 0.02), dk, (0.24, -0.33, 0.9), parent=veh)
    sh = bpy.data.objects.new("shifter", None); bpy.context.scene.collection.objects.link(sh); sh.parent = veh; sh.location = (0.05, -0.12, 0.66)
    box("shboot", (0.12, 0.12, 0.05), dk, (0, 0, 0), base="z", parent=sh); box("shrod", (0.018, 0.018, 0.14), gr, (0, 0, 0.04), base="z", parent=sh)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, segments=14, ring_count=8); kn = bpy.context.object; kn.parent = sh; kn.location = (0, 0, 0.19); kn.scale = (1, 1, 1.25); kn.data.materials.append(fm("knob", (0.75, 0.75, 0.78), 0.15))
    mpos = Vector((0.15, -0.3, 1.0)); mount = bpy.data.objects.new("mount", None); bpy.context.scene.collection.objects.link(mount); mount.parent = veh; mount.location = mpos
    mount.rotation_euler = (Vector(EYE) - mpos).to_track_quat("Z", "Y").to_euler()      # screen faces the driver, upright
    box("mountb", (0.085, 0.165, 0.012), dk, (0, 0, -0.007), parent=mount)
    ph = {s: plane("pscr_" + s, 0.075, 0.154, imgmat("pscrm_" + s, f"{TEX}{s}.png", emit=0.8), (0, 0, 0.0), parent=mount) for s in screens}
    lamp = bpy.data.objects.new("cabl", bpy.data.lights.new("cabl", "POINT")); lamp.data.energy = 18; lamp.data.shadow_soft_size = 0.4; bpy.context.scene.collection.objects.link(lamp); lamp.parent = veh; lamp.location = (0.2, 0.1, 1.25)
    return dict(wheel=whl, stalk=stalk, shifter=sh, mount=mount, phone=ph)

def wheelhands(whl, which=("R", "L")):
    rot = Matrix((Vector((-1, 0, 0)), Vector((0, 0, 1)), Vector((0, 1, 0)))).transposed().to_euler(); out = []
    for nm in which:
        sx = -1 if nm == "R" else 1
        out.append(ghand("h" + nm + "w", whl, (sx * 0.175, -0.02, -0.07), rot, curls=(1.1, 1.15, 1.15, 1.2), thumb=0.7, mirror=(nm == "L")))
    return out

def drivecam(veh, look=(0.3, -8, 1.0), lens=18):
    rig, cam = rigcam(EYE, look, lens=lens, parent=veh); return rig, cam

def garage_set(bar=False):
    W.world(sky=(0.3, 0.3, 0.32), strength=0.25, sun=None, img="sky_day.png")
    plane("pfloor", 40, 60, mat("walk_p", (0.5, 0.5, 0.5)), (0, 0, 0)); plane("pceil", 40, 60, mat("ceil_p", (0.55, 0.55, 0.55)), (0, 0, 2.5), rot=(R(180), 0, 0))
    yl = fm("pline", (0.9, 0.85, 0.7), 0.6)
    for i in range(-6, 7):
        plane(f"pl{i}", 0.1, 5.0, yl, (i * 2.6 + 1.3, -8, 0.004)); box(f"pil{i}", (0.5, 0.5, 2.5), mat("walk_pil", (0.6, 0.6, 0.6)), (i * 7.8, -12, 0), base="z")
    for j in range(-4, 5):
        l = bpy.data.objects.new(f"gl{j}", bpy.data.lights.new(f"gl{j}", "AREA")); l.data.energy = 60; l.data.size = 1.0; l.location = (0, j * 5.0, 2.45); bpy.context.scene.collection.objects.link(l)
        plane(f"glp{j}", 1.2, 0.2, fm(f"glpm{j}", (1, 1, 0.95), emit=3), (0, j * 5.0, 2.48), rot=(R(180), 0, 0))
        for x in (-6, 6): box(f"beam{j}{x}", (14, 0.3, 0.35), mat("walk_b", (0.55, 0.55, 0.55)), (x, j * 5.0, 2.15), base="z")

def bowling_pin(name, h=0.2):
    """Lathed bowling pin: wide belly, narrow neck, round head, two red neck stripes."""
    prof = [(0.0, 0.0), (0.022, 0.0), (0.031, 0.03), (0.034, 0.06), (0.029, 0.09), (0.017, 0.12), (0.0135, 0.135), (0.0165, 0.155), (0.0175, 0.17), (0.012, 0.188), (0.0, 0.195)]
    seg = 20; verts = []; faces = []
    for r_, z in prof:
        for k in range(seg): a = 2 * math.pi * k / seg; verts.append((r_ * math.cos(a) * h / 0.2, r_ * math.sin(a) * h / 0.2, z * h / 0.2))
    for i in range(len(prof) - 1):
        for k in range(seg): a0 = i * seg + k; faces.append((a0, i * seg + (k + 1) % seg, (i + 1) * seg + (k + 1) % seg, (i + 1) * seg + k))
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update(); o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o)
    me.materials.append(fm("pinw", (0.95, 0.95, 0.93), 0.3)); me.materials.append(fm("pinr", (0.8, 0.05, 0.05), 0.35))
    for pl in me.polygons:
        z = pl.center.z * 0.2 / h; pl.use_smooth = True
        if 0.122 < z < 0.128 or 0.14 < z < 0.147: pl.material_index = 1
    return o

# ---------------------------------------------------------------- 5: straightening a shelf of ATTENDEE trophies
def s5():
    W.room((0.62, 0.62, 0.6), (0.4, 0.4, 0.4), w=6, d=5, h=2.7, lamp=80)
    shelf = box("shelf", (1.8, 0.35, 0.04), mat("wood_sh", (0.45, 0.3, 0.15)), (0, 2.3, 1.2), base="z"); box("shelfback", (1.8, 0.03, 0.9), mat("wallm_b", (0.5, 0.52, 0.55)), (0, 2.47, 1.2), base="z")
    gold = fm("gold", (0.85, 0.62, 0.15), 0.25); blk = fm("tbase", (0.05, 0.05, 0.05), 0.4)
    names = ["plaque_attendee", "plaque_attendee", "plaque_bowling", "plaque_attendee", "plaque_attendee"]; tro = []; rnd = random.Random(3)
    for i, nm in enumerate(names):
        r = bpy.data.objects.new(f"tro{i}", None); bpy.context.scene.collection.objects.link(r); r.location = (-0.64 + i * 0.32, 2.3, 1.24); r.rotation_euler = (0, 0, R(rnd.choice([-28, 22, -18, 30, -25])))
        box(f"tb{i}", (0.16, 0.12, 0.1), blk, (0, 0, 0), base="z", parent=r); box(f"tc{i}", (0.05, 0.05, 0.16), gold, (0, 0, 0.1), base="z", parent=r)
        if "bowling" in nm:
            pin = bowling_pin(f"pin{i}"); pin.parent = r; pin.location = (0, 0, 0.26)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.032, segments=16, ring_count=10); ball = bpy.context.object; ball.parent = r; ball.location = (0.055, -0.02, 0.132)
            ball.data.materials.append(fm("ballm", (0.05, 0.05, 0.25), 0.15))
        else:
            bpy.ops.mesh.primitive_cone_add(vertices=14, radius1=0.04, radius2=0.09, depth=0.12); cup = bpy.context.object; cup.parent = r; cup.location = (0, 0, 0.32); cup.data.materials.append(gold)
        plane(f"pq{i}", 0.15, 0.056, imgmat(f"pqm{i}", f"{TEX}{nm}.png", emit=0.15), (0, -0.0605, 0.05), rot=(R(90), 0, 0), parent=r); tro.append(r)
    E = (0.0, 1.35, 1.48); rig, cam = rigcam(E, (-0.6, 2.3, 1.3), lens=24)
    h = ghand("hR", cam, (0.12, -0.15, -0.4), (R(-75), 0, R(-5)), curls=(0.5, 0.5, 0.6, 0.7), thumb=0.5)
    for i, r in enumerate(tro):    # each one turned to face front, reverently; camera pans along and reads the plaques
        f0 = 2 + i * 6; tgt = (-0.64 + i * 0.32, 2.3, 1.3)
        key(rig, f0, rot=lookrot(E, tgt), interp="BEZIER"); key(r, f0 + 2, rot=tuple(r.rotation_euler), interp="LINEAR"); key(r, f0 + 6, rot=(0, 0, 0), interp="BEZIER")
        key(h, f0, loc=(0.1, -0.12, -0.38), interp="LINEAR"); key(h, f0 + 3, loc=(0.06, -0.1, -0.5), interp="LINEAR"); key(h, f0 + 7, loc=(0.1, -0.14, -0.4), interp="LINEAR")
    # 32-48: pan back and push in on one ATTENDEE plaque (trophy 3) until it fills the frame
    pq = (0.32, 2.238, 1.29); Ec = (0.27, 1.72, 1.36); vis(h, 33, False)
    key(rig, 32, loc=E, rot=lookrot(E, (0.0, 2.3, 1.3)), interp="BEZIER"); key(rig, 46, loc=Ec, rot=lookrot(Ec, pq), interp="BEZIER"); key(rig, 48, loc=Ec, rot=lookrot(Ec, pq), interp="LINEAR")
    for f, ln in ((1, 30), (32, 30), (46, 60), (48, 62)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

# ---------------------------------------------------------------- 6: harness clicks, gloves, lap timer started
def s6():
    garage_set(); veh, wg = car_in(); c = cabin(veh, ("timer_000", "timer_001")); swap(c["phone"], [(1, "timer_000"), (40, "timer_001")])
    red = fm("harness", (0.75, 0.05, 0.05), 0.7); straps = []
    for sx in (-1, 1):
        s = box(f"strap{sx}", (0.05, 0.012, 0.55), red, (EYE[0] + sx * 0.12, 0.45, 1.05), rot=(R(-35), 0, 0), base="z", parent=veh); straps.append(s)
        key(s, 1, loc=(EYE[0] + sx * 0.16, 0.5, 1.12), rot=(R(-80), 0, R(sx * 10)), interp="LINEAR"); key(s, 18, loc=(EYE[0] + sx * 0.1, 0.2, 0.62), rot=(R(-5), 0, 0), interp="LINEAR")
    buckle = box("buckle", (0.09, 0.03, 0.09), fm("buck", (0.7, 0.7, 0.72), 0.2), (EYE[0], 0.12, 0.62), parent=veh)
    rig, cam = drivecam(veh, look=(EYE[0], -0.2, 0.62), lens=17)
    hr = ghand("hR", veh, (EYE[0] - 0.15, 0.3, 1.0), (R(200), 0, 0), curls=FIST, thumb=0.9); hl = ghand("hL", veh, (EYE[0] + 0.15, 0.3, 1.0), (R(200), 0, 0), curls=FIST, thumb=0.9, mirror=True)
    for h, sx in ((hr, -1), (hl, 1)):
        key(h, 1, loc=(EYE[0] + sx * 0.18, 0.35, 1.15), rot=(R(160), 0, 0), interp="LINEAR"); key(h, 18, loc=(EYE[0] + sx * 0.08, 0.05, 0.66), rot=(R(200), 0, 0), interp="LINEAR")
    key(cam, 21, rot=(0, 0, 0), interp="LINEAR"); key(cam, 22, rot=(R(-2), 0, R(1)), interp="LINEAR"); key(cam, 25, rot=(0, 0, 0), interp="LINEAR")   # CLICK
    key(rig, 1, rot=lookrot(EYE, (EYE[0], -0.2, 0.62)), interp="BEZIER"); key(rig, 26, rot=lookrot(EYE, (EYE[0], -0.2, 0.62)), interp="BEZIER"); key(rig, 33, rot=lookrot(EYE, (0.1, -0.52, 1.0)), interp="BEZIER")
    vis(hl, 30, False); key(hr, 26, loc=(EYE[0] - 0.08, 0.05, 0.66), rot=(R(200), 0, 0), interp="LINEAR")
    hp = ghand("hP", veh, (0.16, -0.25, 0.95), (R(70), 0, R(170)), curls=POINT, thumb=0.9); vis(hp, 1, False); vis(hp, 30, True); vis(hr, 30, False)
    key(hp, 30, loc=(0.25, -0.15, 0.85), interp="LINEAR"); key(hp, 37, loc=(0.12, -0.38, 0.98), interp="LINEAR"); key(hp, 40, loc=(0.1, -0.44, 1.0), interp="LINEAR"); key(hp, 46, loc=(0.25, -0.2, 0.86), interp="LINEAR")
    for f, ln in ((1, 17), (30, 17), (36, 28)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

def timer_swaps(c, f0, f1, step, start=1):
    sched = []; t = start
    for f in range(f0, f1, step): sched.append((f, f"timer_{t:03d}")); t += 1
    swap(c["phone"], sched)

# ---------------------------------------------------------------- 7: school zone; the lap timer runs at walking pace; crossing guard stares
def s7():
    W.road(); veh, wg = car_in(); c = cabin(veh, tuple(f"timer_{i:03d}" for i in range(3, 7))); timer_swaps(c, 1, 48, 12, 3)
    for y in (-14, -40):
        box(f"post{y}", (0.08, 0.08, 2.2), fm("postm", (0.6, 0.6, 0.6)), (-5.6, y, 0), base="z"); plane(f"ss{y}", 1.4, 0.47, imgmat(f"ssm{y}", TEX + "sign_school.png"), (-5.6, y + 0.05, 2.2), rot=(R(90), 0, 0))
    p, head, fd = W.person("guard", "guard", (1.4, -5.6, 0.78), 0, skin("gsk"), fm("vest", (0.95, 0.55, 0.05), 0.6), fm("ghair", (0.35, 0.25, 0.15)), ["flat", "blank"], bun=True)
    p.rotation_euler = (0, 0, R(180)); swap(fd, [(1, "flat"), (30, "blank"), (34, "flat")])   # in the road, facing the car
    for sx in (-1, 1): box(f"gleg{sx}", (0.15, 0.17, 0.8), fm("gpants", (0.1, 0.12, 0.25), 0.7), (sx * 0.11, 0, -0.8), base="z", parent=p)
    sp = box("stoppole", (0.04, 0.04, 1.5), fm("pole", (0.7, 0.7, 0.7)), (0.3, 0, -0.4), base="z", parent=p); plane("stopsign", 0.5, 0.5, imgmat("stopm", TEX + "sign_stop.png"), (0, -0.03, 1.4), rot=(R(90), 0, 0), parent=sp)
    key(veh, 1, loc=(1.7, 0, 0), interp="LINEAR"); key(veh, 47, loc=(1.7, -1.6, 0), interp="LINEAR")   # walking pace
    rig, cam = drivecam(veh, look=(-3, -9, 1.2), lens=17)
    key(rig, 1, rot=lookrot(EYE, (0.2, -8, 1.0)), interp="BEZIER"); key(rig, 12, rot=lookrot(EYE, (0.2, -8, 1.0)), interp="BEZIER"); key(rig, 24, rot=lookrot(EYE, (-0.2, -6, 1.15)), interp="BEZIER")
    key(rig, 47, rot=lookrot(EYE, (-0.2, -4.6, 1.2)), interp="BEZIER")     # keeps staring at her as he creeps past
    for f, ln in ((1, 17), (20, 17), (44, 30)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    wheelhands(c["wheel"])
    shake(cam, 1, 47, 0.25, step=4, seed=7)

# ---------------------------------------------------------------- 8: speed bump, the lip scrapes, sparks. "Aero's working."
def s8():
    W.road(); veh, wg = T.fk8car(wing=True)
    box("bump", (6, 0.45, 0.07), fm("bumpm", (0.95, 0.8, 0.1), 0.6), (0, -2.0, 0), base="z")
    key(veh, 1, loc=(1.7, 2.0, 0), interp="LINEAR"); key(veh, 10, loc=(1.7, 0.2, 0), interp="LINEAR"); key(veh, 14, loc=(1.7, -0.4, 0.06), rot=(R(-2.5), 0, 0), interp="LINEAR")
    key(veh, 18, loc=(1.7, -0.8, 0.02), rot=(R(1.5), 0, 0), interp="LINEAR"); key(veh, 24, loc=(1.7, -1.1, 0), rot=(0, 0, 0), interp="LINEAR"); key(veh, 60, loc=(1.7, -1.3, 0), interp="LINEAR")
    rig, cam = rigcam((0.2, -5.2, 0.32), (1.7, -1.5, 0.3), lens=22)
    sprk = fm("spark", (1.0, 0.55, 0.1), 0.5, emit=12); rnd = random.Random(8)
    for i in range(26):
        sp = box(f"sp{i}", (0.012, 0.05, 0.012), sprk, (1.7 + rnd.uniform(-0.6, 0.6), -2.0, 0.08))
        st = rnd.randint(11, 18); vis(sp, 1, False); vis(sp, st, True); vis(sp, st + 6, False)
        key(sp, st, loc=(1.7 + rnd.uniform(-0.6, 0.6), -2.1, 0.08), interp="LINEAR"); key(sp, st + 6, loc=(1.7 + rnd.uniform(-1.4, 1.4), -2.6 - rnd.uniform(0, 1.6), rnd.uniform(0.05, 0.5)), rot=(rnd.uniform(0, 6), 0, rnd.uniform(0, 6)), interp="LINEAR")
    shake(cam, 12, 22, 1.2, seed=8)
    for f, ln in ((1, 22), (24, 22), (58, 30)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

# ---------------------------------------------------------------- 9: roundabout; sawing at the wheel, heel-toe, a cyclist overtakes
def s9():
    W.road(); bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=4.0, depth=0.25, location=(0, -16, 0.12)); isl = bpy.context.object; isl.data.materials.append(mat("grass_i", (0.12, 0.35, 0.1)))
    veh, wg = car_in(); c = cabin(veh, ("timer_041",))
    # into the roundabout: a right flick in, then left around it; the wheel follows the heading
    key(veh, 1, loc=(1.7, 0, 0), rot=(0, 0, 0), interp="BEZIER"); key(veh, 16, loc=(1.75, -0.7, 0), rot=(0, 0, R(-5)), interp="BEZIER"); key(veh, 48, loc=(1.9, -2.2, 0), rot=(0, 0, R(6)), interp="BEZIER")
    rig, cam = drivecam(veh, look=(0.3, -8, 1.0), lens=17)
    for f, th in ((1, 0), (8, 30), (16, 10), (26, -45), (40, -40), (48, -30)): key(c["wheel"], f, rot=(R(68), 0, R(th)), interp="BEZIER")
    wheelhands(c["wheel"])
    cy = bpy.data.objects.new("cyc", None); bpy.context.scene.collection.objects.link(cy)
    p, head, fd = W.person("cyclist", "cyclist", (0, 0, 0.42), 0, skin("csk"), fm("jersey", (0.1, 0.6, 0.3), 0.5), fm("chair", (0.1, 0.08, 0.05)), ["flat"]); p.parent = cy; p.rotation_euler = (R(-20), 0, 0)
    for yy in (-0.5, 0.5):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.33, minor_radius=0.025, location=(0, yy, 0.35), rotation=(0, R(90), 0)); w_ = bpy.context.object; w_.parent = cy; w_.data.materials.append(fm("biket", (0.02, 0.02, 0.02)))
    box("frame", (0.04, 1.0, 0.05), fm("bikef", (0.8, 0.1, 0.1)), (0, 0, 0.6), parent=cy)
    cy.scale = (1.15,) * 3
    key(cy, 1, loc=(0.0, 2.5, 0), interp="LINEAR"); key(cy, 20, loc=(0.1, -2.6, 0), interp="LINEAR"); key(cy, 48, loc=(1.4, -8.5, 0), interp="LINEAR")   # overtakes on the right, cuts in ahead
    key(rig, 1, rot=lookrot(EYE, (0.3, -8, 1.0)), interp="BEZIER"); key(rig, 12, rot=lookrot(EYE, (-1.4, -3.5, 1.05)), interp="BEZIER"); key(rig, 26, rot=lookrot(EYE, (-0.6, -6, 1.05)), interp="BEZIER"); key(rig, 46, rot=lookrot(EYE, (0.2, -8, 1.05)), interp="BEZIER")
    shake(cam, 1, 48, 0.7, step=2, seed=9)
    for f, ln in ((1, 17), (18, 17), (34, 26)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)   # punch in on the cyclist pulling away

# ---------------------------------------------------------------- 10: office car park; the wing clips the height bar (bonk)
def s10():
    garage_set(); veh, wg = T.fk8car(wing=True)
    bar = bpy.data.objects.new("barpiv", None); bpy.context.scene.collection.objects.link(bar); bar.location = (0, -1.0, 2.35)
    box("bar", (3.2, 0.12, 0.12), fm("bary", (0.95, 0.75, 0.05), 0.5), (0, 0, -0.93), parent=bar)
    for sx in (-1, 1): box(f"ch{sx}", (0.02, 0.02, 0.9), fm("chain", (0.2, 0.2, 0.2)), (sx * 1.5, 0, -0.45), parent=bar)
    plane("clr", 1.6, 0.3, imgmat("clrm", TEX + "sign_clear.png"), (0, -0.065, -0.93), rot=(R(90), 0, 0), parent=bar)
    # wing rear edge is at car y = +2.28 - ... ; the element's top passes the bar when the car's rear axle area reaches it
    key(veh, 1, loc=(0, 3.2, 0), interp="LINEAR"); key(veh, 18, loc=(0, 1.2, 0), interp="LINEAR"); key(veh, 20, loc=(0, 1.05, 0), interp="LINEAR"); key(veh, 24, loc=(0, 1.25, 0), interp="LINEAR"); key(veh, 48, loc=(0, 1.25, 0), interp="LINEAR")
    for f, rx in ((19, 0), (20, 22), (25, -14), (30, 9), (36, -5), (42, 2), (48, 0)): key(bar, f, rot=(R(rx), 0, 0), interp="BEZIER")
    rig, cam = rigcam((-1.5, 6.4, 1.55), (0, 0.6, 1.4), lens=24); shake(cam, 20, 30, 1.0, seed=10)
    for f, ln in ((1, 24), (19, 24), (24, 34)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

# ---------------------------------------------------------------- 11: parked, window down. "Do you actually race?" "Next season." "You said that last season."
def s11():
    garage_set(); veh, wg = car_in(); c = cabin(veh, ("timer_none",))
    lowcar("nb", (3.2, 0.2, 0), 0, fm("nbb", (0.25, 0.3, 0.4), 0.4), fm("nbg", (0.03, 0.04, 0.05), 0.2), fm("nbt", (0.02, 0.02, 0.02)))
    p, head, fd = W.person("cw", "cowork", (1.55, 0.15, 0.48), R(-90), skin("cwsk"), fm("cwshirt", (0.75, 0.78, 0.82), 0.6), fm("cwhair", (0.15, 0.1, 0.06)), ["flat", "talk", "blank", "squish"])
    sched = [(1, "flat")]
    for a, b in ((5, 56), (100, 151)):
        for f in range(a, b, 4): sched += [(f, "talk"), (f + 2, "flat")]
    p.rotation_euler = (R(-35), 0, R(-90))   # leans down to the driver's window
    sched += [(152, "blank"), (60, "flat"), (70, "squish"), (76, "flat"), (100, "talk")]; swap(fd, sorted(sched))
    for f, rz in ((1, 0), (60, 4), (80, -3), (152, 0)): key(head, f, rot=(R(-12), 0, R(rz)), interp="CONSTANT")
    rig, cam = drivecam(veh, look=(1.1, 0.15, 1.12), lens=19)
    key(rig, 1, rot=lookrot(EYE, (1.1, 0.15, 1.12)), interp="BEZIER")
    for f in (66, 72, 80):  # nodding on "Next season."
        key(rig, f, rot=lookrot(EYE, (1.1, 0.15, 1.06)), interp="BEZIER"); key(rig, f + 3, rot=lookrot(EYE, (1.1, 0.15, 1.15)), interp="BEZIER")
    key(rig, 150, rot=lookrot(EYE, (1.1, 0.15, 1.12)), interp="BEZIER"); key(rig, 162, rot=lookrot(EYE, (1.1, 0.15, 1.13)), interp="LINEAR")
    for f, ln in ((1, 19), (95, 19), (150, 26), (162, 44)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    ghand("hL", veh, (0.7, 0.05, 0.98), (R(90), 0, R(-90)), curls=FLAT, thumb=0.2, mirror=True)   # elbow on the open window

# ---------------------------------------------------------------- 12: tyre check (full tread, sticker still on); writes the reading on his glove
def s12():
    garage_set(); veh, wg = T.fk8car(wing=True)
    wy = T.HALF - 0.938; wx = 0.797 + 0.15
    plane("sticker", 0.12, 0.18, fm("stk", (0.96, 0.96, 0.92), 0.5), (wx + 0.005, wy, 0.62), rot=(0, R(90), 0))
    rig, cam = rigcam((1.75, wy - 0.55, 0.62), (wx, wy, 0.42), lens=20)
    for nm, loc, en in (("k12", (1.6, wy - 1.2, 1.6), 60), ("f12", (2.4, wy + 0.6, 1.0), 25)):     # key and fill so the tyre and the glove read
        l = bpy.data.objects.new(nm, bpy.data.lights.new(nm, "AREA")); l.data.energy = en; l.data.size = 1.2; l.location = loc; bpy.context.scene.collection.objects.link(l)
        l.rotation_euler = (Vector((wx, wy, 0.4)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cl = bpy.data.objects.new("camfill", bpy.data.lights.new("camfill", "POINT")); cl.data.energy = 1.5; cl.data.shadow_soft_size = 0.3; cl.parent = cam; cl.location = (0.05, 0.1, 0.05); bpy.context.scene.collection.objects.link(cl)
    g = box("gauge", (0.05, 0.12, 0.05), fm("gaugem", (0.05, 0.05, 0.05), 0.3), (wx + 0.04, wy - 0.18, 0.2), rot=(0, 0, R(30)))
    hr = ghand("hR", g, (0, 0.08, 0.0), (R(-90), 0, 0), curls=FIST, thumb=0.8); T.cam_arms(cam, ["hR"])
    key(g, 1, loc=(wx + 0.3, wy - 0.4, 0.4), interp="LINEAR"); key(g, 8, loc=(wx + 0.04, wy - 0.18, 0.22), interp="LINEAR"); key(g, 22, loc=(wx + 0.04, wy - 0.18, 0.22), interp="LINEAR"); key(g, 27, loc=(wx + 0.25, wy + 0.5, 0.15), interp="LINEAR"); vis(g, 1, True); vis(g, 28, False)
    hl = ghand("hL", cam, (-0.02, -0.11, -0.22), (0, 0, R(25)), curls=FLAT, thumb=1.0, mirror=True)      # back of the glove facing the camera
    inks = {k: plane(f"ink{k}", 0.11, 0.055, alphamat(f"inkm{k}", f"{TEX}glove_inkw{k}.png"), (0, 0.05, 0.0175), parent=hl) for k in (1, 2, 3)}
    for o in inks.values(): o.scale = (-o.scale[0], o.scale[1], o.scale[2])   # undo the mirrored hand so the ink reads
    vis(hl, 1, False); vis(hl, 28, True); swap(inks, [(1, 0), (34, 1), (38, 2), (42, 3)])
    for o in inks.values(): vis(o, 1, False)
    vis(inks[1], 34, True); vis(inks[1], 38, False); vis(inks[2], 38, True); vis(inks[2], 42, False); vis(inks[3], 42, True)
    pen = ghand("hW", cam, (0.1, -0.06, -0.18), (R(-70), 0, R(30)), curls=FIST, thumb=0.9, hold="pen"); vis(pen, 1, False); vis(pen, 30, True)
    for f in range(30, 47, 2): key(pen, f, loc=(0.088 + 0.007 * ((f - 30) / 2), -0.06 + 0.006 * ((f // 2) % 2), -0.18), interp="LINEAR")
    key(rig, 1, rot=lookrot((1.75, wy - 0.55, 0.62), (wx, wy, 0.42)), interp="BEZIER"); key(rig, 26, rot=lookrot((1.75, wy - 0.55, 0.62), (wx, wy, 0.42)), interp="BEZIER")

# ---------------------------------------------------------------- 13: weather app shows one cloud; gasp; blanket over the wing
def s13():
    T.driveway_set(); veh, wg = T.fk8car(wing=True)
    E = (-0.9, 4.3, 1.62); rig, cam = rigcam(E, (0.0, 2.0, 0.9), lens=20)
    ph, d = W.phone(cam, ["weather"]); key(ph, 1, loc=(-0.012, 0.012, -0.135), interp="LINEAR"); key(ph, 18, loc=(-0.012, 0.012, -0.135), interp="LINEAR"); key(ph, 24, loc=(-0.012, -0.25, -0.135), interp="LINEAR")
    hp = ghand("hL", cam, (-0.03, -0.17, -0.17), (R(-6), R(180), R(4)), curls=FLAT, thumb=0.2); key(hp, 18, loc=(-0.03, -0.17, -0.17), interp="LINEAR"); key(hp, 24, loc=(-0.03, -0.45, -0.17), interp="LINEAR")
    key(cam, 15, rot=(0, 0, 0), interp="LINEAR"); key(cam, 16, rot=(R(4), 0, R(-2)), interp="LINEAR"); key(cam, 20, rot=(0, 0, 0), interp="LINEAR")     # gasp
    bl = box("blanket", (1.85, 0.5, 0.02), mat("blanket_w", (0.5, 0.15, 0.12)), (0, 2.15, 1.47))
    vis(bl, 1, False); vis(bl, 26, True); key(bl, 26, loc=(-0.6, 3.6, 1.4), rot=(R(40), R(30), R(70)), scale=(0.4, 0.4, 1), interp="LINEAR"); key(bl, 36, loc=(0, 2.15, 1.5), rot=(R(-6), 0, 0), scale=(1.05, 1.1, 1), interp="LINEAR"); key(bl, 40, loc=(0, 2.15, 1.47), rot=(0, 0, 0), scale=(1, 1, 1), interp="LINEAR")
    for sx in (-1, 1): s = box(f"drape{sx}", (0.02, 0.5, 0.25), mat("blanket_d", (0.5, 0.15, 0.12)), (sx * 0.93, 2.15, 1.35)); vis(s, 1, False); vis(s, 38, True)
    for f, ln in ((1, 26), (18, 26), (24, 20)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

# ---------------------------------------------------------------- 14: track gate; cars howl past; indicator; U-turn
def s14():
    W.road(); veh, wg = car_in(); c = cabin(veh, ("timer_none",))
    for sx in (-1, 1): box(f"gp{sx}", (0.25, 0.25, 1.4), fm("gpm", (0.3, 0.3, 0.32)), (sx * 4.5, -12, 0), base="z")
    boom = box("boom", (8.8, 0.1, 0.1), fm("boomm", (0.95, 0.95, 0.95), 0.5), (0, -12, 1.1)); plane("tsign", 4.0, 0.6, imgmat("tsm", TEX + "sign_track.png"), (0, -12.2, 2.6), rot=(R(90), 0, 0))
    box("tsignpost", (8.8, 0.15, 0.15), fm("gpm2", (0.3, 0.3, 0.32)), (0, -12.1, 2.25), base="z")
    for sx in (-1, 1): box(f"fence{sx}", (40, 0.05, 1.8), fm("fencem", (0.55, 0.57, 0.6), 0.4), (sx * 25.5, -14, 0), base="z")
    plane("track", 200, 12, mat("road_t", (0.1, 0.1, 0.1)), (0, -22, 0.02))
    cols = [(0.9, 0.1, 0.1), (0.1, 0.3, 0.9), (0.95, 0.75, 0.05), (0.1, 0.1, 0.1)]; gl = fm("tcg", (0.03, 0.04, 0.05), 0.2); ti = fm("tct", (0.02, 0.02, 0.02))
    for i, (f0, col) in enumerate(zip((2, 14, 27, 38), cols)):
        lc = lowcar(f"tc{i}", (-40, -20 - (i % 2) * 3, 0), R(90), fm(f"tcb{i}", col, 0.3), gl, ti); key(lc, f0, loc=(-40, -20 - (i % 2) * 3, 0), interp="LINEAR"); key(lc, f0 + 14, loc=(40, -20 - (i % 2) * 3, 0), interp="LINEAR")
    p, head, fd = W.person("marshal", "marshal", (-3.6, -11.2, 0), R(-20), skin("msk"), fm("vest2", (0.95, 0.55, 0.05), 0.6), fm("mhair", (0.05, 0.05, 0.05)), ["grin", "flat", "blank"])
    swap(fd, [(1, "grin"), (52, "flat"), (66, "blank")])
    a, f_ = W.arm("ma", p, 1, skin("msk2"), fm("vest3", (0.95, 0.55, 0.05), 0.6), up=60, fwd=180, bend=10)
    for f in range(1, 50, 5): key(a, f, rot=(R(55 + 30 * ((f // 5) % 2)), 0, R(-90)), interp="LINEAR")   # waves out to the side, clear of the head
    key(veh, 1, loc=(1.7, 0, 0), interp="LINEAR"); key(veh, 28, loc=(1.7, -3.0, 0), interp="BEZIER"); key(veh, 46, loc=(1.7, -3.4, 0), interp="BEZIER")
    key(veh, 47, rot=(0, 0, 0), interp="BEZIER"); key(veh, 81, loc=(-1.4, -2.0, 0), rot=(0, 0, R(180)), interp="BEZIER")
    rig, cam = drivecam(veh, look=(0.2, -9, 1.2), lens=17)
    hl = ghand("hL", veh, (0.3, -0.25, 0.9), (R(70), 0, R(190)), curls=FIST, thumb=0.6, mirror=True)
    key(hl, 1, loc=(0.52, -0.3, 0.95), interp="LINEAR"); key(hl, 40, loc=(0.52, -0.3, 0.95), interp="LINEAR"); key(hl, 44, loc=(0.3, -0.33, 0.93), interp="LINEAR"); key(hl, 47, loc=(0.32, -0.33, 0.86), interp="LINEAR")
    key(c["stalk"], 45, rot=(0, 0, 0), interp="CONSTANT"); key(c["stalk"], 47, rot=(R(-14), 0, 0), interp="CONSTANT")
    blink = box("blinkL", (0.03, 0.01, 0.02), fm("blinkm", (0.1, 1.0, 0.2), 0.5, emit=8), (0.42, -0.56, 0.96), parent=veh)
    sched = [(1, False)]
    for f in range(47, 82, 8): sched += [(f, True), (f + 4, False)]
    for f, on in sched: vis(blink, f, on)
    wheelhands(c["wheel"], ("R",))
    for f, th in ((1, 0), (46, 0), (54, -150), (74, -150), (81, -60)): key(c["wheel"], f, rot=(R(68), 0, R(th)), interp="BEZIER")   # full left lock for the U-turn, unwinding at the end

# ---------------------------------------------------------------- 15: the mirror: his face for the first time, helmet on; mouth revs and rows the 6-speed; timer --:--
def s15():
    garage_set(); veh, wg = car_in(); c = cabin(veh, ("timer_none",))
    mc = Vector((0.03, -0.33, 1.27)); fr = bpy.data.objects.new("mir", None); bpy.context.scene.collection.objects.link(fr); fr.parent = veh; fr.location = mc; fr.rotation_euler = (R(-5), 0, R(-25))
    MW, MH = 0.27, 0.08; blk = fm("mirf", (0.02, 0.02, 0.02))
    plane("mir_bg", MW, MH, imgmat("mirbg", TEX + "mirror_bg.png", emit=0.9), (0, 0, 0), rot=(R(90), 0, R(180)), parent=fr)
    for nm, sz, lc in (("rt", (MW + 0.02, 0.03, 0.012), (0, 0.004, MH / 2 + 0.004)), ("rb", (MW + 0.02, 0.03, 0.012), (0, 0.004, -MH / 2 - 0.004)), ("rl", (0.012, 0.03, MH + 0.02), (-MW / 2 - 0.004, 0.004, 0)), ("rr", (0.012, 0.03, MH + 0.02), (MW / 2 + 0.004, 0.004, 0))): box("mir_" + nm, sz, blk, lc, parent=fr)
    box("mir_house", (MW + 0.02, 0.03, MH + 0.02), blk, (0, -0.018, 0), parent=fr); box("mir_arm", (0.02, 0.02, 0.06), blk, (0, -0.01, MH / 2 + 0.03), base="z", parent=fr)
    hs = fm("tgface", (0.84, 0.62, 0.48), 0.6, emit=0.25); sc_ = 0.15
    p, head, fd = W.person("him", "tg", (0, 0, 0), 0, hs, fm("suit_m", (0.06, 0.1, 0.45), 0.6, emit=0.2), fm("hhair", (0.02, 0.02, 0.02)), ["blank", "talk", "squish", "flat", "horror"], hair_h=0.02)
    p.parent = fr; p.rotation_euler = (0, 0, R(180)); p.scale = (sc_, sc_ * 0.06, sc_); p.location = (0.0, 0.006, -(0.62 + 0.13) * sc_)
    for o in p.children:
        if o.name.endswith("_torso"): o.hide_render = True
    hel = fm("helmet", (0.95, 0.95, 0.95), 0.25, emit=0.25); red = fm("helred", (0.8, 0.05, 0.05), 0.3, emit=0.25)
    box("hel_top", (0.29, 0.29, 0.08), hel, (0, 0.0, 0.27), parent=head, base="z"); box("hel_stripe", (0.06, 0.3, 0.085), red, (0, 0.0, 0.272), parent=head, base="z")
    for sx in (-1, 1): box(f"hel_side{sx}", (0.05, 0.29, 0.34), hel, (sx * 0.135, 0.02, 0.0), parent=head, base="z")
    box("hel_chin", (0.28, 0.06, 0.07), hel, (0, -0.13, -0.02), parent=head, base="z")
    for e_, fpl in fd.items(): fpl.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.0
    sched = [(1, "blank")]
    for f in range(8, 90, 3): sched += [(f, "squish" if (f // 3) % 2 else "talk")]     # mouth-revving "braaap"
    sched += [(90, "flat"), (98, "blank"), (136, "talk"), (139, "flat"), (142, "talk"), (146, "flat"), (160, "blank")]; swap(fd, sched)
    for f, rz in ((1, 0), (30, 4), (50, -4), (70, 3), (90, 0)): key(head, f, rot=(0, R(rz), 0), interp="CONSTANT")
    a = EYE; b = (0.28, 0.12, 1.22); rig, cam = rigcam(a, (0.1, -0.75, 0.95), lens=19, parent=veh); vz = T.visor(cam, 19)
    key(rig, 1, loc=a, rot=lookrot(a, (0.1, -0.6, 0.8)), interp="BEZIER"); key(rig, 85, loc=a, rot=lookrot(a, (0.1, -0.6, 0.82)), interp="BEZIER"); key(rig, 100, loc=a, rot=lookrot(a, tuple(mc)), interp="BEZIER"); key(rig, 180, loc=b, rot=lookrot(b, tuple(mc), -2), interp="LINEAR")
    for f, ln in ((1, 19), (85, 19), (100, 30), (180, 70)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    T.follow_lens(19, [vz], ((1, 19), (85, 19), (100, 30), (180, 70)))
    # right hand rows the 6-speed through the gears while parked (H pattern), left hand on the wheel
    sh = c["shifter"]; ghand("hR", sh, (0, -0.02, 0.24), (R(170), 0, R(180)), curls=(1.0, 1.0, 1.1, 1.2), thumb=0.7)
    gates = [(-12, 14), (-12, -14), (0, 14), (0, -14), (12, 14), (12, -14)]
    f = 8
    for rep in range(2):
        for gx, gy in gates:
            key(sh, f, rot=(R(gy), R(gx), 0), interp="LINEAR"); key(sh, f + 3, rot=(R(gy), R(gx), 0), interp="LINEAR"); f += 6
    key(sh, f, rot=(0, 0, 0), interp="LINEAR")
    wheelhands(c["wheel"], ("L",))
    shake(cam, 8, 85, 0.5, step=3, seed=15)

def pov_arms(veh_name="veh"):
    """Every POV hand inside the car aims its forearm (hand local -Y) at the driver's matching shoulder, every frame,
    whatever it holds (wheel, shifter, stalk, phone, harness). Keeps arms coming out of the person, not the dash."""
    veh = bpy.data.objects.get(veh_name)
    if veh is None: return
    sh = {}
    for side, x in (("R", EYE[0] - 0.2), ("L", EYE[0] + 0.2)):
        e = bpy.data.objects.new("shoulder_" + side, None); bpy.context.scene.collection.objects.link(e); e.parent = veh; e.location = (x, EYE[1] + 0.13, EYE[2] - 0.19); sh[side] = e
    for o in bpy.data.objects:
        if o.type != "EMPTY" or not any(c.name == o.name + "_palm" for c in o.children): continue
        q = o.parent; inside = False
        while q:
            if q is veh: inside = True
            q = q.parent
        if not inside: continue
        side = "L" if o.name.startswith("hL") or o.name.endswith("L") else "R"
        c = o.constraints.new("DAMPED_TRACK"); c.target = sh[side]; c.track_axis = "TRACK_NEGATIVE_Y"

POV_CABIN = (6, 7, 9, 11, 14, 15)

SHOTS = {5: s5, 6: s6, 7: s7, 8: s8, 9: s9, 10: s10, 11: s11, 12: s12, 13: s13, 14: s14, 15: s15}

if __name__ == "__main__":
    a = sys.argv[sys.argv.index("--") + 1:]; n = int(a[0]); out = a[1]; mode = a[2] if len(a) > 2 else "anim"; res = int(a[3]) if len(a) > 3 else 540; smp = int(a[4]) if len(a) > 4 else 10
    bpy.ops.wm.read_factory_settings(use_empty=True); SHOTS[n]()
    if n in POV_CABIN: pov_arms()
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = smp; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 3
    sc.render.resolution_x = sc.render.resolution_y = res; sc.view_settings.view_transform = "Standard"; sc.render.fps = 30; sc.frame_start = 1; sc.frame_end = NF[n]
    sc.render.image_settings.file_format = "PNG"
    if mode == "anim":
        sc.render.filepath = f"{out}/s{n:02d}/"; bpy.ops.render.render(animation=True)
    else:
        for fr in mode.split(","):
            sc.frame_set(int(fr)); sc.render.filepath = f"{out}/s{n:02d}_f{int(fr):03d}.png"; bpy.ops.render.render(write_still=True)
