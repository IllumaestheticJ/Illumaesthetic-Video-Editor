"""Shot list for the MR2 Spyder Temerario-style reel -> one JSON per shot for projects/huracan-evo/tools/shot.py
(the Huracan sibling's Blender renderer: keyframed orbit/crane/dolly cameras, per-part translate + hinge keys).
  python projects/toyota-mr2-spyder/shots.py         # writes /home/user/media/work/mr2/shots/*.json
  blender -b -P projects/huracan-evo/tools/shot.py -- /home/user/media/work/mr2/shots/<name>.json

Prepped frame (m): ground z=0, long axis Y, NOSE AT +Y (y=+1.94), rear at -Y. Car's right = -X? (nose +Y, so +X is the
car's left... see clips.md). shot.py camera az: 0 = behind the car (-Y), 180 = in front of the nose, +90 = camera on +X.
Shots are rendered a little longer than their slot (SECS) so assembly can trim to the music's accents.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/mr2/blend/"
OUT = "/home/user/media/work/mr2/shots/"
RENDERS = "/home/user/media/work/renders/mr2/"
FPS = 15
EXPOSURE = -0.5  # Huracan measurement: flat-shaded silver at 0 EV clips the roof; -0.5 EV matches the Temerario greys

H_LID = json.load(open(os.path.join(HERE, "hinge_rearlid.json")))
_hh = os.path.join(HERE, "hinge_hood.json")
H_HOOD = json.load(open(_hh)) if os.path.exists(_hh) else {"p": [0, 0, 0], "axis": [1, 0, 0], "open_deg": 0}  # placeholder until fitted
HINGES = {"lid": {"p": H_LID["p"], "axis": H_LID["axis"]}, "hood": {"p": H_HOOD["p"], "axis": H_HOOD["axis"]}}

CAR = {"car": B + "car2.blend"}  # 2 mm full car, hardtop on
PARTS = {"top": "hardtop", "hood": "hood", "fb": "fbumper", "lid": "rearlid"}
EXP = {"base": B + "base.blend", **{k: B + v + ".blend" for k, v in PARTS.items()}}

# part states: offset (m) and hinge angle (deg)
HOME = {"top": {"off": [0, 0, 0]}, "hood": {"off": [0, 0, 0], "deg": 0}, "fb": {"off": [0, 0, 0]}, "lid": {"off": [0, 0, 0], "deg": 0}}
GONE = dict(HOME, top={"off": [0, -0.3, 3.2]})                        # hardtop lifted out of frame (s6)
OPEN = dict(GONE, hood={"off": [0, 0, 0], "deg": H_HOOD["open_deg"] * 0.9}, fb={"off": [0, 0.55, 0.06]},
            lid={"off": [0, 0, 0], "deg": H_LID["open_deg"] * 0.9})
# exploded: panels stacked ABOVE the car (portrait frame; Temerario 25-31 s; Huracan lesson: don't fly along the length)
EXPL = {"top": {"off": [0, -0.15, 1.6]}, "hood": {"off": [0, 0.3, 1.15], "deg": 0}, "fb": {"off": [0, 0.7, 0.8]},
        "lid": {"off": [0, -0.4, 1.05], "deg": 0}}
EXPL_DRIFT = {k: dict(v, off=[v["off"][0], v["off"][1] * 1.06, v["off"][2] * 1.05 + 0.04]) for k, v in EXPL.items()}


def tween(a, b, stagger):
    return {k: [dict(t=0, **a[k]), dict(t=s0, **a[k]), dict(t=s1, **b[k]), dict(t=1, **b[k])] for k, (s0, s1) in stagger.items()}


def hold(state):
    return {k: [dict(t=0, **state[k])] for k in PARTS}


def shot(name, secs, objects, camera, anims=None, light_ref=None, extra=None):
    d = dict(objects=objects, seconds=secs, fps=FPS, res=[1080, 1920], res_pct=75, samples=12, camera=camera,
             out=RENDERS + name, anims=anims or {}, exposure=EXPOSURE, hinges=HINGES)
    if light_ref:
        d["light_ref"] = light_ref
    d.update(extra or {})
    return name, d


T = [0, 0, 0.55]
SHOTS = [
    # 1 intro: low side profile, slow track along the car toward the nose (Temerario 0-3 s); fades up in assembly
    shot("s1_side", 3.6, CAR, [dict(t=0, az=-95, el=3, dist=5.6, target=[0, -0.8, 0.5], lens=40),
                               dict(t=1, az=-84, el=4, dist=5.4, target=[0, 0.6, 0.5], lens=40, lin=True)]),
    # 2 front 3/4 low, slow turntable (ref 4-7 s)
    shot("s2_front34", 4.2, CAR, [dict(t=0, az=-140, el=5, dist=6.6, target=T, lens=50),
                                  dict(t=1, az=-168, el=8, dist=6.3, target=T, lens=50)]),
    # 3 rear 3/4 turntable (ref 8-11 s)
    shot("s3_rear34", 3.6, CAR, [dict(t=0, az=35, el=8, dist=6.5, target=[0, -0.2, 0.55], lens=50),
                                 dict(t=1, az=58, el=11, dist=6.2, target=[0, -0.2, 0.55], lens=50)]),
    # 4 extreme close-up: front wheel + headlight corner (2 mm; wheels were captured on this car)
    shot("s4_wheel", 2.6, CAR, [dict(t=0, az=-122, el=4, dist=2.3, target=[-0.72, 1.32, 0.36], lens=50),
                                dict(t=1, az=-100, el=7, dist=1.9, target=[-0.72, 1.30, 0.38], lens=50)]),
    # 5 extreme close-up: rear lamp / side intake, slow slide
    shot("s5_tail", 2.6, CAR, [dict(t=0, az=-28, el=10, dist=2.4, target=[-0.55, -1.72, 0.72], lens=50),
                               dict(t=1, az=-48, el=12, dist=2.2, target=[-0.62, -1.55, 0.74], lens=50)]),
    # 6 the hardtop lifts off -> roof-down Spyder (high side 3/4)
    shot("s6_hardtop", 4.2, EXP, [dict(t=0, az=-120, el=16, dist=7.0, target=[0, 0, 0.75], lens=40),
                                  dict(t=1, az=-100, el=22, dist=6.6, target=[0, 0, 0.7], lens=40)],
         tween(HOME, GONE, {"top": (0.12, 0.85)}), light_ref="base"),
    # 7 front opens (bumper slides off, hood swings up on its fitted hinge), rear lid opens; front 3/4 high
    shot("s7_open", 4.2, EXP, [dict(t=0, az=-150, el=16, dist=6.8, target=[0, 0.45, 0.5], lens=40),
                               dict(t=1, az=-130, el=20, dist=7.4, target=[0, 0.35, 0.55], lens=40)],
         tween(GONE, OPEN, {"top": (0, 0.01), "fb": (0.05, 0.45), "hood": (0.3, 0.75), "lid": (0.45, 0.92)}),
         light_ref="base", extra={"visible": {"top": [0, 0]}}),
    # 8 top-down: crane up and over, spinning (ref 16-20 s)
    shot("s8_top", 3.6, EXP, [dict(t=0, az=-130, el=60, dist=9.6, target=[0, 0.1, 0.4], lens=40),
                              dict(t=0.55, az=-90, el=89.9, dist=9.2, target=[0, 0.1, 0.4], lens=40),
                              dict(t=1, az=-55, el=89.9, dist=8.9, target=[0, 0.1, 0.4], lens=40)],
         hold(OPEN), light_ref="base", extra={"visible": {"top": [0, 0]}}),
    # 9 exploded view builds: hood/lid close back to flat and every panel rises into a stack above the car (high rear 3/4)
    shot("s9_explode", 4.2, EXP, [dict(t=0, az=40, el=24, dist=7.0, target=[0, 0, 0.8], lens=40),
                                  dict(t=1, az=60, el=20, dist=7.6, target=[0, 0, 1.15], lens=40)],
         tween(dict(OPEN, top={"off": [0, -0.15, 3.4]}), EXPL, {"fb": (0.05, 0.5), "hood": (0.12, 0.6), "lid": (0.2, 0.68), "top": (0.3, 0.85)}),
         light_ref="base"),
    # 10 wide side view, panels floating (ref 25-31 s)
    shot("s10_float", 3.6, EXP, [dict(t=0, az=-70, el=13, dist=8.6, target=[0, 0, 1.2], lens=40),
                                 dict(t=1, az=-100, el=11, dist=8.3, target=[0, 0, 1.2], lens=40, lin=True)],
         {k: [dict(t=0, **EXPL[k]), dict(t=1, lin=True, **EXPL_DRIFT[k])] for k in PARTS}, light_ref="base"),
    # 11 reassembly into the finished hardtop car, front 3/4 hero, fades to black (ref 32-36 s)
    shot("s11_reassemble", 4.6, EXP, [dict(t=0, az=-130, el=14, dist=8.8, target=[0, 0, 1.05], lens=40),
                                      dict(t=1, az=-150, el=7, dist=7.0, target=[0, 0.1, 0.55], lens=40)],
         tween(EXPL_DRIFT, HOME, {"top": (0.0, 0.42), "hood": (0.08, 0.5), "lid": (0.12, 0.55), "fb": (0.2, 0.62)}),
         light_ref="base"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
