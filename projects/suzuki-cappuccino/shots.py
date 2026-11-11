"""Shot list v2 for the Suzuki Cappuccino scan reel -> one tools/shot.py JSON per shot (v1 recipe: shots_v1.py).
Plan: direction.md (scene order from the scan inventory) + director.md (one focus per shot). User v2 brief + addendum A-D.
  python projects/suzuki-cappuccino/shots.py      # writes /home/user/media/work/cappuccino/shots_v2/*.json
Cuts land on the broadband kick onset frames of the source track (onsets.json, beat n -> frame), not the low-band grid.
Prepped frame (m): ground z=0, nose -Y (bumper y=-1.64), car's right = -X. Wheels y=+-1.03, hub z=0.33.
Camera az: 0 = in front of the nose, -90 = car's right side, +-180 = behind, +90 = left side.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/cappuccino/blend/"
OUT = "/home/user/media/work/cappuccino/shots_v2/"
RENDERS = "/home/user/media/work/renders/cappuccino_v2/"
HH = json.load(open(os.path.join(HERE, "hinge_hood.json")))
HT = json.load(open(os.path.join(HERE, "hinge_trunk.json")))
ONSET_F = json.load(open(os.path.join(HERE, "onsets.json")))["frames"]  # beat n -> cut frame at 30 fps
FPS = 15
EXPOSURE = -0.5
HOOD_OPEN, TRUNK_OPEN = HH["open_deg"], HT["open_deg"]  # 100 % = the captured propped angles (v1 used 90 %)

PARTS = {"fb": "fb_nolights", "li": "Front_Bumper_Lights", "rb": "Rear_Bumper", "hood": "hood", "trunk": "trunk"}
EXPLODED = {"base": B + "base.blend", **{k: B + v + ".blend" for k, v in PARTS.items()}}
CAR = {"car": B + "car2.blend"}
HINGES = {"hood": {"p": HH["p"], "axis": HH["axis"]}, "trunk": {"p": HT["p"], "axis": HT["axis"]}}


def secs(b0, b1):
    """render length for a shot between beats b0..b1 (+2 frames at 15 fps of margin for the assembler's trim)"""
    f0 = 0 if b0 == 0 else ONSET_F[b0]
    return round((ONSET_F[b1] - f0) / 30 + 2 / FPS, 3)


def cam(t, az, el, dist, target, lens, **kw):
    return dict(t=t, az=az, el=el, dist=dist, target=target, lens=lens, **kw)


def k(t, off=(0, 0, 0), deg=None, spin=None, lin=False):
    d = dict(t=t, off=list(off))
    if deg is not None:
        d["deg"] = deg
    if spin is not None:
        d["spin"] = [spin, 1, 0, 0]  # about the part's own centre, car-width (X) axis: bumpers tip, never Z-spin
    if lin:
        d["lin"] = True
    return d


HOME = {p: [k(0, deg=0 if p in ("hood", "trunk") else None, spin=0 if p in ("fb", "rb") else None)] for p in PARTS}
# poses (director.md)
F_OUT = {"fb": dict(off=[0, -0.70, -1.00], spin=95), "li": dict(off=[0, -0.95, -0.90])}
R_OUT = {"rb": dict(off=[0, 0.75, -1.05], spin=-95)}
LAYERS = {"hood": dict(off=[0, 0, 0.85], deg=0), "trunk": dict(off=[0, 0, 0.85], deg=0),
          "fb": dict(off=[0, -0.45, 1.20], spin=80), "li": dict(off=[0, -0.55, 1.60]), "rb": dict(off=[0, 0.45, 1.30], spin=-80)}
DRIFT = {p: dict(v, off=[v["off"][0], v["off"][1], v["off"][2] + 0.04]) for p, v in LAYERS.items()}

SHOTS = {}


def shot(name, b0, b1, objects, camera, anims=None, visible=None, light_ref=None):
    d = dict(objects=objects, seconds=secs(b0, b1), fps=FPS, res=[1080, 1920], res_pct=75, samples=12, camera=camera,
             out=RENDERS + name, anims=anims or {}, exposure=EXPOSURE, hinges=HINGES, persist=False)
    if visible:
        d["visible"] = visible
    if light_ref:
        d["light_ref"] = light_ref
    SHOTS[name] = d


# 1 whole car, front-right 3/4, fully in frame, moving from frame 1 (v1 openers were cropped at 4.4-5 m)
shot("s1_whole", 0, 8, CAR, [cam(0, -58, 9, 6.1, [0, -0.05, 0.52], 40), cam(1, -34, 7, 5.5, [0, -0.15, 0.50], 40, lin=True)])  # lin: constant orbit, moving from frame 1

# 2 front: right lamp pair -> lamps out toward the lens -> bumper forward/down and tipped (inner face, mounting tabs)
#   -> camera moves in on the structure behind the bumper and holds (hero beat C)
shot("s2_frontbumper", 8, 28, EXPLODED,
     [cam(0, -30, 8, 1.6, [-0.42, -1.45, 0.45], 50), cam(0.15, -27, 10, 1.5, [-0.30, -1.50, 0.42], 50),
      cam(0.35, -22, 22, 3.6, [0, -1.75, 0.25], 40), cam(0.50, -18, 40, 2.0, [0, -2.16, -0.13], 45),
      cam(0.66, -16, 42, 1.9, [0, -2.16, -0.13], 45), cam(0.80, -12, 12, 1.5, [0, -1.45, 0.35], 45),
      cam(1, -4, 10, 1.3, [0, -1.40, 0.38], 45, lin=True)],
     {"li": [k(0), k(0.15), k(0.30, (0, -0.75, 0)), k(0.66, (0, -0.75, 0)), k(0.80, F_OUT["li"]["off"])],
      "fb": [k(0, spin=0), k(0.30, spin=0), k(0.45, (0, -0.55, -0.45), spin=60), k(0.55, (0, -0.55, -0.45), spin=95),
             k(0.66, (0, -0.55, -0.45), spin=95), k(0.80, F_OUT["fb"]["off"], spin=95)],
      "hood": HOME["hood"], "rb": HOME["rb"], "trunk": HOME["trunk"]}, light_ref="base")

# 3 engine bay: held rise through the break (no cut), hood swings ON the drop (beat 32), push into the bay
_t32 = (ONSET_F[32] - ONSET_F[28]) / (ONSET_F[40] - ONSET_F[28])
shot("s3_engine", 28, 40, EXPLODED,
     [cam(0, -24, 24, 3.2, [0, -0.95, 0.70], 40), cam(_t32, -20, 30, 2.9, [0, -0.95, 0.65], 40),
      cam(0.55, -12, 44, 2.3, [0, -1.0, 0.48], 40), cam(1, -6, 36, 1.75, [0.05, -1.15, 0.42], 45)],
     {"hood": [k(0, deg=0), k(_t32, deg=0), k(_t32 + 0.12, deg=HOOD_OPEN)], "rb": HOME["rb"], "trunk": HOME["trunk"]},
     visible={"fb": [0, 0], "li": [0, 0]}, light_ref="base")

# 4 front-right wheel: REUSED v1 render (renders/cappuccino/s04_wheel) - no JSON here

# 5 rear: bumper back/down and tipped (inner face) -> hold on rear panel / wiring / exhaust (Rear End All Removed)
#   -> trunk lid up to its captured angle (Rear End Trunk Open exists and registers)
shot("s5_rear", 44, 62, EXPLODED,
     [cam(0, -150, 10, 2.0, [-0.35, 1.45, 0.50], 45), cam(0.25, -165, 24, 3.6, [0, 1.80, 0.30], 40),
      cam(0.36, -170, 42, 2.0, [0, 2.00, 0.00], 45), cam(0.47, -172, 44, 1.9, [0, 2.00, -0.03], 45),
      cam(0.58, -160, 14, 1.6, [-0.10, 1.55, 0.40], 45), cam(0.68, -156, 13, 1.5, [-0.10, 1.55, 0.38], 45),
      cam(0.85, -125, 40, 2.8, [0, 1.30, 0.70], 40), cam(1, -118, 46, 2.4, [0, 1.25, 0.68], 40)],
     {"rb": [k(0, spin=0), k(0.11, spin=0), k(0.25, (0, 0.60, -0.50), spin=-40), k(0.36, (0, 0.60, -0.50), spin=-95),
             k(0.47, (0, 0.60, -0.50), spin=-95), k(0.58, R_OUT["rb"]["off"], spin=-95)],
      "trunk": [k(0, deg=0), k(0.68, deg=0), k(0.80, deg=TRUNK_OPEN)], "hood": [k(0, deg=HOOD_OPEN)]},
     visible={"fb": [0, 0], "li": [0, 0], "rb": [0, 0.62]}, light_ref="base")  # rb hidden once it has dropped away (clipped corner in framing v1)

# 6 finale a: rear assembly rises into layers, then the front layers come in (high rear-left crane, not straight down)
shot("x1_layers", 62, 68, EXPLODED,
     [cam(0, 150, 30, 5.6, [0, 1.0, 0.95], 40), cam(1, 140, 40, 10.0, [0, 0.10, 1.05], 40)],
     {"trunk": [k(0, deg=TRUNK_OPEN), k(0.40, LAYERS["trunk"]["off"], deg=0)],
      "rb": [k(0, R_OUT["rb"]["off"], spin=-95), k(0.10, R_OUT["rb"]["off"], spin=-95), k(0.40, (0, 0.75, 1.30), spin=-80),
             k(0.55, LAYERS["rb"]["off"], spin=-80)],
      "hood": [k(0, deg=HOOD_OPEN), k(0.30, deg=HOOD_OPEN), k(0.70, LAYERS["hood"]["off"], deg=0)],
      "fb": [k(0, F_OUT["fb"]["off"], spin=95), k(0.35, F_OUT["fb"]["off"], spin=95), k(0.75, (0, -0.70, 1.20), spin=80),
             k(0.85, LAYERS["fb"]["off"], spin=80)],
      "li": [k(0, F_OUT["li"]["off"]), k(0.45, F_OUT["li"]["off"]), k(0.85, (0, -0.95, 1.60)), k(0.95, LAYERS["li"]["off"])]},
     light_ref="base")

# 7 finale b: layered car -> parts home (outer layers last) -> clean car swaps in on beat 74 -> fade (left-rear 3/4)
_t74 = (ONSET_F[74] - ONSET_F[68]) / (ONSET_F[76] - ONSET_F[68])
shot("x2_reassemble", 68, 76, dict(EXPLODED, car=CAR["car"]),
     [cam(0, 138, 38, 10.0, [0, 0.10, 1.00], 40), cam(0.45, 128, 26, 8.6, [0, 0.05, 0.75], 40),
      cam(1, 122, 10, 5.7, [0, 0.10, 0.52], 40)],
     {"hood": [k(0, **LAYERS["hood"]), k(0.20, lin=True, **DRIFT["hood"]), k(0.45, deg=0)],
      "trunk": [k(0, **LAYERS["trunk"]), k(0.20, lin=True, **DRIFT["trunk"]), k(0.25, **DRIFT["trunk"]), k(0.50, deg=0)],
      "fb": [k(0, **LAYERS["fb"]), k(0.20, lin=True, **DRIFT["fb"]), k(0.30, **DRIFT["fb"]), k(0.50, (0, -0.45, 0), spin=0),
             k(0.62, spin=0)],
      "rb": [k(0, **LAYERS["rb"]), k(0.20, lin=True, **DRIFT["rb"]), k(0.35, **DRIFT["rb"]), k(0.55, (0, 0.45, 0), spin=0),
             k(0.67, spin=0)],
      "li": [k(0, **LAYERS["li"]), k(0.20, lin=True, **DRIFT["li"]), k(0.45, **DRIFT["li"]), k(0.62, (0, -0.55, 0)), k(0.72)]},
     visible={**{p: [0, _t74] for p in list(PARTS) + ["base"]}, "car": [_t74, 1.01]}, light_ref="base")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, d in SHOTS.items():
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
