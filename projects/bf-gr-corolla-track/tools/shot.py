"""BF gr-corolla-track: one renderer for every 3D shot, all in the lookbook GLB frame (m; front = -Y, z up, ground z 0).

blender -b -P shot.py -- SHOT OUTDIR [res_pct] [samples] [f_first f_last]

Shots (frame counts come from the measured kick grid, see SHOTS):
  s1_hook   CGI  low tracking front 3/4 on the circuit
  s2_push   CGI  push in on the nose; its last frame = s3's first camera (1:1 cut)
  s3_scan   SCAN silver scan + V2 kit, same camera move continuing
  s4_lip    CGI  macro on the V2 lip at speed
  s5_lipscan SCAN same macro camera, scan + V2 lip
  s6_cardv2 CARD V2 kit parts exploded around the (absent) car, black, slow orbit
  s7_side   CGI  side tracking past skirt -> spat
  s8_cardv1 CARD V1 kit parts (lookbook V1 nodes), same framing as s6
  s9_pass   CGI  static trackside camera, car passes and drives away
CGI = lookbook GLB car (paint Supersonic Red, kit in black PU) on a procedural circuit, moving environment + spinning wheels,
Cycles motion blur. SCAN = engineering full-car scan aligned to the GLB (tools/photo1to1 align) in the house silver look.
"""
import bpy, sys, math, os
from mathutils import Vector, Matrix

a = sys.argv[sys.argv.index('--') + 1:]
SHOT, OUT = a[0], a[1]
PCT = int(a[2]) if len(a) > 2 else 50
SPP = int(a[3]) if len(a) > 3 else 16
FR = (int(a[4]), int(a[5])) if len(a) > 5 else None
GLB = '/home/user/media/cars/eps-toyota-gr-corolla-v23.glb'
D = '/home/user/media/cars/gr-corolla/scan'
FPS = 30
SPEED = 33.0  # m/s on the straight (~120 km/h)

# Shot windows on the measured kick onsets of 'Electric Youth' (music/kicks.json); frames = round(kick*30) differences.
# v0.2 (user): the scan shots are replaced by the lookbook GLB in a black studio with the V2 parts highlighted;
# carbon canards added (on the car + their own shot).
import json
KICKS = json.load(open('/home/user/media/bf-gr-corolla-track/music/kicks.json'))
WIN = {'s1_hook': (0, 4), 's2_push': (4, 6), 's3_hl': (6, 10), 's4_lip': (10, 12), 's5_liphl': (12, 14), 's6_cardv2': (14, 18),
       's7_side': (18, 22), 's8_cardv1': (22, 26), 's9_canards': (26, 30), 's10_pass': (30, 32)}   # v0.5: cut sooner, before the car slows into the distance (user)
def kf(k): return 0 if k == 0 else round(KICKS[k] * 30)
N = kf(WIN[SHOT][1]) - kf(WIN[SHOT][0])
STUDIO = SHOT in ('s3_hl', 's5_liphl', 's9_canards')
MODE = 'card' if SHOT in ('s6_cardv2', 's8_cardv1') else 'cgi'


def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1,)


def mat(name, col, rough=0.5, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = col if len(col) == 4 else col + (1,)
    p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    p.inputs['Coat Weight'].default_value = coat
    return m


def silver():
    m = bpy.data.materials.new('silver'); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = 0.32; p.inputs['Metallic'].default_value = 0.85
    ao = nt.nodes.new('ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = 0.08
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 0.85
    mx.inputs['A'].default_value = (0.62, 0.63, 0.66, 1); nt.links.new(ao.outputs['Color'], mx.inputs['B'])
    nt.links.new(mx.outputs['Result'], p.inputs['Base Color'])
    return m


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = N
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = PCT
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.render.use_persistent_data = False
sc.view_settings.view_transform = 'AgX'
sc.render.image_settings.file_format = 'PNG'


def ease(t):
    return t * t * (3 - 2 * t)


def look(cam, loc, tgt, roll=0.0):
    loc, tgt = Vector(loc), Vector(tgt)
    q = (tgt - loc).to_track_quat('-Z', 'Y')
    cam.matrix_world = Matrix.Translation(loc) @ q.to_matrix().to_4x4() @ Matrix.Rotation(math.radians(roll), 4, 'Z')


def key_cam(cam, path, lens=None):
    """path: list of (t 0..1, loc, tgt); keyed every frame (eased) so cuts can match exactly."""
    for f in range(1, N + 1):
        t = (f - 1) / max(N - 1, 1)
        for i in range(len(path) - 1):
            if path[i][0] <= t <= path[i + 1][0]:
                u = (t - path[i][0]) / max(path[i + 1][0] - path[i][0], 1e-9); u = ease(u)
                loc = Vector(path[i][1]).lerp(Vector(path[i + 1][1]), u); tgt = Vector(path[i][2]).lerp(Vector(path[i + 1][2]), u)
                break
        look(cam, loc, tgt)
        cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)


cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 20.25; cd.lens = 18; cd.clip_start = 0.02; cd.clip_end = 2000
cam.rotation_mode = 'XYZ'
# safe zones (knowledge/safe-zones.md): every 3D shot is lens-shifted 8 % of the width so the car sits ~86 px left,
# clear of the right-rail buttons; the same shift on both sides of every 1:1 cut keeps the matches exact
if SHOT not in ('s6_cardv2', 's8_cardv1'):
    cd.shift_x = 0.08

# ---------------------------------------------------------------- cameras (car frame; car is static in cgi/scan modes)
CAMS = {
    's1_hook': ([(0, (2.9, -4.6, 0.42), (0.1, -0.6, 0.55)), (1, (2.3, -3.9, 0.40), (0.1, -0.9, 0.50))], 16),
    's2_push': ([(0, (1.9, -4.0, 0.36), (0.0, -1.6, 0.42)), (1, (1.25, -3.45, 0.30), (0.0, -1.85, 0.34))], 16),
    's3_hl': ([(0, (1.25, -3.45, 0.30), (0.0, -1.85, 0.34)), (1, (2.05, -4.1, 0.70), (0.0, -1.2, 0.50))], 16),
    's4_lip': ([(0, (1.10, -3.05, 0.62), (0.50, -2.10, 0.12)), (1, (0.90, -3.10, 0.58), (0.30, -2.13, 0.12))], 16),   # v0.5: higher, looking down (user)
    's5_liphl': ([(0, (0.90, -3.10, 0.58), (0.30, -2.13, 0.12)), (1, (0.74, -3.13, 0.55), (0.12, -2.15, 0.12))], 16),
    's9_canards': ([(0, (1.35, -2.85, 0.56), (0.86, -1.82, 0.38)), (1, (1.70, -2.55, 0.52), (0.86, -1.80, 0.38))], 24),
    's7_side': ([(0, (3.3, -1.1, 0.42), (0.9, -0.4, 0.32)), (1, (3.3, 2.0, 0.42), (0.9, 1.4, 0.30))], 18),
}

if MODE in ('cgi',):
    bpy.ops.import_scene.gltf(filepath=GLB)
    car = bpy.data.objects.new('CAR', None); sc.collection.objects.link(car)
    V2 = {'part_front_lip_v2', 'part_side_skirts_v2', 'part_rear_spats_v2'}
    keep = V2 | {'part_canards'}
    pu = mat('pu_black', srgb('#141414'), 0.55)
    # carbon fibre (procedural 2x2 twill look) for the canards
    cf = bpy.data.materials.new('carbon'); cf.use_nodes = True; nt = cf.node_tree; p = nt.nodes['Principled BSDF']
    ck = nt.nodes.new('ShaderNodeTexChecker'); ck.inputs['Scale'].default_value = 260
    ck.inputs['Color1'].default_value = (0.012, 0.012, 0.013, 1); ck.inputs['Color2'].default_value = (0.09, 0.09, 0.1, 1)
    nt.links.new(ck.outputs['Color'], p.inputs['Base Color']); p.inputs['Roughness'].default_value = 0.25
    p.inputs['Coat Weight'].default_value = 1.0; p.inputs['Coat Roughness'].default_value = 0.02
    # highlight: the V2 parts light up in the studio shots (bright satin + emission that ramps in after the cut)
    hl = bpy.data.materials.new('v2_highlight'); hl.use_nodes = True; nt = hl.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (0.85, 0.87, 0.9, 1); p.inputs['Roughness'].default_value = 0.3; p.inputs['Metallic'].default_value = 0.6
    p.inputs['Emission Color'].default_value = (0.75, 0.88, 1.0, 1)
    HL_TARGET = SHOT if STUDIO else None
    paint = srgb('#b21522')
    for o in list(bpy.data.objects):
        if o.type != 'MESH' and o.name != 'CAR':
            continue
        base = o.name.split('.')[0]
        if base.startswith('part_') and base not in keep:
            o.hide_render = True; continue
        if base == 'livery_castrol':
            o.hide_render = True; continue
        if base in keep:
            o.data.materials.clear()
            if base == 'part_canards':
                o.data.materials.append(cf)
            elif STUDIO and SHOT != 's9_canards':
                o.data.materials.append(hl)
            else:
                o.data.materials.append(pu)
        if o.parent is None and o is not car:
            o.parent = car
    for m in bpy.data.materials:
        if m.name.startswith('paint') and m.node_tree:
            p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if p:
                p.inputs['Base Color'].default_value = paint; p.inputs['Roughness'].default_value = 0.2
                p.inputs['Metallic'].default_value = 0.35; p.inputs['Coat Weight'].default_value = 1.0; p.inputs['Coat Roughness'].default_value = 0.03
    # spinning wheels (about their own hub axis, x)
    bpy.context.view_layer.update()
    for o in [o for o in bpy.data.objects if o.name.startswith('wheel_')]:
        if True:
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; ctr = sum(bb, Vector()) / 8; r = max(v.z for v in bb) / 2
            piv = bpy.data.objects.new('hub_' + o.name, None); sc.collection.objects.link(piv); piv.location = ctr; piv.parent = car
            bpy.context.view_layer.update()
            mw = o.matrix_world.copy(); o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted(); o.matrix_world = mw
            w = SPEED / max(r, 0.3)
            for f in (1, N):
                piv.rotation_euler = (-w * (f - 1) / FPS, 0, 0); piv.keyframe_insert('rotation_euler', frame=f)
            for fc in piv.animation_data.action.fcurves if hasattr(piv.animation_data.action, 'fcurves') else []:
                for k in fc.keyframe_points: k.interpolation = 'LINEAR'

    if STUDIO:
        # body goes dark graphite, the camera sees black; key + rim + front fill; highlighted parts glow in after the cut
        for m in bpy.data.materials:
            if m.name in ('v2_highlight', 'carbon', 'pu_black') or not m.node_tree:
                continue
            p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if p:
                p.inputs['Base Color'].default_value = (0.035, 0.036, 0.04, 1); p.inputs['Metallic'].default_value = 0.3
                p.inputs['Roughness'].default_value = 0.35
                if 'Emission Strength' in p.inputs: p.inputs['Emission Strength'].default_value = 0.0
                for l in list(p.inputs['Base Color'].links): m.node_tree.links.remove(l)
        p = hl.node_tree.nodes['Principled BSDF']
        for f, e in ((1, 0.0), (7, 1.6), (N, 1.1)):
            p.inputs['Emission Strength'].default_value = e; p.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
        w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputWorld'); lp = nt.nodes.new('ShaderNodeLightPath'); mx = nt.nodes.new('ShaderNodeMixShader')
        b1 = nt.nodes.new('ShaderNodeBackground'); b1.inputs[0].default_value = (0.35, 0.36, 0.38, 1); b1.inputs[1].default_value = 0.6
        b2 = nt.nodes.new('ShaderNodeBackground'); b2.inputs[0].default_value = (0.004, 0.004, 0.005, 1)
        nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); nt.links.new(b1.outputs[0], mx.inputs[1]); nt.links.new(b2.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
        def area(name, loc, e, size, col=(1, 1, 1), tgt=(0, -0.5, 0.4)):
            l = bpy.data.lights.new(name, 'AREA'); l.energy = e; l.size = size; l.color = col
            o = bpy.data.objects.new(name, l); sc.collection.objects.link(o); o.location = loc
            o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        area('key', (4, -5, 5), 900, 4); area('rim', (-4, 5, 3.5), 1400, 3, (0.85, 0.92, 1.0)); area('top', (0, 0, 7), 900, 6)
        area('front', (2.5, -8.0, 1.2), 500, 6)
        if SHOT == 's9_canards':
            # carbon weave glows in (highlight), body darker so the canards carry the frame
            pc = cf.node_tree.nodes['Principled BSDF']; ckn = next(n for n in cf.node_tree.nodes if n.type == 'TEX_CHECKER')
            cf.node_tree.links.new(ckn.outputs['Color'], pc.inputs['Emission Color'])
            for f, e in ((1, 0.0), (8, 9.0), (N, 7.0)):
                pc.inputs['Emission Strength'].default_value = e; pc.inputs['Emission Strength'].keyframe_insert('default_value', frame=f)
            for m in bpy.data.materials:
                if m.name in ('v2_highlight', 'carbon') or not m.node_tree: continue
                pp = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                if pp: pp.inputs['Base Color'].default_value = (0.012, 0.012, 0.014, 1)
            # canard close-up: kill the broad front fill, graze the carbon with a narrow strip from above-front
            for nm in ('front', 'key'):
                bpy.data.objects[nm].data.energy *= 0.25
            area('canard', (1.4, -2.6, 1.3), 8, 0.4, tgt=(0.88, -1.8, 0.4)); area('canard2', (1.9, -1.4, 0.9), 6, 0.4, (0.85, 0.92, 1.0), tgt=(0.9, -1.85, 0.4))
        path, lens = CAMS[SHOT]; cd.lens = lens; key_cam(cam, path)
    # ---------------------------------------------------------- circuit environment (moves +Y under the static car)
    env = bpy.data.objects.new('ENV', None); sc.collection.objects.link(env)
    if not STUDIO:
        asphalt = bpy.data.materials.new('asphalt'); asphalt.use_nodes = True; nt = asphalt.node_tree; p = nt.nodes['Principled BSDF']
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 180; nz.inputs['Detail'].default_value = 8
        cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.018, 0.018, 0.02, 1); cr.color_ramp.elements[1].color = (0.06, 0.06, 0.065, 1)
        nt.links.new(nz.outputs['Fac'], cr.inputs[0]); nt.links.new(cr.outputs[0], p.inputs['Base Color']); p.inputs['Roughness'].default_value = 0.75
        bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.25; nt.links.new(nz.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs[0], p.inputs['Normal'])
        grass = mat('grass', srgb('#2f5a24'), 0.9); red = mat('kerb_red', srgb('#c8161d'), 0.5); white = mat('kerb_white', srgb('#e9e9e9'), 0.5)
        line = mat('line', srgb('#f2f2f2'), 0.5); wall = mat('barrier', srgb('#9aa0a6'), 0.4, 0.6); tyre = mat('tyre', srgb('#151515'), 0.8)
        blue = mat('board', srgb('#163a7a'), 0.4); tree = mat('tree', srgb('#1d3b1a'), 0.9); stand = mat('stand', srgb('#5b6168'), 0.6)

        def box(name, loc, size, m):
            bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name; o.scale = size
            o.data.materials.append(m); o.parent = env; return o

        L0, L1 = -420.0, 140.0; LEN = L1 - L0; Y = (L0 + L1) / 2
        box('asphalt', (0.5, Y, -0.05), (13, LEN, 0.1), asphalt)
        box('grassL', (-26.0, Y, -0.06), (40, LEN, 0.1), grass); box('grassR', (27.0, Y, -0.06), (40, LEN, 0.1), grass)
        box('lineL', (-5.85, Y, 0.002), (0.18, LEN, 0.01), line); box('lineR', (6.85, Y, 0.002), (0.18, LEN, 0.01), line)
        k = 0; y = L0
        while y < L1:  # kerbs, 1.5 m blocks alternating
            for x in (-6.6, 7.6):
                box(f'kerb{k}_{x}', (x, y + 0.75, 0.02), (1.4, 1.5, 0.06), red if k % 2 else white)
            y += 1.5; k += 1
        box('armcoL', (-14.0, Y, 0.45), (0.15, LEN, 0.45), wall); box('armcoR', (16.0, Y, 0.45), (0.15, LEN, 0.45), wall)
        y = L0; i = 0
        while y < L1:
            box(f'tyres{i}', (15.4, y, 0.35), (0.7, 6.0, 0.7), tyre)
            if i % 3 == 0:
                box(f'board{i}', (15.9, y + 3, 1.1), (0.1, 5.5, 0.9), blue)
            y += 9.0; i += 1
        y = L0; i = 0
        while y < L1:
            bpy.ops.mesh.primitive_cone_add(radius1=2.2, depth=7.5, location=(-22 - (i % 3) * 4, y, 3.7)); o = bpy.context.object; o.data.materials.append(tree); o.parent = env
            y += 7.0 + (i % 4) * 2; i += 1
        for gy in (-60.0, -180.0, -300.0):  # gantries
            box(f'gantryA{gy}', (-9.5, gy, 3.5), (0.4, 0.4, 7), stand); box(f'gantryB{gy}', (11.5, gy, 3.5), (0.4, 0.4, 7), stand)
            box(f'gantryT{gy}', (1.0, gy, 7.2), (21.5, 0.6, 1.2), blue)
        box('grandstand', (30, -120, 4), (8, 70, 8), stand)

        # sun + sky
        sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 4.5; sun.angle = math.radians(2); so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so)
        so.rotation_euler = (math.radians(50), 0, math.radians(-35))
        w = bpy.data.worlds.new('sky'); sc.world = w; w.use_nodes = True; nt = w.node_tree; bg = nt.nodes['Background']
        tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); rp = nt.nodes.new('ShaderNodeValToRGB')
        nt.links.new(tc.outputs['Generated'], sp.inputs[0]); nt.links.new(sp.outputs['Z'], rp.inputs[0])
        rp.color_ramp.elements[0].position = 0.5; rp.color_ramp.elements[0].color = (0.55, 0.62, 0.72, 1)
        rp.color_ramp.elements[1].position = 0.75; rp.color_ramp.elements[1].color = (0.18, 0.34, 0.68, 1)
        nt.links.new(rp.outputs[0], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0

        sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5

        if SHOT == 's10_pass':
            # environment static; the car drives past a fixed trackside camera
            v9 = 13.0; y0, y1 = -0.8, -v9 * (N - 1) / FPS - 0.8   # slower pass so the car stays in frame for the whole shot
            for f in (1, N):
                car.location = (0, y0 + (y1 - y0) * (f - 1) / (N - 1), 0); car.keyframe_insert('location', frame=f)
            look(cam, (2.6, 0.0, 0.5), (0.3, -10.0, 0.75)); cd.lens = 18
        else:
            for f in (1, N):
                env.location = (0, SPEED * (f - 1) / FPS, 0); env.keyframe_insert('location', frame=f)
            path, lens = CAMS[SHOT]; cd.lens = lens; key_cam(cam, path)
        for ob in (env, car):
            ad = ob.animation_data
            if ad and ad.action:
                for fc in getattr(ad.action, 'fcurves', []):
                    for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

else:
    # ---------------------------------------------------------- scan / card: silver on black, studio lights
    def append_all(path):
        with bpy.data.libraries.load(path) as (src, dst):
            dst.objects = src.objects
        for o in dst.objects:
            if o is not None:
                sc.collection.objects.link(o)   # keep SCAN_ROOT (mm -> m scale) linked, or the meshes lose their frame
        return [o for o in dst.objects if o is not None and o.type == 'MESH']
    sil = silver() if not os.environ.get('CLAY') else mat('clay', (0.5, 0.5, 0.5), 0.6)
    objs = []
    if os.environ.get('WITH_GLB'):
        bpy.ops.import_scene.gltf(filepath=GLB)
    # v0.5 cards (user: components more distinguishable): the lookbook's separate part objects, exploded apart
    bpy.ops.import_scene.gltf(filepath=GLB)
    want = ({'part_front_lip_v2', 'part_side_skirts_v2', 'part_rear_spats_v2'} if SHOT == 's6_cardv2'
            else {'part_front_lip', 'part_side_skirts', 'part_rear_spats'})
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and o.name.split('.')[0] in want:
            objs.append(o)
        elif o.type == 'MESH':
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.context.view_layer.update()
    for o in objs:
        o.data.materials.clear(); o.data.materials.append(sil)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld'); lp = nt.nodes.new('ShaderNodeLightPath'); mx = nt.nodes.new('ShaderNodeMixShader')
    b1 = nt.nodes.new('ShaderNodeBackground'); b1.inputs[0].default_value = (0.35, 0.36, 0.38, 1); b1.inputs[1].default_value = 0.7
    b2 = nt.nodes.new('ShaderNodeBackground'); b2.inputs[0].default_value = (0.004, 0.004, 0.005, 1)
    nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); nt.links.new(b1.outputs[0], mx.inputs[1]); nt.links.new(b2.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])

    def area(name, loc, e, size, col=(1, 1, 1)):
        l = bpy.data.lights.new(name, 'AREA'); l.energy = e; l.size = size; l.color = col
        o = bpy.data.objects.new(name, l); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (Vector((0, 0, 0.5)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    area('key', (4, -5, 5), 1100, 4); area('rim', (-4, 5, 3.5), 1600, 3, (0.85, 0.92, 1.0)); area('top', (0, 0, 7), 1200, 6)
    area('front', (2.5, -8.0, 1.2), 420, 6); area('front2', (-2.5, -7.0, 0.6), 150, 4)

    if MODE == 'scan':
        path, lens = CAMS[SHOT]; cd.lens = lens; key_cam(cam, path)
    else:
        # v0.5 card (user: "components more distinguishable", "can't see the profiles"): a product line-up seen from a
        # low front-3/4 camera - lip on top, ONE side skirt and ONE rear spat below (left side, x > 0), true scale,
        # each turning slowly about z to show its profile; the middle band stays empty for the V2/V1 text
        import bmesh
        def keep_left(o):
            bm = bmesh.new(); bm.from_mesh(o.data); Mw = o.matrix_world
            bmesh.ops.delete(bm, geom=[f for f in bm.faces if (Mw @ f.calc_center_median()).x < 0], context='FACES')
            bm.to_mesh(o.data); bm.free()
        az, el, D = math.radians(35), math.radians(28), 3.6
        right = Vector((math.cos(az), math.sin(az), 0)); up = Vector((0, 0, 1))
        place = {'lip': right * -0.05 + up * 1.05, 'skirts': right * -0.20 + up * -0.50, 'spats': right * 0.42 + up * -0.86 + Vector((math.sin(az), -math.cos(az), 0.45)).normalized() * 1.1}   # spat nearer the lens so the small part reads
        spin = {'lip': (-8, 6), 'skirts': (-62, -50), 'spats': (-70, -52)}
        for o in objs:
            nm = o.name.split('.')[0]; k = 'lip' if 'lip' in nm else 'spats' if 'spats' in nm else 'skirts'
            mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
            bpy.context.view_layer.update()
            if k != 'lip':
                keep_left(o)
            bpy.context.view_layer.update()
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; ctr = sum(bb, Vector()) / 8
            # pivot = an empty at the part's centre; the part hangs under it so it spins in place
            piv = bpy.data.objects.new('piv_' + k, None); sc.collection.objects.link(piv); piv.location = ctr
            bpy.context.view_layer.update(); o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted()
            for f, r_ in ((1, spin[k][0]), (N, spin[k][1])):
                piv.location = place[k]; piv.rotation_euler = (0, 0, math.radians(r_)); piv.keyframe_insert('rotation_euler', frame=f)
            piv.location = place[k]
        cd.lens = 25; cd.shift_x = 0.05
        for f in range(1, N + 1):
            t = ease((f - 1) / (N - 1)); a_ = az + math.radians(6 * t)
            loc = Vector((D * math.cos(el) * math.sin(a_), -D * math.cos(el) * math.cos(a_), D * math.sin(el)))
            look(cam, loc, (0, 0, 0)); cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)

os.makedirs(OUT, exist_ok=True)
sc.render.filepath = os.path.join(OUT, 'f_')
if FR:
    sc.frame_start, sc.frame_end = FR
sc.frame_set(sc.frame_start); print('CAMDBG', sc.camera.name, cam.data.lens, cam.data.sensor_width, tuple(round(x,3) for x in sc.camera.matrix_world.translation), [o.name for o in bpy.data.objects if o.type=='CAMERA'])
bpy.ops.render.render(animation=True)
print('IVE_SHOT_DONE', SHOT, OUT)
