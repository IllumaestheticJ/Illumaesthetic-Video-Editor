"""v0 preview renders for bf-paint-match-roulette.

blender -b --factory-startup -P render_v0.py -- <jobs.json>

jobs.json: {"out": dir, "res": [w,h], "samples": n, "cars": {name: {"glb":..., "scan": optional, "hide": [...]}},
            "jobs": [{"car":..., "name":..., "mode": "paint"|"base"|"mask"|"scan", "hex": "#rrggbb", "finish": "pearl"}]}
Camera: one shared rear-3/4 high "R-cam" in the lookbook frame (car along Y, rear at +Y, ground z=0).
"""
import bpy, sys, json, math, os
from mathutils import Vector

cfg = json.load(open(sys.argv[sys.argv.index('--') + 1]))
OUT = cfg['out']; os.makedirs(OUT, exist_ok=True)
W, H = cfg['res']
CAM = cfg.get('cam', {"loc": [3.9, 6.6, 2.75], "target": [0.0, 0.55, 0.62], "lens": 40})


def srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_rgb(h):
    h = h.lstrip('#')
    return [srgb_to_lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]


def setup_world():
    sc = bpy.context.scene
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = cfg.get('samples', 24)
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = False
    sc.view_settings.view_transform = 'AgX'
    try:
        sc.view_settings.look = 'AgX - Punchy'
    except Exception:
        pass
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.004, 0.004, 0.005, 1); bg.inputs[1].default_value = 1
    # floor: black, slightly glossy (house look: car on black)
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    fl = bpy.context.object; m = bpy.data.materials.new('floor'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.002, 0.002, 0.0025, 1)
    b.inputs['Roughness'].default_value = 0.5
    try: b.inputs['Specular IOR Level'].default_value = 0.0
    except Exception: pass
    fl.data.materials.append(m)
    # lights: big soft key over/behind, rim, fill
    def area(name, loc, rot, size, energy):
        bpy.ops.object.light_add(type='AREA', location=loc, rotation=[math.radians(a) for a in rot])
        l = bpy.context.object; l.data.size = size; l.data.energy = energy; l.visible_camera = False; l.visible_glossy = True; return l
    area('top', (0, 0.5, 6.0), (0, 0, 0), 6, 2600)
    area('key', (5.5, 6.5, 3.5), (60, 0, 140), 4, 2200)
    area('rim', (-5.0, -2.5, 2.8), (65, 0, -120), 3, 1200)
    area('fill', (1.5, -6.0, 2.0), (75, 0, 10), 4, 500)
    cam = bpy.data.cameras.new('cam'); cam.lens = CAM['lens']; cam.sensor_fit = 'AUTO'; cam.sensor_width = 36
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    co.location = Vector(CAM['loc'])
    d = Vector(CAM['target']) - co.location
    co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def paint_mat(name, hexc, finish):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*hex_rgb(hexc), 1)
    met = {'metallic': 0.55, 'pearl': 0.3, 'gloss': 0.0}.get(finish, 0.2)
    b.inputs['Metallic'].default_value = met
    b.inputs['Roughness'].default_value = 0.32 if finish != 'gloss' else 0.25
    try:
        b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Coat Roughness'].default_value = 0.04
    except Exception:
        pass
    return m


def silver_mat():
    m = bpy.data.materials.new('silver'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.48, 0.49, 0.51, 1); b.inputs['Metallic'].default_value = 0.75
    b.inputs['Roughness'].default_value = 0.42
    return m


def emit_mat(v):
    m = bpy.data.materials.new('e%s' % v); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (v, v, v, 1)
    o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0])
    return m


def set_mat(o, m):
    o.data.materials.clear(); o.data.materials.append(m)


def load_glb(p):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=p)
    return [o for o in bpy.data.objects if o not in before]


def clear_car():
    for o in list(bpy.data.objects):
        if o.get('car'):
            bpy.data.objects.remove(o, do_unlink=True)


cache = {}
setup_world()
for job in cfg['jobs']:
    car = cfg['cars'][job['car']]
    clear_car()
    objs = load_glb(car['glb'])
    for o in objs:
        o['car'] = 1
    meshes = [o for o in objs if o.type == 'MESH']
    wing = [o for o in meshes if o.name.split('.')[0] == car.get('wing', 'part_sport_wing')]
    for o in meshes:
        if o.name.split('.')[0] in car.get('hide', []):
            o.hide_render = True
    paint = None
    for mat in bpy.data.materials:
        if mat.name == 'paint':
            paint = mat
    mode = job['mode']
    if mode in ('paint', 'base'):
        pm = paint_mat('p_' + job['name'], job['hex'], job.get('finish', 'pearl'))
        for o in meshes:
            for i, s in enumerate(o.material_slots):
                if s.material and s.material.name.startswith('paint'):
                    o.material_slots[i].material = pm
        if mode == 'base':
            gl = bpy.data.materials.get('plastic_gloss')
            for o in wing:
                for i in range(len(o.material_slots)):
                    o.material_slots[i].material = gl
    elif mode == 'mask':
        blk, wht = emit_mat(0.0), emit_mat(1.0)
        for o in meshes:
            if o.hide_render:
                continue
            for i in range(len(o.material_slots)):
                o.material_slots[i].material = wht if o in wing else blk
    elif mode == 'scan':
        # hide the lookbook car, keep its wing (silver); load the scan in the same frame
        sil = silver_mat()
        for o in meshes:
            if o in wing:
                for i in range(len(o.material_slots)):
                    o.material_slots[i].material = sil
            else:
                o.hide_render = True
        so = load_glb(car['scan'])
        for o in so:
            o['car'] = 1
        sm = [o for o in so if o.type == 'MESH']
        for o in sm:
            set_mat(o, sil)
        # configurator scans: length along +X from 0, front at +X -> rotate so the front is at -Y, centre the length
        from mathutils import Matrix
        for o in sm:
            o.data.transform(o.matrix_world); o.parent = None; o.matrix_world = Matrix.Identity(4)
        pts = [v.co for o in sm for v in o.data.vertices]
        cx = (min(p.x for p in pts) + max(p.x for p in pts)) / 2
        cy = (min(p.y for p in pts) + max(p.y for p in pts)) / 2
        zmin = min(p.z for p in pts)
        M = Matrix.Rotation(math.radians(car.get('scan_rot', -90)), 4, 'Z') @ Matrix.Translation((-cx, -cy, -zmin))
        for o in sm:
            o.data.transform(M)
        # align heading to the lookbook body by PCA in plan view, then centre on the body's bbox
        import numpy as np
        def xy(objs):
            return np.array([(o.matrix_world @ v.co)[:3] for o in objs for v in o.data.vertices])
        P = xy(sm)
        body = [o for o in meshes if o.name.split('.')[0] == 'body']
        B = xy(body)
        def ang(A):
            c = A[:, :2] - A[:, :2].mean(0); w, v = np.linalg.eigh(np.cov(c.T)); e = v[:, np.argmax(w)]
            return math.atan2(e[0], e[1])
        da = ang(B) - ang(P)
        da = (da + math.pi / 2) % math.pi - math.pi / 2
        print('SCAN heading correction deg', math.degrees(da), flush=True)
        R = Matrix.Rotation(-da, 4, 'Z')
        for o in sm:
            o.data.transform(R)
        P = xy(sm)
        off = Vector(((B[:, 0].min() + B[:, 0].max()) / 2 - (P[:, 0].min() + P[:, 0].max()) / 2,
                      (B[:, 1].min() + B[:, 1].max()) / 2 - (P[:, 1].min() + P[:, 1].max()) / 2,
                      B[:, 2].min() - 0.17 - P[:, 2].min() + 0.0))
        off.z = 0.0
        for o in sm:
            o.data.transform(Matrix.Translation(off))
        print('SCAN offset', tuple(round(x, 3) for x in off), 'scan bbox', P.min(0).round(3), P.max(0).round(3), 'body', B.min(0).round(3), B.max(0).round(3), flush=True)
    c = job.get('cam', CAM); co = bpy.context.scene.camera
    co.location = Vector(c['loc']); co.data.lens = c['lens']
    co.rotation_euler = (Vector(c['target']) - co.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.render.filepath = os.path.join(OUT, job['name'] + '.png')
    bpy.ops.render.render(write_still=True)
    print('RENDERED', job['name'], flush=True)
