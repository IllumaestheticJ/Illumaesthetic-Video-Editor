"""Shot list for the MR2 Spyder Temerario-style reel -> one JSON per shot for projects/huracan-evo/tools/shot.py
(the Huracan sibling's Blender renderer: keyframed orbit/crane/dolly cameras, per-part translate + hinge keys).
  python projects/toyota-mr2-spyder/shots.py         # writes /home/user/media/work/mr2/shots/*.json
  blender -b -P projects/huracan-evo/tools/shot.py -- /home/user/media/work/mr2/shots/<name>.json

Prepped frame (m): ground z=0, long axis Y, NOSE AT +Y (y=+1.94), rear at -Y. Car's right = -X? (nose +Y, so +X is the
car's left... see clips.md). shot.py camera az: 0 = behind the car (-Y), 180 = in front of the nose, +90 = camera on +X.
Shots are rendered ~0.25 s longer than their slot so assembly can trim to the music's accents.
Track grid (tools/music_grid.py, kick-anchored): beat n at -0.0591 + 0.53570 n s (112.0 BPM); slots in beats:
  s1 0-5 | s2 5-13 | s3 13-17 (big hit 13) | s4 17-21 | s5 21-25 | s6 25-33 | s7 33-41 | s8 41-45 | s9 45-53 (big hit 45)
  | s10 53-57 | s11 57-62 | logo 62 (final hit 33.69 s) -> ring-out ends ~38.8 s
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
    # v2 opening (feedback on every sibling v1: "starts off too cropped"): whole car in frame, ~65 % of the width (Temerario 0-3 s)
    shot("s1_wide", 3.6, CAR, [dict(t=0, az=-97, el=4, dist=12.6, target=[0, -0.35, 0.6], lens=50),
                               dict(t=1, az=-84, el=5, dist=12.0, target=[0, 0.3, 0.6], lens=50, lin=True)]),
    # v1 opening (cropped side track) - kept for reference, not in the v2 timeline
    shot("s1_side", 3.6, CAR, [dict(t=0, az=-95, el=3, dist=5.6, target=[0, -0.8, 0.5], lens=40),
                               dict(t=1, az=-84, el=4, dist=5.4, target=[0, 0.6, 0.5], lens=40, lin=True)]),
    # 2 front 3/4 low, slow turntable (ref 4-7 s)
    shot("s2_front34", 4.5, CAR, [dict(t=0, az=-140, el=5, dist=6.6, target=T, lens=50),
                                  dict(t=1, az=-168, el=8, dist=6.3, target=T, lens=50)]),
    # 3 rear 3/4 turntable (ref 8-11 s)
    shot("s3_rear34", 2.4, CAR, [dict(t=0, az=35, el=8, dist=6.5, target=[0, -0.2, 0.55], lens=50),
                                 dict(t=1, az=58, el=11, dist=6.2, target=[0, -0.2, 0.55], lens=50)]),
    # 4 extreme close-up: front wheel + headlight corner (2 mm; wheels were captured on this car)
    shot("s4_wheel", 2.4, CAR, [dict(t=0, az=-122, el=4, dist=2.3, target=[-0.72, 1.32, 0.36], lens=50),
                                dict(t=1, az=-100, el=7, dist=1.9, target=[-0.72, 1.30, 0.38], lens=50)]),
    # 5 extreme close-up: rear lamp / side intake, slow slide
    shot("s5_tail", 2.4, CAR, [dict(t=0, az=-28, el=10, dist=2.4, target=[-0.55, -1.72, 0.72], lens=50),
                               dict(t=1, az=-48, el=12, dist=2.2, target=[-0.62, -1.55, 0.74], lens=50)]),
    # 6 the hardtop lifts off -> roof-down Spyder (high side 3/4)
    shot("s6_hardtop", 4.5, EXP, [dict(t=0, az=-120, el=16, dist=7.0, target=[0, 0, 0.75], lens=40),
                                  dict(t=1, az=-100, el=22, dist=6.6, target=[0, 0, 0.7], lens=40)],
         tween(HOME, GONE, {"top": (0.12, 0.85)}), light_ref="base"),
    # 7 front opens (bumper slides off, hood swings up on its fitted hinge), rear lid opens; front 3/4 high
    shot("s7_open", 4.5, EXP, [dict(t=0, az=-150, el=16, dist=6.8, target=[0, 0.45, 0.5], lens=40),
                               dict(t=1, az=-130, el=20, dist=7.4, target=[0, 0.35, 0.55], lens=40)],
         tween(GONE, OPEN, {"top": (0, 0.01), "fb": (0.05, 0.45), "hood": (0.3, 0.75), "lid": (0.45, 0.92)}),
         light_ref="base", extra={"visible": {"top": [0, 0]}, "persistent": False}),
    # v2 7a/7b (feedback: explode too wide / not focused on the part assemblies): one bar each, close on the section that opens
    shot("s7a_front", 2.4, EXP, [dict(t=0, az=-148, el=20, dist=4.6, target=[0, 1.3, 0.75], lens=40),
                                 dict(t=1, az=-128, el=24, dist=4.1, target=[0, 1.25, 0.8], lens=40)],
         tween(GONE, dict(GONE, hood=OPEN["hood"], fb=OPEN["fb"]), {"top": (0, 0.01), "lid": (0, 0.01), "fb": (0.05, 0.5), "hood": (0.3, 0.88)}),
         light_ref="base", extra={"visible": {"top": [0, 0]}, "persistent": False}),
    shot("s7b_rear", 2.4, EXP, [dict(t=0, az=32, el=22, dist=4.6, target=[0, -1.3, 0.85], lens=40),
                                dict(t=1, az=52, el=27, dist=4.2, target=[0, -1.25, 0.95], lens=40)],
         tween(dict(GONE, hood=OPEN["hood"], fb=OPEN["fb"]), OPEN, {"top": (0, 0.01), "fb": (0, 0.01), "hood": (0, 0.01), "lid": (0.08, 0.7)}),
         light_ref="base", extra={"visible": {"top": [0, 0]}, "persistent": False}),
    # 8 top-down: crane up and over, spinning (ref 16-20 s)
    shot("s8_top", 2.4, EXP, [dict(t=0, az=-130, el=60, dist=9.6, target=[0, 0.1, 0.4], lens=40),
                              dict(t=0.55, az=-90, el=89.9, dist=9.2, target=[0, 0.1, 0.4], lens=40),
                              dict(t=1, az=-55, el=89.9, dist=8.9, target=[0, 0.1, 0.4], lens=40)],
         hold(OPEN), light_ref="base", extra={"visible": {"top": [0, 0]}}),
    # 9 exploded view builds: hood/lid close back to flat and every panel rises into a stack above the car (high rear 3/4)
    shot("s9_explode", 4.5, EXP, [dict(t=0, az=40, el=24, dist=7.0, target=[0, 0, 0.8], lens=40),
                                  dict(t=1, az=60, el=20, dist=7.6, target=[0, 0, 1.15], lens=40)],
         tween(dict(OPEN, top={"off": [0, -0.15, 3.4]}), EXPL, {"fb": (0.05, 0.5), "hood": (0.12, 0.6), "lid": (0.2, 0.68), "top": (0.3, 0.85)}),
         light_ref="base", extra={"persistent": False}),
    # v2 9a/9b: the explode as a progressive disassembly seen close (Temerario 12-24 s): front panels rise, then rear + hardtop
    shot("s9a_front", 2.4, EXP, [dict(t=0, az=-142, el=16, dist=5.6, target=[0, 1.45, 1.0], lens=40),
                                 dict(t=1, az=-122, el=19, dist=5.2, target=[0, 1.4, 1.15], lens=40)],
         tween(OPEN, dict(OPEN, hood=EXPL["hood"], fb=EXPL["fb"]), {"top": (0, 0.01), "lid": (0, 0.01), "fb": (0.04, 0.6), "hood": (0.15, 0.82)}),
         light_ref="base", extra={"visible": {"top": [0, 0]}, "persistent": False}),
    shot("s9b_rear", 2.4, EXP, [dict(t=0, az=38, el=18, dist=6.6, target=[0, -0.75, 1.2], lens=40),
                                dict(t=1, az=58, el=21, dist=6.2, target=[0, -0.65, 1.35], lens=40)],
         tween(dict(OPEN, top={"off": [0, -0.15, 3.4]}, hood=EXPL["hood"], fb=EXPL["fb"]), EXPL,
               {"fb": (0, 0.01), "hood": (0, 0.01), "lid": (0.04, 0.6), "top": (0.2, 0.85)}),
         light_ref="base", extra={"persistent": False}),
    # 10 wide side view, panels floating (ref 25-31 s)
    shot("s10_float", 2.4, EXP, [dict(t=0, az=-70, el=13, dist=8.6, target=[0, 0, 1.2], lens=40),
                                 dict(t=1, az=-100, el=11, dist=8.3, target=[0, 0, 1.2], lens=40, lin=True)],
         {k: [dict(t=0, **EXPL[k]), dict(t=1, lin=True, **EXPL_DRIFT[k])] for k in PARTS}, light_ref="base"),
    # 11 reassembly into the finished hardtop car, front 3/4 hero, fades to black (ref 32-36 s)
    shot("s11_reassemble", 2.9, dict(EXP, **CAR), [dict(t=0, az=-130, el=14, dist=8.8, target=[0, 0, 1.05], lens=40),
                                      dict(t=1, az=-150, el=7, dist=7.0, target=[0, 0.1, 0.55], lens=40)],
         tween(EXPL_DRIFT, HOME, {"top": (0.0, 0.42), "hood": (0.08, 0.5), "lid": (0.12, 0.55), "fb": (0.2, 0.62)}),
         light_ref="base", extra={"persistent": False,
                                  # composite + diff parts are ragged at the front once closed -> the clean 2 mm car takes over
                                  # the frame the last panel lands (same frame, same pose: reads as the panels locking in)
                                  "visible": {**{k: [0, 0.64] for k in ["base", *PARTS]}, "car": [0.64, 1.01]}}),
]

# ---- v3 (director.md, 2026-11-11): nose -> roof -> tail, one continuous sequence per section ----
FB_OUT   = [-0.38, 1.00, -0.08]          # bumper parked in black, ahead of the nose and toward the lens-left
HOOD_UP  = H_HOOD["open_deg"] * 0.9       # 53.07 deg (same as v2 OPEN)
LID_UP   = H_LID["open_deg"] * 0.9        # -59.43 deg
TOP_UP   = [0, -0.10, 3.0]                # out of the top of frame in s13
TOP_HIGH = [0, 0.0, 7.5]                  # out of frame at s15 dist 8.2 (portrait half-height ~6.6 m)
FRONT_OPEN = {"fb": {"off": FB_OUT}, "hood": {"off": [0,0,0], "deg": HOOD_UP}}
R15 = {"persistent": False}  # director planned 12 fps; brief fixes 15 fps

# 3 FRONT HERO (12 beats). Hardtop ON, lid shut.
SHOTS.append(shot("s12_front", 6.70, EXP, [
    dict(t=0,    az=-152, el=12, dist=4.8, target=[0, 1.25, 1.0], lens=50),
    dict(t=0.30, az=-158, el=18, dist=4.2, target=[0, 1.45, 0.90], lens=50),   # bumper clear: look into the opening
    dict(t=0.50, az=-162, el=26, dist=3.5, target=[0, 1.35, 0.80], lens=50),
    dict(t=1,    az=-170, el=44, dist=2.7, target=[-0.15, 1.15, 0.60], lens=50)],  # down into the front compartment
  {"fb":   [dict(t=0, off=[0,0,0]), dict(t=0.04, off=[0,0,0]), dict(t=0.30, off=[-0.30, 0.80, -0.05]),
            dict(t=0.62, off=FB_OUT, lin=True), dict(t=1, off=FB_OUT)],
   "hood": [dict(t=0, off=[0,0,0], deg=0), dict(t=0.50, off=[0,0,0], deg=0), dict(t=0.74, off=[0,0,0], deg=HOOD_UP),
            dict(t=1, off=[0,0,0], deg=HOOD_UP)],
   "top":  [dict(t=0, off=[0,0,0])], "lid": [dict(t=0, off=[0,0,0], deg=0)]},
  light_ref="base", extra=R15))

# 4 SIDE + TOP (12 beats). Front stays open.
SHOTS.append(shot("s13_top", 6.70, EXP, [
    dict(t=0,    az=-70, el=28, dist=4.4, target=[0, -0.25, 0.72], lens=40),
    dict(t=0.45, az=-74, el=40, dist=4.0, target=[0, -0.28, 0.60], lens=40),
    dict(t=1,    az=-82, el=66, dist=3.6, target=[0, -0.30, 0.32], lens=40)],
  {"top":  [dict(t=0, off=[0,0,0]), dict(t=0.08, off=[0,0,0]), dict(t=0.34, off=TOP_UP), dict(t=1, off=TOP_UP)],
   "fb":   [dict(t=0, off=FB_OUT)], "hood": [dict(t=0, off=[0,0,0], deg=HOOD_UP)],
   "lid":  [dict(t=0, off=[0,0,0], deg=0)]},
  light_ref="base", extra=dict(R15, visible={"top": [0, 0.45]})))

# 5 REAR (12 beats). Lid starts ON the strong hit (t = 4/12).
SHOTS.append(shot("s14_rear", 6.70, EXP, [
    dict(t=0,     az=-38, el=16, dist=4.0, target=[0, -1.45, 0.92], lens=40),  # tail lamps + grilles fill the width
    dict(t=0.333, az=-32, el=20, dist=3.6, target=[0, -1.40, 0.90], lens=40),
    dict(t=1,     az=-22, el=50, dist=2.9, target=[0, -1.20, 0.90], lens=40)], # down into the engine bay
  {"lid":  [dict(t=0, off=[0,0,0], deg=0), dict(t=0.333, off=[0,0,0], deg=0), dict(t=0.60, off=[0,0,0], deg=LID_UP),
            dict(t=1, off=[0,0,0], deg=LID_UP)],
   "fb":   [dict(t=0, off=FB_OUT)], "hood": [dict(t=0, off=[0,0,0], deg=HOOD_UP)], "top": [dict(t=0, off=TOP_UP)]},
  light_ref="base", extra=dict(R15, visible={"top": [0, 0]})))

# 6 REASSEMBLY (9 beats) -> clean car, fade in assembly.
SHOTS.append(shot("s15_reassemble", 5.05, dict(EXP, **CAR), [
    dict(t=0, az=30, el=26, dist=5.6, target=[0, 0.10, 1.10], lens=40),
    dict(t=1, az=46, el=12, dist=5.6, target=[0, -0.05, 0.78], lens=40)],
  {"fb":   [dict(t=0, off=FB_OUT), dict(t=0.02, off=FB_OUT), dict(t=0.30, off=[0,0,0]), dict(t=1, off=[0,0,0])],
   "hood": [dict(t=0, off=[0,0,0], deg=HOOD_UP), dict(t=0.06, off=[0,0,0], deg=HOOD_UP), dict(t=0.36, off=[0,0,0], deg=0),
            dict(t=1, off=[0,0,0], deg=0)],
   "top":  [dict(t=0, off=TOP_HIGH), dict(t=0.18, off=TOP_HIGH), dict(t=0.55, off=[0,0,0]), dict(t=1, off=[0,0,0])],
   "lid":  [dict(t=0, off=[0,0,0], deg=LID_UP), dict(t=0.34, off=[0,0,0], deg=LID_UP), dict(t=0.62, off=[0,0,0], deg=0),
            dict(t=1, off=[0,0,0], deg=0)]},
  light_ref="base", extra=dict(R15, visible={"base": [0, 0.68], "fb": [0, 0.68], "hood": [0, 0.68], "lid": [0, 0.68],
                                             "top": [0.12, 0.68], "car": [0.68, 1.01]})))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
