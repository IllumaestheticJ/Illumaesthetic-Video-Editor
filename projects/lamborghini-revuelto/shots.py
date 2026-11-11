"""Shot list for the Lamborghini Revuelto Temerario-style reel -> one tools/shot.py JSON per shot.
  python projects/lamborghini-revuelto/shots.py [cuts.json]     # writes /home/user/media/work/revuelto/shots/*.json
Prepped frame (m): ground z=0, nose -Y (y=-2.46), rear +Y (2.46), car's LEFT = +X (the side every part scan covers).
Camera az: 0 = in front of the nose, +90 = car's left side (+X), -90 = right side, 180 = behind.
Shot lengths come from the music's accents (cuts.json, written after `ive beats`); free shots (turntables, close-ups)
are rendered with LEAD seconds of slack so they can be trimmed with `in` without re-rendering.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
M = "/home/user/media/lamborghini-revuelto/blend/"
OUT = "/home/user/media/work/revuelto/shots/"
RENDERS = "/home/user/media/work/renders/revuelto/"
HINGE = json.load(open(os.path.join(HERE, "hinge.json")))
FPS = 15
EXPOSURE = -0.5  # Huracan sibling measured flat-shaded silver vs the Temerario crop: -0.5 EV matches its mid-grey

# shot lengths (s); overwritten from cuts.json once the music is in
DUR = {"s1_side": 3.2, "s2_front34": 3.2, "s3_rear34": 3.2, "s4_headlight": 2.2, "s5_wheel": 2.2,
       "s6_frontopen": 3.4, "s7_top": 3.0, "s8_explode": 4.0, "s9_float": 4.0, "s10_reassemble": 4.4}
CUTS = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "cuts.json")))
DUR.update({k: v for k, v in CUTS["dur"].items() if k in DUR})
LEAD = 0.5  # slack on free shots

PARTS = {"fb": "front_bumper", "hl": "head_lights", "hood": "hood", "fe": "fender", "ssf": "side_skirt_front",
         "ssr": "side_skirt_rear", "fin": "side_fin", "mir": "side_mirrors", "rb": "rear_bumper_forced",
         "wing": "rear_wing", "tll": "tail_light_l", "tlr": "tail_light_r"}
EXPLODED_OBJS = {"base": M + "base.blend", **{k: M + v + ".blend" for k, v in PARTS.items()}}
# full-car beats use the ASSEMBLED composite (base + every part at home): the raw full-car scan's front fascia is
# full of holes (dark trims not captured) that the separately scanned front bumper/headlights fill
CAR = EXPLODED_OBJS
ZONE = {"car": M + "car_zone.blend"}  # 2 mm inside the front-left corner and rear boxes (close-ups)

Z = [0, 0, 0]
HOME = {k: {"off": Z} for k in PARTS}
HOME["hood"] = {"off": Z, "deg": 0}
# front end opens (ref 12-15 s): bumper slides forward and down, headlights forward, lid swings up on its hinge
OPEN = dict(HOME, fb={"off": [0, -0.85, -0.02]}, hl={"off": [0, -0.45, 0.22]},
            hood={"off": Z, "deg": HINGE["open_deg"] * 0.85})
# exploded layout: panels float in layers ABOVE the car (portrait frame; ref 25-31 s), only slightly out toward the
# left-side camera (lesson: keep parts from flying at the lens)
EXPL = {"fb": {"off": [0, -0.25, 0.9]}, "hl": {"off": [0, -0.15, 1.3]}, "hood": {"off": [0, -0.05, 1.7], "deg": 0},
        "fe": {"off": [0.3, 0, 0.8]}, "ssf": {"off": [0.4, 0, 0.4]}, "ssr": {"off": [0.4, 0, 0.45]},
        "fin": {"off": [0.35, 0, 0.6]}, "mir": {"off": [0.3, 0, 0.7]}, "rb": {"off": [0, 0.25, 0.9]},
        "wing": {"off": [0, 0.1, 1.25]}, "tll": {"off": [0.1, 0.15, 1.6]}, "tlr": {"off": [-0.1, 0.15, 1.6]}}
EXPL_DRIFT = {k: dict(v, off=[v["off"][0] * 1.06, v["off"][1] * 1.06, v["off"][2] * 1.06 + 0.04]) for k, v in EXPL.items()}


def tween(a, b, stagger):
    """keys moving every part from state a to b over its own (t0, t1) window (shot fractions)"""
    return {k: [dict(t=0, **a[k]), dict(t=s0, **a[k]), dict(t=s1, **b[k]), dict(t=1, **b[k])]
            for k, (s0, s1) in ((k, stagger.get(k, (0, 0.001))) for k in PARTS)}


def hold(state):
    return {k: [dict(t=0, **state[k])] for k in PARTS}


def shot(name, objects, camera, anims=None, light_ref=None, lead=0.0):
    d = dict(objects=objects, seconds=round(DUR[name] + lead, 3), fps=FPS, res=[1080, 1920], res_pct=75, samples=12,
             camera=camera, out=RENDERS + name, anims=anims or {}, exposure=EXPOSURE,
             hinges={"hood": {"p": HINGE["p"], "axis": HINGE["axis"]}})
    d["light_ref"] = light_ref or ("base" if "base" in objects else "car")
    return name, d


LOCK = round((CUTS["lock_s"] - CUTS["cuts_s"][9]) / DUR["s10_reassemble"], 4)
T = [0, 0, 0.5]
SHOTS = [
    # 1 intro: low side profile, nose right, slow track toward the nose; fades up from black (ref 0-3 s)
    shot("s1_side", CAR, [dict(t=0, az=-96, el=3, dist=5.8, target=[0, 0.8, 0.48], lens=40),
                          dict(t=1, az=-84, el=4, dist=5.5, target=[0, -0.6, 0.48], lens=40, lin=True)], lead=LEAD),
    # 2 front 3/4 low, slow turntable (ref 4-7 s)
    shot("s2_front34", CAR, [dict(t=0, az=-42, el=5, dist=7.0, target=T, lens=50),
                             dict(t=1, az=-14, el=8, dist=6.6, target=T, lens=50)], lead=LEAD),
    # 3 rear 3/4 turntable, left side (ref 8-11 s)
    shot("s3_rear34", CAR, [dict(t=0, az=150, el=10, dist=6.8, target=[0, 0.2, 0.5], lens=50),
                            dict(t=1, az=124, el=13, dist=6.5, target=[0, 0.2, 0.5], lens=50)], lead=LEAD),
    # 4 extreme close-up: front-left headlight + intake, 2 mm, slow slide across (ref 12 s)
    shot("s4_headlight", CAR, [dict(t=0, az=8, el=6, dist=1.7, target=[0.62, -2.05, 0.42], lens=50),
                                dict(t=1, az=34, el=9, dist=1.5, target=[0.62, -2.0, 0.42], lens=50)], lead=LEAD),
    # 5 extreme close-up: front-left wheel - spokes, carbon-ceramic disc, caliper (2 mm)
    shot("s5_wheel", ZONE, [dict(t=0, az=62, el=4, dist=2.0, target=[0.9, -1.45, 0.36], lens=50),
                            dict(t=1, az=92, el=6, dist=1.8, target=[0.9, -1.45, 0.36], lens=50)], lead=LEAD),
    # 6 front end opens: bumper slides off, headlights out, lid swings up on its fitted hinge (ref 12-15 s)
    shot("s6_frontopen", EXPLODED_OBJS,
         [dict(t=0, az=38, el=12, dist=4.6, target=[0, -1.6, 0.5], lens=40),
          dict(t=1, az=24, el=18, dist=5.0, target=[0, -1.8, 0.65], lens=40)],
         tween(HOME, OPEN, {"fb": (0.03, 0.42), "hl": (0.25, 0.62), "hood": (0.62, 0.98)}), light_ref="base"),
    # 7 top-down: crane up and over, spinning, front end open (ref 16-20 s)
    shot("s7_top", EXPLODED_OBJS,
         [dict(t=0, az=20, el=60, dist=9.5, target=[0, -0.5, 0.4], lens=40),
          dict(t=0.55, az=-15, el=89.9, dist=9.0, target=[0, -0.5, 0.4], lens=40),
          dict(t=1, az=-50, el=89.9, dist=8.6, target=[0, -0.5, 0.4], lens=40)],
         hold(OPEN), light_ref="base", lead=LEAD),
    # 8 exploded view builds: every panel separates, staggered (high rear 3/4 left, ref 21-23 s)
    shot("s8_explode", EXPLODED_OBJS,
         [dict(t=0, az=140, el=22, dist=8.6, target=[0, 0, 0.9], lens=40),
          dict(t=1, az=118, el=14, dist=11.0, target=[0, 0, 1.25], lens=40)],
         tween(OPEN, EXPL, {"wing": (0.0, 0.4), "rb": (0.05, 0.45), "tll": (0.1, 0.5), "tlr": (0.1, 0.5),
                            "ssr": (0.15, 0.55), "ssf": (0.18, 0.58), "fin": (0.2, 0.6), "mir": (0.22, 0.62),
                            "fe": (0.25, 0.65), "fb": (0.3, 0.7), "hl": (0.32, 0.72), "hood": (0.35, 0.8)}),
         light_ref="base"),
    # 9 wide side view, panels floating in layers above the car (ref 25-31 s)
    shot("s9_float", EXPLODED_OBJS,
         [dict(t=0, az=100, el=6, dist=11.6, target=[0, 0, 1.25], lens=40),
          dict(t=1, az=82, el=9, dist=11.2, target=[0, 0, 1.25], lens=40, lin=True)],
         {k: [dict(t=0, **EXPL[k]), dict(t=1, lin=True, **EXPL_DRIFT[k])] for k in PARTS}, light_ref="base", lead=LEAD),
    # 10 panels fly home and LOCK on the climax taiko hit (27.97 s, ease-in = they slam in), then rear 3/4 hero
    #    push through the climax; fades out under the last hit (ref 32-35 s)
    shot("s10_reassemble", EXPLODED_OBJS,
         [dict(t=0, az=118, el=14, dist=11.0, target=[0, 0, 1.25], lens=40),
          dict(t=LOCK, az=146, el=9, dist=7.6, target=[0, 0.15, 0.55], lens=40),
          dict(t=1, az=158, el=7, dist=6.6, target=[0, 0.2, 0.5], lens=40, lin=True)],
         {k: [dict(t=0, **EXPL_DRIFT[k]), dict(t=st, **EXPL_DRIFT[k]), dict(t=LOCK, ease="in", **HOME[k]), dict(t=1, **HOME[k])]
          for k, st in zip(PARTS, [0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22])},
         light_ref="base"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
