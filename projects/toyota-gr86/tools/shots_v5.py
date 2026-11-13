"""v5 new shots (direction.md v5): m1_side_marker, c3b_front_bumper_off, x1/x2/x3 explode, h1_reassemble_v5.
User notes on v4: new music (GT2 East City, one shot per 1.9664 s bar = 59 frames) and "make sure all parts are highlighted".
x1/x2/x3/h1 are ONE part animation (local t from frame 826) rendered from four cameras in consecutive 1.967 s windows:
each spec shifts the keys by its window start (shot.py's sampler accepts negative key times).
Poses before x1 = the end of v4 f2_plate_light (shots_v4.py constants, copied here).
  python projects/toyota-gr86/tools/shots_v5.py [--preview]"""
import json
import os
import sys

B = "/home/user/media/work/gr86/blend/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots")
PREVIEW = "--preview" in sys.argv
Z = [0, 0, 0]
HP, LP = [0.0185, -0.7327, 1.0441], [0.0185, 1.5423, 1.1691]
HOOD_OPEN, LID_OPEN = [-50, 0, 0], [65, 0, 0]
HOOD_GONE = [0, -0.15, 3.2]
RB = [0.064, 1.817, 0.638]
FB_PIV = [-0.07, -1.818, 0.605]
FB_PARK, FB_ROT = [0.35, -0.70, -1.60], [110, 0, 0]
RB_OFF, RB_ROT = [0.30, 0.95, -0.45], [-110, 0, 0]
RB_PARK = [0.30, 0.97, -0.48]
MR_END, ML_END = [0.55, -0.05, 0.95], [-0.55, -0.05, 0.95]
FAR = [0, 0, 9.0]
REV_END = [0, 0.25, 0.56]
PL_END = [0.030, 0.770, -0.140]
BAR = 59 / 30


def add(*v):
    return [sum(x) for x in zip(*v)]


def scale(v, s):
    return [x * s for x in v]


def k(t, loc, rot=Z, ease="inout"):
    return {"t": round(t, 4), "loc": loc, "rot": rot, "ease": ease}


def cam(t, loc, target, focal):
    return {"t": t, "loc": loc, "target": target, "focal": focal, "ease": "inout"}


def part(name, keys, pivot=None):
    p = {"blend": B + name + ".blend", "keys": keys}
    if pivot:
        p["pivot"] = pivot
    return p


def spec(name, cams, parts, frames=59, extra_frames=(), base="comp_explode4"):
    s = {"base": [B + base + ".blend"], "parts": parts, "camera": {"keys": cams}, "seconds": round(frames / 30 + 0.1, 4),
         "fps": 30, "res": "1080x1920", "res_pct": 75, "samples": 12, "out": "/home/user/media/work/gr86/shots/" + name}
    if PREVIEW:
        s.update(res_pct=30, samples=8, out="/home/user/media/work/gr86/preview/" + name,
                 frames=["first", "mid", "last", *[max(1, round(t * 30)) for t in extra_frames]])
    json.dump(s, open(os.path.join(OUT, name + ("_pv" if PREVIEW else "") + ".json"), "w"), indent=1)
    print(name, s["seconds"], "s", len(parts), "parts")


def front_static(markers=FAR):
    """everything except the front bumper/markers, poses after c2 (hood gone)"""
    return [part("hood_t", [k(0, HOOD_GONE, HOOD_OPEN)], HP), part("lid_v4", [k(0, Z)], LP),
            part("mirror_R", [k(0, Z)]), part("mirror_L", [k(0, Z)]),
            part("rear_bumper_v4", [k(0, Z)], RB), part("reverse_light", [k(0, Z)], RB), part("plate_light", [k(0, Z)], RB)]


# 4  m1: right side marker pops straight out of its recess (+X 0.15), then to (+0.15,-0.30,+0.30) and holds on black;
#    left one mirrored (hidden by the car). Pure translate: the marker's back was never checked as scanned -> no spin.
MK_R = [0.15, -0.30, 0.30]
MK_L = [-0.15, -0.30, 0.30]
# camera ahead of the corner (preview 1 at (1.70,-2.40,0.55) framed the wheel and lost the marker top-left; pinhole check:
# marker home (0.65,0.57) -> end (0.50,0.31) of the frame)
spec("m1_side_marker", [cam(0, [2.00, -3.10, 0.95], [0.80, -1.80, 0.75], 34), cam(2.0, [1.92, -3.00, 0.95], [0.85, -1.88, 0.82], 42)],   # preview 2: marker reads but small -> push in on its end pose
     [part("front_bumper_v5", [k(0, Z)], FB_PIV),
      part("side_marker_R", [k(0, Z), k(0.05, Z), k(0.30, [0.15, 0, 0], ease="out"), k(0.75, MK_R, ease="out"),
                             k(2.1, add(MK_R, [0.01, -0.02, 0.02]), ease="lin")]),
      part("side_marker_L", [k(0, Z), k(0.05, Z), k(0.30, [-0.15, 0, 0], ease="out"), k(0.75, MK_L, ease="out"),
                             k(2.1, add(MK_L, [-0.01, -0.02, 0.02]), ease="lin")])] + front_static(), extra_frames=(0.30, 0.75))

# 5  c3b: v4 c3 (camera + keys) with the markerless front_bumper_v5; markers parked out of frame
spec("c3b_front_bumper_off", [cam(0, [1.70, -3.70, 1.25], [0.10, -1.80, 0.62], 30), cam(2.45, [1.45, -3.40, 1.10], [0.05, -1.85, 0.55], 30)],
     [part("front_bumper_v5", [k(0, Z), k(0.05, Z), k(0.40, [0, -0.30, 0], ease="out"),
                               k(1.10, [0.30, -0.60, -0.90], FB_ROT, "in"), k(2.55, FB_PARK, FB_ROT, "lin")], FB_PIV),
      part("side_marker_R", [k(0, FAR)]), part("side_marker_L", [k(0, FAR)])] + front_static(), extra_frames=(0.40, 0.80))

# 14-17  explode (one animation, t from frame 826). Offsets: direction.md v5 section 4 (clearances checked by projection).
EX = {"hood": [0, -0.25, 0.85], "lid": [0, 0.25, 0.75], "fb": [0, -0.80, 0], "mR": [0.60, 0, 0.40],
      "rb": [0, 0.80, 0], "rev": [0, 1.20, -0.25], "pl": [0.50, 1.05, 0.20], "kR": [0.55, -0.75, 0.30], "kL": [-0.55, -0.75, 0.30]}
T_OUT_BIG, T_OUT_SMALL, T_HOLD_END = 0.50, 0.60, 5.90
GROW = 1.06
# reassembly windows (local t): (start, land)
HOME = {"rev": (5.90, 6.35), "pl": (5.90, 6.35), "rb": (6.10, 6.65), "lid": (6.30, 6.85), "mR": (6.50, 7.00),
        "kR": (6.70, 7.20), "kL": (6.70, 7.20), "fb": (6.95, 7.45), "hood": (7.25, 4 * BAR)}


def explode_keys(key, start_loc, start_rot, t_out, mid=None):
    """start pose (end of f2 / c3b) -> exploded offset by t_out (ease out) -> +6 % drift to 5.90 -> hold -> home ('in')."""
    ex = EX[key]; t_home0, t_land = HOME[key]
    ks = [k(0, start_loc, start_rot)]
    if mid is not None:
        ks.append(k(mid[0], mid[1], Z, "inout"))
    ks += [k(t_out, ex, Z, "out"), k(T_HOLD_END, scale(ex, GROW), Z, "lin"), k(t_home0, scale(ex, GROW), Z, "lin"),
           k(t_land, Z, Z, "in")]
    ks.sort(key=lambda d: d["t"])
    return ks


def explode_parts(shift):
    def sh(keys):
        return [dict(x, t=round(x["t"] - shift, 4)) for x in keys]
    rev_start = add(RB_PARK, REV_END, [-0.9, 0, 0])
    return [
        part("hood_t", sh(explode_keys("hood", FAR, HOOD_OPEN, T_OUT_BIG)), HP),
        part("lid_v4", sh(explode_keys("lid", FAR, LID_OPEN, T_OUT_BIG)), LP),
        part("front_bumper_v5", sh(explode_keys("fb", FB_PARK, FB_ROT, T_OUT_BIG)), FB_PIV),
        part("side_marker_R", sh(explode_keys("kR", FAR, Z, T_OUT_SMALL))),
        part("side_marker_L", sh(explode_keys("kL", FAR, Z, T_OUT_SMALL))),
        part("mirror_R", sh(explode_keys("mR", add(MR_END, [0, 0, 6]), Z, T_OUT_SMALL))),
        part("mirror_L", sh([k(0, add(ML_END, [0, 0, 6])), k(T_OUT_SMALL, Z, Z, "out")])),   # broken capture: home, hidden by the car
        part("rear_bumper_v4", sh(explode_keys("rb", RB_PARK, RB_ROT, T_OUT_BIG)), RB),
        part("reverse_light", sh(explode_keys("rev", rev_start, RB_ROT, T_OUT_SMALL)), RB),
        part("plate_light", sh(explode_keys("pl", PL_END, Z, T_OUT_SMALL)), RB),
    ]


spec("x1_explode_fr", [cam(0, [2.30, -6.40, 4.60], [-0.38, -0.45, 0.59], 30), cam(BAR, [2.30, -6.40, 4.60], [-0.38, -0.45, 0.59], 31.7)],
     explode_parts(0 * BAR), extra_frames=(0.30, 0.60))
spec("x2_explode_rr", [cam(0, [2.50, 6.60, 4.40], [0.02, 0.45, 0.34], 34), cam(BAR, [2.50, 6.60, 4.40], [0.02, 0.45, 0.34], 35.8)],
     explode_parts(1 * BAR))
spec("x3_explode_high", [cam(0, [1.70, 5.60, 7.00], [0.11, 0.33, 0.17], 40), cam(BAR, [1.70, 5.60, 7.00], [0.11, 0.33, 0.17], 42.8)],
     explode_parts(2 * BAR))
spec("h1_reassemble_v5", [cam(0, [4.40, 1.15, 9.10], [0.12, -0.05, 0.80], 26), cam(BAR, [2.80, 0.70, 6.20], [0, -0.05, 0.80], 26)],
     explode_parts(3 * BAR), extra_frames=(0.70, 1.30))
