"""Count front-wheel points that poke through the kit (fender / bumper / canard) - a point clips when kit surface lies
both inboard and outboard of it along X (inside the shell) or it sits outboard of a kit surface that is directly
behind it within the arch footprint. Body pieces are dropped by --drop (wheels stay on the ground).
  blender -b -P wheel_clip.py -- drop wheel.blend [wheel.blend ...]"""
import bpy, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index("--") + 1:]; DROP = float(a[0]); WHEELS = a[1:]
B = "/home/user/media/work/z400/blend"
KIT = ["front_fender_pass", "front_fender_driver", "front_bumper", "canard_pass", "canard_driver", "front_fender_slats_pass", "front_fender_slats_driver"]
def load(p):
    with bpy.data.libraries.load(p, link=False) as (s, d): d.objects = list(s.objects)
    obs = [o for o in d.objects if o]
    for o in obs: bpy.context.scene.collection.objects.link(o)
    bpy.context.view_layer.update(); return [o for o in obs if o.type == "MESH"]
V, P = [], []
for k in KIT:
    for o in load(f"{B}/k_{k}.blend"):
        M = o.matrix_world; off = len(V); V += [M @ v.co + Vector((0, 0, DROP)) for v in o.data.vertices]; P += [[off + i for i in p.vertices] for p in o.data.polygons]
bvh = BVHTree.FromPolygons(V, P)
for w in WHEELS:
    obs = load(w); pts = []
    for o in obs:
        if o.name.startswith("bomex_decal"): continue
        M = o.matrix_world; vs = o.data.vertices
        idx = np.random.default_rng(0).choice(len(vs), min(len(vs), 20000), replace=False)
        pts += [M @ vs[int(i)].co for i in idx]
    side = 1 if "_fl" in w else -1
    out = Vector((side, 0, 0)); n = 0
    for p in pts:
        if p.z < 0.08: continue
        a1 = bvh.ray_cast(p + out * 0.001, out, 0.25)[0]      # kit outboard of the point
        a2 = bvh.ray_cast(p - out * 0.001, -out, 0.25)[0]     # kit inboard of the point
        if a2 is not None and a1 is None and (p - a2).length < 0.12: n += 1   # wheel sits outside a kit surface
    print("CLIP", w.split("/")[-1], n, "of", len(pts))
    for o in obs: bpy.data.objects.remove(o)
