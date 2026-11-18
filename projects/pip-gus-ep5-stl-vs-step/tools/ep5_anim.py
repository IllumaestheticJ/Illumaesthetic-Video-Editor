"""Pip & Gus Ep 5 ("STL or STEP? Mesh vs NURBS") cartoon animation.

Runs INSIDE the pilot's scene builder so the locked characters, rig, shop, clock, stool and phone are reused unchanged:

  blender -b --factory-startup -P projects/scan-tedium-explainer-reel/tools/partA_scene.py -- \
      --exec projects/pip-gus-ep5-stl-vs-step/tools/ep5_anim.py --out FRAMES_DIR \
      --timeline projects/pip-gus-ep5-stl-vs-step/ep5_timeline.json [--shots E1,E2] [--frames 10,40] [--every N] [--scale 1]

The pilot's talk/blink/expression helpers (partA_anim.py, up to its shot code) are executed first with the Ep 5 timeline;
expr_state is then replaced with the Ep 5 expressions. Every frame is posed procedurally (no keyframes) and rendered as a
still, resumable: FRAMES_DIR/<shot>/<frame>.png is skipped when it exists. No text or numerals anywhere in 3D.

Props (all generic, no brands): a cartoon bumper built three ways from ONE parametric surface - a point cloud (the scan),
a faceted triangle mesh (STL) and smooth patches with a real NURBS edge curve (STEP) - plus a cartoon 3D printer, a cartoon
CNC mill, a tick badge, a "?" badge, a hole + slider, and Gus's floating "cursor" hand. Digital shots play in a dark
"inside the computer" stage far from the shop (VOID).
"""
import math, os, random, json, time
import bpy, bmesh
from mathutils import Vector, Matrix

# ------------------------------------------------------------------------------------------------ pilot helpers (talk etc.)
_PA = os.path.join(os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("-P") + 1])), "partA_anim.py")
_src = open(_PA).read()
_src = _src[: _src.index("def anim_S1(")]
exec(compile(_src, _PA, "exec"), globals())          # defines TL/SF/LN, talk(), set_face(), expr_state(), pose() wrapper ...

LINE = {L["n"]: L for L in TL["lines"]}
SHOTS_EP5 = arg("--shots", ",".join(s["id"] for s in TL["shots"] if s["id"] not in ("REAL", "CARD"))).split(",")


def Ln(n):
    return LINE.get(n)


def wt(n, k):
    """reel time of word k (negative = from the end) of line n"""
    return LINE[n]["words"][k]["t0"]


# ------------------------------------------------------------------------------------------------ Ep 5 expressions
def expr_state(ch, t):
    nm = "GUS" if ch is GUS else "PIP"
    st = dict(fL=0.0, fR=0.0, shape=None, scale=1.0, on=0.0, hL=0.0, hR=0.0, tL=0.0, tR=0.0, roll=None)

    def blend(name, k):
        if k <= 0:
            return
        tgt = dict(zip(("fL", "fR", "shape", "scale", "on", "hL", "hR", "tL", "tR"), STATES[name]))
        for key in ("fL", "fR", "scale", "on", "hL", "hR", "tL", "tR"):
            st[key] = lerp(st[key], tgt[key], k)
        if tgt["shape"] and k > 0.5:
            st["shape"] = tgt["shape"]

    if nm == "GUS":
        for L in TL["lines"]:                       # matter-of-fact: subtle annoyed cut while he explains
            if L["speaker"] == "GUS":
                k = win(t, L["t0"] - 0.15, L["t1"], 0.2, 0.4)
                st["fL"] = st["fR"] = max(st["fL"], 0.2 * k)
                st["on"] = max(st["on"], 0.65 * k)
                st["tL"] = st["tR"] = max(st["tL"], 10 * k)
        if Ln(4):                                   # "...Terrible to edit." slightly annoyed
            L = Ln(4); a = L["words"][3]["t0"]
            k = win(t, a, L["t1"], 0.1, 0.3)
            st["fL"] = st["fR"] = lerp(st["fL"], 0.45, k); st["tL"] = st["tR"] = lerp(st["tL"], 14, k)
        if Ln(12):                                  # weary: "You rebuild it. Surface by surface."
            blend("weary", 0.8 * win(t, Ln(12)["t0"], Ln(12)["t1"], 0.15, 0.3))
        if Ln(14):                                  # flat "...No."
            L = Ln(14); k = win(t, L["t0"] - 0.1, L["t1"] + 0.4, 0.06, 0.3)
            st["fL"] = st["fR"] = lerp(st["fL"], 0.55, k); st["tL"] = st["tR"] = lerp(st["tL"], 16, k)
        if Ln(13):                                  # eye-roll while Pip asks "Is it done yet?"
            L = Ln(13); u = (t - L["t0"]) / max(0.3, L["t1"] - L["t0"])
            if 0 <= u <= 1:
                st["roll"] = (math.cos(math.pi * (1 - u)) * 0.9, math.sin(math.pi * u) * 1.0)
    else:
        for n in (1, 5, 8, 11):                     # curious questions
            if Ln(n):
                blend("curious", win(t, Ln(n)["t0"], Ln(n)["t1"], 0.15, 0.3))
        if Ln(1):                                   # "Wait..." squint at the screen first
            L = Ln(1); k = win(t, L["t0"], L["words"][0]["t1"] + 0.2, 0.1, 0.2)
            st["fL"] = st["fR"] = max(st["fL"], 0.5 * k)
        if Ln(13):                                  # impatient double blink
            L = Ln(13); blend("impatient", win(t, L["t0"], L["t1"], 0.05, 0.3))
            for b0 in (L["t0"], L["t0"] + 0.24):
                bu = (t - b0) / 0.12
                if 0 <= bu < 1:
                    st["fL"] = st["fR"] = max(st["fL"], 1 - abs(2 * bu - 1))
        if Ln(15):                                  # pop to excited on "Illumaesthetic ... Look!"
            L = Ln(15); tw = L["t0"]
            if t >= tw - 0.03:
                pop = eback((t - tw + 0.03) / 0.2, 2.2)
                k = win(t, tw, L["t1"] + 2.0, 0.03, 0.3)
                st["scale"] = lerp(1.0, 1.2, k) * (0.92 + 0.08 * pop)
            blend("excited", win(t, L["words"][-1]["t0"] - 0.05, L["t1"] + 2.0, 0.08, 0.25))
    return st


# ------------------------------------------------------------------------------------------------ helpers
def face_rz(frm, to):
    d = Vector(to) - Vector(frm)
    return math.degrees(math.atan2(d.x, -d.y))


def head_pos(ch):
    bpy.context.view_layer.update()
    return ch.neck.matrix_world @ Vector((0, 0, ch.head_c))


def mesh_obj(name, verts, faces, m, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), smooth=False, ol=0.0):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    if smooth:
        me.shade_smooth()
    ob = bpy.data.objects.new(name, me)
    COLL.objects.link(ob)
    ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    ob.location = loc
    ob.rotation_euler = [math.radians(a) for a in rot]
    if ol > 0:
        add_mods(ob, 0.0, ol)
    return temp(ob)


def sphere_cloud(name, pts, r, m, parent=None):
    bm = bmesh.new()
    for p in pts:
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=r, matrix=Matrix.Translation(p))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    COLL.objects.link(ob)
    ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    return temp(ob)


def tube_path(name, pts, r, m, parent=None, nurbs=False, order=4):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = r
    cu.bevel_resolution = 3
    sp = cu.splines.new("NURBS" if nurbs else "POLY")
    sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts):
        sp.points[i].co = (p[0], p[1], p[2], 1.0)
    if nurbs:
        sp.order_u = order
        sp.use_endpoint_u = True
        sp.resolution_u = 24
    ob = bpy.data.objects.new(name, cu)
    COLL.objects.link(ob)
    ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    return temp(ob)


def pop(t, t0, d=0.25):
    """0 before t0, overshoot pop to 1 over d"""
    return 0.0 if t < t0 else eback(min(1.0, (t - t0) / d), 1.8)


# ------------------------------------------------------------------------------------------------ the bumper (one surface)
TH = 1.2                       # half wrap angle (rad)


def bpt(u, v):
    """Cartoon bumper surface: u 0..1 along the bumper, v 0..1 bottom -> top; front faces -Y; ~1.64 m wide, 0.42 m tall."""
    th = (u - 0.5) * 2 * TH
    n = Vector((math.sin(th), -math.cos(th), 0))
    c = Vector((0.82 * math.sin(th) / math.sin(TH), -0.75 * (math.cos(th) - math.cos(TH)), 0))
    out = 0.055 * math.sin(math.pi * v) - 0.05 * v + (0.03 if v < 0.12 else 0.0) * (1 - v / 0.12)
    return c + n * out + Vector((0, 0, 0.42 * v))


def bnorm(u, v):
    e = 1e-3
    a = bpt(min(1, u + e), v) - bpt(max(0, u - e), v)
    b = bpt(u, min(1, v + e)) - bpt(u, max(0, v - e))
    return a.cross(b).normalized() * -1 if a.cross(b).y > 0 else a.cross(b).normalized()


NU, NV = 24, 7
_rng = random.Random(5)
JIT = [[Vector((_rng.uniform(-1, 1), _rng.uniform(-1, 1), _rng.uniform(-1, 1))) * 0.006 for _ in range(NV)] for _ in range(NU)]


def grid_pts(scale=1.0):
    return [[(bpt(i / (NU - 1), j / (NV - 1)) + JIT[i][j]) * scale for j in range(NV)] for i in range(NU)]


def mesh_bumper(name, m, parent=None, loc=(0, 0, 0), u_max=1.0, u_min=0.0, drag=None, scale=1.0, ol=0.012, rot=(0, 0, 0)):
    """Faceted STL look: the scan grid triangulated (alternating diagonals), flat shaded. `drag` = (Vector offset, u0, v0,
    radius) pulls a clump of vertices (the 'terrible to edit' tear)."""
    P = grid_pts(scale)
    if drag is not None:
        off, u0, v0, rad = drag
        for i in range(NU):
            for j in range(NV):
                d = math.hypot((i / (NU - 1) - u0) * 1.64, (j / (NV - 1) - v0) * 0.42)
                w = max(0.0, 1 - d / rad) ** 1.5
                if w > 0:
                    jag = 0.6 + 0.8 * ((i * 7 + j * 3) % 5) / 4.0      # uneven: tears, not a smooth pull
                    P[i][j] = P[i][j] + off * (w * jag)
    verts, faces, idx = [], [], {}
    for i in range(NU):
        for j in range(NV):
            idx[i, j] = len(verts); verts.append(P[i][j])
    for i in range(NU - 1):
        if not (u_min - 1e-6 <= i / (NU - 1) and (i + 1) / (NU - 1) <= u_max + 1e-6):
            continue
        for j in range(NV - 1):
            a, b, c, d = idx[i, j], idx[i + 1, j], idx[i + 1, j + 1], idx[i, j + 1]
            if (i + j) % 2:
                faces += [(a, b, c), (a, c, d)]
            else:
                faces += [(a, b, d), (b, c, d)]
    used = sorted({k for f in faces for k in f})
    remap = {k: n for n, k in enumerate(used)}
    return mesh_obj(name, [verts[k] for k in used], [[remap[k] for k in f] for f in faces], m, parent, loc, rot, ol=ol)


def wire_bumper(name, m, parent=None, loc=(0, 0, 0), frac=1.0, scale=1.0, r=0.0045):
    """Triangle edges of the mesh as thin tubes; `frac` reveals them in a sweep along u (points -> triangles)."""
    P = grid_pts(scale)
    segs = []
    for i in range(NU):
        for j in range(NV):
            nb = [(i + 1, j), (i, j + 1)]
            nb.append((i + 1, j + 1) if (i + j) % 2 else None)
            if (i + j) % 2 == 0:
                nb.append((i + 1, j - 1) if j > 0 and i + 1 < NU else None)
            for q in nb:
                if q and q[0] < NU and 0 <= q[1] < NV:
                    um = (i + q[0]) / 2 / (NU - 1)
                    if um <= frac:
                        segs.append((P[i][j], P[q[0]][q[1]]))
    if not segs:
        return None
    bm = bmesh.new()
    for a, b in segs:
        d = b - a
        L = d.length
        M = Matrix.Translation((a + b) / 2) @ d.to_track_quat("Z", "Y").to_matrix().to_4x4()
        bmesh.ops.create_cone(bm, cap_ends=False, segments=5, radius1=r * scale, radius2=r * scale, depth=L, matrix=M)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); COLL.objects.link(ob); ob.data.materials.append(m)
    if parent:
        ob.parent = parent
    ob.location = loc
    return temp(ob)


def facet_bumper(name, parent=None, u_min=0.0, u_max=1.0, nu=5, nv=3, r=0.006):
    """Exaggerated STL for 'smooth at any zoom' (owner 2026-11-18: make the angles obvious): the same surface on a very
    coarse grid, every triangle a hard flat facet in alternating light/dark tones with a dark edge line, so the jagged
    silhouette and the facets read at a glance next to the smooth STEP."""
    P = [[bpt(u_min + (u_max - u_min) * i / nu, j / nv) for j in range(nv + 1)] for i in range(nu + 1)]
    tris = []
    for i in range(nu):
        for j in range(nv):
            a, b, c, d = P[i][j], P[i + 1][j], P[i + 1][j + 1], P[i][j + 1]
            tris += [(a, b, c), (a, c, d)] if (i + j) % 2 else [(a, b, d), (b, c, d)]
    for k, tone in enumerate(("#e2e6e2", "#9aa39b")):
        sub = tris[k::2]
        verts = [v for t3 in sub for v in t3]
        mesh_obj(f"{name}_{k}", verts, [(3 * n, 3 * n + 1, 3 * n + 2) for n in range(len(sub))], mat(tone), parent, ol=0.006)
    seen, bm = set(), bmesh.new()
    for t3 in tris:
        for a, b in ((t3[0], t3[1]), (t3[1], t3[2]), (t3[2], t3[0])):
            key = tuple(sorted((tuple(round(x, 5) for x in a), tuple(round(x, 5) for x in b))))
            if key in seen:
                continue
            seen.add(key)
            dv = b - a
            M = Matrix.Translation((a + b) / 2) @ dv.to_track_quat("Z", "Y").to_matrix().to_4x4()
            bmesh.ops.create_cone(bm, cap_ends=False, segments=6, radius1=r, radius2=r, depth=dv.length, matrix=M)
    me = bpy.data.meshes.new(name + "_edges"); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name + "_edges", me); COLL.objects.link(ob); ob.data.materials.append(emit("#141714", 1.0))
    if parent:
        ob.parent = parent
    return temp(ob)


PATCH_U, PATCH_V = 4, 2
PATCH_TONES = ("#d9ddd9", "#c3cac4")


def smooth_bumper(name, parent=None, loc=(0, 0, 0), u_max=1.0, u_min=0.0, scale=1.0, tint=1.0, res=4, ol=0.010, rot=(0, 0, 0)):
    """STEP look: the same surface, smooth, split into PATCH_U x PATCH_V patches (each its own object, so the toon outline
    draws the patch seams). `tint` 0 = plain silver-white, 1 = alternating patch tones."""
    obs = []
    nu, nv = (NU - 1) * res // PATCH_U, (NV - 1) * res // PATCH_V
    for pu in range(PATCH_U):
        for pv in range(PATCH_V):
            ua, ub = pu / PATCH_U, (pu + 1) / PATCH_U
            if ub <= u_min + 1e-6 or ua >= u_max - 1e-6:
                continue
            ua, ub = max(ua, u_min), min(ub, u_max)
            va, vb = pv / PATCH_V, (pv + 1) / PATCH_V
            verts, faces = [], []
            for i in range(nu + 1):
                for j in range(nv + 1):
                    verts.append(bpt(ua + (ub - ua) * i / nu, va + (vb - va) * j / nv) * scale)
            for i in range(nu):
                for j in range(nv):
                    a = i * (nv + 1) + j
                    faces.append((a, a + nv + 1, a + nv + 2, a + 1))
            tone = PATCH_TONES[(pu + pv) % 2] if tint > 0.5 else "#d4d8d4"
            obs.append(mesh_obj(f"{name}_{pu}{pv}", verts, faces, mat(tone), parent, loc, rot, smooth=True, ol=ol))
    return obs


CP_U = [0.0, 0.18, 0.36, 0.5, 0.64, 0.82, 1.0]


def nurbs_edge(name, parent=None, loc=(0, 0, 0), lift=0.0, show_cp=True, scale=1.0, glow=1.0):
    """The bumper's top edge as a real NURBS curve (order 4) through 7 control points floating just above it; the control
    polygon and points drawn. `lift` raises the middle control point (the curve follows: it's an equation)."""
    cps = []
    for k, u in enumerate(CP_U):
        p = (bpt(u, 1.0) + bnorm(u, 1.0) * 0.02 + Vector((0, 0, 0.06))) * scale
        if k == 3:
            p = p + Vector((0, 0, lift)) * scale
        cps.append(p)
    tube_path(name + "_crv", cps, 0.008 * scale, emit("sage_l", 1.6 * glow), parent, nurbs=True)
    if show_cp:
        tube_path(name + "_poly", cps, 0.0025 * scale, mat("#3a3d3a"), parent)
        sphere_cloud(name + "_cp", cps, 0.02 * scale, mat("white"), parent)
    for ob in [o for o in _temp if o.name.startswith(name)]:
        ob.location = Vector(loc)
    return cps


# ------------------------------------------------------------------------------------------------ props
def printer(name, loc, s=1.0, head_x=0.0, part_h=0.0, part_kind="mesh"):
    """Generic cartoon FDM printer (no brand): dark frame, sage gantry, bed; a mini bumper grows on the bed (0..1)."""
    g = temp(empty(name, None, loc))
    g.scale = (s, s, s)
    for x in (-0.32, 0.32):
        for y in (-0.22, 0.22):
            box(f"{name}_post{x}{y}", (0.04, 0.04, 0.62), (x, y, 0.31), mat("dark"), g, ol=0.008)
    box(f"{name}_top", (0.7, 0.48, 0.04), (0, 0, 0.64), mat("dark"), g, bevel=0.01, ol=0.008)
    box(f"{name}_base", (0.72, 0.5, 0.08), (0, 0, 0.04), mat("#3a3d3a"), g, bevel=0.015, ol=0.01)
    box(f"{name}_bed", (0.52, 0.36, 0.02), (0, 0, 0.11), mat("metal"), g, ol=0.006)
    box(f"{name}_gantry", (0.66, 0.05, 0.05), (0, 0, 0.5), mat("sage"), g, bevel=0.01, ol=0.006)
    hd = box(f"{name}_head", (0.08, 0.09, 0.1), (head_x, 0, 0.47), mat("sage_l"), g, bevel=0.01, ol=0.006)
    cyl(f"{name}_nozzle", 0.012, 0.05, (head_x, 0, 0.405), mat("metal"), g, r2=0.003)
    if part_h > 0.01:
        ps = 0.2
        pg = temp(empty(f"{name}_partg", g, (0, 0.02, 0.12)))
        pg.scale = (1, 1, part_h)
        if part_kind == "mesh":
            mesh_bumper(f"{name}_part", mat("scan"), pg, scale=ps, ol=0.004)
        else:
            smooth_bumper(f"{name}_part", pg, scale=ps, ol=0.003)
    return g


def mill(name, loc, s=1.0, spin=0.0, part=False):
    """Generic cartoon CNC mill (no brand): heavy base, column, head with spindle, table."""
    g = temp(empty(name, None, loc))
    g.scale = (s, s, s)
    box(f"{name}_base", (0.78, 0.6, 0.22), (0, 0, 0.11), mat("#3a3d3a"), g, bevel=0.02, ol=0.01)
    box(f"{name}_table", (0.62, 0.42, 0.06), (0, -0.04, 0.25), mat("metal"), g, bevel=0.01, ol=0.008)
    for k in range(4):
        box(f"{name}_slot{k}", (0.6, 0.012, 0.004), (0, -0.2 + k * 0.11, 0.283), mat("dark"), g)
    box(f"{name}_col", (0.22, 0.2, 0.9), (0, 0.28, 0.55), mat("sage"), g, bevel=0.02, ol=0.01)
    box(f"{name}_head", (0.26, 0.32, 0.22), (0, 0.1, 0.82), mat("sage_l"), g, bevel=0.02, ol=0.01)
    sp = temp(empty(f"{name}_spin", g, (0, 0.02, 0.7), (0, 0, spin)))
    cyl(f"{name}_spindle", 0.045, 0.12, (0, 0, -0.02), mat("metal"), sp, ol=0.006)
    box(f"{name}_flute", (0.012, 0.03, 0.12), (0, 0, -0.1), mat("dark"), sp)
    cyl(f"{name}_tool", 0.014, 0.12, (0, 0, -0.12), mat("metal"), sp)
    if part:
        pg = temp(empty(f"{name}_partg", g, (0, -0.04, 0.29)))
        smooth_bumper(f"{name}_part", pg, scale=0.2, ol=0.003)
    return g


def tick_badge(name, loc, k, s=1.0, n=(0, -1, 0)):
    """Green tick in a sage disc (pops with k 0..1)."""
    if k <= 0.01:
        return None
    g = temp(empty(name, None, loc))
    g.rotation_euler = Vector((0, 0, 0)).to_track_quat("Z", "Y").to_euler()
    q = Vector(n).to_track_quat("-Y", "Z")
    g.rotation_euler = q.to_euler()
    g.scale = (s * k, s * k, s * k)
    cyl(f"{name}_disc", 0.12, 0.03, (0, 0, 0), emit("sage", 1.0), g, axis="Y", seg=40, ol=0.008)
    box(f"{name}_a", (0.035, 0.02, 0.09), (-0.035, -0.02, -0.01), emit("white", 1.0), g, rot=(0, 45, 0))
    box(f"{name}_b", (0.035, 0.02, 0.16), (0.03, -0.02, 0.02), emit("white", 1.0), g, rot=(0, -38, 0))
    return g


def question_badge(name, loc, k, s=1.0, n=(0, -1, 0)):
    """'?' made of shapes (no font): red disc, white hook arc, stem and dot."""
    if k <= 0.01:
        return None
    g = temp(empty(name, None, loc))
    g.rotation_euler = Vector(n).to_track_quat("-Y", "Z").to_euler()
    g.scale = (s * k, s * k, s * k)
    cyl(f"{name}_disc", 0.13, 0.03, (0, 0, 0), emit("red", 1.0), g, axis="Y", seg=40, ol=0.008)
    hook = temp(empty(f"{name}_hk", g, (0, -0.02, 0.035), (90, 0, 0)))
    pts = []
    for k2 in range(16):
        a = math.radians(200 - k2 * (250 / 15))
        pts.append(Vector((0.045 * math.cos(a), 0.045 * math.sin(a), 0)))
    pts += [Vector((0.0, -0.06, 0))]
    tube_path(f"{name}_arc", pts, 0.013, emit("white", 1.0), hook)
    cyl(f"{name}_dot", 0.016, 0.02, (0, -0.02, -0.075), emit("white", 1.0), g, axis="Y", seg=16)
    return g


def cursor_hand(name, loc, s=1.0):
    """Gus's floating mitt as an on-screen 'cursor' (same vinyl look as his hands)."""
    g = temp(empty(name, None, loc))
    blob(f"{name}_mitt", tuple(x * s for x in GUS_SPEC["hand"]), (0, 0, 0), mat("vinyl", hl=True), g, ol=0.02 * s)
    blob(f"{name}_thumb", tuple(x * s * 0.45 for x in GUS_SPEC["hand"]), (-0.07 * s, -0.02 * s, 0.03 * s),
         mat("vinyl", hl=True), g, ol=0.015 * s)
    return g


def slider(name, loc, k, s=1.0):
    """Hole-size slider: sage track, white knob at k (0..1). No numbers."""
    g = temp(empty(name, None, loc))
    g.scale = (s, s, s)
    box(f"{name}_track", (0.5, 0.02, 0.03), (0, 0, 0), mat("sage_l"), g, bevel=0.01, ol=0.006)
    box(f"{name}_fill", (0.5 * k + 0.001, 0.025, 0.032), (-0.25 + 0.25 * k, -0.002, 0), mat("sage"), g)
    cyl(f"{name}_knob", 0.035, 0.05, (-0.25 + 0.5 * k, -0.01, 0), mat("white"), g, axis="Y", seg=24, ol=0.008)
    return g


def hole(name, u, v, r, parent=None, scale=1.0, loc=(0, 0, 0)):
    p = bpt(u, v) * scale + Vector(loc)
    n = bnorm(u, v)
    g = temp(empty(name, parent, p + n * 0.004 * scale))
    g.rotation_euler = n.to_track_quat("Z", "Y").to_euler()
    cyl(f"{name}_d", r * scale, 0.004 * scale, (0, 0, 0), mat("#1d201d"), g, seg=32)
    cyl(f"{name}_rim", r * scale * 1.08, 0.002 * scale, (0, 0, -0.001 * scale), mat("#8f958f"), g, seg=32)
    return g


# ------------------------------------------------------------------------------------------------ the digital stage
VOID = Vector((60.0, 0.0, 0.0))


def build_void():
    g = empty("VOID", None, VOID)
    box("void_back", (14, 0.05, 8), (0, 4.0, 3.0), emit("#151816", 1.0), g)
    box("void_floor", (14, 10, 0.02), (0, 0, -0.01), mat("#2a2e2b"), g)
    for k in range(-6, 7):                                   # faint sage grid on the floor
        box(f"void_gx{k}", (0.012, 10, 0.003), (k * 0.5, 0, 0.002), emit("#3d6b4b", 0.6), g)
    for k in range(-8, 9):
        box(f"void_gy{k}", (14, 0.012, 0.003), (0, k * 0.5, 0.002), emit("#3d6b4b", 0.6), g)
    for ob in g.children_recursive:
        for attr in ("visible_shadow",):
            if hasattr(ob, attr) and ob.name.startswith(("void_back", "void_g")):
                setattr(ob, attr, False)
    return g


VOIDG = build_void()
BZ = 0.45                      # bumper base height above the void floor
B0 = VOID + Vector((0, 0, BZ))

# laptop screen content: own empty in the screen plane (local XY, +Z toward the viewer); pilot UI hidden
EP5UI = empty("EP5UI", UI.parent, UI.location, tuple(math.degrees(a) for a in UI.rotation_euler))


def screen_bumper(kind="mesh", frac=1.0, patches=0):
    """Mini bumper drawn on the laptop screen (EP5UI): 'mesh' faceted, 'cloud' points, 'patches' = n smooth patches laid
    over the mesh (E10)."""
    g = temp(empty("scr_b", EP5UI, (0, -0.045, 0.01), (-90, 0, 0)))
    g.scale = (1, 0.15, 1)                                  # flattened onto the screen
    s = 0.2
    if kind == "cloud":
        P = grid_pts(s)
        sphere_cloud("scr_pts", [P[i][j] for i in range(NU) for j in range(NV)], 0.0045, emit("sage_l", 1.2), g)
    else:
        mesh_bumper("scr_mesh", mat("scan"), g, scale=s, ol=0.0)
        wire_bumper("scr_wire", emit("#2f3330", 1.0), g, scale=s, r=0.0012 / s * 0.8)
    if patches:
        obs = smooth_bumper("scr_patch", g, scale=s * 1.012, ol=0.0)
        for k, ob in enumerate(obs):
            set_vis(ob, k < patches)
    return g


# ------------------------------------------------------------------------------------------------ staging
LAP = Vector((3.35, 3.05, 0.955))
PIP_AT = Vector((2.78, 2.62, 0))
GUS_AT = Vector((3.95, 2.58, 0))
FACE_PT = Vector((3.35, 1.0, 0))   # characters turn 3/4 toward the room (camera side), heads toward the screen
SCR_C = None


def screen_centre():
    bpy.context.view_layer.update()
    return EP5UI.matrix_world.translation.copy()


def stage_bench(t, pip_look=(0.4, 0.3), gus_look=(-0.4, 0.3), pip_extra=None, gus_extra=None):
    """Pip left and Gus right of the laptop, both turned toward its screen (which faces the room / camera)."""
    sc = screen_centre()
    mp, lp = talk("PIP", t)
    mg, lg = talk("GUS", t)
    kp = dict(loc=tuple(PIP_AT), rz=face_rz(PIP_AT, FACE_PT), hips=(6, 0, 0), head=(4, 0, 30), armL=(-30, 0, 8), elbowL=-30,
              armR=(-12, 0, -8), mouth=mp, lid=lp, look=pip_look)
    if pip_extra:
        kp.update(pip_extra)
    kg = dict(loc=tuple(GUS_AT), rz=face_rz(GUS_AT, FACE_PT), hips=(4, 0, 0), head=(6, 0, -30), armL=(-12, 0, 8),
              armR=(-40, 0, -6), elbowR=-35, mouth=mg, lid=lg, look=gus_look)
    if gus_extra:
        kg.update(gus_extra)
    pose(PIP, **kp)
    pose(GUS, **kg)
    return sc


# ------------------------------------------------------------------------------------------------ shots
def anim_E1(fr):
    """'Wait... what's a mesh?' Pip squints at the mesh on the laptop; push into the screen at the end."""
    t = fr / FPS
    screen_bumper("mesh")
    sc = stage_bench(t, pip_look=(0.5, 0.2), gus_look=(-0.7, 0.4))
    k = prog(fr, "E1")
    c0, t0 = Vector((3.35, -0.1, 1.35)), Vector((3.35, 2.7, 0.95))
    if k < 0.72:
        look(cam, c0, t0, 28)
    else:
        e = ease((k - 0.72) / 0.28)
        tgt = t0.lerp(sc, e)
        loc = c0.lerp(sc + Vector((0, -0.42, 0.04)), e ** 1.6)
        look(cam, loc, tgt, lerp(28, 40, e))


def void_cam(dist, yaw, pitch, target=None, lens=40):
    pitch = pitch + 10
    tgt = (target if target is not None else B0 + Vector((0, -0.15, 0.2)))
    a, p = math.radians(yaw), math.radians(pitch)
    loc = tgt + Vector((dist * math.sin(a) * math.cos(p), -dist * math.cos(a) * math.cos(p), dist * math.sin(p)))
    look(cam, loc, tgt, lens)


def anim_E2(fr):
    """'A scan is millions of points.' Inside the computer: the bumper appears as a point cloud, sweeping in."""
    t = fr / FPS
    k = prog(fr, "E2")
    P = grid_pts()
    pts = []
    for i in range(NU):
        for j in range(NV):
            ti = 0.05 + 0.55 * (i / (NU - 1)) + 0.05 * ((j * 7) % 5) / 5
            if k >= ti:
                pts.append(P[i][j])
    if pts:
        sphere_cloud("cloud", pts, 0.017, emit("sage_l", 1.4), temp(empty("cloud_g", None, B0)))
    void_cam(lerp(3.3, 2.7, ease(k)), lerp(-24, -14, k), 14)


def anim_E3(fr):
    """'Join them up into tiny triangles. That's a mesh. An STL.' Points connect (sweep), then the faces fill in."""
    t = fr / FPS
    k = prog(fr, "E3")
    g = temp(empty("e3g", None, B0))
    P = grid_pts()
    sphere_cloud("cloud", [P[i][j] for i in range(NU) for j in range(NV)], 0.017 * (1 - 0.5 * cl((k - 0.5) / 0.2)),
                 emit("sage_l", 1.4), g)
    wf = cl(k / 0.45)
    wire_bumper("wire", emit("sage_l", 1.2), g, frac=wf)
    t_fill = wt(3, 6)                                       # "That's a mesh."
    if t >= t_fill - 0.15:
        mesh_bumper("mesh", mat("scan"), g, u_max=cl((t - t_fill + 0.15) / 0.6))
    void_cam(lerp(2.6, 2.35, ease(k)), lerp(-14, 8, k), lerp(14, 18, k))


def anim_E4(fr):
    """'Perfect for printing.' mesh -> cartoon printer -> tick. 'Terrible to edit.' Gus's cursor-hand drags an edge: tear."""
    t = fr / FPS
    L = Ln(4)
    t_edit = L["words"][3]["t0"]                            # "Terrible"
    g = temp(empty("e4g", None, B0))
    pr = VOID + Vector((1.05, -0.55, 0))
    if t < t_edit - 0.1:
        k = cl((t - L["t0"] + 0.2) / max(0.4, t_edit - L["t0"]))
        mesh_bumper("mesh", mat("scan"), g)
        printer("printer", pr, s=1.0, head_x=0.18 * math.sin(t * 9), part_h=cl(k * 1.15))
        tick_badge("tick", pr + Vector((0, -0.25, 0.95)), pop(t, t_edit - 0.55), s=1.2)
        void_cam(3.6, 8, 12, target=VOID + Vector((0.45, -0.35, 0.5)), lens=34)
    else:
        u = cl((t - t_edit) / 0.9)
        off = Vector((0.0, -0.32, 0.38)) * ease(u)
        mesh_bumper("mesh", mat("scan"), g, drag=(off, 0.36, 1.0, 0.33))
        wire_bumper("wire", emit("#2f3330", 1.0), g)
        hp = B0 + bpt(0.36, 1.0) + off + Vector((0, -0.06, 0.08))
        cursor_hand("hand", hp, s=1.4)
        void_cam(2.2, -18, 16, target=B0 + bpt(0.4, 0.75) + Vector((0, 0, 0.05)), lens=38)


def anim_E5(fr):
    """Pip: 'And STEP?' close at the bench, curious, looking up at Gus."""
    t = fr / FPS
    screen_bumper("mesh")
    stage_bench(t, pip_look=(0.8, 0.8), gus_look=(-0.8, 0.2), pip_extra=dict(head=(-14, 0, 30)))
    h = head_pos(PIP)
    k = prog(fr, "E5")
    rz = PIP.root.rotation_euler.z
    fwd = Vector((math.sin(rz), -math.cos(rz), 0))
    side = Vector((math.cos(rz), math.sin(rz), 0))
    look(cam, h + fwd * (1.35 - 0.1 * k) + side * 0.35 + Vector((0, 0, 0.05)), h + Vector((0, 0, -0.1)), 40)


def anim_E6(fr):
    """'STEP is NURBS. Not points... equations.' The mesh re-forms as smooth patches (sweep), then the top edge appears
    as a real NURBS curve with its control points; the middle control point lifts and the curve follows."""
    t = fr / FPS
    k = prog(fr, "E6")
    L = Ln(6)
    g = temp(empty("e6g", None, B0))
    us = cl((t - L["t0"] + 0.1) / 1.1)                     # sweep over "STEP is NURBS"
    if us < 1:
        mesh_bumper("mesh", mat("scan"), g, u_min=us)
    if us > 0:
        smooth_bumper("step", g, u_max=us)
    t_eq = wt(6, -1)                                        # "equations."
    if t >= t_eq - 0.6:
        pk = pop(t, t_eq - 0.6, 0.35)
        lift = 0.1 * math.sin(math.pi * cl((t - t_eq) / 1.0)) if t > t_eq else 0.0
        cps = nurbs_edge("edge", g, lift=lift, show_cp=pk > 0.2, glow=pk)
    void_cam(lerp(2.75, 2.45, ease(k)), lerp(16, 4, k), 20)


def anim_E7(fr):
    """'Smooth at any zoom.' mesh corner vs STEP corner side by side, pushing in: facets get chunky, NURBS stays smooth.
    'Change a hole... it just updates.' a hole on the STEP bumper grows with a slider; the surface stays clean."""
    t = fr / FPS
    L = Ln(7)
    t_hole = wt(7, 4)                                       # "Change"
    if t < t_hole - 0.12:
        k = cl((t - L["t0"] + 0.15) / max(0.5, t_hole - L["t0"]))
        gl = temp(empty("e7l", None, B0 + Vector((-0.85, 0, 0))))   # mesh: its right end just left of the divider
        gr = temp(empty("e7r", None, B0 + Vector((0.85, 0, 0))))    # STEP: its left end just right of it
        facet_bumper("meshL", gl, u_min=0.62)
        smooth_bumper("stepR", gr, u_max=0.38, tint=0.0)
        temp(box("divider", (0.008, 0.008, 1.2), (VOID.x, VOID.y - 0.12, BZ + 0.3), emit("white", 1.0)))
        tgt = Vector((VOID.x, B0.y - 0.1, BZ + 0.3))
        d = lerp(1.5, 0.48, ease(k) ** 1.3)                # pushes in further: the facets get bigger, STEP stays smooth
        look(cam, tgt + Vector((0, -d, d * 0.28)), tgt, 40)
    else:
        u = cl((t - t_hole) / max(0.6, L["t1"] - t_hole))
        kk = ease(cl(u * 1.3))
        g = temp(empty("e7g", None, B0))
        smooth_bumper("step", g, tint=0.0)
        hole("hole", 0.34, 0.5, lerp(0.03, 0.085, kk), loc=B0)
        sl = B0 + bpt(0.34, 1.0) + Vector((0.0, -0.35, 0.32))
        slider("slider", sl, kk, s=0.8)
        cursor_hand("hand", sl + Vector((0.8 * (-0.25 + 0.5 * kk), -0.06, 0.06)), s=1.0)
        void_cam(1.7, -18, 10, target=B0 + bpt(0.34, 0.6) + Vector((0, 0, 0.12)), lens=40)


def anim_E8(fr):
    """Pip: 'So which one?' two-shot at the bench; the screen shows the mesh and the smooth bumper."""
    t = fr / FPS
    g = screen_bumper("mesh")
    g.location.x -= 0.0
    k = prog(fr, "E8")
    sw = 0.6 + 0.4 * math.sin(math.pi * 2 * k)              # looks from screen to Gus and back
    stage_bench(t, pip_look=(lerp(0.4, 0.9, sw), lerp(0.2, 0.8, sw)), gus_look=(-0.6, 0.4),
                pip_extra=dict(head=(-8, 0, lerp(10, 30, sw))))
    look(cam, Vector((3.35, 0.0, 1.35)), Vector((3.35, 2.7, 0.95)), 30)


def anim_E9(fr):
    """'Just printing it? The STL's fine.' mesh slides to the printer -> tick.
    'Making it on a machine? It has to be STEP.' mesh tries the mill -> '?', the STEP bumper goes in -> tick."""
    t = fr / FPS
    L9, L10 = Ln(9), Ln(10)
    pr, ml = VOID + Vector((-1.3, 0.3, 0)), VOID + Vector((1.3, 0.3, 0))
    # forked path on the floor
    for nm, a, b in (("pathL", VOID + Vector((0, -1.2, 0)), pr), ("pathR", VOID + Vector((0, -1.2, 0)), ml)):
        d = b - a
        temp(box(nm, (0.16, d.length, 0.01), (a + b) / 2 + Vector((0, 0, 0.006)), emit("#4b8a5d", 0.8),
                 rot=(0, 0, -math.degrees(math.atan2(d.x, d.y)))))
    t_mill = L10["t0"]
    t_step = wt(10, -2)                                     # "be STEP."
    # printer side
    kp = cl((t - L9["t0"]) / 1.2)
    printer("printer", pr, s=1.1, head_x=0.18 * math.sin(t * 9) if kp >= 1 else 0.0,
            part_h=cl((t - L9["t0"] - 1.0) / 0.8))
    if kp < 1:
        p = (VOID + Vector((0, -1.0, 0.3))).lerp(pr + Vector((0, 0, 0.75)), ease(kp))
        mesh_bumper("m1", mat("scan"), temp(empty("m1g", None, p)), scale=0.32)
    tick_badge("tick1", pr + Vector((0, -0.3, 1.05)), pop(t, L9["t0"] + 1.5), s=1.2)
    # mill side
    spin = t * 20
    mill_part = t > t_step + 0.9
    mill("mill", ml, s=1.1, spin=spin, part=mill_part)
    if t >= t_mill:
        km = cl((t - t_mill) / 1.0)
        if t < t_step:
            bounce = 0.0 if km < 0.8 else -0.25 * math.sin(math.pi * cl((t - t_mill - 0.8) / 0.4))
            p = (VOID + Vector((0, -1.0, 0.3))).lerp(ml + Vector((-0.1, -0.2, 0.55)), ease(km)) + Vector((-0.1, bounce, 0))
            mesh_bumper("m2", mat("scan"), temp(empty("m2g", None, p)), scale=0.32)
            question_badge("q", ml + Vector((0, -0.35, 1.25)), pop(t, t_mill + 0.85) * (1 - cl((t - t_step + 0.2) / 0.2)), s=1.2)
        elif not mill_part:
            ks = cl((t - t_step) / 0.9)
            p = (VOID + Vector((0, -1.0, 0.3))).lerp(ml + Vector((0, -0.05, 0.36)), ease(ks))
            smooth_bumper("s2", temp(empty("s2g", None, p)), scale=0.32 * lerp(1, 0.62, ks), ol=0.004)
        tick_badge("tick2", ml + Vector((0, -0.35, 1.25)), pop(t, t_step + 1.0), s=1.2)
    look(cam, VOID + Vector((0, -4.3, 2.3)), VOID + Vector((0, 0.15, 0.55)), 30)


def anim_E10(fr):
    """Pip: 'And turning a scan into a STEP?' Gus: 'You rebuild it. Surface by surface.' - patches go on one by one."""
    t = fr / FPS
    L12 = Ln(12)
    n = 0 if t < L12["t0"] else 1 + int((t - L12["t0"]) / 0.45)
    screen_bumper("mesh", patches=min(n, PATCH_U * PATCH_V))
    sc = stage_bench(t, pip_look=(0.8, 0.6), gus_look=(-0.5, 0.1),
                     gus_extra=dict(armR=(-58, 0, -10), elbowR=-30, head=(14, 0, -22)))
    k = prog(fr, "E10")
    look(cam, sc + Vector((-0.28, -1.3 + 0.15 * k, 0.32)), sc + Vector((-0.02, 0, -0.08)), 34)


def anim_E11(fr):
    """'Is it done yet?' Pip slumped on the stool under the spinning wall clock. Gus (off) '...No.'"""
    t = fr / FPS
    set_vis(STOOL, True)
    spd = 1.0 + 3.0 * cl((t - Ln(13)["t0"] + 0.5) / 1.5)
    HANDS["minute"].rotation_euler = (0, math.radians(150 + 400 * t * spd), 0)
    HANDS["second"].rotation_euler = (0, math.radians(260 + 1800 * t * spd), 0)
    for o in clock_blur(CLOCK, HANDS):
        temp(o)
    mp, lp = talk("PIP", t, 0.45)
    pose(PIP, loc=(-3.7, 2.68, 0.565), rz=-6, hips=(24, 0, 0), head=(10, 0, -8), armL=(-38, 0, 14), elbowL=-50,
         armR=(-38, 0, -14), elbowR=-50, legL=(-88, 0, 4), legR=(-88, 0, -4), mouth=mp, lid=lp, look=(0.3, 1))
    look(cam, (-3.5, -0.9, 1.6), (-3.82, 2.9, 1.62), 36)


S12_SPLIT = 0.42


def anim_E12(fr):
    """'Illumaesthetic does that. Look!' Pip holds his phone up; the camera pushes along the screen normal until the screen
    fills the frame on the last frame (the real section starts on the next frame)."""
    t = fr / FPS
    k = prog(fr, "E12")
    c, n, u, r = phone_pose_s11()
    mp, lp = talk("PIP", t)
    set_face(PIP, mp, lp, (0.6, 0.6))
    if k < S12_SPLIT:
        look(cam, c + n * 1.2 - r * 0.16 - u * 0.2, c - r * 0.16 - u * 0.2, 38, up=u)
    else:
        s12_cam(c, n, u, (k - S12_SPLIT) / (1 - S12_SPLIT))


ANIM5 = {k: globals()[f"anim_{k}"] for k in ("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12")}


def _purge_temp():
    """Remove this frame's temp objects (and their children) robustly: nested temps may already be gone with a parent."""
    for ob in list(_temp):
        stack = [ob]
        while stack:
            o = stack.pop()
            try:
                stack.extend(o.children)
                bpy.data.objects.remove(o, do_unlink=True)
            except ReferenceError:
                pass
    _temp.clear()


def reset_ep5():
    _purge_temp()
    reset()
    set_vis(CAR, False)
    set_vis(UI, False)
    set_vis(PIPSCAN, False)
    set_vis(EP5UI, True)
    STOOL.location = (-3.7, 2.7, 0)


# ------------------------------------------------------------------------------------------------ run
SFE = {s["id"]: (s["f0"], s["f1"]) for s in TL["shots"]}
SF.update(SFE)
lo_, hi_ = (int(x) for x in RANGE.split(":")) if RANGE else (0, 10 ** 9)
corners = {"doc": "Phone-screen corners (tl,tr,br,bl) in 1080x1920 px per E12 frame; screen renders as key colour #ff00ff.",
           "key_colour": KEY, "shots": {}}
CORN = os.path.join(OUT, "screen_corners.json")
for sh in SHOTS_EP5:
    f0, f1 = SFE[sh]
    d = os.path.join(OUT, sh)
    os.makedirs(d, exist_ok=True)
    per = {}
    for fr in range(f0, f1):
        final = os.path.join(d, f"{fr:04d}.png")
        need_c = sh == "E12"
        todo = (fr - f0) % EVERY == 0 and lo_ <= fr < hi_ and not os.path.exists(final) and (not ONLY or fr in ONLY)
        if not (todo or need_c):
            continue
        CUR_T = fr / FPS
        reset_ep5()
        ANIM5[sh](fr)
        bpy.context.view_layer.update()
        if need_c:
            per[str(fr)] = screen_corners_px()
        if not todo:
            continue
        scn.render.filepath = os.path.join(d, f"{fr:04d}_tmp")
        t0_ = time.time()
        bpy.ops.render.render(write_still=True)
        os.replace(os.path.join(d, f"{fr:04d}_tmp.png"), final)
        print(f"[ep5] {sh} {fr} {time.time() - t0_:.1f} s", flush=True)
    if per:
        corners["shots"][sh] = dict(frames=[f0, f1], per_frame=per)
        json.dump(corners, open(CORN, "w"), indent=1)
