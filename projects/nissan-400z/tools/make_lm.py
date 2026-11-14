"""BBS LM wheels from the user's file (bbs-lm.zip 'LM 1.fbx', ASCII FBX -> tools/fbx_ascii.py -> lm.obj), user 2026-11-14:
chrome on chrome (face + barrel/lip + hardware chrome); Brembo caliper made white, its raised 'Brembo' lettering
(material caliper_logo) removed and replaced by a black Bomex mark decal (GR86 badge art). Scaled to the car's tyre OD
(0.684 m), axis to X, outer face 5 mm inside the kit arch lip, caliper turned to the trailing side.
  blender -b -P make_lm.py -- lm.obj out_dir wheels_v6.json"""
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Matrix, Vector
a = sys.argv[sys.argv.index("--") + 1:]; OBJ, OUT, WJ = a[0], a[1], json.load(open(a[2]))
LOGO = "/home/user/media/nissan-400z/logo/bomex_black.png"


def mat(name, col, rough, metal, img=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if img:
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(img); t.extension = "CLIP"
        nt.links.new(t.outputs["Color"], b.inputs["Base Color"]); nt.links.new(t.outputs["Alpha"], b.inputs["Alpha"])
    return m


def chrome_mat():
    """Chrome that reads as chrome on the black studio set: a perfect mirror only shows black, so add a baked environment
    seen along the reflection vector (bright sky above the horizon, darker ground, soft horizon band) on top of a glossy."""
    m = bpy.data.materials.new("lm_chrome"); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; Lk = nt.links.new
    for n in list(N):
        if n.type != "OUTPUT_MATERIAL": N.remove(n)
    out = [n for n in N if n.type == "OUTPUT_MATERIAL"][0]
    tc = N.new("ShaderNodeTexCoord"); sep = N.new("ShaderNodeSeparateXYZ"); Lk(tc.outputs["Reflection"], sep.inputs[0])
    ramp = N.new("ShaderNodeValToRGB"); Lk(sep.outputs[2], ramp.inputs[0])
    el = ramp.color_ramp.elements; el[0].position = 0.40; el[0].color = (0.10, 0.10, 0.11, 1); el[1].position = 0.56; el[1].color = (0.92, 0.93, 0.95, 1)
    e2 = el.new(0.49); e2.color = (0.35, 0.35, 0.37, 1)
    em = N.new("ShaderNodeEmission"); Lk(ramp.outputs["Color"], em.inputs["Color"]); em.inputs["Strength"].default_value = 0.85
    gl = N.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.04; gl.inputs["Color"].default_value = (0.95, 0.95, 0.96, 1)
    ad = N.new("ShaderNodeAddShader"); Lk(em.outputs[0], ad.inputs[0]); Lk(gl.outputs[0], ad.inputs[1]); Lk(ad.outputs[0], out.inputs[0])
    return m


def tyre_mat(cx, cy):
    """Rubber with tread blocks: a bump from the angle about the wheel axis (object space = model units)."""
    m = bpy.data.materials.new("lm_tyre_v9"); m.use_nodes = True; nt = m.node_tree; N = nt.nodes; Lk = nt.links.new
    b = N["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.008, 0.008, 0.009, 1); b.inputs["Roughness"].default_value = 0.62
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = 0.06  # black rubber, not grey
    tc = N.new("ShaderNodeTexCoord"); sp = N.new("ShaderNodeSeparateXYZ"); Lk(tc.outputs["Object"], sp.inputs[0])
    def mth(op, a, bb=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        for i, v in enumerate((a, bb)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: Lk(v, n.inputs[i])
        return n.outputs[0]
    ang = mth("ARCTAN2", mth("SUBTRACT", sp.outputs[1], cy), mth("SUBTRACT", sp.outputs[0], cx))
    r = mth("LENGTH", 0) if False else None
    dx = mth("SUBTRACT", sp.outputs[0], cx); dy = mth("SUBTRACT", sp.outputs[1], cy)
    rad = mth("SQRT", mth("ADD", mth("MULTIPLY", dx, dx), mth("MULTIPLY", dy, dy)))
    # lateral grooves every 3 deg on the tread (r > 0.965 R), staggered half a pitch across the centre groove
    zz = sp.outputs[2]
    stag = mth("MULTIPLY", mth("GREATER_THAN", zz, TYRE["zmid"]), 0.5)
    ph = mth("FRACT", mth("ADD", mth("DIVIDE", ang, math.radians(3.0)), stag))
    groove = mth("LESS_THAN", mth("ABSOLUTE", mth("SUBTRACT", ph, 0.5)), 0.08)
    on_tread = mth("GREATER_THAN", rad, TYRE["R"] * 0.965)
    h = mth("MULTIPLY", mth("SUBTRACT", 1.0, mth("MULTIPLY", groove, on_tread)), 1.0)
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 4.0
    Lk(h, bump.inputs["Height"]); Lk(bump.outputs["Normal"], b.inputs["Normal"])
    return m


TYRE = {}


def tyre(cx, cy, R, rb, z_out, z_in):
    """Revolved tyre in model units about (cx, cy), axis Z: bead rb, OD radius R, sidewalls at z_out (outboard, larger z)
    and z_in. Rounded shoulders, sidewall bulge, rim-protector rib, 4 circumferential grooves."""
    wdt = z_out - z_in; zm = (z_out + z_in) / 2; TYRE.update(R=R, zmid=zm)
    sw = R - rb
    side = [(rb, 0.000), (rb + 0.10 * sw, 0.020), (rb + 0.16 * sw, 0.034), (rb + 0.20 * sw, 0.030),  # bead, protector rib
            (rb + 0.45 * sw, 0.036), (rb + 0.70 * sw, 0.030), (rb + 0.86 * sw, 0.012), (R - 0.05 * sw, -0.020),
            (R - 0.012 * sw, -0.055)]  # (r, bulge outward as a fraction of width)
    prof = [(r, z_out + b * wdt) for r, b in side]
    # tread across the width with 4 grooves (depth 2.5 % of R)
    gz = [0.20, 0.40, 0.60, 0.80]; gw = 0.035; gd = 0.022 * sw
    t = 0.07
    tread = [(R, z_out - t * wdt)]
    for g in gz:
        a, b2 = 1 - g - gw / 2, 1 - g + gw / 2
        tread += [(R, z_in + b2 * wdt), (R - gd, z_in + b2 * wdt - 0.004 * wdt), (R - gd, z_in + a * wdt + 0.004 * wdt), (R, z_in + a * wdt)]
    tread.append((R, z_in + t * wdt))
    prof += tread + [(r, z_in - b * wdt) for r, b in reversed(side)]
    n = 240; bm = bmesh.new(); rings = []
    for i in range(n):
        th = 2 * math.pi * i / n; c, s_ = math.cos(th), math.sin(th)
        rings.append([bm.verts.new((cx + r * c, cy + r * s_, z)) for r, z in prof])
    for i in range(n):
        A, B = rings[i], rings[(i + 1) % n]
        for j in range(len(prof) - 1):
            bm.faces.new((A[j], A[j + 1], B[j + 1], B[j]))
    me = bpy.data.meshes.new("tyre"); bm.to_mesh(me); bm.free()
    for pl in me.polygons: pl.use_smooth = True
    ob = bpy.data.objects.new("tyre", me); bpy.context.scene.collection.objects.link(ob)
    me.materials.append(tyre_mat(cx, cy))
    return ob


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=OBJ, forward_axis="Y", up_axis="Z")
    objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1: bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active; me = ob.data
    chrome = chrome_mat()
    white = mat("lm_caliper", (0.9, 0.9, 0.9), 0.28, 0.0)
    M = {"generic_tyre1": mat("lm_tyre", (0.018, 0.018, 0.02), 0.78, 0.0), "generic_tread1": mat("lm_tread", (0.014, 0.014, 0.016), 0.85, 0.0),
         "rotor_face": mat("lm_rotor", (0.42, 0.42, 0.43), 0.32, 0.85), "holes1": mat("lm_holes", (0.03, 0.03, 0.03), 0.6, 0.2),
         "caliper_2": white, "caliper_3": white, "caliper_logo": white,
         "wheel_bl": mat("lm_black", (0.02, 0.02, 0.022), 0.5, 0.2), "logo_1": mat("lm_black2", (0.02, 0.02, 0.022), 0.5, 0.2)}
    names = [s.material.name.split(".")[0] if s.material else "" for s in ob.material_slots]
    V = np.array([v.co[:] for v in me.vertices])
    logo_vs = sorted({v for p in me.polygons if names[p.material_index] == "caliper_logo" for v in p.vertices})
    for i, s in enumerate(ob.material_slots):
        s.material = M.get(names[i], chrome)
    bm = bmesh.new(); bm.from_mesh(me)
    drop = {"caliper_logo", "generic_tyre1", "generic_tread1"}  # v9: the file's tyre is a thin stretched shell -> tyre()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if names[f.material_index] in drop], context="FACES")
    bm.to_mesh(me); bm.free()
    # decal: PCA of the lettering patch in the wheel plane (XY), on its outboard (+Z) face
    L = V[logo_vs]; c = L.mean(0); e = np.linalg.eigh(np.cov((L[:, :2] - c[:2]).T))[1][:, ::-1]
    ux = e[:, 0] if e[0, 0] >= 0 else -e[:, 0]; uy = np.array([-ux[1], ux[0]])
    proj = (L[:, :2] - c[:2]) @ np.c_[ux, uy]; w = np.ptp(proj[:, 0]) * 0.95
    img = bpy.data.images.load(LOGO); h = w * img.size[1] / img.size[0]
    if h > np.ptp(proj[:, 1]) * 1.6: h = np.ptp(proj[:, 1]) * 1.6; w = h * img.size[0] / img.size[1]
    z = L[:, 2].max() + 0.6
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new()
    corners = [(-w / 2, -h / 2, 0, 0), (w / 2, -h / 2, 1, 0), (w / 2, h / 2, 1, 1), (-w / 2, h / 2, 0, 1)]
    vs = [bm.verts.new((c[0] + ux[0] * x + uy[0] * y, c[1] + ux[1] * x + uy[1] * y, z)) for x, y, _, _ in corners]
    f = bm.faces.new(vs)
    for lp, (_, _, u, v) in zip(f.loops, corners): lp[uvl].uv = (u, v)
    dm = bpy.data.meshes.new("bomex_decal"); bm.to_mesh(dm); bm.free()
    dob = bpy.data.objects.new("bomex_decal", dm); bpy.context.scene.collection.objects.link(dob)
    dmat = mat("lm_bomex_decal", (0.02, 0.02, 0.02), 0.4, 0.0, LOGO); dm.materials.append(dmat)
    # wheel frame: tread bbox -> centre + OD; axis +Z (outboard)
    tread = V[[v for p in me.polygons for v in p.vertices if names[p.material_index] in ("generic_tread1", "generic_tyre1")]] if False else None
    T = V[[v for p in me.polygons for v in p.vertices]] if False else None
    return ob, dob, c


TV = None
ob, dob, cal = build()
Vw = np.array([v.co[:] for v in ob.data.vertices]); lo, hi = Vw.min(0), Vw.max(0)
# the file's tyre is gone: wheel frame from its known tread (centre 450.98, 389.13; OD 937 units = 0.684 m rim scale)
ctr = np.array([450.9801745, 389.1266395, 0.0]); OD = 936.972251; s = 2 * WJ["r"] / OD
TR = WJ.get("tyre", {}).get("r", WJ["r"])  # v9 tyre radius (m): fuller sidewall like the photo, rim scale unchanged
tob = tyre(ctr[0], ctr[1], TR / s, 386.0, -287.0, -664.0)
hi = np.array([v.co[:] for v in ob.data.vertices]).max(0)
zout = hi[2]
print("OD units", OD, "scale", s, "outer z", zout, "width m", (hi[2] - lo[2]) * s)
cal_ang = math.atan2(cal[1] - ctr[1], cal[0] - ctr[0])
WOBJ = (ob, dob, tob)
for o in WOBJ:
    o.parent = None
base = {}
for o in WOBJ: base[o.name] = o.matrix_world.copy()
SQ = WJ.get("tyre", {}).get("squish", 0.006)
STEER = WJ.get("steer_deg", 0.0)
xc, ho = WJ["xc"], WJ["bbs"]["half_outer"]
os.makedirs(OUT, exist_ok=True)
for k, w in WJ["stock"].items():
    left = k.endswith("l")
    # model -> wheel-local: centre to origin, scale, outer face at local x=0 then out along +x (left) / -x (right)
    T0 = Matrix.Translation(Vector((-ctr[0], -ctr[1], -zout)))
    S = Matrix.Scale(s, 4)
    # spin about the wheel axis so the caliper sits on the trailing side (toward +Y in the car frame), a little above centre
    want = math.radians(15)  # angle in the wheel's (y_car, z_car) plane measured from +Y_car toward +Z_car
    # model X,Y -> car (Y, Z) for left wheels; mirrored for right wheels so the face still looks outboard
    Rz = Matrix.Rotation(want - cal_ang, 4, "Z")
    to_car = Matrix(((0, 0, 1, 0), (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)))  # model (x,y,z) -> car (y,z,x)
    if not left:
        to_car = Matrix(((0, 0, -1, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)))  # outboard = -X, keep caliper trailing
    xo = xc + (ho - 0.005) * (1 if left else -1)
    T1 = Matrix.Translation(Vector((xo, w["y"], TR - SQ)))
    hw = 0.5 * (zout - (-664.0)) * s  # half the tyre width (m): steer about the tyre's centre plane, not the face
    for tag, deg in (("", 0.0), ("_steer", STEER)):
        if tag and not k.startswith("f"):
            continue
        piv = Vector((xo - hw * (1 if left else -1), w["y"], TR - SQ))
        St = Matrix.Translation(piv) @ Matrix.Rotation(math.radians(deg), 4, "Z") @ Matrix.Translation(-piv)
        M = St @ T1 @ to_car @ S @ Rz @ T0
        for o in WOBJ:
            o.matrix_world = M @ base[o.name]
        bpy.context.view_layer.update()
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, f"lm_{k}{tag}.blend"), copy=True)
    bb = [o.matrix_world @ Vector(cc) for cc in ob.bound_box]
    print("wrote", k, [round(min(v[i] for v in bb), 3) for i in range(3)], [round(max(v[i] for v in bb), 3) for i in range(3)])
