"""Cars for the DITL GR Corolla short: his GR Corolla (stock or full Epsilon kit), grandma's Corolla hatch, the WRX from video #1, an FL5 Type R.
All face -Y (nose at -Y), origin on the ground between the axles, like ditl_kit.car()."""
import bpy, bmesh, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots as W
from shots import mat, box, plane, R
from mathutils import Vector
S = "/home/user/epsilon-site/"
GRC = S + "showroom/models/eps-toyota-gr-corolla-v3.glb"; HATCH = S + "showroom/models/eps-toyota-corolla-hatch-e210-v3.glb"
WRX = S + "showroom/models/eps-subaru-wrx-vb-v3.glb"; FL5 = S + "wing-configurator/data/models/honda-civic-type-r-fl5-r4.glb"
KIT = ["part_front_lip_v2", "part_canards", "part_side_skirts_v2", "part_rear_spats_v2", "part_wrc_wing", "part_wing_strakes"]   # the full kit (V2 lip/skirts/spats, canards, WRC wing + strakes)
GRC_OFF = ["part_front_lip", "part_front_lip_2025", "part_side_skirts", "part_rear_spats", "part_spoiler_extension"]

def _imp(path, name):
    before = set(bpy.data.objects); mb = set(bpy.data.materials); bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]; root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    by = {}
    for o in new:
        by[o.name.split(".")[0]] = o
        if o.parent is None: o.parent = root
    mats = {m.name.split(".")[0]: m for m in bpy.data.materials if m not in mb}
    return root, by, mats

def _paint(m, col, rough=0.25, metal=0.0):
    b = [n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"][0]
    for l in list(b.inputs["Base Color"].links): m.node_tree.links.remove(l)
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal

def grc(name="grc", color=(0.62, 0.02, 0.025), kit=True, hide_glass=False, kitcol=(0.012, 0.012, 0.014)):
    """Returns root, by-name dict. kit=True: full Epsilon kit on (gloss black); kit=False: stock (kit parts present but hidden, for the unboxing)."""
    root, by, mats = _imp(GRC, name); _paint(mats["paint"], color)
    km = mats["paint"].copy(); km.name = name + "_kit"; _paint(km, kitcol, 0.18)
    for n in KIT + GRC_OFF:
        by[n].data.materials[0] = km
    for n in GRC_OFF: by[n].hide_render = True
    for n in KIT: by[n].hide_render = not kit
    by["body_roof_spoiler_stock"].hide_render = kit
    if hide_glass: by["glass"].hide_render = True
    return root, by

def hatch(name="hatch", color=(0.62, 0.54, 0.38), wing=False):
    root, by, mats = _imp(HATCH, name); _paint(mats["paint"], color, 0.35)
    km = mats["paint"].copy(); km.name = name + "_kit"; _paint(km, (0.012, 0.012, 0.014), 0.18)
    for n in ("part_front_lip", "part_mid_wing", "part_rear_spats", "part_side_skirts", "part_wrc_wing"):
        by[n].data.materials[0] = km; by[n].hide_render = not (wing and n == "part_wrc_wing")
    return root, by

def wrx(name="wrx", color=(0.02, 0.12, 0.55)):
    root, by, mats = _imp(WRX, name); _paint(mats["paint"], color)
    for n in ("body_front_bumper_stock", "body_rear_bumper_stock", "trim_side_stock", "trim_f1_blank_stock", "part_duckbill"):
        if n in by: by[n].hide_render = True
    return root, by

SIDE = (0.96, 1.36, -0.75, 1.25); SCR = (-0.45, 1.05)
def fl5(name="fl5", color=(0.93, 0.93, 0.95)):
    """FL5 Type R shell from the wing configurator (one mesh, nose +X): painted, glass faces dark, side windows cut open, real wheels, red badge."""
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    before = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=FL5); sh = [o for o in bpy.data.objects if o not in before and o.type == "MESH"][0]
    for o in [o for o in bpy.data.objects if o not in before and o is not sh]: bpy.data.objects.remove(o)
    mw = sh.matrix_world.copy(); sh.parent = None; me = sh.data; me.transform(mw); sh.matrix_world.identity()
    xs = [v.co.x for v in me.vertices]; cx = (min(xs) + max(xs)) / 2
    for v in me.vertices: x, y = v.co.x - cx, v.co.y; v.co.x, v.co.y = y, -x
    paint = W._flat_mat(name + "_paint", color, 0.22); gl = W._flat_mat(name + "_glass", (0.02, 0.025, 0.03), 0.08); me.materials.append(paint); me.materials.append(gl)
    bm = bmesh.new(); bm.from_mesh(me); bm.normal_update(); kill = []
    for f in bm.faces:
        c = f.calc_center_median(); n = f.normal
        if 0.97 < c.z < 1.34 and -0.72 < c.y < 1.45 and abs(c.x) > 0.45 and abs(n.x) > 0.3 and abs(n.z) < 0.8: kill.append(f)
        elif c.z > 0.95 and c.y < -0.3 and 0.45 < abs(n.z) < 0.955 and abs(c.x) < 0.74: f.material_index = 1      # windscreen
        elif c.z > 1.0 and 1.3 < c.y < 1.92 and abs(n.z) > 0.5 and abs(c.x) < 0.6: f.material_index = 1          # hatch glass
    bmesh.ops.delete(bm, geom=kill, context="FACES"); bm.to_mesh(me); bm.free()
    sh.name = name + "_shell"; sh.parent = root
    for pl in me.polygons: pl.use_smooth = True
    dk = W._flat_mat(name + "_dk", (0.03, 0.03, 0.035)); red = W._flat_mat(name + "_red", (0.8, 0.02, 0.02), 0.4, emit=0.5)
    W.realwheels(root, 0.8, -1.345, 1.368, z=0.32, glb=HATCH)
    box(name + "_int", (1.5, 2.4, 0.5), dk, loc=(0, 0.2, 0.42), parent=root, base="z"); box(name + "_seat", (0.5, 0.14, 0.75), W._flat_mat(name + "_seatm", (0.6, 0.03, 0.03)), loc=(0.4, 0.3, 0.5), parent=root, base="z")
    # the Type R wing: two uprights and a plane, black
    for sx in (-1, 1): box(f"{name}_wu{sx}", (0.04, 0.2, 0.2), dk, loc=(sx * 0.48, 2.02, 1.02), rot=(R(-12), 0, 0), parent=root, base="z")
    box(name + "_wing", (1.5, 0.26, 0.035), dk, loc=(0, 2.06, 1.22), rot=(R(-6), 0, 0), parent=root)
    for sx in (-1, 1): box(f"{name}_we{sx}", (0.03, 0.3, 0.1), dk, loc=(sx * 0.75, 2.06, 1.2), parent=root)
    return root, sh
