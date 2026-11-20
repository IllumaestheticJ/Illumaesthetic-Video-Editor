"""blender -b -P tools/wheel_build.py -- rim_part.stl tyre_part.stl out.glb
Showroom wheel format from the TE37 scan (Drive STL 1PvGYb5luOlEnScSWFwCiPoSgtfzbYCUu), already oriented and split by
radius outside Blender: nodes rim / tyre, hub-centred, axle on X, face +X, metres. Stand-in for Epsilon-Site's
te37_wheel.py (repo not reachable from this session); no brake node: kit_render keeps the car's own disc and caliper."""
import bpy, sys
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
for path, name, mat, tris in ((a[0], "rim", "rim", 160000), (a[1], "tyre", "rubber", 160000)):
    bpy.ops.wm.stl_import(filepath=path)
    o = bpy.context.selected_objects[0]; o.name = name; o.data.name = name
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT"); bpy.ops.mesh.remove_doubles(threshold=1e-5); bpy.ops.object.mode_set(mode="OBJECT")
    m = o.modifiers.new("d", "DECIMATE"); m.ratio = min(1.0, tris / len(o.data.polygons)); bpy.ops.object.modifier_apply(modifier="d")
    bpy.ops.object.shade_smooth()
    mt = bpy.data.materials.new(mat); mt.use_nodes = True; o.data.materials.append(mt)
    b = mt.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.012, 0.012, 0.013, 1) if mat == "rubber" else (0.25, 0.25, 0.26, 1)
    b.inputs["Roughness"].default_value = 0.82 if mat == "rubber" else 0.3
    b.inputs["Metallic"].default_value = 0.0 if mat == "rubber" else 0.9
    print("WHEEL", name, len(o.data.polygons))
bpy.ops.export_scene.gltf(filepath=a[2], export_format="GLB", export_yup=True)
