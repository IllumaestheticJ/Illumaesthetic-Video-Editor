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
HINGE = [0.0, 1.757, 1.094]
RB_TIP = -110   # rear bumper tip about X (deg): inner face turns up/back toward the rear camera; sign checked on a still       # trunk-lid hinge line (lid front edge at the rear-window base)


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


T0 = CUES["t0"]                 # shot start in video seconds
P0 = CUES["phase"]


def bt(n):
    """video seconds of beat n (kick grid)"""
    return P0 + n * BEAT


# v1 shots (s3_wheel, s4_nose renders are reused unchanged in v2)
SHOTS = {
    "s3_wheel": {"base": [CAR2], "cam": [
        {"t": 0, "loc": [-1.95, -0.85, 0.42], "target": [-0.85, -1.38, 0.34], "focal": 38},
        {"t": S("s3_wheel"), "loc": [-1.95, -1.95, 0.40], "target": [-0.85, -1.45, 0.34], "focal": 38, "ease": "inout"}]},
    "s4_nose": {"base": [CAR2], "cam": [
        {"t": 0, "loc": [-1.55, -3.35, 0.95], "target": [-0.55, -2.05, 0.72], "focal": 36},
        {"t": S("s4_nose"), "loc": [-0.25, -3.6, 0.85], "target": [-0.3, -2.1, 0.66], "focal": 36, "ease": "inout"}]},
}

# v2 opening (user: "car is clipped at beginning"): whole car in frame (68-78 % width, >=9 % margins), slow push
SHOTS["s1_wide"] = {"base": [CAR], "cam": arc(S("s1_wide"), 6, 8.2, 7.6, -42, -50, 1.2, 1.3, c0=(0, -0.4, 0.6), focal=30)}

# v2 parts (direction.md): ONE global timeline in BEATS, keyed into every shot so parts are continuous across cuts.
# Front bumper = derived outer skin (no inner face): translate only. Rear bumper = part scan with a clean scanned
# inside (chk/backs.jpg): tipped about the width axis toward the camera. Skirt backside not useful: translate only.
# key: (beat, offset, rot, ease)
Z = (0, 0, 0)
PARTS = {
    "fbumper": (None, [(16, Z, Z, "lin"), (17.5, (0, -0.8, -0.3), Z, "out"), (38, (0, -0.84, -0.32), Z, "lin"),
                       (41, (0, -0.84, 0.08), Z, "out"), (43.5, (0, -0.84, 0.08), Z, "lin"), (45, Z, Z, "in")]),
    "sideskirt": ([-0.75, -0.14, 0.26], [(25, Z, Z, "lin"), (26.5, (-0.55, 0, -0.08), Z, "out"),
                                         (38, (-0.58, 0, -0.09), Z, "lin"), (41, (-0.58, 0, 0.31), Z, "out"),
                                         (43, (-0.58, 0, 0.31), Z, "lin"), (44, Z, Z, "in")]),
    "rearbumper": ([-0.04, 1.86, 0.46], [(31, Z, Z, "lin"), (32.5, (0, 0.95, 0.25), Z, "out"),
                                         (34.5, (0, 0.95, 0.25), (RB_TIP, 0, 0), "inout"),
                                         (38, (0, 0.98, 0.26), (RB_TIP, 0, 0), "lin"),
                                         (41, (0, 0.98, 0.66), (RB_TIP, 0, 0), "out"),
                                         (44, (0, 0.98, 0.66), (RB_TIP, 0, 0), "lin"), (46, Z, Z, "in")]),
    "lid": ([0, 1.95, 0.95], [(33, Z, Z, "lin"), (34.5, (0, 0.1, 0.75), Z, "out"), (38, (0, 0.1, 0.78), Z, "lin"),
                              (41, (0, 0.1, 1.15), Z, "out"), (44.5, (0, 0.1, 1.15), Z, "lin"), (46, Z, Z, "in")]),
}


def parts_for(shot):
    t0, out = T0[shot], []
    for name, (piv, keys) in PARTS.items():
        k = [{"t": -100.0, "loc": [0, 0, 0], "rot": [0, 0, 0]}]
        for beat, off, rot, ease in keys:
            k.append({"t": bt(beat) - t0, "loc": list(off), "rot": list(rot), "ease": ease})
        p = {"blend": f"{B}/{name}.blend", "keys": k}
        if piv:
            p["pivot"] = piv
        out.append(p)
    return out


def L(beat, shot):
    return bt(beat) - T0[shot]


XB = f"{B}/comp_explode.blend"
SHOTS.update({
    # HERO: front end. Bumper releases ON the drop (beat 16), forward + down into black; camera pushes in on the
    # intercooler, then swings to the front-right corner (hands off to the side). No rotation before beat 21.
    "s5_front": {"base": [XB], "parts": parts_for("s5_front"), "cam": [
        {"t": 0, "loc": [0.25, -5.9, 1.15], "target": [0, -2.0, 0.45], "focal": 30},
        {"t": L(17.5, "s5_front"), "loc": [0.15, -5.5, 1.10], "target": [0, -2.0, 0.45], "focal": 30, "ease": "inout"},
        {"t": L(21, "s5_front"), "loc": [0.05, -4.3, 0.95], "target": [0, -2.0, 0.42], "focal": 30, "ease": "inout"},
        {"t": S("s5_front"), "loc": [-1.9, -5.2, 1.2], "target": [-0.15, -2.45, 0.3], "focal": 30, "ease": "inout"}]},
    # side: dolly rearward along the right sill, skirt slides out into black beside the car
    "s6_side": {"base": [XB], "parts": parts_for("s6_side"), "cam": [
        {"t": 0, "loc": [-2.6, -1.9, 1.8], "target": [-1.0, 0.1, 0.05], "focal": 30},
        {"t": S("s6_side"), "loc": [-2.7, -0.7, 1.85], "target": [-1.0, 0.7, 0.05], "focal": 30, "ease": "inout"}]},
    # rear: high rear-right 3/4, bumper back + tipped to show its inside, lid lifts off the Rear Trunk Open state
    "s7_rear": {"base": [XB], "parts": parts_for("s7_rear"), "cam": [
        {"t": 0, "loc": [-1.4, 5.4, 2.3], "target": [0, 1.8, 0.6], "focal": 30},
        {"t": L(34, "s7_rear"), "loc": [-1.15, 5.0, 2.5], "target": [0, 1.8, 0.68], "focal": 30, "ease": "inout"},
        {"t": S("s7_rear"), "loc": [-0.85, 4.6, 2.7], "target": [0, 1.75, 0.72], "focal": 30, "ease": "inout"}]},
    # finale: high behind (nose at top), parts lift on beat 40 (loudest), land on the triple hit 44/45/46, rear-left 3/4
    "s8_finale": {"base": [XB], "parts": parts_for("s8_finale"), "cam": [
        {"t": 0, "loc": [-0.4, 2.0, 7.0], "target": [-0.2, -0.1, 0.4], "focal": 28},
        {"t": L(42, "s8_finale"), "loc": [0.6, 2.6, 6.2], "target": [0, 0, 0.45], "focal": 28, "ease": "inout"},
        {"t": L(44, "s8_finale"), "loc": [1.6, 3.6, 6.0], "target": [0, 0.1, 0.5], "focal": 28, "ease": "inout"},
        {"t": L(46.5, "s8_finale"), "loc": [3.7, 4.9, 3.25], "target": [0, 0.15, 0.55], "focal": 28, "ease": "inout"},
        {"t": S("s8_finale"), "loc": [3.62, 4.82, 3.2], "target": [0, 0.15, 0.55], "focal": 28, "ease": "lin"}]},
})


def spec(name, mode):
    s = SHOTS[name]
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 4 / 15,  # +3 tail frames: minterpolate drops ~2 (subaru lesson) "fps": 15, "res": "1080x1920",
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
