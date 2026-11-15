"""v11 (user: "re-animate the front bumper as old bumper off, new bumper on").
OLD = the real stock bumper scan (bumper_shell_v5, registered in place) comes off whole. This writes
  - <out_post>: the pre-kit car with every face within --tol of the stock bumper removed (factory grille kept), shown
    while the bumper is off;
  - <out_kept>: the stock faces the finished car still shows (they lie on the old bumper but survived the kit trim:
    grille surround, nose strip); they fly in with the Bomex bumper so the finished front (kb9B) appears without a pop.
  blender -b -P old_bumper.py -- pre.blend final.blend stock_bumper.blend out_post.blend out_kept.blend"""
import bpy, bmesh, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index("--") + 1:]; PRE, FIN, OLD, OUT_POST, OUT_KEPT = a[:5]; KITS = a[5:]
# v12 (user: "the old bumper comes off but there's still a bumper on the car"): no grille exemption box (it kept the
# bumper's lower bar and surround frame on the car), and KEPT = only stock faces you can actually see on the finished
# car (a ray escapes past the kit), not the stock skin hidden under the kit
DIRS = [Vector(d).normalized() for d in ((0, -1, 0), (0.6, -1, 0), (-0.6, -1, 0), (1, -0.3, 0), (-1, -0.3, 0), (0, -1, 0.5), (0, -1, -0.5))]
TOL = 0.010
GRILLE = (-0.605, 0.435, 0.10, 0.548, -1.55)  # = shots GRILLE recess box  # x0 x1 z0 z1 y-max: factory grille stays on the car


def load(p):
    with bpy.data.libraries.load(p, link=False) as (s, d): d.objects = list(s.objects)
    obs = [o for o in d.objects if o]
    for o in obs: bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.update(); return [o for o in obs if o.type == "MESH"]


def centres(ob):
    me = ob.data; n = len(me.polygons); c = np.empty(n * 3); me.polygons.foreach_get("center", c)
    M = np.array(ob.matrix_world); return c.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]


def on_old(ob):
    c = centres(ob); gx0, gx1, gz0, gz1, gy = GRILLE
    grille = (c[:, 0] > gx0) & (c[:, 0] < gx1) & (c[:, 2] > gz0) & (c[:, 2] < gz1) & (c[:, 1] < gy)
    near = np.array([(lambda r: r[0] is not None and r[3] < TOL)(bvh.find_nearest(Vector(p))) if p[1] < -1.3 else False for p in c])
    # the stock bumper's lower lip is not in the Bumper_Only scan: take it off with the bumper
    low = (c[:, 1] < -1.88) & (c[:, 2] < 0.27) & (np.abs(c[:, 0] + 0.075) < 0.98)
    on_old.extra = low & ~near
    return near | low


def keep_faces(ob, mask, out):
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[i] for i in np.where(~mask)[0]], context="FACES"); bm.to_mesh(ob.data); bm.free()
    for o in list(bpy.context.scene.objects):
        if o.type == "MESH" and o is not ob: bpy.data.objects.remove(o)
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)


bpy.ops.wm.read_factory_settings(use_empty=True)
V, P = [], []
for k in load(OLD):
    M = k.matrix_world; off = len(V); V += [M @ v.co for v in k.data.vertices]; P += [[off + i for i in p.vertices] for p in k.data.polygons]
    bpy.data.objects.remove(k)
bvh = BVHTree.FromPolygons(V, P)
pre = load(PRE)[0]; m = on_old(pre); ex = on_old.extra.copy(); print("POST: removed", int(m.sum()), "of", len(m), "lower lip", int(ex.sum()))
keep_faces(pre, ~m, OUT_POST)
bpy.ops.wm.read_factory_settings(use_empty=True)
pre = load(PRE)[0]; keep_faces(pre, ex, OUT_POST.replace(".blend", "_lip.blend"))  # rides off with the old bumper
bpy.ops.wm.read_factory_settings(use_empty=True)
KV, KP = [], []
for kp in KITS:
    for k in load(kp):
        M = k.matrix_world; off = len(KV); KV += [M @ v.co for v in k.data.vertices]; KP += [[off + i for i in p.vertices] for p in k.data.polygons]
        bpy.data.objects.remove(k)
kbvh = BVHTree.FromPolygons(KV, KP)
fin = load(FIN)[0]; m = on_old(fin)
Mr = fin.matrix_world.to_3x3(); cf = centres(fin)
def visible(i):
    c = Vector(cf[i]); n = (Mr @ fin.data.polygons[i].normal).normalized()
    for d in DIRS:
        if d.dot(n) < -0.1: continue
        if kbvh.ray_cast(c + d * 0.003, d, 1.0)[0] is None: return True
    return False
m = np.array([bool(x) and visible(i) for i, x in enumerate(m)]); print("KEPT stock faces on the finished car:", int(m.sum())); keep_faces(fin, m, OUT_KEPT)
