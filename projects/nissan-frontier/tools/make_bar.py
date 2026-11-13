"""Stand-ins for Ronin parts that have no scan/CAD, built from the SEMA footage (IMG_3223/3226/3227) - NOT data:
  bar.blend    front bumper bar (black tube hoop under the bumper), aluminium skid plate, two red recovery hooks
  lights.blend LED bars behind the upper (2) and lower (1) Ronin grille openings + a marker strip behind the top slots
Absolute prep-frame coordinates (metres; nose -Y). Objects carry a "mat" custom property read by tools/shot.py.
  blender -b -P make_bar.py -- bar.blend lights.blend"""
import bpy, bmesh, math, sys
from mathutils import Vector
a = sys.argv[sys.argv.index("--") + 1:]
CX = -0.042  # truck centreline in the prep frame


def new():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def obj(name, bm, mat):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); o["mat"] = mat; return o


def tube(path, r, mat, name, seg=12):
    # Catmull-Rom resample, then sweep a circle
    pts = [Vector(p) for p in path]; P = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        for s in range(10):
            t = s / 10; p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1])
    bm = bmesh.new(); rings = []
    for i, p in enumerate(out):
        d = (out[min(i + 1, len(out) - 1)] - out[max(i - 1, 0)]).normalized()
        u = d.cross(Vector((0, 0, 1))).normalized(); v = d.cross(u)
        rings.append([bm.verts.new(p + r * (math.cos(2 * math.pi * k / seg) * u + math.sin(2 * math.pi * k / seg) * v)) for k in range(seg)])
    for i in range(len(rings) - 1):
        for k in range(seg):
            bm.faces.new((rings[i][k], rings[i][(k + 1) % seg], rings[i + 1][(k + 1) % seg], rings[i + 1][k]))
    return obj(name, bm, mat)


def box(lo, hi, mat, name):
    bm = bmesh.new(); r = bmesh.ops.create_cube(bm, size=1.0)
    for v in r["verts"]:
        v.co = Vector(((lo[i] + hi[i]) / 2 + v.co[i] * (hi[i] - lo[i]) for i in range(3)))
    return obj(name, bm, mat)


new()
W = 0.86
tube([(CX - 0.98, -2.02, 0.40), (CX - 0.97, -2.45, 0.36), (CX - 0.80, -2.80, 0.33), (CX - 0.4, -2.84, 0.32), (CX + 0.4, -2.84, 0.32),
      (CX + 0.80, -2.80, 0.33), (CX + 0.97, -2.45, 0.36), (CX + 0.98, -2.02, 0.40)], 0.032, "black", "bar")
bm = bmesh.new()   # skid plate: folded sheet under the nose
vs = [bm.verts.new(p) for p in [(CX - 0.50, -2.80, 0.30), (CX + 0.50, -2.80, 0.30), (CX + 0.46, -2.50, 0.17), (CX - 0.46, -2.50, 0.17),
                                (CX + 0.42, -2.10, 0.14), (CX - 0.42, -2.10, 0.14)]]
bm.faces.new((vs[0], vs[1], vs[2], vs[3])); bm.faces.new((vs[3], vs[2], vs[4], vs[5]))
obj("skid", bm, "steel")
for s in (-1, 1):
    box((CX + s * 0.30 - 0.03, -2.74, 0.20), (CX + s * 0.30 + 0.03, -2.62, 0.25), "red", f"hook{s}")
bpy.ops.wm.save_as_mainfile(filepath=a[0])

new()
box((CX - 0.44, -2.585, 0.752), (CX - 0.11, -2.555, 0.800), "led", "led_ul")
box((CX + 0.11, -2.585, 0.752), (CX + 0.44, -2.555, 0.800), "led", "led_ur")
box((CX - 0.40, -2.615, 0.560), (CX + 0.40, -2.585, 0.612), "led", "led_low")
box((CX - 0.46, -2.60, 0.872), (CX + 0.46, -2.575, 0.898), "led", "markers")
for o in list(bpy.context.scene.collection.objects):   # dark housings behind each lens
    lo = Vector((min(v.co[i] for v in o.data.vertices) for i in range(3))); hi = Vector((max(v.co[i] for v in o.data.vertices) for i in range(3)))
    box((lo.x - 0.01, hi.y, lo.z - 0.008), (hi.x + 0.01, hi.y + 0.05, hi.z + 0.008), "black", o.name + "_h")
bpy.ops.wm.save_as_mainfile(filepath=a[1])
print("BARDONE")
