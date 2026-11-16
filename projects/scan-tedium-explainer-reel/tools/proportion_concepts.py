"""Proportion concepts (owner: closer to Madness Interactive grunts - big round head, short wide torso, feet right under it,
small floating hands close to the body). Homage in proportion only. Lookdev stills, run via partA_scene.py --exec.

Rows: 0 current v6 spec, 1 "a little closer" (body -25 %, head +8 %), 2 "Madness-like" (head ~40 % of height, torso ~1.15
head-heights, wider torso, feet under the torso, hands close), 3 halfway between 1 and 2. Writes OUT/props/<row>_<view>.png.
"""
OUTP = os.path.join(OUT, "props")
os.makedirs(OUTP, exist_ok=True)


def variant(S0, row, kid):
    S = dict(S0)
    hw, hd, hh = S0["head"]
    if row == 0:
        return S
    if row == 1:
        hs, bh_k, br_k, hip, foot_k, gap_k, rnd = 1.08, 0.75, 1.0, S0["hip_z"], 1.0, 1.0, 0.0
    elif row == 2:
        hs, bh_k, br_k, hip, foot_k, gap_k, rnd = 1.0, None, 1.3, S0["hip_z"] * 2.0, 1.35, 0.55, 1.0
    else:
        hs, bh_k, br_k, hip, foot_k, gap_k, rnd = 1.04, None, 1.15, S0["hip_z"] * 1.5, 1.18, 0.78, 0.5
    head_h = hh * hs * (1 - 0.1 * rnd)                 # rounder head toward Madness
    head_w = hw * hs * (1 + 0.04 * rnd)
    S["head"] = (head_w, hd * hs, head_h)
    S["taper"] = S0["taper"] * (1 - 0.6 * rnd)
    if bh_k is None:                                   # torso length in head-heights: 1.15 (row 2), halfway (row 3)
        t_heads = 1.15 if row == 2 else (1.15 + (S0["neck_z"] * 0.75) / (hh * 1.08)) / 2
        neck = head_h * t_heads
    else:
        neck = S0["neck_z"] * bh_k
    S["neck_z"] = neck
    S["body_h"] = neck + (S0["body_h"] - S0["neck_z"])
    S["body_r"] = S0["body_r"] * br_k
    S["hip_z"] = hip
    S["foot"] = tuple(v * foot_k for v in S0["foot"])
    S["foot_x"] = S0["foot_x"] * br_k
    hr = S0["hand"][0]
    clothes = S["body_r"] + (0.018 if not kid else 0.02)
    S["hand_x"] = clothes + 2 * hr * (0.88 * gap_k) + hr      # gap ~ one hand width (row 0/1), closer for Madness
    S["shoulder_z"] = neck * 0.88
    S["reach"] = neck * 0.88 - neck * 0.5
    S["eye_z"] = S0["eye_z"] * (1 - 0.6 * rnd)
    return S


chars = {}
xs = {0: -9.0, 1: -6.0, 2: -3.0, 3: 0.0}
for row in (0, 1, 2, 3):
    g = build_char(f"G{row}", variant(GUS_SPEC, row, False))
    p = build_char(f"P{row}", variant(PIP_SPEC, row, True))
    chars[row] = (g, p)
    for ch in (g, p):
        _pose_plain = globals().get("_pose_base", pose)
        _pose_plain(ch, loc=(30, 30 + row, 0))
        set_eyes(ch, 0, 0)
reset()
set_vis(PIPSCAN, False)
pose(GUS, loc=(40, 40, 0)); pose(PIP, loc=(41, 40, 0))
for row, (g, p) in chars.items():
    for o in (g, p):
        pass
for row, (g, p) in chars.items():
    others = [c for r, cs in chars.items() if r != row for c in cs]
    for c in others:
        pose(c, loc=(30, 30, 0))
    for view, rz in (("front", 0.0), ("q34", 35.0)):
        pose(g, loc=(-0.42, -2.0, 0), rz=rz)
        pose(p, loc=(0.42, -2.0, 0), rz=rz)
        set_eyes(g, 0, 0); set_eyes(p, 0, 0)
        bpy.context.view_layer.update()
        look(cam, (0.0, -6.4, 1.05), (0.0, -2.0, 0.95), 52)
        scn.render.resolution_percentage = int(round(SCALE * 100))
        scn.render.filepath = os.path.join(OUTP, f"{row}_{view}")
        bpy.ops.render.render(write_still=True)
        print(f"[props] row {row} {view}", flush=True)
    # phone read: medium shot in the shop, 270 x 480
    pose(g, loc=(-0.35, -1.9, 0), rz=12)
    pose(p, loc=(0.75, -2.3, 0), rz=-15)
    set_eyes(g, 0, 0); set_eyes(p, 0, 0)
    look(cam, (0.25, -5.4, 1.2), (0.25, -2.0, 0.95), 30)
    scn.render.resolution_percentage = 25
    scn.render.filepath = os.path.join(OUTP, f"{row}_phone")
    bpy.ops.render.render(write_still=True)
    print(f"[props] row {row} phone", flush=True)
    for c in (g, p):
        pose(c, loc=(30, 30, 0))
