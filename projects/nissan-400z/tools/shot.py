"""Keyframed scan shot for the Ferrari 296 reel (Temerario style).

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
    if isinstance(path, dict):
        path = path["blend"]
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


_LIV = {}


def mat_livery(spec, fps, nframes):
    """Bomex x Kaido House wrap (tools/livery_tex.py, livery_fit.py): grey paint; PSD side view projected along X onto
    side-facing surfaces (driver +X as drawn, passenger with text pre-mirrored); dark side glass from the PSD render;
    BOMEX hood block projected along Z; dark windscreen/rear glass by height + normal. Revealed where world y > sweep
    (keyed hard-edged wipe from the tail forward) over house silver; sweep keys [[t, y], ...]."""
    if "m" in _LIV:
        return _LIV["m"]
    L = spec["livery"]; T = L["tex"]; M = L["map"]
    m = sr.mat_silver(); nt = m.node_tree; N = nt.nodes; Lk = nt.links.new
    out = [n for n in N if n.type == "OUTPUT_MATERIAL"][0]
    silver = out.inputs[0].links[0].from_node
    geo = N.new("ShaderNodeNewGeometry")
    sp = N.new("ShaderNodeSeparateXYZ"); Lk(geo.outputs["Position"], sp.inputs[0])
    sn = N.new("ShaderNodeSeparateXYZ"); Lk(geo.outputs["Normal"], sn.inputs[0])

    def math(op, a, b=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        for i, v in enumerate((a, b)):
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

    def img(name, v):
        n = N.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(os.path.join(T, name)); n.extension = "CLIP"
        Lk(v, n.inputs[0]); return n

    def mix(f, a, b):
        n = N.new("ShaderNodeMix"); n.data_type = "RGBA"
        for k, v in (("Factor", f), ("A", a), ("B", b)):
            if isinstance(v, (int, float)): n.inputs[k].default_value = v
            elif isinstance(v, tuple): n.inputs[k].default_value = v
            else: Lk(v, n.inputs[k])
        return n.outputs["Result"]
    X, Y, Z = sp.outputs
    nx, ny, nz = (math("ABSOLUTE", o) for o in sn.outputs)
    uv = vec(math("DIVIDE", math("SUBTRACT", Y, M["Y0"]), M["LEN"]), math("DIVIDE", math("SUBTRACT", Z, M["Z0"]), M["HGT"]))
    il, ir, ig = img("side_left.png", uv), img("side_right.png", uv), img("glass.png", uv)
    is_r = math("LESS_THAN", X, L.get("xc", -0.07))
    side = mix(is_r, il.outputs["Color"], ir.outputs["Color"])
    side_a = math("ADD", math("MULTIPLY", il.outputs["Alpha"], math("SUBTRACT", 1.0, is_r)), math("MULTIPLY", ir.outputs["Alpha"], is_r))
    side_w = math("GREATER_THAN", nx, 0.45)
    paint = tuple(L.get("paint", (0.20, 0.21, 0.22))) + (1,)
    dark = tuple(L.get("dark", (0.010, 0.010, 0.012))) + (1,)
    col = mix(math("MULTIPLY", side_w, side_a), paint, side)
    col = mix(math("MULTIPLY", side_w, math("GREATER_THAN", ig.outputs["Alpha"], 0.5)), col, dark)
    H = L["hood"]  # x centre, y top (rear edge), width, height (m); text reads from the front, top toward the screen
    hu = math("ADD", math("DIVIDE", math("SUBTRACT", X, H[0]), H[2]), 0.5)
    hv = math("DIVIDE", math("SUBTRACT", Y, H[1] - H[3]), H[3])
    ih = img("hood.png", vec(hu, hv))
    top_w = math("MULTIPLY", math("GREATER_THAN", nz, 0.55), math("LESS_THAN", Y, H[1] + 0.05))
    col = mix(math("MULTIPLY", top_w, ih.outputs["Alpha"]), col, ih.outputs["Color"])
    glass = math("MULTIPLY", math("MULTIPLY", math("GREATER_THAN", Z, L.get("belt", 1.0)), math("SUBTRACT", 1.0, side_w)),
                 math("LESS_THAN", nz, L.get("glass_nz", 0.95)))
    # cabin seen through the (unscanned) glass: dash/seats inside the body sides, below the roof skin
    C = L.get("cabin", [-0.75, 1.0, 0.80, 1.18, 0.65])  # y0, y1, z0, z1, half-width about xc
    cab = math("MULTIPLY", math("MULTIPLY", math("GREATER_THAN", Y, C[0]), math("LESS_THAN", Y, C[1])),
               math("MULTIPLY", math("MULTIPLY", math("GREATER_THAN", Z, C[2]), math("LESS_THAN", Z, C[3])),
                    math("LESS_THAN", math("ABSOLUTE", math("SUBTRACT", X, L.get("xc", -0.07))), C[4])))
    glass = math("MAXIMUM", glass, cab)
    col = mix(glass, col, dark)
    # windscreen banner (KAIDO*HOUSE), projected along Y onto the top band of the windscreen
    BN = L.get("banner")  # [x centre, width, z bottom, z height, y min, y max]
    ban_w = None
    if BN:
        bu = math("ADD", math("DIVIDE", math("SUBTRACT", X, BN[0]), BN[1]), 0.5)
        bv = math("DIVIDE", math("SUBTRACT", Z, BN[2]), BN[3])
        ib = img("banner.png", vec(bu, bv))
        sel = math("MULTIPLY", math("MULTIPLY", math("GREATER_THAN", Y, BN[4]), math("LESS_THAN", Y, BN[5])),
                   math("MULTIPLY", math("GREATER_THAN", ny, 0.25), math("LESS_THAN", nx, 0.6)))
        ban_w = math("MULTIPLY", sel, math("GREATER_THAN", ib.outputs["Alpha"], 0.5))
        col = mix(ban_w, col, (0.92, 0.92, 0.92, 1))
    wrap = sr.principled(nt, (0.2, 0.2, 0.2, 1), 0.38, 0.0)
    Lk(col, wrap.inputs["Base Color"])
    if "Coat Weight" in wrap.inputs:
        wrap.inputs["Coat Weight"].default_value = 0.3
    # glass: low-specular dark (a glossy dark windscreen mirrors the studio top light and reads white)
    gb = N.new("ShaderNodeBsdfDiffuse"); gb.inputs["Color"].default_value = dark  # no Fresnel sheen
    gsel = math("MAXIMUM", glass, math("MULTIPLY", side_w, math("GREATER_THAN", ig.outputs["Alpha"], 0.5)))
    if ban_w is not None:
        gsel = math("MULTIPLY", gsel, math("SUBTRACT", 1.0, ban_w))
    wm = N.new("ShaderNodeMixShader"); Lk(gsel, wm.inputs[0]); Lk(wrap.outputs[0], wm.inputs[1]); Lk(gb.outputs[0], wm.inputs[2])
    wrap = wm
    val = N.new("ShaderNodeValue")
    f = math("MINIMUM", math("MAXIMUM", math("DIVIDE", math("SUBTRACT", Y, val.outputs[0]), 0.02), 0.0), 1.0)
    mx = N.new("ShaderNodeMixShader"); Lk(f, mx.inputs[0]); Lk(silver.outputs[0], mx.inputs[1]); Lk(wrap.outputs[0], mx.inputs[2])
    Lk(mx.outputs[0], out.inputs[0])
    ks = L.get("sweep", [[0, -9.0]])
    for fr in range(1, nframes + 1):
        t = (fr - 1) / fps
        if t <= ks[0][0]: y = ks[0][1]
        elif t >= ks[-1][0]: y = ks[-1][1]
        else:
            for (t0, y0), (t1, y1) in zip(ks, ks[1:]):
                if t <= t1:
                    uu = (t - t0) / max(1e-9, t1 - t0); uu = uu * uu * (3 - 2 * uu); y = y0 + (y1 - y0) * uu; break
        val.outputs[0].default_value = y
        val.outputs[0].keyframe_insert("default_value", frame=fr)
    _LIV["m"] = m
    return m


def key_vis(objs, e, fps):
    """entry keys show_at / hide_at (s): hard visibility switches on those frames (1:1 swaps on a beat); both may be set."""
    if e.get("show_at") is None and e.get("hide_at") is None:
        return
    f_on = max(1, int(round(e["show_at"] * fps)) + 1) if e.get("show_at") is not None else 1
    f_off = max(1, int(round(e["hide_at"] * fps)) + 1) if e.get("hide_at") is not None else None
    for o in objs:
        o.hide_render = f_on > 1; o.keyframe_insert("hide_render", frame=1)
        if f_on > 1:
            o.hide_render = False; o.keyframe_insert("hide_render", frame=f_on)
        if f_off is not None:
            o.hide_render = True; o.keyframe_insert("hide_render", frame=f_off)


def main():
    spec = json.load(open(sys.argv[sys.argv.index("--") + 1]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    base = []
    body_roots = []  # roots that ride the body (stance drop); entries with "ground": true stay on the ground
    base_objs = []  # (objs, entry) for per-entry material/hide
    for b in spec["base"]:
        objs = load_blend(b)
        base += objs
        base_objs.append((objs, b if isinstance(b, dict) else {}))
        if not (isinstance(b, dict) and b.get("ground")):
            body_roots += list({(o.parent or o) for o in objs})
    bpy.context.view_layer.update()  # matrix_world is stale right after linking
    lo, hi = sr.bbox([o for objs, e in base_objs if not e.get("hide") for o in objs] or base)
    fps = spec.get("fps", 15)
    secs = spec.get("seconds", 0)
    nframes = max(1, int(round(secs * fps)))
    sc.render.fps = int(fps)
    sc.frame_start, sc.frame_end = 1, nframes

    sr.studio_world(sr.rgb(spec.get("bg", "0.004,0.004,0.005")), False)
    sr.studio_lights(lo, hi)
    silver = sr.mat_silver()
    grey = sr.mat_clay()
    liv_all = bool(spec.get("livery"))
    base_mat = (lambda: mat_livery(spec, fps, nframes)) if liv_all else (lambda: grey if spec.get("base_color") == "grey" else silver)
    swap_objs = []
    for objs, e in base_objs:
        for o in objs:
            if not e.get("keep_mats"):
                o.data.materials.clear(); o.data.materials.append(base_mat())
            if e.get("hide"):
                o.hide_render = True
        key_vis(objs, e, fps)
    for sh in spec.get("show", []):  # extra static silver meshes (e.g. the bumper shell alone)
        for o in load_blend(sh):
            o.data.materials.clear(); o.data.materials.append(silver); swap_objs.append(o)
    sw = spec.get("swap")  # hard 1:1 state swap at t: base hidden, swap mesh shown, on a beat (no dissolve)
    if sw:
        fcut = max(1, int(round(sw["t"] * fps)) + 1)
        swobjs = load_blend(sw["blend"])
        for o in swobjs:
            o.data.materials.clear(); o.data.materials.append(base_mat())
            o.hide_render = True
            o.keyframe_insert("hide_render", frame=1)
            o.hide_render = False; o.keyframe_insert("hide_render", frame=fcut)
        for objs, e in base_objs:
            if e.get("swapout", True) and not e.get("hide") and e.get("show_at") is None and e.get("hide_at") is None:
                for o in objs:
                    o.hide_render = False; o.keyframe_insert("hide_render", frame=1)
                    o.hide_render = True; o.keyframe_insert("hide_render", frame=fcut)

    colors = {"red": (0.9, 0.05, 0.03), "cyan": (0.0, 0.7, 1.0), "green": (0.1, 0.9, 0.1),
              "yellow": (1.0, 0.8, 0.0), "magenta": (0.9, 0.0, 0.8)}
    for p in spec.get("parts", []):
        objs = load_blend(p["blend"])
        if not p.get("ground") and not p.get("keys"):
            body_roots += list({(o.parent or o) for o in objs})
        m = mat_check(colors[p["color"]]) if p.get("color") else (mat_livery(spec, fps, nframes) if liv_all else silver)
        for o in objs:
            if p.get("keep_mats"):
                continue
            o.data.materials.clear()
            o.data.materials.append(m)
        key_vis(objs, p, fps)
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
        if not p.get("ground"):
            body_roots.append(pv)
        base_loc = pv.location.copy()
        for f in range(1, nframes + 1):
            t = (f - 1) / fps
            pv.location = base_loc + Vector(sample(keys, t, "loc"))
            pv.rotation_euler = Euler([math.radians(v) for v in sample(keys, t, "rot")], "XYZ")
            pv.keyframe_insert("location", frame=f)
            pv.keyframe_insert("rotation_euler", frame=f)

    bd = spec.get("body_drop")  # stance: [[t, dz], ...] (m) for everything but "ground" entries (new wheels)
    if bd:
        body = bpy.data.objects.new("body", None); sc.collection.objects.link(body)
        for r in body_roots:
            if r.parent is None:
                mw = r.matrix_world.copy(); r.parent = body; r.matrix_world = mw
        for f in range(1, nframes + 1):
            t = (f - 1) / fps
            if t <= bd[0][0]: dz = bd[0][1]
            elif t >= bd[-1][0]: dz = bd[-1][1]
            else:
                for (t0, z0), (t1, z1) in zip(bd, bd[1:]):
                    if t <= t1:
                        u = (t - t0) / max(1e-9, t1 - t0); u = u * u * (3 - 2 * u); dz = z0 + (z1 - z0) * u; break
            body.location = (0, 0, dz); body.keyframe_insert("location", frame=f)

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
    sc.render.use_persistent_data = bool(spec.get("persist", False))  # off: persistent data dropped the lights in s8a f30-51 (and WRX VA)
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
        if spec.get("frame_range"):  # re-render a slice (fresh process); see editlog: persistent data broke after 48 frames
            sc.frame_start, sc.frame_end = spec["frame_range"]
        sc.render.filepath = os.path.join(out, "f_")
        bpy.ops.render.render(animation=True)
    print("IVE_RENDER_DONE", out)


main()
