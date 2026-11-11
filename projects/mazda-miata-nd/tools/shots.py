"""Shot specs for the Mazda Miata ND Temerario-style scan reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/mazda-miata-nd/tools/shots.py preview|final [shot ...]   # writes specs, prints paths
    blender -b -P projects/ferrari-296/tools/shot.py -- <spec.json>

Scan frame (prepped, metres): front = -Y, car's right = -X, ground Z=0; length 3.91 m, height 1.22 m.
Orbit angle 0 = camera in front of the car, -90 = car's right, 180 = behind.
Shot lengths and in-shot action times come from projects/mazda-miata-nd/timing.json (written from the
music's measured accents) so every move lands on the beat; defaults are used before the music exists.
"""
import json
import math
import os
import sys

W = "/home/user/media/work/miata"
P = f"{W}/prep"
OUT = f"{W}/renders"
SPECS = f"{W}/specs"
HERE = os.path.dirname(os.path.abspath(__file__))
TIMING = os.path.join(HERE, "..", "timing.json")

T = {"beat": 0.6, "secs": {"s1_turntable": 6.0, "s2_rear": 5.0, "s3_wheel": 3.6, "s4_lamp": 3.6, "s5_front": 5.0,
                           "s6_rear_open": 5.0, "s7_top": 4.0, "s8_explode": 10.0}}
if os.path.exists(TIMING):
    T = json.load(open(TIMING))
BEAT = T["beat"]
SECS = T["secs"]
ACT = T.get("act", {})  # optional per-shot action times (s)

CAR = f"{P}/car4np.blend"        # 4 mm, licence plate flattened (tools/flatten_plate.py): full-car moves
CAR_F2 = f"{P}/car2_front.blend"  # 2 mm front half: close-ups
HOOD_PIVOT = [-0.1237, -0.458, 0.8887]   # tools/hinge.py fit (prepped m), opens -43.67 deg about X
TRUNK_PIVOT = [-0.1237, 1.3358, 0.9865]  # opens +85.69 deg about X
HOOD_OPEN, TRUNK_OPEN = -43.67, 85.69


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, r0, r1, a0, a1, h0, h1, c0, c1=None, focal=30, n=8, tz=None):
    """Orbit keyed every 1/n of the move (linear loc between far keys would cut a chord toward the car)."""
    c1 = c1 or c0
    keys = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if T.get("ease_arcs", True) else u
        c = [a + (b - a) * e for a, b in zip(c0, c1)]
        keys.append(orbit(secs * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal,
                          ease="lin", tz=tz))
    return keys


def hold_then(t0, t1, loc=(0, 0, 0), rot=(0, 0, 0), ease="inout"):
    z = [0, 0, 0]
    return [{"t": 0, "loc": z, "rot": z}, {"t": t0, "loc": z, "rot": z},
            {"t": t1, "loc": list(loc), "rot": list(rot), "ease": ease}]


S = SECS
SHOTS = {
    # 1. slow front 3/4 turntable, low, moving from frame 1 (hook): car's right front -> more side-on
    "s1_turntable": {"base": [CAR], "cam": arc(S["s1_turntable"], 4.6, 4.4, -28, -58, 0.95, 1.1, (0, -0.15, 0.5))},
    # 2. rear 3/4 orbit on the other side (car's left rear), rising slightly
    "s2_rear": {"base": [CAR], "cam": arc(S["s2_rear"], 4.4, 4.2, 152, 124, 0.8, 1.3, (0, 0.15, 0.5))},
    # 3. extreme close-up: front right wheel (6-spoke, brake behind), slow slide forward along the tyre
    "s3_wheel": {"base": [CAR_F2], "cam": [
        {"t": 0, "loc": [-1.95, -0.62, 0.40], "target": [-0.86, -1.12, 0.33], "focal": 40},
        {"t": S["s3_wheel"], "loc": [-1.94, -1.12, 0.41], "target": [-0.86, -1.18, 0.33], "focal": 40, "ease": "inout"}]},
    # 4. detail: right headlight + grille, sliding across the nose toward the badge
    "s4_lamp": {"base": [CAR_F2], "cam": [
        {"t": 0, "loc": [-1.55, -2.75, 0.88], "target": [-0.55, -1.72, 0.64], "focal": 38},
        {"t": S["s4_lamp"], "loc": [-1.05, -2.92, 0.85], "target": [-0.45, -1.78, 0.62], "focal": 38, "ease": "inout"}]},
}

# 5. front opens: bumper slides forward (pull), then the hood swings up on its fitted hinge to the captured pose
a5 = ACT.get("s5_front", {"bumper": [BEAT, 3 * BEAT], "hood": [2.5 * BEAT, 5 * BEAT]})
SHOTS["s5_front"] = {
    "base": [f"{P}/comp_front.blend"],
    "parts": [{"blend": f"{P}/x_fbumper.blend", "keys": hold_then(a5["bumper"][0], a5["bumper"][1], (0, -0.85, -0.05))},
              {"blend": f"{P}/x_hood.blend", "pivot": HOOD_PIVOT,
               "keys": hold_then(a5["hood"][0], a5["hood"][1], rot=(HOOD_OPEN, 0, 0))}],
    "cam": arc(S["s5_front"], 4.3, 3.9, -36, -18, 2.0, 2.3, (0, -1.25, 0.45), (0, -1.35, 0.45), n=6)}

# 6. rear opens: rear bumper slides back, trunk lid swings up to its captured pose
a6 = ACT.get("s6_rear_open", {"bumper": [BEAT, 3 * BEAT], "trunk": [2.5 * BEAT, 5 * BEAT]})
SHOTS["s6_rear_open"] = {
    "base": [f"{P}/comp_rear.blend"],
    "parts": [{"blend": f"{P}/x_rbumper.blend", "keys": hold_then(a6["bumper"][0], a6["bumper"][1], (0.15, 0.8, -0.12))},
              {"blend": f"{P}/x_trunk.blend", "pivot": TRUNK_PIVOT,
               "keys": hold_then(a6["trunk"][0], a6["trunk"][1], rot=(TRUNK_OPEN, 0, 0))}],
    "cam": arc(S["s6_rear_open"], 4.5, 4.2, 232, 214, 2.0, 2.4, (0, 1.2, 0.55), (0, 1.35, 0.55), n=6)}

# 7. top-down: from a high rear-left 3/4 up and over to ~12 deg off vertical from BEHIND (nose at the top of frame).
# Never pass straight overhead: to_track_quat's up vector is undefined there and the image rolls (v1 snapped ~90 deg).
SHOTS["s7_top"] = {"base": [CAR], "cam": [
    {"t": 0, "loc": [2.3, 3.7, 3.0], "target": [0, 0.2, 0.5], "focal": 30},
    {"t": S["s7_top"], "loc": [0.0, 0.95, 4.95], "target": [0, 0.05, 0.5], "focal": 30, "ease": "inout"}]}

# 8. exploded view: panels separate on an accent, drift while the camera orbits, fly home and LOCK on an accent
a8 = ACT.get("s8_explode", {"sep": 0.0, "hold": 3 * BEAT, "back": S["s8_explode"] - 5 * BEAT, "lock": S["s8_explode"] - 2 * BEAT})


def explode(off, rot=(0, 0, 0), delay=0.0):
    z = [0, 0, 0]
    return [{"t": 0, "loc": z, "rot": z}, {"t": a8["sep"] + delay, "loc": z, "rot": z},
            {"t": a8["hold"] + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": a8["back"], "loc": [o * 1.07 for o in off], "rot": list(rot), "ease": "lin"},  # slow drift outward
            {"t": a8["lock"], "loc": z, "rot": z, "ease": "in"}]


# panels stack ABOVE / around the car (Temerario 25-31 s; portrait-friendly), bumpers flip to show their insides
SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_explode.blend"],
    "parts": [
        {"blend": f"{P}/x_hood.blend", "pivot": HOOD_PIVOT, "keys": explode((0, -0.1, 0.95), (-10, 0, 0))},
        {"blend": f"{P}/x_fbumper.blend", "keys": explode((0, -0.3, 0.7), (-20, 0, 0), 0.05)},
        {"blend": f"{P}/x_trunk.blend", "pivot": TRUNK_PIVOT, "keys": explode((0, 0.05, 0.85), (10, 0, 0), 0.1)},
        {"blend": f"{P}/x_rbumper.blend", "keys": explode((0, 0.3, 0.75), (20, 0, 0), 0.15)},
        {"blend": f"{P}/x_skirt.blend", "keys": explode((-0.5, 0, 0.12), delay=0.08)},
        {"blend": f"{P}/x_mirror_r.blend", "keys": explode((-0.3, 0.0, 0.45), delay=0.12)},
        {"blend": f"{P}/x_mirror_l.blend", "keys": explode((0.3, 0.0, 0.45), delay=0.12)},
    ],
    "cam": arc(S["s8_explode"], 6.1, 6.3, -32, -78, 3.0, 2.7, (0, -0.1, 1.0), (0, 0.1, 1.0), n=12, tz=0.95)}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if not final:
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
