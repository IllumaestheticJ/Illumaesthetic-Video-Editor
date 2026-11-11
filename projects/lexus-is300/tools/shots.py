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

# v2 opening (user: "car is clipped at beginning"): whole car in frame (~65 % width, Temerario), slow push, little rotation
SHOTS["s1_wide"] = {"base": [CAR], "cam": arc(S("s1_wide"), 6, 8.2, 7.6, -42, -50, 1.2, 1.3, c0=(0, -0.4, 0.6), focal=30)}
SHOTS["s2_rear"] = {"base": [CAR], "cam": arc(S("s2_rear"), 6, 8.0, 7.5, 142, 132, 1.25, 1.5, c0=(0, 0.4, 0.6), focal=30)}

# v2 explode (user: "focus on specific sections"): ONE global part timeline in video seconds, seen section by
# section - front bumper (s5/s6), rear bumper + trunk lid (s7), side skirt (s8), all out -> home -> LOCK (s9).
# Parts move along clean axes into clear black (never across the body or at the lens), no spins.
G_BACK, G_LOCK = bt(42.5), bt(46)
PARTS = [  # blend, offset (m), rot (deg), pivot, separate start, end (video s)
    ("fbumper", (0, -0.8, 0.05), (0, 0, 0), None, bt(21), bt(23)),
    ("rearbumper", (0, 0.8, 0.05), (0, 0, 0), None, bt(30.5), bt(32.5)),
    ("lid", (0, 0.2, 0.75), (12, 0, 0), [0, 1.95, 0.95], bt(31), bt(33)),
    ("sideskirt", (-0.55, 0, 0.05), (0, 0, 0), None, bt(34.5), bt(36)),
]


def parts_for(shot):
    t0, out = T0[shot], []
    for name, off, rot, piv, a, b in PARTS:
        p = {"blend": f"{B}/{name}.blend", "keys": [
            {"t": min(0.0, a - t0) - 1, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": a - t0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": b - t0, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": G_BACK - t0, "loc": [o * 1.05 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": G_LOCK - t0, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]}
        if piv:
            p["pivot"] = piv
        out.append(p)
    return out


XB = f"{B}/comp_explode.blend"
SHOTS.update({
    # front corner, framed on the nose: bumper slides straight forward off the FMIC/radiator/crash structure
    "s5_front": {"base": [XB], "parts": parts_for("s5_front"),
                 "cam": arc(S("s5_front"), 6, 3.9, 3.4, -42, -30, 1.25, 1.45, c0=(0, -1.95, 0.5), focal=28)},
    # high over the open front end, looking down into the intercooler/radiator, bumper floating ahead
    "s6_core": {"base": [XB], "parts": parts_for("s6_core"), "cam": [
        {"t": 0, "loc": [0.85, -4.75, 2.45], "target": [0.05, -2.3, 0.35], "focal": 28},
        {"t": S("s6_core"), "loc": [0.4, -4.5, 2.35], "target": [0.0, -2.3, 0.33], "focal": 28, "ease": "inout"}]},
    # rear-left high 3/4, framed on the tail: bumper slides back, trunk lid lifts off its opening
    "s7_rear": {"base": [XB], "parts": parts_for("s7_rear"),
                "cam": arc(S("s7_rear"), 6, 4.2, 3.9, 142, 154, 2.0, 2.2, c0=(0, 1.9, 0.55), focal=28)},
    # low along the right sill: skirt slides straight out
    "s8_side": {"base": [XB], "parts": parts_for("s8_side"), "cam": [
        {"t": 0, "loc": [-2.9, -1.6, 1.55], "target": [-1.0, 0.1, 0.2], "focal": 28},
        {"t": S("s8_side"), "loc": [-2.9, -0.7, 1.5], "target": [-1.0, 0.7, 0.2], "focal": 28, "ease": "inout"}]},
    # high rear-right diagonal: everything out, flies home, LOCKS on beat 46 (last hit), fade to black in the edit
    "s9_wide": {"base": [XB], "parts": parts_for("s9_wide"),
                "cam": arc(S("s9_wide"), 10, 6.6, 7.0, -142, -124, 5.6, 5.0, c0=(0, 0, 0.4), focal=28)},
})


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
