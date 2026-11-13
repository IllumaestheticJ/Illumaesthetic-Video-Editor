"""Keyframed scan shot (from projects/lexus-is350/tools/shot.py, itself from ferrari-296), extended for the
Smart 450 short and the IS350 long-form scan shots (2026-11-12):
  - camera keys may start from a SOLVED camera json ("cam": path) -> exact 1:1 start pose incl. roll + lens shift
  - per-key "roll" (deg about the view axis), constant "shift_x"/"shift_y" (fraction of image WIDTH, sensor_fit HORIZONTAL)
  - base items may carry a visibility window {"blend": ..., "vis": [t0, t1]} (seconds) -> same-camera STATE SWAP
  - "light_bbox": [[x0,y0,z0],[x1,y1,z1]] pins the studio rig so a state swap doesn't relight the car
  - "transparent": true -> RGBA PNG with alpha (film transparent)
  - per-item "look": "silver" (default) | "wire" (silver + dark wireframe edges, mesh-density beat)
  - persistent data always OFF (lighting-dropout lessons)

    blender -b -P projects/smart-450-hellkitten/tools/shot.py -- spec.json

spec.json:
{ "base": ["car.blend" | {"blend": "x.blend", "vis": [t0, t1], "look": "wire"}, ...],
  "camera": {"keys": [{"t":0, "cam": "solved.json"} | {"t":0, "loc":[..], "target":[..], "focal":30, "roll":0, "ease":"inout"}, ...],
             "sensor": 36, "shift_x": 0, "shift_y": 0},
  "seconds": 4, "fps": 15, "res": "1080x1920", "res_pct": 100, "samples": 16,
  "out": "dir/ or still.png", "frames": [..optional subset..], "transparent": false }
A key with "cam" uses that camera's loc/forward/roll/focal (focal converted to the spec sensor); later keys interpolate
from it. Times are seconds; frame f renders t=(f-1)/fps.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Euler, Matrix, Vector

sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/blender")
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
    return t * t * (3 - 2 * t)


def sample(keys, t, field, default=None):
    if t <= keys[0]["t"]:
        return keys[0].get(field, default)
    for a, b in zip(keys, keys[1:]):
        if t <= b["t"]:
            u = (t - a["t"]) / max(1e-9, b["t"] - a["t"])
            k = ease(u, b.get("ease", "inout"))
            va, vb = a.get(field, default), b.get(field, default)
            if isinstance(va, (int, float)):
                return va + (vb - va) * k
            return [x + (y - x) * k for x, y in zip(va, vb)]
    return keys[-1].get(field, default)


def track_rot(loc, tgt, roll_deg):
    q = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y")
    R = q.to_matrix()
    if roll_deg:
        R = R @ Matrix.Rotation(math.radians(roll_deg), 3, "Z")
    return R


def key_from_cam(k, sensor):
    """Turn {"cam": solved.json} into loc/target/roll/focal (focal rescaled to this spec's sensor)."""
    c = json.load(open(k["cam"]))
    R = Matrix(c["blender"]["rotation_matrix"])
    loc = Vector(c["blender"]["location"])
    fwd = -(R @ Vector((0, 0, 1)))
    tgt = loc + fwd * k.get("dist", 3.0)
    R0 = track_rot(loc, tgt, 0)
    up0, up = R0 @ Vector((0, 1, 0)), R @ Vector((0, 1, 0))
    roll = math.degrees(math.atan2(fwd.dot(up0.cross(up)) * -1, up0.dot(up)))
    # sign check: rebuild and pick the sign that reproduces up
    for r in (roll, -roll):
        if (track_rot(loc, tgt, r) @ Vector((0, 1, 0)) - up).length < 1e-4:
            roll = r
            break
    out = dict(k)
    out.update({"loc": list(loc), "target": list(tgt), "roll": roll,
                "focal": c["focal_mm"] * sensor / c["sensor_width_mm"]})
    out.pop("cam")
    return out, c


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


def mat_wire_silver():
    """Silver with dark wireframe edges: the triangles of the scan read as a mesh."""
    m, nt, out = sr.new_mat("ive_wiresilver")
    p = sr.principled(nt, (0.62, 0.63, 0.66, 1), 0.35, 0.8)
    dark = sr.principled(nt, (0.01, 0.012, 0.015, 1), 0.6, 0.0)
    wf = nt.nodes.new("ShaderNodeWireframe")
    wf.use_pixel_size = True
    wf.inputs["Size"].default_value = 0.9
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(wf.outputs[0], mix.inputs[0])
    nt.links.new(p.outputs[0], mix.inputs[1])
    nt.links.new(dark.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


def main():
    spec = json.load(open(sys.argv[sys.argv.index("--") + 1]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    fps = spec.get("fps", 15)
    secs = spec.get("seconds", 0)
    nframes = max(1, int(round(secs * fps)))
    sc.render.fps = int(round(fps))
    sc.render.fps_base = sc.render.fps / fps
    sc.frame_start, sc.frame_end = 1, nframes

    silver = sr.mat_silver()
    wire = None
    allobjs = []
    for b in spec["base"]:
        item = {"blend": b} if isinstance(b, str) else b
        objs = load_blend(item["blend"])
        if item.get("look") == "wire":
            wire = wire or mat_wire_silver()
        for o in objs:
            o.data.materials.clear()
            o.data.materials.append(wire if item.get("look") == "wire" else silver)
            if item.get("vis"):
                t0, t1 = item["vis"]
                for f in range(1, nframes + 1):
                    t = (f - 1) / fps
                    hid = not (t0 <= t < t1)
                    o.hide_render = hid
                    o.keyframe_insert("hide_render", frame=f)
        allobjs += objs
    bpy.context.view_layer.update()
    if spec.get("light_bbox"):
        lo, hi = Vector(spec["light_bbox"][0]), Vector(spec["light_bbox"][1])
    else:
        lo, hi = sr.bbox(allobjs)
    transparent = bool(spec.get("transparent"))
    sr.studio_world(sr.rgb(spec.get("bg", "0.004,0.004,0.005")) if not transparent else (0, 0, 0, 1), transparent)
    root = bpy.data.objects.new("SCAN_ROOT", None)  # light track target = rig centre
    sc.collection.objects.link(root)
    root.location = (lo + hi) / 2
    sr.studio_lights(lo, hi)

    cd = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.sensor_fit = "HORIZONTAL"
    sensor = spec["camera"].get("sensor", 36.0)
    cd.sensor_width = sensor
    cd.clip_start = 0.01
    cd.clip_end = 200
    keys = []
    for k in spec["camera"]["keys"]:
        if "cam" in k:
            k, c = key_from_cam(k, sensor)
            spec["camera"].setdefault("shift_x", c.get("shift_x", 0.0))
            spec["camera"].setdefault("shift_y", c.get("shift_y", 0.0))
        if "roll" not in k and keys:
            k = dict(k, roll=keys[-1].get("roll", 0.0))  # a moved key keeps the solved camera's roll
        keys.append(k)
    cd.shift_x = spec["camera"].get("shift_x", 0.0)
    cd.shift_y = spec["camera"].get("shift_y", 0.0)
    for f in range(1, nframes + 1):
        t = (f - 1) / fps
        loc = sample(keys, t, "loc")
        tgt = sample(keys, t, "target")
        roll = sample(keys, t, "roll", 0.0)
        cam.matrix_world = Matrix.Translation(Vector(loc)) @ track_rot(loc, tgt, roll).to_4x4()
        cd.lens = sample(keys, t, "focal")
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.keyframe_insert("lens", frame=f)

    w, h = (int(v) for v in spec.get("res", "1080x1920").split("x"))
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = spec.get("res_pct", 100)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = spec.get("samples", 16)
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.render.use_overwrite = False
    sc.render.use_persistent_data = bool(spec.get("persistent", False))  # only for camera-only shots; luma-scan every frame
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    sc.render.image_settings.color_depth = "8"
    out = os.path.abspath(spec["out"])
    if spec.get("raycast"):
        sc.frame_set(1)
        sr.raycast(cam, spec["raycast"])
        return
    if spec.get("frames"):
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
