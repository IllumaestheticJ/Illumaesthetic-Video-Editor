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

CIVIC = S + "showroom/models/eps-honda-civic-hatch-fl-v3.glb"
def fl5(name="fl5", color=(0.93, 0.93, 0.95), hide_glass=True):
    """The Type R for the red light. The wing-configurator FL5 shell is one rough unpainted mesh (owner: "blocky in all scenes"),
    so this is the showroom's 11th-gen Civic hatch (FL) game model, the Type R's base body, in Championship White with a
    Type R style wing, red badge and red seats. It is not the wide-body FL5 shell: fenders and bumpers are the hatch's."""
    root, by, mats = _imp(CIVIC, name); _paint(mats["paint"], color, 0.22)
    for n in ("part_front_lip", "part_rear_lip", "part_side_skirts", "part_sport_wing"): by[n].hide_render = True
    if hide_glass: by["glass"].hide_render = True
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); body = by["body"]; inv = body.matrix_world.inverted()
    dk = W._flat_mat(name + "_dk", (0.012, 0.012, 0.014), 0.25); red = W._flat_mat(name + "_red", (0.75, 0.02, 0.03), 0.4)
    def top(x, y):   # highest surface under a point (body, glass or trim); 1.0 m if nothing is hit
        zs = []
        for ob in (body, by["glass"], by["trim"]):
            iv = ob.matrix_world.inverted(); ok, hit, nrm, _ = ob.ray_cast(iv @ Vector((x, y, 3.0)), iv.to_3x3() @ Vector((0, 0, -1)), depsgraph=dg)
            if ok: zs.append((ob.matrix_world @ hit).z)
        return max(zs) if zs else 1.0
    tops = []
    for sx in (-1, 1):   # wing uprights stand on the hatch, found by a ray from above
        z = top(sx * 0.42, 1.98); print("FL5 wing base z", round(z, 3)); box(f"{name}_wu{sx}", (0.03, 0.2, 0.19), dk, loc=(sx * 0.42, 1.98, z - 0.01), rot=(R(-10), 0, 0), parent=root, base="z"); tops.append(z + 0.18)
    zt = sum(tops) / 2; box(name + "_wing", (1.52, 0.27, 0.03), dk, loc=(0, 2.03, zt), rot=(R(-5), 0, 0), parent=root)
    for sx in (-1, 1): box(f"{name}_we{sx}", (0.025, 0.31, 0.09), dk, loc=(sx * 0.76, 2.03, zt - 0.01), parent=root)
    ok, hit, nrm, _ = body.ray_cast(inv @ Vector((0.0, -4.0, 0.72)), inv.to_3x3() @ Vector((0, 1, 0)), depsgraph=dg)
    if ok:
        hit = body.matrix_world @ hit; nrm = (body.matrix_world.to_3x3() @ nrm).normalized(); b = box(name + "_badge", (0.1, 0.075, 0.006), red, loc=tuple(hit + nrm * 0.004), parent=root); b.rotation_euler = nrm.to_track_quat("Z", "Y").to_euler()
    for sx in (-1, 1): box(f"{name}_seat{sx}", (0.5, 0.14, 0.72), red, loc=(sx * 0.38, 0.32, 0.42), parent=root, base="z")
    return root, by
