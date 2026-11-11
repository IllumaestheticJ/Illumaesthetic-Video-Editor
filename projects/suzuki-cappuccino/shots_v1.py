"""Shot list for the Suzuki Cappuccino Temerario-style scan reel -> one tools/shot.py JSON per shot.
  python projects/suzuki-cappuccino/shots.py            # writes /home/user/media/work/cappuccino/shots/*.json
Cut times come from cuts.json (beat-gridded from the music; list of shot start times + end of last scan shot).
Prepped frame (m): ground z=0, nose -Y (bumper y=-1.64), car's right = -X. Wheels y=+-1.03, hub z=0.33.
Camera az: 0 = in front of the nose, -90 = car's right side, +-180 = behind.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/cappuccino/blend/"
OUT = "/home/user/media/work/cappuccino/shots/"
RENDERS = "/home/user/media/work/renders/cappuccino/"
HH = json.load(open(os.path.join(HERE, "hinge_hood.json")))
HT = json.load(open(os.path.join(HERE, "hinge_trunk.json")))
FPS = 15
EXPOSURE = -0.5  # huracan-evo measured: -0.5 EV puts flat-shaded silver at the Temerario ref's median luma
NAMES = ["s01_side", "s02_front34", "s03_rear34", "s04_wheel", "s05_lamp", "s06_frontopen", "s07_trunk",
         "s08_top", "s09_explode", "s10_float", "s11_reassemble"]
_c = os.path.join(HERE, "cuts.json")
CUTS = json.load(open(_c))["cuts"] if os.path.exists(_c) else [0, 3, 5.5, 8, 10, 12, 15, 18, 21, 24, 27, 31]

PARTS = {"fb": "fb_nolights", "li": "Front_Bumper_Lights", "rb": "Rear_Bumper", "hood": "hood", "trunk": "trunk"}
EXPLODED = {"base": B + "base.blend", **{k: B + v + ".blend" for k, v in PARTS.items()}}
CAR = {"car": B + "car2.blend"}  # untouched 2 mm full car for the full-car beats and close-ups
HINGES = {"hood": {"p": HH["p"], "axis": HH["axis"]}, "trunk": {"p": HT["p"], "axis": HT["axis"]}}

HOME = {k: {"off": [0, 0, 0]} for k in PARTS}
HOME["hood"]["deg"] = 0
HOME["trunk"]["deg"] = 0
# front open: bumper + lamps slide forward and down a touch, hood swings to 90 % of its captured opening
FRONT = dict(HOME, fb={"off": [0, -0.75, -0.03]}, li={"off": [0, -0.75, -0.03]},
             hood={"off": [0, 0, 0], "deg": HH["open_deg"] * 0.9})
OPEN = dict(FRONT, rb={"off": [0, 0.7, -0.03]}, trunk={"off": [0, 0, 0], "deg": HT["open_deg"] * 0.9})
# exploded layout stacks panels ABOVE the car (portrait frame; ref 25-31 s and lesson: don't fly parts at the lens)
# (framing v1 flew bumpers/lamps 0.55-0.95 m along the car - out of the 9:16 frame; now they rise in front of / behind it)
# v2 still reached the frame edges in side views: v3 stacks every panel in layers over the car's own footprint
EXPL = {"hood": {"off": [0, -0.1, 0.85], "deg": 0}, "trunk": {"off": [0, 0.1, 0.85], "deg": 0},
        "fb": {"off": [0, 0.35, 1.45]}, "li": {"off": [0, 0.35, 1.95]}, "rb": {"off": [0, -0.35, 1.55]}}
EXPL_DRIFT = {k: {"off": [v["off"][0], v["off"][1] * 1.07, v["off"][2] * 1.07 + 0.04], **({"deg": v["deg"]} if "deg" in v else {})}
              for k, v in EXPL.items()}


def tween(a, b, stagger):
    """keys moving every part from state a to b, part k between shot fractions stagger[k] (default: already there)"""
    out = {}
    for k in PARTS:
        s0, s1 = stagger.get(k, (0, 0.001))
        out[k] = [dict(t=0, **a[k]), dict(t=s0, **a[k]), dict(t=s1, **b[k]), dict(t=1, **b[k])]
    return out


def hold(state):
    return {k: [dict(t=0, **state[k])] for k in PARTS}


def shot(i, objects, camera, anims=None, light_ref=None):
    name = NAMES[i]
    d = dict(objects=objects, seconds=round(CUTS[i + 1] - CUTS[i] + 2 / FPS, 3), fps=FPS, res=[1080, 1920], res_pct=75,
             samples=12, camera=camera, out=RENDERS + name, anims=anims or {}, exposure=EXPOSURE, hinges=HINGES)
    if light_ref:
        d["light_ref"] = light_ref
    return name, d


def cam(t, az, el, dist, target, lens, **kw):
    return dict(t=t, az=az, el=el, dist=dist, target=target, lens=lens, **kw)


SHOTS = [
    # 1 low side profile tracking toward the nose, fades up from black (ref 0-3 s)
    shot(0, CAR, [cam(0, -96, 3, 4.6, [0, 0.55, 0.48], 40), cam(1, -84, 4, 4.4, [0, -0.45, 0.48], 40, lin=True)]),
    # 2 front 3/4 low, slow turntable (ref 4-7 s)
    shot(1, CAR, [cam(0, -42, 5, 5.0, [0, -0.15, 0.5], 50), cam(1, -14, 8, 4.8, [0, -0.15, 0.5], 50)]),
    # 3 rear 3/4 turntable (ref 8-11 s)
    shot(2, CAR, [cam(0, -154, 9, 4.9, [0, 0.2, 0.5], 50), cam(1, -128, 12, 4.7, [0, 0.2, 0.5], 50)]),
    # 4 extreme close-up: front-right wheel (tiny kei car - 14 in rim, can go very tight)
    shot(3, CAR, [cam(0, -60, 8, 0.95, [-0.66, -1.03, 0.55], 50), cam(1, -84, 10, 0.78, [-0.68, -1.03, 0.55], 50)]),
    # 5 extreme close-up: right headlamp and the bumper lamp below it, slow slide across the nose
    shot(4, CAR, [cam(0, -38, 12, 1.35, [-0.42, -1.42, 0.5], 50), cam(1, -12, 9, 1.15, [-0.36, -1.5, 0.45], 50)]),
    # 6 front end opens: bumper + lamps slide off, hood swings up on its fitted hinge (ref 12-15 s)
    shot(5, EXPLODED, [cam(0, -40, 13, 4.2, [0, -0.85, 0.42], 40), cam(1, -22, 19, 4.7, [0, -1.0, 0.5], 40)],
         tween(HOME, FRONT, {"fb": (0.05, 0.5), "li": (0.05, 0.5), "hood": (0.38, 0.92)}), light_ref="base"),
    # 7 rear: bumper slides off, trunk lid swings up on its fitted hinge (front stays open)
    shot(6, EXPLODED, [cam(0, -148, 17, 4.6, [-0.1, 0.85, 0.5], 40), cam(1, -128, 23, 5.0, [-0.1, 0.95, 0.58], 40)],
         tween(FRONT, OPEN, {"rb": (0.05, 0.5), "trunk": (0.38, 0.92)}), light_ref="base"),
    # 8 crane up and over to top-down, spinning, everything open (ref 16-20 s)
    shot(7, EXPLODED, [cam(0, -140, 55, 7.0, [0, 0.1, 0.4], 40), cam(0.55, -170, 89.9, 6.0, [0, 0.0, 0.4], 40),
                       cam(1, -215, 89.9, 5.7, [0, 0.0, 0.4], 40)], hold(OPEN), light_ref="base"),
    # 9 exploded view builds: panels lift and stack above the car (high 3/4, ref 21-23 s)
    shot(8, EXPLODED, [cam(0, -58, 22, 6.2, [0, -0.1, 0.75], 40), cam(1, -78, 12, 6.8, [0, -0.1, 1.1], 40)],
         tween(OPEN, EXPL, {"hood": (0.02, 0.45), "fb": (0.12, 0.55), "li": (0.2, 0.62), "trunk": (0.28, 0.7),
                            "rb": (0.36, 0.8)}), light_ref="base"),
    # 10 wide side view, panels floating, slow drift (ref 25-31 s)
    shot(9, EXPLODED, [cam(0, -96, 7, 6.7, [0, -0.05, 1.15], 40), cam(1, -112, 10, 6.4, [0, -0.05, 1.15], 40, lin=True)],
         {k: [dict(t=0, **EXPL[k]), dict(t=1, lin=True, **EXPL_DRIFT[k])] for k in PARTS}, light_ref="base"),
    # 11 reassembly into the finished car, rear 3/4 hero, fade out (ref 32-35 s)
    shot(10, EXPLODED, [cam(0, -120, 14, 6.8, [0, 0.0, 1.1], 40), cam(1, -146, 9, 5.2, [0, 0.15, 0.52], 40)],
         tween(EXPL_DRIFT, HOME, {"hood": (0.0, 0.42), "trunk": (0.08, 0.5), "li": (0.14, 0.52), "fb": (0.18, 0.6),
                                  "rb": (0.24, 0.66)}), light_ref="base"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
