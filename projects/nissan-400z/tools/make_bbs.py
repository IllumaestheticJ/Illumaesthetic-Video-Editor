"""Stand-in deep-dish mesh wheel in the style of the BBS LM on the built car (user photos 2026-11-13). NOT scan data and
not a BBS file - no scan/CAD of the real wheels exists on the Drive. Polished stepped lip, recessed face with 20 cross-laced
spokes, rivet ring, centre cap, low-profile tyre. Axis X, outer face +X, centre at origin, metres.
  blender -b -P make_bbs.py -- out_dir wheels_v6.json     -> bbs_fl/fr/rl/rr.blend placed in the prepped car frame"""
import bpy, bmesh, json, math, os, sys
from mathutils import Matrix, Vector
out, wj = sys.argv[sys.argv.index("--") + 1:][:2]
WJ = json.load(open(wj)); R = WJ["r"]; W = WJ["bbs"]["width"]; h = W / 2
RIM = 0.245; DISH = 0.105; FACE_X = h - 0.012 - DISH; FACE_R = 0.212


def mat(name, col, rough, metal):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    return m


def build():
    M = {"tyre": mat("bbs_tyre", (0.012, 0.012, 0.013), 0.75, 0.0), "lip": mat("bbs_lip", (0.86, 0.86, 0.88), 0.10, 1.0),
         "face": mat("bbs_face", (0.72, 0.72, 0.74), 0.28, 1.0), "dark": mat("bbs_dark", (0.02, 0.02, 0.022), 0.6, 0.2)}
    objs = []

    def obj(name, bm, m, smooth=True):
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); me.materials.append(M[m])
        for p in me.polygons: p.use_smooth = smooth
        objs.append(o); return o

    def lathe(profile, seg=128):
        bm = bmesh.new(); rings = []
        for i in range(seg):
            a = 2 * math.pi * i / seg
            rings.append([bm.verts.new((x, r * math.cos(a), r * math.sin(a))) for x, r in profile])
        for i in range(seg):
            a, b = rings[i], rings[(i + 1) % seg]
            for j in range(len(profile) - 1):
                if profile[j][1] < 1e-6 and profile[j + 1][1] < 1e-6: continue
                bm.faces.new((a[j], a[j + 1], b[j + 1], b[j]))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        return bm

    def box(p0, p1, wid, dep):
        """bar from p0 to p1 (3D), width in the wheel plane, depth along X"""
        bm = bmesh.new(); d = (p1 - p0); L = d.length; d.normalize()
        xa = Vector((1, 0, 0)); s = d.cross(xa); s.normalize()
        vs = []
        for u in (0, L):
            for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                vs.append(bm.verts.new(p0 + d * u + s * (a * wid / 2) + xa * (b * dep / 2)))
        for f in ((0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            bm.faces.new([vs[i] for i in f])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        return bm
    # tyre
    obj("tyre", lathe([(-h + 0.02, RIM + 0.004), (-h + 0.004, RIM + 0.03), (-h, R - 0.045), (-h + 0.012, R - 0.014), (-h + 0.035, R),
                       (h - 0.035, R), (h - 0.012, R - 0.014), (h, R - 0.045), (h - 0.004, RIM + 0.03), (h - 0.02, RIM + 0.004)]), "tyre")
    # polished lip + stepped dish + barrel
    obj("lip", lathe([(-h + 0.01, RIM - 0.012), (-h + 0.02, RIM + 0.006), (h - 0.02, RIM + 0.006), (h - 0.006, RIM + 0.012), (h, RIM + 0.004),
                      (h - 0.004, RIM - 0.006), (h - 0.018, RIM - 0.012), (h - 0.045, RIM - 0.016), (h - 0.052, RIM - 0.024),
                      (FACE_X + 0.02, RIM - 0.028), (FACE_X + 0.006, FACE_R + 0.012), (FACE_X + 0.006, FACE_R - 0.004)]), "lip")
    # face ring (rivet land) + hub + backing
    obj("ring", lathe([(FACE_X + 0.006, FACE_R + 0.012), (FACE_X + 0.012, FACE_R + 0.004), (FACE_X + 0.012, FACE_R - 0.014), (FACE_X, FACE_R - 0.018)]), "face")
    obj("hub", lathe([(FACE_X - 0.01, 0.0), (FACE_X - 0.01, 0.078), (FACE_X + 0.022, 0.07), (FACE_X + 0.026, 0.036), (FACE_X + 0.034, 0.032), (FACE_X + 0.036, 0.0)], 64), "face")
    obj("cap", lathe([(FACE_X + 0.0365, 0.0), (FACE_X + 0.0365, 0.027)], 48), "dark")
    obj("back", lathe([(FACE_X - 0.03, 0.0), (FACE_X - 0.03, RIM - 0.03)], 64), "dark")
    # 20 cross-laced spokes: neighbours lean opposite ways and cross near the rim
    bm = bmesh.new()
    for i in range(20):
        a0 = 2 * math.pi * i / 20; a1 = a0 + (1 if i % 2 == 0 else -1) * math.radians(15)
        p0 = Vector((FACE_X + 0.016, 0.064 * math.cos(a0), 0.064 * math.sin(a0)))
        p1 = Vector((FACE_X + 0.004, (FACE_R - 0.012) * math.cos(a1), (FACE_R - 0.012) * math.sin(a1)))
        b = box(p0, p1, 0.011, 0.016); me = bpy.data.meshes.new("t"); b.to_mesh(me); b.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)
    obj("spokes", bm, "face", smooth=False)
    # rivets
    bm = bmesh.new()
    for i in range(30):
        a = 2 * math.pi * (i + 0.5) / 30
        bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.0042,
                                  matrix=Matrix.Translation((FACE_X + 0.013, (FACE_R - 0.005) * math.cos(a), (FACE_R - 0.005) * math.sin(a))))
    obj("rivets", bm, "lip")
    return objs


os.makedirs(out, exist_ok=True)
xc = WJ["xc"]; ho = WJ["bbs"]["half_outer"]
for k, w in WJ["stock"].items():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = build()
    left = k.endswith("l")
    T = Matrix.Translation((xc + (ho - h) * (1 if left else -1), w["y"], WJ["r"] + 0.002)) @ (Matrix.Identity(4) if left else Matrix.Rotation(math.pi, 4, "Z"))
    for o in objs:
        o.matrix_world = T
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, f"bbs_{k}.blend"))
    print("wrote", k, [round(v, 3) for v in T.translation])
