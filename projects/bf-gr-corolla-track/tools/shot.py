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

# frames per shot from the measured kick onsets (kicks 0,4,6,10,12,14,18,22,26,30 -> frames 0,59,87,144,172,201,258,315,371,428)
SHOTS = {'s1_hook': 59, 's2_push': 28, 's3_scan': 57, 's4_lip': 28, 's5_lipscan': 29, 's6_cardv2': 57,
         's7_side': 57, 's8_cardv1': 56, 's9_pass': 57}
N = SHOTS[SHOT]
MODE = os.environ.get('FORCE_MODE') or ('scan' if SHOT in ('s3_scan', 's5_lipscan') else 'card' if SHOT.startswith('s6') or SHOT.startswith('s8') else 'cgi')


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

# ---------------------------------------------------------------- cameras (car frame; car is static in cgi/scan modes)
CAMS = {
    's1_hook': ([(0, (2.9, -4.6, 0.42), (0.1, -0.6, 0.55)), (1, (2.3, -3.9, 0.40), (0.1, -0.9, 0.50))], 16),
    's2_push': ([(0, (1.9, -4.0, 0.36), (0.0, -1.6, 0.42)), (1, (1.25, -3.45, 0.30), (0.0, -1.85, 0.34))], 16),
    's3_scan': ([(0, (1.25, -3.45, 0.30), (0.0, -1.85, 0.34)), (1, (2.6, -4.7, 1.05), (0.0, -0.6, 0.62))], 16),
    's4_lip': ([(0, (0.95, -2.62, 0.10), (0.55, -2.08, 0.15)), (1, (0.80, -2.70, 0.09), (0.30, -2.12, 0.15))], 14),
    's5_lipscan': ([(0, (0.80, -2.70, 0.09), (0.30, -2.12, 0.15)), (1, (0.66, -2.76, 0.085), (0.12, -2.14, 0.15))], 14),
    's7_side': ([(0, (3.3, -1.1, 0.42), (0.9, -0.4, 0.32)), (1, (3.3, 2.0, 0.42), (0.9, 1.4, 0.30))], 18),
}

if MODE in ('cgi',):
    bpy.ops.import_scene.gltf(filepath=GLB)
    car = bpy.data.objects.new('CAR', None); sc.collection.objects.link(car)
    keep = {'part_front_lip_v2', 'part_side_skirts_v2', 'part_rear_spats_v2'}
    pu = mat('pu_black', srgb('#141414'), 0.55)
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
            o.data.materials.clear(); o.data.materials.append(pu)
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

    # ---------------------------------------------------------- circuit environment (moves +Y under the static car)
    env = bpy.data.objects.new('ENV', None); sc.collection.objects.link(env)
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

    if SHOT == 's9_pass':
        # environment static; the car drives past a fixed trackside camera
        y0, y1 = 7.5, -SPEED * (N - 1) / FPS + 7.5
        for f in (1, N):
            car.location = (0, y0 + (y1 - y0) * (f - 1) / (N - 1), 0); car.keyframe_insert('location', frame=f)
        look(cam, (2.9, 0.0, 0.55), (0.4, -14.0, 0.7)); cd.lens = 16
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
    if MODE == 'scan':
        objs += append_all(f'{D}/scan.blend'); objs += append_all(f'{D}/v2.blend')
    else:
        objs += append_all(f'{D}/{"v2" if SHOT == "s6_cardv2" else "v1"}.blend')
    for o in objs:
        o.data.materials.clear(); o.data.materials.append(sil)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld'); lp = nt.nodes.new('ShaderNodeLightPath'); mx = nt.nodes.new('ShaderNodeMixShader')
    b1 = nt.nodes.new('ShaderNodeBackground'); b1.inputs[0].default_value = (0.35, 0.36, 0.38, 1); b1.inputs[1].default_value = 1.3
    b2 = nt.nodes.new('ShaderNodeBackground'); b2.inputs[0].default_value = (0.004, 0.004, 0.005, 1)
    nt.links.new(lp.outputs['Is Camera Ray'], mx.inputs[0]); nt.links.new(b1.outputs[0], mx.inputs[1]); nt.links.new(b2.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])

    def area(name, loc, e, size, col=(1, 1, 1)):
        l = bpy.data.lights.new(name, 'AREA'); l.energy = e; l.size = size; l.color = col
        o = bpy.data.objects.new(name, l); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (Vector((0, 0, 0.5)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    area('key', (4, -5, 5), 1800, 4); area('rim', (-4, 5, 3.5), 1600, 3, (0.85, 0.92, 1.0)); area('top', (0, 0, 7), 1200, 6)
    area('front', (2.5, -8.0, 1.2), 1300, 6); area('front2', (-2.5, -7.0, 0.6), 600, 4)

    if MODE == 'scan':
        path, lens = CAMS[SHOT]; cd.lens = lens; key_cam(cam, path)
    else:
        # card: kit parts at their mounting positions, pulled 0.18 m outward from the car centre and drifting in;
        # high side camera, car length along the frame height (nose up), slow 12 deg orbit
        for o in objs:
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; ctr = sum(bb, Vector()) / 8
            d = Vector((ctr.x, ctr.y * 0.35, 0)).normalized() * 0.35 if ctr.length > 0.1 else Vector()
            for f, s in ((1, 1.0), (N, 0.45)):
                o.location = d * s; o.keyframe_insert('location', frame=f)
        cd.lens = 31
        for f in range(1, N + 1):
            t = ease((f - 1) / (N - 1)); ang = math.radians(-16 + 12 * t); r = 5.6
            loc = Vector((r * math.cos(ang) * 0.55, 0.9 + r * math.sin(ang) * 0.2, 4.9)); tgt = Vector((0, -0.05, 0.15))
            cam.matrix_world = Matrix.Translation(loc) @ (tgt - loc).to_track_quat('-Z', 'Y').to_matrix().to_4x4()
            # roll so the nose (-Y) points up in frame
            fwd = (tgt - loc).normalized(); up = Vector((0, -1, 0)); up = (up - fwd * up.dot(fwd)).normalized()
            right = fwd.cross(up); M = Matrix((right, up, -fwd)).transposed().to_4x4(); M.translation = loc; cam.matrix_world = M
            cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)

os.makedirs(OUT, exist_ok=True)
sc.render.filepath = os.path.join(OUT, 'f_')
if FR:
    sc.frame_start, sc.frame_end = FR
sc.frame_set(sc.frame_start); print('CAMDBG', sc.camera.name, cam.data.lens, cam.data.sensor_width, tuple(round(x,3) for x in sc.camera.matrix_world.translation), [o.name for o in bpy.data.objects if o.type=='CAMERA'])
bpy.ops.render.render(animation=True)
print('IVE_SHOT_DONE', SHOT, OUT)
