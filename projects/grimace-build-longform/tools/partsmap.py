"""Parts map on the finished-car model (Blender, Cycles CPU): x-ray body with glowing markers at the six part zones.
usage: blender -b <grimace_glb.blend> --python partsmap.py -- prep <out.blend>     decimate + stand the car up (Z up, nose +Y), save
       blender -b <prepped.blend> --python partsmap.py -- still <out.png> [hero|xray] [azimuth_deg]
The GLB has no suspension, brake or steering geometry, so the zones are illustrated markers, not the real parts."""
import bpy, sys, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
sc = bpy.context.scene


def bounds(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    return Vector([min(p[i] for p in pts) for i in range(3)]), Vector([max(p[i] for p in pts) for i in range(3)])


if a[0] == 'prep':
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    for o in meshes:
        n = len(o.data.polygons)
        r = 0.04 if n > 1e6 else 0.15 if n > 2e5 else 0.4 if n > 5e4 else 1
        if r < 1:
            bpy.context.view_layer.objects.active = o
            m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = r
            bpy.ops.object.modifier_apply(modifier=m.name)
    root = bpy.data.objects.new('CAR', None); sc.collection.objects.link(root)
    for o in bpy.data.objects:
        if o.parent is None and o is not root: o.parent = root
    root.rotation_euler = (math.radians(-90), 0, 0)        # model is -Y up, +Z nose  ->  Z up, +Y nose
    bpy.context.view_layer.update()
    mn, mx = bounds([o for o in bpy.data.objects if o.type == 'MESH'])
    root.location = (-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z)
    bpy.context.view_layer.update()
    print('PREPPED tris', sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH'), 'bounds', bounds([o for o in bpy.data.objects if o.type == 'MESH']))
    bpy.ops.wm.save_as_mainfile(filepath=a[1])
elif a[0] == 'batch':
    # usage: ... -- batch <outdir> [test]   renders: intro orbit, five chapter stills + 'all' still, recap orbit (12 fps, 1280x720)
    import os
    OUT = a[1]; TEST = len(a) > 2
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    mn, mx = bounds(meshes); L, Wd, Ht = mx.y - mn.y, mx.x - mn.x, mx.z - mn.z
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 32; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720
    sc.cycles.transparent_max_bounces = 32; sc.cycles.max_bounces = 32
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.012, 0.014, 0.022, 1)
    sc.view_settings.view_transform = 'Standard'

    def emis(name, col, strength):
        m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        o_ = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
        e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = strength; nt.links.new(e.outputs[0], o_.inputs[0]); return m, e
    xm = bpy.data.materials.new('xray'); xm.use_nodes = True; nt = xm.node_tree; nt.nodes.clear()
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); mix = nt.nodes.new('ShaderNodeMixShader'); tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    em = nt.nodes.new('ShaderNodeEmission'); lw = nt.nodes.new('ShaderNodeLayerWeight'); pw = nt.nodes.new('ShaderNodeMath')
    em.inputs[0].default_value = (0.45, 0.30, 0.95, 1); em.inputs[1].default_value = 0.8; lw.inputs[0].default_value = 0.35
    pw.operation = 'POWER'; pw.inputs[1].default_value = 2.4
    nt.links.new(lw.outputs['Facing'], pw.inputs[0]); nt.links.new(pw.outputs[0], mix.inputs[0])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], o_.inputs[0])
    for o in meshes:
        o.data.materials.clear(); o.data.materials.append(xm)

    COL = dict(coilovers=(1.0, 0.30, 0.16), bushings=(0.25, 1.0, 0.45), brakes=(1.0, 0.72, 0.10), bracing=(0.92, 0.92, 1.0),
               swaybars=(0.95, 0.35, 0.95), steering=(0.25, 0.75, 1.0))
    MAT = {k: emis(k, c, 1.6) for k, c in COL.items()}

    def add(obj, grp):
        obj.data.materials.append(MAT[grp][0]); return obj

    def cyl(p, q, r, grp):
        p, q = Vector(p), Vector(q); d = q - p
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(p + q) / 2, vertices=24)
        o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = d.to_track_quat('Z', 'Y'); return add(o, grp)

    def torus(loc, R, r, grp, axis=(0, 0, 1)):
        bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, major_segments=32, minor_segments=10)
        o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector(axis).to_track_quat('Z', 'Y'); return add(o, grp)

    def box(loc, size, grp):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = size; return add(o, grp)

    fy, ry = L * 0.5 - 0.72, -L * 0.5 + 0.86      # axle lines, from where the wheels sit in the model (illustrative)
    hw = Wd * 0.5 - 0.16
    for sx in (-1, 1):
        for y, front in ((fy, True), (ry, False)):
            lo, hi = Vector((sx * (hw - 0.10), y, 0.26)), Vector((sx * (hw - 0.22), y - 0.02, 0.70))
            cyl(lo, hi, 0.022, 'coilovers')
            for k in range(7):
                torus(lo.lerp(hi, 0.42 + 0.075 * k), 0.052, 0.011, 'coilovers', hi - lo)
            cyl((sx * (hw + 0.012), y, 0.30), (sx * (hw - 0.012), y, 0.30), 0.15 if front else 0.12, 'brakes')
            box((sx * hw, y - 0.11, 0.37), (0.075, 0.10, 0.14) if front else (0.06, 0.07, 0.10), 'brakes')
            for dy in (-0.13, 0.13):
                for z in (0.21, 0.43):
                    torus((sx * (hw - 0.37), y + dy, z), 0.032, 0.014, 'bushings', (0, 1, 0))
        cyl((sx * (hw - 0.03), fy - 0.42, 0.66), (sx * (hw - 0.06), fy - 0.80, 0.30), 0.016, 'bracing')       # fender brace
        cyl((sx * 0.30, fy + 0.16, 0.27), (sx * (hw - 0.07), fy + 0.13, 0.29), 0.012, 'steering')              # tie rod
        cyl((sx * (hw - 0.26), fy + 0.34, 0.21), (sx * (hw - 0.20), fy + 0.06, 0.24), 0.013, 'swaybars')       # front bar arm
        cyl((sx * (hw - 0.30), ry - 0.30, 0.25), (sx * (hw - 0.22), ry - 0.05, 0.27), 0.011, 'swaybars')       # rear bar arm
    cyl((-(hw - 0.22), fy - 0.02, 0.71), (hw - 0.22, fy - 0.02, 0.71), 0.018, 'bracing')                       # strut tower brace
    cyl((-(hw - 0.26), fy + 0.34, 0.21), (hw - 0.26, fy + 0.34, 0.21), 0.013, 'swaybars')
    cyl((-(hw - 0.30), ry - 0.30, 0.25), (hw - 0.30, ry - 0.30, 0.25), 0.011, 'swaybars')
    cyl((-0.30, fy + 0.16, 0.27), (0.30, fy + 0.16, 0.27), 0.024, 'steering')                                   # rack
    cyl((-0.20, fy + 0.16, 0.27), (-0.36, 0.42, 0.80), 0.010, 'steering')                                       # column
    torus((-0.36, 0.36, 0.84), 0.17, 0.014, 'steering', (0, 1, -0.45))                                          # steering wheel

    tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt); tgt.location = (0, 0, Ht * 0.40)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.lens = 50
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'

    def shot(path, az, hl='all', dist=6.6, h=2.3):
        for k, (m, e) in MAT.items():
            e.inputs[1].default_value = 1.6 if hl == 'all' else (2.4 if k == hl else 0.12)
        azr = math.radians(az); cam.location = (dist * math.sin(azr), dist * math.cos(azr), h)
        sc.render.filepath = path; bpy.ops.render.render(write_still=True)

    os.makedirs(OUT, exist_ok=True)
    VIEW = dict(coilovers=(40, 5.6, 1.9), bushings=(28, 5.2, 1.5), brakes=(55, 5.4, 1.6), bracing=(20, 5.6, 2.6), swaybars=(150, 6.0, 2.4), steering=(-30, 5.4, 2.6))
    shot(f'{OUT}/still_all.png', 35)
    if not TEST:
        for k, (az, d, h) in VIEW.items(): shot(f'{OUT}/still_{k}.png', az, k, d, h)
        for name, n, a0, a1 in (('intro', 96, 60, 10), ('recap', 144, 35, 395)):
            os.makedirs(f'{OUT}/{name}', exist_ok=True)
            for i in range(n): shot(f'{OUT}/{name}/{i:04d}.png', a0 + (a1 - a0) * i / (n - 1))
else:
    out, look, az = a[1], (a[2] if len(a) > 2 else 'xray'), math.radians(float(a[3]) if len(a) > 3 else 35)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    mn, mx = bounds(meshes); L, Wd, Ht = mx.y - mn.y, mx.x - mn.x, mx.z - mn.z
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1280, 720; sc.render.film_transparent = False
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.012, 0.014, 0.022, 1) if look == 'xray' else (0.05, 0.05, 0.06, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
    if look == 'xray':
        m = bpy.data.materials.new('xray'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        o_ = nt.nodes.new('ShaderNodeOutputMaterial'); mix = nt.nodes.new('ShaderNodeMixShader'); tr = nt.nodes.new('ShaderNodeBsdfTransparent')
        em = nt.nodes.new('ShaderNodeEmission'); lw = nt.nodes.new('ShaderNodeLayerWeight'); pw = nt.nodes.new('ShaderNodeMath')
        em.inputs[0].default_value = (0.45, 0.30, 0.95, 1); em.inputs[1].default_value = 1.6; lw.inputs[0].default_value = 0.35
        pw.operation = 'POWER'; pw.inputs[1].default_value = 2.2
        nt.links.new(lw.outputs['Facing'], pw.inputs[0]); nt.links.new(pw.outputs[0], mix.inputs[0])
        nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], o_.inputs[0])
        for o in meshes:
            o.data.materials.clear(); o.data.materials.append(m)
        sc.cycles.transparent_max_bounces = 32; sc.cycles.max_bounces = 32

        def marker(name, loc, col, r=0.07):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc); s = bpy.context.object; s.name = name
            mm = bpy.data.materials.new(name); mm.use_nodes = True; nt2 = mm.node_tree; nt2.nodes.clear()
            oo = nt2.nodes.new('ShaderNodeOutputMaterial'); e = nt2.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (*col, 1); e.inputs[1].default_value = 12
            nt2.links.new(e.outputs[0], oo.inputs[0]); s.data.materials.append(mm)
        fx, rx = L * 0.5 - 0.72, -L * 0.5 + 0.86          # axle lines (illustrative, from the wheel positions)
        hw = Wd * 0.5 - 0.16
        for sx in (-1, 1):
            for y in (fx, rx):
                marker('coilover', (sx * (hw - 0.14), y, 0.62), (1.0, 0.25, 0.2))
                marker('brake', (sx * hw, y, 0.30), (1.0, 0.75, 0.1))
                marker('bushing', (sx * (hw - 0.34), y, 0.24), (0.2, 0.9, 0.4), 0.05)
            marker('tierod', (sx * (hw - 0.22), fx + 0.12, 0.27), (0.2, 0.7, 1.0), 0.05)
            marker('brace', (sx * (hw - 0.18), fx + 0.0, 0.80), (1.0, 1.0, 1.0), 0.05)
        marker('swayF', (0, fx + 0.30, 0.22), (0.9, 0.3, 0.9), 0.05); marker('swayR', (0, rx - 0.25, 0.26), (0.9, 0.3, 0.9), 0.05)
    else:
        bpy.ops.object.light_add(type='AREA', location=(2.5, 3.5, 4)); k = bpy.context.object; k.data.energy = 2500; k.data.size = 5
        bpy.ops.object.light_add(type='AREA', location=(-4, -2, 3)); f = bpy.context.object; f.data.energy = 900; f.data.size = 6
        bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
    tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt); tgt.location = (0, 0, Ht * 0.42)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    d = 6.6; cam.location = (d * math.sin(az), d * math.cos(az), 2.3); cam.data.lens = 50
    c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
    sc.render.filepath = out; bpy.ops.render.render(write_still=True)
