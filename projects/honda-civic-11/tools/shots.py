"""Shot specs for the Civic FE1 Temerario-style reel -> JSON for projects/ferrari-296/tools/shot.py (shared renderer).

    python projects/honda-civic-11/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Prepped frame (metres): front = +Y, car's LEFT = -X, floor z = 0, length 4.82 m. Left side is the hero side (the
right-rear wheel is only a tyre ring in the scan). Durations come from SECS (set from the music's accent grid).
"""
import json
import math
import os
import sys

P = "/home/user/media/honda-civic-11/prep"
OUT = "/home/user/media/work/civic/renders"
SPECS = "/home/user/media/work/civic/specs"
HINGE = json.load(open("/home/user/media/honda-civic-11/trunk/hinge2.json"))
BEAT = float(os.environ.get("CIVIC_BEAT", 0.6))
# shot lengths in beats (whole-frame seconds at 30 fps are applied in project.yaml; renders get a small tail)
BEATS = {"s1_front34": 8, "s2_rear34": 7, "s3_wheel": 4, "s4_lamp": 4, "s5_trunk": 7, "s6_top": 6, "s7_explode": 16}
SECS = {k: v * BEAT + 0.2 for k, v in BEATS.items()}   # +0.2 s tail so trims never run out of frames

CAR = f"{P}/car4f.blend"


def orbit(t, r, ang_deg, h, c=(0, 0, 0.6), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (+Y), +90 = car's LEFT (-X), 180 = behind, -90 = car's right."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] - r * math.sin(a), c[1] + r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


LID = {"blend": f"{P}/lid.blend", "pivot": HINGE["pivot_prepped"]}
CLOSED = {"loc": HINGE["blender_closed_loc"], "rot": HINGE["blender_closed_euler_deg"]}
OPEN = {"loc": [0, 0, 0], "rot": [0, 0, 0]}

SHOTS = {
    # 1. slow low front-3/4 turntable on the left side; moving from frame 1 (hook)
    "s1_front34": {"base": [CAR], "cam": [orbit(0, 5.6, 22, 0.85, c=(0, 0.45, 0.6), focal=30, ease="lin"),
                                          orbit(SECS["s1_front34"], 5.1, 46, 1.0, c=(0, 0.1, 0.6), focal=30, ease="out2")]},
    # 2. rear-3/4 orbit, left side, slight rise
    "s2_rear34": {"base": [CAR], "cam": [orbit(0, 5.5, 150, 0.8, c=(0, -0.6, 0.6), focal=30, ease="lin"),
                                         orbit(SECS["s2_rear34"], 4.8, 124, 1.25, focal=30, ease="out2")]},
    # 3. extreme close-up: front-left wheel, brake through the spokes, slow slide rearward along the flank
    "s3_wheel": {"base": [f"{P}/fl2.blend"], "cam": [
        {"t": 0, "loc": [-2.05, 2.15, 0.40], "target": [-0.82, 1.42, 0.34], "focal": 40},
        {"t": SECS["s3_wheel"], "loc": [-2.10, 0.95, 0.42], "target": [-0.82, 1.36, 0.34], "focal": 40, "ease": "inout"}]},
    # 4. detail: front-left headlight + grille corner, slide across the nose
    "s4_lamp": {"base": [f"{P}/fl2.blend"], "cam": [
        {"t": 0, "loc": [-1.80, 3.20, 0.95], "target": [-0.65, 2.15, 0.72], "focal": 45},
        {"t": SECS["s4_lamp"], "loc": [-1.20, 3.55, 0.84], "target": [-0.66, 2.20, 0.70], "focal": 45, "ease": "inout"}]},
    # 5. trunk opens on its fitted hinge (Trunk Open state scan underneath), high rear-left 3/4, camera eases in
    "s5_trunk": {"base": [f"{P}/trunk_base.blend"],
                 "parts": [dict(LID, keys=[dict(t=0, **CLOSED), dict(t=BEAT, **CLOSED),
                                           dict(t=4.5 * BEAT, ease="inout", **OPEN)])],
                 "cam": [orbit(0, 4.6, 152, 2.4, c=(0, -1.3, 0.75), focal=30, ease="lin"),
                         orbit(SECS["s5_trunk"], 4.0, 162, 2.7, c=(0, -1.5, 0.8), focal=30, ease="out2")]},
    # 6. top-down: from a high rear-left 3/4 up and over to straight down (front at the top of frame)
    "s6_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [-2.6, -4.2, 4.0], "target": [0, -0.3, 0.5], "focal": 30},
        {"t": SECS["s6_top"], "loc": [-0.02, -0.25, 6.9], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}

# 7. exploded view (right side: the Door Open scan is the right flank). Panels lift UP and slightly out (not at the
# lens), drift, then fly home and lock. SEP/LOCK land on accents once the music is in.
SEP, HOLD, BACK, LOCK = 0.0, 4 * BEAT, 12 * BEAT, 14.5 * BEAT


def explode(off, rot=(0, 0, 0), delay=0.0, home=None):
    home = home or {"loc": [0, 0, 0], "rot": [0, 0, 0]}
    hl, hr = home["loc"], home["rot"]
    return [dict(t=0, loc=hl, rot=hr), dict(t=SEP + delay, loc=hl, rot=hr),
            {"t": HOLD + delay, "loc": [a + b for a, b in zip(hl, off)], "rot": [a + b for a, b in zip(hr, rot)], "ease": "out"},
            {"t": BACK, "loc": [a + 1.06 * b for a, b in zip(hl, off)], "rot": [a + b for a, b in zip(hr, rot)], "ease": "lin"},
            {"t": LOCK, "loc": hl, "rot": hr, "ease": "in"}]


SHOTS["s7_explode"] = {
    "base": [f"{P}/explode_base.blend"],
    "parts": [{"blend": f"{P}/front_door.blend", "keys": explode((0.75, 0.20, 0.30), (0, 0, -5))},
              {"blend": f"{P}/rear_door.blend", "keys": explode((0.75, -0.20, 0.30), (0, 0, 5), delay=0.5 * BEAT)},
              dict(LID, keys=explode((0, 0.10, 0.75), (-12, 0, 0), delay=BEAT, home=CLOSED))],
    # high rear-right, looking down ~55 deg: nose at the top of the 9:16 frame, doors slide to frame-right
    "cam": [orbit(0, 3.9, -158, 5.3, c=(0.25, 0.1, 0.5), focal=30, ease="lin"),
            orbit(SECS["s7_explode"], 3.6, -138, 5.5, c=(0.25, 0.2, 0.5), focal=30, ease="out2")]}


def spec(name, mode):
    s = SHOTS[name]
    out = {"base": s["base"], "parts": s.get("parts", []), "camera": {"keys": s["cam"], "sensor": 20.25},
           "seconds": SECS[name], "fps": 15, "res": "1080x1920"}
    if mode == "preview":
        out.update(res_pct=30, samples=8, frames=["first", "mid", "last"], out=f"{OUT}/preview/{name}")
    else:
        out.update(res_pct=75, samples=12, out=f"{OUT}/final/{name}")
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(out, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in (sys.argv[2:] or SHOTS):
        print(spec(n, mode))
