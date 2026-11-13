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


MAT_OVERRIDE, MAT_SPEC = {}, {}  # spec["paint_mat"] = {name: [rough, metal, specular]} (v8: deep red body)


def mat_paint(rgb, name, red=None, reveal=None, fps=15):
    """Per-part colour (v7, user: "re-render with all scans in a different color", each part its own colour - like the
    listing's explode photos): satin paint with the same AO multiply as the silver so scan detail still reads."""
    m, nt, out = sr.new_mat(f"ive_paint_{name}")
    c = tuple(rgb) + (1,)
    p = sr.principled(nt, c, *(MAT_OVERRIDE.get(name) or (0.38, 0.25)))
    if MAT_SPEC.get(name) is not None:
        p.inputs["Specular IOR Level"].default_value = MAT_SPEC[name]
    ao = nt.nodes.new("ShaderNodeAmbientOcclusion")
    ao.inputs["Distance"].default_value = 0.08
    ao.inputs["Color"].default_value = (1, 1, 1, 1)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 0.85
    mul.inputs["A"].default_value = c
    if red is not None and reveal is not None and reveal > -1e8:
        # v8: starts as the body red, turns to its own colour over 0.3 s when the part first leaves home
        f0 = 1 + reveal * fps
        mul.inputs["A"].default_value = tuple(red) + (1,)
        mul.inputs["A"].keyframe_insert("default_value", frame=f0)
        mul.inputs["A"].default_value = c
        mul.inputs["A"].keyframe_insert("default_value", frame=f0 + 0.3 * fps)
    elif red is not None and reveal is None:
        mul.inputs["A"].default_value = tuple(red) + (1,)
    nt.links.new(ao.outputs["Color"], mul.inputs["B"])
    nt.links.new(mul.outputs["Result"], p.inputs["Base Color"])
    nt.links.new(p.outputs[0], out.inputs[0])
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
    paint = spec.get("paint") or {}
    for k, v in (spec.get("paint_mat") or {}).items():
        MAT_OVERRIDE[k], MAT_SPEC[k] = (v[0], v[1]), (v[2] if len(v) > 2 else None)
    body = mat_paint(paint["base"], "base") if "base" in paint else None
    for o in base:
        o.data.materials.clear()
        o.data.materials.append(body or (grey if spec.get("base_color") == "grey" else silver))

    colors = {"red": (0.9, 0.05, 0.03), "cyan": (0.0, 0.7, 1.0), "green": (0.1, 0.9, 0.1),
              "yellow": (1.0, 0.8, 0.0), "magenta": (0.9, 0.0, 0.8)}
    for p in spec.get("parts", []):
        objs = load_blend(p["blend"])
        stem = os.path.splitext(os.path.basename(p["blend"]))[0]
        rv = paint.get("reveal")
        if p.get("color"):
            m = mat_check(colors[p["color"]])
        elif stem in paint:
            m = (mat_paint(paint[stem], stem, paint["base"], rv.get(stem), fps) if rv is not None else mat_paint(paint[stem], stem))
        else:
            m = silver
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

    w, h = (int(v) for v in spec.get("res", "1080x1920").split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = spec.get("res_pct", 75)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = spec.get("samples", 12)
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.render.use_persistent_data = bool(spec.get("persist", False))  # off: lighting dropped out mid-animation (lessons)
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = spec.get("look", "None")
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
        if spec.get("frame_range"):  # re-render a slice (fresh process); see editlog: persistent data broke after 48 frames
            sc.frame_start, sc.frame_end = spec["frame_range"]
        sc.render.filepath = os.path.join(out, "f_")
        bpy.ops.render.render(animation=True)
    print("IVE_RENDER_DONE", out)


main()
