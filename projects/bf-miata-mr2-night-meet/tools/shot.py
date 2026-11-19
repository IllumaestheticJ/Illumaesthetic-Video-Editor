"""v0 shot renderer for bf-miata-mr2-night-meet (preview quality).

    blender -b --factory-startup -P shot.py -- spec.json

spec = {
  "out": dir, "frames": N, "fps": 15, "res": [540, 960], "samples": 12,
  "mode": "cgi" | "scan",
  "cars": [ {"car": "mr2"|"nc", "offset": [x, y, z], "yaw": deg} ],
  "camera": [ {"f": 0, "loc": [..], "target": [..], "lens": 35}, ... ]   (linear in f, smoothstep eased),
  "anim": [ {"car": i, "cut": "file.stl", "part": ["file.stl"], "off": [f0, f1], "on": [f2, f3], "dir": [x,y,z]} ],
  "hide_parts_until_on": true
}
Scene frame = lookbook GLB frame: metres, nose -Y, floor z = 0.
CGI: GLB with the sale kit (stock pieces hidden where a kit part is shown), paint set per car, procedural night lot.
SCAN: decimated scan in the GLB frame (house satin silver on black, scan_render.py look); kit parts silver too.
"""
import json
import math
import os
import sys

import bpy
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "blender")); import ive_gpu  # noqa: E402  (GPU when present, else CPU)
from mathutils import Euler, Matrix, Vector

REPO = "/home/user/Illumaesthetic-Video-Editor"
sys.path.insert(0, f"{REPO}/blender")
import scan_render as SR  # noqa: E402  (mat_silver, studio_world)

M = "/home/user/media/bf-miata-mr2-night-meet"
GLB = {"mr2": f"{M}/glb/eps-toyota-mr2-spyder-v19.glb", "nc": f"{M}/glb/eps-mazda-mx5-nc-v19.glb"}
SCAN = {"mr2": f"{M}/dec/mr2_keep.stl", "nc": f"{M}/dec/nc_keep.stl"}
SCAN_FULL = {"mr2": f"{M}/dec/mr2_glbframe.stl", "nc": f"{M}/dec/nc_glbframe.stl"}
PAINT = {"mr2": (0.55, 0.012, 0.018), "nc": (0.38, 0.012, 0.10)}    # linear; MR2 red, NC Rubystar #a61f59
# v1 (user: "start with stock cars and then slowly modify them"): every car starts STOCK; zones install one at a time.
# zone -> (lookbook stock objects that come off, kit parts that go on)
ZONES = {"mr2": {"bumper": (["body_front_bumper_stock", "trim_front_bumper_stock"], ["part_front_bumper"]),   # v1.8 user: "MR2 spyder doesn't show the front bumper"
                 "skirts": (["body_fender_cut_stock", "trim_fender_liner_stock"], ["part_side_skirts"]),
                 "eyelids": (["body_eyelids_stock"], ["part_eyelids"]),
                 "hood": (["body_hood_vent_stock"], ["part_hood_vents"]),
                 # v2.0 user: "the rear bumper should not be getting cut on the MR2 - same with duckbill": see OVER below
                 "spats": (["body_rear_spats_stock"], ["part_rear_spats"]),
                 "duck": (["body_duckbill_stock"], ["part_duckbill"]),
                 "diffuser": ([], ["part_diffuser"]),         # user: include the rear diffuser (black) and the TC wing
                 "wing": (["body_tc_wing_kit_stock"], ["part_tc_wing_kit"])},
         "nc": {"bumper": (["body_front_bumper_scan"], ["part_front_bumper", "part_front_lip", "part_canards"]),
                "fender": (["body_fender_cuts_scan"], ["part_fender_cuts"]),
                "skirts": (["body_side_skirts_stock"], ["part_side_skirts"]),
                "spats": (["body_rear_spats_stock"], ["part_rear_spats"]),   # user: NC rear spats -> the rear bumper is cut
                "wing": ([], ["part_tc_wing"])}}              # engineering NC swan short mount (tools/nc_tcwing.py)
# zones whose part goes OVER the stock body: nothing slides off. The stock patch under the part is only hidden on the frame
# the part seats (it would poke through the part otherwise: user "the rear spats also clip through the body").
OVER = {"mr2": ["spats", "duck"], "nc": []}
# parts that keep their own finish in every shot (MR2 v4 reviewer: black diffuser, carbon wing)
DARK = {"part_diffuser": "black", "part_tc_wing_kit": "carbon", "part_tc_wing": "carbon"}
# never shown (not on sale / not in this ad). v1.8: the MR2 front bumper ("No deal") IS shown now, per the user.
NEVER = {"mr2": ["part_hardtop", "hardtop_rear_window", "trim_soft_top_stock"],
         "nc": ["part_gt_wing", "part_brake_ducts", "part_tire_spats", "trim_front_bumper_off_stock", "body_front_bumper_stock", "body_fender_cuts_stock"]}


def mat_dark(kind):
    m, nt, out = SR.new_mat(f"dark_{kind}")
    p = SR.principled(nt, (0.012, 0.012, 0.013, 1), 0.38 if kind == "black" else 0.22, 0.0)
    if kind == "carbon":
        p.inputs["Coat Weight"].default_value = 1.0; p.inputs["Coat Roughness"].default_value = 0.04
        ch = nt.nodes.new("ShaderNodeTexChecker"); ch.inputs["Scale"].default_value = 900
        ch.inputs["Color1"].default_value = (0.010, 0.010, 0.011, 1); ch.inputs["Color2"].default_value = (0.030, 0.030, 0.033, 1)
        nt.links.new(ch.outputs["Color"], p.inputs["Base Color"])
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


_DM = {}
def dark(kind):
    if kind not in _DM: _DM[kind] = mat_dark(kind)
    return _DM[kind]


def spec():
    return json.load(open(sys.argv[sys.argv.index("--") + 1]))


def import_stl(path, name):
    bpy.ops.wm.stl_import(filepath=path)
    o = bpy.context.selected_objects[0]
    o.name = name
    return o


def parent_to(objs, root):
    for o in objs:
        if o.parent is None:
            o.parent = root


def car_root(i, c):
    r = bpy.data.objects.new(f"car{i}", None)
    bpy.context.scene.collection.objects.link(r)
    r.location = c.get("offset", [0, 0, 0])
    r.rotation_euler = (0, 0, math.radians(c.get("yaw", 0)))
    return r


def mat_paint(rgb):
    m, nt, out = SR.new_mat("paint_v0")
    p = SR.principled(nt, (*rgb, 1), 0.18, 0.35)
    p.inputs["Coat Weight"].default_value = 1.0
    p.inputs["Coat Roughness"].default_value = 0.05
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


def base(n): return n.split(".")[0]


def key_vis(o, f, hidden):
    o.hide_render = hidden; o.keyframe_insert("hide_render", frame=f + 1)


def slide(o, f0, f1, vec, arriving, nframes):
    """arriving: starts at +vec and eases to rest by f1. leaving: rest until f0, then accelerates to +vec."""
    rest = o.location.copy()
    for f in range(0, nframes + 1):
        u = ease((f - f0) / max(1, f1 - f0))
        o.location = rest + Vector(vec) * ((1 - u) if arriving else u ** 1.6)
        o.keyframe_insert("location", frame=f + 1)


def apply_zones(c, objs_of, nframes):
    """objs_of(names) -> objects. c["on"] = zones already installed; c["swap"] = zones that install during the shot."""
    car = c["car"]
    for n in NEVER[car]:
        for o in objs_of([n]): o.hide_render = True
    swaps = {w["zone"]: w for w in c.get("swap", [])}
    for z, (stock, parts) in ZONES[car].items():
        keep = z in OVER[car] and c.get("mode") != "scan"      # CGI: the go-over part sits on the untouched stock body
        if z in c.get("on", []):
            for o in objs_of(stock):
                o.hide_render = not keep
                if keep: set_inset(o)
        elif z in swaps:
            w = swaps[z]; f0, f1 = w["off"]; f2, f3 = w["on"]
            for o in objs_of(stock):
                if z in OVER[car]:
                    key_vis(o, 0, False)
                    if not keep: key_vis(o, f3 - 1, True)
                    else: set_inset(o, f3 - 1)
                    continue
                slide(o, f0, f1, Vector(w.get("dir", [0, 0, 1])) * w.get("dist", 6.0), False, nframes)
                key_vis(o, 0, False); key_vis(o, f1, True)
            for o in objs_of(parts):
                slide(o, f2, f3, w.get("from", [0, 0, 1.5]), True, nframes)
                key_vis(o, 0, True); key_vis(o, f2, False)
        else:
            for o in objs_of(parts): o.hide_render = True


def load_cgi(i, c, nframes):
    root = car_root(i, c)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=GLB[c["car"]])
    new = [o for o in bpy.data.objects if o not in before]
    paint = mat_paint(PAINT[c["car"]])
    if c["car"] == "nc":      # the lookbook NC has no stock nose: use the real stock bumper from our scan, painted
        for zn, nm in (("bumper", "body_front_bumper_scan"), ("fender", "body_fender_cuts_scan")):   # GLB fender stock renders black
            o = import_stl(f"{M}/dec/nc_cut_{zn}.stl", nm); o.data.materials.append(paint)
            for pl in o.data.polygons: pl.use_smooth = True
            new.append(o)
        o = import_stl(f"{M}/kit_nc/part_tc_wing.stl", "part_tc_wing"); new.append(o)
    for o in new:
        if o.type == "MESH":
            if base(o.name) in DARK:
                o.data.materials.clear(); o.data.materials.append(dark(DARK[base(o.name)])); continue
            for sl in o.material_slots:
                if sl.material and sl.material.name.startswith("paint"):
                    sl.material = paint
    # v2.2 (user: all game models): what the bumper hides comes from the bumper-off scans, in dark metal behind the nose
    up = f"{M}/dec/{c['car']}_under_bumper.stl"
    if os.path.exists(up):
        o = import_stl(up, "under_bumper"); o.data.materials.append(dark("black")); new.append(o)
    for z in OVER[c["car"]]:
        inset_under([o for o in new if base(o.name) in ZONES[c["car"]][z][0]], [o for o in new if base(o.name) in ZONES[c["car"]][z][1]])
    parent_to(new, root)
    apply_zones(c, lambda names: [o for o in new if base(o.name) in names], nframes)
    return root


INSET = -0.010
def inset_under(stocks, parts):
    """user 2026-11-19: "the rear spats still clip through the bumper". The go-over part sits on the untouched stock body, but
    their surfaces coincide in patches (blotchy poke-through). Stock vertices within 12 mm of the part surface (in front or behind) get a vertex group; a Displace
    modifier tucks them 10 mm inward once the part is seated (strength keyed in apply_zones). Uncovered stock is untouched."""
    from mathutils.bvhtree import BVHTree
    V, P = [], []
    for q in parts:
        mw = q.matrix_world; n0 = len(V); V += [mw @ v.co for v in q.data.vertices]; P += [[n0 + i for i in pl.vertices] for pl in q.data.polygons]
    if not P: return
    bvh = BVHTree.FromPolygons(V, P)
    for b in stocks:
        mw = b.matrix_world; nm = mw.to_3x3().inverted().transposed(); g = b.vertex_groups.new(name="cov"); k = 0
        for v in b.data.vertices:
            cc = mw @ v.co; n = (nm @ v.normal).normalized()
            if bvh.ray_cast(cc + n * 1e-4, n, 0.012)[0] is not None or bvh.ray_cast(cc + n * 1e-4, -n, 0.012)[0] is not None:
                g.add([v.index], 1.0, "REPLACE"); k += 1
        m = b.modifiers.new("inset", "DISPLACE"); m.vertex_group = "cov"; m.mid_level = 0.0; m.strength = 0.0; m.direction = "NORMAL"
        print("inset_under", b.name, k, "of", len(b.data.vertices), "verts covered")


def set_inset(o, f=None):
    m = o.modifiers.get("inset")
    if m is None: return
    if f is None: m.strength = INSET; return
    m.strength = 0.0; m.keyframe_insert("strength", frame=f); m.strength = INSET; m.keyframe_insert("strength", frame=f + 1)


def load_scan(i, c, silver, nframes):
    root = car_root(i, c); car = c["car"]; K = f"{M}/kit_{car}"
    b0 = import_stl(SCAN[car], f"scan{i}"); b0.data.materials.append(silver); b0.parent = root
    objs = {}
    for z, (stock, parts) in ZONES[car].items():
        cp = f"{M}/dec/{car}_cut_{z}.stl"
        if not os.path.exists(cp): continue_stock = False
        else:
            o = import_stl(cp, f"cut_{z}"); o.data.materials.append(silver); o.parent = root
            for n in stock: objs.setdefault(n, []).append(o)
        for n in parts:
            q = import_stl(f"{K}/{n}.stl", n); q.data.materials.append(dark(DARK[n]) if n in DARK else silver); q.parent = root; objs.setdefault(n, []).append(q)
    seen = set()
    def objs_of(names):
        out = []
        for n in names:
            for o in objs.get(n, []):
                if o.name not in seen or True: out.append(o)
        return list({o.name: o for o in out}.values())
    apply_zones(c, objs_of, nframes)
    return root


def lot_env():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("night"); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes["Background"]; bg.inputs["Color"].default_value = (0.004, 0.006, 0.012, 1); bg.inputs["Strength"].default_value = 1
    # wet asphalt
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0))
    g = bpy.context.object; g.name = "asphalt"
    m, nt, out = SR.new_mat("asphalt")
    p = SR.principled(nt, (0.018, 0.018, 0.02, 1), 0.22, 0.0)
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 3.0
    ramp = nt.nodes.new("ShaderNodeMapRange"); ramp.inputs["To Min"].default_value = 0.08; ramp.inputs["To Max"].default_value = 0.55
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Value"]); nt.links.new(ramp.outputs["Result"], p.inputs["Roughness"])
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.08
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 140
    nt.links.new(n2.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], p.inputs["Normal"])
    nt.links.new(p.outputs[0], out.inputs[0]); g.data.materials.append(m)
    # parking lines
    lm, lnt, lout = SR.new_mat("paintline"); lp = SR.principled(lnt, (0.55, 0.52, 0.42, 1), 0.5); lnt.links.new(lp.outputs[0], lout.inputs[0])
    for x in (-3.9, -1.3, 1.3, 3.9):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, 0.4, 0.002)); o = bpy.context.object
        o.scale = (0.06, 2.6, 1); o.data.materials.append(lm)
    # sodium lamps: spot + visible emissive head on a dark pole
    em, ent, eout = SR.new_mat("lamphead"); e = SR.emission(ent, (1.0, 0.55, 0.22, 1), 40); ent.links.new(e.outputs[0], eout.inputs[0])
    pm, pnt, pout = SR.new_mat("pole"); pp = SR.principled(pnt, (0.02, 0.02, 0.02, 1), 0.5, 0.6); pnt.links.new(pp.outputs[0], pout.inputs[0])
    for (x, y) in ((-3.2, -3.4), (3.4, 3.0), (-4.5, 9.0), (6.0, -9.5), (-9.0, -1.0)):
        d = bpy.data.lights.new("sodium", "SPOT"); d.energy = 9000; d.color = (1.0, 0.58, 0.25); d.spot_size = math.radians(95)
        d.spot_blend = 0.6; d.shadow_soft_size = 0.4
        o = bpy.data.objects.new("sodium", d); bpy.context.scene.collection.objects.link(o); o.location = (x, y, 6.5)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=6.5, location=(x, y, 3.25)); bpy.context.object.data.materials.append(pm)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 6.55)); h = bpy.context.object; h.scale = (0.5, 0.25, 0.08); h.data.materials.append(em)
    # cool fill + a distant cyan neon strip and dim building windows for depth
    d = bpy.data.lights.new("fill", "AREA"); d.energy = 600; d.size = 10; d.color = (0.45, 0.6, 1.0)
    o = bpy.data.objects.new("fill", d); bpy.context.scene.collection.objects.link(o); o.location = (0, 0, 12)
    nm, nnt, nout = SR.new_mat("neon"); ne = SR.emission(nnt, (0.25, 0.9, 1.0, 1), 25); nnt.links.new(ne.outputs[0], nout.inputs[0])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 22, 4)); s = bpy.context.object; s.scale = (14, 0.1, 0.12); s.data.materials.append(nm)
    wm, wnt, wout = SR.new_mat("windows"); we = SR.emission(wnt, (1.0, 0.75, 0.45, 1), 0.6); wnt.links.new(we.outputs[0], wout.inputs[0])
    bm, bnt, bout = SR.new_mat("bldg"); bb = SR.principled(bnt, (0.01, 0.01, 0.012, 1), 0.8); bnt.links.new(bb.outputs[0], bout.inputs[0])
    import random
    random.seed(4)
    for side, yy in ((1, 26), (-1, -26)):
        for k in range(9):
            x = -30 + k * 7.5; hgt = random.uniform(8, 20)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, yy, hgt / 2)); b = bpy.context.object; b.scale = (6, 4, hgt); b.data.materials.append(bm)
            for r in range(int(hgt // 2.2)):
                if random.random() < 0.45:
                    bpy.ops.mesh.primitive_plane_add(size=1, location=(x + random.uniform(-2, 2), yy - side * 2.02, 1.2 + r * 2.2),
                                                     rotation=(math.pi / 2, 0, 0))
                    wi = bpy.context.object; wi.scale = (0.7, 0.5, 1); wi.data.materials.append(wm)
    # light rain haze
    vm, vnt, vout = SR.new_mat("haze"); vs = vnt.nodes.new("ShaderNodeVolumeScatter"); vs.inputs["Density"].default_value = 0.012
    vnt.links.new(vs.outputs[0], vout.inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 8)); hz = bpy.context.object; hz.scale = (70, 70, 16); hz.data.materials.append(vm)


def camera(keys):
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    bpy.context.scene.collection.objects.link(cam); bpy.context.scene.camera = cam
    cam.data.sensor_width = 36
    for k in keys:
        loc, tgt = Vector(k["loc"]), Vector(k["target"])
        cam.location = loc
        cam.rotation_euler = (tgt - loc).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = k.get("lens", 35)
        cam.keyframe_insert("location", frame=k["f"] + 1); cam.keyframe_insert("rotation_euler", frame=k["f"] + 1)
        cam.data.keyframe_insert("lens", frame=k["f"] + 1)
    return cam


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def main():
    sp = spec()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; ive_gpu.use(sc); sc.cycles.samples = sp.get("samples", 12)
    sc.cycles.use_denoising = True; sc.render.use_persistent_data = False
    sc.render.resolution_x, sc.render.resolution_y = sp.get("res", [540, 960]); sc.render.resolution_percentage = 100
    sc.frame_start, sc.frame_end = 1, sp["frames"]
    sc.render.fps = sp.get("fps", 15)
    sc.view_settings.view_transform = "AgX"
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.join(sp["out"], "f_")
    silver = SR.mat_silver()
    roots = []
    for i, c in enumerate(sp["cars"]):
        roots.append(load_cgi(i, c, sp["frames"]) if sp["mode"] == "cgi" else load_scan(i, dict(c, mode="scan"), silver, sp["frames"]))
    if sp["mode"] == "cgi":
        lot_env()
        sc.view_settings.look = "AgX - Medium High Contrast"
        sc.view_settings.exposure = sp.get("exposure", 0.0)
    else:
        SR.studio_world((0.004, 0.004, 0.004, 1), False)
        for name, loc, en, size, col in (("key", (3.5, -4.5, 4.5), 900, 4, (1, 1, 1)), ("rim", (-3.5, 4.5, 3.0), 1100, 2.5, (0.85, 0.92, 1)),
                                          ("top", (0, 0, 6), 700, 6, (1, 1, 1))):
            d = bpy.data.lights.new(name, "AREA"); d.energy = en; d.size = size; d.color = col
            o = bpy.data.objects.new(name, d); sc.collection.objects.link(o); o.location = loc
            o.rotation_euler = (Vector((0, 0, 0.5)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    camera(sp["camera"])
    frames = sp.get("only")
    if frames:
        for f in frames:
            sc.frame_set(f + 1); sc.render.filepath = os.path.join(sp["out"], f"f_{f + 1:04d}"); bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)
    print("SHOT_DONE", sp["out"])


main()
