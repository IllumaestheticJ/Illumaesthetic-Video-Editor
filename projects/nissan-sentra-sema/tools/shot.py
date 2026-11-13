"""Keyframed scan shot (from porsche-gt3rs-992/tools/shot.py) + Sentra additions:
  - camera keys may be {"t":..,"cam":"cam.json"} (solved camera: exact location/rotation/focal) and are slerped with loc/target keys
  - parts/base entries take "mat": silver|grey|dark|white|<colour name> and "visible": [t0, t1] (seconds)
  - base entries may be {"blend":..., "mat":..., "visible":...}
  - "livery": {"wipe": [t0, t1], "stripes": t2}: every mesh gets two vertex-colour layers (paint / paint + stripes) from
    position rules matched by eye to the finished car photos; the silver look is wiped to paint nose-to-tail between
    t0 and t1 and the red stripes switch on at t2. Entries may set "livery_group": "black" (vents, diffuser, wing mount).


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


def main():
    spec = json.load(open(sys.argv[sys.argv.index("--") + 1]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    base = []
    base_items = []
    for b in spec["base"]:
        b = {"blend": b} if isinstance(b, str) else b
        objs = load_blend(b["blend"])
        base += objs
        base_items.append((b, objs))
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
    def mat_plain(name, rgb, rough, metal):
        m, nt, out = sr.new_mat(name)
        p = sr.principled(nt, tuple(rgb) + (1,), rough)
        p.inputs["Metallic"].default_value = metal
        nt.links.new(p.outputs[0], out.inputs[0])
        return m
    mats = {"silver": silver, "grey": grey,
            "dark": mat_plain("ive_dark", (0.045, 0.047, 0.05), 0.55, 0.6),
            "white": mat_plain("ive_white", (0.82, 0.82, 0.80), 0.32, 0.0)}
    def set_mat(objs, item, default):
        m = mats.get(item.get("mat")) or (mat_check(colors[item["mat"]]) if item.get("mat") in colors else default)
        for o in objs:
            o.data.materials.clear()
            o.data.materials.append(m)
    def set_visible(objs, item):
        if not item.get("visible"):
            return
        t0, t1 = item["visible"]
        for f in range(1, nframes + 1):
            hid = not (t0 <= (f - 1) / fps < t1)
            for o in objs:
                o.hide_render = hid
                o.keyframe_insert("hide_render", frame=f)
    colors = {"red": (0.9, 0.05, 0.03), "cyan": (0.0, 0.7, 1.0), "green": (0.1, 0.9, 0.1),
              "yellow": (1.0, 0.8, 0.0), "magenta": (0.9, 0.0, 0.8)}
    for b, objs in base_items:
        set_mat(objs, b, grey if spec.get("base_color") == "grey" else silver)
        set_visible(objs, b)

    colors = {"red": (0.9, 0.05, 0.03), "cyan": (0.0, 0.7, 1.0), "green": (0.1, 0.9, 0.1),
              "yellow": (1.0, 0.8, 0.0), "magenta": (0.9, 0.0, 0.8)}
    for p in spec.get("parts", []):
        objs = load_blend(p["blend"])
        if p.get("color"):
            p["mat"] = p["color"]
        set_mat(objs, p, silver)
        set_visible(objs, p)
        for o in objs:
            o["livery_group"] = p.get("livery_group", "kit")
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

    if spec.get("livery"):
        import numpy as np
        L = spec["livery"]; bpy.context.view_layer.update()
        WHITE, BLACK, DARK, REDC = (0.80, 0.80, 0.78), (0.012, 0.012, 0.014), (0.03, 0.03, 0.035), (0.55, 0.02, 0.03)
        def bake(o, group):
            me = o.data; n = len(me.vertices); co = np.empty(n * 3, np.float32); me.vertices.foreach_get("co", co)
            M = np.array(o.matrix_world); w = co.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]; x, y, z = w[:, 0], w[:, 1], w[:, 2]
            c = np.tile(np.array(WHITE, np.float32), (n, 1))
            # v4 rules, measured on the Nov 12 side photo (152 px/m, front axle at y=1.41): see editlog
            c[(z > 1.00) & (y > -1.9) & (y < 0.9)] = BLACK                        # roof, pillars, glass
            c[(np.abs(x) > 0.85) & (z > 0.95) & (y > 0.45) & (y < 0.95)] = BLACK   # mirrors
            side = (np.abs(x) > 0.70) & (y > -1.75) & (y < 1.02)
            c[side & (z < 0.29)] = BLACK                                           # side skirts
            c[z < 0.185] = BLACK                                                   # splitter / underside
            if group == "kit":
                c[(z < 0.172) & (y > 1.0)] = REDC                                  # red edge of the splitter
                c[side & (z < 0.185)] = REDC                                       # red line under the skirts
            if group == "black": c[:] = BLACK
            wheel = (np.abs(x) > 0.55) & (((y - 1.41) ** 2 + (z - 0.33) ** 2 < 0.37 ** 2) | ((y + 1.30) ** 2 + (z - 0.33) ** 2 < 0.37 ** 2))
            if group != "kit": c[wheel] = DARK
            c2 = c.copy(); u = y - 1.16 * (z - 0.30)      # stripes lean FORWARD at the top (about 49 deg), sill to mid-door
            st = (np.abs(x) > 0.78) & (z > 0.29) & (z < 0.76) & (((u > 0.16) & (u < 0.42)) | ((u > -0.12) & (u < 0.11))) & ~wheel
            if group != "black": c2[st] = REDC
            for name, arr in (("paint", c), ("paint2", c2)):
                a = me.color_attributes.new(name, "FLOAT_COLOR", "POINT")
                a.data.foreach_set("color", np.concatenate([arr, np.ones((n, 1), np.float32)], 1).ravel())
        m, nt, out = sr.new_mat("ive_livery")
        N = nt.nodes.new; lk = nt.links.new
        sil = sr.principled(nt, (0.62, 0.63, 0.66, 1), 0.32, 0.85)
        pa = sr.principled(nt, (1, 1, 1, 1), 0.22, 0.0)
        a1 = N("ShaderNodeAttribute"); a1.attribute_name = "paint"; a2 = N("ShaderNodeAttribute"); a2.attribute_name = "paint2"
        vs = N("ShaderNodeValue"); vs.label = "stripes"; mixc = N("ShaderNodeMix"); mixc.data_type = "RGBA"
        lk(vs.outputs[0], mixc.inputs[0]); lk(a1.outputs["Color"], mixc.inputs[6]); lk(a2.outputs["Color"], mixc.inputs[7])
        lk(mixc.outputs[2], pa.inputs["Base Color"])
        bw = N("ShaderNodeRGBToBW"); lk(mixc.outputs[2], bw.inputs[0])      # dark paint: rougher, so black reads black under the studio lights
        m1 = N("ShaderNodeMath"); m1.operation = "MULTIPLY"; m1.use_clamp = True; m1.inputs[1].default_value = 6.0; lk(bw.outputs[0], m1.inputs[0])
        m2 = N("ShaderNodeMath"); m2.operation = "MULTIPLY_ADD"; m2.inputs[1].default_value = -0.38; m2.inputs[2].default_value = 0.62; lk(m1.outputs[0], m2.inputs[0])
        lk(m2.outputs[0], pa.inputs["Roughness"])
        geo = N("ShaderNodeNewGeometry"); sep = N("ShaderNodeSeparateXYZ"); lk(geo.outputs["Position"], sep.inputs[0])
        vw = N("ShaderNodeValue"); vw.label = "wipe_y"; gt = N("ShaderNodeMath"); gt.operation = "GREATER_THAN"
        lk(sep.outputs["Y"], gt.inputs[0]); lk(vw.outputs[0], gt.inputs[1])
        ms = N("ShaderNodeMixShader"); lk(gt.outputs[0], ms.inputs[0]); lk(sil.outputs[0], ms.inputs[1]); lk(pa.outputs[0], ms.inputs[2])
        lk(ms.outputs[0], out.inputs[0])
        for f in range(1, nframes + 1):
            t = (f - 1) / fps; u = min(1.0, max(0.0, (t - L["wipe"][0]) / (L["wipe"][1] - L["wipe"][0])))
            vw.outputs[0].default_value = 3.0 - 6.0 * (u * u * (3 - 2 * u)); vw.outputs[0].keyframe_insert("default_value", frame=f)
            vs.outputs[0].default_value = 1.0 if t >= L["stripes"] else 0.0; vs.outputs[0].keyframe_insert("default_value", frame=f)
        for o in [o for o in sc.objects if o.type == "MESH"]:
            bake(o, o.get("livery_group", "car")); o.data.materials.clear(); o.data.materials.append(m)

    cd = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.sensor_fit = "HORIZONTAL"
    cd.sensor_width = spec["camera"].get("sensor", 20.25)
    cd.clip_start = 0.01
    ck = spec["camera"]["keys"]
    for k in ck:  # normalise every key to loc / quat / focal
        if k.get("cam"):
            cj = json.load(open(k["cam"]))
            k["loc"] = list(cj["blender"]["location"])
            k["_q"] = Matrix(cj["blender"]["rotation_matrix"]).to_quaternion()
            k.setdefault("focal", cj["focal_mm"])
        else:
            k["_q"] = (Vector(k["target"]) - Vector(k["loc"])).to_track_quat("-Z", "Y")
    def cam_at(t):
        if t <= ck[0]["t"]:
            return Vector(ck[0]["loc"]), ck[0]["_q"], ck[0]["focal"]
        for a, b in zip(ck, ck[1:]):
            if t <= b["t"]:
                u = ease((t - a["t"]) / max(1e-9, b["t"] - a["t"]), b.get("ease", "inout"))
                return Vector(a["loc"]).lerp(Vector(b["loc"]), u), a["_q"].slerp(b["_q"], u), a["focal"] + (b["focal"] - a["focal"]) * u
        return Vector(ck[-1]["loc"]), ck[-1]["_q"], ck[-1]["focal"]
    cam.rotation_mode = "QUATERNION"
    for f in range(1, nframes + 1):
        t = (f - 1) / fps
        loc, q, fl = cam_at(t)
        cam.location = loc
        cam.rotation_quaternion = q
        cd.lens = fl
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_quaternion", frame=f)
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
    sc.render.use_persistent_data = bool(spec.get("persist", False))  # off by default: persistent data dropped the lights mid-animation on sibling reels
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
        sc.render.use_overwrite = False  # resume: skip frames already on disk (container restarts kill long queues)
        bpy.ops.render.render(animation=True)
    print("IVE_RENDER_DONE", out)


main()
