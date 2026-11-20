"""Blender: a corrected copy of the lookbook game model for the reel (owner's v1 notes). The site's GLB is not touched.

    blender -b -P tools/reel_model.py -- eps-toyota-mr2-spyder-v2.glb "MR2 Spyder_game.blend" Map13.png out.glb

What it changes, and the node each change lives in so that a kit state is still a hide list:
  * shading: every mesh welded and smooth-shaded with hard edges kept above 40 degrees ("polygon quality is visibly low":
    the published GLB is unwelded, so every triangle shaded flat);
  * body_hood_cut      the hood skin under the two vents, split off the body: hidden once the vents are fitted
                       ("hood needs to be cut out for the hood vents");
  * body_fender_cut    the piece of each front fender that is cut away for the skirt's arch vent, from the owner's own scan
                       of the cut piece ("Cutted fender Piece" in the kit file): hidden once the skirts are fitted;
  * part_side_skirts   mirrored to the right side (the published node is the left side only);
  * part_tc_wing       the TC wing from the kit file ("rear wing" collection: DEMO_1.006-009 + Bolt.001), registered like the kit;
  * exhaust_stock / exhaust_diffuser   the tail pipe split off the trim; a raised copy that clears the diffuser;
  * tail lamps         the rip's own lights texture (lights_lod0.png, "Map #13" in MR-S_1.blend) back on the lamp faces, whose
                       UVs the GLB still carries; the published GLB shades them flat red.
Kit pieces in the kit file are in the scan's frame: the transform to the GLB frame is found here by ICP of three kit pieces
(Ducktail, Hood Vent, Left Siderskirt + Arch Vent) onto the same pieces in the GLB.
"""
import sys
import bpy, bmesh, numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

a = sys.argv[sys.argv.index("--") + 1:]
GLB, KIT, TEX, OUT = a[:4]
TEX_LENS = TEX.replace(".png", "_lens.png")   # same atlas with alpha: the red lens 66 % opaque, its two clear windows 10 %
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
scene = bpy.context.scene
OBJ = {o.name: o for o in bpy.data.objects}
MAT = {m.name: m for m in bpy.data.materials}

# ---- kit file pieces ------------------------------------------------------------------------------------------------
WANT = ["Ducktail", "Hood Vent lft", "Left Siderskirt", "Left Arch Vent ", "Cutted fender Piece", "DEMO_1.006", "DEMO_1.007", "DEMO_1.008",
        "DEMO_1.009", "Bolt.001"]
with bpy.data.libraries.load(KIT, link=False) as (src, dst):
    dst.objects = [n for n in WANT if n in src.objects]
kit = {}
for o in dst.objects:
    scene.collection.objects.link(o); kit[o.name] = o
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()


def eval_world(o):
    """evaluated (modifiers applied) world-space vertices and triangles"""
    e = o.evaluated_get(dg); me = e.to_mesh(); me.calc_loop_triangles()
    M = np.array(e.matrix_world)
    v = np.array([x.co[:] for x in me.vertices], np.float64) @ M[:3, :3].T + M[:3, 3]
    t = np.array([lt.vertices[:] for lt in me.loop_triangles], np.int64)
    e.to_mesh_clear()
    return v, t


def kd(points):
    k = KDTree(len(points))
    for i, p in enumerate(points):
        k.insert(p, i)
    k.balance(); return k


# ---- registration: scan frame -> GLB frame --------------------------------------------------------------------------
pairs = [("Ducktail", "part_duckbill"), ("Hood Vent lft", "part_hood_vents"), ("Left Siderskirt", "part_side_skirts"), ("Left Arch Vent ", "part_side_skirts")]
src_pts, trees = [], []
rng = np.random.default_rng(0)
for s, t in pairs:
    v, _ = eval_world(kit[s]); v = v[rng.choice(len(v), min(len(v), 3000), replace=False)]
    tv, _ = eval_world(OBJ[t]); src_pts.append(v); trees.append((kd(tv), tv))
R = np.eye(3); T = np.array([0.0, -1.619, 0.595])
for it in range(60):
    P, Q = [], []
    lim = 0.05 if it < 8 else 0.015 if it < 25 else 0.008
    for v, (k, tv) in zip(src_pts, trees):
        w = v @ R.T + T
        for p0, p in zip(v, w):
            co, i, d = k.find(p)
            if d < lim:
                P.append(p0); Q.append(co[:])
    P, Q = np.array(P), np.array(Q); pc, qc = P.mean(0), Q.mean(0)
    U, S, Vt = np.linalg.svd((P - pc).T @ (Q - qc)); D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
    R = Vt.T @ D @ U.T; T = qc - R @ pc
res = np.linalg.norm(P @ R.T + T - Q, axis=1)
print(f"[reel] registration: {len(P)} pairs, median {np.median(res) * 1000:.2f} mm, 90% {np.percentile(res, 90) * 1000:.2f} mm, T {T.round(4)}, "
      f"rot {np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))):.3f} deg")
REG = lambda v: v @ R.T + T


def new_obj(name, verts, tris, mats, tri_mat=None):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in verts], [], [tuple(t) for t in tris]); me.update()
    for m in mats:
        me.materials.append(m)
    if tri_mat is not None:
        me.polygons.foreach_set("material_index", np.asarray(tri_mat, np.int32))
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o); return o


# ---- TC wing --------------------------------------------------------------------------------------------------------
vs, ts, tm, off = [], [], [], 0
for n in ("DEMO_1.006", "DEMO_1.007", "DEMO_1.008", "DEMO_1.009", "Bolt.001"):
    if n not in kit:
        print("[reel] wing piece missing:", n); continue
    v, t = eval_world(kit[n]); v = REG(v)
    print(f"[reel] wing piece {n}: {len(t)} tris, lo {v.min(0).round(3)} hi {v.max(0).round(3)}")
    vs.append(v); ts.append(t + off); tm += [1 if n.startswith("Bolt") else 0] * len(t); off += len(v)
wing = new_obj("part_tc_wing", np.vstack(vs), np.vstack(ts), [MAT["plastic_black"], MAT["chrome"]], tm)
fender_pts = REG(eval_world(kit["Cutted fender Piece"])[0])
print("[reel] fender cut piece lo", fender_pts.min(0).round(3), "hi", fender_pts.max(0).round(3))
for o in kit.values():
    bpy.data.objects.remove(o, do_unlink=True)

# ---- weld + smooth shading ------------------------------------------------------------------------------------------
def smooth(o, angle=40.0):
    me = o.data
    for nm in ("custom_normal", "sharp_face"):
        if nm in me.attributes:
            me.attributes.remove(me.attributes[nm])
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    lim = np.radians(angle)
    for e in bm.edges:
        e.smooth = bool(len(e.link_faces) == 2 and e.calc_face_angle(0.0) < lim)
    for f in bm.faces:
        f.smooth = True
    bm.to_mesh(me); bm.free(); me.update()


for o in list(bpy.data.objects):
    if o.type == "MESH" and o.name != "underbody":
        smooth(o)

# ---- split helpers --------------------------------------------------------------------------------------------------
def split_faces(o, pick, name):
    """Move the faces pick(bm) returns out of object o into a new object `name` (same materials, same transform)."""
    me = o.data; bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    sel = pick(bm, o.matrix_world)
    if not sel:
        bm.free(); print("[reel]", name, ": nothing selected"); return None
    area = sum(f.calc_area() for f in sel)
    keep = set(f.index for f in sel)
    bm2 = bm.copy(); bm2.faces.ensure_lookup_table()
    bmesh.ops.delete(bm2, geom=[f for f in bm2.faces if f.index not in keep], context="FACES")
    bmesh.ops.delete(bm, geom=sel, context="FACES")
    bm.to_mesh(me); bm.free(); me.update()
    me2 = bpy.data.meshes.new(name); bm2.to_mesh(me2); bm2.free()
    for m in me.materials:
        me2.materials.append(m)
    o2 = bpy.data.objects.new(name, me2); o2.matrix_world = o.matrix_world.copy(); scene.collection.objects.link(o2)
    print(f"[reel] {name}: {len(keep)} faces, {area * 1e4:.0f} cm2")
    return o2


# hood under the vents: a point is "under" when a ray straight up meets the vent within 12 cm, and so do points 2 cm to each side
vv, vt = eval_world(OBJ["part_hood_vents"])
vent = BVHTree.FromPolygons([Vector(p) for p in vv], [tuple(t) for t in vt])
up = Vector((0, 0, 1))


dn = Vector((0, 0, -1))


def under_vent(p, grow=0.012):
    """Inside the vent's footprint, with a margin: the vents are recessed INTO the hood (most of the stock skin lies up to
    3 cm above the louvres and hides them), so the ray goes both ways."""
    for dx, dy in ((0, 0), (grow, 0), (-grow, 0), (0, grow), (0, -grow)):
        q = Vector((p.x + dx, p.y + dy, p.z))
        if vent.ray_cast(q + Vector((0, 0, 0.0005)), up, 0.12)[0] is None and vent.ray_cast(q, dn, 0.12)[0] is None:
            return False
    return True


def pick_hood(bm, M):
    inreg = lambda c: -0.56 < c.x < 0.56 and -1.76 < c.y < -1.12 and c.z > 0.5
    for _ in range(6):                               # the filled hood has faces up to 60 cm2: cut the long edges first
        ed = {e for f in bm.faces if inreg(M @ f.calc_center_median()) for e in f.edges if e.calc_length() > 0.007}
        if not ed:
            break
        bmesh.ops.subdivide_edges(bm, edges=list(ed), cuts=1)
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3])
    bm.faces.ensure_lookup_table(); bm.faces.index_update(); bm.verts.index_update()
    out = []
    for f in bm.faces:
        c = M @ f.calc_center_median()
        if inreg(c) and under_vent(c, 0.0):          # by centre, no margin: the cut edge then runs under the vent's own rim
            out.append(f)
    return out


split_faces(OBJ["body"], pick_hood, "body_hood_cut")

# fender: body faces lying on the owner's scan of the cut-off piece (and its mirror image on the other side)
fk = kd(np.vstack([fender_pts, fender_pts * np.array([-1, 1, 1])]))


def pick_fender(bm, M):
    out = []
    for f in bm.faces:
        c = M @ f.calc_center_median()
        if abs(c.x) < 0.6 or c.y > -0.5 or c.y < -1.1:
            continue
        if fk.find(c)[2] < 0.008 and all(fk.find(M @ v.co)[2] < 0.014 for v in f.verts):
            out.append(f)
    return out


split_faces(OBJ["body"], pick_fender, "body_fender_cut")

# ---- exhaust --------------------------------------------------------------------------------------------------------
def islands(bm):
    seen = set(); out = []
    for f in bm.faces:
        if f.index in seen:
            continue
        st = [f]; seen.add(f.index); comp = []
        while st:
            g = st.pop(); comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index); st.append(h)
        out.append(comp)
    return out


def pick_exhaust(bm, M):
    bm.faces.index_update(); out = []
    for comp in islands(bm):
        v = np.array([(M @ x.co)[:] for g in comp for x in g.verts]); lo, hi = v.min(0), v.max(0)
        if lo[0] > 0.33 and hi[0] < 0.49 and lo[1] > 1.58 and hi[1] < 1.88 and lo[2] > 0.18 and hi[2] < 0.42 and len(comp) >= 12:
            out += comp
    return out


ex = split_faces(OBJ["trim"], pick_exhaust, "exhaust_stock")
if ex:
    ev = np.array([(ex.matrix_world @ v.co)[:] for v in ex.data.vertices])
    dv, _ = eval_world(OBJ["part_diffuser"])
    near = dv[(dv[:, 0] > ev[:, 0].min() - 0.03) & (dv[:, 0] < ev[:, 0].max() + 0.03) & (dv[:, 1] > ev[:, 1].min() - 0.03)]
    top = near[:, 2].max() if len(near) else dv[:, 2].max()
    pipe_lo = ev[ev[:, 1] > 1.75][:, 2].min()
    dz = max(0.0, top + 0.012 - pipe_lo)
    ex2 = ex.copy(); ex2.data = ex.data.copy(); ex2.name = "exhaust_diffuser"; scene.collection.objects.link(ex2)
    ex2.matrix_world = Matrix.Translation((0, 0, dz)) @ ex.matrix_world
    print(f"[reel] exhaust: lo {ev.min(0).round(3)} hi {ev.max(0).round(3)}; diffuser top under it {top:.3f}; pipe bottom {pipe_lo:.3f}; raised copy +{dz * 1000:.0f} mm")

# ---- tail lamps: the rip's lights texture ---------------------------------------------------------------------------
img = bpy.data.images.load(TEX)
lm = bpy.data.materials.new("lamp_tex"); lm.use_nodes = True
nt = lm.node_tree; b = nt.nodes["Principled BSDF"]; tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = img
nt.links.new(tx.outputs["Color"], b.inputs["Base Color"])
if "Emission Color" in b.inputs:                     # a little self-light, as a lamp unit has under its cover
    nt.links.new(tx.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = 0.25
b.inputs["Roughness"].default_value = 0.12
for k, v in (("Coat Weight", 1.0), ("Coat Roughness", 0.04)):
    if k in b.inputs:
        b.inputs[k].default_value = v
cm = bpy.data.materials.new("lamp_cover"); cm.use_nodes = True; cb = cm.node_tree.nodes["Principled BSDF"]
cb.inputs["Base Color"].default_value = (1.0, 0.9, 0.9, 1); cb.inputs["Roughness"].default_value = 0.03
cb.inputs["Alpha"].default_value = 0.14              # a thin clear cover: mostly see-through, still catches a highlight
for k, v in (("Coat Weight", 1.0), ("Coat Roughness", 0.02)):
    if k in cb.inputs:
        cb.inputs[k].default_value = v
cm.blend_method = "BLEND" if hasattr(cm, "blend_method") else None
zm = bpy.data.materials.new("lamp_lens"); zm.use_nodes = True; zt = zm.node_tree; zb = zt.nodes["Principled BSDF"]
zx = zt.nodes.new("ShaderNodeTexImage"); zx.image = bpy.data.images.load(TEX_LENS)
zt.links.new(zx.outputs["Color"], zb.inputs["Base Color"]); zt.links.new(zx.outputs["Alpha"], zb.inputs["Alpha"])
zb.inputs["Roughness"].default_value = 0.04
for k, v in (("Coat Weight", 1.0), ("Coat Roughness", 0.02)):
    if k in zb.inputs:
        zb.inputs[k].default_value = v
if hasattr(zm, "blend_method"):
    zm.blend_method = "BLEND"
tr = OBJ["trim"]; me = tr.data; me.materials.append(lm); li = len(me.materials) - 1; me.materials.append(cm); ci = li + 1; n_cov = 0
me.materials.append(zm); zi = ci + 1; n_lens = 0
names = [m.name for m in me.materials]
bm = bmesh.new(); bm.from_mesh(me); uvl = bm.loops.layers.uv.active; n_tex = 0
Mt = tr.matrix_world
for g in bm.faces:                                   # per face (connected pieces mix materials once welded)
    nm = names[g.material_index]
    if nm not in ("light_red", "light_inner"):
        continue
    c3 = Mt @ g.calc_center_median()
    if not (0.44 < abs(c3.x) < 0.80 and 1.5 < c3.y < 1.87 and 0.66 < c3.z < 0.92):
        continue
    uvs = np.array([l[uvl].uv[:] for l in g.loops]); c = uvs.mean(0)
    if np.abs(uvs).max() < 1e-4:                     # no UVs: the outer cover
        if nm == "light_red":
            g.material_index = ci; n_cov += 1
        continue
    lens = c[0] < 0.71 and 0.33 < c[1] < 0.81        # the atlas's big red shape with two clear windows = the red lens
    g.material_index = zi if lens else li; n_lens += lens; n_tex += 1
bm.to_mesh(me); bm.free(); me.update()
print("[reel] tail lamps: faces textured", n_tex, "of them lens (see-through)", n_lens, "cover faces made clear", n_cov)

# ---- side skirts: mirror to the right side if the node is one-sided ----------------------------------------------------
sk = OBJ["part_side_skirts"]; sv = np.array([(sk.matrix_world @ v.co)[:] for v in sk.data.vertices])
if sv[:, 0].min() > 0.2:
    bm = bmesh.new(); bm.from_mesh(sk.data)
    geo = bmesh.ops.duplicate(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:])["geom"]
    nv = [g for g in geo if isinstance(g, bmesh.types.BMVert)]; nf = [g for g in geo if isinstance(g, bmesh.types.BMFace)]
    Mi = sk.matrix_world.inverted() @ Matrix.Scale(-1, 4, (1, 0, 0)) @ sk.matrix_world
    bmesh.ops.transform(bm, matrix=Mi, verts=nv); bmesh.ops.reverse_faces(bm, faces=nf)
    bm.to_mesh(sk.data); bm.free(); sk.data.update(); print("[reel] side skirts mirrored to the right side")

smooth(wing, 35.0)
for n in ("body_hood_cut", "body_fender_cut", "exhaust_stock", "exhaust_diffuser", "part_tc_wing"):
    o = bpy.data.objects.get(n)
    if o:
        v = np.array([(o.matrix_world @ x.co)[:] for x in o.data.vertices]); print(f"[reel] node {n}: {len(o.data.polygons)} faces lo {v.min(0).round(3)} hi {v.max(0).round(3)}")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_apply=True, export_normals=True, export_materials="EXPORT", export_yup=True)
print("[reel] wrote", OUT)
