"""(Copied from projects/huracan-evo/tools/shot.py - sibling reel tool.) Huracan Evo shot renderer (Blender, Cycles CPU). Temerario-style moves the stock scan_render.py can't do:
keyframed spherical camera paths (orbit + crane + dolly + lens in one move), several prepped scan .blends in one
scene, per-part translate / hinge-rotate keys (exploded views, hood opening) and per-object visibility windows.
House look = scan_render.py's satin silver + studio world + lights (imported, not copied).

  blender -b -P projects/huracan-evo/tools/shot.py -- shot.json [--res-pct 30 --samples 8 --frames 1,20,40 --out DIR]

shot.json:
{ "objects": {"car": "/path/car.blend", "fb": "/path/front_bumper.blend", ...},   # prep'd with --like (same frame)
  "seconds": 3.8, "fps": 15, "res": [1080,1920], "res_pct": 75, "samples": 12, "out": "/dir",
  "camera": [ {"t":0, "az":30, "el":8, "dist":7.5, "target":[0,0,0.55], "lens":50}, {"t":1, ...} ],  # az: deg from +X toward +Y... see cam_matrix
  "anims": { "fb": [ {"t":0,"off":[0,0,0]}, {"t":0.6,"off":[0,-1.2,-0.1]} ],
             "hood": [ {"t":0,"deg":0}, {"t":1,"deg":-48}], },
  "hinges": { "hood": {"p":[x,y,z], "axis":[1,0,0]} },     # rotation pivot+axis (m) for "deg" keys
  "visible": { "car_full": [0, 0.5], "apr": [0.5, 1.01] }    # shot-fraction windows; default always visible
}
Keys use shot fractions t in [0,1]; between keys values ease with smoothstep (each key is a rest point) unless the
key has "lin": true. Camera az/el/dist/target/lens all interpolate, so one list describes orbit+crane+push.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "blender"))
import scan_render as sr  # noqa: E402  (house materials/world/lights)


def argv():
    a = sys.argv
    return a[a.index("--") + 1:] if "--" in a else []


def smooth(u):
    return u * u * (3 - 2 * u)


def interp(keys, t, field, default):
    ks = [k for k in keys if field in k]
    if not ks:
        return default
    if t <= ks[0]["t"]:
        return ks[0][field]
    for a, b in zip(ks, ks[1:]):
        if a["t"] <= t <= b["t"]:
            u = (t - a["t"]) / max(1e-9, b["t"] - a["t"])
            u = u if b.get("lin") else (u ** 3 if b.get("ease") == "in" else smooth(u))  # ease-in: arrives at full speed (slam)
            va, vb = a[field], b[field]
            if isinstance(va, list):
                return [x + (y - x) * u for x, y in zip(va, vb)]
            return va + (vb - va) * u
    return ks[-1][field]


def cam_matrix(az, el, dist, target, roll=0.0):
    """az=0: camera on -Y side looking +Y at the nose (car nose is -Y); az=90: camera on +X (car's right... see log)."""
    a, e = math.radians(az), math.radians(el)
    tgt = Vector(target)
    loc = tgt + Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))) * dist
    d = tgt - loc
    up = "Y" if abs(e) < math.radians(89.5) else "Y"
    q = d.to_track_quat("-Z", up)
    M = Matrix.Translation(loc) @ q.to_matrix().to_4x4()
    if abs(e) >= math.radians(89.5):  # straight down: define heading by az so a top-down spin is just an az sweep
        R = Matrix.Rotation(a, 4, "Z") @ Matrix.Rotation(math.pi, 4, "Z")
        M = Matrix.Translation(loc) @ R
    if roll:
        M = M @ Matrix.Rotation(math.radians(roll), 4, "Z")
    return M


def load_objects(spec):
    objs = {}
    for name, path in spec.items():
        with bpy.data.libraries.load(path, link=False) as (src, dst):
            dst.objects = list(src.objects)
        meshes = []
        root = None
        for o in dst.objects:
            if o is None:
                continue
            bpy.context.scene.collection.objects.link(o)
            if o.type == "MESH":
                o["ive_scan"] = True
                meshes.append(o)
            elif o.name.startswith("SCAN_ROOT"):
                root = o
                o.name = f"ROOT_{name}"  # keep the name SCAN_ROOT free for the light rig
        # pivot empty per object group: anims drive the pivot, meshes keep their prepped world transform
        piv = bpy.data.objects.new(f"PIV_{name}", None)
        bpy.context.scene.collection.objects.link(piv)
        bpy.context.view_layer.update()
        for o in meshes:
            top = o
            while top.parent is not None:
                top = top.parent
            if top.parent is None and top is not piv:
                mw = top.matrix_world.copy()
                top.parent = piv
                top.matrix_world = mw
        objs[name] = (piv, meshes)
    return objs


def main():
    a = argv()
    spec = json.load(open(a[0]))
    opt = dict(zip(a[1::2], a[2::2]))
    res_pct = int(opt.get("--res-pct", spec.get("res_pct", 75)))
    samples = int(opt.get("--samples", spec.get("samples", 12)))
    out = opt.get("--out", spec["out"])
    only = [int(v) for v in opt["--frames"].split(",")] if "--frames" in opt else None

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    objs = load_objects(spec["objects"])
    allmesh = [m for _, ms in objs.values() for m in ms]
    lo, hi = sr.bbox(allmesh)

    fps = spec.get("fps", 15)
    n = max(1, int(round(spec["seconds"] * fps)))
    sc.render.fps = int(fps)
    sc.frame_start, sc.frame_end = 1, n

    # look: house satin silver on pure black (no lights visible, no floor)
    bg = tuple(spec.get("bg", [0.004, 0.004, 0.005])) + (1.0,)
    sr.studio_world(bg, False)
    # lights are fixed to the car (not the camera) so reflections slide across the body as the camera moves
    car_lo, car_hi = sr.bbox(objs[spec.get("light_ref", next(iter(objs)))][1])
    root = bpy.data.objects.new("SCAN_ROOT", None)
    sc.collection.objects.link(root)
    root.location = (car_lo + car_hi) / 2
    sr.studio_lights(car_lo, car_hi)
    mat = sr.mat_silver()
    tints = spec.get("tint", {})  # {object: [r,g,b]} - registration-check renders only (part colour over the car)
    tmats = {}
    for k, col in tints.items():
        m, nt, outn = sr.new_mat("tint_" + k)
        pr = sr.principled(nt, tuple(col) + (1,), 0.5, 0.0)
        nt.links.new(pr.outputs[0], outn.inputs[0])
        tmats[k] = m
    owner = {id(m): k for k, (_, ms) in objs.items() for m in ms}
    for o in allmesh:
        o.data.materials.clear()
        o.data.materials.append(tmats.get(owner[id(o)], mat))
        for p in o.data.polygons:
            p.use_smooth = spec.get("smooth", False)  # flat: scan micro-detail reads like the Temerario ref

    cd = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.sensor_fit = "HORIZONTAL"
    cd.sensor_width = spec.get("sensor", 24.0)  # 24 mm wide on a 9:16 frame
    cd.clip_start, cd.clip_end = 0.05, 200
    keys = spec["camera"]
    for f in range(1, n + 1):
        t = (f - 1) / max(1, n - 1)
        M = cam_matrix(interp(keys, t, "az", 30), interp(keys, t, "el", 8), interp(keys, t, "dist", 7),
                       interp(keys, t, "target", [0, 0, 0.55]), interp(keys, t, "roll", 0))
        cam.matrix_world = M
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.lens = interp(keys, t, "lens", 50)
        cd.keyframe_insert("lens", frame=f)

    hinges = spec.get("hinges", {})
    for name, ks in spec.get("anims", {}).items():
        piv = objs[name][0]
        h = hinges.get(name)
        for f in range(1, n + 1):
            t = (f - 1) / max(1, n - 1)
            off = Vector(interp(ks, t, "off", [0, 0, 0]))
            M = Matrix.Translation(off)
            if h:
                deg = interp(ks, t, "deg", 0)
                p = Vector(h["p"])
                R = Matrix.Rotation(math.radians(deg), 4, Vector(h["axis"]).normalized())
                M = M @ Matrix.Translation(p) @ R @ Matrix.Translation(-p)
            spin = interp(ks, t, "spin", None)  # [deg, ax, ay, az] about the part's own centre
            if spin:
                plo, phi = sr.bbox(objs[name][1])
                c = (plo + phi) / 2
                R = Matrix.Rotation(math.radians(spin[0]), 4, Vector(spin[1:]).normalized())
                M = M @ Matrix.Translation(c) @ R @ Matrix.Translation(-c)
            piv.matrix_world = M
            piv.keyframe_insert("location", frame=f)
            piv.keyframe_insert("rotation_euler", frame=f)
            piv.keyframe_insert("scale", frame=f)

    for name, win in spec.get("visible", {}).items():
        for o in objs[name][1]:
            for f in range(1, n + 1):
                t = (f - 1) / max(1, n - 1)
                o.hide_render = not (win[0] <= t < win[1])
                o.keyframe_insert("hide_render", frame=f)

    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    # Huracan sibling: persistent data lost all lights mid-shot when the hood hinge animated; off for animated shots
    sc.render.use_persistent_data = spec.get("persistent", True)
    sc.render.resolution_x, sc.render.resolution_y = spec.get("res", [1080, 1920])
    sc.render.resolution_percentage = res_pct
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = spec.get("exposure", 0.0)
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    os.makedirs(out, exist_ok=True)
    if spec.get("save_blend"):
        bpy.ops.wm.save_as_mainfile(filepath=spec["save_blend"], copy=True)
    frames = only or range(1, n + 1)
    for f in frames:
        path = os.path.join(out, f"f_{f:04d}.png")
        if os.path.exists(path) and not only:
            continue  # resumable
        sc.frame_set(f)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print("IVE_FRAME", f, flush=True)
    print("IVE_SHOT_DONE", out)


if __name__ == "__main__":
    main()
