"""v9 front-end clean-up of the trimmed stock scan (user: "the front end still has some weird artifacting and clipping").
1. Notches: the v7 ray trim removed stock faces at the top corners of the Bomex grille opening that the kit does not
   cover, leaving holes you could see into the car through. Restore the untrimmed faces (from the kb6 source) that are
   missing from the target inside --restore boxes.
2. Clipping: the stock lower grille frame pokes through the kit lip at the lower corners of the opening (the trim test
   left it because the grille duct is excluded). Delete target faces inside --clip boxes that lie within --near m of the
   kit front bumper surface.
  blender -b -P fix_front.py -- src_untrimmed.blend target.blend k_front_bumper.blend out.blend
Boxes are world (prepped, undropped) metres: x0,x1,y0,y1,z0,z1."""
import bpy, bmesh, sys
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree
from mathutils.bvhtree import BVHTree

a = sys.argv[sys.argv.index("--") + 1:]
SRC, TGT, KIT, OUT = a[:4]
RESTORE = [(-0.70, -0.49, -2.25, -1.90, 0.50, 0.66), (0.32, 0.53, -2.25, -1.90, 0.50, 0.66)]
CLIP = [(-0.70, 0.51, -2.16, -1.85, 0.10, 0.31)]
NEAR = 0.012


def load(path):
    with bpy.data.libraries.load(path, link=False) as (s, d):
        d.objects = list(s.objects)
    obs = [o for o in d.objects if o is not None]
    for o in obs: bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.update()
    return [o for o in obs if o.type == "MESH"]


def centres(ob):
    me = ob.data; n = len(me.polygons); c = np.empty(n * 3, np.float32); me.polygons.foreach_get("center", c)
    M = np.array(ob.matrix_world, np.float64); return c.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]


def inbox(c, boxes):
    sel = np.zeros(len(c), bool)
    for x0, x1, y0, y1, z0, z1 in boxes:
        sel |= (c[:, 0] > x0) & (c[:, 0] < x1) & (c[:, 1] > y0) & (c[:, 1] < y1) & (c[:, 2] > z0) & (c[:, 2] < z1)
    return sel


bpy.ops.wm.read_factory_settings(use_empty=True)
tgt = load(TGT)[0]; ct = centres(tgt)
# 2. clipping: target faces near the kit surface in the clip boxes
kit = load(KIT); verts, polys = [], []
for k in kit:
    M = k.matrix_world; off = len(verts)
    verts += [M @ v.co for v in k.data.vertices]; polys += [[off + i for i in p.vertices] for p in k.data.polygons]
bvh = BVHTree.FromPolygons(verts, polys)
cand = np.where(inbox(ct, CLIP))[0]
kill = [int(i) for i in cand if (lambda r: r[0] is not None and r[3] < NEAR)(bvh.find_nearest(Vector(ct[i])))]
# 1. notches: source faces in the restore boxes with no target face at the same centre
src = load(SRC)[0]; cs = centres(src)
sel = np.where(inbox(cs, RESTORE))[0]
tsel = np.where(inbox(ct, [(b[0] - 0.02, b[1] + 0.02, b[2] - 0.02, b[3] + 0.02, b[4] - 0.02, b[5] + 0.02) for b in RESTORE]))[0]
kd = KDTree(len(tsel))
for j, i in enumerate(tsel): kd.insert(Vector(ct[i]), j)
kd.balance()
miss = [int(i) for i in sel if kd.find(Vector(cs[i]))[2] > 0.0005]
# keep only faces that fill a see-through hole: not covered by the kit seen from the front (ray -Y misses it) and not
# standing proud of it (ray +Y does not hit the kit right behind) - the latter are the flaps the trim rightly removed
fwd, back = Vector((0, -1, 0)), Vector((0, 1, 0))
add = [i for i in miss if bvh.ray_cast(Vector(cs[i]) + fwd * 0.002, fwd, 0.4)[0] is None
       and bvh.ray_cast(Vector(cs[i]) + back * 0.002, back, 0.15)[0] is None]
for k in kit: bpy.data.objects.remove(k)
print("FIX clip faces removed", len(kill), "of", len(cand), "| notch faces restored", len(add), "of", len(miss), "missing")
# apply to the target mesh (target local coords)
bm = bmesh.new(); bm.from_mesh(tgt.data); bm.faces.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[bm.faces[i] for i in kill], context="FACES")
Mi = tgt.matrix_world.inverted() @ src.matrix_world
sv = src.data.vertices; vmap = {}
for i in add:
    p = src.data.polygons[i]; vs = []
    for vi in p.vertices:
        if vi not in vmap: vmap[vi] = bm.verts.new(Mi @ sv[vi].co)
        vs.append(vmap[vi])
    try: bm.faces.new(vs)
    except ValueError: pass
bmesh.ops.remove_doubles(bm, verts=list(vmap.values()) + [v for v in bm.verts if False], dist=0.00001)
bm.to_mesh(tgt.data); bm.free()
bpy.data.objects.remove(src)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
