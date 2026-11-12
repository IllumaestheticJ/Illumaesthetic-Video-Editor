"""Stand-in wheel + tyre for the Ronin section (NOT scan data): built from the published specs only -
35x12.50R17 tyre (OD 889 mm, width 318 mm) on a 17x9 beadlock-style wheel (Nissan SEMA 2026 release via press coverage).
Generic geometry: block-tread tyre, 8 split spokes, beadlock ring with 24 bolts. Axis = X, centre at origin, metres.
  blender -b -P make_wheel.py -- out.blend"""
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix
out = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
R, W, RIM = 0.4445, 0.318, 0.216
def obj(name, bm):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); return o
def lathe(profile, seg=96):
    bm = bmesh.new(); rings = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        rings.append([bm.verts.new((x, r * math.cos(a), r * math.sin(a))) for x, r in profile])
    for i in range(seg):
        a, b = rings[i], rings[(i + 1) % seg]
        for j in range(len(profile) - 1):
            bm.faces.new((a[j], a[j + 1], b[j + 1], b[j]))
    return bm
h = W / 2
# tyre carcass: sidewall bulge, square shoulders
tyre = lathe([(-h * 0.80, RIM + 0.005), (-h * 0.98, RIM + 0.06), (-h * 1.0, R - 0.07), (-h * 0.86, R - 0.018), (-h * 0.70, R - 0.012),
              (h * 0.70, R - 0.012), (h * 0.86, R - 0.018), (h * 1.0, R - 0.07), (h * 0.98, RIM + 0.06), (h * 0.80, RIM + 0.005)])
# tread blocks: 3 rows, staggered, plus shoulder lugs down the sidewall
def box(bm, c, sx, sy, sz, rot):
    r = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=r["verts"])
    bmesh.ops.transform(bm, matrix=Matrix.Translation(c), verts=r["verts"])
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(rot, 3, "X"), verts=r["verts"])
n = 30
for i in range(n):
    a = 2 * math.pi * i / n
    box(tyre, (0, 0, R - 0.006), 0.085, 0.060, 0.016, a)
    box(tyre, (-0.095, 0, R - 0.007), 0.075, 0.058, 0.016, a + math.pi / n)
    box(tyre, (0.095, 0, R - 0.007), 0.075, 0.058, 0.016, a + math.pi / n)
    for s in (-1, 1):
        box(tyre, (s * h * 0.93, 0, R - 0.045), 0.03, 0.05, 0.07, a + (0 if i % 2 else math.pi / n))
t = obj("tyre", tyre); t["mat"] = "rubber"
# wheel: barrel, face with 8 split spokes, beadlock ring + bolts, hub
wh = lathe([(-h * 0.80, RIM + 0.006), (-h * 0.80, RIM - 0.012), (h * 0.55, RIM - 0.03), (h * 0.80, RIM - 0.012), (h * 0.80, RIM + 0.006)], 64)
fx = -h * 0.62   # outer face (the -X side faces out on the truck's right; mirrored for the left)
for k in range(8):
    a = 2 * math.pi * k / 8
    for off in (-0.018, 0.018):
        r = bmesh.ops.create_cube(wh, size=1.0)
        bmesh.ops.scale(wh, vec=(0.03, 0.018, RIM - 0.075), verts=r["verts"])
        bmesh.ops.transform(wh, matrix=Matrix.Translation((fx + 0.01, off, 0.055 + (RIM - 0.075) / 2)), verts=r["verts"])
        bmesh.ops.rotate(wh, cent=(0, 0, 0), matrix=Matrix.Rotation(a, 3, "X"), verts=r["verts"])
def disc(bm, x0, x1, r0, r1, seg=64):
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        p = lambda x, r, a: bm.verts.new((x, r * math.cos(a), r * math.sin(a)))
        bm.faces.new((p(x0, r1, a0), p(x0, r1, a1), p(x1, r1, a1), p(x1, r1, a0)))     # outer wall
        bm.faces.new((p(x0, r0, a0), p(x0, r0, a1), p(x0, r1, a1), p(x0, r1, a0)))     # face
        if r0 > 0: bm.faces.new((p(x0, r0, a0), p(x0, r0, a1), p(x1, r0, a1), p(x1, r0, a0)))
disc(wh, fx - 0.012, fx + 0.02, RIM - 0.03, RIM + 0.012)      # beadlock ring
disc(wh, fx - 0.004, fx + 0.03, 0.0, 0.075)                    # hub
w = obj("wheel", wh); w["mat"] = "bronze"
bolts = bmesh.new()
for k in range(24):
    a = 2 * math.pi * k / 24
    r = bmesh.ops.create_cone(bolts, segments=8, radius1=0.007, radius2=0.007, depth=0.012, cap_ends=True)
    bmesh.ops.rotate(bolts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Y"), verts=r["verts"])
    bmesh.ops.transform(bolts, matrix=Matrix.Translation((fx - 0.016, 0, RIM - 0.009)), verts=r["verts"])
    bmesh.ops.rotate(bolts, cent=(0, 0, 0), matrix=Matrix.Rotation(a, 3, "X"), verts=r["verts"])
b = obj("bolts", bolts); b["mat"] = "steel"
for o in (t, w, b):
    for p in o.data.polygons: p.use_smooth = False
bpy.ops.wm.save_as_mainfile(filepath=out)
print("WHEEL", out, [len(o.data.polygons) for o in (t, w, b)])
