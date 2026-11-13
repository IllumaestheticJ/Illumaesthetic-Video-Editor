"""A90 Supra v3 shot renderer (Blender, Cycles CPU) = shots.py + state swaps, real rotation axes, under-light.

v3 additions (per object unless noted):
  "vis": [[t0, t1], ...]      render-visible only inside these shot fractions (1:1 state swaps, parts that exit)
  "pivot": [x, y, z]          absolute pivot (scene m) instead of the bbox centre
  "axis": [x, y, z] + key "ang" (deg)   extra rotation about this axis through the pivot (wheel spin, steering), applied
                               before the keyed loc/rot
  "light_bbox": [[lo],[hi]]   (shot) pin the light rig to this bbox (same light for every shot whatever is loaded)
  "underlight": 0.4           (shot) soft area light under the car, pointing up (underbody shots)
  "frames_at_fps"             shot JSON may carry "fps": used when --fps is not given

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
Optional per object (v2 section highlight, default look unchanged when absent):
  "glow": [{"t":0.30,"v":0},{"t":0.38,"v":1},{"t":0.6,"v":0.25}]  # warm rim emission on the part (0..1)
  "dim":  [{"t":0.28,"v":0},{"t":0.36,"v":1}]                       # darken the base silver (0..1) to isolate a section
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
    ap.add_argument("--fps", type=float, default=0)
    ap.add_argument("--res", default="1080x1920")
    ap.add_argument("--res-pct", type=int, default=75)
    ap.add_argument("--samples", type=int, default=12)
    ap.add_argument("--still", type=float, default=-1, help="render one frame at this shot fraction (0-1) to --out .png")
    ap.add_argument("--stills", default="", help="comma list of fractions -> <out>_<frac>.png (framing checks)")
    ap.add_argument("--persistent", choices=["auto", "on", "off"], default="auto",
                    help="Cycles persistent data; auto = off when any part is keyed (lights dropped mid-shot on v1 s08)")
    ap.add_argument("--preview", action="store_true", help="Workbench engine (seconds per frame) for framing/motion checks")
    ap.add_argument("--frames", default="", help="render only this frame range a-b (re-render dark frames in a fresh process)")
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


def cam_at(ks, t):
    look = Vector(catmull(ks, t, "look"))
    if all(k["cyl"] for k in ks):  # interpolate in cylindrical coords -> true arcs
        az, dist, z = catmull([{"t": k["t"], "c": k["cyl"]} for k in ks], t, "c")
        p = Vector((look.x + dist * math.cos(math.radians(az)), look.y + dist * math.sin(math.radians(az)), z))
    else:
        p = Vector(catmull(ks, t, "p"))
    return p, look, catmull(ks, t, "lens")[0], catmull(ks, t, "roll")[0], Vector(catmull(ks, t, "up"))


SILVER = (0.62, 0.63, 0.66)   # mat_silver base colour
GLOW_GAIN = 5.0               # emission strength at glow 1.0 (rim-weighted, see highlight_mat)
DIM_GAIN = 0.85               # fraction of the surface light replaced by black at dim 1.0 (AgX compresses: 0.5 mix ~ -20 % display)


def highlight_mat():
    """House silver + (a) a warm-white facing-ratio RIM emission whose strength is keyed ("glow") and (b) a keyed
    Mix Shader toward black ("dim"), which darkens reflections too (a base-colour dim barely shows on a metallic).
    glow 0 / dim 0 renders identically to mat_silver. v2 'highlight the section': the separating part gets a short rim
    pulse; parked parts of finished sections are dimmed so the current section reads."""
    m = sr.mat_silver()
    m.name = "ive_silver_hl"
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.45
    pw = nt.nodes.new("ShaderNodeMath")
    pw.operation = "POWER"
    pw.inputs[1].default_value = 1.5
    nt.links.new(lw.outputs["Facing"], pw.inputs[0])
    cm = nt.nodes.new("ShaderNodeMix")  # emission colour = rim mask * warm white
    cm.data_type = "RGBA"
    cm.inputs["A"].default_value = (0, 0, 0, 1)
    cm.inputs["B"].default_value = (1.0, 0.97, 0.93, 1)
    nt.links.new(pw.outputs[0], cm.inputs["Factor"])
    e = sr.emission(nt, (1.0, 0.97, 0.93, 1), 0.0)
    nt.links.new(cm.outputs["Result"], e.inputs["Color"])
    add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(p.outputs[0], add.inputs[0])
    nt.links.new(e.outputs[0], add.inputs[1])
    blk = nt.nodes.new("ShaderNodeBsdfDiffuse")
    blk.inputs["Color"].default_value = (0, 0, 0, 1)
    ms = nt.nodes.new("ShaderNodeMixShader")
    ms.inputs["Fac"].default_value = 0.0
    nt.links.new(add.outputs[0], ms.inputs[1])
    nt.links.new(blk.outputs[0], ms.inputs[2])
    nt.links.new(ms.outputs[0], out.inputs[0])
    return m, {"emit": e, "dim": ms.inputs["Fac"]}


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
    if spec.get("light_bbox"):
        lo, hi = Vector(spec["light_bbox"][0]), Vector(spec["light_bbox"][1])

    # world + house silver
    sr.studio_world(sr.rgb(spec.get("bg", "0.004,0.004,0.005")), False)
    root = bpy.data.objects.new("SCAN_ROOT", None)  # lights track this
    sc.collection.objects.link(root)
    root.location = (lo + hi) / 2
    sr.studio_lights(lo, hi)
    if spec.get("underlight"):
        r = max(hi - lo)
        c = (lo + hi) / 2
        ul = sr.add_light("under", "AREA", Vector((c.x, c.y, lo.z - r * 0.45)), 70 * r * r * spec["underlight"], r * 1.2)
        if ul is not None:
            ul.rotation_euler = Euler((math.pi, 0, 0))   # area lights emit along -Z: flip to shine up
    mat = sr.mat_silver()
    hl_mats = []  # (ob spec, highlight handles) for keyframing below
    for ob, ms in groups:
        mm = mat
        if "color" in ob:  # debug / registration overlays only (house look is silver)
            mm, nt, out = sr.new_mat("dbg")
            nt.links.new(sr.principled(nt, tuple(ob["color"]) + (1,), 0.5).outputs[0], out.inputs[0])
        elif "glow" in ob or "dim" in ob:  # section highlight (v2): own copy of the house silver
            mm, h = highlight_mat()
            hl_mats.append((ob, h))
        for m in ms:
            m.data.materials.clear()
            m.data.materials.append(mm)
            for p in m.data.polygons:
                p.use_smooth = spec.get("smooth", False)
            if ob.get("hide"):
                m.hide_render = True

    fps = a.fps or spec.get("fps", 15)
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
        base = (Vector(ob["pivot"]) if "pivot" in ob else (plo + phi) / 2) + Vector(ob.get("pivot_offset", [0, 0, 0]))
        piv.location = base
        bpy.context.view_layer.update()
        for m in ms:
            r = m.parent or m
            mw = r.matrix_world.copy()
            r.parent = piv
            r.matrix_world = mw
        keys = [dict(k, loc=k.get("loc", [0, 0, 0]), rot=k.get("rot", [0, 0, 0]), ang=[k.get("ang", 0.0)]) for k in ob["keys"]]
        axis = Vector(ob["axis"]).normalized() if "axis" in ob else None
        piv.rotation_mode = "QUATERNION"
        from mathutils import Quaternion
        prev = None
        for f in range(1, nframes + 1):
            t = (f - 1) / max(1, nframes - 1)
            piv.location = base + Vector(seg_ease(keys, t, "loc"))
            q = Euler([math.radians(v) for v in seg_ease(keys, t, "rot")]).to_quaternion()
            if axis is not None:
                q = q @ Quaternion(axis, math.radians(seg_ease(keys, t, "ang")[0]))
            if prev is not None and q.dot(prev) < 0:
                q.negate()
            prev = q.copy()
            piv.rotation_quaternion = q
            piv.keyframe_insert("location", frame=f)
            piv.keyframe_insert("rotation_quaternion", frame=f)

    # v3 mechanism motion: "mats" = rigid 4x4 deltas (scene frame) applied on top of everything else; keys are dense
    # (the generator samples the solved suspension), so matrices are blended element-wise between neighbours.
    from mathutils import Quaternion as _Q
    for ob, ms in groups:
        if "mats" not in ob:
            continue
        E = bpy.data.objects.new("mech", None)
        sc.collection.objects.link(E)
        E.rotation_mode = "QUATERNION"
        bpy.context.view_layer.update()
        tops = {(m.parent or m) for m in ms}
        tops = {(t.parent or t) for t in tops}          # the keyed pivot, when there is one
        for r in tops:
            mw = r.matrix_world.copy(); r.parent = E; r.matrix_world = mw
        mk = ob["mats"]
        prev = None
        for f in range(1, nframes + 1):
            t = (f - 1) / max(1, nframes - 1)
            if t <= mk[0]["t"]:
                M = Matrix(mk[0]["m"])
            elif t >= mk[-1]["t"]:
                M = Matrix(mk[-1]["m"])
            else:
                i = max(j for j in range(len(mk) - 1) if mk[j]["t"] <= t)
                u = (t - mk[i]["t"]) / (mk[i + 1]["t"] - mk[i]["t"])
                A, Bm = Matrix(mk[i]["m"]), Matrix(mk[i + 1]["m"])
                M = Matrix([[A[r_][c_] + (Bm[r_][c_] - A[r_][c_]) * u for c_ in range(4)] for r_ in range(4)])
            loc, q, _s = M.decompose()
            if prev is not None and q.dot(prev) < 0:
                q.negate()
            prev = q.copy()
            E.location, E.rotation_quaternion = loc, q
            E.keyframe_insert("location", frame=f); E.keyframe_insert("rotation_quaternion", frame=f)

    # v3 springs: "stretch" = {"p": fixed end, "keys": [{"t", "axis": [..] (towards the moving end), "s": length ratio}]}
    for ob, ms in groups:
        if "stretch" not in ob:
            continue
        st = ob["stretch"]
        S = bpy.data.objects.new("stretch", None)
        sc.collection.objects.link(S)
        S.rotation_mode = "QUATERNION"
        S.location = Vector(st["p"])
        a0 = Vector(st["axis0"]).normalized()
        S.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(a0)
        bpy.context.view_layer.update()
        for r in {(m.parent or m) for m in ms}:
            mw = r.matrix_world.copy(); r.parent = S; r.matrix_world = mw
        sk = [{"t": k["t"], "v": list(k["axis"]) + [k["s"]]} for k in st["keys"]]
        for f in range(1, nframes + 1):
            t = (f - 1) / max(1, nframes - 1)
            v = seg_ease(sk, t, "v", "linear")
            S.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(v[:3]).normalized())
            S.scale = (1, 1, v[3])
            S.keyframe_insert("rotation_quaternion", frame=f); S.keyframe_insert("scale", frame=f)

    # v3 visibility windows (state swaps, parts that have left)
    for ob, ms in groups:
        if "vis" not in ob:
            continue
        for f in range(1, nframes + 1):
            t = (f - 1) / max(1, nframes - 1)
            on = any(w[0] - 1e-6 <= t <= w[1] + 1e-6 for w in ob["vis"])
            for m in ms:
                m.hide_render = not on
                m.keyframe_insert("hide_render", frame=f)

    # section highlight: per-frame keys of the rim glow strength and the body dim factor
    for ob, h in hl_mats:
        gk = [{"t": k["t"], "v": [k["v"]], "ease": k.get("ease", "ease_in_out")} for k in ob.get("glow", [{"t": 0, "v": 0}])]
        dk = [{"t": k["t"], "v": [k["v"]], "ease": k.get("ease", "ease_in_out")} for k in ob.get("dim", [{"t": 0, "v": 0}])]
        for f in range(1, nframes + 1):
            t = (f - 1) / max(1, nframes - 1)
            g = seg_ease(gk, t, "v")[0]
            d = seg_ease(dk, t, "v")[0]
            h["emit"].inputs["Strength"].default_value = GLOW_GAIN * g
            h["emit"].inputs["Strength"].keyframe_insert("default_value", frame=f)
            h["dim"].default_value = DIM_GAIN * d
            h["dim"].keyframe_insert("default_value", frame=f)

    cd = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.sensor_fit = "VERTICAL" if spec.get("sensor_fit") == "vertical" else "HORIZONTAL"
    cd.sensor_width = spec.get("sensor", 36)
    cd.clip_start, cd.clip_end = 0.01, 200
    ks = cam_keys(spec)
    for f in range(1, nframes + 1):
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
    moving = any(k in ob for ob, _ in groups for k in ("keys", "glow", "dim", "vis", "mats", "stretch"))
    sc.render.use_persistent_data = a.persistent == "on" or (a.persistent == "auto" and not moving)
    if a.preview:
        sc.render.engine = "BLENDER_WORKBENCH"
        sh = sc.display.shading
        sh.light = "STUDIO"; sh.color_type = "SINGLE"; sh.single_color = (0.75, 0.75, 0.78); sh.show_cavity = True
        sc.world.color = (0, 0, 0)
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    if spec.get("look"):                       # v3: more contrast so scan detail reads (same silver material)
        try:
            sc.view_settings.look = spec["look"]
        except TypeError:
            print("IVE_WARN look not available:", spec["look"])
    sc.view_settings.exposure = spec.get("exposure", 0.0)
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
        if a.frames:
            f0, f1 = (int(v) for v in a.frames.split("-"))
            sc.frame_start, sc.frame_end = max(1, f0), min(nframes, f1)
        bpy.ops.render.render(animation=True)
    print("IVE_SHOT_DONE", out, nframes)


if __name__ == "__main__":
    main()
