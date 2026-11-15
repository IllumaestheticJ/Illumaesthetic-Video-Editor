"""v12 (user: "trace and color the windows black a little more accurately"): window areas traced on the SEMA photo
(b096156c) at the solved match camera, transferred to the scan as a per-face attribute "glass" (1 = black glass/frame),
mirrored about the car's centre plane for the driver side. Only the body mesh is loaded, so the mirror and other parts
do not occlude the tracing. The material uses the attribute instead of the band/side-texture guesses (LIV glass_attr).
  blender -b -P glass_mask.py -- in.blend out.blend cam_match.json solve_drop"""
import bpy, json, math, sys
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
a = sys.argv[sys.argv.index("--") + 1:]; IN, OUT, CAM, SDROP = a[0], a[1], json.load(open(a[2])), float(a[3])
W, H, XC = 1206, 2144, -0.072
# photo-pixel polygons (b096156c), traced on the dark glass incl. its black frame
POLYS = {
    "windscreen": [(345, 922), (420, 912), (490, 909), (560, 910), (630, 918), (665, 935), (705, 965), (735, 995), (748, 1013),
                   (690, 1018), (600, 1022), (500, 1027), (420, 1031), (382, 1034), (368, 990), (355, 950)],
    "side": [(220, 950), (248, 935), (275, 925), (333, 921), (343, 960), (352, 1000), (357, 1028), (300, 1018), (235, 1004),
             (225, 980)],
}


def basis(loc, target, roll):
    f = np.asarray(target, float) - loc; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    t = math.radians(roll); return f, r * math.cos(t) + u * math.sin(t), u * math.cos(t) - r * math.sin(t)


def inside(poly, x, y):  # even-odd ray crossing (no matplotlib in Blender's python)
    res = np.zeros(len(x), bool); P = np.asarray(poly, float); m = len(P)
    for k in range(m):
        x1, y1 = P[k]; x2, y2 = P[(k + 1) % m]
        cr = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
        res ^= cr
    return res


bpy.ops.wm.read_factory_settings(use_empty=True)  # (the default startup cube got saved into the output once)
with bpy.data.libraries.load(IN, link=False) as (s, d): d.objects = list(s.objects)
for o in d.objects:
    if o: bpy.context.scene.collection.objects.link(o)
bpy.context.view_layer.update()
ob = [o for o in d.objects if o and o.type == "MESH"][0]; me = ob.data
M = np.array(ob.matrix_world); n = len(me.polygons)
c = np.empty(n * 3); me.polygons.foreach_get("center", c); c = c.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
cs = c + np.array([0, 0, SDROP])  # the camera was solved with the body dropped by SDROP
loc = np.array(CAM["loc"]); f, r, u = basis(loc, CAM["target"], CAM["roll"]); fx = CAM["focal"] / 36.0 * W
def project(P):
    dv = P - loc; z = dv @ f; return W / 2 + fx * (dv @ r) / z, H / 2 - fx * (dv @ u) / z, z


def cand_of(P):
    x, y, z = project(P); m = np.zeros(len(P), bool)
    for poly in POLYS.values(): m |= inside(poly, x, y)
    return m & (z > 0)


verts = [ob.matrix_world @ v.co + Vector((0, 0, SDROP)) for v in me.vertices]
bvh = BVHTree.FromPolygons(verts, [list(p.vertices) for p in me.polygons])
L = Vector(loc)


def seen(P, idx, tol):
    out = np.zeros(len(P), bool)
    for i in idx:
        p = Vector(P[i]); dd = p - L; hit = bvh.ray_cast(L, dd.normalized(), dd.length + 0.05)
        out[i] = hit[0] is not None and (hit[0] - p).length < tol
    return out


# passenger side + windscreen: traced directly; driver side: its mirror image (about XC) traced on the passenger side
direct = seen(cs, np.where(cand_of(cs) & (c[:, 0] < XC + 0.25))[0], 0.012)
csm = cs.copy(); csm[:, 0] = 2 * XC - csm[:, 0]
drv = c[:, 0] > XC
# a driver-side face is glass if its mirror image projects into a traced window AND lands within 5 cm of a traced
# passenger-side glass face (the two sides of the scan are not exactly symmetric, so a strict ray test missed them)
kdg = KDTree(int(direct.sum()))
for j, i in enumerate(np.where(direct)[0]): kdg.insert(Vector(cs[i]), j)
kdg.balance()
mirr = np.zeros(n, bool)
for i in np.where(cand_of(csm) & drv)[0]:
    mirr[i] = kdg.find(Vector(csm[i]))[2] < 0.05
g = (direct | mirr).astype(np.float32)
print("GLASS direct", int(direct.sum()), "mirrored", int(mirr.sum()))
# close pinholes: a face whose 6 nearest neighbours are mostly glass becomes glass (and vice versa)
kd2 = KDTree(n)
for i in range(n): kd2.insert(Vector(c[i]), i)
kd2.balance()
sel = np.where((np.abs(c[:, 0] - XC) < 0.95) & (c[:, 2] > 0.85))[0]
g2 = g.copy()
for i in sel:
    nb = [j for _, j, _ in kd2.find_n(Vector(c[i]), 9)]
    g2[i] = 1.0 if g[nb].mean() > 0.5 else 0.0
print("GLASS total faces", int(g2.sum()))
at = me.attributes.new("glass", "FLOAT", "FACE"); at.data.foreach_set("value", g2)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
