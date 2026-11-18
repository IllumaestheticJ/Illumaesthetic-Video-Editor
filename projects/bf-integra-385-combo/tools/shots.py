# bf-integra-385-combo v0 shot builder (Blender 5.3, Cycles CPU).
# usage: blender -b --factory-startup -P shots.py -- --shot 1 --out DIR [--res-pct 50] [--samples 16] [--step 2] [--frames a-b]
# Frame (GLB): metres, Z up, nose -Y, rear +Y, car's right side = -X.
import bpy, sys, math, json, argparse, mathutils
from mathutils import Vector, Matrix

ap = argparse.ArgumentParser()
ap.add_argument('--shot', type=int, required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--res-pct', type=int, default=50)
ap.add_argument('--samples', type=int, default=16)
ap.add_argument('--step', type=int, default=2)
ap.add_argument('--frames', default='')
ap.add_argument('--reg-dir', default='/home/user/media/bf-integra-385-combo/work/reg', help='scan pieces (reg = 6 mm preview, reg3 = 3 mm final)')
ap.add_argument('--fps60', action='store_true', help='true 60 fps: native render, animation time-stretched x2 (same motion, same cut times)')
ap.add_argument('--glb', default='/home/user/media/bf-integra-385-combo/glb/eps-acura-integra-type-s-de5-v19.glb')
ap.add_argument('--scan', default='/home/user/media/bf-integra-385-combo/scan/car.blend')
ap.add_argument('--reg', default='/home/user/media/bf-integra-385-combo/work/reg/scan_to_glb.json')
A = ap.parse_args(sys.argv[sys.argv.index('--') + 1:])

LEN = {1: 97, 2: 70, 3: 71, 4: 142, 5: 71, 6: 70}  # v0.6: shot 4 (price) two bars so the deal reads   # frames @30 fps, cut on bar kicks of "Get Low"

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = A.samples; sc.cycles.use_denoising = True
sc.render.use_persistent_data = False
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = A.res_pct
sc.render.fps = 30
sc.view_settings.view_transform = 'AgX'
sc.render.image_settings.file_format = 'PNG'
w = bpy.data.worlds.new('w'); w.use_nodes = True
w.node_tree.nodes['Background'].inputs[0].default_value = (0.004, 0.004, 0.004, 1)
w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
sc.world = w


def mat(name, base, metal=0.0, rough=0.4, coat=0.0, emit=None, estr=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*base, 1)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    b.inputs['Coat Weight'].default_value = coat
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1)
        b.inputs['Emission Strength'].default_value = estr
    return m

M_GLOSS = mat('gloss_black', (0.012, 0.012, 0.013), rough=0.12, coat=1.0)
M_WHITE = mat('platinum_white', (0.80, 0.80, 0.78), rough=0.25, coat=1.0)
M_SILVER = mat('scan_silver', (0.62, 0.63, 0.65), metal=0.85, rough=0.38)
M_SILVER_PART = mat('scan_silver_part', (0.42, 0.43, 0.45), metal=0.85, rough=0.30)
M_BOX = mat('box_charcoal', (0.018, 0.018, 0.02), rough=0.8)
M_CYAN = mat('scan_cyan', (0.0, 0.73, 0.76), emit=(0.0, 0.73, 0.76), estr=25.0)
# v0.3 (user: "add color to the box and the beginning") - Epsilon+ site palette
EPS_VIOLET = (0.107, 0.100, 0.807)   # #5C59E8 in linear
EPS_CYAN = (0.0, 0.73, 0.76)         # #01dee2
EPS_PINK = (0.807, 0.100, 0.304)     # #E85995
# v1.0 (user: "the colors in the beginning are super unnatural - make it the color of an actual cardboard box"):
# kraft corrugated cardboard with fibre noise, clear tan packing tape, neutral studio backdrop and white rims
def kraft(name, base, dark):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 140.0; nz.inputs['Detail'].default_value = 8.0
    nz2 = nt.nodes.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 9.0; nz2.inputs['Detail'].default_value = 3.0
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'FLOAT'; mx.inputs['Factor'].default_value = 0.5
    nt.links.new(nz.outputs['Fac'], mx.inputs['A']); nt.links.new(nz2.outputs['Fac'], mx.inputs['B'])
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (*dark, 1); cr.color_ramp.elements[1].color = (*base, 1)
    cr.color_ramp.elements[0].position = 0.3; cr.color_ramp.elements[1].position = 0.75
    nt.links.new(mx.outputs['Result'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.08; nt.links.new(nz.outputs['Fac'], bm.inputs['Height'])
    nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = 0.88; b.inputs['Specular IOR Level'].default_value = 0.25
    return m
M_BOXV = kraft('box_kraft', (0.42, 0.24, 0.105), (0.30, 0.165, 0.07))
M_BOXIN = kraft('box_inner_kraft', (0.30, 0.17, 0.075), (0.20, 0.11, 0.05))
LOGO = '/home/user/media/bf-integra-385-combo/logo/Epsilon+ Logo.png'


def logo_decal(name, loc, rot, width, ink=(0.012, 0.010, 0.009)):
    """Epsilon+ wordmark printed on the kraft in dark ink (the PNG's alpha is the ink mask)"""
    img = bpy.data.images.load(LOGO, check_existing=True); asp = img.size[1] / img.size[0]
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = (width, width * asp, 1)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = img; tx.extension = 'CLIP'
    b.inputs['Base Color'].default_value = (*ink, 1); b.inputs['Roughness'].default_value = 1.0
    b.inputs['Specular IOR Level'].default_value = 0.0; b.inputs['Coat Weight'].default_value = 0.0
    nt.links.new(tx.outputs['Alpha'], b.inputs['Alpha'])
    m.blend_method = 'HASHED' if hasattr(m, 'blend_method') else None
    o.data.materials.append(m)
    return o
M_BAND = mat('box_tape', (0.48, 0.33, 0.17), rough=0.22, coat=0.6)  # clear packing tape over kraft


def add_plate():
    """Epsilon+ licence plate (user: "put an epsilon plate on the back of the car"): US 12x6 in, satin black, white
    wordmark, on the rear plate mount (plane fitted on scan + lookbook body: centre (0, 2.349, 0.584), ~8 deg tilt)."""
    import json as _j
    pm = _j.load(open('/home/user/media/bf-integra-385-combo/work/reg/plate_mount.json'))['car_nospoiler_filled']
    n = Vector(pm['normal']).normalized(); c = Vector(pm['centre']) + n * (pm['ymax'] - pm['centre'][1] + 0.006)
    q = n.to_track_quat('Z', 'Y')                    # plate +Z faces out of the car
    bpy.ops.mesh.primitive_cube_add(size=1); pl = bpy.context.object; pl.name = 'eps_plate'
    pl.scale = (0.305, 0.152, 0.004); bpy.ops.object.transform_apply(scale=True)
    bev = pl.modifiers.new('bev', 'BEVEL'); bev.width = 0.008; bev.segments = 3
    pm_ = bpy.data.materials.new('plate_black'); pm_.use_nodes = True; bb = pm_.node_tree.nodes['Principled BSDF']
    bb.inputs['Base Color'].default_value = (0.008, 0.008, 0.009, 1); bb.inputs['Roughness'].default_value = 0.35
    pl.data.materials.append(pm_)
    pl.rotation_mode = 'QUATERNION'; pl.rotation_quaternion = q; pl.location = c
    lg = logo_decal('plate_logo', (0, 0, 0), (0, 0, 0), 0.25, ink=(0.85, 0.85, 0.85))
    lg.parent = pl; lg.location = (0, 0, 0.0025); lg.rotation_euler = (0, 0, 0)
    return pl


def area(name, loc, target, size, energy, color=(1, 1, 1)):
    L = bpy.data.lights.new(name, 'AREA'); L.size = size; L.energy = energy; L.color = color
    o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return o


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def import_glb():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=A.glb)
    objs = {o.name: o for o in bpy.data.objects if o not in before}
    for o in objs.values():
        if o.type == 'MESH':  # bake transforms so parenting/empties don't matter
            o.matrix_world = o.matrix_world.copy()
    return objs


def recentre(o):
    """move object origin to its bbox centre (world) and return that centre"""
    mw = o.matrix_world
    bb = [mw @ Vector(c) for c in o.bound_box]
    c = sum(bb, Vector()) / 8
    me = o.data
    local_c = mw.inverted() @ c
    me.transform(Matrix.Translation(-local_c))
    o.matrix_world = mw @ Matrix.Translation(local_c)
    return c


def camera(lens=40):
    cam = bpy.data.cameras.new('cam'); cam.lens = lens; cam.sensor_fit = 'VERTICAL'; cam.sensor_height = 24
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    return co


def look(co, loc, tgt):
    co.location = Vector(loc)
    co.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


def key(o, f, loc=True, rot=True):
    if loc: o.keyframe_insert('location', frame=f)
    if rot: o.keyframe_insert('rotation_euler', frame=f)


# ---------------------------------------------------------------- stage (shots 1-4)
def build_stage():
    objs = import_glb()
    for n, o in objs.items():
        if n not in ('part_sport_wing', 'part_duckbill'):
            bpy.data.objects.remove(o, do_unlink=True)
    wing = bpy.data.objects['part_sport_wing']; lip = bpy.data.objects['part_duckbill']
    for o in (wing, lip):
        o.parent = None; recentre(o); o.data.materials.clear(); o.data.materials.append(M_GLOSS)
        o.rotation_mode = 'XYZ'
    # box 1.50 x 0.70 x 0.32 m, bottom at z=0, long side along X
    bw, bd, bh, t = 1.50, 0.70, 0.32, 0.012
    def slab(name, size, loc, m):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        o = bpy.context.object; o.name = name; o.scale = size
        bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); return o
    slab('box_floor', (bw, bd, t), (0, 0, t / 2), M_BOXV)
    slab('box_front', (bw, t, bh), (0, -bd / 2, bh / 2), M_BOXV)
    slab('box_back', (bw, t, bh), (0, bd / 2, bh / 2), M_BOXV)
    slab('box_l', (t, bd, bh), (-bw / 2, 0, bh / 2), M_BOXV)
    slab('box_r', (t, bd, bh), (bw / 2, 0, bh / 2), M_BOXV)
    slab('box_inner', (bw - 0.03, bd - 0.03, 0.004), (0, 0, t + 0.003), M_BOXIN)
    logo_decal('logo_front', (0, -bd / 2 - t / 2 - 0.002, bh * 0.50), (math.radians(90), 0, 0), 1.15)
    lid = slab('lid', (bw + 0.02, bd + 0.02, t), (0, 0, bh + t / 2), M_BOXV)
    lband = slab('lid_tape', (bw + 0.03, 0.075, t + 0.003), (0, 0, bh + t / 2), M_BAND)
    lband.parent = lid; lband.matrix_parent_inverse = Matrix.Translation(lid.location).inverted()
    llogo = logo_decal('logo_lid', (0, -0.20, bh + t + 0.0025), (0, 0, 0), 0.95)
    llogo.parent = lid; llogo.matrix_parent_inverse = Matrix.Translation(lid.location).inverted()
    # violet glow backdrop far behind the stage (radial gradient -> black)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 6.0, 1.2), rotation=(math.radians(90), 0, 0))
    bd_ = bpy.context.object; bd_.scale = (40, 40, 1)
    mb = bpy.data.materials.new('backdrop'); mb.use_nodes = True; nt = mb.node_tree
    for n_ in list(nt.nodes): nt.nodes.remove(n_)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); gr = nt.nodes.new('ShaderNodeTexGradient')
    gr.gradient_type = 'SPHERICAL'; cr = nt.nodes.new('ShaderNodeValToRGB')
    mp.inputs['Scale'].default_value = (6.5, 7.5, 1.0); mp.inputs['Location'].default_value = (0, 0.25, 0)
    cr.color_ramp.elements[0].color = (0, 0, 0, 1); cr.color_ramp.elements[1].color = (0.060, 0.055, 0.050, 1)  # neutral warm grey studio glow
    cr.color_ramp.elements[1].position = 0.9; cr.color_ramp.interpolation = 'EASE'
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], gr.inputs['Vector'])
    nt.links.new(gr.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], em.inputs['Color'])
    em.inputs['Strength'].default_value = 0.42; nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    bd_.data.materials.append(mb); bd_.visible_shadow = False
    flaps = lid
    # lights: soft top key + two rims + low fill
    area('key', (0.5, -1.5, 4.0), (0, 0, 0.6), 3.0, 160, (1.0, 0.96, 0.9))
    sky = area('sky', (0, 2.8, 4.2), (0, 0, 1.0), 6.0, 260); sky.data.shape = 'RECTANGLE'; sky.data.size_y = 0.35
    sky2 = area('sky2', (0, 1.2, 4.6), (0, 0, 1.0), 6.0, 160); sky2.data.shape = 'RECTANGLE'; sky2.data.size_y = 0.2
    area('rimL', (-3.0, 2.5, 2.2), (0, 0, 0.8), 1.5, 600, (1.0, 0.97, 0.92))
    area('rimR', (3.0, 2.5, 2.2), (0, 0, 0.8), 1.5, 600, (0.92, 0.95, 1.0))
    area('fill', (0, -4.0, 0.6), (0, 0, 0.6), 4.0, 40)
    return wing, lip, flaps


def flap_anim(lid, f0, f1, open_at_start=False):
    lid.rotation_mode = 'XYZ'
    if open_at_start:
        lid.hide_render = True
        for ch in lid.children: ch.hide_render = True  # tape + printed logo go with the lid
        return
    key(lid, f0)
    lid.location = lid.location + Vector((0.15, 0.6, 2.6)); lid.rotation_euler = (math.radians(-35), math.radians(10), 0)
    key(lid, f1)


def hide_until(o, f):
    o.hide_render = True; o.keyframe_insert('hide_render', frame=1)
    o.hide_render = False; o.keyframe_insert('hide_render', frame=f)


WING_HOME = Vector((0, 0, 1.25)); LIP_HOME = Vector((0, 0, 0.78))
WING_IN = Vector((0, 0, 0.16)); LIP_IN = Vector((0, 0, 0.10))


def shot_stage(n):
    wing, lip, flaps = build_stage()
    co = camera(24)
    N = LEN[n]
    if n == 1:
        for o in (wing, lip): o.location = WING_IN if o is wing else LIP_IN
        flap_anim(flaps, 70, 92)
        # cyan scanner sweep: thin emissive bar crossing the closed box f38-70
        bpy.ops.mesh.primitive_cube_add(size=1); bar = bpy.context.object; bar.name = 'sweep'
        bar.scale = (0.012, 0.85, 0.42); bar.data.materials.append(M_CYAN)
        bar.location = (-0.85, 0, 0.21); key(bar, 38, rot=False)
        bar.location = (0.85, 0, 0.21); key(bar, 70, rot=False)
        hide_until(bar, 38); bar.hide_render = True; bar.keyframe_insert('hide_render', frame=71)
        # camera: box sits low-right, black space above for the title and left for Eps
        look(co, (0.0, -4.8, 2.9), (0.0, 0, 0.95)); key(co, 1)
        look(co, (0.0, -4.55, 2.75), (0.0, 0, 0.95)); key(co, N)
    elif n == 2:
        flap_anim(flaps, 0, 0, open_at_start=True)
        lip.location = LIP_IN
        wing.location = WING_IN; wing.rotation_euler = (0, 0, 0); key(wing, 1)
        wing.location = WING_HOME; wing.rotation_euler = (math.radians(18), 0, math.radians(18)); key(wing, 40)
        wing.location = WING_HOME + Vector((0, 0, 0.03)); wing.rotation_euler = (math.radians(20), 0, math.radians(24)); key(wing, N)
        look(co, (0.0, -5.0, 1.9), (0.0, 0, 1.0)); key(co, 1)
        look(co, (0.0, -4.75, 1.85), (0.0, 0, 1.0)); key(co, N)
    elif n == 3:
        flap_anim(flaps, 0, 0, open_at_start=True)
        wing.location = WING_HOME + Vector((0, 0.05, 0.05)); wing.rotation_euler = (math.radians(20), 0, math.radians(24)); key(wing, 1)
        lip.location = LIP_IN; lip.rotation_euler = (0, 0, 0); key(lip, 1)
        lip.location = LIP_HOME; lip.rotation_euler = (math.radians(16), 0, math.radians(-14)); key(lip, 40)
        lip.location = LIP_HOME + Vector((0, 0, 0.02)); lip.rotation_euler = (math.radians(18), 0, math.radians(-18)); key(lip, N)
        look(co, (0.0, -5.0, 1.9), (0.0, 0, 1.0)); key(co, 1)
        look(co, (0.0, -4.75, 1.85), (0.0, 0, 1.0)); key(co, N)
    elif n == 4:
        flap_anim(flaps, 0, 0, open_at_start=True)
        wing.location = WING_HOME + Vector((0.0, 0.05, 0.08)); wing.rotation_euler = (math.radians(20), 0, math.radians(10)); key(wing, 1)
        wing.rotation_euler = (math.radians(20), 0, math.radians(-6)); key(wing, N)
        lip.location = LIP_HOME + Vector((0.0, 0, 0.02)); lip.rotation_euler = (math.radians(18), 0, math.radians(-10)); key(lip, 1)
        lip.rotation_euler = (math.radians(18), 0, math.radians(6)); key(lip, N)
        # parts high-right, Del bottom-right pointing left at the receipt (left)
        look(co, (0.15, -5.0, 2.2), (0.0, 0, 0.55)); key(co, 1)
        look(co, (-0.15, -4.95, 2.2), (0.0, 0, 0.55)); key(co, N)
    return N


# ---------------------------------------------------------------- car shots (5-6)
CAM5_A = ((-4.75, 7.05, 1.5), (0.05, 1.3, 0.12))
CAM5_B = ((-4.45, 6.6, 1.45), (0.05, 1.3, 0.12))
def orbit(p, tgt, deg):
    a = math.radians(deg); x, y = p[0] - tgt[0], p[1] - tgt[1]
    return (tgt[0] + x * math.cos(a) - y * math.sin(a), tgt[1] + x * math.sin(a) + y * math.cos(a), p[2])
CAM6_B = (orbit(CAM5_B[0], CAM5_B[1], -28), CAM5_B[1])


def car_lights():
    area('key', (0, 1.0, 6.0), (0, 0.5, 0), 6.0, 2500)
    area('rimL', (5.0, 5.5, 2.5), (0, 1, 0.7), 3.0, 1500)
    area('rimR', (-5.5, 4.0, 2.0), (0, 1, 0.7), 3.0, 1200)
    area('front', (-2.0, -6.0, 2.0), (0, 0, 0.7), 3.0, 600)


def shot5():
    objs = import_glb()
    for n, o in objs.items():
        if o.type != 'MESH': continue
        if n in ('body',):
            o.data.materials.clear(); o.data.materials.append(M_WHITE)
        if n in ('part_sport_wing', 'part_duckbill'):
            o.data.materials.clear(); o.data.materials.append(M_GLOSS)
    wing = bpy.data.objects['part_sport_wing']; lip = bpy.data.objects['part_duckbill']
    for o in (wing, lip): o.parent = None; o.matrix_world = o.matrix_world.copy()
    w0 = wing.location.copy(); l0 = lip.location.copy()
    wing.location = w0 + Vector((0, 0.3, 1.6)); key(wing, 1, rot=False)
    wing.location = w0 + Vector((0, 0.05, 0.25)); key(wing, 30, rot=False)
    wing.location = w0; key(wing, 46, rot=False)
    lip.location = l0 + Vector((0, 1.4, 0.35)); key(lip, 1, rot=False)
    lip.location = l0 + Vector((0, 1.1, 0.30)); key(lip, 16, rot=False)
    lip.location = l0; key(lip, 56, rot=False)
    add_plate(); car_lights()
    co = camera(36); look(co, *CAM5_A); key(co, 1); look(co, *CAM5_B); key(co, LEN[5])
    return LEN[5]


def shot6():
    objs = import_glb()
    keep = ('part_sport_wing', 'part_duckbill')
    for n, o in list(objs.items()):
        if n not in keep: bpy.data.objects.remove(o, do_unlink=True)
    for n in keep:
        o = bpy.data.objects[n]; o.parent = None; o.matrix_world = o.matrix_world.copy()
        o.data.materials.clear(); o.data.materials.append(M_SILVER_PART)
    with bpy.data.libraries.load(A.scan) as (src, dst):
        dst.objects = [n for n in src.objects]
    T = Matrix(json.load(open(A.reg))['matrix'])
    for o in dst.objects:
        if o is not None: sc.collection.objects.link(o)
    bpy.context.view_layer.update()
    for o in dst.objects:
        if o is not None and o.parent is None:
            o.matrix_world = T @ o.matrix_world
    for o in dst.objects:
        if o is not None and o.type == 'MESH':
            o.data.materials.clear(); o.data.materials.append(M_SILVER)
    car_lights()
    co = camera(36); look(co, *CAM5_B); key(co, 1)
    # orbit toward rear-on, eased
    for i, f in enumerate(range(1, LEN[6] + 1, 3)):
        u = ease((f - 1) / (LEN[6] - 1))
        look(co, orbit(CAM5_B[0], CAM5_B[1], -28 * u), CAM5_B[1]); key(co, f)
    return LEN[6]


# ---------------------------------------------------------------- v0.2 scan section (user: "the scan section needs to show
# the stock wing coming off") and the kitted CGI car. Scan pieces are in the GLB frame (split_spoiler.py).
REG = A.reg_dir
LEN.update({7: 70, 8: 71, 9: 71})
CAM7_A = ((-2.9, 5.5, 2.35), (0.0, 1.75, 0.55))
CAM7_B = ((-2.7, 5.15, 2.25), (0.0, 1.75, 0.55))


def ply(name, m):
    bpy.ops.wm.ply_import(filepath=f'{REG}/{name}.ply', forward_axis='Y', up_axis='Z')
    o = bpy.context.selected_objects[0]; o.data.materials.clear(); o.data.materials.append(m)
    bpy.ops.object.shade_flat() if False else None
    return o


def scan_car(with_spoiler):
    ply('car_nospoiler_filled', M_SILVER); ply('deck_patch', M_SILVER)
    sp = ply('stock_spoiler', M_SILVER) if with_spoiler else None
    if sp is not None:  # origin at its bbox centre so it lifts and tilts about itself
        recentre(sp); sp.rotation_mode = 'XYZ'
    return sp


def shot7():
    """scan, stock car: the factory trunk spoiler lifts off whole and leaves the frame"""
    sp = scan_car(True)
    p0 = sp.location.copy()
    key(sp, 12)
    sp.location = p0 + Vector((0, 0.10, 0.32)); sp.rotation_euler = (math.radians(-12), 0, 0); key(sp, 34)
    sp.location = p0 + Vector((0.2, 1.6, 2.6)); sp.rotation_euler = (math.radians(-40), math.radians(8), 0); key(sp, 60)
    sp.hide_render = False; sp.keyframe_insert('hide_render', frame=60)
    sp.hide_render = True; sp.keyframe_insert('hide_render', frame=61)
    add_plate(); car_lights()
    co = camera(36); look(co, *CAM7_A); key(co, 1); look(co, *CAM7_B); key(co, LEN[7])
    return LEN[7]


def glb_parts(m):
    objs = import_glb()
    for n, o in list(objs.items()):
        if n not in ('part_sport_wing', 'part_duckbill'): bpy.data.objects.remove(o, do_unlink=True)
    wing = bpy.data.objects['part_sport_wing']; lip = bpy.data.objects['part_duckbill']
    for o in (wing, lip):
        o.parent = None; o.matrix_world = o.matrix_world.copy(); o.data.materials.clear(); o.data.materials.append(m)
    return wing, lip


def install_anim(wing, lip):
    w0 = wing.location.copy(); l0 = lip.location.copy()
    lip.location = l0 + Vector((0, 0.9, 0.55)); key(lip, 1, rot=False)
    lip.location = l0 + Vector((0, 0.06, 0.04)); key(lip, 20, rot=False)
    lip.location = l0; key(lip, 26, rot=False)
    wing.location = w0 + Vector((0, 0.25, 1.4)); key(wing, 8, rot=False)
    wing.location = w0 + Vector((0, 0.02, 0.10)); key(wing, 32, rot=False)
    wing.location = w0; key(wing, 38, rot=False)


def shot8():
    """scan, spoiler gone: the Epsilon trunk lip then the Sport Wing go on; camera ends on CAM5_B (1:1 into shot 9)"""
    scan_car(False)
    wing, lip = glb_parts(M_SILVER_PART); install_anim(wing, lip)
    add_plate(); car_lights()
    co = camera(36); look(co, *CAM7_B); key(co, 1)
    for f in range(1, LEN[8] + 1, 3):
        u = ease((f - 1) / (LEN[8] - 1))
        loc = tuple(CAM7_B[0][i] + (CAM5_B[0][i] - CAM7_B[0][i]) * u for i in range(3))
        tgt = tuple(CAM7_B[1][i] + (CAM5_B[1][i] - CAM7_B[1][i]) * u for i in range(3))
        look(co, loc, tgt); key(co, f)
    look(co, *CAM5_B); key(co, LEN[8])
    return LEN[8]


def shot9():
    """CGI Integra Type S (Platinum White) with BOTH parts on (gloss black), orbit toward rear-on"""
    objs = import_glb()
    for n, o in objs.items():
        if o.type != 'MESH': continue
        if n == 'body': o.data.materials.clear(); o.data.materials.append(M_WHITE)
        if n in ('part_sport_wing', 'part_duckbill'): o.data.materials.clear(); o.data.materials.append(M_GLOSS)
    add_plate(); car_lights()
    co = camera(36)
    for f in range(1, LEN[9] + 1, 3):
        u = ease((f - 1) / (LEN[9] - 1))
        look(co, orbit(CAM5_B[0], CAM5_B[1], -28 * u), CAM5_B[1]); key(co, f)
    look(co, orbit(CAM5_B[0], CAM5_B[1], -28), CAM5_B[1]); key(co, LEN[9])
    return LEN[9]


N = {1: shot_stage, 2: shot_stage, 3: shot_stage, 4: shot_stage}.get(A.shot, None)
N = N(A.shot) if N else {5: shot5, 6: shot6, 7: shot7, 8: shot8, 9: shot9}[A.shot]()
for o in bpy.data.objects:
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, 'fcurves') else []:
            for kp in fc.keyframe_points: kp.interpolation = 'BEZIER'
sc.frame_start, sc.frame_end = 1, N
if A.fps60:  # true 60 fps: every 1/60 s rendered natively (no interpolation); keys authored at 30 fps -> remap x2
    sc.render.fps = 60; sc.render.frame_map_old = 1; sc.render.frame_map_new = 2; sc.frame_end = 2 * N
sc.frame_step = A.step
if A.frames:
    a, b = A.frames.split('-'); sc.frame_start, sc.frame_end = int(a), int(b)
sc.render.use_overwrite = False; sc.render.use_placeholder = True  # resumable long renders
sc.render.filepath = A.out.rstrip('/') + '/f'
bpy.ops.render.render(animation=True)
print('SHOT_DONE', A.shot, N)
