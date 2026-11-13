"""Night-city expressway for tools/cgi_drive.py (v4: the v3 road was "very low detail" - a flat plane, light bars, 60 boxes).

build(sc, mover, spec, LEN) parents everything to `mover` (the road slides toward -Y under the car, car lane centre x=0):
  wet patched asphalt with tar seams + lane paint + cat's-eyes | concrete barriers with rail and reflectors | lamp posts with
  real warm spots (light pools sweep over the paint) | gantry signs and two overpasses | opposite carriageway with oncoming
  headlights | near row of low buildings with shopfront signs, far row of towers (punched windows / lit office floors,
  roof plant, red beacons) | horizon-glow sky.  Geometry is batched: one mesh per material.
"""
import math, random
import bpy
from mathutils import Vector


class Batch:
    def __init__(self):
        self.v, self.f = [], []

    def box(self, size, loc):
        sx, sy, sz = (s / 2 for s in size); x, y, z = loc; b = len(self.v)
        self.v += [(x + dx * sx, y + dy * sy, z + dz * sz) for dz in (-1, 1) for dy in (-1, 1) for dx in (-1, 1)]
        self.f += [tuple(b + i for i in q) for q in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5))]

    def quad(self, p0, p1, p2, p3):
        b = len(self.v); self.v += [p0, p1, p2, p3]; self.f.append((b, b + 1, b + 2, b + 3))

    def obj(self, sc, name, mat, parent):
        me = bpy.data.meshes.new(name); me.from_pydata(self.v, [], self.f); me.materials.append(mat)
        o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); o.parent = parent
        return o


def emit(name, rgb, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    e.inputs["Color"].default_value = (*rgb, 1); e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs[0], o.inputs["Surface"]); return m


def pbr(name, rgb, rough, metal=0.0, noise=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; p = nt.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*rgb, 1); p.inputs["Roughness"].default_value = rough; p.inputs["Metallic"].default_value = metal
    if noise:                                             # (scale, colour variation, bump)
        tc = nt.nodes.new("ShaderNodeTexCoord"); n = nt.nodes.new("ShaderNodeTexNoise")
        n.inputs["Scale"].default_value = noise[0]; n.inputs["Detail"].default_value = 8
        nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
        mx = nt.nodes.new("ShaderNodeMixRGB"); mx.blend_type = "MULTIPLY"; mx.inputs["Fac"].default_value = noise[1]
        mx.inputs["Color1"].default_value = (*rgb, 1); nt.links.new(n.outputs["Color"], mx.inputs["Color2"])
        nt.links.new(mx.outputs[0], p.inputs["Base Color"])
        b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = noise[2]
        nt.links.new(n.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs[0], p.inputs["Normal"])
    return m


def asphalt_mat():
    m = bpy.data.materials.new("asphalt"); m.use_nodes = True; nt = m.node_tree; L = nt.links
    p = nt.nodes.get("Principled BSDF"); tc = nt.nodes.new("ShaderNodeTexCoord")

    def noise(scale, detail, stretch=None):
        n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail
        if stretch:
            mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = stretch
            L.new(tc.outputs["Object"], mp.inputs["Vector"]); L.new(mp.outputs[0], n.inputs["Vector"])
        else:
            L.new(tc.outputs["Object"], n.inputs["Vector"])
        return n

    def rng(src, a, b, lo, hi):
        r = nt.nodes.new("ShaderNodeMapRange"); r.inputs["From Min"].default_value = a; r.inputs["From Max"].default_value = b
        r.inputs["To Min"].default_value = lo; r.inputs["To Max"].default_value = hi; L.new(src, r.inputs["Value"]); return r

    grain = noise(140, 4)                                  # aggregate
    patch = noise(0.35, 5)                                 # repaired patches / wear, metres across
    wet = noise(0.12, 3, (1.0, 0.25, 1.0))                 # long damp streaks along the lanes
    wheel = nt.nodes.new("ShaderNodeTexWave"); wheel.inputs["Scale"].default_value = 0.2857   # tyre-polished tracks every 3.5 m
    wheel.inputs["Distortion"].default_value = 0.6; L.new(tc.outputs["Object"], wheel.inputs["Vector"])
    col = nt.nodes.new("ShaderNodeMixRGB"); col.inputs["Color1"].default_value = (0.012, 0.012, 0.013, 1)
    col.inputs["Color2"].default_value = (0.034, 0.033, 0.032, 1); L.new(rng(patch.outputs["Fac"], 0.35, 0.65, 0, 1).outputs[0], col.inputs["Fac"])
    col2 = nt.nodes.new("ShaderNodeMixRGB"); col2.blend_type = "MULTIPLY"; col2.inputs["Fac"].default_value = 0.5
    L.new(col.outputs[0], col2.inputs["Color1"]); L.new(grain.outputs["Color"], col2.inputs["Color2"]); L.new(col2.outputs[0], p.inputs["Base Color"])
    r1 = rng(wet.outputs["Fac"], 0.42, 0.62, 0.5, 0.1)       # damp = glossy: lamps and tail-lights streak in it
    r2 = nt.nodes.new("ShaderNodeMath"); r2.operation = "MULTIPLY"; L.new(r1.outputs[0], r2.inputs[0])
    L.new(rng(wheel.outputs["Fac"], 0, 1, 0.8, 1.15).outputs[0], r2.inputs[1]); L.new(r2.outputs[0], p.inputs["Roughness"])
    seam = nt.nodes.new("ShaderNodeTexVoronoi"); seam.feature = "DISTANCE_TO_EDGE"; seam.inputs["Scale"].default_value = 0.22
    L.new(tc.outputs["Object"], seam.inputs["Vector"])
    h = nt.nodes.new("ShaderNodeMath"); h.operation = "ADD"; L.new(grain.outputs["Fac"], h.inputs[0])
    L.new(rng(seam.outputs["Distance"], 0.0, 0.006, -0.8, 0.0).outputs[0], h.inputs[1])      # tar seams / cracks
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.18; b.inputs["Distance"].default_value = 0.02
    L.new(h.outputs[0], b.inputs["Height"]); L.new(b.outputs[0], p.inputs["Normal"])
    return m


def sky(sc, strength):
    w = bpy.data.worlds.new("night"); w.use_nodes = True; nt = w.node_tree; bg = nt.nodes["Background"]
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    e = ramp.color_ramp.elements; e[0].position = 0.0; e[0].color = (0.05, 0.028, 0.03, 1)       # sodium glow on the horizon
    e[1].position = 0.45; e[1].color = (0.004, 0.007, 0.02, 1)
    k = ramp.color_ramp.elements.new(0.12); k.color = (0.022, 0.016, 0.034, 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = strength
    sc.world = w


def build(sc, mover, spec, LEN=1180.0, seed=7):
    rnd = random.Random(seed); Y0 = -430.0      # 430 m behind the start: the front shot looks back down the road
    B = {k: Batch() for k in ("road", "paint", "paint_y", "conc", "steel", "eye", "amber", "lamp", "bldg", "bldg2", "glass",
                              "win_w", "win_c", "win_o", "red", "sign_g", "sign_w", "neon_c", "neon_m", "neon_y", "head", "dark", "shop_w", "shop_c")}
    # ---- carriageway: 3 lanes (edges -5.25 / 5.25, car in the middle lane), shoulders, opposite carriageway on the left
    B["road"].box((40.0, LEN, 0.02), (-8.0, Y0 + LEN / 2, -0.012))
    for x in (-5.25, 5.25):
        B["paint"].box((0.15, LEN, 0.004), (x, Y0 + LEN / 2, 0.003))
    B["paint_y"].box((0.15, LEN, 0.004), (-6.6, Y0 + LEN / 2, 0.003))
    for x in (-21.5, -11.0):
        B["paint"].box((0.15, LEN, 0.004), (x, Y0 + LEN / 2, 0.003))
    y = Y0
    while y < Y0 + LEN:
        for x in (-1.75, 1.75, -14.5, -18.0):
            B["paint"].box((0.15, 3.0, 0.004), (x, y, 0.003))
            B["eye"].box((0.10, 0.10, 0.02), (x, y + 6.0, 0.012))
        y += 12.0
    # ---- barriers: right shoulder, median, far side; steel rail on top, amber reflectors
    for x in (7.4, -8.0, -24.4):
        B["conc"].box((0.62, LEN, 0.45), (x, Y0 + LEN / 2, 0.225)); B["conc"].box((0.30, LEN, 0.45), (x, Y0 + LEN / 2, 0.675))
        B["steel"].box((0.08, LEN, 0.08), (x, Y0 + LEN / 2, 1.08))
        y = Y0
        while y < Y0 + LEN:
            B["steel"].box((0.06, 0.06, 0.2), (x, y, 0.98)); B["amber"].box((0.02, 0.12, 0.08), (x - 0.17 if x > 0 else x + 0.17, y + 2, 0.72))
            y += 4.0
    # ---- lamp posts (right verge and median), alternating, with real spots
    lamps = []
    y = Y0 + 10; i = 0
    while y < Y0 + LEN:
        x, s = ((9.0, -1) if i % 2 == 0 else (-8.0, 1))
        B["steel"].box((0.22, 0.22, 10.0), (x, y, 5.0)); B["steel"].box((3.4, 0.14, 0.14), (x + s * 1.6, y, 10.0))
        B["lamp"].box((0.9, 0.34, 0.08), (x + s * 3.0, y, 9.9)); lamps.append((x + s * 3.0, y, 9.8))
        if i % 2:                                         # median posts carry a second arm over the opposite lanes
            B["steel"].box((3.4, 0.14, 0.14), (x - 1.6, y, 10.0)); B["lamp"].box((0.9, 0.34, 0.08), (x - 3.0, y, 9.9)); lamps.append((x - 3.0, y, 9.8))
        y += 19.0; i += 1
    # ---- gantry signs and overpasses
    for y in (130.0, 330.0, 560.0):
        for x in (-8.0, 9.2):
            B["steel"].box((0.35, 0.35, 7.6), (x, y, 3.8))
        B["steel"].box((17.6, 0.3, 0.5), (0.6, y, 7.4)); B["steel"].box((17.6, 0.3, 0.12), (0.6, y, 6.6))
        for x, w in ((-3.2, 4.6), (2.6, 5.4)):
            B["sign_g"].box((w, 0.08, 2.3), (x, y - 0.2, 8.6)); B["sign_g"].box((w, 0.08, 2.3), (x, y + 0.2, 8.6))
            for r in range(3):
                for yy in (y - 0.26, y + 0.26):
                    B["sign_w"].box((w * rnd.uniform(0.45, 0.8), 0.02, 0.26), (x, yy, 9.25 - r * 0.62))
    for y in (235.0, 455.0):
        B["conc"].box((80.0, 13.0, 1.5), (-8.0, y, 7.6)); B["conc"].box((80.0, 0.3, 1.0), (-8.0, y - 6.5, 8.8)); B["conc"].box((80.0, 0.3, 1.0), (-8.0, y + 6.5, 8.8))
        for x in (-25.6, -8.0, 8.6):
            B["conc"].box((1.3, 9.0, 6.9), (x, y, 3.45))
        for x in (-16.0, -3.5, 0.0, 3.5):
            B["lamp"].box((0.3, 9.0, 0.06), (x, y, 6.8))
        lamps += [(0.0, y, 6.7), (-16.0, y, 6.7)]
    # ---- buildings: near row (shops, low blocks) and far row (towers)
    def windows(x0, x1, y0, y1, h, style, k):
        """lit openings on all four faces; style 0 = punched windows, 1 = office floors (long bands), 2 = dark glass, few lit"""
        dz = 3.3 if style != 1 else 3.9
        faces = [((x0 - 0.06, None), y0, y1, "x"), ((x1 + 0.06, None), y0, y1, "x"), ((None, y0 - 0.06), x0, x1, "y"), ((None, y1 + 0.06), x0, x1, "y")]
        for (fx, fy), a, b, ax in faces:
            nf = int(h // dz)
            for zi in range(1, nf):
                z = zi * dz + 0.9
                if style == 1:
                    if rnd.random() < 0.3:
                        continue
                    u = a + 0.6
                    while u < b - 1.0:
                        w = min(rnd.uniform(3, 14), b - 0.6 - u)
                        if rnd.random() < 0.7:
                            q = [(u, z), (u + w, z), (u + w, z + 1.5), (u, z + 1.5)]
                            B[k if rnd.random() < 0.85 else "win_w"].quad(*[((fx, p, zz) if ax == "x" else (p, fy, zz)) for p, zz in q])
                        u += w + rnd.choice((0.3, 0.3, 2.4))
                else:
                    u = a + 0.9; lit = 0.5 if style == 0 else 0.16
                    while u < b - 1.7:
                        if rnd.random() < lit:
                            q = [(u, z), (u + 1.4, z), (u + 1.4, z + 1.7), (u, z + 1.7)]
                            kk = k if rnd.random() < 0.7 else rnd.choice(("win_w", "win_c", "win_o"))
                            B[kk].quad(*[((fx, p, zz) if ax == "x" else (p, fy, zz)) for p, zz in q])
                        u += 2.5

    for side in (1, -1):
        edge = 12.0 if side == 1 else -27.5              # verge ends here
        yb = Y0
        while yb < Y0 + LEN - 10:                          # near row: continuous street wall, 9-40 m
            d = rnd.uniform(14, 34); w = rnd.uniform(14, 24); h = rnd.choice((9, 12, 15, 20, 26, 33, 40)) * rnd.uniform(0.9, 1.1)
            x0 = edge + side * rnd.uniform(0.5, 4.0); x1 = x0 + side * w; xa, xb = min(x0, x1), max(x0, x1)
            mat = rnd.choice(("bldg", "bldg2", "glass"))
            B[mat].box((w, d, h), ((xa + xb) / 2, yb + d / 2, h / 2))
            B["dark"].box((w * 0.5, d * 0.4, 1.6), ((xa + xb) / 2, yb + d / 2, h + 0.8))         # roof plant
            if rnd.random() < 0.5:
                B["steel"].box((0.12, 0.12, rnd.uniform(4, 9)), (xa + w * 0.3, yb + d * 0.3, h + 3))
            windows(xa, xb, yb, yb + d, h, 2 if mat == "glass" else rnd.choice((0, 0, 1)), rnd.choice(("win_w", "win_w", "win_c", "win_o")))
            xf = x0 - side * 0.12                          # shopfront strip + sign on the road face
            u = yb + 0.8; sk = rnd.choice(("shop_w", "shop_c"))       # shopfront bays with mullions, a third of them shut
            while u < yb + d - 3.0:
                if rnd.random() < 0.65:
                    B[sk].quad((xf, u, 0.7), (xf, u + 2.4, 0.7), (xf, u + 2.4, 2.9), (xf, u, 2.9))
                u += 2.8
            if rnd.random() < 0.75:
                sw = rnd.uniform(4, min(12, d - 2)); sy = yb + rnd.uniform(1, d - sw - 1); sz = rnd.uniform(4.2, min(h - 2, 14)); sh = rnd.uniform(0.9, 2.2)
                B[rnd.choice(("neon_c", "neon_m", "neon_y", "red"))].quad((xf - side * 0.1, sy, sz), (xf - side * 0.1, sy + sw, sz), (xf - side * 0.1, sy + sw, sz + sh), (xf - side * 0.1, sy, sz + sh))
            if rnd.random() < 0.3:                         # vertical blade sign
                B[rnd.choice(("neon_c", "neon_m", "neon_y"))].box((0.9, 0.2, rnd.uniform(5, 11)), (xf - side * 0.6, yb + rnd.uniform(1, d - 1), rnd.uniform(8, max(9, h - 6))))
            yb += d + rnd.choice((0.0, 0.0, 3.0, 9.0))
        yb = Y0
        while yb < Y0 + LEN:                               # far row: towers 50-190 m
            d = rnd.uniform(22, 40); w = rnd.uniform(22, 38); h = rnd.uniform(50, 190)
            x0 = edge + side * rnd.uniform(34, 95); xa, xb = sorted((x0, x0 + side * w))
            mat = rnd.choice(("glass", "glass", "bldg2"))
            B[mat].box((w, d, h), ((xa + xb) / 2, yb + d / 2, h / 2))
            if rnd.random() < 0.6:                         # setback crown
                B[mat].box((w * 0.6, d * 0.6, h * 0.12), ((xa + xb) / 2, yb + d / 2, h * 1.06)); top = h * 1.12
            else:
                top = h
            B["steel"].box((0.3, 0.3, 12), ((xa + xb) / 2, yb + d / 2, top + 6)); B["red"].box((0.7, 0.7, 0.7), ((xa + xb) / 2, yb + d / 2, top + 12.3))
            for cx in (xa, xb):
                for cy in (yb, yb + d):
                    B["red"].box((0.5, 0.5, 0.5), (cx, cy, h + 0.3))
            windows(xa, xb, yb, yb + d, h, rnd.choice((1, 1, 2, 0)), rnd.choice(("win_w", "win_c", "win_c", "win_o")))
            yb += d + rnd.uniform(4, 30)
    # ---- oncoming traffic on the opposite carriageway (own mover: closes at car speed + its own)
    onc = bpy.data.objects.new("oncoming", None); sc.collection.objects.link(onc); onc.parent = mover
    Bh, Bd = Batch(), Batch()
    for j in range(26):
        x = rnd.choice((-12.75, -16.25, -19.75)); y = Y0 + 380 + j * rnd.uniform(34, 60) + j * 30
        Bd.box((1.8, 4.4, 1.25), (x, y, 0.78))
        for dx in (-0.62, 0.62):
            Bh.box((0.28, 0.06, 0.14), (x + dx, y - 2.22, 0.68))
    MAT = {
        "road": asphalt_mat(), "paint": pbr("paint_w", (0.62, 0.62, 0.58), 0.55), "paint_y": pbr("paint_y", (0.7, 0.5, 0.06), 0.55),
        "conc": pbr("concrete", (0.11, 0.108, 0.1), 0.85, noise=(3.0, 0.55, 0.25)), "steel": pbr("steel", (0.16, 0.17, 0.18), 0.38, 1.0),
        "eye": emit("catseye", (1.0, 0.95, 0.8), 1.2), "amber": emit("reflector", (1.0, 0.42, 0.06), 4.0), "lamp": emit("lamp", (1.0, 0.62, 0.3), 55.0),
        "bldg": pbr("facade_a", (0.03, 0.028, 0.03), 0.7, noise=(0.6, 0.5, 0.1)), "bldg2": pbr("facade_b", (0.018, 0.02, 0.026), 0.55, noise=(0.4, 0.4, 0.05)),
        "glass": pbr("curtain_wall", (0.008, 0.012, 0.02), 0.06, 0.9), "dark": pbr("roofplant", (0.012, 0.012, 0.014), 0.8),
        "win_w": emit("win_warm", (1.0, 0.66, 0.32), 1.5), "win_c": emit("win_cool", (0.5, 0.72, 1.0), 1.2), "win_o": emit("win_office", (0.8, 0.92, 0.8), 0.9),
        "shop_w": emit("shop_warm", (1.0, 0.8, 0.55), 1.3), "shop_c": emit("shop_cool", (0.7, 0.85, 1.0), 1.1),
        "red": emit("beacon", (1.0, 0.06, 0.03), 9.0), "sign_g": emit("sign_green", (0.01, 0.16, 0.07), 1.6), "sign_w": emit("sign_text", (0.9, 0.95, 0.9), 2.4),
        "neon_c": emit("neon_cyan", (0.1, 0.85, 1.0), 4.0), "neon_m": emit("neon_magenta", (1.0, 0.12, 0.6), 4.0), "neon_y": emit("neon_yellow", (1.0, 0.75, 0.1), 3.5),
    }
    for k, b in B.items():
        if b.f and k in MAT:
            b.obj(sc, "env_" + k, MAT[k], mover)
    Bh.obj(sc, "onc_head", emit("headlight", (0.95, 0.97, 1.0), 60.0), onc); Bd.obj(sc, "onc_body", pbr("carbody", (0.02, 0.02, 0.025), 0.3, 0.6), onc)
    # ---- real lights: only the lamps the shot can reach (travel + view distance), warm sodium
    lo, hi = spec.get("light_range", [-330.0, 330.0])
    for j, (x, y, z) in enumerate(l for l in lamps if lo < l[1] < hi):
        L = bpy.data.lights.new(f"sl{j}", "SPOT"); L.energy = spec.get("lamp_w", 3600.0); L.color = (1.0, 0.66, 0.36)
        L.spot_size = math.radians(150); L.spot_blend = 0.6; L.shadow_soft_size = 0.35
        o = bpy.data.objects.new(f"sl{j}", L); sc.collection.objects.link(o); o.parent = mover; o.location = (x, y, z)
    sky(sc, spec.get("sky", 1.0))
    return onc
