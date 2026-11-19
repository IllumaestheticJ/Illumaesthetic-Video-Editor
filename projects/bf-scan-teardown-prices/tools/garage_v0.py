"""Plain warehouse-garage set (user 2026-11-18: "plain background instead of black, like a warehouse car garage").
Procedural, no downloads: polished concrete floor, plain grey walls, rows of LED tube lights.
The room is aligned to a camera's yaw around the car at the origin, so the back wall faces the lens.
Used by ron_still_v0.py / ron_mask_v0.py (GARAGE=1) and importable for the scan shots."""
import bpy, math
from mathutils import Vector

def _mat(name, base, rough, noise=0.0, emit=None, strength=0.0, spec=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; p = nt.nodes["Principled BSDF"]
    p.inputs["Specular IOR Level"].default_value = spec   # low on the floor: grazing camera (0.38 m) turns it into a mirror
    p.inputs["Base Color"].default_value = (*base, 1); p.inputs["Roughness"].default_value = rough
    if noise:   # subtle concrete mottling
        tx = nt.nodes.new("ShaderNodeTexNoise"); tx.inputs["Scale"].default_value = 6.0; tx.inputs["Detail"].default_value = 8.0
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*[c * (1 - noise) for c in base], 1); ramp.color_ramp.elements[1].color = (*[min(1, c * (1 + noise)) for c in base], 1)
        nt.links.new(tx.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
        rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs[3].default_value = rough * 0.7; rr.inputs[4].default_value = rough * 1.4
        nt.links.new(tx.outputs["Fac"], rr.inputs[0]); nt.links.new(rr.outputs[0], p.inputs["Roughness"])
    if emit:
        p.inputs["Emission Color"].default_value = (*emit, 1); p.inputs["Emission Strength"].default_value = strength
    return m

def _box(name, size, loc, mat, parent, coll):
    me = bpy.data.meshes.new(name); o = bpy.data.objects.new(name, me); coll.objects.link(o)
    sx, sy, sz = [s / 2 for s in size]
    v = [(x, y, z) for x in (-sx, sx) for y in (-sy, sy) for z in (-sz, sz)]
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me.from_pydata(v, [], f); me.materials.append(mat); o.location = loc; o.parent = parent
    return o

def build(cam, back=9.0, front=22.0, half_w=12.0, height=5.6, floor_z=0.0, band=False, floor_base=(0.06, 0.06, 0.058),
          floor_rough=0.3, floor_spec=0.3, scan=False, wall_base=(0.24, 0.24, 0.235), wall_spec=0.5):
    """v0.12 (user: "the car is floating"): floor top at the tyre contact height (floor_z), no dark wall band at
    tyre level, a faint polished sheen so the tyres reflect. scan=True: ceiling never seen by the camera (the T2 top
    view starts above it); LED tubes are made camera-invisible per frame by the renderer when the lens is above them."""
    sc = bpy.context.scene
    coll = bpy.data.collections.new("GARAGE"); sc.collection.children.link(coll)
    d = Vector((-cam.location.x, -cam.location.y, 0)).normalized()          # camera -> car, horizontal
    yaw = math.atan2(d.y, d.x) - math.pi / 2                                 # room +Y axis = away from camera
    root = bpy.data.objects.new("garage_root", None); coll.objects.link(root); root.rotation_euler = (0, 0, yaw + math.pi); root.location.z = floor_z
    floor = _mat("g_floor", floor_base, floor_rough, noise=0.25, spec=floor_spec)
    wall = _mat("g_wall", wall_base, 0.85, noise=0.05, spec=wall_spec)
    band_m = _mat("g_band", (0.10, 0.10, 0.10), 0.7)
    ceil = _mat("g_ceil", (0.06, 0.06, 0.06), 0.9)
    led = _mat("g_led", (1, 1, 1), 0.5, emit=(1.0, 0.97, 0.92), strength=15.0)
    t = 0.2
    L = back + front; cy = (front - back) / 2          # room spans y in [-front, back] in root space (root -Y = toward camera)
    _box("g_floor", (2 * half_w, L, t), (0, cy, -t / 2 - 0.001), floor, root, coll)
    cz = _box("g_ceiling", (2 * half_w, L, t), (0, cy, height + t / 2), ceil, root, coll)
    if scan: cz.visible_camera = False
    _box("g_wall_back", (2 * half_w, t, height), (0, -back - t / 2, height / 2), wall, root, coll)
    _box("g_wall_front", (2 * half_w, t, height), (0, front + t / 2, height / 2), wall, root, coll)
    for s in (-1, 1):
        _box(f"g_wall_side{s}", (t, L, height), (s * (half_w + t / 2), cy, height / 2), wall, root, coll)
    # dark lower band (1.1 m) on the back + side walls, a plain workshop detail
    if band: _box("g_band_back", (2 * half_w, 0.02, 1.1), (0, -back + 0.01, 0.55), band_m, root, coll)
    for s in (-1, 1) if band else ():
        _box(f"g_band_side{s}", (0.02, L, 1.1), (s * (half_w - 0.01), cy, 0.55), band_m, root, coll)
    # LED tube rows running toward the back wall (perspective lines + long highlights in the paint)
    for x in (-6.0, -2.0, 2.0, 6.0):
        for k in range(6):
            o = _box(f"g_led_{x}_{k}", (0.12, 2.4, 0.05), (x, front - 2.5 - k * ((L - 4) / 6), height - 0.05), led, root, coll); o["led"] = 1
    sc.view_layers[0].update()
    return coll
