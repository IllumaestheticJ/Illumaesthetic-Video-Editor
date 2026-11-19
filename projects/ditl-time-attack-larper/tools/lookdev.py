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


SIDE_GLASS = "/home/user/media/ditl-time-attack-larper/tex/fk8_side_glass.png"   # from the scan's own side drawing (x0 -12.3 mm, 4590 px = 4590 mm; z 73.8..1409.8 mm)


def body_mat(paint):
    """Paint and glass in one shader. Side glass = the side drawing's window opening projected across the car (sides only);
    hatch glass = the centre-line profile box. Edges cut through faces, so they stay clean on the coarse scan mesh."""
    m = bpy.data.materials.new("body"); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; L = nt.links.new
    out = N["Material Output"]; pb = N["Principled BSDF"]; pb.inputs["Base Color"].default_value = (*paint, 1); pb.inputs["Roughness"].default_value = 0.28
    gl = N.new("ShaderNodeBsdfPrincipled"); gl.inputs["Base Color"].default_value = (0.01, 0.012, 0.016, 1); gl.inputs["Roughness"].default_value = 0.4
    tc = N.new("ShaderNodeTexCoord"); sp = N.new("ShaderNodeSeparateXYZ"); L(tc.outputs["Object"], sp.inputs[0])
    sn = N.new("ShaderNodeSeparateXYZ"); L(tc.outputs["Normal"], sn.inputs[0])   # object-space normal (car can move)
    def op(o, a, b=None, clamp=False):
        n = N.new("ShaderNodeMath"); n.operation = o; n.use_clamp = clamp
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: L(v, n.inputs[i])
        return n.outputs[0]
    u = op("DIVIDE", op("ADD", op("MULTIPLY", sp.outputs["X"], 1000.0), 12.3), 4590.0)
    v = op("DIVIDE", op("SUBTRACT", op("MULTIPLY", sp.outputs["Z"], 1000.0), 73.8), 1336.0)
    cv = N.new("ShaderNodeCombineXYZ"); L(u, cv.inputs[0]); L(v, cv.inputs[1])
    tx = N.new("ShaderNodeTexImage"); tx.image = bpy.data.images.load(SIDE_GLASS); tx.extension = "CLIP"; L(cv.outputs[0], tx.inputs[0])
    side = op("GREATER_THAN", op("ABSOLUTE", sn.outputs["Y"]), 0.35)
    sideglass = op("MULTIPLY", op("GREATER_THAN", tx.outputs["Color"], 0.5), side)
    X, Y, Z = sp.outputs["X"], op("ABSOLUTE", sp.outputs["Y"]), sp.outputs["Z"]
    hatch = op("MULTIPLY", op("MULTIPLY", op("GREATER_THAN", X, 0.46), op("LESS_THAN", X, 1.0)),
               op("MULTIPLY", op("MULTIPLY", op("GREATER_THAN", Z, 1.15), op("LESS_THAN", Y, 0.56)), op("GREATER_THAN", sn.outputs["Z"], 0.8)))
    # FK8 black lower aero: the rear diffuser/valance and the bottom band of the skirts and lip, as straight cuts
    trim = op("MAXIMUM", op("MULTIPLY", op("LESS_THAN", X, 0.33), op("LESS_THAN", Z, 0.40)), op("LESS_THAN", Z, 0.21))
    fac = op("MAXIMUM", op("MAXIMUM", sideglass, hatch), trim)
    if os.environ.get("DBG"):
        em = N.new("ShaderNodeEmission"); dd = {"hatch": hatch, "side": sideglass, "nz": sn.outputs["Z"], "z": Z, "y": Y, "x": X}[os.environ["DBG"]]
        L(dd, em.inputs["Strength"]); L(em.outputs[0], out.inputs["Surface"]); return m
    mix = N.new("ShaderNodeMixShader"); L(fac, mix.inputs[0]); L(pb.outputs[0], mix.inputs[1]); L(gl.outputs[0], mix.inputs[2]); L(mix.outputs[0], out.inputs["Surface"])
    return m


def fill_holes(o, sides=400):
    """The scan has ~3.5k open edges (missed glass, seams); dark holes read as choppy panels. Fill loops up to `sides` edges."""
    import bmesh
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.002)
    before = sum(1 for e in bm.edges if e.is_boundary)
    bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=sides)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    print("fill_holes: boundary edges", before, "->", sum(1 for e in bm.edges if e.is_boundary))
    bm.to_mesh(o.data); bm.free()


def fk8(paint=(0.85, 0.86, 0.87)):
    """Configurator FK8 (our scan, one untextured mesh): smooth-shaded; paint/glass in the shader, black only for wheel-well liners and diffuser."""
    car = [o for o in imp(GLB) if o.type == "MESH"][0]; car.name = "fk8"
    fill_holes(car)
    car.data.materials.append(body_mat(paint)); car.data.materials.append(mat("trim", (0.015, 0.015, 0.015), 0.7))
    mw = car.matrix_world
    for p in car.data.polygons:
        c = mw @ p.center; mi = 0
        for wx, wy, wr in WHEELS:
            if math.hypot(c.x - wx, c.z - wy) < wr * 1.08 and abs(c.y) < 0.9: mi = 1   # wheel-well liner
        p.material_index = mi
    smooth_labels(car)
    bpy.context.view_layer.objects.active = car; car.select_set(True)
    try: bpy.ops.object.shade_auto_smooth(angle=R(32))
    except Exception: bpy.ops.object.shade_smooth()
    (te37() if os.environ.get('WHEEL', 'te37') == 'te37' else wheels())
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
