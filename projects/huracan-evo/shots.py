"""Shot list for the Huracan Evo Temerario-style reel -> one tools/shot.py JSON per shot.
  python projects/huracan-evo/shots.py            # writes /home/user/media/work/huracan/shots/*.json
Cuts on kick peaks of reel_track_a (bars of 4 beats = 2.4 s):
  0 | 3.677 | 7.277 | 9.678 | 12.078 | 16.878 | 19.279 (lift) | 24.079 | 28.879 | 36.080 (music stops, logo) | 40.046
Prepped frame (m): ground z=0, nose -Y (y=-2.253), car's right = -X (the side with skirt/fender part scans).
Camera az: 0 = in front of the nose, -90 = car's right side, +-180 = behind.
"""
import json
import os

B = "/home/user/media/work/huracan/blend/"
OUT = "/home/user/media/work/huracan/shots/"
RENDERS = "/home/user/media/work/renders/huracan/"
HINGE = json.load(open(os.path.join(os.path.dirname(__file__), "hinge.json")))

# Music: reel_track_a (generated for these reels by the parent session at the user's request), 100.0 BPM.
# Kick-peak grid (40-120 Hz peaks, global pick + LSQ): t = 0.0768 + 0.60006*k ; lift at k=32 (19.278), last kick k=60 (36.080)
def K(k):
    return round(0.0768 + 0.60006 * k, 3)
CUTS = [0, K(6), K(12), K(16), K(20), K(28), K(32), K(40), K(48), K(60)]
FPS = 15
EXPOSURE = -0.5  # flat-shaded silver at 0 EV clipped the roof; ref surfaces sit mid-light grey

PARTS = {"fb": "front_bumper", "rb": "Rear_Bumper", "sk": "Side_Skirts", "fe": "Fender",
         "hood": "Hood_Only", "tc": "top_cowl", "lc": "left_cowl", "rc": "right_cowl"}
EXPLODED_OBJS = {"base": B + "base.blend", **{k: B + v + ".blend" for k, v in PARTS.items()}}
CAR = {"car": B + "car2.blend"}  # 2 mm full car for the full-car beats (more grille/vent detail than 3 mm)

# part states (offset m, hood hinge deg)
HOME = {k: {"off": [0, 0, 0]} for k in PARTS}
HOME["hood"]["deg"] = 0
OPEN = dict(HOME, fb={"off": [0, -0.95, -0.02]}, fe={"off": [-0.55, -0.05, 0.02]},
            hood={"off": [0, 0, 0], "deg": HINGE["open_deg"] * 0.85})
# exploded layout stacks panels ABOVE the car (portrait frame; ref 28-31 s) - flying them along the car's length
# sent the bumpers out of a 9:16 frame in the first framing test
EXPL = {"fb": {"off": [0, -0.45, 0.95]}, "rb": {"off": [0, 0.45, 1.0]}, "sk": {"off": [-0.55, 0, 0.6]},
        "fe": {"off": [-0.5, -0.1, 0.8]}, "hood": {"off": [0, -0.05, 1.6], "deg": 0},
        "tc": {"off": [0, 0, 0.95]}, "lc": {"off": [0.22, 0, 0.8]}, "rc": {"off": [-0.22, 0, 0.8]}}
EXPL_DRIFT = {k: {"off": [v["off"][0] * 1.06, v["off"][1] * 1.06, v["off"][2] * 1.06 + 0.04], **({"deg": v["deg"]} if "deg" in v else {})}
              for k, v in EXPL.items()}


def tween(a, b, t0, t1, stagger=None):
    """keys moving every part from state a to b between shot fractions t0..t1 (optionally staggered per part)"""
    anims = {}
    for i, k in enumerate(PARTS):
        s0, s1 = t0, t1
        if stagger:
            s0, s1 = stagger[k]
        anims[k] = [dict(t=0, **a[k]), dict(t=s0, **a[k]), dict(t=s1, **b[k]), dict(t=1, **b[k])]
    return anims


def hold(state):
    return {k: [dict(t=0, **state[k])] for k in PARTS}


# animated parts -> no Cycles persistent data: lights dropped mid-shot in s5 (hinge) AND s8 (translate-only drift)
HINGE_SHOTS = ("s5_frontopen", "s7_explode", "s8_float", "s9_reassemble")


def shot(name, i, objects, camera, anims=None, light_ref=None, extra=None):
    d = dict(objects=objects, seconds=round(CUTS[i + 1] - CUTS[i], 3), fps=FPS, res=[1080, 1920], res_pct=75, samples=12,
             camera=camera, out=RENDERS + name, anims=anims or {}, exposure=EXPOSURE, hinges={"hood": {"p": HINGE["p"], "axis": HINGE["axis"]}})
    if light_ref:
        d["light_ref"] = light_ref
    if name in HINGE_SHOTS:
        d["persistent"] = False
    d.update(extra or {})
    return name, d


T = [0, 0, 0.55]
SHOTS = [
    # 1 intro: low side profile tracking slowly along the car (ref 0-3 s), fades up from black in assembly
    shot("s1_side", 0, CAR, [dict(t=0, az=-95, el=3, dist=6.3, target=[0, 0.9, 0.5], lens=40),
                             dict(t=1, az=-84, el=3, dist=6.0, target=[0, -0.7, 0.5], lens=40, lin=True)]),
    # 2 front 3/4 slow turntable, low (ref 4-7 s)
    shot("s2_front34", 1, CAR, [dict(t=0, az=-40, el=5, dist=7.4, target=T, lens=50),
                                dict(t=1, az=-10, el=8, dist=7.0, target=T, lens=50)]),
    # 3 rear 3/4 turntable (ref 8-11 s)
    shot("s3_rear34", 2, CAR, [dict(t=0, az=-152, el=9, dist=7.2, target=[0, 0.2, 0.55], lens=50),
                               dict(t=1, az=-130, el=12, dist=6.9, target=[0, 0.2, 0.55], lens=50)]),
    # 4 extreme close-up: front-right corner, wheel off - brake disc, caliper, hub, suspension
    #   ('Front Wheel Wells' state scan at 2 mm spliced into the car; the full-car scan never captured the dark rims)
    shot("s4_wheel", 3, {"car": B + "car_nowheelzone.blend", "wz": B + "fww_zone.blend"},
         [dict(t=0, az=-62, el=6, dist=2.2, target=[-0.78, -1.37, 0.38], lens=50),
          dict(t=1, az=-84, el=9, dist=1.75, target=[-0.78, -1.37, 0.40], lens=50)], light_ref="car"),
    # 5 front end opens: bumper slides off, fender steps out, hood swings up on its hinge (ref 12-15 s)
    shot("s5_frontopen", 4, EXPLODED_OBJS,
         [dict(t=0, az=-42, el=10, dist=5.6, target=[-0.1, -1.35, 0.5], lens=40),
          dict(t=1, az=-24, el=16, dist=6.2, target=[-0.1, -1.5, 0.55], lens=40)],
         tween(HOME, OPEN, 0, 0, stagger={"fb": (0.125, 0.5), "fe": (0.375, 0.625), "hood": (0.5, 0.875), **{k: (0, 0.01) for k in ("rb", "sk", "tc", "lc", "rc")}}),
         light_ref="base"),
    # 6 top-down: crane up and over, spinning (ref 16-20 s)
    shot("s6_top", 5, EXPLODED_OBJS,
         [dict(t=0, az=-20, el=62, dist=10.5, target=[0, -0.4, 0.4], lens=40),
          dict(t=0.55, az=20, el=89.9, dist=10.0, target=[0, -0.4, 0.4], lens=40, lin=False),
          dict(t=1, az=55, el=89.9, dist=9.6, target=[0, -0.4, 0.4], lens=40)],
         hold(OPEN), light_ref="base"),
    # 7 exploded view builds: every panel separates (high rear 3/4, ref 21-23 s)
    shot("s7_explode", 6, EXPLODED_OBJS,
         [dict(t=0, az=-145, el=26, dist=8.6, target=[0, 0, 0.75], lens=40),
          dict(t=1, az=-120, el=18, dist=9.0, target=[0, 0, 1.05], lens=40)],
         tween(OPEN, EXPL, 0, 0, stagger={"rb": (0.0, 0.375), "sk": (0.125, 0.5), "fe": (0.25, 0.625), "fb": (0.25, 0.625),
                                          "hood": (0.375, 0.75), "tc": (0.5, 0.875), "lc": (0.5, 0.875), "rc": (0.5, 0.875)}),
         light_ref="base"),
    # 8 wide side view, panels floating (ref 25-31 s)
    shot("s8_float", 7, EXPLODED_OBJS,
         [dict(t=0, az=-100, el=6, dist=10.2, target=[0, 0, 1.15], lens=40),
          dict(t=1, az=-80, el=9, dist=9.7, target=[0, 0, 1.15], lens=40, lin=True)],
         {k: [dict(t=0, **EXPL[k]), dict(t=1, lin=True, **EXPL_DRIFT[k])] for k in PARTS}, light_ref="base"),
    # 9 reassembly into the finished car, rear 3/4 hero, fade out (ref 32-36 s)
    shot("s9_reassemble", 8, EXPLODED_OBJS,
         [dict(t=0, az=-120, el=14, dist=9.0, target=[0, 0, 1.05], lens=40),
          dict(t=0.5, az=-145, el=9, dist=7.8, target=[0, 0.15, 0.6], lens=40, lin=True),
          dict(t=1, az=-168, el=7, dist=7.4, target=[0, 0.15, 0.55], lens=40)],
         tween(EXPL_DRIFT, HOME, 0, 0, stagger={"tc": (0.0, 2 / 12), "lc": (0.0, 2 / 12), "rc": (0.0, 2 / 12), "hood": (0.0, 3 / 12),
                                                "fe": (1 / 12, 4 / 12), "fb": (1 / 12, 4 / 12), "sk": (2 / 12, 5 / 12), "rb": (3 / 12, 6 / 12)}),
         light_ref="base"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
