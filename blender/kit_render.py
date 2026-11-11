"""Render an Epsilon showroom car GLB (Epsilon-Site `showroom/models/eps-*.glb`) with its kit fitted.

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
    ap.add_argument("--glb", required=True)
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
    ap.add_argument("--steer", type=float, default=0, help="turn the front wheels (wheel_FL / wheel_FR) this many degrees about "
                    "their own vertical axis; positive = steering left (game menus park cars with the wheels turned)")
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
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    bpy.ops.import_scene.gltf(filepath=a.glb)
    missing = hide_nodes([n for n in a.hide.split(",") if n])
    if missing:
        print("IVE_WARN hide: no such node(s): " + ",".join(missing))
    lookdev(a)

    if a.steer:
        for n in ("wheel_FL", "wheel_FR"):
            o = bpy.data.objects.get(n)
            if not o:
                print("IVE_WARN steer: no node " + n); continue
            wl, wh = bbox([x for x in [o] + list(o.children_recursive) if x.type == "MESH"])
            c = (wl + wh) / 2
            R = Matrix.Translation(c) @ Matrix.Rotation(math.radians(a.steer), 4, "Z") @ Matrix.Translation(-c)
            o.matrix_world = R @ o.matrix_world
        bpy.context.view_layer.update()

    # turntable pivot: everything imported hangs off one empty at the car's footprint centre
    lo, hi = bbox(visible_meshes())
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
