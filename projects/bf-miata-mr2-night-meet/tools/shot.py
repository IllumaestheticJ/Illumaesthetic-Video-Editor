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
from mathutils import Euler, Matrix, Vector

REPO = "/home/user/Illumaesthetic-Video-Editor"
sys.path.insert(0, f"{REPO}/blender")
import scan_render as SR  # noqa: E402  (mat_silver, studio_world)

M = "/home/user/media/bf-miata-mr2-night-meet"
GLB = {"mr2": f"{M}/glb/eps-toyota-mr2-spyder-v19.glb", "nc": f"{M}/glb/eps-mazda-mx5-nc-v19.glb"}
SCAN = {"mr2": f"{M}/dec/mr2_keep.stl", "nc": f"{M}/dec/nc_keep.stl"}
SCAN_FULL = {"mr2": f"{M}/dec/mr2_glbframe.stl", "nc": f"{M}/dec/nc_glbframe.stl"}
PAINT = {"mr2": (0.55, 0.012, 0.018), "nc": (0.38, 0.012, 0.10)}    # linear; MR2 red, NC Rubystar #a61f59
# sale kit per car (owner's BF sheet + plan): parts shown; matching stock pieces hidden
SHOW = {"mr2": ["part_front_bumper", "part_eyelids", "part_hood_vents", "part_side_skirts", "part_rear_spats", "part_duckbill"],
        "nc": ["part_front_bumper", "part_front_lip", "part_fender_cuts", "part_side_skirts", "part_rear_spats", "part_canards"]}
HIDE = {"mr2": ["body_front_bumper_stock", "trim_front_bumper_stock", "body_eyelids_stock", "body_hood_vent_stock",
                "body_fender_cut_stock", "trim_fender_liner_stock", "body_rear_spats_stock", "body_duckbill_stock",
                "part_diffuser", "part_tc_wing_kit", "body_tc_wing_kit_stock", "part_hardtop", "hardtop_rear_window"],
        "nc": ["body_front_bumper_stock", "trim_front_bumper_off_stock", "body_fender_cuts_stock", "body_side_skirts_stock",
               "body_rear_spats_stock", "part_gt_wing", "part_brake_ducts", "part_tire_spats", "body_tire_spats_stock"]}


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


def load_cgi(i, c):
    root = car_root(i, c)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=GLB[c["car"]])
    new = [o for o in bpy.data.objects if o not in before]
    paint = mat_paint(PAINT[c["car"]])
    for o in new:
        if o.name.split(".")[0] in HIDE[c["car"]]:
            o.hide_render = True
        if o.type == "MESH":
            for s in o.material_slots:
                if s.material and s.material.name.startswith("paint"):
                    s.material = paint
    parent_to(new, root)
    return root


def load_scan(i, c, silver, anim):
    root = car_root(i, c)
    base = import_stl(SCAN[c["car"]] if c.get("keep", True) else SCAN_FULL[c["car"]], f"scan{i}")
    base.data.materials.append(silver)
    base.parent = root
    for k, pth in enumerate(c.get("static", [])):
        o = import_stl(pth, f"static{i}_{k}"); o.data.materials.append(silver); o.parent = root
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


def animate(sp, roots, silver):
    for a in sp.get("anim", []):
        root = roots[a.get("car", 0)]
        d = Vector(a.get("dir", [0, 0, 1]))
        if a.get("cut"):
            o = import_stl(a["cut"], "cut"); o.data.materials.append(silver); o.parent = root
            f0, f1 = a["off"]
            for f in range(f0, f1 + 1):
                o.location = d * (ease((f - f0) / max(1, f1 - f0)) ** 1.6) * a.get("dist", 6.0)
                o.keyframe_insert("location", frame=f + 1)
        for pth in a.get("part", []):
            o = import_stl(pth, "part"); o.data.materials.append(silver); o.parent = root
            f2, f3 = a["on"]
            for f in range(min(f2, sp["frames"]), sp["frames"] + 1):
                u = 1 - ease((f - f2) / max(1, f3 - f2))
                o.location = Vector(a.get("from", [0, 0, 1.6])) * u
                o.keyframe_insert("location", frame=f + 1)
            o.hide_render = True; o.keyframe_insert("hide_render", frame=1)
            o.hide_render = False; o.keyframe_insert("hide_render", frame=f2 + 1)


def main():
    sp = spec()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = sp.get("samples", 12)
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
        roots.append(load_cgi(i, c) if sp["mode"] == "cgi" else load_scan(i, c, silver, sp.get("anim", [])))
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
        animate(sp, roots, silver)
    camera(sp["camera"])
    frames = sp.get("only")
    if frames:
        for f in frames:
            sc.frame_set(f + 1); sc.render.filepath = os.path.join(sp["out"], f"f_{f + 1:04d}"); bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)
    print("SHOT_DONE", sp["out"])


main()
