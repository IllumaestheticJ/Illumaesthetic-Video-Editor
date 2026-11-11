"""Shot specs for the Mazda 3 (gen 4) Temerario-style scan reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/mazda-3-gen4/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (prepped car4.json, metres): nose = -Y, car's LEFT = +X (clean side; the right rear quarter has scan ribbing),
body sits z 0.08..1.53 (car scanned raised ~15 cm on jacks; we float it on black). Length 4.46 m, width 1.93 m incl. mirrors.
SECS are render lengths: planned durations + margin, trimmed to the music in project.yaml.
"""
import json, math, os, sys

P = "/home/user/media/mazda-3-gen4/prep"
OUT = "/home/user/media/work/m3/renders"
SPECS = "/home/user/media/work/m3/specs"
CAR = f"{P}/car4.blend"
SECS = {"s1_front34": 5.6, "s2_rear34": 5.0, "s3_lamp": 3.0, "s4_flank": 3.6, "s5_tail": 3.0,
        "s6_wing": 4.6, "s7_top": 3.6, "s8_explode": 12.4}
BEAT = 0.5453  # mazda-3-gen4_track.mp3: 110.0 BPM, grid fitted on kick peaks (tools/music_grid.py)


def orbit(t, r, ang_deg, h, c=(0, 0, 0.7), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); +90 = car's left (+X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, r0, r1, a0, a1, h0, h1, c=(0, 0, 0.7), focal=30, n=8, tz=None, shape="out2"):
    """Orbit keyed every secs/n so linear interpolation between keys follows the circle, eased overall."""
    keys = []
    for k in range(n + 1):
        u = k / n
        e = 1 - (1 - u) ** 2 if shape == "out2" else (u * u * (3 - 2 * u) if shape == "inout" else u)
        keys.append(orbit(secs * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c, focal, "lin", tz))
    return keys


S = SECS
SHOTS = {
    # 1. hook: low front-left 3/4 turntable, moving from frame 1
    "s1_front34": {"base": [CAR], "cam": arc(S["s1_front34"], 4.8, 4.5, 22, 48, 0.95, 1.05, focal=30, tz=0.62, shape="lin")},
    # 2. rear-left 3/4, slow orbit forward + rise
    "s2_rear34": {"base": [CAR], "cam": arc(S["s2_rear34"], 4.6, 4.4, 158, 132, 0.85, 1.35, focal=30, tz=0.65)},
    # 3. extreme close-up: left headlamp from the side, slide forward (grille mesh is holey - kept out of frame) (2 mm front block)
    "s3_lamp": {"base": [f"{P}/c2_front.blend"], "cam": [
        {"t": 0, "loc": [1.55, -3.35, 0.98], "target": [0.64, -2.02, 0.8], "focal": 70},
        {"t": S["s3_lamp"], "loc": [1.95, -2.95, 0.93], "target": [0.66, -2.0, 0.79], "focal": 70, "ease": "inout"}]},
    # 4. Kodo surfacing: glide forward along the left flank from behind the rear wheel, reflections sliding over the doors (2 mm left block)
    "s4_flank": {"base": [f"{P}/c2_left.blend"], "cam": [
        {"t": 0, "loc": [1.75, 2.55, 1.05], "target": [0.35, -0.5, 0.55], "focal": 30},
        {"t": S["s4_flank"], "loc": [1.85, 1.5, 0.95], "target": [0.35, -1.45, 0.55], "focal": 30, "ease": "inout"}]},
    # 5. close-up: left tail lamp + hatch shoulder (2 mm rear block)
    "s5_tail": {"base": [f"{P}/c2_rear.blend"], "cam": [
        {"t": 0, "loc": [1.65, 3.05, 1.12], "target": [0.55, 2.05, 0.95], "focal": 40},
        {"t": S["s5_tail"], "loc": [0.85, 3.45, 1.05], "target": [0.4, 2.1, 0.95], "focal": 40, "ease": "inout"}]},
    # 6. panel off: the rear wing lifts off the hatch and reveals its mounts (Wing Removed state scan)
    "s6_wing": {"base": [f"{P}/comp_wingoff.blend"],
                "parts": [{"blend": f"{P}/rwing.blend",
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 2 * BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},  # shot starts b28 (15.319): lift b30 -> b34
                                    {"t": 6 * BEAT, "loc": [0, 0.12, 0.42], "rot": [-10, 0, 0], "ease": "inout"},
                                    {"t": S["s6_wing"], "loc": [0, 0.14, 0.46], "rot": [-11, 0, 0], "ease": "lin"}]}],
                "cam": [{"t": 0, "loc": [1.9, 3.75, 2.25], "target": [0, 1.55, 1.25], "focal": 32},
                        {"t": S["s6_wing"], "loc": [1.25, 3.45, 2.55], "target": [0, 1.5, 1.3], "focal": 32, "ease": "out2"}]},
    # 7. top-down: from a high rear-right 3/4 up and over to straight down (nose at the top of frame)
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [-2.6, 3.9, 3.6], "target": [0, 0.3, 0.7], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, 0.2, 5.5], "target": [0, 0.0, 0.7], "focal": 30, "ease": "inout"}]},
}

# 8. exploded view: wing rises off the hatch, the (unregistered) aero-kit spoiler floats down into the layer above it,
# camera orbits behind the car left -> right; wing seats again (lock) while the aero spoiler lifts away.
T8 = S["s8_explode"]
# shot starts on b42 (22.954 s): separate on b44 (+2 beats) -> b48, drift, return from b56, LOCK on b60 (32.770), hold to b64 (logo)
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
    "cam": arc(T8, 3.9, 4.3, 120, 228, 2.5, 2.8, c=(0, 1.1, 1.2), focal=28, n=12, tz=1.55, shape="inout")}


def spec(name, mode):
    s = SHOTS[name]; final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name], "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if not final:
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"; json.dump(sp, open(p, "w"), indent=1); return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
