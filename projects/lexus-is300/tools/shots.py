"""Shot specs for the Lexus IS300 Temerario-style reel -> JSON for tools/shot.py (copy of the ferrari-296
sibling renderer: keyed camera + parts on pivots, house silver on black, + exposure).

    python projects/lexus-is300/tools/shots.py preview|final|still [shot ...]

Prepped frame (metres): nose at -Y, car's right = -X, floor Z=0; length 4.47 m, width 1.86 m incl. mirrors,
height 1.44 m. Shot lengths come from projects/lexus-is300/cues.json (seconds, set from the track's accents).
"""
import json
import math
import os
import sys

W = "/home/user/media/work/is300"
B = f"{W}/blend"
OUT = f"{W}/renders"
SPECS = f"{W}/specs"
HERE = os.path.dirname(os.path.abspath(__file__))
CUES = json.load(open(os.path.join(HERE, "..", "cues.json")))
SECS = CUES["secs"]          # shot -> seconds
BEAT = CUES["beat"]
CAR = f"{B}/car.blend"       # 4 mm full car
CAR2 = f"{B}/car2.blend"     # 2 mm full car (close-ups)
ROOT = (-0.0141, 0.1920, 0.7641)  # prepped = levelled_mm / 1000 + ROOT
HINGE = [0.0, 1.757, 1.094]       # trunk-lid hinge line (lid front edge at the rear-window base)


def orbit(t, r, ang_deg, h, c=(0, 0, 0.6), focal=30, ease="inout", tz=None):
    """angle 0 = in front of the car (-Y); -90 = car's right (-X); +90 = car's left (+X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(T, n, r0, r1, a0, a1, h0, h1, c0=(0, 0, 0.6), c1=None, focal=30, tz=None, ease_all=True):
    """Orbit keyed every T/n so the camera follows the circle (linear between far keys would cut a chord).
    Whole move eased in/out by remapping the parameter."""
    c1 = c1 or c0
    keys = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if ease_all else u
        c = [a + (b - a) * e for a, b in zip(c0, c1)]
        keys.append(orbit(T * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal,
                          ease="lin", tz=tz))
    return keys


def S(name):
    return SECS[name]


SHOTS = {
    # 1. slow front 3/4 turntable, low; moving from frame 1 (hook)
    "s1_front34": {"base": [CAR], "cam": arc(S("s1_front34"), 8, 4.0, 3.8, -34, -56, 0.85, 1.0, c0=(0, -0.45, 0.55))},
    # 2. rear 3/4 orbit on the other side, slight rise
    "s2_rear34": {"base": [CAR], "cam": arc(S("s2_rear34"), 8, 4.0, 3.8, 152, 132, 0.8, 1.2, c0=(0, 0.45, 0.6))},
    # 3. extreme close-up: front-right wheel (multi-spoke wheel + brake), slow slide
    "s3_wheel": {"base": [CAR2], "cam": [
        {"t": 0, "loc": [-1.95, -0.85, 0.42], "target": [-0.85, -1.38, 0.34], "focal": 38},
        {"t": S("s3_wheel"), "loc": [-1.95, -1.95, 0.40], "target": [-0.85, -1.45, 0.34], "focal": 38, "ease": "inout"}]},
    # 4. detail: headlight + grille, slide across the nose
    "s4_nose": {"base": [CAR2], "cam": [
        {"t": 0, "loc": [-1.55, -3.35, 0.95], "target": [-0.55, -2.05, 0.72], "focal": 36},
        {"t": S("s4_nose"), "loc": [-0.25, -3.6, 0.85], "target": [-0.3, -2.1, 0.66], "focal": 36, "ease": "inout"}]},
    # 5. front bumper comes off forward/down -> FMIC, radiator, crash structure from the 'bumper removed' scan
    "s5_front_off": {"base": [f"{B}/comp_front.blend"],
                     "parts": [{"blend": f"{B}/fbumper.blend", "keys": [
                         {"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                         {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                         {"t": 3 * BEAT, "loc": [0, -0.55, 0.45], "rot": [0, 0, 0], "ease": "inout"},
                         {"t": 99, "loc": [0, -0.62, 0.50], "rot": [0, 0, 0], "ease": "lin"}]}],
                     "cam": arc(S("s5_front_off"), 6, 3.9, 3.5, -24, -10, 1.5, 1.4, c0=(0, -1.8, 0.6), c1=(0, -2.0, 0.6))},
    # 6. trunk opens on its hinge -> trunk interior from the 'Rear Trunk Open' scan
    "s6_trunk": {"base": [f"{B}/comp_trunk.blend"],
                 "parts": [{"blend": f"{B}/lid.blend", "pivot": HINGE, "keys": [
                     {"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                     {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                     {"t": 4 * BEAT, "loc": [0, 0, 0], "rot": [62, 0, 0], "ease": "inout"}]}],
                 "cam": [{"t": 0, "loc": [1.35, 4.15, 2.35], "target": [0, 1.75, 0.8], "focal": 30},
                         {"t": S("s6_trunk"), "loc": [0.65, 3.85, 2.6], "target": [0, 1.8, 0.75], "focal": 30, "ease": "out2"}]},
    # 7. top-down: high front-left 3/4 up and over to straight down, nose at the BOTTOM (explode then opens nose-up)
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [2.0, -4.2, 4.0], "target": [0, -0.3, 0.5], "focal": 30},
        {"t": S("s7_top"), "loc": [0.0, -0.2, 6.6], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}


def explode(off, rot=(0, 0, 0), delay=0.0):
    sep, hold, back, lock = CUES["x_sep"], CUES["x_hold"], CUES["x_back"], CUES["x_lock"]
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": sep + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": hold + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": back, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": lock, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


# 8. exploded view (right side): panels lift/slide off, drift while the camera orbits front-right -> rear-right,
# fly home and lock. Stacked up/out (Temerario 25-31 s: panels float in layers above the car), never at the lens.
SHOTS["s8_explode"] = {
    "base": [f"{B}/comp_explode.blend"],
    "parts": [
        {"blend": f"{B}/sideskirt.blend", "keys": explode((-0.6, 0, 0.35))},
        {"blend": f"{B}/fbumper.blend", "keys": explode((0, -0.85, 0.35), delay=0.08)},
        {"blend": f"{B}/rearbumper.blend", "keys": explode((0, 0.75, 0.45), delay=0.12)},
        {"blend": f"{B}/lid.blend", "keys": explode((0, 0.15, 0.9), (15, 0, 0), 0.16)},
    ],
    # steep high rear-right 3/4 (~50 deg down), nose at the top of the 9:16 frame so the car's length + the
    # front/rear bumper gaps run along the frame height; slow 25 deg orbit for parallax
    "cam": arc(S("s8_explode"), 12, 3.3, 3.6, -174, -148, 5.6, 5.3, c0=(0, -0.25, 0.4), focal=26),
}


def spec(name, mode):
    s = SHOTS[name]
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if mode == "final" else 30, "samples": 12 if mode == "final" else 6,
          "out": f"{OUT}/{mode}/{name}", "exposure": -0.5}
    if mode == "still":
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
