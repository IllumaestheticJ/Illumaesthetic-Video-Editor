"""v0 preview renderer for bf-scan-teardown-prices (Ron's frame: front -Y, car's left +X, z up, metres).

    blender -b scene_v0.blend -P render_v0.py -- <shot T1|T2|STILL> <out_dir> [pct] [spp] [fps] [t0] [t1] [step]

Times are SONG seconds (the music starts at video 0). Parts carry keyed offsets; cameras are keyed loc/target/focal.
Quick draft: Cycles CPU, low samples + OIDN, silver house look (blender/scan_render.py)."""
import math, os, sys
import bpy
from mathutils import Vector, Matrix
sys.path.insert(0, "/home/user/Illumaesthetic-Video-Editor/blender")
import scan_render as sr  # noqa

a = sys.argv[sys.argv.index("--") + 1:]
SHOT, OUT = a[0], a[1]
PCT = int(a[2]) if len(a) > 2 else 50
SPP = int(a[3]) if len(a) > 3 else 16
FPS = float(a[4]) if len(a) > 4 else 15

# ---------------------------------------------------------------- timing (song s, measured: grid 0.024 + 0.5374 k)
UNLOCK, LIP, SKIRT, REAR, WING = 2.159, 4.296, 6.432, 9.381, 11.262
CUT1 = 13.398           # T1 -> T2 (measured onset)
HOME0, LOCK = 14.466, 17.235   # fly home starts / locks on the kick entry (beat 32)
CUT2 = 19.390           # T2 -> Ron render (kick)
SWEEP0, SWEEP1 = 0.813, 2.159  # Eps scan line, first hit -> unlock


def ease(u, k="inout"):
    u = min(1, max(0, u))
    return {"in": u ** 3, "out": 1 - (1 - u) ** 3, "lin": u}.get(k, u * u * (3 - 2 * u))


def path(keys, t):
    """keys: [(t, value(list), ease)] -> eased piecewise value"""
    if t <= keys[0][0]:
        return keys[0][1]
    for (ta, va, _), (tb, vb, e) in zip(keys, keys[1:]):
        if t <= tb:
            k = ease((t - ta) / max(1e-9, tb - ta), e)
            return [x + (y - x) * k for x, y in zip(va, vb)]
    return keys[-1][1]


Z = [0, 0, 0]
U = 0.02  # unlock lift
def unlock(t0):
    return [(0, Z, "lin"), (UNLOCK, Z, "lin"), (UNLOCK + 0.15, [0, 0, U], "out"), (UNLOCK + 0.5, Z, "inout")]


PARK = {"kit_lip": [0.45, -0.55, -0.32], "kit_skirt_L": [0.80, 0, -0.18], "kit_skirt_R": [-0.80, 0, -0.18],
        "kit_rear": [0, 0.80, -0.24], "kit_wing": [0, 0, 0.95]}
OFF = {
    "kit_lip": unlock(0) + [(LIP, Z, "lin"), (LIP + 0.25, [0, -0.06, -0.06], "out"), (LIP + 1.3, PARK["kit_lip"], "inout")],
    "kit_skirt_L": unlock(0) + [(SKIRT, Z, "lin"), (SKIRT + 0.25, [0.15, 0, 0], "out"), (SKIRT + 1.2, PARK["kit_skirt_L"], "inout")],
    "kit_skirt_R": unlock(0) + [(SKIRT, Z, "lin"), (SKIRT + 0.25, [-0.15, 0, 0], "out"), (SKIRT + 1.2, PARK["kit_skirt_R"], "inout")],
    "kit_rear": unlock(0) + [(REAR, Z, "lin"), (REAR + 0.25, [0, 0, -0.06], "out"), (REAR + 1.2, PARK["kit_rear"], "inout")],
    "kit_wing": unlock(0) + [(WING, Z, "lin"), (WING + 1.1, PARK["kit_wing"], "inout")],
}
# fly home: staggered starts, ALL lock on the kick (LOCK); ease "in" so they slam home
for i, n in enumerate(["kit_lip", "kit_skirt_L", "kit_skirt_R", "kit_rear", "kit_wing"]):
    st = HOME0 + [0, 0.27, 0.27, 0.54, 0.81][i]
    OFF[n] += [(st, PARK[n], "lin"), (LOCK, Z, "in")]

C = (0.0, 0.30, 0.55)
CAM = {
    "T1": [  # one take round the car's LEFT (+X): front-left -> left side -> rear-left -> above the deck
        (0.0, dict(loc=(3.5, -5.5, 1.9), tgt=(0, 0.45, 0.55), f=27), "lin"),
        (UNLOCK + 0.6, dict(loc=(3.1, -4.9, 1.6), tgt=(0, 0.2, 0.5), f=28), "inout"),
        (LIP + 0.1, dict(loc=(2.6, -4.9, 1.0), tgt=(0.3, -1.5, 0.25), f=26), "inout"),
        (SKIRT - 0.3, dict(loc=(2.9, -4.4, 1.0), tgt=(0.4, -1.3, 0.25), f=26), "inout"),
        (SKIRT + 0.2, dict(loc=(4.3, -0.7, 0.85), tgt=(0.7, 0.4, 0.4), f=26), "inout"),
        (REAR - 0.4, dict(loc=(4.2, 1.4, 0.85), tgt=(0.6, 0.9, 0.4), f=26), "inout"),
        (REAR + 0.1, dict(loc=(3.0, 6.1, 1.1), tgt=(0.1, 2.6, 0.35), f=26), "inout"),
        (WING - 0.2, dict(loc=(2.9, 6.0, 1.25), tgt=(0, 2.4, 0.6), f=26), "inout"),
        (WING + 1.0, dict(loc=(2.9, 6.1, 2.4), tgt=(0, 2.0, 1.2), f=26), "inout"),
        (CUT1 + 0.2, dict(loc=(3.0, 6.3, 2.55), tgt=(0, 2.0, 1.2), f=26), "inout"),
    ],
    "T2": [  # near-top exploded view (nose up), then down to the render-7 (Camera.006) direction for the 1:1 cut
        (CUT1, dict(loc=(1.9, 1.0, 9.4), tgt=(0, 1.0, 0.3), f=28, up=(0, -1, 0)), "lin"),   # v0.2: wider + content shifted up into the safe band (knowledge/safe-zones.md)
        (HOME0, dict(loc=(1.7, 1.0, 9.0), tgt=(0, 1.0, 0.3), f=28, up=(0, -1, 0)), "inout"),
        (HOME0 + 1.3, dict(loc=(5.2, 8.6, 5.0), tgt=(0, 0.4, 0.5), f=40, up=(0, 0.5, 1)), "inout"),
        (LOCK, "END", "inout"),
        (CUT2 + 0.1, "END", "lin"),
    ],
}


def cam_end():
    c = bpy.data.objects.get("Camera.006(L5)")
    return c.matrix_world.copy()


def setup():
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = SPP
    sc.cycles.use_denoising = True
    sc.cycles.use_adaptive_sampling = True
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, PCT
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "AgX"
    sc.render.use_persistent_data = False
    sr.studio_world((0.004, 0.004, 0.004, 1), False)
    car = bpy.data.objects["FE1 Fl"]
    silver = sr.mat_silver()
    # scan line: cyan emission band sweeping nose -> tail along Y, added on top of the silver
    nt = silver.node_tree
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    surf = out.inputs[0].links[0].from_socket
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    front = nt.nodes.new("ShaderNodeValue"); front.name = "sweep_front"
    d = nt.nodes.new("ShaderNodeMath"); d.operation = "SUBTRACT"
    nt.links.new(sep.outputs[1], d.inputs[0]); nt.links.new(front.outputs[0], d.inputs[1])
    ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"; nt.links.new(d.outputs[0], ab.inputs[0])
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 0.012
    nt.links.new(ab.outputs[0], lt.inputs[0])
    em = sr.emission(nt, (0.435, 0.765, 0.839, 1), 30.0)
    mix = nt.nodes.new("ShaderNodeMixShader"); nt.links.new(lt.outputs[0], mix.inputs[0])
    nt.links.new(surf, mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs[0])
    car.data.materials.clear(); car.data.materials.append(silver)
    m, knt, kout = sr.new_mat("kit_pu")  # unpainted PU / gloss black, kept readable on black by a cool rim
    p = sr.principled(knt, (0.018, 0.019, 0.021, 1), 0.42, 0.0)
    knt.links.new(p.outputs[0], kout.inputs[0])
    for n in PARK:
        o = bpy.data.objects[n]; o.data.materials.clear(); o.data.materials.append(m); o["rest"] = list(o.location)
    gold, gnt, gout = sr.new_mat("rim_gold"); g = sr.principled(gnt, (0.62, 0.42, 0.14, 1), 0.3, 1.0); gnt.links.new(g.outputs[0], gout.inputs[0])
    rub, rnt, rout = sr.new_mat("rubber"); r = sr.principled(rnt, (0.03, 0.03, 0.03, 1), 0.7, 0.0); rnt.links.new(r.outputs[0], rout.inputs[0])
    for o in bpy.data.objects:
        if o.name.startswith("wheel_"):
            for i, sl in enumerate(o.material_slots):
                sl.material = gold if i == 0 else rub
    lo = Vector((-1.2, -2.2, 0.0)); hi = Vector((1.2, 2.8, 1.6))
    root = bpy.data.objects.new("SCAN_ROOT", None); sc.collection.objects.link(root); root.location = (lo + hi) / 2
    sr.studio_lights(lo, hi)
    sr.add_light("kit_rim", "AREA", Vector((0, 0, 4.5)), 400, 4.0, (0.8, 0.9, 1.0))
    cam = bpy.data.objects.new("v0cam", bpy.data.cameras.new("v0cam")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.sensor_fit = "HORIZONTAL"; cam.data.sensor_width = 20.25; cam.data.clip_start = 0.05
    return cam, front


def look(loc, tgt, up=(0, 0, 1)):
    f = (Vector(tgt) - Vector(loc)).normalized(); u = Vector(up)
    r = f.cross(u).normalized(); u2 = r.cross(f)
    m = Matrix(((r.x, u2.x, -f.x), (r.y, u2.y, -f.y), (r.z, u2.z, -f.z)))
    return m.to_quaternion()


def cam_at(keys, t):
    """keyed camera, interpolating loc / target / up / focal (so blends always look at the subject).
    'END' = the render-7 pose: Camera.006(L5) position and direction, lens fitted to portrait."""
    def pose(v):
        if v == "END":
            mw = cam_end(); r = mw.to_3x3()
            fwd = -(r @ Vector((0, 0, 1))); up = r @ Vector((0, 1, 0))
            return mw.translation.copy(), mw.translation + fwd * 15.0, up, END_F
        return Vector(v["loc"]), Vector(v["tgt"]), Vector(v.get("up", (0, 0, 1))), v["f"]
    def res(l, g, u, f):
        return l, look(l, g, u.normalized()), f
    if t <= keys[0][0]:
        return res(*pose(keys[0][1]))
    for (ta, va, _), (tb, vb, e) in zip(keys, keys[1:]):
        if t <= tb:
            k = ease((t - ta) / max(1e-9, tb - ta), e)
            A, B = pose(va), pose(vb)
            return res(A[0].lerp(B[0], k), A[1].lerp(B[1], k), A[2].lerp(B[2], k), A[3] + (B[3] - A[3]) * k)
    return res(*pose(keys[-1][1]))


END_F = 72.0


def main():
    cam, front = setup()
    sc = bpy.context.scene
    if SHOT == "STILL":   # quick framing check at given song times
        times = [float(x) for x in a[5].split(",")]
    else:
        t0, t1 = (CUT1 if SHOT == "T2" else 0.0), (CUT2 if SHOT == "T2" else CUT1)
        if len(a) > 6:
            t0, t1 = float(a[5]), float(a[6])
        n = int(round((t1 - t0) * FPS)) + 1
        times = [t0 + i / FPS for i in range(n)]
    os.makedirs(OUT, exist_ok=True)
    keys = CAM["T2" if SHOT == "T2" or (SHOT == "STILL" and len(a) > 6 and a[6] == "T2") else "T1"]
    if SHOT == "STILL" and len(a) > 6 and a[6] == "T2": keys = CAM["T2"]
    for i, t in enumerate(times):
        for n, ks in OFF.items():
            o = bpy.data.objects[n]; o.location = Vector(o["rest"]) + Vector(path(ks, t))
        y = -2.3 + (t - SWEEP0) / (SWEEP1 - SWEEP0) * 5.2 if SWEEP0 <= t <= SWEEP1 else 99.0
        front.outputs[0].default_value = y
        l, q, f = cam_at(keys, t)
        cam.location = l; cam.rotation_mode = "QUATERNION"; cam.rotation_quaternion = q; cam.data.lens = f
        name = f"{SHOT}_{t:07.3f}.png" if SHOT == "STILL" else f"f{i:04d}.png"
        sc.render.filepath = os.path.join(OUT, name)
        bpy.ops.render.render(write_still=True)
        print("FRAME", i, round(t, 3), flush=True)


main()
