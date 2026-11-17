"""Keyframed scan shot for the GR Corolla reel (copied from projects/ferrari-296/tools/shot.py) (Temerario style).

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


def mat_livery():
    """Silver house look where the face has no livery (attribute alpha 0); gloss paint in the 'livery' colour elsewhere
    (Castrol livery transferred from the website model, livery.py / livery_attr.py)."""
    m, nt, out = sr.new_mat("ive_livery")
    silver = sr.principled(nt, (0.62, 0.63, 0.66, 1), 0.32, 0.85)
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.08
    ao.inputs["Color"].default_value = (1, 1, 1, 1)
    mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 0.85; mul.inputs["A"].default_value = (0.62, 0.63, 0.66, 1)
    nt.links.new(ao.outputs["Color"], mul.inputs["B"]); nt.links.new(mul.outputs["Result"], silver.inputs["Base Color"])
    att = nt.nodes.new("ShaderNodeAttribute"); att.attribute_name = "livery"
    paint = sr.principled(nt, (0.8, 0.8, 0.8, 1), 0.28, 0.0)
    if "Coat Weight" in paint.inputs:
        paint.inputs["Coat Weight"].default_value = 0.6
    nt.links.new(att.outputs["Color"], paint.inputs["Base Color"])
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(att.outputs["Alpha"], mix.inputs[0])
    nt.links.new(silver.outputs[0], mix.inputs[1]); nt.links.new(paint.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


CLASS_LOOK = {  # game-model surfaces (website eps-toyota-gr-corolla-v23.glb + game-model render wheels): rgb, rough, metal, emit
    "glass": ((0.015, 0.017, 0.02), 0.03, 0.0, 0), "glass_tint": ((0.008, 0.008, 0.01), 0.03, 0.0, 0),
    "light_inner": ((0.75, 0.76, 0.78), 0.15, 1.0, 0), "plastic_gloss": ((0.01, 0.01, 0.01), 0.15, 0.0, 0),
    "plastic_black": ((0.03, 0.03, 0.03), 0.55, 0.0, 0), "grille": ((0.02, 0.02, 0.02), 0.4, 0.2, 0),
    "light_lens": ((0.6, 0.62, 0.66), 0.04, 0.3, 0), "light_red": ((0.45, 0.01, 0.01), 0.1, 0.0, 1.5),
    "chrome": ((0.9, 0.9, 0.9), 0.08, 1.0, 0), "light_amber": ((0.9, 0.4, 0.02), 0.1, 0.0, 0.8),
    "underbody": ((0.02, 0.02, 0.02), 0.9, 0.0, 0), "mirror_glass": ((0.8, 0.8, 0.82), 0.02, 1.0, 0),
    "w_tyre": ((0.025, 0.025, 0.025), 0.6, 0.0, 0), "w_caliper": ((0.64, 0.8, 0.03), 0.12, 0.06, 0),
    "w_hub": ((0.02, 0.02, 0.02), 0.5, 0.0, 0), "w_metal": ((0.8, 0.8, 0.8), 0.15, 1.0, 0),
    "w_chrome": ((1.0, 1.0, 1.0), 0.15, 1.0, 0), "w_blue": ((0.0, 0.0, 1.0), 0.15, 0.0, 0),
    "w_white": ((0.9, 0.9, 0.9), 0.07, 0.0, 0), "w_rimpaint": ((0.88, 0.88, 0.88), 0.25, 0.0, 0),
    "w_glass": ((0.02, 0.02, 0.02), 0.05, 0.0, 0), "w_titanium": ((0.27, 0.31, 0.37), 0.7, 1.0, 0),
}


def mat_class(name):
    if name == "silver":
        return sr.mat_silver()
    if name == "paint":
        return mat_paint()
    rgb, rough, metal, emit = CLASS_LOOK[name]
    m, nt, out = sr.new_mat("cls_" + name)
    p = sr.principled(nt, rgb + (1,), rough, metal)
    if emit:
        p.inputs["Emission Color"].default_value = rgb + (1,)
        p.inputs["Emission Strength"].default_value = emit
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


def mat_paint():
    """Livery paint revealed like vinyl tape going on (user v13): wipe position W (world y, keyed per frame on the shared
    Value node) sweeps front -> rear; each 10 cm horizontal strip starts with its own delay (hash of the strip index), so
    strips are laid one by one with a crisp edge. Before the tape: house silver."""
    m, nt, out = sr.new_mat("ive_paint_tape")
    silver = sr.principled(nt, (0.62, 0.63, 0.66, 1), 0.32, 0.85)
    paint = sr.principled(nt, (0.8, 0.8, 0.8, 1), 0.28, 0.0)
    if "Coat Weight" in paint.inputs:
        paint.inputs["Coat Weight"].default_value = 0.6
    att = nt.nodes.new("ShaderNodeAttribute"); att.attribute_name = "livery"
    nt.links.new(att.outputs["Color"], paint.inputs["Base Color"])
    tape_node = nt.nodes.new("ShaderNodeValue"); tape_node.name = "tape_wipe"; tape_node.outputs[0].default_value = 10.0
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    def math(op, a, b=None, v=None):
        n = nt.nodes.new("ShaderNodeMath"); n.operation = op
        for i, x in enumerate((a, b)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = x
            else:
                nt.links.new(x, n.inputs[i])
        return n.outputs[0]
    band = math("FLOOR", math("DIVIDE", sep.outputs["Z"], 0.10))
    h = math("FRACT", math("MULTIPLY", math("SINE", math("MULTIPLY", band, 12.9898)), 43758.5453))
    delay = math("MULTIPLY", h, 0.9)
    edge = math("SUBTRACT", math("SUBTRACT", tape_node.outputs[0], sep.outputs["Y"]), delay)
    reveal = math("MINIMUM", math("MAXIMUM", math("DIVIDE", edge, 0.012), 0.0), 1.0)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(reveal, mix.inputs[0]); nt.links.new(silver.outputs[0], mix.inputs[1]); nt.links.new(paint.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
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
    livery = mat_livery()
    class_mats = {}
    for o in base:
        names = [mt.name for mt in o.data.materials if mt]
        if names and all(n.startswith("cls_") for n in names):   # per-face surface classes (class_attr.py)
            for i, n in enumerate(names):
                cn = n.split(".")[0][4:]
                if cn not in class_mats:
                    class_mats[cn] = mat_class(cn)
                o.data.materials[i] = class_mats[cn]
            continue
        o.data.materials.clear()
        if "livery" in o.data.attributes:
            o.data.materials.append(livery)
        else:
            o.data.materials.append(grey if spec.get("base_color") == "grey" else silver)

    colors = {"red": (0.9, 0.05, 0.03), "cyan": (0.0, 0.7, 1.0), "green": (0.1, 0.9, 0.1),
              "yellow": (1.0, 0.8, 0.0), "magenta": (0.9, 0.0, 0.8)}
    for p in spec.get("parts", []):
        objs = load_blend(p["blend"])
        m = mat_check(colors[p["color"]]) if p.get("color") else silver
        for o in objs:
            o.data.materials.clear()
            o.data.materials.append(m)
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

    if spec.get("tape") and "paint" in class_mats:   # livery taped on: wipe position (world y) per frame
        tn = class_mats["paint"].node_tree.nodes["tape_wipe"]
        for f in range(1, nframes + 1):
            tn.outputs[0].default_value = sample(spec["tape"], (f - 1) / fps, "v")
            tn.outputs[0].keyframe_insert("default_value", frame=f)

    w, h = (int(v) for v in spec.get("res", "1080x1920").split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = spec.get("res_pct", 75)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = spec.get("samples", 12)
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    # persistent data off whenever parts move: long animated renders went black mid-shot with it on (GR Corolla s8,
    # Miata s8); spec "persistent": true/false overrides
    moving = any(len(p.get("keys") or []) > 1 for p in spec.get("parts", []))
    sc.render.use_persistent_data = bool(spec.get("persistent", not moving))
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
