"""Blender: the wheel the car's original source file sits on, as a showroom-format wheel GLB (nodes rim / tyre, hub-centred, axle on X,
face +X) for `kit-render --wheels`.      blender -b -P tools/source_wheel.py -- MR-S_1.blend out.glb
Source: MR-S_1.blend (Drive folder "MRS"), scene "Scene", collection WHEELS: rim `wor_crkai_wheel_wheel_inner_rim_.004` (a Forza
"Work CR Kai" wheel, i.e. an aftermarket design, not Toyota's factory five-spoke: the folder holds no factory wheel) and tyre
`Tire main.009`. The file's Brembo kit is left out; the car model's own disc and caliper stay."""
import bpy, sys, math, numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(a[0], link=False) as (src, dst):
    dst.objects = ["wor_crkai_wheel_wheel_inner_rim_.004", "Tire main.009"]
rim, tyre = dst.objects
sc = bpy.context.scene
mats = {}
def mat(name, col, metal, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = col; b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
    return m
M = {"rim": mat("rim", (0.62, 0.63, 0.65, 1), 1.0, 0.25), "rubber": mat("rubber", (0.02, 0.02, 0.02, 1), 0.0, 0.8)}
out = []
for o, name, mn in ((rim, "rim", "rim"), (tyre, "tyre", "rubber")):
    sc.collection.objects.link(o); W = o.matrix_world.copy(); o.parent = None; o.matrix_world = W
bpy.context.view_layer.update()
ctr = rim.matrix_world.translation.copy(); side = 1 if ctr.x < 0 else -1      # in this file the outer face of a wheel at -x points to +x (seen on a test render)
T = (Matrix.Rotation(math.pi, 4, "Z") if side < 0 else Matrix.Identity(4)) @ Matrix.Translation(-ctr)
for o, name, mn in ((rim, "rim", "rim"), (tyre, "tyre", "rubber")):
    me = o.data.copy()
    if name == "tyre":       # its parent empty (scale, position) is not loaded with it: centre it on the hub and size it as it sits in the file (OD 0.579 m)
        v = np.array([x.co[:] for x in me.vertices]); c = (v.min(0) + v.max(0)) / 2; k = 0.579 / (v[:, 2].max() - v[:, 2].min())
        me.transform(Matrix.Scale(k, 4) @ Matrix.Translation(Vector(-c)))
    else:
        me.transform(T @ o.matrix_world)
        if (T @ o.matrix_world).determinant() < 0: me.flip_normals()
        v = np.array([x.co[:] for x in me.vertices]); c = (v.min(0) + v.max(0)) / 2; c[0] = 0
        me.transform(Matrix.Translation(Vector(-c)))
    me.materials.clear(); me.materials.append(M[mn])
    for p in me.polygons: p.material_index = 0; p.use_smooth = True
    n = bpy.data.objects.new(name, me); sc.collection.objects.link(n); out.append(n)
    v = np.array([x.co[:] for x in me.vertices]); print("WHEEL", name, len(me.polygons), v.min(0).round(3), v.max(0).round(3))
for o in (rim, tyre): bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=a[1], export_format="GLB", export_apply=True, export_yup=True)
