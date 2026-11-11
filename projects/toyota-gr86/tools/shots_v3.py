"""v3 shot specs from projects/toyota-gr86/direction.md (scene director, v3): c_front, d_mirror, e_rear, f_lights, h_reassemble.
Base for every shot: comp_explode3 (car - hood_t - lid - both bumpers - both mirrors + state fills). Rear bumper = comp_rb_nolights
(plate lamp + reverse light cut out of it); the two lights ride with the bumper (same keys, same pivot RB) plus their own offset.
Times are local shot seconds; seconds = slot + 0.2 (minterpolate tail).
  python projects/toyota-gr86/tools/shots_v3.py"""
import json
import os

B = "/home/user/media/work/gr86/blend/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots")
Z = [0, 0, 0]
RB = [0.064, 1.817, 0.638]       # rear bumper bbox centre (Blender m) - pivot for the bumper AND the lights riding in it
FB_PIV = [-0.07, -1.818, 0.605]
HOOD_OFF = [0, -0.10, 1.20]
FB_OFF, FB_ROT = [0.30, -0.90, -0.45], [110, 0, 0]
RB_OFF, RB_ROT = [0.30, 0.95, -0.45], [-110, 0, 0]
LID_OFF = [0, 0.30, 0.95]
MR_OFF, ML_OFF = [0.40, -0.10, 0.45], [-0.40, -0.10, 0.45]
FAR = [0, 0, 9.0]                # parked far out of frame (another section's part)
REV_END = [0, 0.18, 0.40]   # reverse-light offset at the end of f_lights (on top of the bumper pose)
# plate lamp: when the bumper tips it ends up lens-down INSIDE the bumper (check render), so it turns back upright
# (rot 0 about RB = its scanned lens facing +Y, the camera) and lands past the bumper's near edge, toward the lens
PL_LAND, PL_END = [0.12, 1.15, 0.10], [0.13, 1.20, 0.13]   # lands in the black band above the bumper (silver on bumper skin vanished)


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


def spec(name, cams, seconds, parts):
    s = {"base": [B + "comp_explode3.blend"], "parts": parts, "camera": {"keys": cams}, "seconds": seconds, "fps": 15,
         "res": "1080x1920", "res_pct": 75, "samples": 12, "out": "/home/user/media/work/gr86/shots/" + name}
    json.dump(s, open(os.path.join(OUT, name + ".json"), "w"), indent=1)
    print(name, seconds, "s", len(parts), "parts")


def rear_group(keys_loc_rot, extra_rev=None, extra_pl=None):
    """Bumper + both lights with the same keys about RB; extra_* = list of (t, offset) added to each light's loc."""
    bump = part("comp_rb_nolights", [k(t, l, r, e) for t, l, r, e in keys_loc_rot], RB)
    out = [bump]
    for name, extra in (("reverse_light", extra_rev), ("plate_light", extra_pl)):
        if extra is None:
            keys = [k(t, l, r, e) for t, l, r, e in keys_loc_rot]
        else:
            keys = [k(t, add(l, off), r, e) for (t, l, r, e), off in extra]
        out.append(part(name, keys, RB))
    return out


# C: front section - hood off (lands 9.83), bay, front bumper off + tipped (lands 12.28), structure push-in
spec("c_front", [
    cam(0, [2.20, -4.90, 2.00], [0.10, -1.40, 0.80], 30),
    cam(2.45, [1.40, -3.90, 2.70], [0.05, -1.15, 0.75], 30),
    cam(3.37, [1.20, -3.60, 2.40], [0.00, -1.10, 0.70], 32),
    cam(4.90, [2.10, -4.70, 1.70], [0.10, -2.10, 0.50], 30),
    cam(7.37, [1.00, -3.60, 1.20], [0.00, -1.85, 0.55], 30)], 7.57,
    [part("hood_t", [k(0, Z), k(0.15, Z), k(2.45, HOOD_OFF, ease="out")]),
     part("front_bumper", [k(0, Z), k(3.37, Z), k(4.90, FB_OFF, FB_ROT), k(7.37, [1.70, -1.30, -0.45], FB_ROT)], FB_PIV),
     part("mirror_R", [k(0, Z)]), part("mirror_L", [k(0, Z)]), part("lid", [k(0, Z)])]
    + rear_group([(0, Z, Z, "inout")]))

# D: right mirror flies off -> scanned mirror mount (left mirror stays out of frame)
spec("d_mirror", [
    cam(0, [2.10, -1.75, 1.55], [0.80, -0.30, 1.05], 30),
    cam(2.43, [1.55, -1.05, 1.30], [0.80, -0.32, 1.03], 35)], 2.63,
    [part("mirror_R", [k(0, Z), k(0.10, Z), k(1.00, MR_OFF, ease="out"), k(2.43, [0.55, -0.05, 0.95])]),
     part("mirror_L", [k(0, Z), k(0.10, Z), k(1.00, ML_OFF, ease="out"), k(2.43, [-0.55, -0.05, 0.95])]),
     part("hood_t", [k(0, HOOD_OFF)]), part("front_bumper", [k(0, FB_OFF, FB_ROT)], FB_PIV), part("lid", [k(0, Z)])]
    + rear_group([(0, Z, Z, "inout")]))

# E: rear - lid lifts off (lands 19.62) -> TRUNK OPEN cargo -> rear bumper off + tipped (lands 24.52) -> crash beam
spec("e_rear", [
    cam(0, [2.60, 4.90, 2.00], [0.30, 1.30, 0.85], 30),
    cam(2.45, [1.80, 4.30, 1.80], [0.05, 1.50, 0.80], 30),
    cam(4.60, [1.30, 3.90, 1.55], [0.05, 1.55, 0.72], 30),
    cam(7.35, [2.10, 4.90, 1.50], [0.15, 2.20, 0.45], 30),
    cam(9.80, [1.05, 3.70, 1.15], [0.05, 1.95, 0.68], 30)], 10.0,
    [part("lid", [k(0, Z), k(0.15, Z), k(2.45, LID_OFF, ease="out"), k(4.60, [0, 0.35, 2.60])]),
     part("hood_t", [k(0, FAR)]), part("front_bumper", [k(0, [1.7, -1.3, -0.45], FB_ROT)], FB_PIV),
     part("mirror_R", [k(0, add(MR_OFF, [0, 0, 6]))]), part("mirror_L", [k(0, add(ML_OFF, [0, 0, 6]))])]
    + rear_group([(0, Z, Z, "inout"), (5.20, Z, Z, "inout"), (7.35, RB_OFF, RB_ROT, "inout"), (9.80, add(RB_OFF, [0, 0, -0.12]), RB_ROT, "inout")]))

# F: the two light scans leave the tipped bumper's inner face (plate lamp lands 29.42)
L0 = (0, RB_OFF, RB_ROT, "inout")
spec("f_lights", [
    cam(0, [1.05, 4.55, 1.65], [0.36, 2.75, 0.25], 28),
    cam(2.45, [0.75, 4.05, 1.30], [0.36, 2.80, 0.32], 32),
    cam(4.90, [0.60, 3.75, 1.15], [0.30, 2.85, 0.40], 35)], 5.1,
    [part("lid", [k(0, [0, 0.35, 6.0])]), part("hood_t", [k(0, FAR)]),
     part("front_bumper", [k(0, [1.7, -1.3, -0.45], FB_ROT)], FB_PIV),
     part("mirror_R", [k(0, add(MR_OFF, [0, 0, 6]))]), part("mirror_L", [k(0, add(ML_OFF, [0, 0, 6]))])]
    + rear_group([L0, (0.15, RB_OFF, RB_ROT, "inout"), (1.00, RB_OFF, RB_ROT, "out"), (1.85, RB_OFF, RB_ROT, "lin"),
                  (2.45, RB_OFF, RB_ROT, "out"), (4.90, RB_OFF, RB_ROT, "lin")],
                 extra_rev=[((0, RB_OFF, RB_ROT, "inout"), Z), ((0.15, RB_OFF, RB_ROT, "inout"), Z),
                            ((1.00, RB_OFF, RB_ROT, "out"), [0, 0.15, 0.35]), ((1.85, RB_OFF, RB_ROT, "lin"), [0, 0.16, 0.37]),
                            ((2.45, RB_OFF, RB_ROT, "lin"), [0, 0.165, 0.38]), ((4.90, RB_OFF, RB_ROT, "lin"), REV_END)],
                 extra_pl=[((0, RB_OFF, RB_ROT, "inout"), Z), ((1.85, RB_OFF, RB_ROT, "inout"), Z),
                           ((2.45, Z, Z, "out"), PL_LAND), ((4.90, Z, Z, "lin"), PL_END)]))

# H: every part flies home rear -> front, hood last on the loud return (34.32 = local 2.45); fade in the assembler
spec("h_reassemble", [
    cam(0, [1.80, 4.60, 4.60], [0, -0.05, 0.75], 29),
    cam(4.90, [1.60, 4.20, 4.20], [0, -0.20, 0.90], 33)], 5.1,
    [part("hood_t", [k(0, HOOD_OFF), k(1.60, HOOD_OFF), k(2.45, Z, ease="in")]),
     part("front_bumper", [k(0, FB_OFF, FB_ROT), k(1.50, FB_OFF, FB_ROT), k(2.45, Z, Z, "in")], FB_PIV),
     part("mirror_R", [k(0, MR_OFF), k(1.30, MR_OFF), k(2.10, Z, ease="in")]),
     part("mirror_L", [k(0, ML_OFF), k(1.30, ML_OFF), k(2.10, Z, ease="in")]),
     part("lid", [k(0, LID_OFF), k(1.00, LID_OFF), k(1.85, Z, ease="in")])]
    + rear_group([(0, RB_OFF, RB_ROT, "inout"), (0.60, RB_OFF, RB_ROT, "inout"), (1.50, Z, Z, "in")],
                 extra_rev=[((0, RB_OFF, RB_ROT, "inout"), REV_END), ((0.15, RB_OFF, RB_ROT, "inout"), REV_END),
                            ((0.55, RB_OFF, RB_ROT, "in"), Z), ((0.60, RB_OFF, RB_ROT, "inout"), Z), ((1.50, Z, Z, "in"), Z)],
                 extra_pl=[((0, Z, Z, "inout"), PL_END), ((0.15, Z, Z, "inout"), PL_END),
                           ((0.55, RB_OFF, RB_ROT, "in"), Z), ((0.60, RB_OFF, RB_ROT, "inout"), Z), ((1.50, Z, Z, "in"), Z)]))
