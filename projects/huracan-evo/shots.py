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
# v3: rear bumper with the scanned licence plate removed (plate x -0.15..0.20, z 0.49..0.68 m, legible in the s9 hero)
EXPLODED_OBJS["rb"] = B + "Rear_Bumper_np.blend"
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


# ---------------------------------------------------------------- v3 (NFSU2 car-lot reference + Temerario detail zooms)
# Music track_a_ext.wav (groove repeated 7 bars): beats t = 0.0768 + 0.60006*n. New shots only; s5-s9 renders are reused
# at their v2 lengths (s8 plays its first 2.4 s).
def KB(n):
    return round(0.0768 + 0.60006 * n, 3)


V3_CUTS = {"c1_lot": (0, 16), "c2_lot": (16, 32), "c3_swap": (32, 36),
           "z1_bumper": (56, 60), "z2_hood": (60, 64), "z3_side": (64, 68), "z4_rear": (68, 72)}
COUPE = {"car": B + "coupe2_np.blend"}       # (plate removed: x -0.17..0.20, z 0.58..0.81 m) 2023 'Huracan Evo Coupe Scan Data (New)' full car, 2 mm (own levelling)
SPYDER = {"car": B + "car2.blend"}           # 2026 set = Spyder (roof step behind the cabin), 2 mm
LOT = {"radius": 3.1, "spot": 3800, "spot_deg": 58, "spot_h": 7.0}  # v3 framing test: disc read as a bright mirror; NFSU2 floor is dark
PARTS2 = {k: B + v + "_2mm.blend" for k, v in PARTS.items()}
PARTS2["rb"] = B + "Rear_Bumper_2mm_np.blend"
EXPLODED2 = {"base": B + "base.blend", **PARTS2}


def v3shot(name, objects, camera, anims=None, extra=None, light_ref=None):
    a, b = V3_CUTS[name]
    d = dict(objects=objects, seconds=round(KB(b) - (KB(a) if a else 0), 3), fps=FPS, res=[1080, 1920], res_pct=75,
             samples=12, camera=camera, out=RENDERS + name, anims=anims or {}, exposure=EXPOSURE,
             hinges={"hood": {"p": HINGE["p"], "axis": HINGE["axis"]}})
    if light_ref:
        d["light_ref"] = light_ref
    d.update(extra or {})
    if anims:
        d["persistent"] = False
    return name, d


def turntable(d0, d1):
    return {"car": [dict(t=0, spin=[d0, 0, 0, 1]), dict(t=1, spin=[d1, 0, 0, 1], lin=True)]}


def hold_expl():
    return {k: [dict(t=0, **EXPL[k])] for k in PARTS}


fb_c, hood_c, side_c, rb_c = [-0.01, -2.24, 1.37], [0.0, -1.62, 2.1], [-1.25, -0.55, 1.05], [0.35, 2.40, 1.12]  # rb_c low/right: diffuser+exhaust, keeps the scanned plate oblique
V3_SHOTS = [
    # car lot: static camera, the car turns on the lit platform; lights come up on 'select' with the start-up
    v3shot("c1_lot", COUPE, [dict(t=0, az=38, el=12, dist=7.0, target=[0, 0, 0.55], lens=45)],
           turntable(-8, 30), extra={"lot": dict(LOT, lights_up=[0.0, 0.07])}),
    v3shot("c2_lot", COUPE, [dict(t=0, az=-28, el=8, dist=6.9, target=[0, 0, 0.6], lens=50),
                             dict(t=1, az=-28, el=8, dist=6.4, target=[0, 0, 0.6], lens=50, lin=True)],
           turntable(30, 75), extra={"lot": LOT}),
    # the lot swaps to the Spyder on the music lift (second start-up), same lot framing as c1
    v3shot("c3_swap", SPYDER, [dict(t=0, az=38, el=12, dist=7.0, target=[0, 0, 0.55], lens=45)],
           turntable(-25, -10), extra={"lot": dict(LOT, lights_up=[0.0, 0.12])}),
    # Temerario-style detail zooms while exploded (2 mm parts), each a push-in with a small orbit
    v3shot("z1_bumper", EXPLODED2, [dict(t=0, az=-24, el=6, dist=3.2, target=fb_c, lens=50),
                                    dict(t=1, az=-4, el=4, dist=2.2, target=fb_c, lens=50)], hold_expl(), light_ref="base"),
    v3shot("z2_hood", EXPLODED2, [dict(t=0, az=-62, el=-20, dist=3.0, target=hood_c, lens=45),
                                  dict(t=1, az=-46, el=-18, dist=2.4, target=hood_c, lens=45)], hold_expl(), light_ref="base"),
    v3shot("z3_side", EXPLODED2, [dict(t=0, az=-98, el=4, dist=3.5, target=side_c, lens=45),
                                  dict(t=1, az=-80, el=6, dist=2.8, target=side_c, lens=45)], hold_expl(), light_ref="base"),
    v3shot("z4_rear", EXPLODED2, [dict(t=0, az=-104, el=-14, dist=2.9, target=rb_c, lens=50),
                                  dict(t=1, az=-96, el=-12, dist=2.3, target=rb_c, lens=50)], hold_expl(), light_ref="base"),
]

if __name__ == "__main__":
    for name, d in V3_SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")


# ---------------------------------------------------------------- v3 HP (user's Hot Pursuit Remastered car-select clip)
# Music track_a_hp.wav: 3 s lead-in, beats t = 3.0768 + 0.60006*n, lift n=64 (41.481), stop n=108 (67.883).
# Coupe section: slow close detail angles in a dark garage, dip to black between angles (ref: ~6.5 s angles, dips).
def KH(n):
    return round(3.0768 + 0.60006 * n, 3)


HP_BEATS = [("h0_select", 0, 3), ("h1_tail", 3, 12), ("h2_front", 12, 21), ("h3_hood", 21, 30), ("h4_wheel", 30, 39),
            ("h5_side", 39, 48), ("h6_high", 48, 57), ("h7_rear", 57, 64)]
GARAGE = {"radius": 14.0, "spot": 2200, "spot_deg": 60, "spot_h": 7.5, "rough": 0.16, "color": [0.0015, 0.0015, 0.002]}  # dark glossy (HP tunnel floor); framing test read as bright grey at rough 0.3


def hpshot(name, a, b, camera, extra=None):
    t0 = 0 if a == 0 else KH(a)
    d = dict(objects=COUPE, seconds=round(KH(b) - t0, 3), fps=FPS, res=[1080, 1920], res_pct=75, samples=12,
             camera=camera, out=RENDERS + name, anims={}, exposure=EXPOSURE, lot=dict(GARAGE))
    d.update(extra or {})
    return name, d


CAMS = {
    "h0_select": [dict(t=0, az=35, el=9, dist=8.6, target=[0, 0, 0.55], lens=45), dict(t=1, az=33, el=9, dist=8.2, target=[0, 0, 0.55], lens=45, lin=True)],   # v3: d 7.4/7.0 cropped the nose (director: whole-car shot needs margins)
    "h1_tail": [dict(t=0, az=150, el=6, dist=2.0, target=[0.55, 2.1, 0.85], lens=50), dict(t=1, az=164, el=6, dist=1.75, target=[0.5, 2.1, 0.85], lens=50, lin=True)],
    "h2_front": [dict(t=0, az=-42, el=2, dist=3.7, target=[0, -1.6, 0.45], lens=40), dict(t=1, az=-26, el=3, dist=3.3, target=[0, -1.6, 0.45], lens=40, lin=True)],
    "h3_hood": [dict(t=0, az=-14, el=37, dist=2.5, target=[0, -1.65, 0.68], lens=60), dict(t=1, az=12, el=35, dist=2.25, target=[0, -1.7, 0.68], lens=60, lin=True)],  # el>=34 keeps the scan-holed windscreen out of the 9:16 frame
    "h4_wheel": [dict(t=0, az=76, el=4, dist=1.7, target=[0.85, -1.35, 0.35], lens=50), dict(t=1, az=60, el=5, dist=1.4, target=[0.85, -1.35, 0.35], lens=50, lin=True)],
    "h5_side": [dict(t=0, az=90, el=3, dist=5.0, target=[0, 1.1, 0.5], lens=40), dict(t=1, az=90, el=3, dist=5.0, target=[0, -1.1, 0.5], lens=40, lin=True)],
    "h6_high": [dict(t=0, az=140, el=40, dist=6.2, target=[0, 0, 0.6], lens=45), dict(t=1, az=124, el=36, dist=6.0, target=[0, 0, 0.6], lens=45, lin=True)],
    "h7_rear": [dict(t=0, az=-150, el=8, dist=7.6, target=[0, 0.2, 0.55], lens=45), dict(t=1, az=-144, el=8, dist=8.6, target=[0, 0.2, 0.55], lens=45, lin=True)],   # v3: d 6.3/7.3 cropped the tail
}
HP_SHOTS = [hpshot(n, a, b, CAMS[n], extra={"lot": dict(GARAGE, lights_up=[0.04, 0.3])} if n == "h0_select" else None)
            for n, a, b in HP_BEATS]

if __name__ == "__main__":
    for name, d in HP_SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")


# ---------------------------------------------------------------- v3 revision per direction.md (v2 brief: travel + section focus)
COUPE = {"car": B + "coupe2_npc.blend"}   # plate + 2 floating debris specks (47 tris above nose/roof) removed
HP_BEATS = [("h0_select", 0, 3), ("h2_front", 3, 17), ("h4_wheel", 17, 32), ("h5_side", 32, 47),
            ("h1_tail", 47, 57), ("h7_rear", 57, 64)]   # h3_hood dropped after tests: blown out under the top light at -1.4 EV,
            # windscreen holes still in frame, and it repeated h2's front - one continuous front sequence instead   # front -> side -> rear; h6_high dropped (roof glass holes, 3rd whole-car 3/4)
CAMS["h3_hood"] = [dict(t=0, az=-14, el=40, dist=2.4, target=[0, -2.05, 0.52], lens=60),
                   dict(t=1, az=12, el=40, dist=2.2, target=[0, -2.05, 0.52], lens=60, lin=True)]   # nose half: shield + intakes, no windscreen
CAMS["h4_wheel"] = [dict(t=0, az=60, el=5, dist=1.7, target=[0.85, -1.35, 0.35], lens=50),
                    dict(t=1, az=76, el=4, dist=1.4, target=[0.85, -1.35, 0.35], lens=50, lin=True)]   # sweeps rearward
CAMS["h5_side"] = [dict(t=0, az=90, el=3, dist=5.0, target=[0, -1.1, 0.5], lens=40),
                   dict(t=1, az=90, el=3, dist=5.0, target=[0, 1.1, 0.5], lens=40, lin=True)]           # slides front -> rear
HP_SHOTS = [hpshot(n, a, b, CAMS[n], extra={"exposure": -1.4} if n == "h3_hood" else None)   # hood under the top light blew out at -0.5
            for n, a, b in HP_BEATS if n not in ("h0_select", "h1_tail")]   # h0/h1 already rendered (h1 stretched 9 -> 10 beats)

# Spyder section shots (n64-108): each part comes off in its own section shot, tips its scanned inner face to the lens
OPEN_DEG = HINGE["open_deg"] * 0.85
Z = [0, 0, 0]
def P(off=Z, spin=0.0, ax=(1, 0, 0), deg=None):
    d = {"off": list(off), "spin": [spin, *ax]}
    if deg is not None:
        d["deg"] = deg
    return d
ST = {}   # running part state, updated shot by shot
ST0 = {k: P() for k in PARTS}
ST0["hood"] = P(deg=0)
OPEN_ST = dict(ST0, fb=P([0, -0.95, -0.02]), fe=P([-0.55, -0.05, 0.02], ax=(0, 1, 0)), hood=P(deg=OPEN_DEG))
S2_END = dict(OPEN_ST, fb=P([0, -1.55, 0.30], 125))
S2_OUT = dict(OPEN_ST, fb=P([0, -1.95, -0.45], 125))   # where S2 leaves it (out of the way, below the nose)
S3_END = dict(S2_OUT, hood=P([0, 0.05, 0.60], deg=HINGE["open_deg"]), tc=P([0, 0, 0.45]), lc=P([-0.22, -0.10, 0.35]),
              rc=P([0.22, -0.10, 0.35]))
S4_END = dict(S3_END, fe=P([-0.95, -0.15, 0.40], -120, (0, 1, 0)), sk=P([-0.55, 0, -0.15], -120, (0, 1, 0)))
S5_END = dict(S4_END, rb=P([0, 1.00, 0.35], -125))
S5_OUT = dict(S4_END, rb=P([0, 1.35, -1.6], -125))   # v3 full render: at z -0.45 it sat in the bottom of the last rear frames
SP_N = {"sp_bumper": (72, 80), "sp_hood": (80, 86), "sp_side": (86, 92), "sp_rear": (92, 98), "sp_finale": (98, 108)}


def moves(a, b, windows, extra=None):
    """keys: every part holds state a, parts in `windows` move a->b between their (t0, t1); extra = additional keys"""
    an = {}
    for k in PARTS:
        if k in windows:
            t0, t1 = windows[k]
            an[k] = [dict(t=0, **a[k]), dict(t=t0, **a[k]), dict(t=t1, **b[k]), dict(t=1, **b[k])]
        else:
            an[k] = [dict(t=0, **a[k])]
    for k, ks in (extra or {}).items():
        an[k] = an[k][:-1] + ks if len(an[k]) > 1 else an[k] + ks
    return an


def spshot(name, camera, anims, objects=EXPLODED2, extra=None):
    a, b = SP_N[name]
    d = dict(objects=objects, seconds=round(KH(b) - KH(a), 3), fps=FPS, res=[1080, 1920], res_pct=75, samples=12,
             camera=camera, out=RENDERS + name, anims=anims, exposure=EXPOSURE, light_ref="base", persistent=False,
             hinges={"hood": {"p": HINGE["p"], "axis": HINGE["axis"]}})
    d.update(extra or {})
    return name, d


SP_SHOTS = [
    # S2 front bumper: forward into clear black, tips its inner face toward the lens (beat = 0.125)
    spshot("sp_bumper", [dict(t=0, az=-45, el=25, dist=3.6, target=[0, -2.70, 0.45], lens=45),
                         dict(t=0.5, az=-48, el=28, dist=3.3, target=[0, -2.85, 0.50], lens=45),
                         dict(t=1, az=-30, el=22, dist=2.3, target=[0, -1.95, 0.45], lens=45)],
           # bumper tips its inner face to the lens (0.125-0.5), then drops forward/down out of the way while the camera
           # moves in and holds on the scanned structure it covered (addendum C: bumper-removed data is the hero beat)
           moves(OPEN_ST, S2_END, {"fb": (0.125, 0.5)}, {"fb": [dict(t=1, off=[0, -1.95, -0.45], spin=[125, 1, 0, 0])]})),
    # S3 under the hood: hood swings full open and lifts, cowls lift straight off (translate only) (beat = 0.167)
    spshot("sp_hood", [dict(t=0, az=-22, el=26, dist=4.4, target=[0, -1.45, 1.25], lens=40),
                       dict(t=1, az=-14, el=32, dist=3.9, target=[0, -1.45, 1.20], lens=40)],   # whole lifted hood in frame
           moves(S2_OUT, S3_END, {"hood": (0.0, 0.5), "tc": (0.333, 0.667), "lc": (0.333, 0.833), "rc": (0.5, 0.833)})),
    # S4 right side: fender then skirt move outboard and tip their inner faces up/out to the lens
    spshot("sp_side", [dict(t=0, az=-102, el=24, dist=5.4, target=[-1.1, -0.55, 0.62], lens=45),
                       dict(t=1, az=-92, el=22, dist=5.1, target=[-1.1, -0.30, 0.55], lens=45)],   # fender clipped at the top at d 4.6   # fender + skirt both in frame
           moves(S3_END, S4_END, {"fe": (0.0, 0.5), "sk": (0.333, 0.833)})),
    # S5 rear bumper: back past the tail onto black, tips its inner face
    spshot("sp_rear", [dict(t=0, az=-140, el=24, dist=4.4, target=[0, 2.35, 0.60], lens=45),
                       dict(t=0.5, az=-135, el=27, dist=3.9, target=[0, 2.75, 0.60], lens=45),
                       dict(t=1, az=-150, el=20, dist=2.4, target=[0, 1.95, 0.55], lens=45)],
           # rear bumper back past the tail, tips its inner face, then drops away; camera moves in on the structure behind
           moves(S4_END, S5_END, {"rb": (0.0, 0.5)}, {"rb": [dict(t=1, off=[0, 1.35, -1.6], spin=[-125, 1, 0, 0])]})),
    # S6 the one full-explode view, then reassembly in reverse travel order, clean car swap on n106 (t=0.8), fade in assembly
    spshot("sp_finale", [dict(t=0, az=-172, el=58, dist=10.5, target=[0, -0.2, 0.70], lens=40),
                         dict(t=0.35, az=-185, el=44, dist=9.0, target=[0, 0.0, 0.65], lens=40, lin=True),
                         dict(t=1, az=-212, el=14, dist=8.2, target=[0, 0.2, 0.55], lens=40)],   # d 6.3 clipped the nose (frames 78-89); length runs up the 9:16 frame (A90 lesson)
           moves(S5_OUT, ST0, {"rb": (0.3, 0.5), "sk": (0.4, 0.6), "fe": (0.4, 0.6), "tc": (0.4, 0.6), "lc": (0.4, 0.6),
                               "rc": (0.4, 0.6), "hood": (0.5, 0.7), "fb": (0.5, 0.75)}),
           objects=dict(EXPLODED2, clean=B + "car2.blend"),
           extra={"visible": dict({k: [0, 0.8] for k in ["base", *PARTS]}, clean=[0.8, 1.01])}),
]

if __name__ == "__main__":
    for name, d in HP_SHOTS + SP_SHOTS:
        json.dump(d, open(OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
