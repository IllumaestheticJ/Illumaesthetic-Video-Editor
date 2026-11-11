"""Project copy of blender/kit_render.py for the NFSU1 car-select reel, with three additions:
  --steer DEG        turn the front wheels (wheel_FL / wheel_FR about their own vertical axis), as the game does
  --frs-green BLEND  open Ron's `GT2 Animation FRS-green.blend` (Drive 1q8-BnHUn-hvb6Tzi1Cy_OsfSdG_QCBVv, the green
                     race-livery FR-S) instead of a GLB: floor, lights, cameras and two stray glass sheets are dropped,
                     the car is scaled to the ZN6's real length and put in the showroom frame. Its own materials stay.
  --cam-anim JSON    a list of cameras (ive schema), one per output frame: renders a sequence along a solved camera path

Original docstring: Render an Epsilon showroom car GLB (Epsilon-Site `showroom/models/eps-*.glb`) with its kit fitted.

    blender -b -P blender/kit_render.py -- --glb eps-acura-integra-de-v8.glb \
        --hide part_fender_flares --paint "#848586" --az 35 --el 8 --out work/integra.png

The GLBs are already in one frame: metres, Z up, nose at -Y, tyres on z = 0, one node per body
zone / kit part (`part_*`), materials named by role (`paint`, `glass_tint`, `rim_dark`, ...). This
script never edits geometry: it only hides nodes, re-shades the named materials for Cycles and
places a camera, so "the GLB as it is on the site" is what ends up on screen.

Kit state comes from `python -m ive kit <car-id>` (reads the showroom manifests: which stock
nodes a part replaces, which parts share a slot). Pass its `hide` list to --hide.

Camera: --camera cam.json (schema of `ive solve` / `ive lookat`, e.g. a camera matched to a
plate) or --az/--el/--dist/--focal around the car. Azimuth 0 = dead front, 90 = car's left side.
Motion: --spin (car turntable, degrees over the shot) and/or --orbit (camera, degrees).
Output is RGBA on a transparent film; --ground shadow adds a shadow catcher at z = 0,
--ground gloss a dark glossy floor (showroom reflection), --ground none nothing.
"""
import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector


def argv():
    a = sys.argv
    return a[a.index("--") + 1:] if "--" in a else a[1:]


def parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", default="")
    ap.add_argument("--frs-green", default="")
    ap.add_argument("--livery", default="", help="material name of a livery carrier node (livery_castrol, livery_ak4some): its image goes on the paint, through the body's own UVs, as the showroom does")
    ap.add_argument("--tail-glow", type=float, default=0.0, help="emission strength for tail-lamp materials (the game's cars sit with their lights on)")
    ap.add_argument("--steer", type=float, default=0.0, help="front wheel steer angle, degrees (+ = wheels point to the car's left)")
    ap.add_argument("--cam-anim", default="", help="JSON list of cameras, one per frame")
    ap.add_argument("--frames", default="", help="with --cam-anim: 'a-b' subset of frame indices (0-based, inclusive)")
    ap.add_argument("--out", required=True, help=".png for a still, or a directory for a PNG sequence")
    ap.add_argument("--hide", default="", help="comma-separated node names to hide (with their children)")
    ap.add_argument("--paint", default="", help="body colour, sRGB hex (default: the GLB's own paint colour)")
    ap.add_argument("--part-paint", default="", help="kit part colour, sRGB hex or 'raw' (satin black); default: body colour")
    ap.add_argument("--finish", default="gloss", choices=["gloss", "metallic", "pearl", "matte"])
    ap.add_argument("--camera", help="camera JSON (ive schema)")
    ap.add_argument("--az", type=float, default=35.0)
    ap.add_argument("--el", type=float, default=8.0)
    ap.add_argument("--dist", type=float, default=0.0, help="metres from the car centre; 0 = fit the car in frame")
    ap.add_argument("--fit", type=float, default=0.82, help="fraction of the frame the car fills when --dist is 0")
    ap.add_argument("--focal", type=float, default=50.0)
    ap.add_argument("--sensor", type=float, default=36.0)
    ap.add_argument("--target-z", type=float, default=-1.0, help="look-at height; default = 45 %% of car height")
    ap.add_argument("--res", default="1920x1080")
    ap.add_argument("--res-pct", type=int, default=100)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--seconds", type=float, default=0, help="0 = single still")
    ap.add_argument("--spin", type=float, default=0, help="car turntable, degrees over the shot (about Z)")
    ap.add_argument("--spin-start", type=float, default=0, help="car heading at frame 1, degrees about Z")
    ap.add_argument("--orbit", type=float, default=0, help="camera orbit, degrees over the shot")
    ap.add_argument("--ease", default="linear", choices=["linear", "ease_in_out"])
    ap.add_argument("--rig", default="carlot", choices=["carlot", "studio"])
    ap.add_argument("--rig-json", help="override light rig: {world:[r,g,b,strength], lights:[{loc,rot,size,energy,color,glossy_only,only_nodes}], materials:{name:{principled inputs}}}")
    ap.add_argument("--exposure", type=float, default=0.0)
    ap.add_argument("--view", default="Standard", help="view transform: Standard (game-like) | AgX | Filmic")
    ap.add_argument("--ground", default="shadow", choices=["shadow", "gloss", "none"])
    ap.add_argument("--bg", default="transparent", help="'transparent' or r,g,b (linear)")
    ap.add_argument("--samples", type=int, default=48)
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--save-blend")
    return ap.parse_args(argv())


def srgb_hex(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v / 12.92) if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (1.0,)


def bsdf(mat):
    if not mat or not mat.use_nodes:
        return None
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            return n
    return None


def setp(b, **kw):
    """Set Principled inputs by name, skipping the ones this Blender build does not have."""
    for k, v in kw.items():
        name = k.replace("_", " ").title().replace("Ior", "IOR")
        if name in b.inputs:
            b.inputs[name].default_value = v


# role -> shading. Colours stay the GLB's own unless given here.
LOOK = {
    "plastic_black": dict(roughness=0.55),
    "plastic_gloss": dict(roughness=0.12, coat_weight=0.6, coat_roughness=0.05),
    "grille": dict(roughness=0.6),
    "underbody": dict(roughness=0.9),
    "interior": dict(roughness=0.8),
    "rubber": dict(roughness=0.82),
    "chrome": dict(metallic=1.0, roughness=0.07),
    "mirror_glass": dict(metallic=1.0, roughness=0.02),
    "rim": dict(metallic=1.0, roughness=0.22),
    "rim_dark": dict(metallic=0.9, roughness=0.3),
    "brake": dict(metallic=1.0, roughness=0.4),
    "caliper": dict(roughness=0.35, coat_weight=0.5),
    "carbon": dict(roughness=0.35, coat_weight=1.0, coat_roughness=0.05),
    "glass": dict(roughness=0.02),
    "glass_tint": dict(roughness=0.02),
    "light_lens": dict(roughness=0.03),
    "light_inner": dict(metallic=1.0, roughness=0.12),
    "light_drl": dict(roughness=0.2),
    "light_amber": dict(roughness=0.1),
    "light_red": dict(roughness=0.1),
}
PAINT = {
    "gloss": dict(metallic=0.0, roughness=0.32, coat_weight=1.0, coat_roughness=0.04),
    "metallic": dict(metallic=0.75, roughness=0.36, coat_weight=1.0, coat_roughness=0.04),
    "pearl": dict(metallic=0.35, roughness=0.3, coat_weight=1.0, coat_roughness=0.03),
    "matte": dict(metallic=0.0, roughness=0.7, coat_weight=0.0),
}


def lookdev(a):
    paint = bpy.data.materials.get("paint")
    if paint and bsdf(paint):
        b = bsdf(paint)
        if a.paint:
            b.inputs["Base Color"].default_value = srgb_hex(a.paint)
        setp(b, **PAINT[a.finish])
    for name, kw in LOOK.items():
        m = bpy.data.materials.get(name)
        if m and bsdf(m):
            setp(bsdf(m), **kw)
    # kit parts in their own colour: give part_* nodes a copy of the paint material
    if a.part_paint and paint:
        pm = paint.copy()
        pm.name = "paint_parts"
        b = bsdf(pm)
        if a.part_paint == "raw":
            b.inputs["Base Color"].default_value = (0.012, 0.012, 0.013, 1)
            setp(b, metallic=0.0, roughness=0.42, coat_weight=0.0)
        else:
            b.inputs["Base Color"].default_value = srgb_hex(a.part_paint)
        for o in bpy.data.objects:
            top = o
            while top.parent:
                top = top.parent
            if o.type == "MESH" and top.name.startswith("part_"):
                for s in o.material_slots:
                    if s.material == paint:
                        s.material = pm


def prep_frs_green(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    for o in list(bpy.data.objects):
        if o.type in ("LIGHT", "CAMERA") or o.name.startswith("Plane.001") or o.name.startswith("113_T"):
            bpy.data.objects.remove(o, do_unlink=True)
    for o in bpy.data.objects:
        o.animation_data_clear()
    bpy.context.view_layer.update()
    import numpy as np
    def vb(o):
        a = np.empty(len(o.data.vertices) * 3, "f"); o.data.vertices.foreach_get("co", a)
        M = np.array(o.matrix_world); w = a.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
        return w.min(0), w.max(0)
    wheels = [o for o in bpy.data.objects if o.name.startswith("BKP037")]
    wb = [vb(o) for o in wheels]
    zmin = min(b[0][2] for b in wb)
    cx = sum((b[0][0] + b[1][0]) / 2 for b in wb) / 4
    blo, bhi = vb(bpy.data.objects["FRS_Exterior_body"]); flo, fhi = vb(bpy.data.objects["bumper"])
    y0, y1 = min(blo[1], flo[1]), bhi[1]
    s = 4.234 / (y1 - y0)                                    # ZN6 length, showroom manifest-frs.json lengthM
    T = Matrix.Scale(s, 4) @ Matrix.Translation((-cx, -(y0 + y1) / 2, -zmin))
    for o in [o for o in bpy.data.objects if o.parent is None]:
        o.matrix_world = T @ o.matrix_world
    bpy.context.view_layer.update()
    for o in wheels:
        bpy.context.view_layer.objects.active = o
        for x in bpy.data.objects:
            x.select_set(x is o)
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    bpy.context.view_layer.update()
    for o in wheels:
        p = o.matrix_world.translation
        o.name = "wheel_" + ("F" if p.y < 0 else "R") + ("L" if p.x > 0 else "R")
        print("IVE_WHEEL", o.name, [round(v, 3) for v in p])
    for o in bpy.data.objects:                                # brake discs follow their wheel when it steers
        if o.name.startswith("Cylinder"):
            p = o.matrix_world.translation
            w = min(wheels, key=lambda w: (w.matrix_world.translation - p).length)
            mw = o.matrix_world.copy(); o.parent = w; o.matrix_world = mw
    sc = bpy.context.scene
    sc.render.use_compositing = False
    sc.render.use_sequencer = False
    sc.render.use_border = False
    sc.render.use_simplify = False
    sc.render.pixel_aspect_x = sc.render.pixel_aspect_y = 1
    sc.cycles.pixel_filter_type = "BLACKMAN_HARRIS"
    sc.frame_set(1)
    print(f"IVE_FRS scale={s:.4f}")


def apply_livery(name):
    src = bpy.data.materials.get(name)
    paint = bpy.data.materials.get("paint")
    img = next((n.image for n in src.node_tree.nodes if n.type == "TEX_IMAGE"), None) if src else None
    if not (img and paint):
        print("IVE_WARN livery: not found " + name)
        return
    nt = paint.node_tree
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = img
    nt.links.new(t.outputs["Color"], bsdf(paint).inputs["Base Color"])
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True


def tail_glow(strength):
    if strength <= 0:
        return
    for m in bpy.data.materials:
        n = m.name.lower()
        if not (n.startswith("light_red") or n.startswith("lampphoto_tail") or n.startswith("lampphoto_hmsl") or "tl_red" in n or n.startswith("red_glass")):
            continue
        b = bsdf(m)
        if not b:
            continue
        src = b.inputs["Base Color"]
        e = b.inputs.get("Emission Color") or b.inputs.get("Emission")
        if src.is_linked:
            m.node_tree.links.new(src.links[0].from_socket, e)
        else:
            c = list(src.default_value)
            e.default_value = (max(c[0], 0.6), c[1] * 0.3, c[2] * 0.3, 1)
        b.inputs["Emission Strength"].default_value = strength


_STEER_BASE = {}


def steer(deg):
    for n in ("wheel_FL", "wheel_FR"):
        o = bpy.data.objects.get(n)
        if o and n in _STEER_BASE:
            o.matrix_world = _STEER_BASE[n]
        elif o:
            _STEER_BASE[n] = o.matrix_world.copy()
    bpy.context.view_layer.update()
    if not deg:
        return
    for n in ("wheel_FL", "wheel_FR"):
        o = bpy.data.objects.get(n)
        if not o:
            print("IVE_WARN steer: no node " + n)
            continue
        mw = o.matrix_world.copy()
        c = mw.translation.copy()
        if o.type == "MESH" or o.children:
            pts = [x.matrix_world @ Vector(b) for x in [o] + list(o.children_recursive) if x.type == "MESH" for b in x.bound_box]
            if pts:
                c = sum(pts, Vector()) / len(pts)
        R = Matrix.Translation(c) @ Matrix.Rotation(math.radians(deg), 4, "Z") @ Matrix.Translation(-c)
        o.matrix_world = R @ mw
    bpy.context.view_layer.update()


def hide_nodes(names):
    missing = []
    for n in names:
        o = bpy.data.objects.get(n)
        if not o:
            missing.append(n)
            continue
        for x in [o] + list(o.children_recursive):
            x.hide_render = True
            x.hide_viewport = True
    return missing


def visible_meshes():
    return [o for o in bpy.data.objects if o.type == "MESH" and not o.hide_render]


def bbox(objs):
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in objs:
        for c in o.bound_box:
            v = o.matrix_world @ Vector(c)
            for i in range(3):
                lo[i], hi[i] = min(lo[i], v[i]), max(hi[i], v[i])
    return lo, hi


def area(name, loc, rot_deg, size, energy, color=(1, 1, 1), glossy_only=False):
    d = bpy.data.lights.new(name, "AREA")
    d.shape = "RECTANGLE"
    d.size, d.size_y = size
    d.energy = energy
    d.color = color
    o = bpy.data.objects.new(name, d)
    o.location = loc
    o.rotation_euler = [math.radians(v) for v in rot_deg]
    bpy.context.scene.collection.objects.link(o)
    if glossy_only:            # a panel that only shows up in reflections (a game-style environment map)
        o.visible_diffuse = False
        o.visible_volume_scatter = False
    return o


RIGS = {
    # night car lot: cool overhead canopy strips (long reflections down the body sides), a warm
    # sodium kicker from behind, almost-black sky
    "carlot": {
        "world": [0.010, 0.012, 0.020, 1.0],
        "lights": [
            {"loc": [0, 0, 5.0], "rot": [0, 0, 0], "size": [1.2, 7.0], "energy": 320, "color": [0.92, 0.96, 1.0]},
            {"loc": [-3.2, -0.5, 4.2], "rot": [0, -38, 0], "size": [0.6, 7.0], "energy": 170, "color": [0.9, 0.95, 1.0]},
            {"loc": [3.2, -0.5, 4.2], "rot": [0, 38, 0], "size": [0.6, 7.0], "energy": 170, "color": [0.9, 0.95, 1.0]},
            {"loc": [0, -6.5, 2.2], "rot": [72, 0, 0], "size": [5.0, 1.2], "energy": 110, "color": [1.0, 0.97, 0.92]},
            {"loc": [2.5, 6.5, 2.6], "rot": [-70, 0, 0], "size": [4.0, 1.0], "energy": 120, "color": [1.0, 0.72, 0.42]},
        ],
    },
    "studio": {
        "world": [0.05, 0.05, 0.055, 1.0],
        "lights": [
            {"loc": [0, 0, 5.5], "rot": [0, 0, 0], "size": [5.0, 8.0], "energy": 420, "color": [1, 1, 1]},
            {"loc": [-5, -3, 2.5], "rot": [70, 0, -60], "size": [4.0, 2.0], "energy": 130, "color": [1, 1, 1]},
            {"loc": [5, 3, 2.5], "rot": [70, 0, 120], "size": [4.0, 2.0], "energy": 90, "color": [1, 1, 1]},
        ],
    },
}


def build_rig(a):
    rig = json.load(open(a.rig_json)) if a.rig_json else RIGS[a.rig]
    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = tuple(rig["world"][:3]) + (1,)
    bg.inputs[1].default_value = rig["world"][3]
    bpy.context.scene.world = w
    for i, l in enumerate(rig["lights"]):
        lo = area(f"L{i}", l["loc"], l["rot"], l["size"], l["energy"], l.get("color", (1, 1, 1)), l.get("glossy_only", False))
        if l.get("only_nodes"):          # light linking: this light reaches only the named GLB nodes (e.g. ["glass"])
            coll = bpy.data.collections.new(f"recv_L{i}")
            for n in l["only_nodes"]:
                o = bpy.data.objects.get(n)
                for x in ([o] + list(o.children_recursive)) if o else []:
                    coll.objects.link(x)
            lo.light_linking.receiver_collection = coll
    # a rig can also restyle materials to sit in a plate, e.g. {"materials": {"glass_tint": {"metallic": 0.8}}}
    for name, kw in rig.get("materials", {}).items():
        for m in bpy.data.materials:
            if m.name == name or m.name.startswith(name + "."):
                b = bsdf(m)
                if b:
                    setp(b, **kw)


def build_ground(a, lo, hi):
    if a.ground == "none":
        return
    bpy.ops.mesh.primitive_plane_add(size=60, location=((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, 0))
    g = bpy.context.active_object
    g.name = "ground"
    m = bpy.data.materials.new("ground")
    m.use_nodes = True
    b = bsdf(m)
    if a.ground == "shadow":
        g.is_shadow_catcher = True
        b.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)
        setp(b, roughness=0.6)
    else:
        b.inputs["Base Color"].default_value = (0.02, 0.02, 0.022, 1)
        setp(b, roughness=0.12)
    g.data.materials.append(m)


def cam_from_json(path, cam_obj):
    c = json.load(open(path))
    cam = cam_obj.data
    cam.sensor_fit = "HORIZONTAL"
    cam.sensor_width = c.get("sensor_width_mm", 36.0)
    cam.lens = c["focal_mm"]
    cam.shift_x, cam.shift_y = c.get("shift_x", 0.0), c.get("shift_y", 0.0)
    R = Matrix(c["blender"]["rotation_matrix"]).to_4x4()
    cam_obj.matrix_world = Matrix.Translation(c["blender"]["location"]) @ R
    return c.get("image_size")


def cam_orbit(a, cam_obj, lo, hi, aspect):
    cam = cam_obj.data
    cam.sensor_fit = "HORIZONTAL"
    cam.sensor_width, cam.lens = a.sensor, a.focal
    ctr = (lo + hi) / 2
    tz = a.target_z if a.target_z >= 0 else lo.z + (hi.z - lo.z) * 0.45
    target = Vector((ctr.x, ctr.y, tz))
    az, el = math.radians(a.az), math.radians(a.el)
    # az 0 looks at the nose (camera on -Y), az 90 = camera on +X (car's left side)
    d = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    dist = a.dist
    if dist <= 0:
        # fit the 8 bbox corners: project on the camera's right/up axes, need half-fov to cover them
        fwd = -d
        right = fwd.cross(Vector((0, 0, 1))).normalized()
        up = right.cross(fwd)
        hx = math.atan(a.sensor / 2 / a.focal)
        hy = math.atan(a.sensor / aspect / 2 / a.focal)
        dist = 1.0
        for cx in (lo.x, hi.x):
            for cy in (lo.y, hi.y):
                for cz in (lo.z, hi.z):
                    v = Vector((cx, cy, cz)) - target
                    depth_off = v.dot(fwd)
                    dist = max(dist, abs(v.dot(right)) / (math.tan(hx) * a.fit) - depth_off,
                               abs(v.dot(up)) / (math.tan(hy) * a.fit) - depth_off)
    cam_obj.location = target + d * dist
    q = (target - cam_obj.location).to_track_quat("-Z", "Y")
    cam_obj.rotation_euler = q.to_euler()
    return target, dist


def ease(t, kind):
    return t if kind == "linear" else t * t * (3 - 2 * t)


def main():
    a = parse()
    if a.frs_green:
        prep_frs_green(a.frs_green)
        sc = bpy.context.scene
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        bpy.ops.import_scene.gltf(filepath=a.glb)
    missing = hide_nodes([n for n in a.hide.split(",") if n])
    if missing:
        print("IVE_WARN hide: no such node(s): " + ",".join(missing))
    lookdev(a)
    if a.livery:
        apply_livery(a.livery)
    tail_glow(a.tail_glow)
    steer(a.steer)

    # turntable pivot: everything imported hangs off one empty at the car's footprint centre
    lo, hi = bbox([o for o in visible_meshes() if not a.frs_green or o.name in ("FRS_Exterior_body", "bumper", "Wing", "wheel_FL", "wheel_RR")])
    pivot = bpy.data.objects.new("car_pivot", None)
    pivot.location = ((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, 0)
    sc.collection.objects.link(pivot)
    bpy.context.view_layer.update()
    for o in [o for o in bpy.data.objects if o.parent is None and o is not pivot]:
        mw = o.matrix_world.copy()
        o.parent = pivot
        o.matrix_world = mw

    build_rig(a)
    build_ground(a, lo, hi)

    w, h = (int(v) for v in a.res.split("x"))
    cd = bpy.data.cameras.new("cam")
    co = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(co)
    sc.camera = co
    cd.clip_start, cd.clip_end = 0.05, 500
    target = None
    if a.camera:
        size = cam_from_json(a.camera, co)
        if size and a.res == "1920x1080":
            w, h = size
    else:
        target, dist = cam_orbit(a, co, lo, hi, w / h)
        print(f"IVE_CAM dist={dist:.3f} target={[round(v, 3) for v in target]} loc={[round(v, 3) for v in co.location]}")

    r = sc.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, a.res_pct
    r.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = a.samples
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.max_bounces = 6
    sc.cycles.transparent_max_bounces = 12
    if a.threads:
        r.threads_mode, r.threads = "FIXED", a.threads
    r.film_transparent = a.bg == "transparent"
    if a.bg != "transparent":
        bgc = [float(v) for v in a.bg.split(",")]
        sc.world.node_tree.nodes["Background"].inputs[0].default_value = tuple(bgc) + (1,)
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = a.view
    sc.view_settings.exposure = a.exposure
    r.fps = int(round(a.fps))

    n = max(1, int(round(a.seconds * a.fps)))
    sc.frame_start, sc.frame_end = 1, n
    if n > 1 or a.spin_start:
        orbit_pivot = None
        if a.orbit and not a.camera:
            orbit_pivot = bpy.data.objects.new("orbit_pivot", None)
            orbit_pivot.location = target
            sc.collection.objects.link(orbit_pivot)
            bpy.context.view_layer.update()
            mw = co.matrix_world.copy()
            co.parent = orbit_pivot
            co.matrix_world = mw
        for f in range(1, n + 1):
            t = ease((f - 1) / max(1, n - 1), a.ease)
            pivot.rotation_euler = (0, 0, math.radians(a.spin_start + a.spin * t))
            pivot.keyframe_insert("rotation_euler", frame=f)
            if orbit_pivot:
                orbit_pivot.rotation_euler = (0, 0, math.radians(a.orbit * t))
                orbit_pivot.keyframe_insert("rotation_euler", frame=f)

    if a.cam_anim:
        r.use_persistent_data = True          # only the camera moves between frames: keep the BVH and textures loaded
        cams = json.load(open(a.cam_anim))
        idx = list(range(len(cams)))
        if a.frames:
            f0, f1 = (int(v) for v in a.frames.split("-"))
            idx = [i for i in idx if f0 <= i <= f1]
        os.makedirs(a.out, exist_ok=True)
        for i in idx:
            c = cams[i]
            dst = os.path.join(os.path.abspath(a.out), f"f_{c.get('src', i):04d}.png")
            if c is None or os.path.exists(dst):
                continue
            if "steer" in c:
                steer(c["steer"])
            cd.lens = c["focal_mm"]; cd.sensor_width = c.get("sensor_width_mm", 36.0); cd.sensor_fit = "HORIZONTAL"
            cd.shift_x, cd.shift_y = c.get("shift_x", 0.0), c.get("shift_y", 0.0)
            co.matrix_world = Matrix.Translation(c["blender"]["location"]) @ Matrix(c["blender"]["rotation_matrix"]).to_4x4()
            r.filepath = dst
            bpy.ops.render.render(write_still=True)
        print("IVE_SEQUENCE " + a.out)
        return
    if a.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.save_blend))
    out = os.path.abspath(a.out)
    if n == 1:
        r.filepath = out
        bpy.ops.render.render(write_still=True)
        print("IVE_STILL " + out)
    else:
        os.makedirs(out, exist_ok=True)
        r.filepath = os.path.join(out, "f_")
        bpy.ops.render.render(animation=True)
        print(f"IVE_SEQUENCE {out} frames={n} fps={a.fps}")
    print(f"IVE_BBOX lo={[round(v, 3) for v in lo]} hi={[round(v, 3) for v in hi]}")


main()
