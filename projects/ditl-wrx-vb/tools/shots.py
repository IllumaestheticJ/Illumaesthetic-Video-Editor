"""All 16 shots of the DITL WRX short. blender -b --python shots.py -- <shot 1-16> <outdir> [still_frame|anim] [res] [samples]"""
import bpy, sys, math, random, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ditl_kit as k
from ditl_kit import mat, imgmat, procmat, box, plane, R, TEX
from mathutils import Vector

# ---- video-game textures: low-res tiles, Closest filtering, box-projected ----
_flat_mat = mat
def texmat(name, file, scale=1.0, tint=None, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = rough
    co = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (scale,) * 3
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(TEX + file, check_existing=True); t.interpolation = "Closest"; t.projection = "BOX"; t.projection_blend = 0.0
    nt.links.new(co.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], t.inputs["Vector"])
    if tint is None: nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    else:
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs[0].default_value = 1.0; mx.inputs[7].default_value = (*[min(1.0, c * 1.2) for c in tint], 1)
        nt.links.new(t.outputs["Color"], mx.inputs[6]); nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    return m
TEXMAP = {"walk": ("tx_concrete.png", 0.5, True), "grass": ("tx_grass.png", 0.35, False), "sid": ("tx_siding.png", 0.45, True), "roof": ("tx_shingle.png", 0.6, True), "wallm": ("tx_plaster.png", 0.5, True),
          "wall": ("tx_plaster.png", 0.5, True), "ceil": ("tx_plaster.png", 0.5, True), "blanket": ("tx_plaid.png", 1.2, False), "card": ("tx_cardboard.png", 1.5, False), "camo": ("tx_camo.png", 3.0, False),
          "dump": ("tx_metal.png", 1.0, True), "door": ("tx_metal.png", 1.0, True), "van_beige": ("tx_metal.png", 0.5, True), "lshirt": ("tx_fabric.png", 6, True), "polo": ("tx_fabric.png", 6, True), "mshirt": ("tx_fabric.png", 6, True),
          "kshirt": ("tx_fabric.png", 6, True), "htee": ("tx_camo.png", 3.0, False), "cabm": ("tx_metal.png", 1.0, True), "pil": ("tx_fabric.png", 5, True), "flag": ("tx_fabric.png", 5, True), "win": None}
def mat(name, col, rough=0.9, emit=0.0):
    if not emit:
        for kk, v in TEXMAP.items():
            if v and name.startswith(kk): return texmat(name, v[0], v[1], col if v[2] else None, rough)
    return _flat_mat(name, col, rough, emit)
def procmat(name, kind, c1, c2, scale=1.0):
    f, sc_, tint = {"asphalt": ("tx_asphalt.png", 0.4, None), "road": ("tx_asphalt.png", 0.4, None), "brick": ("tx_brick.png", 0.5, None), "wood": ("tx_wood.png", 1.2, None), "floor": ("tx_tile.png", 0.6, None)}.get(name, ("tx_carpet.png", 1.5, c2))
    return texmat(name, f, sc_, tint)
k.mat = mat; k.procmat = procmat
_world = k.world
def world(sky=(0.42, 0.62, 0.95), strength=1.0, sun=(3.5, 48, 35), img="sky_day.png"):
    _world(sky, strength, sun)
    if sun:
        nt = bpy.context.scene.world.node_tree; e = nt.nodes.new("ShaderNodeTexEnvironment"); e.image = bpy.data.images.load(TEX + img, check_existing=True); e.interpolation = "Closest"
        nt.links.new(e.outputs["Color"], nt.nodes["Background"].inputs[0]); nt.nodes["Background"].inputs[1].default_value = 1.0
k.world = world

WHEELGLB = "/home/user/epsilon-site/showroom/models/eps-toyota-supra-a90-v2.glb"
def realwheels(root, x, yf, yr, z=0.33, scale=1.0, glb=WHEELGLB):
    """Real modelled wheels (alloy + tyre) from a showroom model, placed at the given axles."""
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=glb); new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        if o.name.split(".")[0] in ("wheel_FL", "wheel_FR", "wheel_RL", "wheel_RR"):
            nm = o.name.split(".")[0]; mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw; o.parent = root
            o.location = ((x if nm[-1] == "L" else -x), (yf if nm[-2] == "F" else yr), z * scale); o.scale = (scale,) * 3; o.name = root.name + "_" + nm
        else: bpy.data.objects.remove(o)

NF = [65, 48, 47, 48, 47, 47, 95, 95, 47, 47, 95, 48, 47, 47, 79, 150]
OPEN, FIST, POINT, FLAT = (0.12, 0.06, 0.1, 0.22), (1.3, 1.35, 1.35, 1.4), (0.0, 1.3, 1.35, 1.4), (0.02, 0.0, 0.02, 0.05)

def key(o, f, loc=None, rot=None, scale=None, interp="BEZIER"):
    bpy.context.preferences.edit.keyframe_new_interpolation_type = interp
    if loc is not None: o.location = loc; o.keyframe_insert("location", frame=f)
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert("rotation_euler", frame=f)
    if scale is not None: o.scale = scale; o.keyframe_insert("scale", frame=f)

def vis(o, f, show):
    for x in [o] + list(o.children_recursive):
        x.hide_render = not show; x.keyframe_insert("hide_render", frame=f)

def swap(d, sched):
    for f, name in sched:
        for n, o in d.items(): vis(o, f, n == name)

def lookrot(loc, look, roll=0):
    e = (Vector(look) - Vector(loc)).to_track_quat("-Z", "Y").to_euler(); e.rotate_axis("Z", R(roll)); return tuple(e)

def rigcam(loc, look, lens=20, roll=0, parent=None):
    sc = bpy.context.scene; rig = bpy.data.objects.new("rig", None); sc.collection.objects.link(rig)
    rig.location = loc; rig.rotation_euler = lookrot(loc, look, roll); rig.parent = parent
    c = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(c); sc.camera = c; c.parent = rig
    c.data.lens = lens; c.data.sensor_width = 36; c.data.clip_start = 0.02; c.data.clip_end = 600
    return rig, c

def shake(cam, f0, f1, amp, step=2, seed=1):
    rnd = random.Random(seed)
    for f in range(f0, f1, step): key(cam, f, rot=(R(rnd.uniform(-amp, amp)), R(rnd.uniform(-amp, amp)), R(rnd.uniform(-amp, amp) * 0.6)), interp="LINEAR")
    key(cam, f1, rot=(0, 0, 0), interp="LINEAR")

def skinmat(name="skin_him", c1=(0.30, 0.165, 0.09), c2=(0.38, 0.22, 0.13)):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.5
    co = nt.nodes.new("ShaderNodeTexCoord"); t = nt.nodes.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = 55; t.inputs["Detail"].default_value = 6
    r = nt.nodes.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].color = (*c1, 1); r.color_ramp.elements[1].color = (*c2, 1); r.color_ramp.elements[0].position = 0.3; r.color_ramp.elements[1].position = 0.7
    nt.links.new(co.outputs["Object"], t.inputs["Vector"]); nt.links.new(t.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], b.inputs["Base Color"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.25; nt.links.new(t.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

def rnd_(o, w, seg=3):
    m = o.modifiers.new("bev", "BEVEL"); m.width = w; m.segments = seg
    for p in o.data.polygons: p.use_smooth = True
    return o

_S = {}
def S():
    if "s" not in _S: _S["s"] = skinmat(); _S["n"] = mat("nail", (0.62, 0.45, 0.36), 0.3); _S["p"] = mat("palmskin", (0.5, 0.31, 0.22), 0.55)
    return _S

def hand(name, parent, loc, rot, curls=OPEN, thumb=0.3, mirror=False, sleeve=None, hold=None):
    """Rounded 3D hand. Fingers along local +Y, back of hand +Z, forearm toward -Y."""
    s = S(); skin = s["s"]; root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    root.parent = parent; root.location = loc; root.rotation_euler = rot
    if mirror: root.scale = (-1, 1, 1)
    palm = rnd_(box(name + "_palm", (0.086, 0.098, 0.03), skin, parent=root, base="y", taper=1.1), 0.012, 4)
    rnd_(box(name + "_pad", (0.07, 0.08, 0.012), s["p"], loc=(0, 0.01, -0.012), parent=root, base="y"), 0.005)
    rnd_(box(name + "_wr", (0.062, 0.05, 0.04), skin, loc=(0, -0.04, 0), parent=root, base="y", taper=1.25), 0.014, 4)
    rnd_(box(name + "_arm", (0.085, 0.4, 0.07), skin, loc=(0, -0.44, 0), parent=root, base="y", taper=0.7), 0.024, 4)
    if sleeve: rnd_(box(name + "_slv", (0.11, 0.22, 0.095), sleeve, loc=(0, -0.6, 0), parent=root, base="y"), 0.02)
    xs = (-0.032, -0.0105, 0.011, 0.0315); ln = (0.04, 0.045, 0.042, 0.032)
    for i in range(4):
        c = curls[i]
        k1 = rnd_(box(f"{name}_k{i}", (0.021, 0.02, 0.024), skin, loc=(xs[i], 0.092, 0.002), parent=palm), 0.008)
        s1 = rnd_(box(f"{name}_f{i}a", (0.019, ln[i], 0.019), skin, loc=(xs[i], 0.098, 0), rot=(-c, 0, 0), parent=palm, base="y"), 0.007)
        s2 = rnd_(box(f"{name}_f{i}b", (0.018, ln[i] * 0.72, 0.017), skin, loc=(0, ln[i], 0), rot=(-c * 1.15, 0, 0), parent=s1, base="y"), 0.0065)
        s3 = rnd_(box(f"{name}_f{i}c", (0.0165, ln[i] * 0.6, 0.015), skin, loc=(0, ln[i] * 0.72, 0), rot=(-c * 0.9, 0, 0), parent=s2, base="y", taper=0.8), 0.006)
        rnd_(box(f"{name}_n{i}", (0.012, ln[i] * 0.34, 0.003), s["n"], loc=(0, ln[i] * 0.22, 0.0078), parent=s3, base="y"), 0.001, 2)
    t1 = rnd_(box(name + "_t1", (0.026, 0.05, 0.026), skin, loc=(-0.044, 0.018, -0.006), rot=(0, 0, R(50) - thumb), parent=palm, base="y"), 0.009)
    t2 = rnd_(box(name + "_t2", (0.022, 0.038, 0.02), skin, loc=(0, 0.05, 0), rot=(0, 0, -thumb), parent=t1, base="y", taper=0.8), 0.007)
    rnd_(box(name + "_tn", (0.014, 0.014, 0.003), s["n"], loc=(0, 0.02, 0.0105), parent=t2, base="y"), 0.001, 2)
    if hold == "vape":
        v = rnd_(box(name + "_vape", (0.03, 0.14, 0.022), mat("vape", (0.75, 0.08, 0.5), 0.25), loc=(0, 0.03, -0.035), rot=(0, 0, R(80)), parent=root), 0.006)
        box(name + "_vtip", (0.012, 0.03, 0.012), mat("vtip", (0.03, 0.03, 0.03), 0.3), loc=(0, 0.085, 0), parent=v)
    if hold == "pen":
        box(name + "_pen", (0.011, 0.011, 0.16), mat("pen", (0.05, 0.1, 0.6), 0.3), loc=(0.0, 0.07, -0.06), rot=(R(20), 0, 0), parent=root)
    return root

def person(name, who, loc, rz, skin, shirt, hair, faces, hair_h=0.12, bun=False, scale=1.0):
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root); root.location = loc; root.rotation_euler = (0, 0, rz); root.scale = (scale,) * 3
    box(name + "_torso", (0.46, 0.26, 0.56), shirt, parent=root, base="z", taper=1.15)
    box(name + "_neck", (0.1, 0.1, 0.08), skin, loc=(0, 0, 0.56), parent=root, base="z")
    head = box(name + "_head", (0.21, 0.22, 0.27), skin, loc=(0, 0, 0.62), parent=root, base="z", taper=1.12)
    box(name + "_hair", (0.25, 0.26, hair_h), hair, loc=(0, 0.012, 0.265), parent=head, base="z", taper=0.85)
    box(name + "_hairb", (0.25, 0.05, 0.2), hair, loc=(0, 0.125, 0.1), parent=head, base="z")
    if bun: box(name + "_bun", (0.16, 0.16, 0.14), hair, loc=(0, 0.02, 0.265 + hair_h), parent=head, base="z", taper=0.8)
    fd = {}
    for e in faces:
        fd[e] = plane(f"{name}_face_{e}", 0.21, 0.26, imgmat(f"{name}_fm_{e}", f"{TEX}face_{who}_{e}.png"), loc=(0, -0.1235, 0.135), rot=(R(90), 0, 0), parent=head)
    swap(fd, [(1, faces[0])])
    return root, head, fd

def arm(name, root, side, skin, shirt, up=0.0, fwd=0.0, bend=60):
    a = box(name + "_ua", (0.1, 0.3, 0.1), shirt, loc=(side * 0.27, 0, 0.47), rot=(R(up), 0, R(90) * side + R(fwd) * -side), parent=root, base="y", taper=0.85)
    f = box(name + "_fa", (0.085, 0.28, 0.085), skin, loc=(0, 0.3, 0), rot=(R(bend), 0, 0), parent=a, base="y", taper=0.9)
    box(name + "_hd", (0.1, 0.11, 0.04), skin, loc=(0, 0.28, 0), parent=f, base="y")
    return a, f

def alphamat(name, path):
    m = imgmat(name, path); nt = m.node_tree; nt.links.new(nt.nodes["Image Texture"].outputs["Alpha"], nt.nodes["Principled BSDF"].inputs["Alpha"]); return m

def glassmat(name="pane", a=0.08):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.6, 0.75, 0.85, 1); b.inputs["Alpha"].default_value = a; b.inputs["Roughness"].default_value = 0.05; return m

def phone(cam, screens, loc=(-0.012, 0.012, -0.135), rot=(R(-6), R(3), R(4))):
    ph = k.box("phone", (0.082, 0.168, 0.009), mat("phbody", (0.02, 0.02, 0.02), 0.3), loc, rot=rot, parent=cam)
    d = {s: plane("scr_" + s, 0.075, 0.154, imgmat("scrm_" + s, f"{TEX}screen_{s}.png", emit=0.7), (0, 0, 0.0052), parent=ph) for s in screens}
    swap(d, [(1, screens[0])]); return ph, d

def bunk(cam):
    k.world(sky=(0.02, 0.02, 0.04), strength=0.35, sun=None)
    box("bed", (2, 3, 0.4), mat("blanket", (0.14, 0.19, 0.11)), (0, 1.0, 0.25)); box("wall", (6, 0.2, 3), mat("wall", (0.3, 0.3, 0.27)), (0, 2.6, 1.5)); box("pillow", (0.7, 0.4, 0.15), mat("pil", (0.7, 0.7, 0.66)), (0.5, 1.6, 0.5))
    l = bpy.data.objects.new("pl", bpy.data.lights.new("pl", "AREA")); l.data.energy = 0.09; l.data.size = 0.2; l.data.color = (0.8, 0.85, 1); bpy.context.scene.collection.objects.link(l); l.parent = cam; l.location = (0, 0.05, -0.08)

def room(wallc, floorc, w=7, d=6, h=3.2, lamp=120):
    k.world(sky=(0.75, 0.78, 0.8), strength=0.5, sun=None)
    plane("floor", w, d, procmat("floor", "noise", floorc, tuple(c * 1.3 for c in floorc), 3), (0, 0, 0))
    wm = mat("wallm", wallc)
    box("wb", (w, 0.1, h), wm, (0, d / 2, h / 2)); box("wl", (0.1, d, h), wm, (-w / 2, 0, h / 2)); box("wr", (0.1, d, h), wm, (w / 2, 0, h / 2)); plane("ceil", w, d, mat("ceil", (0.8, 0.8, 0.78)), (0, 0, h), rot=(R(180), 0, 0))
    for x in (-1.5, 1.5):
        l = bpy.data.objects.new("al", bpy.data.lights.new("al", "AREA")); l.data.energy = lamp; l.data.size = 1.0; l.data.color = (1, 0.95, 0.85); l.location = (x, 0, h - 0.05); bpy.context.scene.collection.objects.link(l)
        plane("lp" + str(x), 1.0, 0.4, mat("lpm" + str(x), (1, 1, 0.95), emit=3), (x, 0, h - 0.02), rot=(R(180), 0, 0))

def road():
    k.world(sky=(0.5, 0.66, 0.92)); rd = procmat("road", "noise", (0.06, 0.06, 0.065), (0.13, 0.13, 0.135), 1.5)
    plane("ground", 14, 900, rd, (0, -250, 0)); wl = mat("wl", (0.85, 0.85, 0.85)); yl = mat("yl", (0.9, 0.8, 0.25))
    for i in range(-110, 30):
        for x in (-1.6, 1.7): plane(f"d{i}{x}", 0.14, 2.0, wl, (x, i * 5, 0.006))
    for x in (-5.0, 5.0): plane(f"e{x}", 0.16, 900, yl, (x, -250, 0.006))
    for sx in (-1, 1):
        plane(f"walk{sx}", 4, 900, mat(f"walk{sx}", (0.55, 0.55, 0.53)), (sx * 9, -250, 0.01)); plane(f"grass{sx}", 60, 900, mat(f"grass{sx}", (0.12, 0.35, 0.1)), (sx * 41, -250, 0.004))
    cols = [(0.42, 0.5, 0.62), (0.62, 0.55, 0.42), (0.5, 0.6, 0.5), (0.66, 0.66, 0.68)]; rf = mat("roof", (0.12, 0.12, 0.2)); wn = mat("hw", (0.85, 0.87, 0.9))
    sm = [mat(f"sid{i}", c) for i, c in enumerate(cols)]
    for i in range(-48, 8):
        for sx in (-1, 1):
            y = i * 9.5; box(f"h{i}{sx}", (7, 6.5, 5), sm[(i + sx) % 4], (sx * 15.5, y, 0), base="z"); box(f"r{i}{sx}", (7.6, 7, 2.2), rf, (sx * 15.5, y, 5), base="z", taper=0.25)
            for q in (-1.8, 1.8): box(f"hw{i}{sx}{q}", (0.1, 1.1, 1.3), wn, (sx * 11.98, y + q, 1.6), base="z")

def ourcar(hide_glass=False):
    veh = bpy.data.objects.new("veh", None); bpy.context.scene.collection.objects.link(veh)
    for o in k.car():
        if o.parent is None: o.parent = veh
        if hide_glass and o.name == "glass": o.hide_render = True
    return veh

def lowbody(name, loc, body, L, Wd, Hlow, Hroof, cab0, cab1, badge=None, badge_side=1):
    """Low-poly car with open greenhouse. Faces -Y. Returns root; parts are children."""
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root); root.location = loc
    gl = mat(name + "_gl", (0.03, 0.04, 0.05), 0.1); tr = mat(name + "_tire", (0.02, 0.02, 0.02)); dk = mat(name + "_dk", (0.06, 0.06, 0.065)); lt = mat(name + "_lt", (0.9, 0.1, 0.08), emit=0.6)
    box(name + "_low", (Wd, L, Hlow - 0.28), body, loc=(0, 0, 0.28), parent=root, base="z", taper=0.96)
    box(name + "_roof", (Wd * 0.84, (cab1 - cab0) * 0.82, 0.06), body, loc=(0, (cab0 + cab1) / 2 + 0.05, Hroof - 0.06), parent=root, base="z")
    ph = Hroof - Hlow
    for sx in (-1, 1):
        x = sx * Wd * 0.43
        box(f"{name}_pa{sx}", (0.07, 0.08, ph * 1.18), body, loc=(x, cab0, Hlow - 0.02), rot=(R(-32), 0, 0), parent=root, base="z")
        box(f"{name}_pb{sx}", (0.07, 0.1, ph), body, loc=(x, (cab0 + cab1) / 2, Hlow - 0.02), parent=root, base="z")
        box(f"{name}_pc{sx}", (0.07, 0.2, ph * 1.1), body, loc=(x, cab1, Hlow - 0.02), rot=(R(24), 0, 0), parent=root, base="z")
        box(f"{name}_tl{sx}", (0.3, 0.06, 0.14), lt, loc=(sx * Wd * 0.34, L / 2, Hlow - 0.2), parent=root)
        box(f"{name}_mir{sx}", (0.16, 0.08, 0.1), body, loc=(sx * (Wd / 2 + 0.06), cab0 + 0.12, Hlow + 0.05), parent=root)
    box(name + "_dash", (Wd * 0.8, 0.4, 0.16), dk, loc=(0, cab0 + 0.25, Hlow - 0.08), parent=root, base="z")
    box(name + "_floor", (Wd * 0.8, cab1 - cab0, 0.05), dk, loc=(0, (cab0 + cab1) / 2, Hlow - 0.25), parent=root)
    if badge: plane(name + "_badge", 0.22, 0.22, badge, loc=(badge_side * (Wd / 2 * 0.99 + 0.002), -L * 0.37, Hlow - 0.2), rot=(R(90), 0, R(90) * badge_side), parent=root)
    return root

G80 = "/home/user/epsilon-site/wing-configurator/data/models/bmw-m3-g80.glb"
def bmw(loc, faces):
    """Real G80 M3 body shell from the wing configurator: painted, side windows cut open, dark glass, wheels, driver."""
    import bmesh
    root = bpy.data.objects.new("bmw", None); bpy.context.scene.collection.objects.link(root); root.location = loc
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=G80); sh = [o for o in bpy.data.objects if o not in before and o.type == "MESH"][0]
    for o in [o for o in bpy.data.objects if o not in before and o is not sh]: bpy.data.objects.remove(o)
    mw = sh.matrix_world.copy(); sh.parent = None; sh.matrix_world = mw
    me = sh.data; me.transform(sh.matrix_world); sh.matrix_world.identity()
    xs = [v.co.x for v in me.vertices]; cx = (min(xs) + max(xs)) / 2
    for v in me.vertices: x, y = v.co.x - cx, v.co.y; v.co.x, v.co.y = y, -x      # nose +X -> nose -Y, centred
    paint = mat("bmw_paint", (0.015, 0.16, 0.09), 0.22); paint.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.6
    gl = mat("bmw_glass", (0.02, 0.025, 0.03), 0.08); me.materials.append(paint); me.materials.append(gl)
    bm = bmesh.new(); bm.from_mesh(me); bm.normal_update(); kill = []
    for f in bm.faces:
        c = f.calc_center_median(); n = f.normal
        if 0.99 < c.z < 1.37 and -0.62 < c.y < 1.05 and abs(c.x) > 0.5 and abs(n.x) > 0.35 and abs(n.z) < 0.75: kill.append(f)
        elif c.z > 1.0 and abs(n.y) > 0.25 and 0.15 < abs(n.z) < 0.97 and (c.y < -0.35 or c.y > 0.95) and abs(c.x) < 0.72: f.material_index = 1
    bmesh.ops.delete(bm, geom=kill, context="FACES"); bm.to_mesh(me); bm.free()
    for pl in me.polygons: pl.use_smooth = True
    sh.parent = root; sh.location = (0, 0, 0)
    dk = mat("bmw_dk", (0.05, 0.05, 0.055))
    for sx in (-1, 1):
        box(f"bmw_bp{sx}", (0.05, 0.1, 0.27), dk, loc=(sx * 0.77, 0.28, 0.97), rot=(0, R(-14) * sx, 0), parent=root, base="z")
    realwheels(root, 0.8, -1.5, 1.36)
    box("bmw_int", (1.5, 2.3, 0.5), dk, loc=(0, 0.3, 0.45), parent=root, base="z")
    box("bmw_seat", (0.5, 0.14, 0.75), mat("bseat", (0.35, 0.12, 0.08)), loc=(0.4, 0.24, 0.5), parent=root, base="z")
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    ok, hit, nrm, _ = sh.ray_cast(Vector((2.0, -1.02, 0.80)), Vector((-1, 0, 0)), depsgraph=dg)
    if ok:   # badge sits flush on the fender, facing along the surface normal, with transparent corners
        bd = plane("bmw_badge", 0.11, 0.11, alphamat("roundel", TEX + "roundel.png"), loc=hit + nrm * 0.003, parent=root)
        bd.rotation_euler = nrm.to_track_quat("Z", "Y").to_euler(); bd.rotation_euler.rotate_axis("Z", R(90))
    bs = mat("bskin", (0.74, 0.52, 0.38), 0.7); polo = mat("polo", (0.93, 0.93, 0.96))
    p, head, fd = person("beamer", "beamer", (0.4, -0.12, 0.26), R(72), bs, polo, mat("bhair", (0.5, 0.36, 0.14)), faces, hair_h=0.07); p.parent = root
    a, f = arm("barm", p, -1, bs, polo, up=-10, fwd=-10, bend=75)
    k.box("b_vape", (0.035, 0.035, 0.14), mat("bvape", (0.1, 0.7, 0.8), 0.3), loc=(0, 0.3, 0.05), parent=f)
    return root, p, head, fd, a

def van(loc, mom_faces, kid_faces, kid_back=False):
    bg = mat("van_beige", (0.5, 0.44, 0.32), 0.35); r = lowbody("van", loc, bg, 5.1, 1.95, 1.05, 1.78, -1.35, 2.3, badge=alphamat("hb", TEX + "hbadge.png"), badge_side=-1)
    realwheels(r, 0.9, -1.58, 1.58, scale=1.05, glb="/home/user/epsilon-site/showroom/models/eps-subaru-wrx-vb-v3.glb")
    ms = mat("mskin", (0.84, 0.66, 0.55), 0.7)
    m, mh, mf = person("mom", "mom", (0.45, -0.75, 0.62), 0, ms, mat("mshirt", (0.5, 0.25, 0.4)), mat("mhair", (0.25, 0.14, 0.08)), mom_faces, hair_h=0.1, bun=True); m.parent = r
    if kid_back: kl, krz = (0.0, 2.05, 0.75), R(180)
    else: kl, krz = (-0.66, 0.75, 0.72), R(-90)
    kd, kh, kf = person("kid", "kid", kl, krz, ms, mat("kshirt", (0.9, 0.75, 0.1)), mat("khair", (0.6, 0.45, 0.15)), kid_faces, hair_h=0.07, scale=0.8); kd.parent = r
    g = glassmat()
    plane("van_g1", 1.1, 0.62, g, loc=(-0.842, -0.7, 1.4), rot=(R(90), 0, R(90)), parent=r); plane("van_g2", 1.5, 0.62, g, loc=(-0.842, 0.95, 1.4), rot=(R(90), 0, R(90)), parent=r)
    return r, m, mh, mf, kd, kh, kf

def sill(cam, side=1):
    blue = mat("ourdoor", (0.02, 0.12, 0.55), 0.25); dk = mat("ourtrim", (0.03, 0.03, 0.035), 0.5)
    box("sill", (1.3, 0.09, 0.2), blue, (0.0, -0.37, -0.75), rot=(R(8), 0, R(-3) * side), parent=cam); box("sill2", (1.3, 0.06, 0.04), dk, (0.0, -0.275, -0.74), rot=(R(8), 0, R(-3) * side), parent=cam)
    box("apill", (0.07, 0.9, 0.07), dk, (-0.5 * side, 0.05, -0.7), rot=(0, 0, R(-24) * side), parent=cam); box("hdr", (1.4, 0.07, 0.1), dk, (0, 0.34, -0.72), rot=(R(-6), 0, R(-3) * side), parent=cam)

def accessport(parent, loc, rot, states):
    b = box("ap", (0.062, 0.016, 0.1), mat("apb", (0.03, 0.03, 0.03), 0.4), loc, rot=rot, parent=parent); b.scale = (1.7, 1.7, 1.7)
    d = {s: plane("ap_" + s, 0.054, 0.088, imgmat("apm_" + s, f"{TEX}ap_{s}.png", emit=1.0), (0, 0.0085, 0), rot=(R(90), 0, R(180)), parent=b) for s in states}
    box("ap_arm", (0.012, 0.012, 0.08), mat("apa", (0.02, 0.02, 0.02)), (0, 0.012, -0.08), parent=b); swap(d, [(1, states[0])]); return b, d

def wheel(parent, loc):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.018, major_segments=20, minor_segments=6); w = bpy.context.object
    w.data.materials.append(mat("whl", (0.03, 0.03, 0.03), 0.6)); w.parent = parent; w.location = loc; w.rotation_euler = (R(68), 0, 0)
    box("whl_hub", (0.3, 0.05, 0.02), mat("whl2", (0.04, 0.04, 0.04)), (0, 0, 0), parent=w); box("whl_hub2", (0.06, 0.06, 0.03), mat("whl3", (0.06, 0.06, 0.07)), (0, 0, 0), parent=w); return w

# ---------------- shots ----------------
def s1():
    room((0.78, 0.74, 0.6), (0.35, 0.3, 0.22)); rig, cam = rigcam((0, -0.7, 1.52), (0.04, 0.5, 1.2), lens=21)
    wood = procmat("wood", "noise", (0.3, 0.16, 0.07), (0.42, 0.24, 0.11), 6); box("counter", (3.2, 0.7, 1.05), wood, (0, 0.05, 0), base="z")
    plane("sign", 2.4, 0.36, imgmat("signm", TEX + "sign_office.png"), (-1.45, 2.94, 2.3), rot=(R(90), 0, 0))
    box("clock", (0.4, 0.05, 0.4), mat("clk", (0.95, 0.95, 0.9)), (1.5, 2.92, 2.3)); box("cab", (1.0, 0.5, 1.4), mat("cabm", (0.4, 0.42, 0.45)), (1.9, 2.6, 0), base="z")
    ls = mat("lskin", (0.8, 0.6, 0.48), 0.7); p, head, fd = person("lady", "lady", (0.14, 0.72, 0.78), 0, ls, mat("lshirt", (0.2, 0.4, 0.3)), mat("lhair", (0.3, 0.12, 0.06)), ["flat", "blank", "twitch", "horror"], bun=True)
    swap(fd, [(1, "flat"), (18, "blank"), (36, "twitch"), (50, "horror")])
    for f, rz in ((1, 0), (18, 6), (36, -8), (50, 4), (58, -5), (65, 6)): key(head, f, rot=(R(-4 if f < 50 else -14), 0, R(rz)), interp="CONSTANT")
    fm = {i: plane(f"form{i}", 0.24, 0.32, imgmat(f"formm{i}", TEX + n), (0.03, -0.1, 1.053 + i * 0.0005), rot=(0, 0, R(8))) for i, n in enumerate(("form_withdraw.png", "form_withdraw2.png"))}
    swap(fm, [(1, 0), (10, 1)])
    # open on the form so the dropout reads, stamp at 10, whip up to the lady
    L0 = (0, -0.7, 1.52); fl = (0.03, -0.12, 1.053); ll = (0.04, 0.5, 1.2)
    key(rig, 1, rot=lookrot(L0, fl, -6), interp="LINEAR"); key(rig, 22, rot=lookrot(L0, fl, -3), interp="LINEAR"); key(rig, 27, rot=lookrot(L0, ll), interp="LINEAR")
    for f, ln in ((1, 74), (9, 80), (10, 70), (22, 74), (27, 21)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    key(cam, 9, rot=(0, 0, 0), interp="LINEAR"); key(cam, 10, rot=(R(-1.5), R(0.8), R(2)), interp="LINEAR"); key(cam, 13, rot=(0, 0, 0), interp="LINEAR")
    h = hand("hR", cam, (0.1, -0.02, -0.5), (R(-62), 0, R(8)), curls=FLAT, thumb=0.1)
    key(h, 1, loc=(0.6, -0.7, -0.3), interp="CONSTANT"); key(h, 24, loc=(0.6, -0.7, -0.3), interp="LINEAR")
    slaps = [30, 40, 49, 57, 64]; prev = 24
    for sf in slaps:
        up = max(prev + 1, sf - max(3, (sf - prev) // 2))
        key(h, up, loc=(0.12, 0.08, -0.46), rot=(R(-40), 0, R(8)), interp="LINEAR"); key(h, sf, loc=(0.03, -0.235, -0.56), rot=(R(-86), 0, R(6)), interp="LINEAR"); prev = sf
    hl = hand("hL", cam, (-0.3, -0.3, -0.5), (R(-70), 0, R(-25)), curls=OPEN, mirror=True)
    key(hl, 1, loc=(-0.7, -0.7, -0.3), interp="CONSTANT"); key(hl, 24, loc=(-0.7, -0.7, -0.3), interp="LINEAR"); key(hl, 28, loc=(-0.3, -0.3, -0.5), interp="LINEAR")
    for sf in slaps: key(cam, sf - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, sf, rot=(R(-2.2), R(0.6), 0), interp="LINEAR"); key(cam, sf + 2, rot=(0, 0, 0), interp="LINEAR")

def s2():
    room((0.42, 0.45, 0.4), (0.25, 0.22, 0.2)); rig, cam = rigcam((0, -0.5, 1.5), (0, 0.22, 0.8), lens=19)
    wood = procmat("wood", "noise", (0.22, 0.12, 0.06), (0.33, 0.19, 0.09), 6); box("desk", (1.8, 0.9, 0.78), wood, (0, 0.1, 0), base="z")
    d = {i: plane(f"form{i}", 0.3, 0.4, imgmat(f"fm{i}", f"{TEX}form_enlist{i}.png"), (0, 0.02, 0.783), rot=(0, 0, R(-4))) for i in (0, 1, 2)}
    swap(d, [(1, 0), (12, 1), (24, 2)])
    sc = plane("scrib", 0.2, 0.075, imgmat("scm", TEX + "scribble.png"), (0.035, -0.115, 0.7845), rot=(0, 0, R(-4))); sc.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 1
    nt = sc.data.materials[0].node_tree; nt.links.new(nt.nodes["Image Texture"].outputs["Alpha"], nt.nodes["Principled BSDF"].inputs["Alpha"]); vis(sc, 1, False); vis(sc, 36, True)
    rs = mat("rskin", (0.21, 0.11, 0.07), 0.7); cam_ = mat("camo", (0.3, 0.33, 0.2))
    p, head, fd = person("rec", "recruiter", (0, 0.92, 0.45), 0, rs, cam_, mat("rhair", (0.03, 0.03, 0.03)), ["grin", "proud"], hair_h=0.05)
    p.rotation_euler = (R(-28), 0, 0); swap(fd, [(1, "grin"), (30, "proud")])
    for f, rz in ((1, -5), (12, 6), (24, -4), (36, 8)): key(head, f, rot=(R(-20), 0, R(rz)), interp="CONSTANT")
    arm("ra", p, 1, rs, cam_, up=-20, fwd=60, bend=40); arm("rb", p, -1, rs, cam_, up=-20, fwd=60, bend=40)
    h = hand("hR", cam, (0.05, -0.1, -0.5), (R(-70), 0, R(10)), curls=FIST, thumb=0.9, hold="pen"); rnd = random.Random(5)
    for f in range(1, 49, 2):
        x = -0.07 + 0.12 * (f / 48) + rnd.uniform(-0.03, 0.03); key(h, f, loc=(x, -0.15 + rnd.uniform(-0.03, 0.03), -0.6), rot=(R(-72 + rnd.uniform(-6, 6)), 0, R(10 + rnd.uniform(-12, 12))), interp="LINEAR")
    hl = hand("hL", cam, (-0.2, -0.14, -0.58), (R(-80), 0, R(-20)), curls=FLAT, mirror=True); shake(cam, 1, 48, 0.5, seed=2)
    # signing bonus: a brick of cash slides across the desk and he grabs it
    cb = box("cash", (0.5, 0.25, 0.12), mat("cashm", (0.1, 0.33, 0.14)), (-0.3, 0.7, 0.84)); plane("cash_top", 0.5, 0.25, imgmat("cashtm", TEX + "cash_top.png"), (0, 0, 0.061), parent=cb)
    vis(cb, 1, False); vis(cb, 25, True); key(cb, 25, loc=(-0.3, 0.75, 0.84), rot=(0, 0, R(40)), interp="LINEAR"); key(cb, 32, loc=(-0.52, 0.16, 0.84), rot=(0, 0, R(-10)), interp="LINEAR")
    key(hl, 32, loc=(-0.2, -0.14, -0.58), interp="LINEAR"); key(hl, 37, loc=(-0.3, 0.0, -0.66), interp="LINEAR")
    for f in range(39, 48, 4): key(hl, f, loc=(-0.3, 0.03, -0.62), interp="LINEAR"); key(hl, f + 2, loc=(-0.3, 0.0, -0.67), interp="LINEAR")

def s3():
    room((0.42, 0.45, 0.4), (0.25, 0.22, 0.2)); rig, cam = rigcam((0, -0.35, 1.45), (0, 0.9, 1.42), lens=19)
    wood = procmat("wood", "noise", (0.22, 0.12, 0.06), (0.33, 0.19, 0.09), 6); box("desk", (1.8, 0.9, 0.78), wood, (0, 0.1, 0), base="z")
    plane("form", 0.3, 0.4, imgmat("fm", TEX + "form_enlist2.png"), (0, 0.02, 0.783), rot=(0, 0, R(-4)))
    plane("sign", 2.0, 0.5, imgmat("signm", TEX + "sign_recruit.png"), (0, 2.94, 2.5), rot=(R(90), 0, 0))
    plane("sign_b", 1.6, 0.3, imgmat("signbm", TEX + "sign_bonus.png"), (-2.0, 2.94, 2.5), rot=(R(90), 0, 0))
    box("flagpole", (0.04, 0.04, 2.4), mat("pole", (0.7, 0.6, 0.2), 0.3), (1.5, 2.6, 0), base="z"); box("flag", (0.05, 0.9, 1.3), mat("flag", (0.6, 0.05, 0.07)), (1.5, 2.2, 1.1), base="z")
    rs = mat("rskin", (0.21, 0.11, 0.07), 0.7); cm = mat("camo", (0.3, 0.33, 0.2))
    p, head, fd = person("rec", "recruiter", (0, 1.05, 0.85), 0, rs, cm, mat("rhair", (0.03, 0.03, 0.03)), ["proud", "grin", "twitch"], hair_h=0.05)
    swap(fd, [(1, "grin"), (8, "proud"), (31, "twitch")]); a, f = arm("ra", p, -1, rs, cm, up=10, fwd=0, bend=-20)
    key(a, 1, rot=(R(-60), 0, R(-90)), interp="LINEAR"); key(a, 7, rot=(R(35), 0, R(-90)), interp="LINEAR"); key(f, 1, rot=(R(10), 0, 0), interp="LINEAR"); key(f, 7, rot=(R(0), 0, R(-125)), interp="LINEAR")
    arm("rb", p, 1, rs, cm, up=-70, fwd=0, bend=5)
    for fr, rz in ((1, 0), (8, 3), (31, -8), (38, 6)): key(head, fr, rot=(R(0), 0, R(rz)), interp="CONSTANT")
    h = hand("hR", cam, (0.22, -0.4, -0.4), (R(-50), 0, R(-10)), curls=FIST, thumb=0.7, hold="vape")
    key(h, 6, loc=(0.24, -0.4, -0.42), rot=(R(-50), 0, R(-10)), interp="LINEAR"); key(h, 22, loc=(0.2, -0.02, -0.34), rot=(R(-20), R(-30), R(-40)), interp="LINEAR")
    key(h, 29, loc=(0.1, 0.13, -0.16), rot=(R(-5), R(-50), R(-75)), interp="LINEAR"); key(h, 34, loc=(0.16, 0.05, -0.3), rot=(R(-15), R(-40), R(-60)), interp="LINEAR"); key(h, 47, loc=(0.2, -0.05, -0.36), rot=(R(-20), R(-30), R(-45)), interp="LINEAR")
    key(cam, 28, rot=(0, 0, 0), interp="LINEAR"); key(cam, 30, rot=(R(7), 0, R(3)), interp="LINEAR"); shake(cam, 31, 47, 1.6, seed=3)
    # the signing bonus, already in his other fist
    hl = hand("hL", cam, (-0.24, -0.5, -0.42), (R(10), R(20), R(30)), curls=FIST, thumb=0.7, mirror=True)
    cb = box("cash", (0.2, 0.1, 0.055), mat("cashm", (0.1, 0.33, 0.14)), (0, 0.05, -0.05), rot=(0, 0, R(90)), parent=hl); plane("cash_top", 0.2, 0.1, imgmat("cashtm", TEX + "cash_top.png"), (0, 0, -0.029), rot=(R(180), 0, 0), parent=cb); plane("cash_top2", 0.2, 0.1, imgmat("cashtm2", TEX + "cash_top.png"), (0, 0, 0.029), parent=cb)
    key(hl, 4, loc=(-0.24, -0.5, -0.42), interp="LINEAR"); key(hl, 12, loc=(-0.2, -0.1, -0.42), interp="LINEAR")
    for i, f in enumerate(range(15, 47, 4)): key(hl, f, loc=(-0.2 - 0.04 * (i % 2), -0.1 + 0.05 * (i % 2), -0.42), rot=(R(10), R(20), R(30 + 25 * (i % 2))), interp="LINEAR")

def s4():
    rig, cam = rigcam((0, 0, 1.0), (0, 1.0, 0.47), lens=22); bunk(cam)
    ph, d = phone(cam, ["item0", "item1", "item2", "item3", "checkout"]); sw = [(1, "item0"), (11, "item1"), (21, "item2"), (31, "item3"), (41, "checkout")]; swap(d, sw)
    hand("hL", cam, (-0.03, -0.1, -0.17), (R(-6), R(180), R(4)), curls=FLAT, thumb=0.2)
    h = hand("hR", cam, (0.06, -0.125, -0.1), (R(-38), R(4), R(32)), curls=POINT, thumb=0.9)
    for f, _ in sw[1:]:
        key(h, f - 5, loc=(0.065, -0.13, -0.1), interp="LINEAR"); key(h, f - 1, loc=(0.045, -0.085, -0.105), interp="LINEAR"); key(h, f + 2, loc=(0.075, -0.15, -0.09), interp="LINEAR")
        key(ph, f - 1, loc=(-0.012, 0.012, -0.135), interp="LINEAR"); key(ph, f, loc=(-0.012, 0.02, -0.135), interp="LINEAR"); key(ph, f + 3, loc=(-0.012, 0.012, -0.135), interp="LINEAR")

def s5():
    rig, cam = rigcam((0, 0, 1.0), (0, 1.0, 0.47), lens=22); bunk(cam); ph, d = phone(cam, ["checkout", "pressed"])
    hand("hL", cam, (-0.03, -0.1, -0.17), (R(-6), R(180), R(4)), curls=FLAT, thumb=0.2); h = hand("hR", cam, (0.06, -0.125, -0.1), (R(-38), R(4), R(32)), curls=POINT, thumb=0.9)
    f = 6.0; gap = 6.0; sched = [(1, "checkout")]; rnd = random.Random(2)
    while f < 46:
        fi = int(round(f)); sched += [(fi, "pressed"), (fi + 2, "checkout")]
        key(h, fi - 2, loc=(0.065, -0.135, -0.085), interp="LINEAR"); key(h, fi, loc=(0.045, -0.105, -0.115), interp="LINEAR"); key(h, fi + 1, loc=(0.06, -0.13, -0.09), interp="LINEAR")
        a = 0.004 + 0.012 * f / 46; key(ph, fi, loc=(-0.012 + rnd.uniform(-a, a), 0.012 - a, -0.135 - a), rot=(R(-6 + rnd.uniform(-4, 4)), R(3), R(4 + rnd.uniform(-5, 5))), interp="LINEAR"); key(ph, fi + 2, loc=(-0.012, 0.012, -0.135), rot=(R(-6), R(3), R(4)), interp="LINEAR")
        f += gap; gap = max(2.6, gap * 0.82)
    swap(d, sched); key(cam.data, 1); cam.data.lens = 22; cam.data.keyframe_insert("lens", frame=1); cam.data.lens = 27; cam.data.keyframe_insert("lens", frame=47)

def s6():
    rig, cam = rigcam((0, 0, 1.0), (0, 1.0, 0.47), lens=24); bunk(cam); ph, d = phone(cam, ["balance"])
    hand("hL", cam, (-0.03, -0.1, -0.17), (R(-6), R(180), R(4)), curls=FLAT, thumb=0.2)
    h = hand("hR", cam, (0.3, -0.2, -0.2), (R(-20), R(-80), R(60)), curls=FIST, thumb=-0.5)
    key(h, 1, loc=(0.3, -0.25, -0.2), interp="LINEAR"); key(h, 9, loc=(0.085, -0.02, -0.11), interp="LINEAR")
    for f in range(11, 30, 4): key(h, f, loc=(0.085, -0.02 + 0.012, -0.11), interp="LINEAR"); key(h, f + 2, loc=(0.085, -0.02 - 0.01, -0.11), interp="LINEAR")
    h2 = hand("hP", cam, (0.07, -0.05, -0.09), (R(-10), R(5), R(25)), curls=FLAT, thumb=0.2); vis(h2, 1, False); vis(h2, 31, True); vis(h, 31, False)
    for i, f in enumerate(range(31, 48, 4)): key(h2, f, loc=(0.06, 0.02, -0.115), interp="LINEAR"); key(h2, f + 2, loc=(0.06, -0.06, -0.115), interp="LINEAR")
    key(ph, 1, loc=(-0.012, 0.012, -0.135)); shake(cam, 1, 8, 0.8, seed=6)

def lot(n_boxes=7, seed=4):
    k.world(img="sky_dawn.png"); k.lot_set(); card = mat("card", (0.55, 0.4, 0.24)); rnd = random.Random(seed); bx = []
    for i in range(n_boxes):
        x, y = rnd.uniform(0.6, 4.4), rnd.uniform(-4.6, -2.4)
        bx.append(box(f"bx{i}", (rnd.uniform(.5, 1.1), rnd.uniform(.4, .9), rnd.uniform(.25, .6)), card, (x, y, 0), rot=(0, 0, rnd.uniform(0, 3)), base="z"))
    return card

def s7():
    """He rips the box open, pulls each kit part out and chucks it at the stock car; each one lands in place."""
    card = lot(); objs = k.car(); bpy.context.view_layer.update(); by = {o.name: o for o in objs}
    cl = (4.0, -3.4, 1.7); look = (0.0, 0.2, 0.6); rig, cam = rigcam(cl, look, lens=21); dv = (Vector(look) - Vector(cl)).normalized()
    bxl = Vector(cl) + dv * 1.4; bxl.z = 0; box("bigbox", (0.95, 0.75, 0.55), card, tuple(bxl), rot=(0, 0, R(48)), base="z"); box("bigbox_in", (0.85, 0.65, 0.02), mat("boxin", (0.05, 0.035, 0.02)), (bxl.x, bxl.y, 0.56), rot=(0, 0, R(48)))
    hold = Vector(cl) + dv * 0.8 + Vector((0, 0, -0.28)); wind = hold - dv * 0.2 + Vector((0, 0, 0.12))
    hr = hand("hR", cam, (0.16, -0.36, -0.5), (R(-70), 0, R(-10)), curls=OPEN, thumb=-0.3); hl = hand("hL", cam, (-0.16, -0.36, -0.5), (R(-70), 0, R(10)), curls=OPEN, thumb=-0.3, mirror=True)
    for i, f in enumerate(range(1, 13, 3)):
        o = 0.05 + 0.2 * (i % 2); key(hr, f, loc=(0.05 + o, -0.3 + 0.1 * (i % 2), -0.5), rot=(R(-70 + 25 * (i % 2)), 0, R(-10 - 30 * (i % 2))), interp="LINEAR"); key(hl, f, loc=(-0.05 - o, -0.3 + 0.1 * (i % 2), -0.5), rot=(R(-70 + 25 * (i % 2)), 0, R(10 + 30 * (i % 2))), interp="LINEAR")
    rnd = random.Random(9)
    for i in range(12):
        p = plane(f"fl{i}", rnd.uniform(.12, .3), rnd.uniform(.1, .25), card, (0, -0.3, -0.7), parent=cam); a = rnd.uniform(0, 6.28); st = rnd.choice([2, 4, 6, 8])
        vis(p, 1, False); vis(p, st, True); key(p, st, loc=(rnd.uniform(-.1, .1), -0.32, -0.7), rot=(0, 0, 0), interp="LINEAR")
        key(p, st + 12, loc=(math.cos(a) * 0.9, 0.3 + math.sin(a) * 0.5, -rnd.uniform(0.7, 1.4)), rot=(rnd.uniform(0, 9), rnd.uniform(0, 9), rnd.uniform(0, 9)), interp="LINEAR"); vis(p, st + 13, False)
    PARTS = [("part_front_bumper", ["body_front_bumper_stock", "trim_f1_blank_stock"], 0.42), ("part_side_skirts", ["trim_side_stock"], 0.3), ("part_rear_bumper", ["body_rear_bumper_stock"], 0.42), ("part_wrc_wing", [], 0.55)]
    for i, (pn, stock, hs) in enumerate(PARTS):
        s0 = 14 + i * 19; land = s0 + 13; src = by[pn]; ms = [o for o in [src] + list(src.children_recursive) if o.type == "MESH"]
        pts = [m.matrix_world @ Vector(c) for m in ms for c in m.bound_box]; c = sum(pts, Vector()) / len(pts)
        hd = bpy.data.objects.new("thrown_" + pn, None); bpy.context.scene.collection.objects.link(hd); hd.location = c; bpy.context.view_layer.update()
        for m in ms:
            d = m.copy(); bpy.context.scene.collection.objects.link(d); d.parent = hd; d.matrix_parent_inverse = hd.matrix_world.inverted(); d.matrix_basis = m.matrix_world.copy(); d.hide_render = False
            m.hide_render = True
        for sn in stock:
            if sn in by: vis(by[sn], 1, True); vis(by[sn], land, False)
        spin = (6.2832 * (1 if i % 2 else -1), 6.2832, 6.2832 * (2 if i < 2 else -1)); inbox = (bxl.x, bxl.y, 0.4)
        vis(hd, 1, False); vis(hd, s0, True)
        key(hd, s0, loc=inbox, rot=spin, scale=(hs * 0.5,) * 3, interp="LINEAR"); key(hd, s0 + 5, loc=tuple(hold), rot=spin, scale=(hs,) * 3, interp="LINEAR"); key(hd, s0 + 7, loc=tuple(wind), rot=tuple(v * 0.97 for v in spin), scale=(hs,) * 3, interp="LINEAR")
        mid = (Vector(wind) + c) / 2 + Vector((0, 0, 0.9)); key(hd, s0 + 10, loc=tuple(mid), rot=tuple(v * 0.5 for v in spin), scale=((hs + 1) / 2,) * 3, interp="LINEAR")
        key(hd, land, loc=tuple(c), rot=(0, 0, 0), scale=(1.14,) * 3, interp="LINEAR"); key(hd, land + 3, loc=tuple(c), rot=(0, 0, 0), scale=(1, 1, 1), interp="LINEAR")
        for h, sx in ((hr, 1), (hl, -1)):
            key(h, s0 - 1, loc=(0.2 * sx, -0.3, -0.5), rot=(R(-60), 0, R(-20 * sx)), interp="LINEAR"); key(h, s0 + 1, loc=(0.14 * sx, -0.46, -0.6), rot=(R(-95), 0, R(-10 * sx)), interp="LINEAR")
            key(h, s0 + 5, loc=(0.2 * sx, -0.24, -0.5), rot=(R(-50), R(30 * sx), R(-30 * sx)), interp="LINEAR"); key(h, s0 + 7, loc=(0.22 * sx, -0.12, -0.36), rot=(R(-30), R(30 * sx), R(-30 * sx)), interp="LINEAR")
            key(h, s0 + 10, loc=(0.12 * sx, -0.14, -0.72), rot=(R(-75), 0, R(-8 * sx)), interp="LINEAR"); key(h, s0 + 15, loc=(0.2 * sx, -0.3, -0.5), rot=(R(-60), 0, R(-20 * sx)), interp="LINEAR")
        key(cam, land - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, land, rot=(R(1.6), R(-1.2), R(1.5)), interp="LINEAR"); key(cam, land + 3, rot=(0, 0, 0), interp="LINEAR")
    for h, sx in ((hr, 1), (hl, -1)):
        for j, f in enumerate(range(87, 96, 4)): key(h, f, loc=(0.26 * sx, -0.08 + 0.06 * (j % 2), -0.44), rot=(R(-20), 0, R(-25 * sx)), interp="LINEAR")
    for f, ln in ((1, 21), (84, 21), (95, 30)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)

def s8():
    lot(5, 6); k.car(); loc = (0.9, -1.72, 1.13); rig, cam = rigcam(loc, (-0.5, 0.35, 1.12), lens=18)
    cam.rotation_euler = (0, 0, R(-38)); key(cam, 1, rot=(0, 0, R(-34))); key(cam, 95, rot=(0, 0, R(-42)))
    h = hand("hR", rig, (0.12, -0.12, -0.7), (R(-88), 0, R(15)), curls=FIST, thumb=0.9)
    for f in range(1, 95, 5): key(h, f, loc=(0.12, -0.1, -0.7), rot=(R(-70), 0, R(15)), interp="LINEAR"); key(h, f + 2, loc=(0.12, -0.2, -0.72), rot=(R(-92), 0, R(15)), interp="LINEAR")
    v = hand("hL", rig, (-0.3, -0.3, -0.3), (R(-30), R(40), R(40)), curls=FIST, thumb=0.7, mirror=True, hold="vape")
    key(v, 8, loc=(-0.35, -0.35, -0.3), interp="LINEAR"); key(v, 22, loc=(-0.1, 0.0, -0.14), interp="LINEAR"); key(v, 44, loc=(-0.1, 0.0, -0.14), interp="LINEAR"); key(v, 56, loc=(-0.36, -0.36, -0.3), interp="LINEAR")
    tg = bpy.data.objects.new("tags", None); bpy.context.scene.collection.objects.link(tg); tg.parent = rig; tg.location = (0.16, 0.2, -0.3)
    box("chain", (0.004, 0.004, 0.36), mat("chain", (0.6, 0.6, 0.62), 0.25), (0, 0, -0.18), parent=tg); tm = imgmat("tagm", TEX + "tags.png")
    for i, rz in enumerate((8, -14)): 
        t = box(f"tag{i}", (0.03, 0.002, 0.05), mat(f"tagb{i}", (0.6, 0.6, 0.62), 0.25), (0.003 * i, 0.004 * i, -0.385), rot=(0, R(rz), 0), parent=tg); plane(f"tagf{i}", 0.028, 0.048, tm, (0, 0.0012 + 0.0001, 0), rot=(R(-90), 0, 0), parent=t)
    for f in range(1, 96, 8): key(tg, f, rot=(R(6 * math.sin(f)), R(-58 + 14 * math.sin(f * 0.7)), 0), interp="BEZIER")
    cm = mat("cloud", (0.92, 0.92, 0.95), emit=0.35); rnd = random.Random(3)
    for i in range(9):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1); s = bpy.context.object; s.data.materials.append(cm); s.parent = rig; st = 44 + i * 2
        vis(s, 1, False); vis(s, st, True); key(s, st, loc=(-0.06, -0.02, -0.2), scale=(0.02,) * 3, interp="LINEAR")
        key(s, st + 26, loc=(rnd.uniform(-0.5, 0.3), rnd.uniform(-0.25, 0.3), -rnd.uniform(0.9, 1.6)), scale=(rnd.uniform(0.16, 0.3),) * 3, interp="LINEAR"); key(s, 95, scale=(0.36,) * 3, interp="LINEAR")
    shake(rig.children[0], 1, 2, 0)  # no-op keeps API parity

def s9():
    lot(4, 7); k.car(); a = (1.75, 3.25, 1.5); b = (1.0, 2.45, 1.24); tgt = (0.62, 2.12, 1.16); rig, cam = rigcam(a, tgt, lens=20)
    key(rig, 1, loc=a, rot=lookrot(a, tgt, 4), interp="LINEAR"); key(rig, 12, loc=(1.6, 3.05, 1.45), rot=lookrot((1.6, 3.05, 1.45), tgt, -3), interp="LINEAR"); key(rig, 26, loc=b, rot=lookrot(b, tgt, 6), interp="LINEAR"); key(rig, 47, loc=(0.93, 2.4, 1.22), rot=lookrot((0.93, 2.4, 1.22), tgt, 9), interp="LINEAR")
    hr = hand("hR", cam, (0.3, -0.3, -0.4), (R(-70), R(10), R(-20)), curls=OPEN, thumb=-0.2); hl = hand("hL", cam, (-0.3, -0.3, -0.4), (R(-70), R(-10), R(20)), curls=OPEN, thumb=-0.2, mirror=True)
    key(hr, 1, loc=(0.34, -0.34, -0.36), interp="LINEAR"); key(hl, 1, loc=(-0.34, -0.34, -0.36), interp="LINEAR")
    key(hr, 14, loc=(0.2, -0.1, -0.5), rot=(R(-75), R(40), R(-10)), interp="LINEAR"); key(hl, 14, loc=(-0.2, -0.1, -0.5), rot=(R(-75), R(-40), R(10)), interp="LINEAR")
    key(hr, 26, loc=(0.15, -0.04, -0.3), rot=(R(-80), R(60), R(-5)), interp="LINEAR"); key(hl, 26, loc=(-0.15, -0.04, -0.3), rot=(R(-80), R(-60), R(5)), interp="LINEAR")
    shake(cam, 26, 47, 0.7, seed=8)

def cablight(veh):
    l = bpy.data.objects.new("cabl", bpy.data.lights.new("cabl", "POINT")); l.data.energy = 14; l.data.shadow_soft_size = 0.4; l.data.color = (1, 0.97, 0.9)
    bpy.context.scene.collection.objects.link(l); l.parent = veh; l.location = (0.2, 0.25, 1.28)
    jn = texmat("jeans", "tx_fabric.png", 8, (0.12, 0.16, 0.3))
    for sx in (-1, 1): box(f"leg{sx}", (0.17, 0.62, 0.15), jn, (0.36 + sx * 0.12, -0.02, 0.66), rot=(R(8), 0, R(-6) * sx), parent=veh)
    box("seatpan", (0.56, 0.6, 0.2), _flat_mat("seatpan", (0.04, 0.04, 0.045)), (0.36, 0.25, 0.5), parent=veh); box("floorpan", (1.7, 2.4, 0.05), _flat_mat("floorpan", (0.03, 0.03, 0.035)), (0, 0.2, 0.3), parent=veh)

def cabin(lens=19, look=(0.1, -0.8, 1.0), loc=(0.36, 0.14, 1.25), glass=True):
    veh = ourcar(hide_glass=glass); rig, cam = rigcam(loc, look, lens=lens, parent=veh); cablight(veh); return veh, rig, cam

def s10():
    road(); veh, rig, cam = cabin(look=(0.14, -0.6, 1.08)); ap, d = accessport(veh, (0.14, -0.4, 1.13), (R(-10), 0, R(-14)), ["off", "ok"]); swap(d, [(1, "off"), (27, "ok")])
    # the hand lives in car space so every smack lands flat on the Accessport itself
    hit = (0.145, -0.335, 1.2); back = (0.17, -0.27, 1.33); hr0 = (R(55), 0, R(163)); h = hand("hR", veh, back, hr0, curls=FLAT, thumb=0.2)
    for cf in (6, 14, 22, 26):
        key(h, cf - 4, loc=back, rot=(R(55), 0, R(163)), interp="LINEAR"); key(h, cf, loc=hit, rot=(R(22), 0, R(163)), interp="LINEAR")
        key(cam, cf - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, cf, rot=(R(-2.5), 0, R(1)), interp="LINEAR"); key(cam, cf + 2, rot=(0, 0, 0), interp="LINEAR")
    key(h, 31, loc=(0.3, -0.2, 1.02), rot=(R(15), 0, R(163)), interp="LINEAR")
    for f in range(34, 48, 4): key(h, f, loc=(0.3, -0.2, 1.02), interp="LINEAR"); key(h, f + 2, loc=(0.3, -0.2, 1.05), interp="LINEAR")
    cam.data.lens = 19; cam.data.keyframe_insert("lens", frame=26); cam.data.lens = 24; cam.data.keyframe_insert("lens", frame=30)

def beamer_setup(lens, faces):
    road(); r, p, head, fd, a = bmw((-3.05, -0.1, 0), faces); loc = (-0.55, 0.3, 1.22); rig, cam = rigcam(loc, (-2.63, -0.2, 1.06), lens=lens, roll=3); sill(cam)
    return r, p, head, fd, a, rig, cam

def s11():
    r, p, head, fd, a, rig, cam = beamer_setup(30, ["smug", "talk", "grin"])
    sched = [(1, "smug")] + [(70 + i * 3, "talk" if i % 2 == 0 else "smug") for i in range(7)] + [(91, "grin")]; swap(fd, sched)
    for f, rx, rz in ((1, 0, -6), (6, 14, -6), (10, -4, -6), (14, 12, -6), (18, 0, -6), (70, -6, 4), (76, 4, -8), (82, -6, 6), (91, 0, 0)): key(head, f, rot=(R(rx), R(-6), R(rz)), interp="CONSTANT" if f >= 70 else "LINEAR")
    h = hand("hR", cam, (0.16, -0.2, -0.42), (R(-66), R(10), R(-22)), curls=POINT, thumb=0.9)
    key(h, 1, loc=(0.3, -0.4, -0.4), interp="LINEAR"); key(h, 14, loc=(0.16, -0.2, -0.42), rot=(R(-66), R(10), R(-22)), interp="LINEAR")
    for f in range(20, 44, 6): key(h, f, loc=(0.1, -0.24, -0.4), rot=(R(-110), R(10), R(10)), interp="LINEAR"); key(h, f + 3, loc=(0.1, -0.27, -0.42), rot=(R(-120), R(10), R(10)), interp="LINEAR")
    h2 = hand("hF", cam, (0.16, -0.16, -0.42), (R(-50), R(10), R(-20)), curls=OPEN, thumb=-0.2); vis(h2, 1, False); vis(h2, 46, True); vis(h, 46, False)
    for f in range(46, 95, 5): u = ((f - 46) // 5) % 2; key(h2, f, loc=(0.16, -0.17 + 0.03 * u, -0.42), rot=(R(-50 + 30 * u), R(10), R(-20)), interp="LINEAR")
    shake(cam, 1, 95, 0.35, step=3, seed=11)

def s12():
    r, p, head, fd, a, rig, cam = beamer_setup(36, ["grin", "smug", "horror"]); swap(fd, [(1, "grin"), (14, "smug"), (26, "grin"), (36, "horror")])
    h = hand("hR", cam, (0.2, -0.16, -0.42), (R(-50), R(10), R(-20)), curls=FIST, thumb=0.9)
    for i, rf in enumerate((4, 17, 30)):
        key(a, rf - 3, rot=(R(-10), 0, R(-80)), interp="LINEAR"); key(a, rf + 2, rot=(R(50), 0, R(-80)), interp="LINEAR"); key(a, rf + 9, rot=(R(-10), 0, R(-80)), interp="LINEAR")
        key(h, rf - 3, loc=(0.2, -0.24, -0.42), interp="LINEAR"); key(h, rf + 2, loc=(0.2, 0.0, -0.4), interp="LINEAR"); key(h, rf + 9, loc=(0.2, -0.24, -0.42), interp="LINEAR")
        key(head, rf, rot=(R(-10), R(-6), R(-6)), interp="CONSTANT"); key(head, rf + 6, rot=(R(6), R(-6), R(4)), interp="CONSTANT"); shake(cam, rf, rf + 10, 1.3, seed=20 + i)
    key(head, 36, rot=(R(-14), R(-4), R(-18)), interp="CONSTANT"); cam.data.lens = 36; cam.data.keyframe_insert("lens", frame=35); cam.data.lens = 50; cam.data.keyframe_insert("lens", frame=47)

def s13():
    road(); r, m, mh, mf, kd, kh, kf = van((2.42, 0.25, 0), ["flat", "blink"], ["squish"]); loc = (0.36, 0.25, 1.22); rig, cam = rigcam(loc, (2.4, 0.1, 1.32), lens=19); sill(cam, side=-1)
    key(rig, 1, rot=lookrot(loc, (0.36, -6, 1.2)), interp="LINEAR"); key(rig, 5, rot=lookrot(loc, (2.4, 0.1, 1.32), -3), interp="LINEAR"); key(rig, 47, rot=lookrot(loc, (2.4, 0.0, 1.32), -2), interp="LINEAR")
    swap(mf, [(1, "flat"), (26, "blink"), (30, "flat")]); key(mh, 1, rot=(0, 0, 0), interp="LINEAR"); key(mh, 12, rot=(0, 0, 0), interp="LINEAR"); key(mh, 17, rot=(0, 0, R(-78)), interp="LINEAR"); key(mh, 34, rot=(0, 0, R(-78)), interp="LINEAR"); key(mh, 39, rot=(0, 0, 0), interp="LINEAR")
    key(kh, 1, rot=(0, R(10), 0)); h = hand("hR", cam, (0.1, -0.1, -0.5), (R(-20), R(10), R(-10)), curls=FLAT, thumb=0.2)
    key(h, 5, loc=(0.25, -0.35, -0.3), interp="LINEAR")
    for sf in (10, 17):
        key(h, sf - 3, loc=(0.1, -0.05, -0.5), rot=(R(-30), R(10), R(-10)), interp="LINEAR"); key(h, sf, loc=(0.06, 0.02, -0.92), rot=(R(-8), R(10), R(-10)), interp="LINEAR")
        key(cam, sf - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, sf, rot=(R(1.5), R(-1.5), 0), interp="LINEAR"); key(cam, sf + 2, rot=(0, 0, 0), interp="LINEAR")
    key(h, 22, loc=(0.1, -0.1, -0.5), rot=(R(-40), R(10), R(-10)), interp="LINEAR")
    h2 = hand("hP", cam, (0.2, -0.12, -0.45), (R(-75), R(0), R(-75)), curls=POINT, thumb=0.9); vis(h2, 1, False); vis(h2, 25, True); vis(h, 25, False)
    for f in range(25, 48, 4): u = ((f - 25) // 4) % 2; key(h2, f, loc=(0.2 + 0.05 * u, -0.12, -0.45), interp="LINEAR")

def drive(veh, f0, y0, f1, y1): key(veh, f0, loc=(0, y0, 0), interp="LINEAR"); key(veh, f1, loc=(0, y1, 0), interp="LINEAR")

def s14():
    road(); veh, rig, cam = cabin(lens=18, look=(0.3, -8, 1.1)); accessport(veh, (0.14, -0.4, 1.13), (R(-10), 0, R(-14)), ["ok"])
    r, p, head, fd, a = bmw((-3.05, -0.1, 0), ["grin"]); vn = van((3.3, 0.25, 0), ["flat"], ["squish"])
    box("pole", (0.15, 0.15, 5), mat("pole", (0.2, 0.2, 0.2)), (5.6, -9, 0), base="z"); box("lightbox", (0.4, 0.3, 1.1), mat("lb", (0.08, 0.08, 0.08)), (4.6, -9, 4.3), base="z"); box("green", (0.26, 0.05, 0.26), mat("grn", (0.1, 1, 0.3), emit=6), (4.6, -8.84, 4.42), base="z")
    for f, y in ((1, 0), (17, 0), (24, -1.2), (32, -5), (40, -11.5), (47, -19)): key(veh, f, loc=(0, y, 0), interp="LINEAR")
    for f, y in ((1, -0.1), (18, -0.1), (26, -1.0), (34, -4.2), (47, -15.5)): key(r, f, loc=(-3.05, y, 0), interp="LINEAR")
    hr = hand("hR", cam, (0.16, -0.2, -0.4), (R(-60), 0, R(-10)), curls=FIST, thumb=0.9); hl = hand("hL", cam, (-0.16, -0.2, -0.4), (R(-60), 0, R(10)), curls=FIST, thumb=0.9, mirror=True)
    for pf in (3, 8, 13):
        for hh, sx in ((hr, 1), (hl, -1)): key(hh, pf - 2, loc=(sx * 0.15, -0.02, -0.38), rot=(R(-30), 0, R(-10 * sx)), interp="LINEAR"); key(hh, pf, loc=(sx * 0.13, -0.2, -0.44), rot=(R(-70), 0, R(-10 * sx)), interp="LINEAR")
        key(cam, pf - 1, rot=(0, 0, 0), interp="LINEAR"); key(cam, pf, rot=(R(-2), 0, 0), interp="LINEAR"); key(cam, pf + 1, rot=(0, 0, 0), interp="LINEAR")
    key(hr, 18, loc=(0.24, -0.3, -0.42), rot=(R(-80), 0, R(-30)), interp="LINEAR"); key(hl, 18, loc=(-0.15, -0.17, -0.43), rot=(R(-60), 0, R(15)), interp="LINEAR")
    key(cam, 16, rot=(0, 0, 0), interp="LINEAR"); key(cam, 20, rot=(R(6), 0, 0), interp="LINEAR"); shake(cam, 21, 47, 1.4, seed=14)
    for f in range(21, 47, 2): cam.rotation_euler.x += R(4); cam.keyframe_insert("rotation_euler", frame=f)
    cam.data.lens = 18; cam.data.keyframe_insert("lens", frame=17); cam.data.lens = 13.5; cam.data.keyframe_insert("lens", frame=30)

def s15():
    road(); veh, rig, cam = cabin(lens=15, look=(0.5, -8, 1.15)); accessport(veh, (0.14, -0.4, 1.13), (R(-10), 0, R(-14)), ["ok"])
    r, p, head, fd, a = bmw((-3.05, -0.1, 0), ["horror"]); vr, m, mh, mf, kd, kh, kf = van((3.3, 0, 0), ["flat"], ["grin", "squish"], kid_back=True)
    y0 = -19.0; v = 0.9
    key(veh, 1, loc=(0, y0, 0), interp="LINEAR"); key(veh, 79, loc=(0, y0 - 78 * v, 0), interp="LINEAR"); key(r, 1, loc=(-3.05, y0 + 3.2, 0), interp="LINEAR"); key(r, 79, loc=(-3.05, y0 - 78 * v + 1.2, 0), interp="LINEAR")
    key(vr, 1, loc=(3.3, y0 + 7.5, 0), interp="LINEAR"); key(vr, 30, loc=(3.3, y0 - 29 * v - 5.5, 0), interp="LINEAR"); key(vr, 79, loc=(3.3, y0 - 78 * v - 46, 0), interp="LINEAR")
    ka, kf_ = arm("ka", kd, 1, mat("kskin2", (0.84, 0.66, 0.55)), mat("kshirt2", (0.9, 0.75, 0.1)), up=60, fwd=0, bend=20)
    for f in range(1, 80, 4): key(ka, f, rot=(R(60 + 25 * ((f // 4) % 2)), 0, R(90)), interp="LINEAR")
    loc = (0.36, 0.14, 1.25); key(rig, 1, rot=lookrot(loc, (0.5, -8, 1.15)), interp="LINEAR"); key(rig, 22, rot=lookrot(loc, (2.6, -6, 1.2)), interp="LINEAR"); key(rig, 79, rot=lookrot(loc, (1.0, -9, 1.12)), interp="LINEAR")
    hr = hand("hR", cam, (0.24, -0.3, -0.42), (R(-80), 0, R(-30)), curls=FIST, thumb=0.9); hl = hand("hL", cam, (-0.15, -0.17, -0.43), (R(-60), 0, R(15)), curls=FIST, thumb=0.9, mirror=True)
    hr2 = hand("hR2", cam, (0.2, -0.2, -0.42), (R(-60), 0, R(-15)), curls=OPEN); hl2 = hand("hL2", cam, (-0.2, -0.2, -0.42), (R(-60), 0, R(15)), curls=OPEN, mirror=True)
    for o in (hr2, hl2): vis(o, 1, False); vis(o, 34, True)
    for o in (hr, hl): vis(o, 34, False)
    key(hr2, 34, loc=(0.2, -0.2, -0.42), interp="LINEAR"); key(hr2, 79, loc=(0.24, -0.34, -0.36), rot=(R(-40), 0, R(-15)), interp="LINEAR"); key(hl2, 34, loc=(-0.2, -0.2, -0.42), interp="LINEAR"); key(hl2, 79, loc=(-0.24, -0.34, -0.36), rot=(R(-40), 0, R(15)), interp="LINEAR")
    shake(cam, 1, 30, 1.0, seed=15); shake(cam, 31, 79, 0.25, step=4, seed=16)
    cam.data.lens = 13.5; cam.data.keyframe_insert("lens", frame=1); cam.data.lens = 22; cam.data.keyframe_insert("lens", frame=60)

def s16():
    road(); veh = ourcar(hide_glass=True); cablight(veh); ap, d = accessport(veh, (0.14, -0.4, 1.13), (R(-10), 0, R(-14)), ["ok", "bad"]); swap(d, [(1, "ok"), (16, "bad"), (20, "ok"), (24, "bad")])
    mc = Vector((0.03, -0.25, 1.268)); fr = bpy.data.objects.new("mir", None); bpy.context.scene.collection.objects.link(fr); fr.location = mc; fr.rotation_euler = (R(-5), 0, R(20))
    MW, MH = 0.36, 0.125; blk = mat("mirf", (0.02, 0.02, 0.02))
    plane("mir_bg", MW, MH, imgmat("mirbg", TEX + "mirror_bg.png", emit=0.9), (0, 0, 0), rot=(R(90), 0, R(180)), parent=fr)
    for nm, sz, lc in (("rt", (MW + 0.02, 0.03, 0.012), (0, 0.004, MH / 2 + 0.004)), ("rb", (MW + 0.02, 0.03, 0.012), (0, 0.004, -MH / 2 - 0.004)), ("rl", (0.012, 0.03, MH + 0.02), (-MW / 2 - 0.004, 0.004, 0)), ("rr", (0.012, 0.03, MH + 0.02), (MW / 2 + 0.004, 0.004, 0))): box("mir_" + nm, sz, blk, lc, parent=fr)
    box("mir_house", (MW + 0.02, 0.03, MH + 0.02), blk, (0, -0.018, 0), parent=fr)
    hs = mat("skin_face", (0.33, 0.185, 0.105), 0.6, emit=0.25); sc_ = 0.2
    p, head, fd = person("him", "him", (0, 0, 0), 0, hs, mat("htee", (0.25, 0.28, 0.2), emit=0.2), mat("hhair", (0.02, 0.02, 0.02)), ["blank", "twitch", "pinpoint", "horror"], hair_h=0.04)
    p.parent = fr; p.rotation_euler = (0, 0, R(180)); p.scale = (sc_, sc_ * 0.06, sc_); p.location = (0.0, 0.006, -(0.62 + 0.15) * sc_)
    for o in p.children:
        if o.name.endswith("_torso"): o.hide_render = True
    for e_, fp in fd.items(): fp.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.0
    box("him_sh", (0.15, 0.004, 0.022), mat("htee2", (0.25, 0.28, 0.2), emit=0.2), (0, 0.004, -MH / 2 + 0.011), parent=fr)
    box("him_chain", (0.05, 0.003, 0.004), mat("hch", (0.75, 0.75, 0.78), 0.2, emit=0.3), (0, 0.0065, -MH / 2 + 0.02), parent=fr)
    swap(fd, [(1, "blank"), (66, "twitch"), (72, "blank"), (84, "twitch"), (98, "pinpoint"), (124, "horror")])
    for f, rz in ((1, 0), (66, 5), (72, 0), (84, -6), (98, 3), (124, -4), (136, 5), (144, -5)): key(head, f, rot=(0, R(rz), 0), interp="CONSTANT")
    a = (0.36, 0.14, 1.25); b = (0.24, 0.1, 1.26); rig, cam = rigcam(a, (0.1, -0.75, 1.06), lens=19, parent=veh)
    key(rig, 1, loc=a, rot=lookrot(a, (0.1, -0.75, 1.06)), interp="BEZIER"); key(rig, 40, loc=a, rot=lookrot(a, (0.1, -0.75, 1.07)), interp="BEZIER"); key(rig, 58, loc=a, rot=lookrot(a, tuple(mc)), interp="BEZIER"); key(rig, 150, loc=b, rot=lookrot(b, tuple(mc), -2), interp="LINEAR")
    for f, ln in ((1, 19), (40, 22), (58, 30), (150, 78)): cam.data.lens = ln; cam.data.keyframe_insert("lens", frame=f)
    hit = (0.145, -0.335, 1.2); up = (0.17, -0.28, 1.3); away = (0.45, 0.1, 0.85); h = hand("hR", veh, away, (R(22), 0, R(163)), curls=FLAT, thumb=0.2)
    key(h, 26, loc=away, rot=(R(22), 0, R(163)), interp="LINEAR"); key(h, 34, loc=hit, rot=(R(22), 0, R(163)), interp="LINEAR")
    for f in range(36, 54, 5): key(h, f, loc=up, rot=(R(48), 0, R(163)), interp="LINEAR"); key(h, f + 2, loc=hit, rot=(R(22), 0, R(163)), interp="LINEAR")
    key(h, 62, loc=away, rot=(R(22), 0, R(163)), interp="LINEAR"); shake(cam, 14, 26, 0.9, seed=17)

SHOTS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16]
if __name__ == "__main__":
    a = sys.argv[sys.argv.index("--") + 1:]; n = int(a[0]); out = a[1]; mode = a[2] if len(a) > 2 else "anim"; res = int(a[3]) if len(a) > 3 else 540; smp = int(a[4]) if len(a) > 4 else 14
    bpy.ops.wm.read_factory_settings(use_empty=True); SHOTS[n - 1]()
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = smp; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 3
    sc.render.resolution_x = sc.render.resolution_y = res; sc.view_settings.view_transform = "Standard"; sc.render.fps = 30; sc.frame_start = int(a[5]) if len(a) > 5 else 1; sc.frame_end = NF[n - 1]
    sc.render.image_settings.file_format = "PNG"
    if mode == "anim":
        sc.render.filepath = f"{out}/s{n:02d}/"; bpy.ops.render.render(animation=True)
    else:
        for fr in mode.split(","):
            sc.frame_set(int(fr)); sc.render.filepath = f"{out}/s{n:02d}_f{int(fr):03d}.png"; bpy.ops.render.render(write_still=True)
