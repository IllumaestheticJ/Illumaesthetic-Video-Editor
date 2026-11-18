"""scene.py : BF10 turkey-crossing - one Blender renderer for every 3D shot (country road, cartoon turkey, GR Corolla GLB).

blender -b -P scene.py -- SHOT OUTDIR [res_pct] [samples] [f_first f_last]

World frame (m): the road runs along Y, centre line x = 0; the car drives in the x = +1.75 lane toward -Y (GLB front = -Y);
the turkey crosses from the verge (x = +3.4) to the middle of that lane (x = 1.75, y = 0) and stops there.
All animation is keyed on GLOBAL video frames (30 fps, video t = 0 = track 10.812 s of PhonkFlux 'TRANSFORMATION'), so the
car, turkey and feathers are one continuous event across shots. Cuts (measured hits):
  f0 (10.812)  f55 (12.650)  f108 (14.419)  f135 (15.322)  f162 (16.227 DROP = impact)  f216 (18.023, s6 half-speed to f324)  f324 (21.630 logo)
Shots:
  s1_cross  f0-55    low road-level shot, the turkey waddles in from the right (car a red speck far down the road)
  s2_look   f55-108  push-in; it stops on the lane, snaps its head to camera at f81 (cowbells out), blinks
  s3_car    f108-135 low tracking shot ahead of the charging GR Corolla (V2 kit), headlights on
  s4_eyes   f135-162 turkey close-up from the car's side, headlights flood it, eyes go huge, feathers puff
  s5_poof   f162-216 impact on the drop: POOF cloud + feather burst, the car blasts past the lens; turkey gone
  s6_feath  f216-324 empty road, feathers drifting down in half-speed slow-mo (plate for the sale text, slow-reader rule)
"""
import bpy, sys, math, os, random
from mathutils import Vector, Matrix, Euler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from turkey import build_turkey, feather_mesh, toon, srgb, TAIL_COLS

a = sys.argv[sys.argv.index('--') + 1:]
SHOT, OUT = a[0], a[1]
PCT = int(a[2]) if len(a) > 2 else 50
SPP = int(a[3]) if len(a) > 3 else 16
GLB = '/home/user/media/cars/eps-toyota-gr-corolla-v23.glb'
FPS = 30
SH = {'s1_cross': (0, 55), 's2_look': (55, 108), 's3_car': (108, 135), 's4_eyes': (135, 162), 's5_poof': (162, 216), 's6_feath': (216, 324)}
# owner rule 2026-11-18 (slow down under text): s6 plays the feather fall at half speed - 54 sim frames over 108 video frames
SLOW_AT, SLOW = 216, 0.5
F0, F1 = SH[SHOT]
if len(a) > 5:
    F0, F1 = int(a[4]), int(a[5]) + 1
IMPACT = 162
V = 35.0 / FPS          # car speed, m per frame (126 km/h)
LANE = 1.75
TX0 = 3.4               # turkey start x (verge)
STOP = 70               # turkey reaches the lane centre
STEP = 0.4505 * FPS     # one waddle step per music beat (13.5 frames)


def car_y(f):
    return 2.3 + (IMPACT - f) * V   # car centre; nose (y - 2.27) just reaches the turkey's chest on the drop


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def eout(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; C = sc.collection
sc.render.fps = FPS; sc.frame_start = F0; sc.frame_end = F1 - 1
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = PCT
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4; sc.cycles.diffuse_bounces = 2; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 2
sc.render.use_persistent_data = False
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy' if 'AgX - Punchy' in [i.identifier for i in sc.view_settings.bl_rna.properties['look'].enum_items] else 'None'
sc.render.image_settings.file_format = 'PNG'
sc.render.use_motion_blur = SHOT in ('s3_car', 's5_poof'); sc.render.motion_blur_shutter = 0.45
rnd = random.Random(10)


def mat(name, hexcol, rough=0.6, metal=0.0, emit=0.0):
    return toon(name, hexcol, rough, emit) if not metal else _metal(name, hexcol, rough, metal)


def _metal(name, hexcol, rough, metal):
    m = bpy.data.materials.new(name); m.use_nodes = True; p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = srgb(hexcol); p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metal
    return m


def noisy(name, c1, c2, scale=6.0, rough=0.85, detail=4.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; p = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale
    nz.inputs['Detail'].default_value = detail
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = srgb(c1); cr.color_ramp.elements[1].color = srgb(c2)
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector']); nt.links.new(nz.outputs['Fac'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], p.inputs['Base Color']); p.inputs['Roughness'].default_value = rough
    return m


def add(mesh_fn, name, loc, scale=(1, 1, 1), rot=(0, 0, 0), m=None, smooth=False):
    mesh_fn()
    o = bpy.context.active_object; o.name = name; o.location = loc; o.scale = scale; o.rotation_euler = rot
    if m:
        o.data.materials.append(m)
    if not smooth:
        for p in o.data.polygons:
            p.use_smooth = False
    return o


# ------------------------------------------------------------------ world + sun (late-afternoon autumn, warm and cute)
w = bpy.data.worlds.new('sky'); sc.world = w; w.use_nodes = True; nt = w.node_tree
bg = nt.nodes['Background']; bg.inputs['Strength'].default_value = 1.0
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); cr = nt.nodes.new('ShaderNodeValToRGB')
nrm = nt.nodes.new('ShaderNodeVectorMath'); nrm.operation = 'NORMALIZE'
nt.links.new(tc.outputs['Generated'], nrm.inputs[0]); nt.links.new(nrm.outputs['Vector'], sep.inputs['Vector']); nt.links.new(sep.outputs['Z'], cr.inputs['Fac'])
cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = srgb('#ffd9a3')
cr.color_ramp.elements[1].position = 0.3; cr.color_ramp.elements[1].color = srgb('#6fa6e0')
nt.links.new(cr.outputs['Color'], bg.inputs['Color'])
sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.6; sun.color = (1.0, 0.86, 0.68); sun.angle = math.radians(4)
so = bpy.data.objects.new('sun', sun); C.objects.link(so); so.rotation_euler = (math.radians(62), 0, math.radians(-35))

# ------------------------------------------------------------------ ground, road, markings
grass = noisy('grass', '#7f8f38', '#b39a42', scale=0.15, rough=0.9)
add(lambda: bpy.ops.mesh.primitive_plane_add(size=1), 'ground', (0, 60, -0.01), (600, 700, 1), m=grass)
asph = noisy('asphalt', '#2c2d31', '#45464b', scale=9.0, rough=0.8, detail=8)
add(lambda: bpy.ops.mesh.primitive_plane_add(size=1), 'road', (0, 60, 0), (7.0, 700, 1), m=asph)
grav = noisy('gravel', '#7d715d', '#a39579', scale=12, rough=0.95)
for s in (1, -1):
    add(lambda: bpy.ops.mesh.primitive_plane_add(size=1), 'shoulder', (s * 3.95, 60, -0.004), (0.9, 700, 1), m=grav)
yel = mat('yellow_line', '#f2c230', 0.5); wht = mat('white_line', '#efefe8', 0.5)
for s in (1, -1):
    add(lambda: bpy.ops.mesh.primitive_plane_add(size=1), 'edge', (s * 3.3, 60, 0.003), (0.13, 700, 1), m=wht)
for i in range(-30, 70):
    y = i * 9.0
    add(lambda: bpy.ops.mesh.primitive_plane_add(size=1), 'dash', (0, y, 0.003), (0.13, 3.0, 1), m=yel)

# ------------------------------------------------------------------ autumn trees, fence, pumpkins, hay, hills
TREE_COLS = ['#d9661f', '#eba12f', '#bf3a1f', '#d1b23a', '#7a9236', '#e07b2a']
trunk = mat('trunk', '#5b3a24', 0.8)
tmats = [mat(f'leaf{i}', c, 0.75) for i, c in enumerate(TREE_COLS)]
for i in range(150):
    s = 1 if i % 2 else -1
    x = s * rnd.uniform(6.0, 34.0); y = rnd.uniform(-70, 260)
    if abs(x) < 9 and -8 < y < 8:
        x = s * rnd.uniform(9, 20)
    h = rnd.uniform(1.6, 3.0); r = rnd.uniform(1.3, 2.6)
    add(lambda: bpy.ops.mesh.primitive_cylinder_add(vertices=7, radius=0.18, depth=h), 'trunk', (x, y, h / 2), m=trunk)
    if rnd.random() < 0.65:
        add(lambda: bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1), 'crown', (x, y, h + r * 0.75),
            (r, r, r * 1.1), (rnd.random(), rnd.random(), rnd.random()), m=rnd.choice(tmats))
    else:
        add(lambda: bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=1, radius2=0, depth=1), 'crown', (x, y, h + r * 1.1),
            (r * 0.85, r * 0.85, r * 2.6), (0, 0, rnd.random() * 6), m=rnd.choice(tmats))
wood = mat('wood', '#8a5e3b', 0.85)
for i in range(-12, 50):
    y = i * 2.6
    add(lambda: bpy.ops.mesh.primitive_cube_add(size=1), 'post', (5.2, y, 0.5), (0.12, 0.12, 1.0), m=wood)
for z in (0.45, 0.85):
    add(lambda: bpy.ops.mesh.primitive_cube_add(size=1), 'rail', (5.2, 70, z), (0.06, 260, 0.1), m=wood)
pk = mat('pumpkin', '#f07a1a', 0.55); stem = mat('stem', '#4f6b26', 0.7)
for (x, y, r) in [(4.6, 1.8, 0.28), (4.9, 2.6, 0.2), (-4.5, -1.5, 0.3), (-4.8, 3.5, 0.22), (4.7, -2.5, 0.24), (-4.6, 9, 0.3)]:
    add(lambda: bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=1), 'pumpkin', (x, y, r * 0.75), (r, r, r * 0.75), m=pk)
    add(lambda: bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=0.03, depth=0.12), 'stem', (x, y, r * 1.5 + 0.03), m=stem)
hay = mat('hay', '#e1bf62', 0.9)
for (x, y) in [(9.5, 6), (11.5, 14), (-10, 20), (-9, -6)]:
    add(lambda: bpy.ops.mesh.primitive_cylinder_add(vertices=14, radius=0.7, depth=1.2), 'hay', (x, y, 0.7), rot=(0, math.radians(90), 0), m=hay)
hill = mat('hill', '#8aa36a', 0.95)
for i in range(9):
    x = -260 + i * 65 + rnd.uniform(-20, 20); r = rnd.uniform(60, 110)
    add(lambda: bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=1), 'hill', (x, 330 + rnd.uniform(-30, 60), -r * 0.55),
        (r, r * 0.6, r * 0.8), m=hill, smooth=True)
    bpy.context.active_object.data.polygons.foreach_set('use_smooth', [True] * len(bpy.context.active_object.data.polygons))

# ------------------------------------------------------------------ turkey
T = build_turkey(C)
tparts = [o for o in bpy.data.objects if o.name.startswith('TURKEY_')]


def key(o, path, f, val):
    setattr(o, path, val); o.keyframe_insert(path, frame=f)


for f in range(F0, F1):
    # position + heading
    if f <= STOP:
        u = f / STOP; x = TX0 + (LANE - TX0) * (u if u < 0.85 else 0.85 + (1 - (1 - (u - 0.85) / 0.15) ** 2) * 0.15)
        walking = True
    else:
        x = LANE; walking = f < STOP + 4
    key(T['root'], 'location', f, Vector((x, 0, 0)))
    key(T['root'], 'rotation_euler', f, Euler((0, 0, math.radians(-90))))
    ph = 2 * math.pi * f / (2 * STEP)
    amp = 1.0 if f <= STOP else max(0.0, 1 - (f - STOP) / 4)
    # body roll / bob
    puff = 1.0
    if 135 <= f < IMPACT:
        puff = 1 + 0.13 * eout((f - 139) / 4) + 0.012 * math.sin(f * 2.7)
    key(T['body'], 'rotation_euler', f, Euler((0, math.radians(8) * math.sin(ph) * amp + (math.radians(2.5) * math.sin(f * 3.1) if 140 <= f < IMPACT else 0), 0)))
    key(T['body'], 'location', f, Vector((0, 0, 0.03 * abs(math.sin(ph)) * amp)))
    key(T['body'], 'scale', f, Vector((puff, puff, puff)))
    key(T['leg_l'], 'rotation_euler', f, Euler((math.radians(28) * math.sin(ph) * amp, 0, 0)))
    key(T['leg_r'], 'rotation_euler', f, Euler((-math.radians(28) * math.sin(ph) * amp, 0, 0)))
    key(T['tail'], 'rotation_euler', f, Euler((0, math.radians(5) * math.sin(ph + 0.6) * amp, 0)))
    key(T['tail'], 'scale', f, Vector((1 + 0.25 * eout((f - 139) / 4), 1, 1 + 0.2 * eout((f - 139) / 4))) if f >= 135 else Vector((1, 1, 1)))
    # head: bob while walking; snaps to camera on the cowbell drop-out (f81); turns to the headlights in s4
    yaw = 0.0; pitch = math.radians(10) * math.sin(2 * ph) * amp; roll = 0.0
    if 81 <= f < 135:
        yaw = math.radians(90) * eout((f - 81) / 3)
        roll = math.radians(14) * ease((f - 100) / 4)
    if f >= 135:
        yaw = math.radians(-90); pitch = math.radians(-6)
    key(T['head'], 'rotation_euler', f, Euler((pitch, roll, yaw)))
    blink = 1.0
    for b in (88, 97, 120):
        if b <= f < b + 2:
            blink = 0.12
    big = 1 + 0.32 * eout((f - 139) / 3) if f >= 135 else 1.0
    for e in (T['eye_l'], T['eye_r']):
        key(e, 'scale', f, Vector((big, big, big * blink)))
    hide = f >= IMPACT
    for o in tparts:
        if o.type == 'MESH':
            o.hide_render = hide; o.keyframe_insert('hide_render', frame=f)

# ------------------------------------------------------------------ the GR Corolla (lookbook GLB, V2 kit, plates as in the GLB)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
imported = [o for o in bpy.data.objects if o not in before]
# BF6 fitment fix (owner via parent, 2026-11-18): the lookbook V2 spats hang ~16 mm under the bumper; seat them with BF6's fit
# (2 deg pitch about the part centre, +10 mm rearward, +14 mm up; projects/bf-gr-corolla-track/spat_v2_fit.json)
import json as _json
_f = _json.load(open('/home/user/Illumaesthetic-Video-Editor/projects/bf-gr-corolla-track/spat_v2_fit.json'))
bpy.context.view_layer.update()
for _o in imported:
    if _o.name.split('.')[0] == 'part_rear_spats_v2':
        _piv = Vector(_f['pivot'])
        _T = Matrix.Translation(_piv + Vector((0, _f['dy'], _f['dz']))) @ Matrix.Rotation(math.radians(_f['pitch']), 4, 'X') @ Matrix.Translation(-_piv)
        _mw = _o.matrix_world.copy(); _o.parent = None; _o.matrix_world = _T @ _mw
car = bpy.data.objects.new('CAR', None); C.objects.link(car)
KEEP = {'part_front_lip_v2', 'part_side_skirts_v2', 'part_rear_spats_v2'}
pu = _metal('pu_black', '#141414', 0.55, 0.0)
for o in imported:
    base = o.name.split('.')[0]
    if o.type == 'MESH' and ((base.startswith('part_') and base not in KEEP) or base == 'livery_castrol'):
        o.hide_render = True
    if o.type == 'MESH' and base in KEEP:
        o.data.materials.clear(); o.data.materials.append(pu)
    if o.parent is None:
        o.parent = car
for m in bpy.data.materials:
    if not m.node_tree:
        continue
    p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not p:
        continue
    if m.name.startswith('paint'):
        p.inputs['Base Color'].default_value = srgb('#b21522'); p.inputs['Roughness'].default_value = 0.2
        p.inputs['Metallic'].default_value = 0.35; p.inputs['Coat Weight'].default_value = 1.0; p.inputs['Coat Roughness'].default_value = 0.03
    if m.name.startswith('light_inner'):
        p.inputs['Emission Color'].default_value = (1.0, 0.95, 0.85, 1); p.inputs['Emission Strength'].default_value = 25.0
# headlight beams (spot lights parented to the car) + glow cards so the lights read from far down the road
glow = toon('hl_glow', '#fff4dc', 0.3, emit=60.0)
for s in (1, -1):
    sp = bpy.data.lights.new('hl', 'SPOT'); sp.energy = 900 if SHOT in ('s4_eyes',) else 250; sp.spot_size = math.radians(55)
    sp.spot_blend = 0.4; sp.color = (1.0, 0.95, 0.85); sp.shadow_soft_size = 0.08
    so_ = bpy.data.objects.new('hl', sp); C.objects.link(so_); so_.parent = car; so_.location = (s * 0.68, -2.25, 0.72)
    so_.rotation_euler = (math.radians(85), 0, math.radians(180))
    if SHOT in ('s1_cross', 's2_look'):
        g = add(lambda: bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.22), 'hlglow', (s * 0.68, -2.1, 0.72), m=glow)
        g.parent = car
bpy.context.view_layer.update()
hubs = []
for o in [o for o in bpy.data.objects if o.name.startswith('wheel_')]:
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]; ctr = sum(bb, Vector()) / 8; r = max(v.z for v in bb) / 2
    piv = bpy.data.objects.new('hub_' + o.name, None); C.objects.link(piv); piv.location = ctr; piv.parent = car
    bpy.context.view_layer.update()
    mw = o.matrix_world.copy(); o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted(); o.matrix_world = mw
    hubs.append((piv, r))
for f in range(F0 - 1, F1 + 1):
    key(car, 'location', f, Vector((LANE, car_y(f), 0)))
    for piv, r in hubs:
        key(piv, 'rotation_euler', f, Euler((V * f / r, 0, 0)))
for o in [car] + [p for p, _ in hubs]:
    if o.animation_data and o.animation_data.action:
        act = o.animation_data.action
        fcs = act.fcurves if hasattr(act, 'fcurves') else [fc for l in act.layers for st in l.strips for cb in st.channelbags for fc in cb.fcurves]
        for fc in fcs:
            for k in fc.keyframe_points:
                k.interpolation = 'LINEAR'

# ------------------------------------------------------------------ POOF cloud + feathers (from the impact on)
HIT = Vector((LANE - 0.1, 0.0, 0.55))
if SHOT in ('s5_poof', 's6_feath'):
    puffm = toon('puff', '#ffffff', 0.9, emit=0.5)
    if SHOT == 's5_poof':
        for i in range(18):
            d = Vector((rnd.uniform(-1, 1), rnd.uniform(-0.6, 0.6), rnd.uniform(-0.4, 1))).normalized() * rnd.uniform(0.15, 0.6)
            rr = rnd.uniform(0.28, 0.55)
            pf = add(lambda: bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1), 'puff', HIT + d, m=puffm, smooth=True)
            for p in pf.data.polygons:
                p.use_smooth = True
            for f in range(F0, F1):
                t = f - IMPACT
                g = eout(t / 5) * (1 - ease((t - 16 - i % 5) / 14))
                key(pf, 'scale', f, Vector((rr, rr, rr)) * max(g, 0.0001) * (1 + 0.25 * eout(t / 20)))
                key(pf, 'location', f, HIT + d * (1 + 0.8 * eout(t / 12)) + Vector((0, 0, 0.35 * ease(t / 30))))
    fm = feather_mesh('flyfeather')
    fmats = [toon(f'ff{c}', c, 0.65) for c in TAIL_COLS + ['#7a4a2a', '#f2dcae', '#6b4126']]
    N_BURST, N_RAIN = 70, 26
    feathers = []
    for i in range(N_BURST + N_RAIN):
        o = bpy.data.objects.new(f'feather{i}', fm); C.objects.link(o); o.data.materials.append(fmats[i % len(fmats)])
        # all feathers share one mesh, so per-object materials go on the object slot
        o.material_slots[0].link = 'OBJECT'; o.material_slots[0].material = fmats[i % len(fmats)]
        o.rotation_mode = 'XYZ'; L = rnd.uniform(0.17, 0.3); o.scale = (L, L, L)
        if i < N_BURST:
            d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(0.1, 1.6))).normalized()
            p = HIT.copy(); v = d * rnd.uniform(3.0, 7.5) / FPS; t0 = IMPACT
        else:   # a second, gentle 'rain' of feathers near the camera for the text plate
            p = Vector((rnd.uniform(0.6, 3.4), rnd.uniform(-2.2, 1.8), rnd.uniform(1.6, 3.2))); v = Vector((0, 0, 0)); t0 = 200
        rot = Vector((rnd.uniform(0, 6), rnd.uniform(0, 6), rnd.uniform(0, 6))); wv = Vector((rnd.uniform(-.3, .3), rnd.uniform(-.3, .3), rnd.uniform(-.3, .3)))
        ph = rnd.uniform(0, 6.28); feathers.append((o, p, v, rot, wv, t0, ph))
    G = 1.4 / FPS / FPS; K = 0.88
    for o, p, v, rot, wv, t0, ph in feathers:
        p = p.copy(); v = v.copy(); rot = rot.copy(); landed = False
        sim = float(IMPACT)
        while True:
            out = sim if sim < SLOW_AT else SLOW_AT + (sim - SLOW_AT) / SLOW   # video frame of this sim time
            if out >= F1:
                break
            st = 1.0 if sim < SLOW_AT else SLOW
            if out >= F0 and abs(out - round(out)) < 1e-6:
                f = int(round(out)); vis = sim >= t0
                o.hide_render = not vis; o.keyframe_insert('hide_render', frame=f)
                key(o, 'location', f, p.copy()); key(o, 'rotation_euler', f, Euler(tuple(rot)))
            if sim >= t0 and not landed:
                v.z -= G * st
                v *= K ** st
                p += v * st + Vector((0.006 * math.sin(sim * 0.21 + ph), 0.004 * math.cos(sim * 0.17 + ph), 0)) * st
                rot += wv * (0.6 + v.length * 20) * st
                if p.z <= 0.012:
                    p.z = 0.012; landed = True; rot = Vector((math.radians(90), 0, rot.z))
            sim += st

# ------------------------------------------------------------------ cameras (keyed per frame)
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); C.objects.link(cam); sc.camera = cam
cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 20.25; cd.clip_start = 0.02; cd.clip_end = 3000
cam.rotation_mode = 'XYZ'


def look(loc, tgt, roll=0.0):
    loc, tgt = Vector(loc), Vector(tgt)
    q = (tgt - loc).to_track_quat('-Z', 'Y')
    return Matrix.Translation(loc) @ q.to_matrix().to_4x4() @ Matrix.Rotation(math.radians(roll), 4, 'Z')


def lerp(p, q, u):
    return Vector(p).lerp(Vector(q), u)


for f in range(F0, F1):
    u = (f - F0) / max(F1 - F0 - 1, 1)
    roll = 0
    if SHOT == 's1_cross':
        cd.lens = 32
        loc = lerp((2.15, -3.1, 0.36), (1.95, -2.9, 0.36), u); tgt = lerp((2.25, 0, 0.22), (2.05, 0, 0.22), u)
    elif SHOT == 's2_look':
        cd.lens = 35
        uu = ease(u)
        loc = lerp((1.75, -3.3, 0.42), (1.62, -1.75, 0.74), uu); tgt = lerp((1.75, 0, 0.62), (1.62, 0, 0.82), uu)
    elif SHOT == 's3_car':
        cd.lens = 24
        yn = car_y(f) - 2.27; d = 6.2 + (3.0 - 6.2) * u
        loc = (LANE + 0.75, yn - d, 0.3); tgt = (LANE - 0.1, yn + 1.0, 0.62); roll = 0
    elif SHOT == 's4_eyes':
        cd.lens = 38
        loc = lerp((1.6, 1.25, 0.95), (1.58, 0.95, 0.93), ease(u)); tgt = (1.56, 0.05, 0.86)
        roll = 1.2 * math.sin(f * 2.3) * ease((f - 140) / 6)
    elif SHOT == 's5_poof':
        cd.lens = 22
        t = f - IMPACT; sh = 0.06 * math.exp(-t / 4) if t < 14 else 0
        loc = (-1.6 + sh * math.sin(t * 2.9), -4.6 + sh * math.cos(t * 3.7), 0.85 + sh * math.sin(t * 4.1)); tgt = (1.6, 0.4, 0.8)
    elif SHOT == 's6_feath':
        cd.lens = 26
        loc = lerp((3.0, -3.4, 0.32), (2.9, -3.1, 0.34), u); tgt = (1.6, 0.6, 0.9)
    cam.matrix_world = look(loc, tgt, roll)
    cam.keyframe_insert('location', frame=f); cam.keyframe_insert('rotation_euler', frame=f)
    cd.keyframe_insert('lens', frame=f)

# lens shift: keep the subject clear of the right-rail buttons (knowledge/safe-zones.md)
cd.shift_x = 0.04
os.makedirs(OUT, exist_ok=True)
sc.render.filepath = os.path.join(OUT, 'f_####')
if '--still' in sys.argv:
    pass
bpy.ops.render.render(animation=True)
print('DONE', SHOT, F0, F1 - 1)
