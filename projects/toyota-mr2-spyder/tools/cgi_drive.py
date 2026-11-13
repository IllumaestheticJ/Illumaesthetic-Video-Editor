"""CGI driving shot for the MR2 reel ending: the Epsilon lookbook car (eps-toyota-mr2-spyder-v19.glb, full kit) placed in the
scan frame (kit/model_to_scan.json), on a procedural night road. Used because no clean real driving shot exists (survey
2026-11-12). The car stays at the scan-frame origin and the road, lane marks and light bars move past it, so the camera
keys are the same spherical keys as tools/shot3.py and frame 1 can be a 1:1 match to the last scan + kit frame.

    blender -b -P cgi_drive.py -- spec.json [--res-pct 30 --samples 8 --frames 1,60,120 --out DIR]

spec: {"seconds": 8, "fps": 30, "camera": [ {t, az, el, dist, target, lens}, ... ],      # shot3.py convention
       "speed": [ {"t": 0, "v": 14}, {"t": 1, "v": 30} ],                                  # m/s, integrated per frame
       "paint": [r, g, b] (sRGB 0-1), "samples": 24, "res_pct": 75, "out": dir, "exposure": 0,
       "pull": [ {"t": .7, "y": 0}, {"t": 1, "y": 9} ]   # the car pulls away: camera rig slides back by y metres }
"""
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shot3  # noqa: E402  (cam_matrix, interp)

M = "/home/user/media/toyota-mr2-spyder"
GLB = f"{M}/glb/eps-toyota-mr2-spyder-v19.glb"


def srgb(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def emit_mat(name, rgb, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (*rgb, 1)
    e.inputs["Strength"].default_value = strength
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0])
    return m


def box(name, size, loc, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    o.data.materials.append(mat)
    return o


def main():
    a = shot3.argv()
    spec = json.load(open(a[0]))
    opt = dict(zip(a[1::2], a[2::2]))
    res_pct = int(opt.get("--res-pct", spec.get("res_pct", 75)))
    samples = int(opt.get("--samples", spec.get("samples", 24)))
    out = opt.get("--out", spec["out"])
    only = [int(v) for v in opt["--frames"].split(",")] if "--frames" in opt else None

    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    fps = spec.get("fps", 30)
    n = max(1, int(round(spec["seconds"] * fps)))
    sc.render.fps = int(fps)
    sc.frame_start, sc.frame_end = 1, n

    # --- car: lookbook model in the scan frame -------------------------------------------------------------------
    bpy.ops.import_scene.gltf(filepath=GLB)
    imp = list(bpy.context.selected_objects)
    T = json.load(open(f"{M}/kit/model_to_scan.json"))
    R = Matrix(T["R"]).to_4x4()
    root = bpy.data.objects.new("eps_root", None)
    sc.collection.objects.link(root)
    for o in imp:
        if o.parent is None:
            o.parent = root
    root.matrix_world = Matrix.Translation(Vector(T["t"])) @ R @ Matrix.Scale(T["scale"], 4)
    for o in imp:
        if o.name.endswith("_stock"):       # stock variants are replaced by the Epsilon parts
            o.hide_render = True
    rgb = spec.get("paint", [0.76, 0.05, 0.07])
    for m in bpy.data.materials:
        if not m.node_tree:
            continue
        p = next((x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED"), None)
        if p is None:
            continue
        if m.name.startswith("paint"):
            for l in list(p.inputs["Base Color"].links):
                m.node_tree.links.remove(l)
            p.inputs["Base Color"].default_value = (srgb(rgb[0]), srgb(rgb[1]), srgb(rgb[2]), 1)
            p.inputs["Metallic"].default_value = 0.0
            p.inputs["Roughness"].default_value = 0.2
            p.inputs["Coat Weight"].default_value = 1.0
            p.inputs["Coat Roughness"].default_value = 0.04
    blk = bpy.data.materials.get("plastic_black")
    for o in imp:
        if o.name == "part_diffuser" and blk:              # user v3 note: the diffuser is black, not body colour
            for sl in o.material_slots:
                sl.material = blk
    bpy.context.view_layer.update()

    # --- speed -> travelled distance per frame ----------------------------------------------------------------------
    sk = spec.get("speed", [{"t": 0, "v": 22}])
    dist = [0.0]
    for f in range(2, n + 1):
        t = (f - 1.5) / max(1, n - 1)
        dist.append(dist[-1] + shot3.interp(sk, t, "v", 22) / fps)

    # wheels spin about their axle (model x axis through the wheel centre)
    for o in imp:
        if o.name.startswith("wheel_") and o.type == "MESH":
            bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
            c = sum(bb, Vector()) / 8
            r = (max(v.z for v in bb) - min(v.z for v in bb)) / 2
            piv = bpy.data.objects.new("PIV_" + o.name, None)
            sc.collection.objects.link(piv)
            piv.location = c
            bpy.context.view_layer.update()
            mw = o.matrix_world.copy()
            o.parent = piv
            o.matrix_world = mw
            for f in range(1, n + 1):
                piv.rotation_euler = (-dist[f - 1] / r, 0, 0)   # nose +Y: rolling forward = negative rotation about +X
                piv.keyframe_insert("rotation_euler", frame=f)
            for fc in piv.animation_data.action.fcurves if hasattr(piv.animation_data.action, "fcurves") else []:
                for k in fc.keyframe_points:
                    k.interpolation = "LINEAR"

    # --- road: everything on one mover empty sliding toward -Y ---------------------------------------------------
    mover = bpy.data.objects.new("road_mover", None)
    sc.collection.objects.link(mover)
    RZ = spec.get("road_z", 0.0)   # road sits at the model's tyre bottom in the scan frame
    import city_env                                       # v4 environment (the v3 plane + bars + boxes was "very low detail")
    onc = city_env.build(sc, mover, spec)
    for f in range(1, n + 1):
        mover.location = (0, -dist[f - 1], RZ)
        mover.keyframe_insert("location", frame=f)

    # --- light: dim night sky + a soft key fixed to the car so the red reads between bars ---------------------------
    for f in range(1, n + 1):                              # oncoming traffic: 24 m/s of its own on top of the road's slide
        onc.location = (0, -24.0 * (f - 1) / fps, 0)
        onc.keyframe_insert("location", frame=f)
    for nm, loc, e, size in (("key", (-4.5, 3.0, 5.0), 900, 5.0), ("rim", (4.0, -5.0, 3.0), 500, 4.0)):
        L = bpy.data.lights.new(nm, "AREA")
        L.energy = e * spec.get("key_scale", 1.0)
        L.size = size
        lo = bpy.data.objects.new(nm, L)
        sc.collection.objects.link(lo)
        lo.location = loc
        lo.rotation_euler = (Vector((0, 0, 0.6)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()

    # --- camera -----------------------------------------------------------------------------------------------------
    cd = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cd)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cd.sensor_fit = "HORIZONTAL"
    cd.sensor_width = spec.get("sensor", 24.0)
    cd.clip_start, cd.clip_end = 0.05, 3000
    keys = spec["camera"]
    pull = spec.get("pull", [])
    for f in range(1, n + 1):
        t = (f - 1) / max(1, n - 1)
        Mx = shot3.cam_matrix(shot3.interp(keys, t, "az", 30), shot3.interp(keys, t, "el", 8), shot3.interp(keys, t, "dist", 7),
                              shot3.interp(keys, t, "target", [0, 0, 0.55]), shot3.interp(keys, t, "roll", 0))
        py = shot3.interp(pull, t, "y", 0.0)
        if py:                                  # camera falls behind and keeps aiming at the car
            loc = Mx.translation + Vector((0, -py, 0))
            tgt = Vector(shot3.interp(keys, t, "target", [0, 0, 0.55]))
            Mx = Matrix.Translation(loc) @ (tgt - loc).to_track_quat("-Z", "Y").to_matrix().to_4x4()
        cam.matrix_world = Mx
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.lens = shot3.interp(keys, t, "lens", 50)
        cd.keyframe_insert("lens", frame=f)

    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.cycles.caustics_reflective = sc.cycles.caustics_refractive = False
    sc.render.use_motion_blur = spec.get("motion_blur", True)
    sc.render.motion_blur_shutter = spec.get("shutter", 0.4)
    sc.render.use_persistent_data = False
    sc.render.resolution_x, sc.render.resolution_y = spec.get("res", [1080, 1920])
    sc.render.resolution_percentage = res_pct
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = spec.get("exposure", 0.0)
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    os.makedirs(out, exist_ok=True)
    for f in (only or range(1, n + 1)):
        path = os.path.join(out, f"f_{f:04d}.png")
        if os.path.exists(path) and not only:
            continue
        sc.frame_set(f)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        print("IVE_FRAME", f, flush=True)
    print("IVE_SHOT_DONE", out)


if __name__ == "__main__":
    main()
