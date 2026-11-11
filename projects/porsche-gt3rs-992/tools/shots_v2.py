"""v2 shot specs (projects/porsche-gt3rs-992/direction.md) -> JSON for tools/shot.py.

    python projects/porsche-gt3rs-992/tools/shots_v2.py preview|final [shot ...]

One clockwise lap, one section per sequence, parts come off section by section and STAY off (progressive explode),
then a top overview of everything off, then the layered stack on the drop + reassembly. Part keys are LOCAL seconds
(reel time - shot start frame / 30). Scan frame: front = -Y, car's left = +X, z up, metres.
"""
import json
import os
import sys

P = "/home/user/media/porsche-gt3rs-992/prep"
OUT = "/home/user/media/work/gt3/renders"
SPECS = "/home/user/media/work/gt3/specs"
CAR = f"{P}/car4.blend"
# base = full car with ONLY the 9 moving parts cut out (comp_v2). Strakes, fender vent, rear strake, diffuser trim and
# the hood-vent duct stay as scanned (their cut-outs would be hollow: no removed-state scans exist).
BASE = [f"{P}/comp_v2.blend"]

# off offsets (m, deg) after each part's section; home centre z for the Sh9 layers
OFF = {
    "front_lower_lip": ((0, -0.30, -0.14), (-12, 0, 0)),
    "front_grille_trim": ((0, -0.15, 0.035), (0, 0, 0)),
    "hood_vent_top_warped": ((0, -0.20, 0.45), (0, 0, 0)),
    "rear_diffuser_1": ((0, 0.55, -0.06), (10, 0, 0)),
    "rear_qpanel_intake_1": ((-0.45, -0.25, 0.15), (0, 0, 0)),
    "rear_qpanel_intake_2": ((0.45, -0.10, 0.25), (0, 0, 0)),
    "sideskirt_lower": ((0.25, 0, -0.30), (0, 0, 0)),
    "side_skirt_upper": ((0.35, 0, -0.12), (0, 0, 0)),
    "side_skirt_strake": ((0.30, -0.05, -0.20), (0, 0, 0)),
}
HOME_Z = {"front_lower_lip": 0.18, "front_grille_trim": 0.30, "hood_vent_top_warped": 0.79, "rear_diffuser_1": 0.21,
          "rear_qpanel_intake_1": 0.71, "rear_qpanel_intake_2": 0.71, "sideskirt_lower": 0.17, "side_skirt_upper": 0.17,
          "side_skirt_strake": 0.35}
FRONT = ["front_lower_lip", "front_grille_trim", "hood_vent_top_warped"]
REAR = ["rear_diffuser_1", "rear_qpanel_intake_1", "rear_qpanel_intake_2"]
SIDE = ["sideskirt_lower", "side_skirt_upper", "side_skirt_strake"]
# shot start frames (30 fps) from the measured onsets
START = {"v2_sh1": 0, "v2_sh3": 167, "v2_sh4": 338, "v2_sh6": 504, "v2_sh7": 563, "v2_sh8": 676, "v2_sh9": 789}
SECS = {"v2_sh1": 3.9, "v2_sh3": 5.85, "v2_sh4": 3.0, "v2_sh6": 2.1, "v2_sh7": 3.9, "v2_sh8": 3.9, "v2_sh9": 7.0}


def loc(shot, reel_t):
    return round(reel_t - START[shot] / 30, 4)


def part(name, keys):
    return {"blend": f"{P}/x_{name}.blend", "keys": keys}


def still_off(name):
    o, r = OFF[name]
    return part(name, [{"t": 0, "loc": list(o), "rot": list(r)}])


def home(name):
    return part(name, [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}])


def come_off(name, t0, t1, ease="inout"):
    o, r = OFF[name]
    return part(name, [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": t0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                       {"t": t1, "loc": list(o), "rot": list(r), "ease": ease}])


def cam(*keys):
    out = []
    for t, l, g, f, *e in keys:
        out.append({"t": t, "loc": list(l), "target": list(g), "focal": f, "ease": e[0] if e else "inout"})
    return out


S = "v2_sh3"
SH3 = [come_off("front_lower_lip", loc(S, 7.530), loc(S, 9.311)),
       come_off("front_grille_trim", loc(S, 8.465), loc(S, 9.311)),
       come_off("hood_vent_top_warped", loc(S, 9.311), loc(S, 10.340))] + [home(n) for n in REAR + SIDE]
S = "v2_sh6"
SH6 = [still_off(n) for n in FRONT] + [come_off("rear_diffuser_1", loc(S, 16.807), loc(S, 17.60)),
                                       come_off("rear_qpanel_intake_1", loc(S, 17.10), loc(S, 17.90)),
                                       come_off("rear_qpanel_intake_2", loc(S, 17.10), loc(S, 17.90))] + [home(n) for n in SIDE]
S = "v2_sh7"
SH7 = [still_off(n) for n in FRONT + REAR] + [come_off("sideskirt_lower", loc(S, 18.779), loc(S, 19.718)),
                                              come_off("side_skirt_upper", loc(S, 19.249), loc(S, 20.187)),
                                              come_off("side_skirt_strake", loc(S, 20.567), loc(S, 21.40))]

# Sh9: from off offsets rise into three layered columns above their homes, hold, fly home, lock on 31.905
S = "v2_sh9"
LAYERS = {"front_lower_lip": 1.75, "front_grille_trim": 2.05, "hood_vent_top_warped": 2.35,
          "sideskirt_lower": 1.75, "side_skirt_upper": 2.00, "side_skirt_strake": 2.25,
          "rear_diffuser_1": 1.75, "rear_qpanel_intake_1": 2.10, "rear_qpanel_intake_2": 2.10}
ORDER = sorted(LAYERS, key=lambda n: LAYERS[n])  # lower layers first
LAND, BACK, LOCK = loc(S, 29.121), loc(S, 30.033), loc(S, 31.905)
SH9 = []
for k, n in enumerate(ORDER):
    o, r = OFF[n]
    lx = 0.08 * (1 if o[0] > 0 else -1 if o[0] < 0 else 0)  # keep x near home, a touch outward
    lay = [lx, 0.0, LAYERS[n] - HOME_Z[n]]
    SH9.append(part(n, [{"t": 0, "loc": list(o), "rot": list(r)},
                        {"t": 0.12 * k, "loc": list(o), "rot": list(r)},
                        {"t": LAND, "loc": lay, "rot": [0, 0, 0], "ease": "out"},
                        {"t": BACK, "loc": [lay[0], lay[1], lay[2] + 0.04], "rot": [0, 0, 0], "ease": "lin"},
                        {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]))

SHOTS = {
    # 1 whole car, low front-left 3/4, slide + small push, no orbit
    "v2_sh1": {"base": [CAR], "parts": [],
               "cam": cam((0, (3.55, -6.0, 1.0), (0.15, -0.2, 0.5), 30),
                          (3.9, (3.9, -5.45, 0.92), (0.2, -0.15, 0.5), 30, "out2"))},
    # 3 nose: lip off, grille trim toward camera, hood vent top up
    "v2_sh3": {"base": BASE, "parts": SH3,
               "cam": cam((0, (1.75, -4.6, 0.7), (0.2, -1.95, 0.42), 30),
                          (2.0, (0.8, -4.85, 0.85), (0.08, -2.0, 0.48), 30),
                          (5.85, (0.0, -4.95, 1.0), (0.0, -2.0, 0.55), 30))},
    # 4 right front fender louvres, front parts held off
    "v2_sh4": {"base": BASE, "parts": [still_off(n) for n in FRONT] + [home(n) for n in REAR + SIDE],
               "cam": cam((0, (-2.1, -1.95, 1.15), (-0.82, -1.15, 0.72), 38),
                          (3.0, (-2.15, -0.95, 1.1), (-0.84, -1.08, 0.66), 38))},
    # 6 rear-right 3/4 push-in: diffuser + undertray back, QP intakes out
    "v2_sh6": {"base": BASE, "parts": SH6,
               "cam": cam((0, (-2.85, 5.95, 1.2), (-0.2, 1.65, 0.5), 30),
                          (2.1, (-2.5, 5.55, 1.1), (-0.15, 1.7, 0.45), 30, "out2"))},
    # 7 left sill dolly rear -> front, skirts off
    "v2_sh7": {"base": BASE, "parts": SH7,
               "cam": cam((0, (4.1, 1.5, 0.75), (0.85, 0.9, 0.3), 30),
                          (3.9, (4.1, -1.05, 0.75), (0.85, -0.6, 0.3), 30))},
    # 8 crane from high rear-left to near top-down, everything off
    "v2_sh8": {"base": BASE, "parts": [still_off(n) for n in OFF],
               "cam": cam((0, (2.3, 5.0, 5.0), (0, 0.1, 0.5), 30),
                          (3.9, (1.0, 1.7, 7.5), (0, 0.0, 0.45), 30))},
    # 9 drop: layered stack above the car (left side), fly home, lock, rear-left 3/4 hero
    "v2_sh9": {"base": BASE, "parts": SH9,
               "cam": cam((0, (8.6, -0.15, 2.0), (0, -0.2, 1.25), 30),
                          (3.75, (7.6, 3.9, 2.7), (0, 0.2, 1.25), 30),
                          (5.62, (4.95, 5.35, 1.4), (0, 0.7, 0.6), 30),
                          (7.0, (4.8, 5.2, 1.35), (0, 0.7, 0.6), 30))},
}


def spec(name, mode, frames=None):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s["parts"], "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name], "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6, "persist": False,
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
