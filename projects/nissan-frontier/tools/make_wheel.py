"""Stand-in wheel + tyre for the Ronin section (NOT scan data). v3 (user: v2 was ugly, must be solid on the inside):
a clean SOLID lathe - closed tyre with a smooth carcass and low all-terrain tread blocks; one-piece wheel with a flat
dark-bronze face closed front and back (nothing to see through), 8 shallow dark window insets, beadlock ring with 24
bolts, dark centre cap. 35x12.50R17 (OD 889 mm, width 318 mm), axis = X, centre at origin, metres; outer face at -X.
  blender -b -P make_wheel.py -- out.blend"""
import bpy, bmesh, math, sys
from mathutils import Matrix
out = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
R, W, RIM = 0.4445, 0.318, 0.216
h = W / 2


def obj(name, bm, mat, smooth=False):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); o["mat"] = mat
    for p in me.polygons: p.use_smooth = smooth
    return o


def lathe(profile, seg=96, close=True):
    """profile = [(x, r), ...]; r = 0 ends are capped by the fan"""
    bm = bmesh.new(); rings = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        rings.append([bm.verts.new((x, r * math.cos(a), r * math.sin(a))) for x, r in profile])
    for i in range(seg):
        a, b = rings[i], rings[(i + 1) % seg]
        for j in range(len(profile) - 1):
            bm.faces.new((a[j], a[j + 1], b[j + 1], b[j]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    return bm


# tyre: closed section (bead to bead across the inside too), rounded shoulders
tyre = lathe([(-h * 0.78, RIM), (-h * 0.97, RIM + 0.05), (-h * 1.0, R - 0.085), (-h * 0.93, R - 0.035), (-h * 0.78, R - 0.012), (-h * 0.5, R - 0.008),
              (h * 0.5, R - 0.008), (h * 0.78, R - 0.012), (h * 0.93, R - 0.035), (h * 1.0, R - 0.085), (h * 0.97, RIM + 0.05), (h * 0.78, RIM),
              (-h * 0.78, RIM)], 128)
obj("tyre", tyre, "rubber", smooth=True)
tread = bmesh.new()
n = 44
for i in range(n):
    a = 2 * math.pi * i / n
    for j, xo in enumerate((-0.105, -0.035, 0.035, 0.105)):
        r = bmesh.ops.create_cube(tread, size=1.0)
        bmesh.ops.scale(tread, vec=(0.056, 0.046, 0.016), verts=r["verts"])
        bmesh.ops.transform(tread, matrix=Matrix.Translation((xo, 0, R - 0.006)), verts=r["verts"])
        bmesh.ops.rotate(tread, cent=(0, 0, 0), matrix=Matrix.Rotation(a + (math.pi / n if j % 2 else 0), 3, "X"), verts=r["verts"])
obj("tread", tread, "rubber")
# wheel: one closed solid. outer face at fx (flat), beadlock lip, barrel, closed back
fx = -h * 0.60
wheel = lathe([(fx - 0.004, 0.0), (fx - 0.004, 0.05), (fx + 0.012, 0.062), (fx + 0.012, RIM - 0.05), (fx - 0.006, RIM - 0.036), (fx - 0.016, RIM - 0.030),
               (fx - 0.016, RIM + 0.010), (fx + 0.006, RIM + 0.012), (h * 0.80, RIM + 0.004), (h * 0.80, 0.0)], 96)
obj("wheel", wheel, "bronze")
ins = bmesh.new()   # 8 shallow window insets: dark plates 1.5 mm proud of the face (solid wheel, reads as windows)
for k_ in range(8):
    a = 2 * math.pi * k_ / 8
    r = bmesh.ops.create_cube(ins, size=1.0)
    bmesh.ops.scale(ins, vec=(0.003, 0.050, 0.066), verts=r["verts"])
    for v in r["verts"]:                      # trapezoid: wider toward the rim
        v.co.y *= 0.72 + 0.56 * (v.co.z / 0.066 + 0.5)
    bmesh.ops.transform(ins, matrix=Matrix.Translation((fx + 0.0105, 0, 0.118)), verts=r["verts"])
    bmesh.ops.rotate(ins, cent=(0, 0, 0), matrix=Matrix.Rotation(a, 3, "X"), verts=r["verts"])
obj("insets", ins, "black")
bolts = bmesh.new()
for k_ in range(24):
    a = 2 * math.pi * k_ / 24
    r = bmesh.ops.create_cone(bolts, segments=8, radius1=0.006, radius2=0.006, depth=0.010, cap_ends=True)
    bmesh.ops.rotate(bolts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"), verts=r["verts"])
    bmesh.ops.transform(bolts, matrix=Matrix.Translation((fx - 0.020, 0, RIM - 0.010)), verts=r["verts"])
    bmesh.ops.rotate(bolts, cent=(0, 0, 0), matrix=Matrix.Rotation(a, 3, "X"), verts=r["verts"])
obj("bolts", bolts, "steel")
cap = lathe([(fx - 0.012, 0.0), (fx - 0.012, 0.036), (fx - 0.004, 0.044), (fx - 0.004, 0.0)], 48)
obj("cap", cap, "black")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("WHEEL", out)
