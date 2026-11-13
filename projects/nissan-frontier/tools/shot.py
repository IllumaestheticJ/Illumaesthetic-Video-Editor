"""Keyframed scan shot (copied from projects/ferrari-296/tools/shot.py for the Nissan Frontier reel).
Change: "persistent": false in the spec turns off Cycles persistent data - with it on, the scene went unlit once a
hinged part started rotating (huracan-evo, 2026-11-11).

    blender -b -P projects/nissan-frontier/tools/shot.py -- spec.json

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


HL_RGB = (0.25, 0.82, 1.0)  # cyan accent for "this scan section" (house 'scan' look accent)


def _w(keys, t):
    """piecewise-linear weight from [[t, w], ...]"""
    if not keys:
        return 0.0
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, w0), (t1, w1) in zip(keys, keys[1:]):
        if t <= t1:
            u = (t - t0) / max(1e-9, t1 - t0)
            u = u * u * (3 - 2 * u)
            return w0 + (w1 - w0) * u
    return keys[-1][1]


def mat_hl(keys, keys_all, fps):
    """House silver mixed toward a cyan-tinted metallic with a soft cyan glow; mix factor keyed per frame."""
    m = sr.mat_silver()
    nt = m.node_tree
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    silver_bsdf = out.inputs[0].links[0].from_node
    hp = sr.principled(nt, (HL_RGB[0] * 0.55, HL_RGB[1] * 0.55, HL_RGB[2] * 0.6, 1), 0.3, 0.7)
    he = sr.emission(nt, HL_RGB + (1,), 0.55)
    add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(hp.outputs[0], add.inputs[0]); nt.links.new(he.outputs[0], add.inputs[1])
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(silver_bsdf.outputs[0], mix.inputs[1]); nt.links.new(add.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    sc = bpy.context.scene
    for f in range(sc.frame_start, sc.frame_end + 1):
        t = (f - 1) / fps
        mix.inputs[0].default_value = max(_w(keys, t), _w(keys_all, t))
        mix.inputs[0].keyframe_insert("default_value", frame=f)
    return m


LIV = "/home/user/media/nissan-frontier/livery/tex"
# livery side-view mapping (prep metres): PSD truck bbox spans nose..tail (y -2.685..2.685) and z 0.067..1.608
LIV_Y0, LIV_LEN, LIV_Z0, LIV_H = -2.685, 5.37, 0.067, 1.541
TILE_W = 2.3


def mat_simple(name, rgb, rough, metal=0.0):
    m, nt, out = sr.new_mat(name)
    p = sr.principled(nt, rgb + (1,), rough, metal)
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


_MATS = {}
LED_KEYS = None  # [[t, w], ...] from the spec ("led"); None = always on


LED2_KEYS = None  # second, independently switched LED group ("led2": fender lights, v8)


def mat_led(name="r_led", which=1):
    """LED lens: dark until switched on, then white emission (keyed strength)."""
    LED_KEYS = globals()["LED_KEYS" if which == 1 else "LED2_KEYS"]
    m, nt, out = sr.new_mat(name)
    p = sr.principled(nt, (0.03, 0.03, 0.035, 1), 0.25)
    e = sr.emission(nt, (1.0, 0.96, 0.9, 1), 3.0)
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(p.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    sc = bpy.context.scene; fps = sc.render.fps
    for f in range(sc.frame_start, sc.frame_end + 1):
        mx.inputs[0].default_value = 1.0 if LED_KEYS is None else _w(LED_KEYS, (f - 1) / fps)
        mx.inputs[0].keyframe_insert("default_value", frame=f)
    return m


def named_mat(k):
    if k not in _MATS:
        _MATS[k] = {"black": lambda: mat_simple("r_black", (0.018, 0.018, 0.02), 0.42),
                    "rubber": lambda: mat_simple("r_rubber", (0.012, 0.012, 0.013), 0.78),
                    "bronze": lambda: mat_simple("r_bronze", (0.17, 0.115, 0.055), 0.38, 1.0),
                    "steel": lambda: mat_simple("r_steel", (0.55, 0.55, 0.57), 0.3, 1.0),
                    "red": lambda: mat_simple("r_red", (0.5, 0.02, 0.015), 0.4),
                    "led": lambda: mat_led(), "led2": lambda: mat_led("r_led2", 2)}[k]()
    return _MATS[k]


def mat_livery(sweep_keys, fps):
    """Ronin wrap from the user's files (tools/livery_tex.py): side view projected along X onto side-facing surfaces
    (left/right images; right has the logo pre-flipped), topo tile on top/front/rear faces, dark glass above the beltline.
    Revealed where world y < sweep (keyed), over house silver."""
    if "livery" in _MATS:
        return _MATS["livery"]
    m = sr.mat_silver(); nt = m.node_tree; N = nt.nodes; Lk = nt.links.new
    out = [n for n in N if n.type == "OUTPUT_MATERIAL"][0]
    silver = out.inputs[0].links[0].from_node
    geo = N.new("ShaderNodeNewGeometry")
    sp = N.new("ShaderNodeSeparateXYZ"); Lk(geo.outputs["Position"], sp.inputs[0])
    sn = N.new("ShaderNodeSeparateXYZ"); Lk(geo.outputs["Normal"], sn.inputs[0])

    def math(op, a, b=None, c=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: Lk(v, n.inputs[i])
        return n.outputs[0]

    def vec(x, y):
        n = N.new("ShaderNodeCombineXYZ")
        for i, v in enumerate((x, y)):
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: Lk(v, n.inputs[i])
        return n.outputs[0]

    def img(name, v, ext):
        n = N.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(os.path.join(LIV, name)); n.extension = ext
        Lk(v, n.inputs[0]); return n

    def mix(f, a, b):
        n = N.new("ShaderNodeMix"); n.data_type = "RGBA"
        for k, v in (("Factor", f), ("A", a), ("B", b)):
            if isinstance(v, (int, float)): n.inputs[k].default_value = v
            elif isinstance(v, tuple): n.inputs[k].default_value = v
            else: Lk(v, n.inputs[k])
        return n.outputs["Result"]
    X, Y, Z = sp.outputs
    u = math("DIVIDE", math("SUBTRACT", Y, LIV_Y0), LIV_LEN)
    v = math("DIVIDE", math("SUBTRACT", Z, LIV_Z0), LIV_H)
    uv = vec(u, v)
    il, ir, iw = img("side_left.png", uv, "CLIP"), img("side_right.png", uv, "CLIP"), img("window_util.png", uv, "CLIP")
    is_right = math("LESS_THAN", X, 0.0)
    side = mix(is_right, il.outputs["Color"], ir.outputs["Color"])
    side_a = math("ADD", math("MULTIPLY", il.outputs["Alpha"], math("SUBTRACT", 1.0, is_right)), math("MULTIPLY", ir.outputs["Alpha"], is_right))
    aspect = 715 / 2048
    ax, ay, az = (math("ABSOLUTE", o) for o in sn.outputs)
    t_top = img("topo_tile.png", vec(math("DIVIDE", X, TILE_W), math("DIVIDE", Y, TILE_W * aspect)), "REPEAT")
    t_frt = img("topo_tile.png", vec(math("DIVIDE", X, TILE_W), math("DIVIDE", Z, TILE_W * aspect)), "REPEAT")
    t_sid = img("topo_tile.png", vec(math("DIVIDE", Y, TILE_W), math("DIVIDE", Z, TILE_W * aspect)), "REPEAT")
    tile = mix(math("GREATER_THAN", ay, az), t_top.outputs["Color"], t_frt.outputs["Color"])
    side_w = math("GREATER_THAN", ax, 0.55)
    side_col = mix(math("GREATER_THAN", side_a, 0.5), t_sid.outputs["Color"], side)
    side_col = mix(math("GREATER_THAN", iw.outputs["Alpha"], 0.5), side_col, (0.012, 0.012, 0.014, 1))
    col = mix(side_w, tile, side_col)
    glass = math("MULTIPLY", math("MULTIPLY", math("GREATER_THAN", Z, 1.08), math("SUBTRACT", 1.0, side_w)), math("LESS_THAN", sn.outputs[2], 0.93))
    col = mix(glass, col, (0.012, 0.012, 0.014, 1))
    wrap = sr.principled(nt, (0.2, 0.4, 0.38, 1), 0.34, 0.0)
    Lk(col, wrap.inputs["Base Color"])
    if "Coat Weight" in wrap.inputs:
        wrap.inputs["Coat Weight"].default_value = 0.35
    val = N.new("ShaderNodeValue")
    f = math("MINIMUM", math("MAXIMUM", math("DIVIDE", math("SUBTRACT", val.outputs[0], Y), 0.25), 0.0), 1.0)
    mx = N.new("ShaderNodeMixShader"); Lk(f, mx.inputs[0]); Lk(silver.outputs[0], mx.inputs[1]); Lk(wrap.outputs[0], mx.inputs[2])
    Lk(mx.outputs[0], out.inputs[0])
    sc = bpy.context.scene
    for fr in range(sc.frame_start, sc.frame_end + 1):
        t = (fr - 1) / fps
        ks = sweep_keys
        if t <= ks[0][0]: y = ks[0][1]
        elif t >= ks[-1][0]: y = ks[-1][1]
        else:
            for (t0, y0), (t1, y1) in zip(ks, ks[1:]):
                if t <= t1:
                    uu = (t - t0) / max(1e-9, t1 - t0); uu = uu * uu * (3 - 2 * uu); y = y0 + (y1 - y0) * uu; break
        val.outputs[0].default_value = y
        val.outputs[0].keyframe_insert("default_value", frame=fr)
    _MATS["livery"] = m
    return m


def main():
    spec = json.load(open(sys.argv[sys.argv.index("--") + 1]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    base = []
    groups = []  # (name, objs, hl keys) for highlight + label anchors
    base_mats = {}
    for b in spec["base"]:
        bb = b if isinstance(b, dict) else {"blend": b}
        objs = load_blend(bb["blend"])
        base += objs
        groups.append((bb.get("name"), objs, bb.get("hl")))
        base_mats[len(groups) - 1] = bb.get("mat")
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
    hl_all = spec.get("hl_all")
    global LED_KEYS, LED2_KEYS
    LED_KEYS = spec.get("led"); LED2_KEYS = spec.get("led2")
    liv = spec.get("livery")
    for gi, (name, objs, hl) in enumerate(groups):
        if base_mats.get(gi) == "livery":
            lm = mat_livery(liv["sweep"], fps)
            for o in objs:
                o.data.materials.clear(); o.data.materials.append(lm)
            continue
        m = grey if spec.get("base_color") == "grey" else (mat_hl(hl, hl_all, fps) if (hl or hl_all) else silver)
        for o in objs:
            o.data.materials.clear()
            o.data.materials.append(m)

    colors = {"red": (0.9, 0.05, 0.03), "cyan": (0.0, 0.7, 1.0), "green": (0.1, 0.9, 0.1),
              "yellow": (1.0, 0.8, 0.0), "magenta": (0.9, 0.0, 0.8)}
    for p in spec.get("parts", []):
        objs = load_blend(p["blend"])
        m = mat_check(colors[p["color"]]) if p.get("color") else (
            mat_hl(p.get("hl"), hl_all, fps) if (p.get("hl") or hl_all) else silver)
        groups.append((p.get("name"), objs, None))
        for o in objs:
            o.data.materials.clear()
            k = o.get("mat") or p.get("mat")
            o.data.materials.append(mat_livery(liv["sweep"], fps) if k == "livery" else (named_mat(k) if k else m))
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
        if len(keys) == 1:  # parked part: place it once, no animation data (keeps the scene static for persistent data)
            pv.location = base_loc + Vector(keys[0]["loc"])
            pv.rotation_euler = Euler([math.radians(v) for v in keys[0]["rot"]], "XYZ")
            continue
        for f in range(1, nframes + 1):
            t = (f - 1) / fps
            pv.location = base_loc + Vector(sample(keys, t, "loc"))
            pv.rotation_euler = Euler([math.radians(v) for v in sample(keys, t, "rot")], "XYZ")
            pv.keyframe_insert("location", frame=f)
            pv.keyframe_insert("rotation_euler", frame=f)

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
        q = (tgt - loc).to_track_quat("-Z", "Y")
        if any("roll" in kk for kk in ck):  # roll about the view axis (deg) - needed to end on a solved, tilted IRL camera
            from mathutils import Quaternion
            q = q @ Quaternion((0, 0, 1), math.radians(sample([dict(kk, roll=kk.get("roll", 0.0)) for kk in ck], t, "roll")))
        cam.rotation_euler = q.to_euler()
        cd.lens = sample(ck, t, "focal")
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.keyframe_insert("lens", frame=f)
    for fc in (cam.animation_data.action.fcurves if hasattr(cam.animation_data.action, "fcurves") else []):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

    w, h = (int(v) for v in spec.get("res", "1080x1920").split("x"))
    if spec.get("anchors_out"):  # per-frame screen position (0..1, y down) of each named group's bbox centre
        from bpy_extras.object_utils import world_to_camera_view
        sc.render.resolution_x, sc.render.resolution_y = w, h
        anchors = {}
        for f in range(1, nframes + 1):
            sc.frame_set(f)
            for name, objs, _ in groups:
                if not name:
                    continue
                pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
                c = sum(pts, Vector()) / len(pts)
                p2 = world_to_camera_view(sc, cam, c)
                anchors.setdefault(name, []).append([round(p2.x, 4), round(1 - p2.y, 4)])
        json.dump({"fps": fps, "anchors": anchors}, open(spec["anchors_out"], "w"))
        print("IVE_ANCHORS", spec["anchors_out"])
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = spec.get("res_pct", 75)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = spec.get("samples", 12)
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.render.use_persistent_data = spec.get("persistent", True)
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = spec.get("exposure", 0.0)
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
