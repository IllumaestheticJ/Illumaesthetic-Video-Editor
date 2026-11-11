"""Shot specs v2 for the Mazda 3 (gen 4) scan reel -> JSON for projects/ferrari-296/tools/shot.py.
v1 (tools/shots_v1.py) cropped the car (101-143 % of the frame width even in the 'wide' shots; 70 mm close-ups).
User: "too much of the car is cropped - this is just a standard full car scan". v2: EVERY shot shows the whole car.
Each camera key is pulled back/in along its view line until the car (+ lifted parts) spans FIT of the 9:16 frame
(tools/fitcheck.py projection; +-1 = frame edge), so framing is measured, not guessed.

    python projects/mazda-3-gen4/tools/shots.py preview|final [shot ...]

Scan frame (prepped car4.json, metres): nose = -Y, car's LEFT = +X (clean side), body z 0.08..1.53.
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitcheck as fc  # noqa: E402

P = "/home/user/media/mazda-3-gen4/prep"
OUT = "/home/user/media/work/m3/renders"
SPECS = "/home/user/media/work/m3/specs"
CAR = f"{P}/car4.blend"
BEAT = 0.5453  # mazda-3-gen4_track.mp3: 110.0 BPM, grid fitted on kick peaks (tools/music_grid.py)
SECS = {"s1_front34": 4.6, "s2_rear34": 4.6, "s3_front": 2.5, "s4_side": 2.5, "s5_rear": 2.5,
        "s6_wing": 4.6, "s7_top": 3.6, "s8_explode": 12.4}
FIT = 0.86

_TRI = np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
_J = json.load(open(f"{P}/car4.json"))
def _pts(stl, step=20):
    return np.fromfile(stl, dtype=_TRI, offset=84)["v"].mean(1)[::step] * _J["unit_scale"] + np.array(_J["root_location"])
WING = _pts("/home/user/media/mazda-3-gen4/dec/rwing.stl")
SPOILER = _pts("/home/user/media/mazda-3-gen4/dec/spoiler_reg.stl", 10)
PTS = {"car": fc.c,
       "wing": np.vstack([fc.c, WING + [0, 0.14, 0.46]]),
       "stack": np.vstack([fc.c, WING + [0, 0.17, 0.56], SPOILER + [0, 0.32, 1.12]])}


def fit(key, pts, target=FIT):
    """Slide the camera along its view line so the points span `target` of the frame."""
    L, T = np.array(key["loc"], float), np.array(key["target"], float)
    lo, hi = 0.2, 6.0
    for _ in range(40):
        m = (lo + hi) / 2
        if fc.extent(pts, T + (L - T) * m, T, key["focal"]) > target: lo = m
        else: hi = m
    key = dict(key); key["loc"] = list(T + (L - T) * hi); return key


def orbit(t, ang_deg, h, c=(0, 0, 0.7), focal=35, ease="lin", tz=None, r=6.0):
    """angle 0 = camera in front of the car (-Y); +90 = car's left (+X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, a0, a1, h0, h1, c=(0, 0, 0.7), focal=35, n=8, tz=None, shape="inout", pts="car", fit_to=FIT, push=1.0):
    """Orbit keyed every secs/n (linear between keys follows the circle); each key fitted; `push` <1 ends slightly tighter."""
    keys = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if shape == "inout" else (1 - (1 - u) ** 2 if shape == "out2" else u)
        keys.append(fit(orbit(secs * u, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c, focal, "lin", tz),
                        PTS[pts], fit_to * (1 + (1 / push - 1) * e)))
    return keys


S = SECS
SHOTS = {
    # 1. hook: front-left 3/4 turntable, whole car, moving from frame 1
    "s1_front34": {"base": [CAR], "cam": arc(S["s1_front34"], 24, 52, 1.35, 1.45, tz=0.68, shape="lin")},
    # 2. rear-left 3/4 orbit forward + rise
    "s2_rear34": {"base": [CAR], "cam": arc(S["s2_rear34"], 158, 132, 1.1, 1.7, tz=0.7)},
    # 3. low front-RIGHT 3/4 (other side from s1), slow swing toward the nose: whole car; head-on put the holey grille mesh centre-frame
    "s3_front": {"base": [CAR], "cam": arc(S["s3_front"], -42, -26, 0.7, 0.8, tz=0.62, focal=40, push=0.95)},
    # 4. left side profile, slightly high, slow drift: the door reflections over the whole flank
    "s4_side": {"base": [CAR], "cam": arc(S["s4_side"], 98, 84, 1.25, 1.35, tz=0.7, focal=40)},
    # 5. rear, low and nearly head-on, slight swing: tail lamps + hatch, whole car
    "s5_rear": {"base": [CAR], "cam": arc(S["s5_rear"], 192, 172, 0.85, 0.95, tz=0.72, focal=40, push=0.94)},
    # 6. panel off: high rear 3/4, the rear wing lifts off the hatch onto its mounts (Wing Removed state), whole car
    "s6_wing": {"base": [f"{P}/comp_wingoff.blend"],
                "parts": [{"blend": f"{P}/rwing.blend",
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 2 * BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},  # shot starts b28: lift b30 -> b34
                                    {"t": 6 * BEAT, "loc": [0, 0.12, 0.42], "rot": [-10, 0, 0], "ease": "inout"},
                                    {"t": S["s6_wing"], "loc": [0, 0.14, 0.46], "rot": [-11, 0, 0], "ease": "lin"}]}],
                "cam": arc(S["s6_wing"], 140, 150, 2.9, 3.2, c=(0, 0.2, 0.8), tz=0.85, pts="wing", shape="out2")},
}
# 7. top-down: rear-right high 3/4 up and over to straight down, whole car throughout
def _top(n=12):
    A, B = np.array([-2.6, 3.9, 3.6]), np.array([0.0, 0.2, 6.0]); TA, TB = np.array([0, 0.3, 0.7]), np.array([0, 0.0, 0.7])
    keys = []
    for k in range(n + 1):
        u = k / n; e = u * u * (3 - 2 * u)
        d = (A - TA) * (1 - e) + (B - TB) * e; d = d / np.linalg.norm(d) * 6.0  # direction slerp-ish, fixed length before fit
        T = TA * (1 - e) + TB * e
        keys.append(fit({"t": S["s7_top"] * u, "loc": list(T + d), "target": list(T), "focal": 35, "ease": "lin"}, PTS["car"]))
    return keys
SHOTS["s7_top"] = {"base": [CAR], "cam": _top()}

# 8. exploded view: wing rises off the hatch, the (unregistered) aero-kit spoiler floats down into the layer above it,
# camera orbits behind the car left -> right with the WHOLE car + stack in frame; wing seats (lock) while the spoiler lifts away.
# shot starts on b42 (22.954 s): separate on b44 -> b48, drift, return from b56, LOCK on b60 (32.770), hold to b64 (logo)
T8 = S["s8_explode"]
SEP0, SEP1, BACK0, LOCK = 2 * BEAT, 6 * BEAT, 14 * BEAT, 18 * BEAT
SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_wingoff.blend"],
    "parts": [
        {"blend": f"{P}/rwing.blend", "keys": [
            {"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": SEP0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": SEP1, "loc": [0, 0.15, 0.5], "rot": [-12, 0, 0], "ease": "out"},
            {"t": BACK0, "loc": [0, 0.17, 0.56], "rot": [-14, 0, 0], "ease": "lin"},
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]},
        {"blend": f"{P}/spoiler.blend", "keys": [
            {"t": 0, "loc": [0, 0.3, 2.6], "rot": [0, 0, 0]}, {"t": SEP0 + BEAT, "loc": [0, 0.3, 2.6], "rot": [0, 0, 0]},
            {"t": SEP1 + 2 * BEAT, "loc": [0, 0.3, 1.05], "rot": [0, 0, 0], "ease": "out"},
            {"t": BACK0, "loc": [0, 0.32, 1.12], "rot": [0, 0, 0], "ease": "lin"},
            {"t": LOCK + BEAT, "loc": [0, 0.4, 2.8], "rot": [0, 0, 0], "ease": "in2"}]},
    ],
    "cam": arc(T8, 120, 228, 2.7, 3.0, c=(0, 0.3, 1.0), focal=35, n=12, tz=1.1, pts="stack")}


def spec(name, mode):
    s = SHOTS[name]; final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name], "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final2' if final else 'preview2'}/{name}"}
    if not final:
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}2.json"; json.dump(sp, open(p, "w"), indent=1); return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
