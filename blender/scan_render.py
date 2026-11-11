"""Render a prepared scan scene (from scan_prep.py) with a scan "look" and camera move.

    blender -b -P blender/scan_render.py -- --scene work/scene.blend --look scan \
        --camera work/cam_A.json --move orbit --seconds 4 --fps 24 --out work/renders/scanA/

Looks (see knowledge/scan-looks.md for when to use each):
  clay        neutral matte grey; reads as "engineering model"
  scan        dark body + cyan fresnel rim + faint wireframe; the hero scan look
  wire        emissive wireframe on black; data/tech beat
  points      point cloud (Geometry Nodes); raw-capture beat
  xray        additive fresnel glass; layered/inside-the-part beat
  color       captured vertex colour / texture, softly lit; closest to IRL
  sweep       scan-line sweeps along an axis turning clay -> scan; reveal beat

Camera:
  --camera cam.json   exact camera from `ive solve` (the 1:1 match pose). The FIRST
                      frame of every move is that exact pose so it cuts 1:1.
  (none)              auto-framed 3/4 front view
Moves: static | orbit | push | pull | rise   (amount via --move-amount)

Also: --raycast "name:x,y;name2:x,y" prints the 3D scan point under each pixel of
this camera's render. Agents use it to turn landmarks picked on a reference render
into the xyz values needed by matchpoints.json.
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
    ap.add_argument("--scene", required=True)
    ap.add_argument("--out", required=True, help="output dir for PNG sequence, or a .png path for a single still")
    ap.add_argument("--look", default="silver", choices=["silver", "clay", "scan", "wire", "points", "xray", "color", "sweep"])
    ap.add_argument("--accent", default="0.0,0.85,1.0", help="accent RGB 0-1 (default illumaesthetic cyan)")
    ap.add_argument("--bg", default="0.004,0.004,0.005", help="background RGB, or 'transparent'")
    ap.add_argument("--camera", help="camera JSON from `ive solve`")
    ap.add_argument("--res", default="", help="WxH; defaults to camera image_size or 1920x1080")
    ap.add_argument("--res-pct", type=int, default=100)
    ap.add_argument("--fps", type=float, default=24)
    ap.add_argument("--seconds", type=float, default=0, help="0 = single still")
    ap.add_argument("--move", default="static", choices=["static", "orbit", "push", "pull", "rise"])
    ap.add_argument("--move-amount", type=float, default=0, help="degrees for orbit, fraction for push/pull, metres for rise")
    ap.add_argument("--ease", default="ease_out", choices=["linear", "ease_in", "ease_out", "ease_in_out"])
    ap.add_argument("--sweep-axis", default="y", choices=["x", "y", "z"])
    ap.add_argument("--engine", default="cycles", choices=["cycles", "eevee", "workbench"])
    ap.add_argument("--samples", type=int, default=32)
    ap.add_argument("--explode", action="append", default=[],
                    help="'part.blend:dx,dy,dz[:start:end[:rotZdeg:rstart:rend]]' append a prepared part scan, move it by "
                         "dx,dy,dz (m) between start..end (fractions of the shot), then optionally spin it [x|y|z]deg "
                         "(prefix start with 'r', e.g. r0.2, to run it backwards: part flies back into place) "
                         "about its own centre (x = flip about the car's width axis, best for bumpers) between rstart..rend - exploded views that show inside + outside")
    ap.add_argument("--look-at", default="", help="x,y,z pivot for orbit moves (default: scan bbox centre)")
    ap.add_argument("--raycast", help="'name:x,y;...' pixel coords in this camera's render")
    ap.add_argument("--save-blend", help="also save the lookdev'd scene here for manual tweaking")
    return ap.parse_args(argv())


def rgb(s):
    return tuple(float(v) for v in s.split(",")) + (1.0,)


def scan_objects():
    objs = [o for o in bpy.data.objects if o.type == "MESH" and o.get("ive_scan")]
    return objs or [o for o in bpy.data.objects if o.type == "MESH"]


def bbox(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


# ---------------------------------------------------------------- materials
def new_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    return m, nt, out


def principled(nt, color, rough=0.6, metal=0.0):
    p = nt.nodes.new("ShaderNodeBsdfPrincipled")
    p.inputs["Base Color"].default_value = color
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    return p


def emission(nt, color, strength):
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = color
    e.inputs["Strength"].default_value = strength
    return e


def fresnel_mix(nt, a_out, b_out, ior=1.25, power=1.0):
    fr = nt.nodes.new("ShaderNodeLayerWeight")
    fr.inputs["Blend"].default_value = 0.35 * power
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(fr.outputs["Facing"], mix.inputs[0])
    nt.links.new(a_out, mix.inputs[1])
    nt.links.new(b_out, mix.inputs[2])
    return mix


def mat_silver():
    """House look (Temerario reel): satin metallic silver; scan micro-detail reads in reflections."""
    m, nt, out = new_mat("ive_silver")
    p = principled(nt, (0.62, 0.63, 0.66, 1), 0.32, 0.85)
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.08
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 0.85
    mul.inputs["A"].default_value = (0.62, 0.63, 0.66, 1)
    nt.links.new(ao.outputs["Color"], mul.inputs["B"])
    ao.inputs["Color"].default_value = (1, 1, 1, 1)
    nt.links.new(mul.outputs["Result"], p.inputs["Base Color"])
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


def studio_world(bg, transparent):
    """Camera sees `bg`; reflections/lighting see a soft studio gradient (bright top, dark floor)."""
    w = bpy.data.worlds.new("ive_world")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    lp = nt.nodes.new("ShaderNodeLightPath")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1)
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    env = nt.nodes.new("ShaderNodeBackground")
    env.inputs["Strength"].default_value = 1.2
    nt.links.new(ramp.outputs[0], env.inputs["Color"])
    cam_bg = nt.nodes.new("ShaderNodeBackground")
    cam_bg.inputs["Color"].default_value = bg
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(env.outputs[0], mix.inputs[1])
    nt.links.new(cam_bg.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    bpy.context.scene.render.film_transparent = transparent


def mat_clay():
    m, nt, out = new_mat("ive_clay")
    p = principled(nt, (0.55, 0.55, 0.56, 1), 0.55)
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


def mat_scan(accent, wire_amount=0.25):
    m, nt, out = new_mat("ive_scan")
    body = principled(nt, (0.02, 0.025, 0.03, 1), 0.35, 0.2)
    rim = emission(nt, accent, 3.0)
    mix = fresnel_mix(nt, body.outputs[0], rim.outputs[0])
    wf = nt.nodes.new("ShaderNodeWireframe")
    wf.use_pixel_size = True
    wf.inputs["Size"].default_value = 0.6
    wmul = nt.nodes.new("ShaderNodeMath")
    wmul.operation = "MULTIPLY"
    wmul.inputs[1].default_value = wire_amount
    nt.links.new(wf.outputs[0], wmul.inputs[0])
    wem = emission(nt, accent, 2.0)
    mix2 = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(wmul.outputs[0], mix2.inputs[0])
    nt.links.new(mix.outputs[0], mix2.inputs[1])
    nt.links.new(wem.outputs[0], mix2.inputs[2])
    nt.links.new(mix2.outputs[0], out.inputs[0])
    return m


def mat_wire(accent):
    m, nt, out = new_mat("ive_wire")
    wf = nt.nodes.new("ShaderNodeWireframe")
    wf.use_pixel_size = True
    wf.inputs["Size"].default_value = 0.8
    holdout = nt.nodes.new("ShaderNodeEmission")
    holdout.inputs["Color"].default_value = (0, 0, 0, 1)
    em = emission(nt, accent, 4.0)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(wf.outputs[0], mix.inputs[0])
    nt.links.new(holdout.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


def mat_xray(accent):
    m, nt, out = new_mat("ive_xray")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    em = emission(nt, accent, 0.5)
    mix = fresnel_mix(nt, tr.outputs[0], em.outputs[0], power=2.4)  # glowing edges, see-through faces
    add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(mix.outputs[0], add.inputs[0])
    nt.links.new(tr.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs[0])
    if hasattr(m, "blend_method"):
        m.blend_method = "BLEND"
    return m


def mat_color(obj):
    if obj.active_material and obj.data.uv_layers:
        return obj.active_material  # textured scan: keep its own material
    m, nt, out = new_mat("ive_color")
    p = principled(nt, (0.6, 0.6, 0.6, 1), 0.5)
    if obj.data.color_attributes:
        vc = nt.nodes.new("ShaderNodeVertexColor")
        vc.layer_name = obj.data.color_attributes[0].name
        nt.links.new(vc.outputs["Color"], p.inputs["Base Color"])
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


def mat_sweep(accent, axis, lo, hi, f0, f1):
    """Clay behind the front, glowing scan line at the front, scan look ahead of it."""
    m, nt, out = new_mat("ive_sweep")
    clay = principled(nt, (0.55, 0.55, 0.56, 1), 0.55)
    scan_body = principled(nt, (0.02, 0.025, 0.03, 1), 0.35, 0.2)
    rim = emission(nt, accent, 3.0)
    scan = fresnel_mix(nt, scan_body.outputs[0], rim.outputs[0])
    line = emission(nt, accent, 25.0)

    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    front = nt.nodes.new("ShaderNodeValue")
    ai = "xyz".index(axis)
    margin = 0.05 * (hi[ai] - lo[ai])
    front.outputs[0].default_value = lo[ai] - margin
    front.outputs[0].keyframe_insert("default_value", frame=f0)
    front.outputs[0].default_value = hi[ai] + margin
    front.outputs[0].keyframe_insert("default_value", frame=f1)

    d = nt.nodes.new("ShaderNodeMath")
    d.operation = "SUBTRACT"
    nt.links.new(sep.outputs[ai], d.inputs[0])
    nt.links.new(front.outputs[0], d.inputs[1])
    behind = nt.nodes.new("ShaderNodeMath")
    behind.operation = "LESS_THAN"
    behind.inputs[1].default_value = 0.0
    nt.links.new(d.outputs[0], behind.inputs[0])
    band = nt.nodes.new("ShaderNodeMath")
    band.operation = "ABSOLUTE"
    nt.links.new(d.outputs[0], band.inputs[0])
    bandm = nt.nodes.new("ShaderNodeMath")
    bandm.operation = "LESS_THAN"
    bandm.inputs[1].default_value = 0.004 * (hi[ai] - lo[ai]) + 0.002
    nt.links.new(band.outputs[0], bandm.inputs[0])

    m1 = nt.nodes.new("ShaderNodeMixShader")  # behind the front = scanned (scan look)
    nt.links.new(behind.outputs[0], m1.inputs[0])
    nt.links.new(clay.outputs[0], m1.inputs[1])
    nt.links.new(scan.outputs[0], m1.inputs[2])
    m2 = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(bandm.outputs[0], m2.inputs[0])
    nt.links.new(m1.outputs[0], m2.inputs[1])
    nt.links.new(line.outputs[0], m2.inputs[2])
    nt.links.new(m2.outputs[0], out.inputs[0])
    return m


def to_points(obj, accent, radius):
    gn = bpy.data.node_groups.new("ive_points", "GeometryNodeTree")
    if hasattr(gn, "interface"):
        gn.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
        gn.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    gi = gn.nodes.new("NodeGroupInput")
    go = gn.nodes.new("NodeGroupOutput")
    mp = gn.nodes.new("GeometryNodeMeshToPoints")
    mp.inputs["Radius"].default_value = radius
    sm = gn.nodes.new("GeometryNodeSetMaterial")
    m, nt, out = new_mat("ive_points")
    nt.links.new(emission(nt, accent, 3.0).outputs[0], out.inputs[0])
    sm.inputs["Material"].default_value = m
    gn.links.new(gi.outputs[0], mp.inputs["Mesh"])
    gn.links.new(mp.outputs[0], sm.inputs["Geometry"])
    gn.links.new(sm.outputs[0], go.inputs[0])
    mod = obj.modifiers.new("ive_points", "NODES")
    mod.node_group = gn


# ---------------------------------------------------------------- lighting/world
def setup_world(bg, transparent):
    w = bpy.data.worlds.new("ive_world")
    bpy.context.scene.world = w
    w.use_nodes = True
    b = w.node_tree.nodes.get("Background")
    b.inputs["Color"].default_value = bg
    b.inputs["Strength"].default_value = 1.0
    bpy.context.scene.render.film_transparent = transparent


def add_light(name, kind, loc, energy, size=2.0, color=(1, 1, 1)):
    d = bpy.data.lights.new(name, kind)
    d.energy = energy
    d.color = color
    if kind == "AREA":
        d.size = size
    o = bpy.data.objects.new(name, d)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    track = o.constraints.new("TRACK_TO")
    track.target = bpy.data.objects.get("SCAN_ROOT") or scan_objects()[0]
    return o


def studio_lights(lo, hi):
    c = (lo + hi) / 2
    r = max(hi - lo)
    # Temerario reference: soft top/key, gentle rim, no hard shadows, dark background.
    add_light("key", "AREA", c + Vector((r * 0.9, -r * 0.9, r * 0.9)), 90 * r * r, r)
    add_light("rim", "AREA", c + Vector((-r * 0.8, r * 1.0, r * 0.6)), 120 * r * r, r * 0.6, (0.85, 0.92, 1.0))
    add_light("top", "AREA", c + Vector((0, 0, r * 1.5)), 70 * r * r, r * 1.5)


# ---------------------------------------------------------------- camera
def make_camera(args, lo, hi):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("ive_cam")
    cam = bpy.data.objects.new("ive_cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.clip_start = 0.01
    cd.clip_end = 1000
    cd.sensor_fit = "HORIZONTAL"
    if args.camera:
        cj = json.load(open(args.camera))
        cd.sensor_width = cj["sensor_width_mm"]
        cd.lens = cj["focal_mm"]
        cd.shift_x = cj.get("shift_x", 0.0)
        cd.shift_y = cj.get("shift_y", 0.0)
        R = Matrix(cj["blender"]["rotation_matrix"])
        cam.matrix_world = Matrix.Translation(Vector(cj["blender"]["location"])) @ R.to_4x4()
        size = cj["image_size"]
    else:
        cd.sensor_width = 36
        cd.lens = 50
        c = (lo + hi) / 2
        r = (hi - lo).length
        cam.location = c + Vector((r * 0.95, -r * 1.25, r * 0.35))
        direction = c - cam.location
        cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        size = [1920, 1080]
    if args.res:
        size = [int(v) for v in args.res.lower().split("x")]
    sc.render.resolution_x, sc.render.resolution_y = size
    sc.render.resolution_percentage = args.res_pct
    return cam


def ease(t, kind):
    if kind == "ease_in":
        return t * t
    if kind == "ease_out":
        return 1 - (1 - t) ** 2
    if kind == "ease_in_out":
        return t * t * (3 - 2 * t)
    return t


def animate_camera(cam, args, lo, hi, f0, f1):
    """Every move starts from the exact (matched) pose at f0 so the cut is 1:1."""
    if args.move == "static" or f1 <= f0:
        return
    M0 = cam.matrix_world.copy()
    c = (lo + hi) / 2
    pivot = Vector((c.x, c.y, M0.translation.z * 0 + c.z))
    for f in range(f0, f1 + 1):
        t = ease((f - f0) / (f1 - f0), args.ease)
        if args.move == "orbit":
            ang = math.radians(args.move_amount or 25) * t
            Rz = Matrix.Rotation(ang, 4, "Z")
            M = Matrix.Translation(pivot) @ Rz @ Matrix.Translation(-pivot) @ M0
        elif args.move in ("push", "pull"):
            amt = (args.move_amount or 0.2) * (1 if args.move == "push" else -1)
            fwd = -(M0.to_3x3() @ Vector((0, 0, 1)))
            dist = (c - M0.translation).length
            M = Matrix.Translation(fwd * dist * amt * t) @ M0
        else:  # rise
            M = Matrix.Translation(Vector((0, 0, (args.move_amount or 0.5) * t))) @ M0
        cam.matrix_world = M
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
    cam.matrix_world = M0


# ---------------------------------------------------------------- raycast
def raycast(cam, spec):
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    W = sc.render.resolution_x
    H = sc.render.resolution_y
    frame = cam.data.view_frame(scene=sc)  # 4 corners in camera space (tr, br, bl, tl)
    tr, br, bl, tl = frame
    res = {}
    for item in spec.split(";"):
        if not item.strip():
            continue
        name, xy = item.split(":")
        x, y = (float(v) for v in xy.split(","))
        u, v = x / W, y / H
        top = tl.lerp(tr, u)
        bot = bl.lerp(br, u)
        p_cam = top.lerp(bot, v)
        origin = cam.matrix_world.translation
        if cam.data.type == "ORTHO":
            origin = cam.matrix_world @ Vector((p_cam.x, p_cam.y, 0))
            d = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
        else:
            d = (cam.matrix_world @ p_cam) - origin
        hit, loc, *_ = sc.ray_cast(dg, origin, d.normalized())
        res[name] = list(loc) if hit else None
    print("IVE_RAYCAST", json.dumps(res))
    return res


# ---------------------------------------------------------------- main
def main():
    args = parse()
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(args.scene))
    sc = bpy.context.scene
    objs = scan_objects()
    lo, hi = bbox(objs)
    accent = rgb(args.accent)

    parts = []
    for spec in args.explode:
        bits = spec.split(":")
        path, off = bits[0], Vector([float(v) for v in bits[1].split(",")])
        reverse = len(bits) > 2 and bits[2].startswith("r")  # "r0.2": part starts exploded and returns home
        if reverse:
            bits[2] = bits[2][1:]
        a0 = float(bits[2]) if len(bits) > 2 else 0.15
        a1 = float(bits[3]) if len(bits) > 3 else 0.85
        rot = None
        if len(bits) > 6:  # rotation spec: "180" (about Z) or "x180" / "y-90" / "z180"
            ax = bits[4][0].lower() if bits[4][0].isalpha() else "z"
            deg = float(bits[4][1:] if bits[4][0].isalpha() else bits[4])
            rot = (deg, float(bits[5]), float(bits[6]), "xyz".index(ax))
        with bpy.data.libraries.load(os.path.abspath(path), link=False) as (src, dst):
            dst.objects = list(src.objects)
        for o in dst.objects:
            if o is None:
                continue
            bpy.context.scene.collection.objects.link(o)
            if o.type == "MESH":
                o["ive_scan"] = True
                parts.append((o, off, a0, a1, rot, reverse))
    objs = objs + [p[0] for p in parts]

    cam = make_camera(args, lo, hi)
    if args.raycast:
        raycast(cam, args.raycast)
        return

    sc.render.fps = int(round(args.fps))
    sc.render.fps_base = sc.render.fps / args.fps
    nframes = max(1, int(round(args.seconds * args.fps)))
    sc.frame_start, sc.frame_end = 1, nframes

    transparent = args.bg == "transparent"
    if args.look == "silver":
        studio_world((0, 0, 0, 1) if transparent else rgb(args.bg), transparent)
        studio_lights(lo, hi)
    else:
        setup_world((0, 0, 0, 1) if transparent else rgb(args.bg), transparent)
    if args.look in ("clay", "color", "sweep", "scan"):
        studio_lights(lo, hi)

    for o in objs:
        if args.look == "points":
            to_points(o, accent, radius=max(hi - lo) / 1500)
            continue
        m = {
            "silver": mat_silver,
            "clay": mat_clay,
            "scan": lambda: mat_scan(accent),
            "wire": lambda: mat_wire(accent),
            "xray": lambda: mat_xray(accent),
            "color": lambda: mat_color(o),
            "sweep": lambda: mat_sweep(accent, args.sweep_axis, lo, hi, 1, nframes),
        }[args.look]()
        o.data.materials.clear()
        o.data.materials.append(m)

    if args.look_at:
        c = Vector([float(v) for v in args.look_at.split(",")])
        lo, hi = c, c
    animate_camera(cam, args, lo, hi, 1, nframes)
    for o, off, a0, a1, rot, reverse in parts:
        # Pivot empty at the part's own centre so spins happen in place, not about the car origin.
        bpy.context.view_layer.update()
        plo, phi = bbox([o])
        pivot = bpy.data.objects.new(f"pivot_{o.name}", None)
        bpy.context.scene.collection.objects.link(pivot)
        pivot.location = (plo + phi) / 2
        bpy.context.view_layer.update()
        root = o.parent or o
        mw = root.matrix_world.copy()
        root.parent = pivot
        root.matrix_world = mw
        base = pivot.location.copy()
        for f in range(1, nframes + 1):
            t = (f - 1) / max(1, nframes - 1)
            tm = min(1.0, max(0.0, (t - a0) / max(1e-6, a1 - a0)))
            k = ease(tm, "ease_in_out")
            pivot.location = base + off * ((1 - k) if reverse else k)
            pivot.keyframe_insert("location", frame=f)
            if rot:
                tr = min(1.0, max(0.0, (t - rot[1]) / max(1e-6, rot[2] - rot[1])))
                e = [0.0, 0.0, 0.0]
                kr = ease(tr, "ease_in_out")
                e[rot[3]] = math.radians(rot[0]) * ((1 - kr) if reverse else kr)
                pivot.rotation_euler = e
                pivot.keyframe_insert("rotation_euler", frame=f)

    if args.engine == "cycles":
        sc.render.engine = "CYCLES"
        sc.cycles.samples = args.samples
        sc.cycles.use_denoising = True
        sc.render.use_persistent_data = True  # keep BVH between frames: 3M-tri scans otherwise re-sync every frame
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.device = "CPU"
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            for t in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
                try:
                    prefs.compute_device_type = t
                    prefs.get_devices()
                    if any(d.type == t for d in prefs.devices):
                        for d in prefs.devices:
                            d.use = True
                        sc.cycles.device = "GPU"
                        break
                except TypeError:
                    continue
        except Exception:
            pass
    elif args.engine == "eevee":
        sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in {e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items} else "BLENDER_EEVEE"
    else:
        sc.render.engine = "BLENDER_WORKBENCH"

    try:
        sc.view_settings.view_transform = "AgX"
    except TypeError:
        sc.view_settings.view_transform = "Filmic"
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"

    if args.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(args.save_blend), copy=True)

    out = os.path.abspath(args.out)
    if nframes == 1 and out.endswith(".png"):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
    else:
        os.makedirs(out, exist_ok=True)
        sc.render.filepath = os.path.join(out, "f_")
        bpy.ops.render.render(animation=True)
    print("IVE_RENDER_DONE", out)


if __name__ == "__main__":
    main()
