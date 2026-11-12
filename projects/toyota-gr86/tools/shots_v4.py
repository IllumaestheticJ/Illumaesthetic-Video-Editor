"""v4 shot specs from projects/toyota-gr86/direction.md (scene director, v4): one shot per kick, one action per shot.
User v3 notes: faster; no bumper leftovers (comp_explode4 + front/rear_bumper_v4); hood hinges open THEN comes off;
trunk lid cut on its shut lines (lid_v4) and done the same way.
Part-move shots render at 30 fps (minterpolate smears fast moves); camera-only shots at 15 fps (+ minterpolate).
seconds = slot + 0.1 (3 spare frames). Local times are shot seconds.
  python projects/toyota-gr86/tools/shots_v4.py [--preview]   (preview: 30 % / 8 spp, first/mid/last + action frames)"""
import json
import os
import sys

B = "/home/user/media/work/gr86/blend/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots")
PREVIEW = "--preview" in sys.argv
Z = [0, 0, 0]
# hinge lines (levelled mm -> Blender m = mm*0.001 + root): hood (9,-885,850) = its rear corners; lid (9,1390,975) = its
# front-edge corners (director check: a pivot behind the lid's front edge dips that edge ~3 cm into the glass mid-swing)
HP = [0.0185, -0.7327, 1.0441]
LP = [0.0185, 1.5423, 1.1691]
HOOD_OPEN, LID_OPEN = [-50, 0, 0], [65, 0, 0]
HOOD_GONE = [0, -0.15, 3.2]     # lifted off the open pose, above frame
LID_GONE = [0, 0.10, 3.2]
RB = [0.064, 1.817, 0.638]      # rear bumper pivot (the lights ride on it)
FB_PIV = [-0.07, -1.818, 0.605]
FB_PARK, FB_ROT = [0.35, -0.70, -1.60], [110, 0, 0]   # below frame in c4 (preview: a corner showed)
RB_OFF, RB_ROT = [0.30, 0.95, -0.45], [-110, 0, 0]
MR_END, ML_END = [0.55, -0.05, 0.95], [-0.55, -0.05, 0.95]
FAR = [0, 0, 9.0]
# light poses placed with a pinhole projection of the f1/f2 end cameras (checked against a debug render, 0.02 off):
# reverse light ends in the black band between car and parked bumper (f1 end v 0.37); plate lamp lands ~1.1 m from the
# f2 camera at screen (0.55, 0.30), below the beam (v3 pose sat 0.6 m from the lens: huge, over the structure)
REV_UP, REV_END = [0, 0.22, 0.50], [0, 0.25, 0.56]
PL_LAND, PL_END = [0.027, 0.746, -0.151], [0.030, 0.770, -0.140]   # preview 2: +0.12 m toward the lens/up, off the bumper edge


def add(a, b):
    return [x + y for x, y in zip(a, b)]


def k(t, loc, rot=Z, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def cam(t, loc, target, focal):
    return {"t": t, "loc": loc, "target": target, "focal": focal, "ease": "inout"}


def part(name, keys, pivot=None):
    p = {"blend": B + name + ".blend", "keys": keys}
    if pivot:
        p["pivot"] = pivot
    return p


def spec(name, cams, frames, parts, fps=30, base="comp_explode4", extra_frames=()):
    seconds = frames / 30 + 0.1
    s = {"base": [B + base + ".blend"], "parts": parts, "camera": {"keys": cams}, "seconds": round(seconds, 4), "fps": fps,
         "res": "1080x1920", "res_pct": 75, "samples": 12, "out": "/home/user/media/work/gr86/shots/" + name}
    if PREVIEW:
        s.update(res_pct=30, samples=8, out="/home/user/media/work/gr86/preview/" + name,
                 frames=["first", "mid", "last", *[max(1, round(t * fps)) for t in extra_frames]])
    json.dump(s, open(os.path.join(OUT, name + ("_pv" if PREVIEW else "") + ".json"), "w"), indent=1)
    print(name, round(seconds, 3), "s", fps, "fps", len(parts), "parts")


def rear_group(keys, rev=None, pl=None):
    """rear bumper + both lights on the same keys about RB; rev/pl = per-key offsets added to that light's loc."""
    out = [part("rear_bumper_v4", [k(t, l, r, e) for t, l, r, e in keys], RB)]
    for name, extra in (("reverse_light", rev), ("plate_light", pl)):
        if extra is None:
            out.append(part(name, [k(t, l, r, e) for t, l, r, e in keys], RB))
        else:
            out.append(part(name, [k(t, add(l, o), r, e) for (t, l, r, e), o in extra], RB))
    return out


def static(hood=(Z, Z), lid=(Z, Z), fb=(Z, Z), mR=Z, mL=Z, rb=None):
    """parts that don't move in this shot, at the given (loc, rot) poses"""
    ps = [part("hood_t", [k(0, *hood)], HP), part("lid_v4", [k(0, *lid)], LP),
          part("front_bumper_v4", [k(0, *fb)], FB_PIV), part("mirror_R", [k(0, mR)]), part("mirror_L", [k(0, mL)])]
    if rb is not None:
        ps += rear_group([(0, rb[0], rb[1], "inout")])
    return ps


def drop(ps, name):
    return [p for p in ps if not p["blend"].endswith("/" + name + ".blend")]


# 3  hood hinges open -50 deg (t 0.05 -> 0.85), camera on the hinge side (hood underside never scanned)
spec("c1_hood_hinge", [cam(0, [2.40, -0.55, 1.70], [0.10, -1.30, 1.10], 27),
                       cam(2.45, [2.20, -0.75, 2.15], [0.05, -1.30, 1.25], 26)], 73,
     [part("hood_t", [k(0, Z), k(0.05, Z), k(0.85, Z, HOOD_OPEN, "out")], HP)]
     + drop(static(rb=(Z, Z)), "hood_t"), extra_frames=(0.45,))
# 4  hood lifts off the open pose (t 0.05 -> 0.70), push into the bay
spec("c2_hood_off", [cam(0, [2.20, -0.95, 2.45], [0.05, -1.30, 1.15], 27),
                     cam(2.45, [1.35, -1.75, 2.15], [0.00, -1.30, 0.80], 32)], 74,
     [part("hood_t", [k(0, Z, HOOD_OPEN), k(0.05, Z, HOOD_OPEN), k(0.70, [0, -0.15, 1.30], HOOD_OPEN, "in"),
                      k(1.10, HOOD_GONE, HOOD_OPEN, "lin")], HP)]
     + drop(static(rb=(Z, Z)), "hood_t"), extra_frames=(0.35,))
# 5  front bumper pulls straight out 0.30 (black gap all round), then tips and drops out bottom-right
spec("c3_front_bumper_off", [cam(0, [1.70, -3.70, 1.25], [0.10, -1.80, 0.62], 30),
                             cam(2.45, [1.45, -3.40, 1.10], [0.05, -1.85, 0.55], 30)], 73,
     [part("front_bumper_v4", [k(0, Z), k(0.05, Z), k(0.40, [0, -0.30, 0], ease="out"),
                               k(1.10, [0.30, -0.60, -0.90], FB_ROT, "in"), k(2.55, FB_PARK, FB_ROT, "lin")], FB_PIV)]
     + drop(static(hood=(HOOD_GONE, HOOD_OPEN), rb=(Z, Z)), "front_bumper_v4"), extra_frames=(0.40, 0.80))
# 6  camera-only push on what is behind the front bumper
spec("c4_front_structure", [cam(0, [0.95, -3.60, 0.95], [0.00, -1.90, 0.60], 30),
                            cam(1.70, [0.60, -3.10, 0.86], [0.00, -1.95, 0.58], 35),
                            cam(2.45, [0.55, -3.05, 0.85], [0.00, -1.95, 0.58], 35)], 73,
     static(hood=(HOOD_GONE, HOOD_OPEN), fb=(FB_PARK, FB_ROT), rb=(Z, Z)), fps=15)
# 7  right mirror flies off -> scanned mount (v3 keys, now on comp_explode4)
spec("d_mirror4", [cam(0, [2.10, -1.75, 1.55], [0.80, -0.30, 1.05], 30),
                   cam(2.43, [1.55, -1.05, 1.30], [0.80, -0.32, 1.03], 35)], 74,
     [part("mirror_R", [k(0, Z), k(0.05, Z), k(0.85, [0.40, -0.10, 0.45], ease="out"), k(2.50, MR_END)]),
      part("mirror_L", [k(0, Z), k(0.05, Z), k(0.85, [-0.40, -0.10, 0.45], ease="out"), k(2.50, ML_END)])]
     + drop(drop(static(hood=(HOOD_GONE, HOOD_OPEN), fb=(FB_PARK, FB_ROT), rb=(Z, Z)), "mirror_R"), "mirror_L"),
     extra_frames=(0.45,))
MIRRORS_OUT = dict(mR=add(MR_END, [0, 0, 6]), mL=add(ML_END, [0, 0, 6]))
# 8  lid hinges open +65 deg, camera forward of the lid on the right (its scanned outer face toward the lens)
spec("e1_lid_hinge", [cam(0, [3.00, 0.30, 3.20], [0.05, 1.80, 1.05], 30),   # preview 3: pulled back, wheel only a sliver at the bottom
                      cam(2.45, [2.85, 0.45, 3.25], [0.05, 1.82, 1.10], 31)], 74,
     [part("lid_v4", [k(0, Z), k(0.05, Z), k(0.85, Z, LID_OPEN, "out")], LP)]
     + drop(static(hood=(FAR, HOOD_OPEN), fb=(FB_PARK, FB_ROT), rb=(Z, Z), **MIRRORS_OUT), "lid_v4"), extra_frames=(0.45,))
# 9  lid lifts off the open pose -> TRUNK OPEN cargo (<= 30 deg down)
spec("e2_lid_off_cargo", [cam(0, [2.30, 2.70, 1.75], [0.05, 1.60, 0.85], 30),
                          cam(2.45, [1.30, 3.90, 1.55], [0.05, 1.55, 0.72], 30)], 73,
     [part("lid_v4", [k(0, Z, LID_OPEN), k(0.05, Z, LID_OPEN), k(0.65, [0, 0.10, 1.30], LID_OPEN, "in"),
                      k(1.05, LID_GONE, LID_OPEN, "lin")], LP)]
     + drop(static(hood=(FAR, HOOD_OPEN), fb=(FB_PARK, FB_ROT), rb=(Z, Z), **MIRRORS_OUT), "lid_v4"), extra_frames=(0.35,))
REAR_FIXED = dict(hood=(FAR, HOOD_OPEN), lid=(FAR, LID_OPEN), fb=(FB_PARK, FB_ROT), **MIRRORS_OUT)
# 10 rear bumper (+ both lights) pulls straight back 0.30, then tips and drops to the park pose
spec("e3_rear_bumper_off", [cam(0, [1.85, 4.20, 1.30], [0.12, 2.00, 0.55], 30),
                            cam(2.45, [1.60, 3.90, 1.15], [0.10, 1.95, 0.50], 30)], 74,
     static(**REAR_FIXED)
     + rear_group([(0, Z, Z, "inout"), (0.05, Z, Z, "inout"), (0.40, [0, 0.30, 0], Z, "out"), (1.10, RB_OFF, RB_ROT, "in"),
                   (2.55, add(RB_OFF, [0, 0.02, -0.03]), RB_ROT, "lin")]), extra_frames=(0.40, 0.80))
RB_PARK = add(RB_OFF, [0, 0.02, -0.03])
# 11 camera-only push on the rear crash beam
spec("e4_rear_beam", [cam(0, [1.35, 4.10, 1.20], [0.05, 1.95, 0.68], 30),
                      cam(1.70, [0.85, 3.60, 1.06], [0.05, 1.98, 0.66], 35),
                      cam(2.45, [0.80, 3.55, 1.05], [0.05, 1.98, 0.66], 35)], 73,
     static(**REAR_FIXED, rb=(RB_PARK, RB_ROT)), fps=15)
# 12 reverse light lifts straight off the parked bumper's inner face (socket side to the lens)
L0 = (0, RB_PARK, RB_ROT, "inout")
spec("f1_reverse_light", [cam(0, [1.05, 4.55, 1.65], [0.36, 2.75, 0.25], 28),
                          cam(2.45, [0.80, 4.15, 1.40], [0.30, 2.80, 0.35], 32)], 74,
     static(**REAR_FIXED)
     + rear_group([L0, (0.05, RB_PARK, RB_ROT, "inout"), (0.65, RB_PARK, RB_ROT, "out"), (2.55, RB_PARK, RB_ROT, "lin")],
                  rev=[((0, RB_PARK, RB_ROT, "inout"), Z), ((0.05, RB_PARK, RB_ROT, "inout"), Z),
                       ((0.65, RB_PARK, RB_ROT, "out"), REV_UP), ((2.55, RB_PARK, RB_ROT, "lin"), REV_END)]),
     extra_frames=(0.35,))
# 13 plate lamp lifts out, turns upright and lands on black above the bumper
spec("f2_plate_light", [cam(0, [0.55, 3.85, 1.05], [0.15, 2.85, 0.40], 38),
                        cam(2.45, [0.45, 3.65, 0.95], [0.15, 2.88, 0.45], 42)], 73,
     static(**REAR_FIXED)
     + rear_group([L0, (0.05, RB_PARK, RB_ROT, "inout"), (0.55, RB_PARK, RB_ROT, "in"), (2.55, RB_PARK, RB_ROT, "lin")],
                  rev=[(L0, REV_END), ((0.05, RB_PARK, RB_ROT, "inout"), REV_END), ((0.55, RB_PARK, RB_ROT, "in"), add(REV_END, [-0.9, 0, 0])),
                       ((2.55, RB_PARK, RB_ROT, "lin"), add(REV_END, [-0.9, 0, 0]))],   # starts at the left edge: clears out
                  pl=[(L0, Z), ((0.05, RB_PARK, RB_ROT, "inout"), Z), ((0.55, add(RB_PARK, [0, 0, 0.05]), RB_ROT, "out"), Z),
                      ((1.20, Z, Z, "out"), PL_LAND), ((2.55, Z, Z, "lin"), PL_END)]),
     extra_frames=(0.35,))
# 14 reassembly rear -> front; hood swings shut exactly on the cut (local 2.447 = frame 1030)
spec("h1_reassemble", [cam(0, [1.80, 4.60, 4.60], [0, -0.05, 0.75], 29),
                       cam(2.45, [1.65, 4.35, 4.35], [0, -0.20, 0.90], 31)], 74,
     [part("hood_t", [k(0, add(HOOD_GONE, [0, 0, -0.6]), HOOD_OPEN), k(1.60, add(HOOD_GONE, [0, 0, -0.6]), HOOD_OPEN),
                      k(2.05, Z, HOOD_OPEN, "out"), k(2.447, Z, Z, "in")], HP),
      part("lid_v4", [k(0, [0, 0.10, 2.6], LID_OPEN), k(0.70, [0, 0.10, 2.6], LID_OPEN), k(1.20, Z, LID_OPEN, "out"),
                      k(1.55, Z, Z, "in")], LP),
      part("front_bumper_v4", [k(0, FB_PARK, FB_ROT), k(1.30, FB_PARK, FB_ROT), k(1.85, Z, Z, "in")], FB_PIV),
      part("mirror_R", [k(0, MR_END), k(1.05, MR_END), k(1.50, Z, ease="in")]),
      part("mirror_L", [k(0, ML_END), k(1.05, ML_END), k(1.50, Z, ease="in")])]
     + rear_group([(0, RB_PARK, RB_ROT, "inout"), (0.35, RB_PARK, RB_ROT, "inout"), (0.95, Z, Z, "in")],
                  rev=[((0, RB_PARK, RB_ROT, "inout"), REV_END), ((0.05, RB_PARK, RB_ROT, "inout"), REV_END),
                       ((0.35, RB_PARK, RB_ROT, "in"), Z), ((0.95, Z, Z, "in"), Z)],
                  pl=[((0, Z, Z, "inout"), PL_END), ((0.05, Z, Z, "inout"), PL_END),
                      ((0.35, RB_PARK, RB_ROT, "in"), Z), ((0.95, Z, Z, "in"), Z)]),
     extra_frames=(0.70, 1.40, 2.10))
# 15 clean complete car (car4) hero from high on the right; fade in the assembler
spec("h2_hero", [cam(0, [2.80, 0.70, 6.20], [0, -0.05, 0.80], 28), cam(2.45, [2.50, 0.50, 6.60], [0, -0.05, 0.80], 28)], 73,
     [], fps=15, base="car4")
