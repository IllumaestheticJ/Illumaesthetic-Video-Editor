"""v3 shot list (direction.md '## v3 direction'): v2.1's travel + one bumper-only explode shot after the front and after
the rear section (inner face -> turn -> its scanned sub-parts come off). v3 geometry (blend3: real tyre bottoms).
  python projects/lamborghini-revuelto/shots_v3.py     # writes /home/user/media/work/revuelto/shots/v3_*.json
Keys are written in absolute music seconds and converted per shot. Each shot renders round(dur*15)+3 frames.
"""
import json
import os

import shots as S

FPS = 15
B = S.M
Z = [0, 0, 0]
CUTS = {"v3_whole": (0.0, 4.6333), "v3_front": (4.6333, 9.3), "v3_fb": (9.3, 13.9667), "v3_side": (13.9667, 16.3333),
        "v3_rear": (16.3333, 21.0), "v3_rb": (21.0, 25.7), "v3_reassemble": (25.7, 30.4)}  # frame cuts 139/279/419/490/630/771/912
HOOD_OPEN = S.HINGE["open_deg"] * 0.85
OFF = {"fb": [0, -0.6, 1.6], "hl": [0, -0.4, 1.9], "fe": [0.35, 0, 0.75], "ssf": [0.60, 0, 0], "ssr": [0.60, 0, 0],
       "fin": [0.45, 0, 0.55], "wing": [0, 0.10, 1.25], "tll": [0.15, 0.20, 1.65], "tlr": [-0.15, 0.20, 1.65], "rb": [0, 0.35, 1.75]}
DRIFT = {k: [v[0] * 1.06, v[1] * 1.06, v[2] * 1.06 + 0.04] for k, v in OFF.items()}
FB_PIECES = {"fb_hl_trim": [0, 0, 0.95], "fb_markers": [0, 0, 0.45], "fb_fog_l": [0, -0.45, 0.22], "fb_fog_r": [0, -0.45, 0.22],
             "fb_fogtrim_l": [0, -0.45, -0.25], "fb_fogtrim_r": [0, -0.45, -0.25], "fb_center_cover": [0, -0.55, 0],
             "fb_center_carbon": [0, -0.55, -0.55], "fb_radar": [0, -0.95, 0.05], "fb_towhook": [0, -0.95, 0.05]}
RB_PIECES = {"rb_diffuser_forced": [0, 0, -0.5], "rb_top_half1": [0, 0, 0.7], "rb_trim_cover": [0, 0.50, 1.25],
             "rb_reflector_l": [0, 0.55, 0.05], "rb_reflector_r": [0, 0.55, 0.05], "rb_corner_marker_l": [0.15, 0, 0.25]}


def nframes(name):
    return round((CUTS[name][1] - CUTS[name][0]) * FPS) + 3


def fr(name, t_abs):
    return round(min(1.0, max(0.0, (t_abs - CUTS[name][0]) / ((nframes(name) - 1) / FPS))), 4)


def keys(name, pts):
    """pts: [(t_abs, {fields}), ...] -> shot.py keys with shot fractions"""
    return [dict(t=fr(name, t), **d) for t, d in pts]


def blend(objs):
    return {k: B + v + ".blend" for k, v in objs.items()}


def shot(name, objects, camera, anims=None, visible=None, light_ref=None):
    n = nframes(name)
    d = dict(objects=objects, seconds=round(n / FPS, 4), fps=FPS, res=[1080, 1920], res_pct=75, samples=12,
             camera=keys(name, camera), out=S.RENDERS + name, anims=anims or {}, exposure=S.EXPOSURE,
             hinges={"hood": {"p": S.HINGE["p"], "axis": S.HINGE["axis"]}},
             light_ref=light_ref or ("base" if "base" in objects else "car"), persistent=False)
    if visible:
        d["visible"] = {k: [fr(name, a) if a is not None else 0, fr(name, b) if b is not None else 1.01] for k, (a, b) in visible.items()}
        for k, (a, b) in visible.items():
            if a is None and b is None:
                d["visible"][k] = [0, 0]  # loaded for the light rig only, never rendered
            elif b is None:
                d["visible"][k][1] = 1.01
    return name, d


def cam(az, el, dist, target, lin=False):
    return dict(az=az, el=el, dist=dist, target=target, lens=40, **({"lin": True} if lin else {}))


def held(state):
    return [dict(t=0, **state)]


ALL = S.EXPLODED_OBJS
n, SHOTS = None, []

# 1 whole car, front-left 3/4, slow push (v2.1 move in 8 beats); round tyres in frame
n = "v3_whole"
SHOTS.append(shot(n, S.CAR, [(0, cam(50, 7, 7.1, [0, 0.10, 0.46])), (4.6333, cam(36, 10, 6.5, [0, -0.15, 0.46], lin=True))]))

# 2 front: bumper slides off the nose then lifts away, headlights out, lid up on its hinge, push in on the structure
n = "v3_front"
SHOTS.append(shot(n, S.WITH_CAR,
    [(4.6333, cam(36, 13, 5.2, [0, -1.7, 0.75])), (6.96, cam(24, 18, 5.0, [0, -1.8, 0.65], lin=True)),
     (8.13, cam(12, 14, 2.4, [0, -2.10, 0.36])), (9.3, cam(6, 13, 2.2, [0, -2.12, 0.34], lin=True))],
    {"fb": keys(n, [(4.6333, {"off": Z}), (4.70, {"off": Z}), (5.79, {"off": [0, -0.60, 0.12]}), (6.96, {"off": OFF["fb"]})]),
     "hl": keys(n, [(4.6333, {"off": Z}), (5.20, {"off": Z}), (5.79, {"off": [0, -0.30, 0.25]}), (6.96, {"off": OFF["hl"]})]),
     "hood": keys(n, [(4.6333, {"off": Z, "deg": 0}), (5.79, {"off": Z, "deg": 0}), (7.20, {"off": Z, "deg": HOOD_OPEN})])},
    visible={"car": (4.6333, 4.70), "base": (4.70, None)}))

# 3 the front bumper alone: inner face (brackets, ducts) -> turns to its outer face -> its 10 scanned pieces come off
n = "v3_fb"
objs = blend({"car": "car_3mm", "fbA": "front_bumper", "fb_stripped": "fb_stripped", **{k: k for k in FB_PIECES}})
an = {"fbA": keys(n, [(9.3, {"spin": [180, 0, 0, 1]}), (10.471, {"spin": [162, 0, 0, 1], "lin": True}), (11.642, {"spin": [0, 0, 0, 1]})])}
for i, (k, off) in enumerate(FB_PIECES.items()):
    st = 11.642 + 0.08 * (i // 3)
    an[k] = keys(n, [(9.3, {"off": Z}), (st, {"off": Z}), (st + 1.1, {"off": off})])
vis = {"car": (None, None), "fbA": (9.3, 11.642), "fb_stripped": (11.642, None), **{k: (11.642, None) for k in FB_PIECES}}
SHOTS.append(shot(n, objs, [(9.3, cam(8, 16, 3.8, [0, -1.98, 0.28])), (11.642, cam(11, 30, 4.1, [0, -2.15, 0.30])),
                            (13.9667, cam(14, 30, 3.95, [0, -2.15, 0.30], lin=True))], an, vis, light_ref="car"))

# 4 left side: fender lifts, skirts slide out, fin lifts; one continuous track
n = "v3_side"
side_objs = {k: v for k, v in ALL.items() if k not in ("fb", "hl")}  # front parts are parked out of frame: not loaded
SHOTS.append(shot(n, side_objs, [(13.9667, cam(62, 20, 4.0, [0.85, -1.25, 0.48])), (16.3333, cam(96, 16, 5.2, [0.90, 0.10, 0.38]))],
    {"hood": held({"off": Z, "deg": HOOD_OPEN}),
     "fe": keys(n, [(13.9667, {"off": Z}), (14.05, {"off": Z}), (14.75, {"off": OFF["fe"]})]),
     "ssf": keys(n, [(13.9667, {"off": Z}), (14.75, {"off": Z}), (15.45, {"off": OFF["ssf"]})]),
     "ssr": keys(n, [(13.9667, {"off": Z}), (14.75, {"off": Z}), (15.45, {"off": OFF["ssr"]})]),
     "fin": keys(n, [(13.9667, {"off": Z}), (14.95, {"off": Z}), (15.65, {"off": OFF["fin"]})])}))

# 5 rear: wing, tail lights, rear bumper lift away (bumper clear on phrase C 18.665), surge in on the rear structure
n = "v3_rear"
rear_objs = {k: v for k, v in ALL.items() if k not in ("fb", "hl")}
SHOTS.append(shot(n, rear_objs,
    [(16.3333, cam(145, 14, 6.4, [0, 1.5, 0.70])), (18.665, cam(148, 14, 6.2, [0, 1.55, 0.70], lin=True)),
     (19.835, cam(162, 12, 2.8, [0, 2.20, 0.56])), (21.0, cam(168, 12, 2.6, [0, 2.22, 0.55], lin=True))],
    {"hood": held({"off": Z, "deg": HOOD_OPEN}), **{k: held({"off": OFF[k]}) for k in ("fe", "ssf", "ssr", "fin")},
     "wing": keys(n, [(16.3333, {"off": Z}), (16.40, {"off": Z}), (17.20, {"off": OFF["wing"]})]),
     "tll": keys(n, [(16.3333, {"off": Z}), (16.90, {"off": Z}), (17.49, {"off": OFF["tll"]})]),
     "tlr": keys(n, [(16.3333, {"off": Z}), (16.90, {"off": Z}), (17.49, {"off": OFF["tlr"]})]),
     "rb": keys(n, [(16.3333, {"off": Z}), (17.494, {"off": Z}), (18.665, {"off": OFF["rb"]})])}))

# 6 the rear bumper alone: inner face (wiring loom, brackets) -> outer face -> diffuser / upper half / small parts separate
n = "v3_rb"
objs = blend({"car": "car_3mm", "rbA": "rear_bumper_forced", **{k: k for k in RB_PIECES}})
an = {"rbA": keys(n, [(21.0, {"spin": [180, 0, 0, 1]}), (22.176, {"spin": [162, 0, 0, 1], "lin": True}), (23.347, {"spin": [0, 0, 0, 1]})])}
for i, (k, off) in enumerate(RB_PIECES.items()):
    st = 23.347 + 0.08 * (i // 2)
    an[k] = keys(n, [(21.0, {"off": Z}), (st, {"off": Z}), (st + 1.1, {"off": off})])
vis = {"car": (None, None), "rbA": (21.0, 23.347), **{k: (23.347, None) for k in RB_PIECES}}
SHOTS.append(shot(n, objs, [(21.0, cam(172, 16, 3.8, [0.02, 2.02, 0.36])), (23.347, cam(169, 30, 3.9, [0.02, 2.15, 0.45])),
                            (25.7, cam(166, 30, 3.75, [0.02, 2.15, 0.45], lin=True))], an, vis, light_ref="car"))

# 7 everything home: parts slam in (ease-in) on the climax attack, lid closes, base -> car on the lock frame; hero push
n = "v3_reassemble"
LOCK = 27.94
movers = ["hood", "hl", "wing", "tll", "tlr", "fe", "fin", "fb", "ssf", "ssr", "rb"]
an = {}
for i, k in enumerate(movers):
    st = 25.7 + 0.1 * i
    a = {"off": Z, "deg": HOOD_OPEN} if k == "hood" else {"off": DRIFT[k]}
    h = {"off": Z, "deg": 0} if k == "hood" else {"off": Z}
    an[k] = keys(n, [(25.7, a), (st, a), (LOCK, dict(h, ease="in"))])
SHOTS.append(shot(n, S.WITH_CAR, [(25.7, cam(128, 16, 9.6, [0, 0.3, 1.4])), (LOCK, cam(146, 9, 7.6, [0, 0.15, 0.46])),
                                  (30.4, cam(158, 7, 6.6, [0, 0.2, 0.42], lin=True))], an,
                  visible={"base": (25.7, LOCK), "car": (LOCK, None)}))

if __name__ == "__main__":
    os.makedirs(S.OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(S.OUT + name + ".json", "w"), indent=1)
        print(name, CUTS[name], round(d["seconds"] * FPS), "frames")
