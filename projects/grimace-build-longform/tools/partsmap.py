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
