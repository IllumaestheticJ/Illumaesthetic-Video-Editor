"""Shot specs for the Infiniti G35 coupe Temerario-style reel -> JSON for tools/shot.py (copied from ferrari-296).

    python projects/infiniti-g35/tools/shots.py preview|final [shot ...]

Prepped frame (metres): nose -Y, +X = car's left, car floats z 0.17..1.57 (tyre bottoms ~0.17), length 4.63 m.
Orbit angle 0 = camera in front of the nose, -90 = car's right (-X), +90 = car's left, 180 = behind.
SECS / BEAT are set from the music (see project.yaml); shots are rendered 1 frame long and trimmed by `dur`.
"""
import json, math, os, sys

P = "/home/user/media/infiniti-g35/prep"
OUT = "/home/user/media/work/g35/renders"
SPECS = "/home/user/media/work/g35/specs"
BEAT = float(os.environ.get("G35_BEAT", 0.6))
SECS = json.loads(os.environ.get("G35_SECS", "{}")) or {
    "s1_turntable": 5.0, "s2_rear": 4.6, "s3_wheel": 2.6, "s4_lamp": 2.6, "s5_tail": 2.6,
    "s6_trunk": 4.2, "s7_top": 3.2, "s8_explode": 11.0}
CAR, CAR_HI = f"{P}/car4.blend", f"{P}/car25.blend"
CZ = 0.80  # visual centre height


def orbit(t, r, ang, h, c=(0, 0, CZ), focal=30, ease="inout", tz=None):
    a = math.radians(ang)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def shots():
    S = SECS
    d = {
        # 1. slow low front 3/4 turntable (car's right), moving from frame 1
        "s1_turntable": {"base": [CAR], "cam": [orbit(0, 6.4, -24, 1.0, focal=30, ease="lin"),
                                                 orbit(S["s1_turntable"], 6.9, -46, 1.15, focal=30, ease="out2")]},
        # 2. rear 3/4 orbit, car's left, slight rise
        "s2_rear": {"base": [CAR], "cam": [orbit(0, 6.5, 160, 0.95, focal=30, ease="lin"),
                                            orbit(S["s2_rear"], 7.0, 136, 1.45, focal=30, ease="out2")]},
        # 3. extreme close-up: front right wheel (mesh rim) slide forward
        "s3_wheel": {"base": [CAR_HI], "cam": [
            {"t": 0, "loc": [-2.15, -0.85, 0.62], "target": [-0.9, -1.42, 0.58], "focal": 40},
            {"t": S["s3_wheel"], "loc": [-2.10, -1.85, 0.60], "target": [-0.9, -1.52, 0.58], "focal": 40}]},
        # 4. close-up: right headlight / front fascia slide across the nose
        "s4_lamp": {"base": [CAR_HI], "cam": [
            {"t": 0, "loc": [-1.95, -3.05, 1.25], "target": [-0.62, -1.95, 0.98], "focal": 42},
            {"t": S["s4_lamp"], "loc": [-0.95, -3.55, 1.20], "target": [-0.52, -2.05, 0.98], "focal": 42}]},
        # 5. close-up: left tail lamp + spoiler, rising slide
        "s5_tail": {"base": [CAR_HI], "cam": [
            {"t": 0, "loc": [1.95, 3.30, 1.35], "target": [0.55, 2.0, 1.15], "focal": 42},
            {"t": S["s5_tail"], "loc": [0.95, 3.75, 1.75], "target": [0.40, 2.05, 1.20], "focal": 42}]},
        # 6. trunk lid (part scan) + spoiler hinge open on the lid's front edge
        "s6_trunk": {"base": [f"{P}/base_trunk.blend"],
                     "parts": [{"blend": b, "pivot": [0, 1.56, 1.23],
                                "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                         {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                         {"t": 4 * BEAT, "loc": [0, 0, 0], "rot": [62, 0, 0]}]}
                               for b in (f"{P}/trunk.blend", f"{P}/x_spoiler.blend")],
                     "cam": [orbit(0, 3.6, 148, 2.4, c=(0, 1.4, 0.9), focal=30, ease="lin"),
                             orbit(S["s6_trunk"], 3.3, 162, 2.75, c=(0, 1.5, 0.9), focal=30, ease="out2")]},
        # 7. top-down: high front-left 3/4 up and over to straight down (nose at the bottom of frame)
        "s7_top": {"base": [CAR], "cam": [
            {"t": 0, "loc": [2.4, -4.6, 4.0], "target": [0, -0.3, 0.7], "focal": 30},
            {"t": S["s7_top"], "loc": [0.0, -0.25, 7.0], "target": [0, 0.0, 0.7], "focal": 30}]},
    }
    # 8. exploded view: panels lift into layers above/around the car, drift, return and lock
    E = S["s8_explode"]
    SEP, HOLD, LOCK = 0.0, 4 * BEAT, E - 2 * BEAT  # separate on the climax kick, out by 4 beats, lock 2 beats before the cut
    BACK = LOCK - 3 * BEAT

    def ex(off, rot=(0, 0, 0), delay=0.0):
        return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": HOLD + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
                {"t": BACK, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},
                {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]
    # portrait-friendly stacking (Temerario 25-31 s): panels rise into layers ABOVE the car, small lateral spread
    parts = [("x_hood", (0, -0.15, 1.05), (-12, 0, 0), 0.0), ("x_fbumper", (0, -0.45, 0.55), (0, 0, 0), 0.0),
             ("trunk", (0, 0.25, 1.05), (14, 0, 0), 0.08), ("x_spoiler", (0, 0.30, 1.65), (14, 0, 0), 0.08),
             ("x_rbumper", (0, 0.45, 0.55), (0, 0, 0), 0.04), ("x_door_r", (-0.45, 0, 0.75), (0, -8, 0), 0.12),
             ("x_door_l", (0.45, 0, 0.75), (0, 8, 0), 0.12)]
    d["s8_explode"] = {"base": [f"{P}/base.blend"],
                       "parts": [{"blend": f"{P}/{n}.blend", "keys": ex(o, r, dl)} for n, o, r, dl in parts],
                       "cam": [orbit(E * k / 12, 6.4 + 1.6 * math.sin(math.pi * k / 12), -38 - 84 * (k / 12),
                                     2.2 + 0.4 * math.sin(math.pi * k / 12), c=(0, -0.3 + 0.6 * (k / 12), 1.2), focal=28,
                                     ease="lin", tz=1.25) for k in range(13)]}
    return d


def spec(name, mode, frames=None):
    s = shots()[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 2 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if not final:
        sp["frames"] = frames or ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SECS):
        print(spec(n, mode))
