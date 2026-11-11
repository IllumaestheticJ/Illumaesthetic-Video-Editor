"""Copy of projects/a90-supra/tools/shots.py (keyframed camera + parts) with two additions for the A90
scan-process reel: spec "look": "xray" (scan_render.mat_xray, grey glass) and spec "morph": [f0, f1]
(shot fractions) = blend every material into flat clay and the camera background into "morph_bg" before
dissolving into a grey product render. Spec "cam" keys may also carry "lens" and the spec a "sensor".

Original docstring:
A90 Supra Temerario-style shot renderer (Blender, Cycles CPU).

    blender -b -P projects/a90-supra/tools/shots.py -- --shot projects/a90-supra/shots/s01.json \
        --out /home/user/media/work/a90/renders/s01 [--res-pct 75 --samples 12 --fps 15] [--still 0.5]

Reuses the house look from blender/scan_render.py (mat_silver, studio_world, studio_lights) so the
silver matches the 240SX/FG2 reels. What it adds over `ive render`:
  * keyframed cameras in cylindrical coords around a target (az deg, dist m, z m) -> smooth turntables,
    orbits, close-up glides and a top-down move, interpolated with Catmull-Rom + a global ease
  * several prepared .blend scans per shot (all prepped with `--like` the base, so they share one frame),
    each with keyframed offset / rotation about its own centre (exploded view + reassembly)

Shot JSON:
{
  "seconds": 4.0, "lens": 50, "sensor": 36, "ease": "ease_in_out" | "linear",
  "objects": [{"blend": ".../car.blend"},
              {"blend": ".../fbumper.blend", "keys": [{"t":0, "loc":[0,0,0], "rot":[0,0,0]}, ...]}],
  "cam": [{"t":0, "az":35, "dist":6.5, "z":1.2, "look":[0,0,0.6]}, ...]   # or "pos":[x,y,z]
}
az = degrees around +Z from +X (car nose is +X), so az 0 = straight at the nose, 90 = left side (+Y).
"""
import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Vector, Euler, Matrix

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "blender"))
import scan_render as sr  # noqa: E402  (house materials / world / lights)


def args():
    a = sys.argv[sys.argv.index("--") + 1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=15)
    ap.add_argument("--res", default="1080x1920")
    ap.add_argument("--res-pct", type=int, default=75)
    ap.add_argument("--samples", type=int, default=12)
    ap.add_argument("--still", type=float, default=-1, help="render one frame at this shot fraction (0-1) to --out .png")
    ap.add_argument("--stills", default="", help="comma list of fractions -> <out>_<frac>.png (framing checks)")
    return ap.parse_args(a)


def ease(t, kind):
    if kind == "ease_in_out":
        return t * t * (3 - 2 * t)
    if kind == "ease_out":
        return 1 - (1 - t) ** 2
    if kind == "ease_in":
        return t * t
    if kind == "sine":
        return 0.5 - 0.5 * math.cos(math.pi * t)
    return t


def catmull(keys, t, field):
    """Piecewise Catmull-Rom over key[field] (lists) at key['t']."""
    ts = [k["t"] for k in keys]
    if t <= ts[0]:
        return list(keys[0][field])
    if t >= ts[-1]:
        return list(keys[-1][field])
    i = max(j for j in range(len(ts) - 1) if ts[j] <= t)
    u = (t - ts[i]) / (ts[i + 1] - ts[i])
    p0 = keys[max(0, i - 1)][field]
    p1, p2 = keys[i][field], keys[i + 1][field]
    p3 = keys[min(len(keys) - 1, i + 2)][field]
    out = []
    for a, b, c, d in zip(p0, p1, p2, p3):
        out.append(0.5 * ((2 * b) + (-a + c) * u + (2 * a - 5 * b + 4 * c - d) * u * u + (-a + 3 * b - 3 * c + d) * u ** 3))
    return out


def seg_ease(keys, t, field, kind="ease_in_out"):
    """Per-segment eased lerp (parts: each move starts and stops softly)."""
    ts = [k["t"] for k in keys]
    if t <= ts[0]:
        return list(keys[0][field])
    if t >= ts[-1]:
        return list(keys[-1][field])
    i = max(j for j in range(len(ts) - 1) if ts[j] <= t)
    u = ease((t - ts[i]) / (ts[i + 1] - ts[i]), keys[i + 1].get("ease", kind))
    return [a + (b - a) * u for a, b in zip(keys[i][field], keys[i + 1][field])]


def cam_keys(spec):
    ks = []
    for k in spec["cam"]:
        look = k.get("look", [0, 0, 0.6])
        if "pos" in k:
            p = Vector(k["pos"])
        else:
            az = math.radians(k["az"])
            p = Vector((look[0] + k["dist"] * math.cos(az), look[1] + k["dist"] * math.sin(az), k["z"]))
        ks.append({"t": k["t"], "p": list(p), "look": list(look), "lens": [k.get("lens", spec.get("lens", 50))],
                   "cyl": [k["az"], k["dist"], k["z"]] if "pos" not in k else None, "roll": [k.get("roll", 0.0)],
                   "up": list(k.get("up", [0, 0, 1]))})
    return ks


def cam_seg(spec, t):
    """spec "cam_interp": "seg" - per-segment eased camera (key "ease", default ease_in_out). Each key is either
    {pos, look} or cylindrical {az, dist, z, look}; a segment between two cylindrical keys with the same look moves on
    a true arc, otherwise positions are lerped. lens/roll lerp. Holds = two identical keys."""
    ks = spec["cam"]
    def P(k):
        if "pos" in k:
            return Vector(k["pos"])
        lk = k["look"]; az = math.radians(k["az"])
        return Vector((lk[0] + k["dist"] * math.cos(az), lk[1] + k["dist"] * math.sin(az), k["z"]))
    if t <= ks[0]["t"]:
        i, u = 0, 0.0
    elif t >= ks[-1]["t"]:
        i, u = len(ks) - 2, 1.0
    else:
        i = max(j for j in range(len(ks) - 1) if ks[j]["t"] <= t)
        u = ease((t - ks[i]["t"]) / (ks[i + 1]["t"] - ks[i]["t"]), ks[i + 1].get("ease", "ease_in_out"))
    a, b = ks[i], ks[i + 1]
    la, lb = Vector(a["look"]), Vector(b["look"])
    look = la.lerp(lb, u)
    if "az" in a and "az" in b and list(a["look"]) == list(b["look"]):
        az = math.radians(a["az"] + (b["az"] - a["az"]) * u); dist = a["dist"] + (b["dist"] - a["dist"]) * u
        z = a["z"] + (b["z"] - a["z"]) * u
        p = Vector((la[0] + dist * math.cos(az), la[1] + dist * math.sin(az), z))
    else:
        p = P(a).lerp(P(b), u)
    L = lambda k, f, d: k.get(f, spec.get(f, d))
    lens = L(a, "lens", 50) + (L(b, "lens", 50) - L(a, "lens", 50)) * u
    roll = a.get("roll", 0.0) + (b.get("roll", 0.0) - a.get("roll", 0.0)) * u
    return p, look, lens, roll, Vector((0, 0, 1))


def cam_at(ks, t):
    look = Vector(catmull(ks, t, "look"))
    if all(k["cyl"] for k in ks):  # interpolate in cylindrical coords -> true arcs
        az, dist, z = catmull([{"t": k["t"], "c": k["cyl"]} for k in ks], t, "c")
        p = Vector((look.x + dist * math.cos(math.radians(az)), look.y + dist * math.sin(math.radians(az)), z))
    else:
        p = Vector(catmull(ks, t, "p"))
    return p, look, catmull(ks, t, "lens")[0], catmull(ks, t, "roll")[0], Vector(catmull(ks, t, "up"))


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


def main():
    a = args()
    spec = json.load(open(a.shot))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    groups = []
    for ob in spec["objects"]:
        ms = load_blend(ob["blend"])
        groups.append((ob, ms))
    allm = [m for _, ms in groups for m in ms]
    bpy.context.view_layer.update()
    lo, hi = sr.bbox([m for (ob, ms) in groups[:1] for m in ms])  # lights sized from the base car

    # world + house silver (or x-ray)
    look = spec.get("look", "silver")
    if look == "silver":
        sr.studio_world(sr.rgb(spec.get("bg", "0.004,0.004,0.005")), False)
    else:
        sr.setup_world(sr.rgb(spec.get("bg", "0.004,0.004,0.005")), False)
    root = bpy.data.objects.new("SCAN_ROOT", None)  # lights track this
    sc.collection.objects.link(root)
    root.location = (lo + hi) / 2
    sr.studio_lights(lo, hi)
    mat = sr.mat_silver() if look == "silver" else sr.mat_xray(sr.rgb(spec.get("accent", "0.8,0.82,0.86")))
    fps_, n_ = a.fps, max(1, int(round(spec["seconds"] * a.fps)))
    if "morph" in spec:
        f0, f1 = (max(1, int(round(1 + v * (n_ - 1)))) for v in spec["morph"])
        mat = sr.morph_to_clay(mat, sr.rgb(spec.get("clay_color", "0.30,0.30,0.31")), f0, f1)
        wb = sc.world.node_tree.nodes.get("Background")
        if wb is not None:
            wb.inputs["Color"].keyframe_insert("default_value", frame=f0)
            wb.inputs["Color"].default_value = sr.rgb(spec.get("morph_bg", "0.007,0.0085,0.007"))
            wb.inputs["Color"].keyframe_insert("default_value", frame=f1)
    for ob, ms in groups:
        mm = mat
        if "color" in ob:  # debug / registration overlays only (house look is silver)
            mm, nt, out = sr.new_mat("dbg")
            nt.links.new(sr.principled(nt, tuple(ob["color"]) + (1,), 0.5).outputs[0], out.inputs[0])
        for m in ms:
            m.data.materials.clear()
            m.data.materials.append(mm)
            for p in m.data.polygons:
                p.use_smooth = spec.get("smooth", False)
            if ob.get("hide"):
                m.hide_render = True

    fps = a.fps
    nframes = max(1, int(round(spec["seconds"] * fps)))
    sc.render.fps = int(round(fps))
    sc.frame_start, sc.frame_end = 1, nframes
    gease = spec.get("ease", "ease_in_out")

    # parts: pivot empty at the part's centre, keyframed loc offset + rot (deg) about that centre
    for ob, ms in groups:
        if "keys" not in ob:
            continue
        plo, phi = sr.bbox(ms)
        piv = bpy.data.objects.new("piv", None)
        sc.collection.objects.link(piv)
        base = (plo + phi) / 2 + Vector(ob.get("pivot_offset", [0, 0, 0]))
        piv.location = base
        bpy.context.view_layer.update()
        for m in ms:
            r = m.parent or m
            mw = r.matrix_world.copy()
            r.parent = piv
            r.matrix_world = mw
        keys = [dict(k, loc=k.get("loc", [0, 0, 0]), rot=k.get("rot", [0, 0, 0])) for k in ob["keys"]]
        for f in range(1, nframes + 1):
            t = (f - 1) / max(1, nframes - 1)
            piv.location = base + Vector(seg_ease(keys, t, "loc"))
            piv.rotation_euler = Euler([math.radians(v) for v in seg_ease(keys, t, "rot")])
            piv.keyframe_insert("location", frame=f)
            piv.keyframe_insert("rotation_euler", frame=f)

    cd = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.sensor_fit = "VERTICAL" if spec.get("sensor_fit") == "vertical" else "HORIZONTAL"
    cd.sensor_width = spec.get("sensor", 36)
    cd.clip_start, cd.clip_end = 0.01, 200
    ks = cam_keys(spec) if spec.get("cam_interp") != "seg" else None
    for f in range(1, nframes + 1):
        if spec.get("cam_interp") == "seg":
            p, look, lens, roll, up = cam_seg(spec, (f - 1) / max(1, nframes - 1))
        else:
            t = ease((f - 1) / max(1, nframes - 1), gease)
            p, look, lens, roll, up = cam_at(ks, t)
        cam.location = p
        f_ = (look - p).normalized()
        if abs(f_.dot(up.normalized())) > 0.995:  # looking along the up hint: fall back to "away from camera"
            up = Vector((-(look - p).x, -(look - p).y, 0)) if (look - p).xy.length > 1e-4 else Vector((1, 0, 0))
        r_ = f_.cross(up).normalized()
        u_ = r_.cross(f_)
        cam.rotation_euler = Matrix((r_, u_, -f_)).transposed().to_euler()
        if roll:
            cam.rotation_euler.rotate_axis("Z", math.radians(roll))
        cd.lens = lens
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.keyframe_insert("lens", frame=f)

    W, H = [int(v) for v in a.res.split("x")]
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.resolution_percentage = a.res_pct
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = a.samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.render.use_persistent_data = bool(spec.get("persistent", False))  # off by default (all-reels brief: lighting dropouts)
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"

    out = os.path.abspath(a.out)
    fr = [float(v) for v in a.stills.split(",") if v] if a.stills else ([a.still] if a.still >= 0 else [])
    if fr:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        for x in fr:
            sc.frame_set(1 + int(round(x * (nframes - 1))))
            sc.render.filepath = f"{out}_{x:.2f}.png" if len(fr) > 1 or a.stills else out
            bpy.ops.render.render(write_still=True)
    else:
        os.makedirs(out, exist_ok=True)
        sc.render.filepath = os.path.join(out, "f_")
        sc.render.use_overwrite = False  # resumable: frames already on disk are skipped
        sc.render.use_placeholder = True
        bpy.ops.render.render(animation=True)
    print("IVE_SHOT_DONE", out, nframes)


if __name__ == "__main__":
    main()
