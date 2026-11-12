"""v4 (Epsilon) NEW shots: the kit goes on the scan car (direction.md "## v4 (Epsilon)").

    python projects/honda-civic-11/tools/shots_v4.py preview|final|inb [shot ...]

Order lip -> wheels -> skirts -> apron -> wing; every installed part stays on in later shots. Parts = Epsilon lookbook model
fitted to the scan (align_kit.py / kit_parts.py), painted white as in Ron's render, rims gold. Each part is seated by SEAT[s]
seconds and then holds (trimmable, so the shots can be re-timed to another track). W_kit = one still at the camera solved
against Ron's render 1 (match_render.py). Axes: front +Y, car's left -X.
"""
import json
import math
import os
import sys

K = "/home/user/media/honda-civic-11/prep/kit"
CAR = "/home/user/media/honda-civic-11/prep/car4f.blend"
NOW = f"{K}/car_nowheels.blend"
OUT = "/home/user/media/work/civic/renders"
SPECS = "/home/user/media/work/civic/specs"
Z3 = [0, 0, 0]
SECS = {"I1_lip": 2.07, "I2_wheels": 2.29, "I3_skirt": 2.68, "I4_apron": 2.27, "I5_wing": 2.28, "W_kit": 0.07}
SEAT = {"I1_lip": 0.62, "I2_wheels": 1.26, "I3_skirt": 1.24, "I4_apron": 0.83, "I5_wing": 0.64}


def part(name, mat="kit", keys=None):
    d = {"blend": f"{K}/{name}.blend"}
    if mat:
        d["mat"] = mat
    if keys:
        d["keys"] = keys
    return d


def fly(start, seat, secs, t0=0.0):
    """wait at `start` until t0, seated (ease out) at `seat`, hold."""
    k = [dict(t=0, loc=start, rot=Z3)]
    if t0 > 0:
        k.append(dict(t=t0, loc=start, rot=Z3))
    return k + [dict(t=seat, loc=Z3, rot=Z3, ease="out"), dict(t=secs, loc=Z3, rot=Z3)]


def wheels(side, keys=None):
    return [part(f"rims_{side}", "gold", keys), part(f"tyres_{side}", "rubber", keys), part(f"brakes_{side}", None, keys)]


def cam(t, tgt, dist, az, h, focal, ease="inout"):
    """az: 0 = in front of the car (+Y), +90 = the car's LEFT (-X), 180 = behind."""
    a = math.radians(az)
    return {"t": t, "loc": [tgt[0] - dist * math.sin(a), tgt[1] + dist * math.cos(a), h], "target": list(tgt),
            "focal": focal, "ease": ease}


S = SECS
LIP, SK = part("front_lip"), [part("skirt_L"), part("skirt_R")]
NEW_WHEELS = wheels("L") + wheels("R")
MATCH = json.load(open("/home/user/media/work/civic/match/ron1_shotcam.json"))["key"]
SHOTS = {
    "I1_lip": {"base": [CAR], "parts": [part("front_lip", keys=fly([0, 0.45, -0.15], SEAT["I1_lip"], S["I1_lip"]))],
               "cam": [cam(0, (0.09, 2.25, 0.45), 3.7, 15, 0.45, 35, "lin"), cam(S["I1_lip"], (0.09, 2.25, 0.45), 3.45, 15, 0.45, 35, "lin")],
               "motion": [0, SEAT["I1_lip"]]},
    # left side (both scanned left wheels are complete): scanned wheels pull outboard and leave frame-left, new wheels slide
    # in along the axle. The hidden right-side wheels swap unseen (popped far below) - v4 preview: flying them out the far
    # side from a high camera was clutter.
    "I2_wheels": {"base": [NOW], "parts": [LIP,
                  part("scanwheels_L", None, [dict(t=0, loc=Z3, rot=Z3), dict(t=0.65, loc=[-4.5, 0, 0], rot=Z3, ease="in"), dict(t=S["I2_wheels"], loc=[-9, 0, 0], rot=Z3, ease="lin")]),
                  part("scanwheels_R", None, [dict(t=0, loc=Z3, rot=Z3), dict(t=0.30, loc=Z3, rot=Z3), dict(t=0.31, loc=[0, 0, -30], rot=Z3, ease="lin"), dict(t=S["I2_wheels"], loc=[0, 0, -30], rot=Z3)])]
                  + wheels("L", fly([-4.5, 0, 0], SEAT["I2_wheels"], S["I2_wheels"], 0.62))
                  + wheels("R", [dict(t=0, loc=[0, 0, -30], rot=Z3), dict(t=0.30, loc=[0, 0, -30], rot=Z3), dict(t=0.31, loc=Z3, rot=Z3, ease="lin"), dict(t=S["I2_wheels"], loc=Z3, rot=Z3)]),
                  "cam": [cam(0, (-0.35, 0.35, 0.55), 6.5, 58, 1.3, 30, "lin"), cam(S["I2_wheels"], (-0.35, 0.35, 0.55), 6.2, 61, 1.3, 30, "lin")],
                  "motion": [0, SEAT["I2_wheels"]]},
    "I3_skirt": {"base": [NOW], "parts": [LIP] + NEW_WHEELS + [
                 part("skirt_L", keys=[dict(t=0, loc=[-0.40, 0, 0], rot=Z3), dict(t=0.82, loc=[-0.32, 0, 0], rot=Z3, ease="lin"), dict(t=SEAT["I3_skirt"], loc=Z3, rot=Z3, ease="out"), dict(t=S["I3_skirt"], loc=Z3, rot=Z3)]),
                 part("skirt_R", keys=[dict(t=0, loc=[0.40, 0, 0], rot=Z3), dict(t=0.82, loc=[0.32, 0, 0], rot=Z3, ease="lin"), dict(t=SEAT["I3_skirt"], loc=Z3, rot=Z3, ease="out"), dict(t=S["I3_skirt"], loc=Z3, rot=Z3)])],
                 "cam": [{"t": 0, "loc": [-2.7, 3.5, 0.38], "target": [-0.9, -0.2, 0.34], "focal": 30, "ease": "lin"},
                         {"t": S["I3_skirt"], "loc": [-2.65, 2.9, 0.42], "target": [-0.9, -0.4, 0.34], "focal": 30, "ease": "lin"}],
                 "motion": [0.7, SEAT["I3_skirt"]]},
    "I4_apron": {"base": [NOW], "parts": [LIP] + NEW_WHEELS + SK + [part("rear_lip", keys=fly([0, -0.45, -0.15], SEAT["I4_apron"], S["I4_apron"]))],
                 "cam": [cam(0, (0.05, -2.15, 0.62), 3.9, 140, 0.55, 35, "lin"), cam(S["I4_apron"], (0.05, -2.15, 0.62), 3.65, 140, 0.55, 35, "lin")],
                 "motion": [0, SEAT["I4_apron"]]},
    "I5_wing": {"base": [NOW], "parts": [LIP] + NEW_WHEELS + SK + [part("rear_lip"), part("sport_wing", keys=fly([0, 0, 0.6], SEAT["I5_wing"], S["I5_wing"]))],
                "cam": [cam(0, (0.05, -1.95, 1.38), 3.3, -147, 1.95, 35, "lin"), cam(S["I5_wing"], (0.05, -1.95, 1.38), 3.1, -150, 1.95, 35, "lin")],
                "motion": [0, SEAT["I5_wing"]]},
    "W_kit": {"base": [NOW], "parts": [LIP] + NEW_WHEELS + SK + [part("rear_lip"), part("sport_wing")], "cam": [dict(MATCH, t=0)]},
}


def spec(name, mode):
    s = SHOTS[name]; secs = SECS[name]; n15 = max(1, int(round(secs * 15)))
    out = {"base": s["base"], "parts": s["parts"], "camera": {"keys": s["cam"], "sensor": 20.25}, "seconds": secs,
           "fps": 15, "res": "1080x1920", "persist": False}
    if mode == "preview":
        seat = int(SEAT.get(name, 0) * 15) + 1
        out.update(res_pct=30, samples=8, out=f"{OUT}/preview4/{name}", frames=sorted({1, max(1, seat // 2), seat, n15}))
    elif mode == "final":
        out.update(res_pct=75, samples=12, out=f"{OUT}/final4/{name}")
    else:   # true 30 fps in-betweens (even frames) while parts move
        if "motion" not in s:
            return None
        a, b = s["motion"]
        out.update(res_pct=75, samples=12, fps=30, out=f"{OUT}/final4/{name}_30",
                   frames=[j for j in range(2, 2 * n15, 2) if a - 0.04 <= (j - 1) / 30 <= b + 0.04])
    p = f"{SPECS}/{name}_v4{mode}.json"
    json.dump(out, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    for n in (sys.argv[2:] or SHOTS):
        print(spec(n, sys.argv[1]))
