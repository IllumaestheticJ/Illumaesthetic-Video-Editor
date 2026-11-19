"""Blender kit for the DITL shorts (copied from ditl-wrx-vb, parametrised for the track-guy FK8). blender -b --python ditl_kit.py -- <shot> <out.png> [res] [samples]
Shots: reveal (7), beamer (11), affirm (5). Stills for the look test; animation comes later."""
import bpy, math, sys, random
from mathutils import Vector, Euler
GLB = "/home/user/epsilon-site/wing-configurator/data/models/honda-civic-type-r-fk8-r3.glb"
WING_GLB = "/home/user/media/work/fk8-tc/fk8_tc_wing.glb"  # configurator-exact TC wing assembly
TEX = "/home/user/media/ditl-time-attack-larper/tex/"
R = math.radians

def mat(name, col, rough=0.9, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough
    if emit: b.inputs["Emission Color"].default_value = (*col, 1); b.inputs["Emission Strength"].default_value = emit
    return m

def imgmat(name, path, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(path); t.interpolation = "Closest"
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.9
    if emit:
        for l in list(b.inputs["Base Color"].links): nt.links.remove(l)
        b.inputs["Base Color"].default_value = (0, 0, 0, 1); b.inputs["Roughness"].default_value = 1.0
        nt.links.new(t.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = emit
    return m

def procmat(name, kind, c1, c2, scale=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]; b.inputs["Roughness"].default_value = 0.95
    co = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (scale,) * 3
    nt.links.new(co.outputs["Object"], mp.inputs["Vector"])
    if kind == "brick":
        t = nt.nodes.new("ShaderNodeTexBrick"); t.inputs["Color1"].default_value = (*c1, 1); t.inputs["Color2"].default_value = (*c2, 1)
        t.inputs["Mortar"].default_value = (0.55, 0.52, 0.48, 1); t.inputs["Scale"].default_value = 4
        nt.links.new(mp.outputs["Vector"], t.inputs["Vector"]); nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    else:
        t = nt.nodes.new("ShaderNodeTexNoise"); t.inputs["Scale"].default_value = 40; t.inputs["Detail"].default_value = 8
        r = nt.nodes.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].color = (*c1, 1); r.color_ramp.elements[1].color = (*c2, 1)
        r.color_ramp.elements[0].position = 0.35; r.color_ramp.elements[1].position = 0.65
        nt.links.new(mp.outputs["Vector"], t.inputs["Vector"]); nt.links.new(t.outputs["Fac"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], b.inputs["Base Color"])
    return m

def box(name, size, m, loc=(0, 0, 0), rot=(0, 0, 0), parent=None, base="center", taper=1.0):
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object; o.name = name
    sx, sy, sz = size
    for v in o.data.vertices:
        v.co.x *= sx; v.co.y *= sy; v.co.z *= sz
        if base == "y": v.co.y += sy / 2
        if base == "z": v.co.z += sz / 2
    if taper != 1.0:
        ax = 1 if base == "y" else 2
        top = max(v.co[ax] for v in o.data.vertices)
        for v in o.data.vertices:
            if abs(v.co[ax] - top) < 1e-6:
                for a in range(3):
                    if a != ax: v.co[a] *= taper
    o.data.materials.append(m); o.location = loc; o.rotation_euler = rot
    for p in o.data.polygons: p.use_smooth = False
    if parent: o.parent = parent
    return o

def plane(name, w, h, m, loc, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; o.name = name; o.scale = (w, h, 1)
    o.data.materials.append(m); o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    return o

def hand(name, skin, parent, loc, rot, curls=(0.2, 0.2, 0.2, 0.2), thumb=0.3, mirror=False, sleeve=None):
    """Fingers along local +Y, back of hand local +Z, forearm toward -Y. curls: index..pinky in radians per joint."""
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    root.parent = parent; root.location = loc; root.rotation_euler = rot
    if mirror: root.scale = (-1, 1, 1)
    palm = box(name + "_palm", (0.088, 0.1, 0.032), skin, parent=root, base="y", taper=1.08)
    box(name + "_arm", (0.07, 0.36, 0.055), skin, loc=(0, -0.36, 0), parent=root, base="y", taper=0.82)
    if sleeve: box(name + "_slv", (0.1, 0.2, 0.085), sleeve, loc=(0, -0.5, 0), parent=root, base="y")
    xs = (-0.033, -0.011, 0.011, 0.033); ln = (0.042, 0.047, 0.044, 0.034)
    for i in range(4):
        c = curls[i]
        s1 = box(f"{name}_f{i}a", (0.019, ln[i], 0.02), skin, loc=(xs[i], 0.1, 0), rot=(-c, 0, 0), parent=palm, base="y")
        s2 = box(f"{name}_f{i}b", (0.018, ln[i] * 0.8, 0.018), skin, loc=(0, ln[i], 0), rot=(-c * 1.2, 0, 0), parent=s1, base="y")
        box(f"{name}_f{i}c", (0.017, ln[i] * 0.6, 0.016), skin, loc=(0, ln[i] * 0.8, 0), rot=(-c, 0, 0), parent=s2, base="y", taper=0.75)
    t1 = box(name + "_t1", (0.024, 0.05, 0.024), skin, loc=(-0.046, 0.02, -0.004), rot=(0, 0, R(48) - thumb), parent=palm, base="y")
    box(name + "_t2", (0.021, 0.04, 0.02), skin, loc=(0, 0.05, 0), rot=(0, 0, -thumb), parent=t1, base="y", taper=0.75)
    return root

def person(name, loc, rz, skin, shirt, hair, face_png, hair_h=0.12, arm_out=None):
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root); root.location = loc; root.rotation_euler = (0, 0, rz)
    box(name + "_torso", (0.46, 0.26, 0.56), shirt, loc=(0, 0, 0), parent=root, base="z", taper=1.15)
    box(name + "_neck", (0.1, 0.1, 0.08), skin, loc=(0, 0, 0.56), parent=root, base="z")
    head = box(name + "_head", (0.21, 0.22, 0.27), skin, loc=(0, 0, 0.62), parent=root, base="z", taper=1.12)
    box(name + "_hair", (0.25, 0.26, hair_h), hair, loc=(0, 0.01, 0.27), parent=head, base="z", taper=0.85)
    plane(name + "_face", 0.21, 0.26, imgmat(name + "_facem", face_png), loc=(0, -0.118, 0.135), rot=(R(90), 0, 0), parent=head)
    if arm_out is not None:
        a = box(name + "_arm", (0.1, 0.34, 0.1), shirt, loc=(arm_out * 0.26, 0, 0.46), rot=(0, 0, R(90) * arm_out), parent=root, base="y", taper=0.8)
        box(name + "_fore", (0.085, 0.3, 0.085), skin, loc=(0, 0.34, 0), rot=(R(55), 0, 0), parent=a, base="y", taper=0.9)
    return root, head

def car(color=(0.02, 0.12, 0.55)):
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=GLB); new = [o for o in bpy.data.objects if o not in before]
    hide = {"body_front_bumper_stock", "body_rear_bumper_stock", "trim_side_stock", "trim_f1_blank_stock", "part_duckbill"}
    for o in new:
        if o.name in hide: o.hide_render = True
    m = bpy.data.materials["paint"]; b = [n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
    for l in list(b.inputs["Base Color"].links): m.node_tree.links.remove(l)
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = 0.25
    return new

def lowcar(name, loc, rz, body, glass, tire, L=4.7, Wd=1.85, Hh=1.42, badge=None):
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root); root.location = loc; root.rotation_euler = (0, 0, rz)
    box(name + "_low", (Wd, L, Hh * 0.42), body, loc=(0, 0, 0.3), parent=root, base="z", taper=0.97)
    box(name + "_cab", (Wd * 0.9, L * 0.5, Hh * 0.4), glass, loc=(0, 0.25, 0.3 + Hh * 0.42), parent=root, base="z", taper=0.78)
    box(name + "_roof", (Wd * 0.72, L * 0.38, 0.05), body, loc=(0, 0.25, 0.3 + Hh * 0.82), parent=root, base="z")
    for sx in (-1, 1):
        for sy in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.34, depth=0.24, location=(0, 0, 0)); w = bpy.context.object
            w.data.materials.append(tire); w.parent = root; w.location = (sx * Wd / 2 * 0.95, sy * L * 0.3, 0.34); w.rotation_euler = (0, R(90), 0)
    if badge: plane(name + "_badge", 0.2, 0.2, badge, loc=(Wd / 2 + 0.006, -L * 0.36, 0.72), rot=(R(90), 0, R(90)), parent=root)
    return root

def world(sky=(0.42, 0.62, 0.95), strength=1.0, sun=(3.5, 48, 35)):
    sc = bpy.context.scene; w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (*sky, 1); bg.inputs[1].default_value = strength
    if sun:
        s = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN")); s.data.energy = sun[0]; s.data.angle = R(3)
        s.rotation_euler = (R(sun[1]), 0, R(sun[2])); sc.collection.objects.link(s)

def camera(loc, look=None, rot=None, lens=20, roll=0):
    sc = bpy.context.scene; c = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(c); sc.camera = c
    c.data.lens = lens; c.data.sensor_width = 36; c.data.clip_start = 0.02; c.location = loc
    if look is not None:
        e = (Vector(look) - Vector(loc)).to_track_quat("-Z", "Y").to_euler(); c.rotation_euler = e
        c.rotation_euler.rotate_axis("Z", R(roll))
    else: c.rotation_euler = rot
    return c

SKIN = lambda: mat("skin_him", (0.33, 0.19, 0.11), 0.6)

def lot_set():
    asphalt = procmat("asphalt", "noise", (0.05, 0.05, 0.055), (0.12, 0.12, 0.125), 1.5)
    plane("ground", 80, 80, asphalt, (0, 0, 0))
    line = mat("line", (0.85, 0.85, 0.8))
    for i in range(-3, 4): plane(f"ln{i}", 0.12, 5.2, line, (i * 2.7 + 1.35, 0, 0.005))
    brick = procmat("brick", "brick", (0.42, 0.2, 0.14), (0.5, 0.27, 0.18), 1.2); win = mat("win", (0.08, 0.1, 0.14), 0.2); door = mat("door", (0.25, 0.3, 0.33))
    box("apt", (26, 6, 9), brick, (0, 10, 0), base="z")
    for i in range(-4, 5):
        for k in range(3):
            box(f"w{i}{k}", (1.3, 0.1, 1.2), win, (i * 2.8, 6.98, 1.6 + k * 2.9), base="z")
    box("dumpster", (2.2, 1.3, 1.3), mat("dump", (0.08, 0.3, 0.14)), (-5.0, 5.6, 0), base="z")
    box("ac", (0.9, 0.5, 0.6), door, (4.2, 6.7, 2.2), base="z")

def shot_reveal():
    world(); lot_set(); car()
    cam = camera((1.9, -3.9, 1.35), look=(-0.15, -0.4, 0.7), lens=20, roll=-5)
    skin = SKIN(); card = mat("card", (0.55, 0.4, 0.24)); tape = mat("tape", (0.75, 0.7, 0.6))
    random.seed(4)
    for i in range(7):
        x, y = random.uniform(-0.5, 4.2), random.uniform(-4.4, -2.6)
        box(f"bx{i}", (random.uniform(.5, 1.1), random.uniform(.4, .9), random.uniform(.25, .6)), card, (x, y, 0), rot=(0, 0, random.uniform(0, 3)), base="z")
    for i in range(9):  # cardboard flying near the lens
        p = plane(f"fl{i}", random.uniform(.12, .3), random.uniform(.1, .25), card, (random.uniform(-.55, .55), random.uniform(-.1, .5), random.uniform(-1.3, -.7)), rot=(random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3)), parent=cam)
    hand("hR", skin, cam, (0.2, -0.17, -0.42), (R(-62), R(8), R(-14)), curls=(0.1, 0.05, 0.1, 0.25), thumb=-0.3)
    hand("hL", skin, cam, (-0.21, -0.15, -0.44), (R(-58), R(-10), R(18)), curls=(0.15, 0.1, 0.1, 0.2), thumb=-0.3, mirror=True)

def shot_beamer():
    world(sky=(0.5, 0.66, 0.92)); road = procmat("road", "noise", (0.06, 0.06, 0.065), (0.13, 0.13, 0.135), 1.5)
    plane("ground", 200, 200, road, (0, 0, 0)); line = mat("line", (0.9, 0.85, 0.3))
    for i in range(-10, 10): plane(f"d{i}", 0.14, 2.0, mat("wl", (0.85, 0.85, 0.85)), (-1.6, i * 5, 0.005))
    plane("yl", 0.16, 200, line, (1.9, 0, 0.005))
    plane("walk", 4, 200, mat("walk", (0.55, 0.55, 0.53)), (-8.4, 0, 0.01)); plane("grass", 40, 200, mat("grass", (0.12, 0.35, 0.1)), (-30, 0, 0.008))
    sid = mat("siding", (0.42, 0.5, 0.62)); rf = mat("roof", (0.12, 0.12, 0.2)); wn = mat("hw", (0.85, 0.87, 0.9))
    for i in range(-5, 6):
        box(f"h{i}", (7, 6.5, 5), sid, (-15, i * 9.5, 0), base="z"); box(f"r{i}", (7.6, 7, 2.2), rf, (-15, i * 9.5, 5), base="z", taper=0.25)
        for k in (-1.8, 1.8): box(f"hw{i}{k}", (0.1, 1.1, 1.3), wn, (-11.48, i * 9.5 + k, 1.6), base="z")
    bw = mat("bmw_white", (0.82, 0.83, 0.85), 0.3); gl = mat("bmw_glass", (0.03, 0.04, 0.05), 0.1); tr = mat("tire", (0.02, 0.02, 0.02))
    bm = lowcar("bmw", (-3.05, -0.1, 0), 0, bw, gl, tr, badge=imgmat("roundel", TEX + "roundel.png"))
    for o in bm.children:
        if o.name in ("bmw_cab", "bmw_roof"): o.hide_render = True   # open cabin so the driver reads
    bx = -3.05
    box("bmw_pA", (0.07, 0.09, 0.62), bw, (bx + 0.82, -0.92, 0.9), rot=(R(-30), 0, 0), base="z"); box("bmw_pC", (0.07, 0.3, 0.6), bw, (bx + 0.82, 1.25, 0.9), rot=(R(24), 0, 0), base="z")
    box("bmw_pA2", (0.07, 0.09, 0.62), bw, (bx - 0.82, -0.92, 0.9), rot=(R(-30), 0, 0), base="z"); box("bmw_back", (1.7, 0.1, 0.55), gl, (bx, 1.4, 0.9), rot=(R(24), 0, 0), base="z")
    box("bmw_roof2", (1.72, 2.1, 0.07), bw, (bx, 0.32, 1.44), base="z"); box("bmw_seat", (0.5, 0.14, 0.7), mat("seat", (0.1, 0.1, 0.1)), (bx + 0.42, 0.62, 0.75), base="z")
    box("bmw_dash", (1.6, 0.4, 0.2), mat("dash", (0.07, 0.07, 0.07)), (bx, -0.8, 0.72), base="z"); box("bmw_far", (0.05, 2.0, 0.5), gl, (bx - 0.84, 0.3, 0.9), base="z")
    bskin = mat("bskin", (0.74, 0.52, 0.38), 0.7)
    pr, head = person("beamer", (-2.63, 0.3, 0.5), R(72), bskin, mat("polo", (0.92, 0.92, 0.95)), mat("bhair", (0.5, 0.36, 0.14)), TEX + "face_beamer_smug.png", hair_h=0.09, arm_out=1)
    head.rotation_euler = (R(4), R(-6), R(-6))
    box("b_vape", (0.035, 0.035, 0.14), mat("vape", (0.8, 0.1, 0.5), 0.3), (-2.0, 0.42, 1.2), rot=(R(15), 0, 0))
    cam = camera((-0.55, 0.3, 1.22), look=(-2.7, 0.25, 1.22), lens=24, roll=3)
    blue = mat("ourdoor", (0.02, 0.12, 0.55), 0.25); dk = mat("ourtrim", (0.03, 0.03, 0.035), 0.5)
    box("sill", (1.2, 0.09, 0.2), blue, (0.0, -0.36, -0.75), rot=(R(8), 0, R(-3)), parent=cam); box("sill2", (1.2, 0.06, 0.04), dk, (0.0, -0.265, -0.74), rot=(R(8), 0, R(-3)), parent=cam)
    box("apill", (0.07, 0.9, 0.07), dk, (-0.47, 0.05, -0.7), rot=(0, 0, R(-24)), parent=cam); box("hdr", (1.3, 0.07, 0.1), dk, (0, 0.33, -0.72), rot=(R(-6), 0, R(-3)), parent=cam)
    hand("hR", SKIN(), cam, (0.16, -0.2, -0.42), (R(-66), R(10), R(-22)), curls=(0.0, 1.3, 1.35, 1.4), thumb=0.9)   # pointing

def shot_affirm():
    world(sky=(0.02, 0.02, 0.04), strength=0.3, sun=None)
    cam = camera((0, 0, 1.0), rot=(R(62), 0, 0), lens=22)
    box("bed", (2, 3, 0.4), mat("blanket", (0.16, 0.2, 0.12)), (0, 1.0, 0.25)); box("wall", (6, 0.2, 3), mat("wall", (0.3, 0.3, 0.27)), (0, 2.6, 1.5))
    box("pillow", (0.7, 0.4, 0.15), mat("pil", (0.7, 0.7, 0.66)), (0.5, 1.6, 0.5))
    skin = SKIN()
    ph = box("phone", (0.082, 0.168, 0.009), mat("phbody", (0.02, 0.02, 0.02), 0.3), (-0.012, 0.012, -0.135), rot=(R(-6), R(3), R(4)), parent=cam)
    plane("screen", 0.075, 0.154, imgmat("scr", TEX + "screen_checkout.png", emit=0.7), (0, 0, 0.0052), parent=ph)
    hand("hL", skin, cam, (-0.03, -0.1, -0.17), (R(-6), R(180), R(4)), curls=(0.05, 0.05, 0.05, 0.05), thumb=0.2)   # palm under the phone
    hand("hR", skin, cam, (0.06, -0.125, -0.1), (R(-38), R(4), R(32)), curls=(0.0, 1.3, 1.35, 1.4), thumb=0.9)  # index jabbing Confirm
    l = bpy.data.objects.new("pl", bpy.data.lights.new("pl", "AREA")); l.data.energy = 0.07; l.data.size = 0.2; l.data.color = (0.8, 0.85, 1); bpy.context.scene.collection.objects.link(l)
    l.parent = cam; l.location = (0, 0.05, -0.1)

if __name__ == "__main__":
    a = sys.argv[sys.argv.index("--") + 1:]; shot, out = a[0], a[1]; res = int(a[2]) if len(a) > 2 else 540; smp = int(a[3]) if len(a) > 3 else 24
    bpy.ops.wm.read_factory_settings(use_empty=True)
    {"reveal": shot_reveal, "beamer": shot_beamer, "affirm": shot_affirm}[shot]()
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = smp; sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 3; sc.render.resolution_x = sc.render.resolution_y = res; sc.view_settings.view_transform = "Standard"
    sc.render.filepath = out; bpy.ops.render.render(write_still=True)
