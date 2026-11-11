"""Shot specs for the Ferrari 296 Temerario-style reel -> JSON for tools/shot.py.

    python projects/ferrari-296/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Timing: ferrari296_track.mp3 accent grid (103.4 BPM, beat 0.5803 s); cuts listed in project.yaml. Scan frame (normalised, metres):
front = -Y, car's right = -X, ground Z=0; length 4.56 m, width 2.22 m incl. mirrors.
"""
import json
import math
import os
import sys

P = "/home/user/media/ferrari-296/prep"
OUT = "/home/user/media/work/f296/renders"
SPECS = "/home/user/media/work/f296/specs"
BAR = 2.4  # (old 100 BPM plan; kept for s1 which was already rendered on it)
BEAT = 0.5803  # ferrari296_track.mp3: 103.4 BPM, see editlog
SECS = {"s1_turntable": 4.8, "s2_rear": 140 / 30, "s3_wheel": 69 / 30, "s4_nose": 70 / 30, "s5_hood": 122 / 30,
        "s6_engine": 69 / 30, "s7_top": 70 / 30, "s8_explode": 348 / 30}

CAR = f"{P}/car4.blend"        # 4 mm: full-car moves
CAR_HI = f"{P}/car3.blend"     # 3 mm: close-ups


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=35, ease="inout", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


# angle 0 = camera in front of the car (-Y); +90 = car's left (+X); -90 = car's right (-X); 180 = behind
SHOTS = {
    # 1. slow 3/4 front turntable, low, starts moving on frame 1 (hook)
    "s1_turntable": { "base": [CAR], "cam": [orbit(0, 5.3, -32, 1.0, focal=30, ease="lin"),
                                                      orbit(2 * BAR, 5.1, -62, 1.1, focal=30, ease="out2")]},
    # 2. rear 3/4 orbit, other side, slight rise
    "s2_rear": { "base": [CAR], "cam": [orbit(0, 5.2, 148, 0.85, focal=30, ease="lin"),
                                                 orbit(SECS["s2_rear"], 5.0, 120, 1.3, focal=30, ease="out2")]},
    # 3. extreme close-up: front right wheel / brake through the spokes, slow slide forward
    "s3_wheel": { "base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-2.25, -0.95, 0.42], "target": [-0.95, -1.42, 0.36], "focal": 40},
        {"t": SECS["s3_wheel"], "loc": [-2.15, -1.75, 0.40], "target": [-0.95, -1.47, 0.36], "focal": 40, "ease": "inout"}]},
    # 4. detail: front lamp + intake, slide across the nose (tail lamps are scan holes - not used)
    "s4_nose": { "base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.75, -3.35, 0.9], "target": [-0.6, -2.0, 0.62], "focal": 38},
        {"t": SECS["s4_nose"], "loc": [-0.55, -3.7, 0.8], "target": [-0.45, -2.1, 0.58], "focal": 38, "ease": "inout"}]},
    # 5. hood opens on its rear hinge (frunk from "Front Fully Removed"), camera eases in
    "s5_hood": { "base": [f"{P}/comp_hood.blend"],
                "parts": [{"blend": f"{P}/hood_combined.blend", "pivot": [0, -0.86, 0.88],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 4 * BEAT, "loc": [0, 0, 0], "rot": [-58, 0, 0], "ease": "inout"}]}],
                "cam": [orbit(0, 4.3, -30, 2.2, c=(0, -1.0, 0.5), focal=30, ease="lin"),
                        orbit(SECS["s5_hood"], 3.7, -16, 2.5, c=(0, -1.2, 0.5), focal=30, ease="out2")]},
    # 6. engine cover opens (louvred lid, "Engine Bay" scan under it), high rear 3/4
    "s6_engine": { "base": [f"{P}/comp_engine.blend"],
                  "parts": [{"blend": f"{P}/enginer_cover.blend", "pivot": [0, 1.63, 0.9],
                             "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                      {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                      {"t": 3 * BEAT, "loc": [0, 0, 0], "rot": [85, 0, 0], "ease": "inout"}]}],
                  "cam": [{"t": 0, "loc": [1.35, 3.6, 2.55], "target": [0, 1.7, 0.8], "focal": 30},
                          {"t": SECS["s6_engine"], "loc": [0.75, 3.35, 2.75], "target": [0, 1.75, 0.8], "focal": 30, "ease": "out2"}]},
    # 7. top-down: from a high rear 3/4 up and over to straight down (front at the top of frame)
    "s7_top": { "base": [CAR], "cam": [
        {"t": 0, "loc": [2.2, 4.6, 4.0], "target": [0, 0.3, 0.5], "focal": 30},
        {"t": SECS["s7_top"], "loc": [0.0, 0.25, 6.9], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}

# 8. exploded view: panels separate on the 23.066 s lift (loudest accent), drift while the camera orbits
# front-right -> rear-right, fly home and LOCK on the 32.350 s accent (heaviest bass), hold 4 beats -> logo
SEP, HOLD, BACK, LOCK = 0.0, 4 * BEAT, 13 * BEAT, 16 * BEAT


def explode(off, rot=(0, 0, 0), delay=0.0):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": HOLD, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": BACK, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},  # slow drift outward
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_explode.blend"],
    "parts": [
        {"blend": f"{P}/x_hood.blend", "keys": explode((0, -0.25, 0.95), (-12, 0, 0))},
        {"blend": f"{P}/x_fbumper.blend", "keys": explode((0, -1.0, -0.05))},
        {"blend": f"{P}/x_fender.blend", "keys": explode((-0.75, 0, 0.18), (0, -8, 0), 0.05)},
        {"blend": f"{P}/x_skirt.blend", "keys": explode((-0.65, 0, -0.18), delay=0.05)},
        {"blend": f"{P}/x_ecover.blend", "keys": explode((0, 0.15, 0.85), (20, 0, 0), 0.1)},
        {"blend": f"{P}/x_rbumper.blend", "keys": explode((0, 0.95, 0.05))},
        {"blend": f"{P}/x_diffuser.blend", "keys": explode((0, 0.75, -0.35), delay=0.1)},
    ],
    # radius swells side-on (exploded length ~6.6 m spans the 9:16 width there); keyed every 1/12 of the move: linear loc interpolation between far-apart keys would cut a chord toward the car
    "cam": [orbit(SECS["s8_explode"] * k / 12, 7.5 + 1.8 * math.sin(math.pi * k / 12), -50 - 75 * (k / 12), 3.0 - 0.3 * (k / 12),
                  c=(0.1, -0.6 + 1.0 * (k / 12), 0.5), focal=28, ease="lin", tz=0.4) for k in range(13)]}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + (0 if name == "s1_turntable" else 1 / 15), "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
