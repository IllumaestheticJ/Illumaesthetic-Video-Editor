"""Eyebrow concept stills (owner: current brows read as a second pair of eyes). Lookdev only, no shot renders.

  blender -b --factory-startup -P partA_scene.py -- --engine EEVEE --exec brow_concepts.py --out DIR --scale 0.4 --spp 4

Renders DIR/brows/<opt>_<who>_<state>.png (front-on head close-ups) and DIR/brows/<opt>_phone.png (medium shot, both characters,
annoyed, 270x480 for the phone read). Options:
  A thin mid-grey tapered line brows   B lid shapes only (no brows)   C brow cap attached to the dot
  D character-integrated (Gus's goggles / Pip's cap move) + lid shapes   E lid shapes + low-contrast vinyl forehead creases
"""
OUTB = os.path.join(OUT, "brows")
os.makedirs(OUTB, exist_ok=True)
STATES4 = ["neutral", "annoyed", "worried", "surprised"]
_tmp = []


def tmp(o):
    _tmp.append(o)
    return o


def clear_tmp():
    for o in _tmp:
        try:
            bpy.data.objects.remove(o, do_unlink=True)
        except ReferenceError:
            pass
    _tmp.clear()


def taper_arc(name, R, rt, a0, a1, m, parent, loc, rot=(0, 0, 0), n=16, rs=8):
    """Tapered stroke along an arc in the XZ plane (thin in the middle of nothing: fat middle, pointed ends)."""
    bm = bmesh.new()
    rings = []
    for i in range(n + 1):
        u = i / n
        a = math.radians(a0 + (a1 - a0) * u)
        c = Vector((R * math.cos(a), 0, R * math.sin(a)))
        nrm = c.normalized()
        r = rt * (0.15 + 0.85 * math.sin(math.pi * u) ** 0.7)
        ring = [bm.verts.new(c + (nrm * math.cos(2 * math.pi * k / rs) + Vector((0, 1, 0)) * math.sin(2 * math.pi * k / rs)) * r)
                for k in range(rs)]
        rings.append(ring)
    for i in range(n):
        for k in range(rs):
            bm.faces.new((rings[i][k], rings[i + 1][k], rings[i + 1][(k + 1) % rs], rings[i][(k + 1) % rs]))
    for ring in (rings[0], rings[-1]):
        bm.faces.new(ring)
    _smooth(bm)
    return tmp(new_obj(name, bm, [m], parent, loc, rot))


BASE = {}


def remember():
    for nm in ("GUS_cupp1", "GUS_cupp-1", "PIP_capp"):
        o = bpy.data.objects[nm]
        BASE[nm] = (tuple(o.location), tuple(o.rotation_euler))


def restore():
    for nm, (l, r) in BASE.items():
        o = bpy.data.objects[nm]
        o.location, o.rotation_euler = l, r
    for ch in (GUS, PIP):
        for e in ch.eyeset:
            e["piv"].rotation_euler = (0, 0, 0)


def lids(ch, state, sx_tilt=18):
    """B-style lid shapes: annoyed = flat cut tilted inner-down, worried = cut tilted inner-up, surprised = round x1.3."""
    if state == "neutral":
        set_eyes(ch, 0, 0)
    elif state == "annoyed":
        set_eyes(ch, 0.42, 0.42)
        for e, sx in zip(ch.eyeset, (1, -1)):
            e["piv"].rotation_euler = (0, math.radians(-sx * sx_tilt), 0)
    elif state == "worried":
        set_eyes(ch, 0.36, 0.36)
        for e, sx in zip(ch.eyeset, (1, -1)):
            e["piv"].rotation_euler = (0, math.radians(sx * sx_tilt), 0)
    else:
        set_eyes(ch, 0, 0, scale=1.3)


def opt_A(ch, state):
    """Thin mid-grey (#6e6e6e) tapered strokes with a slight arch - a different weight and colour from the eyes."""
    S = ch.S
    dot_h = 2 * S["eye_r"] * 1.15
    for b in ch.browset:
        for c in b["piv"].children:
            c.hide_render = True
        L = S["brow_len"] * 1.15
        taper_arc(f"A_{ch.root.name}{b['sx']}", L, dot_h / 6, 62, 118, mat("#6e6e6e"), b["piv"], (0, 0, -L * 0.95))
    h, t, sc = {"neutral": (0, 0, 1.0), "annoyed": (-0.006, 16, 1.0), "worried": (0.004, -16, 1.0), "surprised": (0.022, 0, 1.2)}[state]
    if ch is PIP:
        h = min(h, 0.008)
    b_on = 1.0
    for b in ch.browset:
        b["piv"].hide_render = False
        b["piv"].scale = (1, 1, 1)
        b["piv"].location.z = b["z"] + h
        b["piv"].rotation_euler = (0, math.radians(-b["sx"] * t), 0)
    set_eyes(ch, 0.25 if state == "annoyed" else 0, 0.25 if state == "annoyed" else 0, scale=sc)


def opt_B(ch, state):
    set_brows(ch, 0)
    lids(ch, state)


def opt_C(ch, state):
    """A short black lid-cap sitting right on top of each dot (touching): one shape, a dot with a little cap."""
    set_brows(ch, 0)
    er = ch.S["eye_r"]
    tilt = {"neutral": None, "annoyed": 22, "worried": -22, "surprised": 0}[state]
    set_eyes(ch, 0, 0, scale=1.25 if state == "surprised" else 1.0)
    if tilt is None:
        return
    for e, sx in zip(ch.eyeset, (1, -1)):
        cp = tmp(empty(f"C_capp{ch.root.name}{sx}", e["piv"], (0, -0.003, e["rz"] * 0.82), (0, -sx * tilt, 0)))
        o = blob(f"C_cap{ch.root.name}{sx}", (er * 1.3, er * 0.75, er * 0.42), (0, 0, er * 0.18), mat("black"), cp)
        tmp(o)


def opt_D(ch, state):
    """Nothing added to the face: Gus's goggle cups tilt/slide like brows, Pip's cap tilts/lifts; plus lid shapes."""
    set_brows(ch, 0)
    lids(ch, state)
    if ch is GUS:
        for sx in (1, -1):
            o = bpy.data.objects[f"GUS_cupp{sx}"]
            l, r = BASE[o.name]
            dz, ry, rx = {"neutral": (0, 0, 0), "annoyed": (-0.045, -sx * 30, 22), "worried": (0.015, sx * 30, -10),
                          "surprised": (0.07, 0, -35)}[state]
            o.location = (l[0], l[1], l[2] + dz)
            o.rotation_euler = (r[0] + math.radians(rx), r[1] + math.radians(ry), r[2])
    else:
        o = bpy.data.objects["PIP_capp"]
        l, r = BASE[o.name]
        dz, rx, ry = {"neutral": (0, 0, 0), "annoyed": (-0.008, 7, 0), "worried": (0.008, -6, 10), "surprised": (0.035, -10, 0)}[state]
        o.location = (l[0], l[1], l[2] + dz)
        o.rotation_euler = (r[0] + math.radians(rx), r[1] + math.radians(ry), r[2])


def opt_E(ch, state):
    """Lid shapes + soft creases moulded into the vinyl (a shade darker than the head): they read as folds, never as eyes."""
    set_brows(ch, 0)
    lids(ch, state)
    S = ch.S
    hz, er = ch.head_c, S["eye_r"]
    crease = mat("#b2b0af")
    k = 0.55 if ch is PIP else 1.0     # Pip's forehead is under his cap: creases sit just above his eyes
    def fy(x, z):
        return head_surface_y(S, x, z) - 0.002
    if state == "annoyed":       # short furrow between the eyes, angled in
        for sx in (1, -1):
            x, z = sx * 0.022, S["eye_z"] + er * 2.2 * k
            taper_arc(f"E_f{ch.root.name}{sx}", 0.05, 0.006, 70, 110, crease, ch.neck, (x, fy(x, z), hz + z - 0.05),
                      rot=(0, math.radians(90 + sx * 12), 0))
    elif state == "worried":     # two wavy forehead lines, inner ends up
        for j, dz in enumerate((er * 3.0 * k, er * 4.1 * k)):
            for sx in (1, -1):
                x, z = sx * 0.045, S["eye_z"] + dz
                taper_arc(f"E_w{ch.root.name}{j}{sx}", 0.06, 0.005, 60, 120, crease, ch.neck, (x, fy(x, z), hz + z - 0.06),
                          rot=(0, math.radians(-sx * -14), 0))
    elif state == "surprised":   # three high straight forehead lines
        for j, dz in enumerate((er * 3.6 * k, er * 4.6 * k, er * 5.6 * k)):
            z = S["eye_z"] + dz
            taper_arc(f"E_s{ch.root.name}{j}", 0.14, 0.005, 72, 108, crease, ch.neck, (0, fy(0, z), hz + z - 0.14))


OPTS = {"A": opt_A, "B": opt_B, "C": opt_C, "D": opt_D, "E": opt_E}
remember()
for who, ch, loc in (("GUS", GUS, (0.0, -1.8, 0)), ("PIP", PIP, (1.6, -1.8, 0))):
    for on, fn in OPTS.items():
        for st in STATES4:
            clear_tmp(); restore()
            reset()
            set_vis(PIPSCAN, False)
            other = PIP if ch is GUS else GUS
            pose(other, loc=(30, 30, 0))
            pose(ch, loc=loc, rz=0)
            fn(ch, st)
            bpy.context.view_layer.update()
            hc = ch.neck.matrix_world @ Vector((0, 0, ch.head_c))
            d = 1.25 if ch is GUS else 1.0
            look(cam, hc + Vector((0.0, -d * 2.0, -0.08)), hc + Vector((0, 0, -0.12)), 62)
            scn.render.filepath = os.path.join(OUTB, f"{on}_{who}_{st}")
            bpy.ops.render.render(write_still=True)
            print(f"[brows] {on} {who} {st}", flush=True)
# phone read: both characters, annoyed, medium shot, 270x480
scn.render.resolution_percentage = 25
for on, fn in OPTS.items():
    clear_tmp(); restore()
    reset()
    set_vis(PIPSCAN, False)
    pose(GUS, loc=(-0.35, -1.9, 0), rz=12)
    pose(PIP, loc=(0.75, -2.3, 0), rz=-15)
    fn(GUS, "annoyed")
    fn(PIP, "annoyed")
    look(cam, (0.25, -5.4, 1.35), (0.25, -2.0, 1.1), 30)
    scn.render.filepath = os.path.join(OUTB, f"{on}_phone")
    bpy.ops.render.render(write_still=True)
    print(f"[brows] {on} phone", flush=True)
