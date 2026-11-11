"""Shot specs for the Porsche Macan Temerario-style reel -> JSON for tools/shot.py (copied from ferrari-296).

    python projects/porsche-macan/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (prepped, metres): front = -Y, car's right = -X, ground Z=0. Length 4.79 m (bbox), width 2.04 m,
height 1.66 m. Front axle y=-1.45, rear y=+1.40, hub z~0.38. Hinges fitted to the state scans (tools/hinge.py):
hood about X at its rear edge, -54.9 deg = captured open hood; hatch about X at the roof edge, +69.8 deg.
Event times inside shots are seconds from the shot start and are set from the music (see project.yaml / editlog).
"""
import json
import math
import os
import sys

P = "/home/user/media/porsche-macan/prep"
OUT = "/home/user/media/work/macan/renders"
SPECS = "/home/user/media/work/macan/specs"
HINGE = "/home/user/media/work/macan/hinge"
CAR = f"{P}/car4.blend"      # 4 mm: full-car moves
CAR_HI = f"{P}/car3.blend"   # 3 mm: close-ups

TIMING = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "timing.json")))
SECS = TIMING["secs"]        # rendered length of each shot (s)
EV = TIMING["events"]        # in-shot event times (s)
hood = json.load(open(f"{HINGE}/hood.json"))
hatch = json.load(open(f"{HINGE}/hatch.json"))


def orbit(t, r, ang_deg, h, c=(0, 0, 0.6), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); +90 = car's left (+X); -90 = car's right (-X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(T, n, r0, r1, a0, a1, h0, h1, c=(0, 0, 0.6), focal=30, tz=None, shape=lambda u: u):
    """Orbit keyed n times (linear between keys would cut a chord toward the car)."""
    keys = []
    for k in range(n + 1):
        u = k / n; e = shape(u)
        keys.append(orbit(T * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal, ease="lin", tz=tz))
    return keys


smooth = lambda u: u * u * (3 - 2 * u)
easeout = lambda u: 1 - (1 - u) ** 2

SHOTS = {
    # 1. slow front 3/4 turntable, low (hook: moving on frame 1)
    "s1_front": {"base": [CAR], "cam": arc(SECS["s1_front"], 8, 5.7, 5.3, -42, -14, 0.95, 1.1, focal=30, tz=0.62, shape=easeout)},
    # (v0 swung -28 -> -58 toward side-on: the nose left the 9:16 frame - turn toward the front instead)
    # 2. rear 3/4 orbit, car's left side, slight rise; light bar in view
    "s2_rear": {"base": [CAR], "cam": arc(SECS["s2_rear"], 8, 5.6, 5.3, 122, 156, 0.85, 1.3, focal=30, tz=0.62, shape=easeout)},
    # (v0 swung 150 -> 122 toward side-on and cropped the tail - turn toward the rear instead)
    # 3. extreme close-up: front right wheel / brake through the spokes, slow slide forward
    "s3_wheel": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-2.35, -0.95, 0.45], "target": [-0.95, -1.40, 0.38], "focal": 40},
        {"t": SECS["s3_wheel"], "loc": [-2.25, -1.85, 0.42], "target": [-0.95, -1.47, 0.38], "focal": 40, "ease": "inout"}]},
    # 4. detail: rear light bar, slow slide across the tail (car's left -> centre)
    "s4_lightbar": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [1.35, 3.5, 1.45], "target": [0.5, 2.2, 1.15], "focal": 55},
        {"t": SECS["s4_lightbar"], "loc": [0.2, 3.78, 1.42], "target": [-0.2, 2.25, 1.15], "focal": 55, "ease": "inout"}]},
    # 5. one continuous move over the hit-less pre-drop build: high front-left 3/4 -> along the left side -> high rear-left
    #    3/4. The hood opens on its fitted hinge (bay from "Hood Removed"), then the hatch on its own (boot from
    #    "Rear Hatch Fully Open"). Base = comp_open (hood + hatch cut out).
    "s5_open": {"base": [f"{P}/comp_open.blend"],
                "parts": [{"blend": f"{P}/x_hood.blend", "pivot": hood["pivot"],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": EV["hood_open0"], "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": EV["hood_open1"], "loc": [0, 0, 0], "rot": [hood["open_deg"], 0, 0], "ease": "inout"}]},
                          {"blend": f"{P}/x_hatch.blend", "pivot": hatch["pivot"],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": EV["hatch_open0"], "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": EV["hatch_open1"], "loc": [0, 0, 0], "rot": [hatch["open_deg"], 0, 0], "ease": "inout"}]}],
                "cam": [orbit(SECS["s5_open"] * k / 12, 4.9 + 0.5 * math.sin(math.pi * k / 12), 32 + 118 * smooth(k / 12),
                              2.55 - 0.15 * (k / 12), c=(0, -0.9 + 1.8 * smooth(k / 12), 0.6), focal=30, ease="lin", tz=0.75)
                        for k in range(13)]},
}

# 7. top-down, slow spin; the four doors pop straight out sideways on an accent (doors are full-skinned: door scan
#    + the car's own skin inside each door outline; openings from "Doors and Hood Open")
DOOR_OUT = {"fl": (0.95, 0.0, 0.0), "rl": (0.95, 0.12, 0.0), "fr": (-0.95, 0.0, 0.0), "rr": (-0.95, 0.12, 0.0)}


def door_keys(d, t0, t1, delay=0.0):
    off = DOOR_OUT[d]
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": t0 + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": t1 + delay, "loc": list(off), "rot": [0, 0, 0], "ease": "out"}]


T7 = SECS["s7_top"]
SHOTS["s7_top"] = {
    "base": [f"{P}/comp_doors.blend"],
    "parts": [{"blend": f"{P}/x_door_{d}.blend", "keys": door_keys(d, EV["doors_out0"], EV["doors_out1"], 0.0 if d[0] == "f" else 0.07)}
              for d in ("fl", "fr", "rl", "rr")],
    # straight down, front at the top of frame; slow 14 deg spin + slight rise as the doors leave
    "cam": [{"t": T7 * k / 6, "loc": [0.02 * math.sin(math.radians(-7 + 14 * k / 6)), 0.02 * math.cos(math.radians(-7 + 14 * k / 6)),
                                       7.0 + 0.5 * k / 6],
             "target": [0, 0, 0.5], "focal": 30, "ease": "lin"} for k in range(7)]}

# 8. exploded view: doors are already out (continuity from s7); the rest separate on the accent, drift while the
#    camera orbits front-left -> left side -> rear-left, then everything flies home and LOCKS on a heavy accent.
SEP, HOLD, BACK, LOCK = EV["sep"], EV["hold"], EV["back"], EV["lock"]


def explode(off, rot=(0, 0, 0), delay=0.0, start=None):
    s = list(start) if start else [0, 0, 0]
    return [{"t": 0, "loc": s, "rot": [0, 0, 0]},
            {"t": SEP + delay, "loc": s, "rot": [0, 0, 0]},
            {"t": HOLD + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": BACK, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},  # slow drift outward
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


def door_x(d):
    o = DOOR_OUT[d]
    return [{"t": 0, "loc": list(o), "rot": [0, 0, 0]},
            {"t": BACK, "loc": [o[0] * 1.12, o[1], o[2]], "rot": [0, 0, 0], "ease": "lin"},
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


T8 = SECS["s8_explode"]
SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_explode.blend"],
    "parts": [
        # portrait: panels stack ABOVE the car (Temerario 25-31 s) instead of flying fore/aft past the frame edges
        {"blend": f"{P}/x_hood.blend", "keys": explode((0, -0.15, 1.35), (-10, 0, 0))},
        {"blend": f"{P}/x_fbumper.blend", "keys": explode((0, -0.5, 0.6))},
        {"blend": f"{P}/x_fender.blend", "keys": explode((0.55, -0.1, 0.8), (0, 10, 0), 0.05)},
        {"blend": f"{P}/x_hatch.blend", "keys": explode((0, 0.25, 1.15), (15, 0, 0), 0.08)},
        {"blend": f"{P}/x_rbumper.blend", "keys": explode((0, 0.5, 0.6), delay=0.04)},
    ] + [{"blend": f"{P}/x_door_{d}.blend", "keys": door_x(d)} for d in ("fl", "fr", "rl", "rr")],
    "cam": [orbit(T8 * k / 12, 6.0 + 1.1 * math.sin(math.pi * k / 12), 38 + 97 * smooth(k / 12), 3.3 - 0.5 * (k / 12),
           c=(0.1, 0.0, 0.7), focal=28, ease="lin", tz=0.75) for k in range(13)]}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if mode == "preview":
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
