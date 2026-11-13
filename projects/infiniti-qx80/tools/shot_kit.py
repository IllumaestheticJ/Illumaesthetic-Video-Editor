"""Kit-on-scan shot for the QX80 R-Spec v4 reel (copied from the ferrari-296 shot.py, extended).
Adds: part "show": [t_on, t_off] visibility windows, part "mat": silver|kit|black|purple, and a spec "paint"
wipe {"t0","t1","y0","y1","soft"} that sweeps every material to its "paint" target (base -> purple; parts -> their
"paint" key) along the car's Y axis (world position), front (+Y) to rear by default.

Original doc:

    blender -b -P projects/ferrari-296/tools/shot.py -- spec.json

Reuses the house look from blender/scan_render.py (mat_silver, studio_world, studio_lights) but
adds what that script can't do: a camera path through several keyed poses (loc/target/focal),
and parts that move/rotate about an arbitrary pivot (hinged hood, engine cover) on keyed times.

spec.json:
{
  "base": ["car.blend", ...],            # prepared .blend files (all prepped --like the car)
  "parts": [{"blend": "hood.blend", "pivot": [x,y,z], "color": "red"?,   # color only for checks
             "keys": [{"t": 0.0, "loc": [dx,dy,dz], "rot": [rx,ry,rz], "ease": "inout"}, ...]}],
  "camera": {"keys": [{"t": 0, "loc": [..], "target": [..], "focal": 30, "ease": "inout"}, ...],
             "sensor": 20.25},
  "seconds": 4.8, "fps": 15, "res": "1080x1920", "res_pct": 75, "samples": 12,
  "out": "dir/ or still.png", "base_color": "silver|grey"
}
Times are seconds from the shot start; "ease" applies to the segment ENDING at that key
(inout | in | out | lin). rot is degrees, XYZ euler about the part's pivot.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Euler, Matrix, Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "blender"))
import scan_render as sr  # noqa: E402


def ease(t, kind):
    t = min(1.0, max(0.0, t))
    if kind == "in":
        return t * t * t
    if kind == "out":
        return 1 - (1 - t) ** 3
    if kind == "lin":
        return t
    if kind == "in2":
        return t * t
    if kind == "out2":
        return 1 - (1 - t) ** 2
    return t * t * (3 - 2 * t)  # inout (smoothstep)


def sample(keys, t, field):
    """Piecewise eased interpolation of keys[field] at time t."""
    if t <= keys[0]["t"]:
        return keys[0][field]
    for a, b in zip(keys, keys[1:]):
        if t <= b["t"]:
            u = (t - a["t"]) / max(1e-9, b["t"] - a["t"])
            k = ease(u, b.get("ease", "inout"))
            va, vb = a[field], b[field]
            if isinstance(va, (int, float)):
                return va + (vb - va) * k
            return [x + (y - x) * k for x, y in zip(va, vb)]
    return keys[-1][field]


def load_blend(path):
    with bpy.data.libraries.load(os.path.abspath(path), link=False) as (src, dst):
        dst.objects = list(src.objects)
    meshes = []
    for o in dst.objects:
        if o is None:
            continue
        bpy.context.scene.collection.objects.link(o)
        if o.type == "MESH":
            o["ive_scan"] = True
            meshes.append(o)
    return meshes


def mat_check(rgb):
    m, nt, out = sr.new_mat("ive_check")
    p = sr.principled(nt, rgb + (1,), 0.5)
    e = sr.emission(nt, rgb + (1,), 0.6)
    add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(p.outputs[0], add.inputs[0])
    nt.links.new(e.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs[0])
    return m


def mat_kit():
    """Kit parts in the blue of Ecky's design viewport screenshots (satin, slightly metallic)."""
    m, nt, out = sr.new_mat("qx_kit")
    p = sr.principled(nt, (0.02, 0.30, 0.48, 1), 0.38, 0.25)
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


def mat_black():
    m, nt, out = sr.new_mat("qx_black")
    p = sr.principled(nt, (0.012, 0.012, 0.014, 1), 0.42, 0.1)
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


def mat_purple():
    """Midnight Purple colour-shift wrap: deep purple facing, blue/teal at grazing angles, glossy metallic.
    Wrap only covers the body: wheels (measured axles y +1.65 / -1.44, centre z 0.42, r 0.39), the glasshouse band
    (z 1.30-1.84) and the stock grille (y > 2.35, |x| < 0.62, z 0.35-1.05) render gloss black."""
    m, nt, out = sr.new_mat("qx_purple")
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.45
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.032, 0.004, 0.060, 1)
    ramp.color_ramp.elements[1].color = (0.004, 0.045, 0.080, 1)
    mid = ramp.color_ramp.elements.new(0.55); mid.color = (0.085, 0.022, 0.030, 1)   # copper flip seen on the real wrap (photo 1702)
    nt.links.new(lw.outputs["Facing"], ramp.inputs[0])
    p = sr.principled(nt, (0.04, 0.008, 0.07, 1), 0.24, 0.8)
    nt.links.new(ramp.outputs[0], p.inputs["Base Color"])
    blk = sr.principled(nt, (0.008, 0.008, 0.01, 1), 0.18, 0.2)
    for q in (p, blk):
        try: q.inputs["Coat Weight"].default_value = 0.8
        except KeyError: pass
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    X, Y, Z = sep.outputs[0], sep.outputs[1], sep.outputs[2]
    def op(o, a, b=None):
        n = nt.nodes.new("ShaderNodeMath"); n.operation = o
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: nt.links.new(v, n.inputs[i])
        return n.outputs[0]
    ax = op("ABSOLUTE", X)
    def wheel(yc):
        dy = op("SUBTRACT", Y, yc); dz = op("SUBTRACT", Z, 0.42)
        r2 = op("ADD", op("MULTIPLY", dy, dy), op("MULTIPLY", dz, dz))
        return op("MULTIPLY", op("LESS_THAN", r2, 0.39 * 0.39), op("GREATER_THAN", ax, 0.75))
    wheels = op("MAXIMUM", wheel(1.65), wheel(-1.44))
    glass = op("MULTIPLY", op("GREATER_THAN", Z, 1.30), op("LESS_THAN", Z, 1.84))
    grille = op("MULTIPLY", op("MULTIPLY", op("GREATER_THAN", Y, 2.35), op("LESS_THAN", ax, 0.62)),
                op("MULTIPLY", op("GREATER_THAN", Z, 0.35), op("LESS_THAN", Z, 1.05)))
    black = op("MAXIMUM", op("MAXIMUM", wheels, glass), grille)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(black, mix.inputs[0]); nt.links.new(p.outputs[0], mix.inputs[1]); nt.links.new(blk.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


EDGE = {}


def paint_mix(pre, post, name):
    """New material = mix(pre, post) by world-Y sweep factor driven by the shared EDGE value node per material."""
    m = pre.copy(); m.name = name
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    pre_link = out.inputs[0].links[0].from_socket
    # bring the post material's node tree in as a group-free copy: rebuild post shader inside
    post_out_node = next(n for n in post.node_tree.nodes if n.type == "OUTPUT_MATERIAL")
    mapping = {}
    for n in post.node_tree.nodes:
        if n.type == "OUTPUT_MATERIAL":
            continue
        c = nt.nodes.new(n.bl_idname)
        for k in ("blend_type", "operation", "data_type"):
            if hasattr(n, k):
                try: setattr(c, k, getattr(n, k))
                except Exception: pass
        if n.bl_idname == "ShaderNodeValToRGB":
            for i, e in enumerate(n.color_ramp.elements):
                if i < len(c.color_ramp.elements): c.color_ramp.elements[i].position = e.position; c.color_ramp.elements[i].color = e.color
        for i, inp in enumerate(n.inputs):
            if hasattr(inp, "default_value"):
                try: c.inputs[i].default_value = inp.default_value
                except Exception: pass
        mapping[n.name] = c
    for l in post.node_tree.links:
        if l.to_node.type == "OUTPUT_MATERIAL":
            post_sock = mapping[l.from_node.name].outputs[l.from_socket.name]
            continue
        nt.links.new(mapping[l.from_node.name].outputs[l.from_socket.name], mapping[l.to_node.name].inputs[l.to_socket.identifier] if False else mapping[l.to_node.name].inputs[list(l.to_node.inputs).index(l.to_socket)])
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    edge = nt.nodes.new("ShaderNodeValue"); edge.name = "qx_edge"
    soft = EDGE["soft"]
    sub = nt.nodes.new("ShaderNodeMath"); sub.operation = "SUBTRACT"   # y - edge
    nt.links.new(sep.outputs[1], sub.inputs[0]); nt.links.new(edge.outputs[0], sub.inputs[1])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -soft; mr.inputs["From Max"].default_value = soft
    mr.clamp = True
    nt.links.new(sub.outputs[0], mr.inputs["Value"])
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mr.outputs[0], mix.inputs[0])   # 1 where y > edge -> painted
    if EDGE.get("rear_to_front"):   # painted where y < edge (edge sweeps -Y -> +Y)
        nt.links.new(post_sock, mix.inputs[1]); nt.links.new(pre_link, mix.inputs[2])
    else:                           # painted where y > edge (edge sweeps +Y -> -Y)
        nt.links.new(pre_link, mix.inputs[1]); nt.links.new(post_sock, mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    EDGE.setdefault("nodes", []).append(edge)
    return m


def main():
    spec = json.load(open(sys.argv[sys.argv.index("--") + 1]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    base = []
    for b in spec["base"]:
        base += load_blend(b)
    bpy.context.view_layer.update()  # matrix_world is stale right after linking
    lo, hi = sr.bbox(base)
    fps = spec.get("fps", 15)
    secs = spec.get("seconds", 0)
    nframes = max(1, int(round(secs * fps)))
    sc.render.fps = int(fps)
    sc.frame_start, sc.frame_end = 1, nframes

    sr.studio_world(sr.rgb(spec.get("bg", "0.004,0.004,0.005")), False)
    sr.studio_lights(lo, hi)
    silver = sr.mat_silver()
    grey = sr.mat_clay()
    MATS = {"silver": silver, "kit": mat_kit(), "black": mat_black(), "purple": mat_purple(), "grey": grey}
    paint = spec.get("paint")
    if paint:
        EDGE["soft"] = paint.get("soft", 0.15)
        EDGE["rear_to_front"] = paint["y1"] > paint["y0"]
    def material(name, paint_to):
        if not paint or not paint_to:
            return MATS[name]
        key = f"{name}->{paint_to}"
        if key not in MATS:
            MATS[key] = paint_mix(MATS[name], MATS[paint_to], key)
        return MATS[key]
    base_mat = material(spec.get("base_mat", "grey" if spec.get("base_color") == "grey" else "silver"), spec.get("base_paint", "purple"))
    for o in base:
        o.data.materials.clear()
        o.data.materials.append(base_mat)

    colors = {"red": (0.9, 0.05, 0.03), "cyan": (0.0, 0.7, 1.0), "green": (0.1, 0.9, 0.1),
              "yellow": (1.0, 0.8, 0.0), "magenta": (0.9, 0.0, 0.8)}
    for p in spec.get("parts", []):
        objs = load_blend(p["blend"])
        m = mat_check(colors[p["color"]]) if p.get("color") else material(p.get("mat", "silver"), p.get("paint"))
        for o in objs:
            o.data.materials.clear()
            o.data.materials.append(m)
        if p.get("show"):
            t_on, t_off = p["show"]
            for f in range(1, nframes + 1):
                t = (f - 1) / fps
                hid = not (t_on <= t < t_off)
                for o in objs:
                    o.hide_render = hid
                    o.keyframe_insert("hide_render", frame=f)
        keys = p.get("keys")
        if not keys:
            continue
        bpy.context.view_layer.update()  # else bbox is in raw mm and rotations swing about a far pivot
        plo, phi = sr.bbox(objs)
        pv = bpy.data.objects.new("pivot", None)
        sc.collection.objects.link(pv)
        pv.location = Vector(p["pivot"]) if p.get("pivot") else (plo + phi) / 2
        bpy.context.view_layer.update()
        for o in objs:
            root = o.parent or o
            mw = root.matrix_world.copy()
            root.parent = pv
            root.matrix_world = mw
        base_loc = pv.location.copy()
        for f in range(1, nframes + 1):
            t = (f - 1) / fps
            pv.location = base_loc + Vector(sample(keys, t, "loc"))
            pv.rotation_euler = Euler([math.radians(v) for v in sample(keys, t, "rot")], "XYZ")
            pv.keyframe_insert("location", frame=f)
            pv.keyframe_insert("rotation_euler", frame=f)

    if paint:
        for f in range(1, nframes + 1):
            t = (f - 1) / fps
            u = min(1.0, max(0.0, (t - paint["t0"]) / max(1e-6, paint["t1"] - paint["t0"])))
            u = u * u * (3 - 2 * u)
            e = paint["y0"] + (paint["y1"] - paint["y0"]) * u
            for n in EDGE.get("nodes", []):
                n.outputs[0].default_value = e
                n.outputs[0].keyframe_insert("default_value", frame=f)

    cd = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.sensor_fit = "HORIZONTAL"
    cd.sensor_width = spec["camera"].get("sensor", 20.25)
    cd.clip_start = 0.01
    ck = spec["camera"]["keys"]
    for f in range(1, nframes + 1):
        t = (f - 1) / fps
        loc = Vector(sample(ck, t, "loc"))
        tgt = Vector(sample(ck, t, "target"))
        cam.location = loc
        cam.rotation_euler = (tgt - loc).to_track_quat("-Z", "Y").to_euler()
        cd.lens = sample(ck, t, "focal")
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.keyframe_insert("lens", frame=f)
    for fc in (cam.animation_data.action.fcurves if hasattr(cam.animation_data.action, "fcurves") else []):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

    w, h = (int(v) for v in spec.get("res", "1080x1920").split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = spec.get("res_pct", 75)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = spec.get("samples", 12)
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    # persistent data + animated parts renders the scene unlit mid-shot (huracan-evo / lexus-is350 finding)
    sc.render.use_persistent_data = not (paint or any(p.get("keys") or p.get("show") for p in spec.get("parts", [])))
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    out = os.path.abspath(spec["out"])
    if spec.get("frames"):  # framing check: only these frames ("first", "mid", "last" or numbers)
        os.makedirs(out, exist_ok=True)
        named = {"first": 1, "mid": (nframes + 1) // 2, "last": nframes}
        for f in spec["frames"]:
            f = named.get(f, f)
            sc.frame_set(int(f))
            sc.render.filepath = os.path.join(out, f"f_{int(f):04d}.png")
            bpy.ops.render.render(write_still=True)
    elif nframes == 1 and out.endswith(".png"):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sc.frame_set(1)
        sc.render.filepath = out
        bpy.ops.render.render(write_still=True)
    else:
        os.makedirs(out, exist_ok=True)
        sc.render.filepath = os.path.join(out, "f_")
        bpy.ops.render.render(animation=True)
    print("IVE_RENDER_DONE", out)


main()
