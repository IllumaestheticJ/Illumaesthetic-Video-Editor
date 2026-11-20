import bpy, sys, numpy as np, bmesh
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=a[0])
for o in bpy.context.scene.objects:
    if o.type != "MESH": continue
    top = o
    while top.parent: top = top.parent
    me = o.data; M = np.array(o.matrix_world)
    v = np.array([x.co[:] for x in me.vertices]); v = v @ M[:3, :3].T + M[:3, 3]
    mats = [m.name for m in me.materials]
    img = [n.image.name for m in me.materials if m and m.use_nodes for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image]
    print(f"{top.name:28s} {o.name:44s} tris {len(me.polygons):6d} mats {mats} img {img} lo {v.min(0).round(2)} hi {v.max(0).round(2)}")
print("images", [(i.name, i.size[:]) for i in bpy.data.images])
