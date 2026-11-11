"""Shot specs for the Nissan 400Z Temerario-style reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/nissan-400z/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Prepped scan frame (metres): nose at -Y, car's right = -X, ground Z=0; length 4.40 m (y -2.17..2.23),
height 1.32 m. Front wheels y~-1.25, rear y~1.40, track x~+-0.8. Durations come from projects/nissan-400z/cues.json
("secs": {shot: seconds}) once the track is measured; renders carry 1 extra frame so the cut never runs dry.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/z400/blend"
OUT = "/home/user/media/work/z400/renders"
SPECS = "/home/user/media/work/z400/specs"
HINGE = json.load(open(os.path.join(HERE, "..", "hinge.json")))
CUES = json.load(open(os.path.join(HERE, "..", "cues.json")))
SECS = CUES["secs"]
CAR = f"{B}/car.blend"          # 3 mm: full-car moves
FRONT = f"{B}/front2.blend"     # 2 mm crops for close-ups (seam outside frame)
REAR = f"{B}/rear2.blend"
SIDE = f"{B}/side2.blend"    # right side, rear of the A-pillar


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, r0, r1, a0, a1, h0, h1, c0=(0, 0, 0.55), c1=None, focal=30, n=8, ease_out=True, tz=None):
    """Smooth orbit sampled every 1/n (linear chords between far keys would cut toward the car)."""
    c1 = c1 or c0
    keys = []
    for k in range(n + 1):
        u = k / n
        e = 1 - (1 - u) ** 2 if ease_out else u * u * (3 - 2 * u)
        c = [a + (b - a) * e for a, b in zip(c0, c1)]
        keys.append(orbit(secs * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal, ease="lin", tz=tz))
    return keys


def slide(secs, p0, t0, p1, t1, focal):
    return [{"t": 0, "loc": p0, "target": t0, "focal": focal},
            {"t": secs, "loc": p1, "target": t1, "focal": focal, "ease": "inout"}]


S = SECS
SHOTS = {
    # 1. slow low front 3/4 turntable (fade up from black in the edit)
    "s1_front34": {"base": [CAR], "cam": arc(S["s1_front34"], 5.3, 5.0, -22, -50, 0.95, 1.05, c0=(0, -0.15, 0.55), focal=30)},
    # 2. rear 3/4 orbit on the other side, slight rise
    "s2_rear34": {"base": [CAR], "cam": arc(S["s2_rear34"], 5.2, 5.0, 162, 138, 0.8, 1.2, c0=(0, 0.15, 0.55), focal=30)},
    # 3. close-up glide along the right rear haunch / door shut line toward the C-pillar (2 mm right-rear crop).
    #    (Wheel close-up dropped: the dark rims scanned as hollow spoke fragments - see editlog.)
    "s3_haunch": {"base": [SIDE], "cam": slide(S["s3_haunch"], [-1.08, 2.75, 1.55], [-0.8, 0.9, 0.85],
                                                [-1.28, 1.55, 1.5], [-0.75, -0.3, 0.85], 35)},
    # 4. extreme close-up: headlight + grille edge, slide across the nose
    "s4_lamp": {"base": [FRONT], "cam": slide(S["s4_lamp"], [-1.55, -2.95, 0.95], [-0.55, -1.85, 0.68],
                                              [-0.45, -3.3, 0.85], [-0.35, -1.95, 0.62], 40)},
    # 5. extreme close-up: full-width tail lamp bar + badge, slow lateral slide
    "s5_tail": {"base": [REAR], "cam": slide(S["s5_tail"], [1.35, 3.5, 1.05], [0.25, 2.15, 0.85],
                                             [-0.6, 3.6, 1.0], [-0.25, 2.15, 0.85], 38)},
    # 6. hood opens on the fitted hinge (engine bay from 'Hood Open'), high front 3/4, camera eases in
    "s6_hood": {"base": [f"{B}/comp_hood.blend"],
                "parts": [{"blend": f"{B}/p_hood.blend", "pivot": HINGE["pivot"],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": CUES.get("hood_start", 0.5), "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": CUES.get("hood_open", 2.4), "loc": [0, 0, 0], "rot": [HINGE["open_deg"], 0, 0], "ease": "inout"}]}],
                "cam": arc(S["s6_hood"], 3.9, 3.4, -34, -20, 2.2, 2.4, c0=(0, -1.0, 0.6), c1=(0, -1.15, 0.65), focal=30)},
    # 7. top-down: from a high rear 3/4 up and over to straight down, nose to the top of the frame
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [1.9, 4.4, 3.8], "target": [0, 0.3, 0.5], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, 0.15, 6.8], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}

# 8. exploded view: panels separate on an accent, drift while the camera orbits, fly home and lock on a later accent.
SEP, HOLD, BACK, LOCK = (CUES.get("ex_" + k, v) for k, v in (("sep", 0.25), ("hold", 2.2), ("back", 6.0), ("lock", 8.0)))


def explode(off, rot=(0, 0, 0), delay=0.0):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": HOLD + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": BACK, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


# portrait-friendly: panels mostly stack UP (Temerario 25-31 s) and only modestly fore/aft/out
SHOTS["s8_explode"] = {
    "base": [f"{B}/comp_explode.blend"],
    "parts": [
        {"blend": f"{B}/p_hood.blend", "keys": explode((0, -0.05, 1.45), (-8, 0, 0))},
        {"blend": f"{B}/bumper_shell.blend", "keys": explode((0, -0.22, 0.62), delay=0.05)},
        {"blend": f"{B}/p_grille.blend", "keys": explode((0, -0.3, 1.02), delay=0.12)},
        {"blend": f"{B}/p_wing.blend", "keys": explode((0, 0.1, 0.85), (14, 0, 0), 0.08)},
        {"blend": f"{B}/p_mirror_r.blend", "keys": explode((-0.45, 0, 0.35), (0, 0, -20), 0.1)},
        {"blend": f"{B}/p_mirror_l.blend", "keys": explode((0.45, 0, 0.35), (0, 0, 20), 0.1)},
    ],
    "cam": arc(S["s8_explode"], 5.3, 5.6, -18, -55, 4.4, 3.8, c0=(0, -0.55, 0.75), c1=(0, -0.35, 0.75), focal=28, n=12,
               ease_out=False, tz=0.7)}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if mode == "frames":
        sp["frames"] = ["first", "mid", "last"]
        sp["out"] = f"{OUT}/frames/{name}"
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
