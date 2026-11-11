"""Shot specs for the Toyota Sera Temerario-style reel -> JSON for tools/shot.py.

    python projects/toyota-sera/tools/shots.py preview|final [shot ...]   # writes specs, prints their paths

Scan frame (prepped, metres): nose = -Y, car's right = -X, ground z = 0; 3.84 x 1.72 x 1.24 m. Front axle ~y -1.15.
Timing: toyota-sera_track.mp3, 100.0 BPM; cuts in project.yaml. Shots render a little longer than they play.
Camera moves use linear / ease-out segments so any sub-window still moves from frame 1.
"""
import json
import math
import os
import sys

P = "/home/user/media/toyota-sera/prep"
C = "/home/user/media/toyota-sera/clean"
OUT = "/home/user/media/work/sera/renders"
SPECS = "/home/user/media/work/sera/specs"
BEAT = 0.59999  # toyota-sera_track.mp3 kick grid: 0.0355 + 0.59999 n (100.0 BPM), tools/accents.py
EXPOSURE = -0.35  # measured: 0 EV clipped 9 % of car pixels in a front 3/4 (p90 249); Temerario ref p90 ~231

CAR = f"{P}/car4.blend"      # 4 mm: full-car moves
CAR_HI = f"{P}/car3.blend"   # 3 mm: close-ups
SECS = {"s1_turntable": 6.0, "s2_rear": 5.0, "s3_wheel": 3.0, "s4_nose": 3.0, "s5_hood": 3.4, "s6_doors": 4.6,
        "s7_top": 2.8, "s8_explode": 11.0}


def hinge(name):
    return json.load(open(f"{C}/{name}_hinge.json"))


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(t0, t1, r0, r1, a0, a1, h0, h1, c=(0, 0, 0.55), focal=30, n=8, ease_last="out2", tz=None):
    """Orbit keyed every 1/n of the move (linear loc between far-apart keys would cut a chord toward the car)."""
    ks = []
    for k in range(n + 1):
        u = k / n
        if ease_last == "out2":
            w = 1 - (1 - u) ** 2
        elif ease_last == "inout":
            w = u * u * (3 - 2 * u)
        else:
            w = u
        ks.append(orbit(t0 + (t1 - t0) * u, r0 + (r1 - r0) * w, a0 + (a1 - a0) * w, h0 + (h1 - h0) * w, c, focal,
                        "lin", tz))
    return ks


def swing(name, t0, t1, frac=1.0, hold_from=0.0):
    h = hinge(name)
    return {"blend": f"{P}/{name}_panel.blend", "pivot": h["pivot"], "axis": h["axis"],
            "keys": [{"t": 0, "loc": [0, 0, 0], "ang": 0}, {"t": t0, "loc": [0, 0, 0], "ang": 0},
                     {"t": t1, "loc": [0, 0, 0], "ang": h["open_deg"] * frac, "ease": "inout"}]}


S = SECS
SHOTS = {
    # 1. slow low front 3/4 turntable (car's right), moving from frame 1 - the hook
    "s1_turntable": {"base": [CAR], "cam": arc(0, S["s1_turntable"], 3.9, 3.7, -28, -62, 0.95, 1.05, focal=30, ease_last="lin")},
    # 2. rear 3/4 orbit on the other side, slight rise
    "s2_rear": {"base": [CAR], "cam": arc(0, S["s2_rear"], 3.8, 3.6, 150, 122, 0.85, 1.25, focal=30, ease_last="lin")},
    # 3. extreme close-up: front-right wheel + arch, slide toward the nose
    "s3_wheel": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.95, -0.45, 0.42], "target": [-0.80, -1.10, 0.32], "focal": 40},
        {"t": S["s3_wheel"], "loc": [-1.90, -1.75, 0.40], "target": [-0.80, -1.20, 0.32], "focal": 40, "ease": "lin"}]},
    # 4. detail: slide across the nose - headlamp, grille slot, bumper vents (the tail panel read flat: blank plate)
    "s4_nose": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.15, -2.95, 0.80], "target": [-0.45, -1.85, 0.62], "focal": 38},
        {"t": S["s4_nose"], "loc": [0.55, -3.10, 0.74], "target": [0.25, -1.85, 0.60], "focal": 38, "ease": "lin"}]},
    # 5. hood opens on its fitted hinge (engine bay from 'Hood open'), camera drifts in and up
    "s5_hood": {"base": [f"{P}/hood_base.blend"], "parts": [swing("hood", BEAT, 4 * BEAT)],
                "cam": arc(0, S["s5_hood"], 3.6, 3.2, -34, -16, 1.9, 2.25, c=(0, -0.95, 0.55), focal=30, ease_last="lin")},
    # 6. both butterfly doors swing up on their fitted hinges (interior from 'Door Open'); front-right 3/4
    "s6_doors": {"base": [f"{P}/doors_base.blend"], "parts": [swing("door", BEAT, 5 * BEAT), swing("door2", BEAT, 5 * BEAT)],
                 "cam": arc(0, S["s6_doors"], 4.5, 4.1, -62, -38, 1.25, 1.6, c=(0, -0.1, 0.7), focal=30, ease_last="lin")},
    # 7. top-down: high rear 3/4 up and over to straight down (front at the top of frame)
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [1.6, 3.2, 2.9], "target": [0, 0.3, 0.5], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, 0.18, 5.0], "target": [0, 0.0, 0.5], "focal": 30, "ease": "out2"}]},
}

# 8. exploded view on the music: the shot starts ON the 24.035 s phrase downbeat and the panels separate right there,
# ease out over 3 beats, drift through the kick break (25.2-27.6 s), fly home from beat 12 and LOCK on the 33.635 s
# phrase downbeat (beat 16), hold 2 beats -> logo.
EXPLODE = {"SEP": 0.0, "HOLD": 3 * BEAT, "BACK": 12 * BEAT, "LOCK": 16 * BEAT}
OFFSETS = {  # panels stack in layers ABOVE the car (Temerario 25-31 s; portrait-friendly, never at the lens); doors also swing open as they lift
    "hood": ((0, 0.05, 1.35), None),
    "front_bumper_3mm": ((0, -0.35, 0.75), None),
    "rear_bumper_only_3mm": ((0, 0.35, 0.85), None),
    "door": ((-0.45, 0.05, 0.65), 0.35),
    "door2": ((0.45, 0.05, 0.65), 0.35),
}


def explode_keys(off, delay, E):
    return [{"t": 0, "loc": [0, 0, 0]}, {"t": E["SEP"] + delay, "loc": [0, 0, 0]},
            {"t": E["HOLD"], "loc": list(off), "ease": "out"},
            {"t": E["BACK"], "loc": [o * 1.06 for o in off], "ease": "lin"},
            {"t": E["LOCK"], "loc": [0, 0, 0], "ease": "in"}]


def explode_shot(E=EXPLODE, secs=S["s8_explode"]):
    parts = []
    for i, (n, (off, swing_frac)) in enumerate(OFFSETS.items()):
        blend = f"{P}/{n}.blend" if n.endswith("mm") else f"{P}/{n}_panel.blend"
        keys = explode_keys(off, 0.05 * (i % 3), E)
        p = {"blend": blend, "keys": keys}
        if swing_frac:
            h = hinge(n); p.update(pivot=h["pivot"], axis=h["axis"])
            a = h["open_deg"] * swing_frac
            for k, ang in zip(keys, [0, 0, a, a, 0]):
                k["ang"] = ang
        else:
            for k in keys:
                k["rot"] = [0, 0, 0]
        parts.append(p)
    n = 12  # orbit front-right -> right side -> rear-right, radius swells side-on
    cam = [orbit(secs * k / n, 5.2 + 1.7 * math.sin(math.pi * k / n), -35 - 110 * (k / n), 3.2 - 0.4 * (k / n),
                 c=(0, -0.2 + 0.4 * (k / n), 0.95), focal=28, ease="lin", tz=0.95) for k in range(n + 1)]
    return {"base": [f"{P}/explode_base.blend"], "parts": parts, "cam": cam}


SHOTS["s8_explode"] = explode_shot()


def spec(name, mode, frames=None):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name], "fps": 15, "res": "1080x1920", "res_pct": 75 if final else 30,
          "samples": 12 if final else 6, "exposure": EXPOSURE,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if frames:
        sp["frames"] = frames
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode, ["first", "mid", "last"] if mode == "preview" else None))
