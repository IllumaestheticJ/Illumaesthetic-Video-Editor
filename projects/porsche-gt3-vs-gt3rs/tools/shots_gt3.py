"""GT3 (992) panel of the GT3 vs GT3 RS comparison reel -> JSON for tools/shot.py (1080x960 panel, bottom half).

    python projects/porsche-gt3-vs-gt3rs/tools/shots_gt3.py preview|final [shot ...]

Frame (prepped, metres): front = -Y, car's right = -X. Base comp_gt3 = full car minus hood lid, tail-light bar, right
skirt, rear bumper, diffuser, rear lip, wing, engine-lid spoiler and the FR wheel, with the stripped-state scans filled
in (Front Hood Open, FR wheel well, SideSkirt Removed, Rear End No Diffuser, rear wing mounting reference, Rear End
Trunk Open Lights Out). Parts leave along collision-checked exits (tools/clipcheck.py) and STAY off until g_home.
Music grid: Alkitran from 171.651 s, beat B = 0.47244 s; shot start beats in START.
"""
import json
import os
import sys

G = "/home/user/media/porsche-gt3-992/prep"
OUT = "/home/user/media/work/gt3vs/renders"
SPECS = "/home/user/media/work/gt3vs/specs"
B = 0.47244
BASE = [f"{G}/comp_gt3.blend"]
# order follows the RS panel: whole, front, front wheel (RS fender vent), wing, rear (RS rear + side), side (RS wheel house)
START = {"g_whole": 0, "g_front": 8, "g_wheel": 20, "g_wing": 26, "g_rear": 32, "g_side": 44, "g_wide": 54, "g_home": 62}
BEATS = {"g_whole": 8, "g_front": 12, "g_wheel": 6, "g_wing": 6, "g_rear": 12, "g_side": 10, "g_wide": 8, "g_home": 15}
SECS = {k: round(v * B + 0.2, 3) for k, v in BEATS.items()}
HOOD_PIVOT = [0.0, -0.76, 0.87]
# part -> (first exit leg, final off offset, rot at final); offsets in metres from home
PATH = {
    "hood_lid": (None, (0, 0, 0), (-50, 0, 0)),
    "wheel_fr": ((-0.45, 0, 0), (-0.60, -1.05, 0.05), (0, 0, 0)),
    "sideskirt": ((0, 0, -0.10), (-0.30, 0, -0.28), (0, 0, 0)),
    "rear_wing": ((0, 0.15, 0.26), (0, 0.15, 1.35), (0, 0, 0)),
    "rear_bumper": ((0, 0.30, -0.17), (0, 0.75, 0.70), (0, 0, 0)),
    "rear_diffuser": ((0, 0.20, -0.20), (0, 0.45, -0.40), (0, 0, 0)),
    "rear_lip": ((0, 0.30, -0.08), (0, 1.20, -0.30), (0, 0, 0)),
    "tail_lights": ((0, 0.25, 0.25), (0, 0.45, 1.05), (0, 0, 0)),
    "rear_duckbill": ((0, 0.30, 0.10), (0, 0.15, 1.00), (0, 0, 0)),
}
ORDER = list(PATH)


def part(n, keys):
    d = {"blend": f"{G}/x_{n}.blend", "keys": keys}
    if n == "hood_lid":
        d["pivot"] = HOOD_PIVOT
    return d


def home(n):
    return part(n, [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}])


def off(n):
    _, o, r = PATH[n]
    return part(n, [{"t": 0, "loc": list(o), "rot": list(r)}])


def leave(n, shot, b0, b1):
    """home until reel beat b0, at the final offset by b1 (via the exit leg)."""
    e, o, r = PATH[n]
    t0, t1 = (b0 - START[shot]) * B, (b1 - START[shot]) * B
    keys = [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": t0, "loc": [0, 0, 0], "rot": [0, 0, 0]}]
    if e:
        keys.append({"t": t0 + 0.35 * (t1 - t0), "loc": list(e), "rot": [0, 0, 0], "ease": "inout"})
    keys.append({"t": t1, "loc": list(o), "rot": list(r), "ease": "inout"})
    return part(n, keys)


def back(n, shot, b0, b1):
    """at the final offset until reel beat b0, seated by b1 (via the exit leg)."""
    e, o, r = PATH[n]
    t0, t1 = (b0 - START[shot]) * B, (b1 - START[shot]) * B
    keys = [{"t": 0, "loc": list(o), "rot": list(r)}, {"t": t0, "loc": list(o), "rot": list(r)}]
    if e:
        keys.append({"t": t0 + 0.7 * (t1 - t0), "loc": list(e), "rot": [0, 0, 0], "ease": "inout"})
    keys.append({"t": t1, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"})
    return part(n, keys)


def state(shot, moving):
    """parts list for a shot: `moving` = {name: (b0, b1)}; parts that left in an earlier shot stay off, later ones are home."""
    done = {"g_whole": [], "g_front": [], "g_wheel": ["hood_lid"], "g_wing": ["hood_lid", "wheel_fr"],
            "g_rear": ["hood_lid", "wheel_fr", "rear_wing"],
            "g_side": ["hood_lid", "wheel_fr", "rear_wing", "rear_bumper", "rear_diffuser", "rear_lip", "tail_lights", "rear_duckbill"],
            "g_wide": ORDER, "g_home": []}[shot]
    out = []
    for n in ORDER:
        if n in moving:
            out.append(leave(n, shot, *moving[n]))
        elif n in done:
            out.append(off(n))
        else:
            out.append(home(n))
    return out


def cam(*keys):
    return [{"t": t, "loc": list(l), "target": list(g), "focal": f, "ease": (e[0] if e else "inout")} for t, l, g, f, *e in keys]


S = SECS
SHOTS = {
    # whole car, same camera as the RS opener
    "g_whole": {"parts": state("g_whole", {}),
                "cam": cam((0, (4.7, -5.9, 1.2), (0.15, -0.15, 0.5), 30), (S["g_whole"], (2.75, -6.15, 0.9), (0.1, -0.3, 0.5), 30, "lin"))},
    # front: lid hinges open b9 -> b14, camera rises over the frunk
    "g_front": {"parts": state("g_front", {"hood_lid": (9, 14)}),
                "cam": cam((0, (1.75, -4.6, 1.0), (0.1, -1.7, 0.55), 30), (2.0, (0.9, -4.7, 1.6), (0.05, -1.6, 0.6), 30),
                           (S["g_front"], (0.0, -4.3, 2.45), (0.0, -1.5, 0.65), 30))},
    # FR wheel slides off its axle b20.5 -> b23, push into the wheel well (brake, spring)
    "g_wheel": {"parts": state("g_wheel", {"wheel_fr": (20.5, 23)}),
                "cam": cam((0, (-3.3, -0.27, 0.85), (-0.80, -1.22, 0.40), 30), (S["g_wheel"], (-2.2, -0.75, 0.6), (-0.78, -1.22, 0.38), 30))},
    # right sill dolly rear -> front through the breakdown, skirt drops then moves out b44.5 -> b47.5, ends on the open wheel well
    "g_side": {"parts": state("g_side", {"sideskirt": (44.5, 47.5)}),
               "cam": cam((0, (-4.1, 1.5, 0.75), (-0.85, 0.9, 0.3), 30), (S["g_side"], (-4.1, -1.05, 0.75), (-0.85, -0.6, 0.3), 30))},
    # wing + engine lid from high behind; wing lifts b29 -> b32
    "g_wing": {"parts": state("g_wing", {"rear_wing": (29, 32)}),
               "cam": cam((0, (1.6, 3.75, 1.85), (0.05, 1.9, 1.0), 38), (S["g_wing"], (-1.2, 3.85, 1.95), (-0.05, 1.9, 1.05), 38))},
    # rear strip: bumper b32->35, diffuser + lip b34->37, tail lights + engine-lid spoiler b36->39, push in on the exhaust
    "g_rear": {"parts": state("g_rear", {"rear_bumper": (32, 35), "rear_diffuser": (34, 37), "rear_lip": (34.5, 37.5),
                                         "tail_lights": (36, 39), "rear_duckbill": (36.5, 39.5)}),
               "cam": cam((0, (-2.9, 6.1, 1.35), (-0.1, 1.9, 0.85), 30), (6.5 * B, (-2.7, 5.8, 1.25), (-0.1, 1.9, 0.8), 30),
                          (S["g_rear"], (-1.3, 4.3, 0.8), (0.0, 1.9, 0.5), 30))},
    # everything off, wide from the front-right, high
    "g_wide": {"parts": state("g_wide", {}),
               "cam": cam((0, (-5.5, -5.5, 3.0), (0, 0.45, 0.95), 30), (S["g_wide"], (-6.6, -2.9, 3.3), (0, 0.5, 0.95), 30, "lin"))},
    # parts fly home b68 -> lock b74, seen from the rear-left; fade in the assembler
    "g_home": {"parts": [back(n, "g_home", 68 + 0.25 * i, 74) for i, n in enumerate(ORDER)],
               "cam": cam((0, (5.9, 5.3, 2.6), (0, 0.5, 0.75), 30), (12 * B, (5.0, 5.4, 1.5), (0, 0.7, 0.6), 30),
                          (S["g_home"], (4.85, 5.25, 1.4), (0, 0.7, 0.6), 30))},
}


def spec(name, mode, frames=None):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": BASE, "parts": s["parts"], "camera": {"sensor": 20.25, "keys": s["cam"]}, "seconds": SECS[name], "fps": 15,
          "res": "1080x960", "res_pct": 75 if final else 35, "samples": 12 if final else 6, "persist": False,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if not final:
        sp["frames"] = frames or ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
