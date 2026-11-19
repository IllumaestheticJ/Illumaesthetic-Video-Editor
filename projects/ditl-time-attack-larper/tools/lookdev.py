"""Look-test stills for the track-guy short. blender -b --python lookdev.py -- <shot> <out.png> [res] [samples]
Shots: driveway (shot 4: rear 3/4, gloved hand on the TC endplate), garage (shot 10: wing under the height bar)."""
import bpy, sys, os, math
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ditl_kit import mat, box, plane, hand, world, camera, procmat, GLB, WING_GLB, R

WHEELS = [(0.938, 0.323, 0.328), (3.637, 0.323, 0.328)]  # car JSON wheels: x from rear bumper, centre height, radius (m)


def imp(path):
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def fk8(paint=(0.85, 0.86, 0.87)):
    """Configurator FK8 (one untextured mesh): faces get paint / glass / tyre / rim / trim by position and normal."""
    car = [o for o in imp(GLB) if o.type == "MESH"][0]; car.name = "fk8"
    mats = [mat("paint", paint, 0.3), mat("glass", (0.012, 0.015, 0.02), 0.45), mat("tyre", (0.02, 0.02, 0.02), 0.9),
            mat("rim", (0.06, 0.06, 0.065), 0.4), mat("trim", (0.015, 0.015, 0.015), 0.7)]
    for m in mats: car.data.materials.append(m)
    mw = car.matrix_world
    for p in car.data.polygons:
        c = mw @ p.center; n = (mw.to_3x3() @ p.normal).normalized()
        mi = 0
        for wx, wy, wr in WHEELS:
            if math.hypot(c.x - wx, c.z - wy) < wr * 1.08 and abs(c.y) < 0.9: mi = 4   # wheel-well liner
        if mi == 0 and 1.0 < c.z < 1.33 and abs(n.y) > 0.55 and 0.7 < c.x < 3.2 and abs(c.y) < 0.76: mi = 1   # side glass
        if mi == 0 and 0.44 < c.x < 1.02 and 1.14 < c.z < 1.33 and n.z > 0.85 and n.x < -0.12 and abs(c.y) < 0.58: mi = 1   # hatch glass (centre-line profile)
        if mi == 0 and c.x < 0.3 and c.z < 0.42: mi = 4                                       # rear diffuser
        p.material_index = mi; p.use_smooth = False
    smooth_labels(car, keep=(4,))
    (te37() if os.environ.get('WHEEL') == 'te37' else wheels())
    return car


def smooth_labels(o, passes=4, keep=()):
    """Majority vote of each face's material over its edge neighbours: removes the speckle the position rules leave."""
    import bmesh
    bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
    nb = [[g.index for e in f.edges for g in e.link_faces if g.index != f.index] for f in bm.faces]
    lab = [f.material_index for f in bm.faces]
    for _ in range(passes):
        new = lab[:]
        for i, ns in enumerate(nb):
            if lab[i] in keep or not ns: continue
            cnt = {}
            for j in ns: cnt[lab[j]] = cnt.get(lab[j], 0) + 1
            best = max(cnt, key=cnt.get)
            if cnt[best] * 2 > len(ns): new[i] = best
        lab = new
    for f, l in zip(bm.faces, lab): f.material_index = l
    bm.to_mesh(o.data); bm.free()


CIVIC = "/home/user/epsilon-site/showroom/models/eps-honda-civic-hatch-fl-v3.glb"
TRACK = 0.797  # car JSON track 1594 mm / 2


def wheels():
    """Factory Civic wheels from our showroom model, moved to the FK8's measured axles (configurator stand-in positions)."""
    from mathutils import Matrix
    for o in imp(CIVIC):
        nm = o.name.split(".")[0]
        if nm not in ("wheel_FL", "wheel_FR", "wheel_RL", "wheel_RR") or o.type != "MESH":
            bpy.data.objects.remove(o); continue
        vs = [o.matrix_world @ v.co for v in o.data.vertices]
        c = Vector([(min(v[i] for v in vs) + max(v[i] for v in vs)) / 2 for i in range(3)])
        r = (max(v[2] for v in vs) - min(v[2] for v in vs)) / 2; k = WHEELS[0][2] / r
        tgt = Vector((WHEELS[1][0] if nm[-2] == "F" else WHEELS[0][0], TRACK if nm[-1] == "L" else -TRACK, WHEELS[0][1]))
        mw = Matrix.Translation(tgt) @ Matrix.Rotation(R(90), 4, "Z") @ Matrix.Scale(k, 4) @ Matrix.Translation(-c) @ o.matrix_world
        o.parent = None; o.matrix_world = mw


TE37 = "/home/user/epsilon-site/showroom/models/wheels/eps-wheel-te37-v1.glb"


def te37(finish=(0.35, 0.22, 0.08)):
    """Our scanned TE37-style 6-spoke (showroom wheel: axle on X, face +X, hub-centred) at the four FK8 axles."""
    from mathutils import Matrix
    for nm, x, y in (("FL", WHEELS[1][0], TRACK), ("FR", WHEELS[1][0], -TRACK), ("RL", WHEELS[0][0], TRACK), ("RR", WHEELS[0][0], -TRACK)):
        parts = [o for o in imp(TE37) if o.type == "MESH"]
        k = WHEELS[0][2] / 0.317; rz = R(90) if y > 0 else R(-90)
        for o in parts:
            o.matrix_world = Matrix.Translation((x, y, WHEELS[0][1])) @ Matrix.Rotation(rz, 4, "Z") @ Matrix.Scale(k, 4) @ o.matrix_world
            o.name = f"te37_{nm}_{o.name.split('.')[0]}"
            if o.name.endswith("rim"): o.data.materials.clear(); o.data.materials.append(mat("bronze", finish, 0.35))


def tc_wing():
    parts = [o for o in imp(WING_GLB) if o.type == "MESH"]
    blk = mat("wing_black", (0.02, 0.02, 0.022), 0.35); alu = mat("stand", (0.03, 0.03, 0.032), 0.5)
    for o in parts:
        o.data.materials.clear(); o.data.materials.append(blk if o.name.startswith(("wing", "endplate")) else alu)
    return parts


def driveway():
    world((0.55, 0.7, 0.95), 0.8, sun=(2.6, 50, 140))
    plane("drive", 30, 30, procmat("concrete", "noise", (0.3, 0.29, 0.28), (0.38, 0.37, 0.35), 0.8), (0, 0, 0))
    plane("grass", 30, 30, procmat("grass", "noise", (0.12, 0.25, 0.07), (0.2, 0.36, 0.1), 2.0), (0, 18, -0.01))
    siding = procmat("siding", "brick", (0.72, 0.7, 0.62), (0.78, 0.76, 0.68), 0.5)
    box("house", (14, 6, 5), siding, (2, 8.5, 0), base="z")
    box("gdoor", (5, 0.08, 2.4), mat("gdoor", (0.86, 0.86, 0.84), 0.6), (2.2, 5.46, 0), base="z")
    box("roof", (15, 7, 0.4), mat("roof", (0.18, 0.16, 0.15)), (2, 8.5, 5), base="z")


def shot_driveway():
    driveway(); fk8(); w = tc_wing()
    # close on the right rear corner: the near (right) endplate fills the frame, the gloved hand comes in from the camera
    camera((-0.5, -1.35, 1.45), look=(0.12, -0.85, 1.33), lens=22)
    from hands import hand as rhand, FLAT
    glove = mat("glove", (0.55, 0.04, 0.03), 0.65); suit = mat("suit", (0.06, 0.1, 0.45), 0.8)
    from mathutils import Matrix
    fy = Vector((0.92, 0, 0.38)).normalized(); bz = Vector((0, -1, 0)); fx = fy.cross(bz)   # fingers forward along the endplate, palm on it
    rot = Matrix((fx, fy, bz)).transposed().to_euler()
    rhand("handR", None, (0.0, -0.848 - 0.017, 1.27), rot, curls=FLAT, thumb=0.15, sleeve=suit, glove=glove)


def shot_garage():
    world((0.3, 0.3, 0.32), 0.25, sun=None)
    plane("floor", 40, 40, procmat("deck", "noise", (0.3, 0.3, 0.31), (0.4, 0.4, 0.41), 1.0), (0, 0, 0))
    yel = mat("yellow", (0.9, 0.7, 0.05), 0.5)
    box("bar", (0.12, 3.2, 0.12), yel, (-0.05, 0, 1.38), base="z")          # height bar exactly at the wing's top edge
    for s in (-1, 1): box(f"chain{s}", (0.02, 0.02, 1.3), mat("chain", (0.2, 0.2, 0.2)), (-0.05, s * 1.5, 1.5), base="z")
    box("ceiling", (40, 40, 0.3), mat("conc", (0.45, 0.45, 0.46)), (0, 0, 2.6), base="z")
    for i in range(-3, 4):
        l = bpy.data.objects.new(f"lamp{i}", bpy.data.lights.new(f"lamp{i}", "AREA")); l.data.energy = 45; l.data.size = 1.2
        l.location = (i * 3.0, 0, 2.5); bpy.context.scene.collection.objects.link(l)
    fk8((0.85, 0.86, 0.87)); tc_wing()
    camera((1.6, -2.4, 1.15), look=(-0.1, 0.1, 1.33), lens=22)


if __name__ == "__main__":
    a = sys.argv[sys.argv.index("--") + 1:]; shot, out = a[0], a[1]
    res = int(a[2]) if len(a) > 2 else 540; spp = int(a[3]) if len(a) > 3 else 24
    bpy.ops.wm.read_factory_settings(use_empty=True)
    {"driveway": shot_driveway, "garage": shot_garage}[shot]()
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = spp
    sc.render.resolution_x = sc.render.resolution_y = res; sc.render.filepath = out
    sc.view_settings.view_transform = "Standard"
    bpy.ops.render.render(write_still=True)
