"""v0 scene from Ron's files, memory-light: load only 'FE1 Fl' + his kit pieces, vertex-cluster the 20M-face scan
(5 mm cells) in numpy, drop floor scraps (z < 0.012 m), add wing.002 from his render .blend, save scene_v0.blend.
    blender -b --factory-startup -P prep_v0.py"""
import bpy, numpy as np, time
M = "/home/user/media/bf-scan-teardown-prices"; R = M + "/ron/"
t0 = time.time()
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
KIT = {"kit_lip": ["FrontFL1", "FrontFL2", "FrontFL3"], "kit_rear": ["Rear1", "Rear2", "Rear3"],
       "kit_skirt_L": ["SideDriver1", "SideDriver2"], "kit_skirt_R": ["SidePass1", "SidePass2"]}
names = ["FE1 Fl"] + sum(KIT.values(), [])
with bpy.data.libraries.load(R + "Civic 11th gen lip kit review.blend", link=False) as (s, d):
    d.objects = [n for n in s.objects if n in names]
sc = bpy.context.scene
for o in d.objects: sc.collection.objects.link(o)
bpy.context.view_layer.update()
print("loaded", time.time() - t0, flush=True)
car = bpy.data.objects["FE1 Fl"]; me = car.data
nv, nf = len(me.vertices), len(me.polygons)
v = np.empty(nv * 3, np.float32); me.vertices.foreach_get("co", v); v = v.reshape(-1, 3)
mw = np.array(car.matrix_world, np.float64); print("MW", mw.round(4).tolist(), car.parent, flush=True); v = (v @ mw[:3, :3].T + mw[:3, 3]).astype(np.float32)
f = np.empty(nf * 3, np.int32); me.polygons.foreach_get("vertices", f) if all(len(p.vertices) == 3 for p in me.polygons[:10]) else None
f = f.reshape(-1, 3)
print("tris", nv, nf, time.time() - t0, flush=True)
CELL = 0.005
q = np.floor(v / CELL).astype(np.int64); q -= q.min(0); D = int(q.max()) + 1
key = (q[:, 0] * D + q[:, 1]) * D + q[:, 2]
uk, inv = np.unique(key, return_inverse=True); inv = inv.ravel()
cnt = np.bincount(inv); nvv = np.zeros((len(uk), 3)); np.add.at(nvv, inv, v); nvv /= cnt[:, None]
del q, key, v
ff = inv[f]; del f
ok = (ff[:, 0] != ff[:, 1]) & (ff[:, 1] != ff[:, 2]) & (ff[:, 0] != ff[:, 2]); ff = ff[ok]
ff = np.unique(np.sort(ff, 1) * 0 + ff, axis=0) if False else ff
s3 = np.sort(ff, 1); _, ui = np.unique(s3, axis=0, return_index=True); ff = ff[np.sort(ui)]
zc = nvv[ff].mean(1)[:, 2]; ff = ff[zc > 0.012]
used = np.unique(ff); remap = -np.ones(len(nvv), np.int64); remap[used] = np.arange(len(used))
nvv = nvv[used]; ff = remap[ff]
print("clustered", len(nvv), len(ff), time.time() - t0, flush=True)
nm = bpy.data.meshes.new("car")
nm.vertices.add(len(nvv)); nm.vertices.foreach_set("co", nvv.astype(np.float32).ravel())
nm.loops.add(len(ff) * 3); nm.loops.foreach_set("vertex_index", ff.astype(np.int32).ravel())
nm.polygons.add(len(ff)); nm.polygons.foreach_set("loop_start", np.arange(0, len(ff) * 3, 3, dtype=np.int32))
nm.polygons.foreach_set("loop_total", np.full(len(ff), 3, np.int32))
nm.update(calc_edges=True); nm.validate(clean_customdata=False)
nm.polygons.foreach_set("use_smooth", np.ones(len(ff), bool))
old = car.data; car.data = nm; car.matrix_world.identity(); bpy.data.meshes.remove(old)
print("car mesh", len(nm.polygons), time.time() - t0, flush=True)
dg = bpy.context.evaluated_depsgraph_get()
for new, parts in KIT.items():
    objs = [bpy.data.objects[n] for n in parts]
    for o in objs:
        em = bpy.data.meshes.new_from_object(o.evaluated_get(dg)); o.modifiers.clear(); o.data = em
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); objs[0].name = new
with bpy.data.libraries.load(R + "Honda Civic Sedan 2022-render.blend", link=False) as (s, d):
    d.objects = [n for n in s.objects if n in ("wing.002", "Camera.006(L5)", "FL.001", "FR.001", "RL.001", "RR.001")]
for o in d.objects: sc.collection.objects.link(o)
w = bpy.data.objects["wing.002"]; dg = bpy.context.evaluated_depsgraph_get()
em = bpy.data.meshes.new_from_object(w.evaluated_get(dg)); w.modifiers.clear(); w.data = em; w.name = "kit_wing"
for n in ("FL", "FR", "RL", "RR"):
    bpy.data.objects[n + ".001"].name = "wheel_" + n   # Ron's wheels where he placed them (v5, approved)
for o in bpy.data.objects:
    if o.type == "MESH":
        if not o.name.startswith("wheel_"): o.data.materials.clear()
        bpy.ops.object.select_all(action="DESELECT"); o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        if o.name != "FE1 Fl":
            o.data.polygons.foreach_set("use_smooth", np.ones(len(o.data.polygons), bool))
        print("OBJ", o.name, len(o.data.polygons), [round(x, 3) for x in o.bound_box[0]], [round(x, 3) for x in o.bound_box[6]], flush=True)
bpy.ops.outliner.orphans_purge(do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=M + "/scene_v0.blend")
print("saved", time.time() - t0, flush=True)
