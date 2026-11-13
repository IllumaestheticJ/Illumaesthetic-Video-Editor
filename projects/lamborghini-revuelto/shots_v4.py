"""v4 shot list (user on v3: add the rear-wing-removed section; rear bumper clipped the tail lights and wing on its way
off; exhaust sections after the bumper; parts must stay on screen while they come off; new song 'Sector Shift').
Music edit: 140 BPM, bar = 1.714291 s, reel t(bar) = 3.428582 + 1.714291*bar (bar 0 = first drop, bar 20 = second drop).
Every removal is a WIDE where the parts end inside the frame, then a hard cut to a close shot of what they exposed
(parts not loaded there: fully out, never clipped at the edge).
  python projects/lamborghini-revuelto/shots_v4.py     # writes /home/user/media/work/revuelto/shots/v4_*.json
Reused renders: v3_whole, v3_fb, v3_rb (re-timed with src_fps in project.yaml).
"""
import json
import os

import shots as S

B = S.M
BAR = 1.714291
T = lambda bar: 3.428582 + BAR * bar
KICK = BAR / 4
Z = [0, 0, 0]
HOOD_OPEN = S.HINGE["open_deg"] * 0.85
# cut frames (30 fps) on bar lines
FR = {"v4_front": (103, 206), "v4_frontin": (206, 309), "v4_side": (463, 566), "v4_wing": (566, 617), "v4_wingin": (617, 669), "v4_rear": (669, 771),
      "v4_exh": (771, 926), "v4_reassemble": (1080, 1234)}
FPS = {"v4_exh": 30}  # state swaps: native 30 fps (minterpolate would ghost the swap frame)
# parked poses: inside the wide frames, clear of each other (tools/pathcheck.py)
OFF = {"fb": [0, -0.75, 1.75], "hl": [0, -0.35, 2.15], "fe": [0.30, 0, 0.55], "ssf": [0.50, 0, 0], "ssr": [0.50, 0, 0],
       "fin": [0.40, 0, 0.45], "wing": [0, -0.10, 0.60], "tll": [0.55, 0, 0.80], "tlr": [-0.55, 0, 0.80],
       "rb": [0, 0.95, 1.75]}
VIA = {"fb": [0, -0.75, 0.05], "rb": [0, 0.95, 0.0], "hl": [0, -0.35, 0.03], "tll": [0.05, 0.28, 0.0], "tlr": [-0.05, 0.28, 0.0]}  # bumpers slide off along the car first, then rise
EX = {"ex_tips": [0, 0.15, 0.95], "ex_catback": [0, 1.05, -0.05], "ex_cat_lh": [0.03, 0.05, 0.50], "ex_cat_rh": [-0.03, 0.05, 0.50]}


def fps(name):
    return FPS.get(name, 15)


def nframes(name):
    f = FR[name][1] - FR[name][0]
    return f if fps(name) == 30 else (f + 3 + 1) // 2 + 1


def fr(name, t_abs):
    return round(min(1.0, max(0.0, (t_abs - FR[name][0] / 30) / ((nframes(name) - 1) / fps(name)))), 4)


def keys(name, pts):
    return [dict(t=fr(name, t), **d) for t, d in pts]


def shot(name, objects, camera, anims=None, visible=None, light_ref=None):
    n = nframes(name)
    d = dict(objects=objects, seconds=round(n / fps(name), 4), fps=fps(name), res=[1080, 1920], res_pct=75, samples=12,
             camera=keys(name, camera), out=S.RENDERS + name, anims=anims or {}, exposure=S.EXPOSURE,
             hinges={"hood": {"p": S.HINGE["p"], "axis": S.HINGE["axis"]}},
             light_ref=light_ref or ("base" if "base" in objects else "car"), persistent=False)
    if visible:
        d["visible"] = {}
        for k, (a, b) in visible.items():
            d["visible"][k] = [0, 0] if a is None and b is None else [(fr(name, a) if fr(name, a) > 0.01 else 0) if a is not None else 0, fr(name, b) if b is not None else 1.01]
    return name, d


def cam(az, el, dist, target, lin=False):
    return dict(az=az, el=el, dist=dist, target=target, lens=40, **({"lin": True} if lin else {}))


def held(state):
    return [dict(t=0, **state)]


def blend(objs):
    return {k: B + v + ".blend" for k, v in objs.items()}


ALL = S.EXPLODED_OBJS
SHOTS = []

# front (bars 0-2): bumper slides off the nose on the drop, rises; headlights follow; lid swings up. Everything ends in frame.
n = "v4_front"; t0 = T(0)
SHOTS.append(shot(n, S.WITH_CAR, [(t0, cam(34, 9, 7.1, [0, -1.2, 1.35])), (T(2), cam(26, 10, 6.9, [0, -1.3, 1.35], lin=True))],
    {"fb": keys(n, [(t0, {"off": Z}), (t0 + 0.07, {"off": Z}), (t0 + 2 * KICK, {"off": VIA["fb"]}), (t0 + 4 * KICK, {"off": OFF["fb"]})]),
     "hl": keys(n, [(t0, {"off": Z}), (t0 + 2 * KICK, {"off": Z}), (t0 + 3 * KICK, {"off": VIA["hl"]}), (t0 + 4.5 * KICK, {"off": OFF["hl"]})]),
     "hood": keys(n, [(t0, {"off": Z, "deg": 0}), (t0 + 4 * KICK, {"off": Z, "deg": 0}), (t0 + 7 * KICK, {"off": Z, "deg": HOOD_OPEN})])},
    visible={"car": (t0, t0 + 0.07), "base": (t0 + 0.07, None)}))

# front structure (bars 2-4): close on what the bumper hid; bumper and headlights are not in this shot
n = "v4_frontin"
objs = {k: v for k, v in ALL.items() if k not in ("fb", "hl")}
SHOTS.append(shot(n, objs, [(T(2), cam(16, 15, 3.6, [0.12, -2.05, 0.45])), (T(4), cam(6, 13, 2.9, [0.05, -2.12, 0.40], lin=True))],
                  {"hood": held({"off": Z, "deg": HOOD_OPEN})}))

# left side (bars 7-9): fender lifts, skirts slide out, fin lifts; wide enough that all four stay in frame
n = "v4_side"; t0 = T(7)
SHOTS.append(shot(n, objs, [(t0, cam(72, 14, 8.4, [0.4, -0.25, 0.6])), (T(9), cam(86, 12, 8.1, [0.4, -0.15, 0.6], lin=True))],
    {"hood": held({"off": Z, "deg": HOOD_OPEN}),
     "fe": keys(n, [(t0, {"off": Z}), (t0 + 0.07, {"off": Z}), (t0 + 2 * KICK, {"off": OFF["fe"]})]),
     "ssf": keys(n, [(t0, {"off": Z}), (t0 + 2 * KICK, {"off": Z}), (t0 + 4 * KICK, {"off": OFF["ssf"]})]),
     "ssr": keys(n, [(t0, {"off": Z}), (t0 + 2 * KICK, {"off": Z}), (t0 + 4 * KICK, {"off": OFF["ssr"]})]),
     "fin": keys(n, [(t0, {"off": Z}), (t0 + 4 * KICK, {"off": Z}), (t0 + 6 * KICK, {"off": OFF["fin"]})])}))

# rear wing removed (bars 9-11): wing lifts straight off its mounts, camera moves in on the deck and mounts it exposes
n = "v4_wing"; t0 = T(9)
robjs = {k: v for k, v in ALL.items() if k in ("base", "hood", "wing", "tll", "tlr", "rb", "mir")}
SHOTS.append(shot(n, robjs, [(t0, cam(150, 18, 6.6, [0, 1.6, 1.0])), (T(10), cam(155, 20, 6.2, [0, 1.7, 1.0], lin=True))],
    {"hood": held({"off": Z, "deg": HOOD_OPEN}),
     "wing": keys(n, [(t0, {"off": Z}), (t0 + 0.07, {"off": Z}), (t0 + 3 * KICK, {"off": OFF["wing"]})])}))
# close on the deck the wing sat on (wing not in this shot)
n = "v4_wingin"
nowing = {k: v for k, v in robjs.items() if k != "wing"}
SHOTS.append(shot(n, nowing, [(T(10), cam(160, 30, 3.0, [0, 2.15, 0.80])), (T(11), cam(168, 34, 2.6, [0, 2.2, 0.80], lin=True))],
                  {"hood": held({"off": Z, "deg": HOOD_OPEN})}))

# rear (bars 11-13): tail lights out to the sides, bumper slides straight back then rises clear of lights and wing
n = "v4_rear"; t0 = T(11)
SHOTS.append(shot(n, nowing, [(t0, cam(148, 13, 8.2, [0, 1.6, 1.25])), (T(13), cam(156, 14, 7.9, [0, 1.7, 1.25], lin=True))],
    {"hood": held({"off": Z, "deg": HOOD_OPEN}),
     "tll": keys(n, [(t0, {"off": Z}), (t0 + 0.07, {"off": Z}), (t0 + 1 * KICK, {"off": VIA["tll"]}), (t0 + 2 * KICK, {"off": OFF["tll"]})]),
     "tlr": keys(n, [(t0, {"off": Z}), (t0 + 0.07, {"off": Z}), (t0 + 1 * KICK, {"off": VIA["tlr"]}), (t0 + 2 * KICK, {"off": OFF["tlr"]})]),
     "rb": keys(n, [(t0, {"off": Z}), (t0 + 2 * KICK, {"off": Z}), (t0 + 4 * KICK, {"off": VIA["rb"]}), (t0 + 6 * KICK, {"off": OFF["rb"]})])}))

# exhaust (bars 13-16), after the bumper: the bumper-off state as scanned -> tip assembly and catback come off (state swap
# to 'Engine Bay Cats On') -> both cats come out (swap to 'Engine Bay No Exhaust'). Each state scan shown alone, as captured.
n = "v4_exh"; t0 = T(13); s2 = T(13) + 2 * KICK; s3 = T(15)  # kicks: 0-2 Exhaust On, 2-3 tips, 3-5 catback, hold, 8-9.5 cats, hold
objs = blend({"s1": "st_eb_exhaust_on_c", "s2": "st_eb_cats_on_c", "s3": "st_eb_no_exhaust_c", **{k: k for k in EX}})
SHOTS.append(shot(n, objs, [(t0, cam(168, 20, 3.0, [0.03, 2.1, 0.55])), (s2 + 3 * KICK, cam(164, 28, 4.5, [0.03, 2.45, 0.80])), (T(16), cam(158, 31, 4.4, [0.03, 2.4, 0.80], lin=True))],
    {"ex_tips": keys(n, [(t0, {"off": Z}), (s2, {"off": Z}), (s2 + 1 * KICK, {"off": EX["ex_tips"]})]),
     "ex_catback": keys(n, [(t0, {"off": Z}), (s2 + 1 * KICK, {"off": Z}), (s2 + 3 * KICK, {"off": EX["ex_catback"]})]),
     "ex_cat_lh": keys(n, [(t0, {"off": Z}), (s3, {"off": Z}), (s3 + 1.5 * KICK, {"off": EX["ex_cat_lh"]})]),
     "ex_cat_rh": keys(n, [(t0, {"off": Z}), (s3, {"off": Z}), (s3 + 1.5 * KICK, {"off": EX["ex_cat_rh"]})])},
    visible={"s1": (t0, s2), "s2": (s2, s3), "s3": (s3, None), "ex_tips": (s2, None), "ex_catback": (s2, None),
             "ex_cat_lh": (s3, None), "ex_cat_rh": (s3, None)}, light_ref="s1"))

# reassemble (bars 18-22): every part flies home through the fill and locks ON the second drop (bar 20); hero push; fade
n = "v4_reassemble"; t0 = T(19); LOCK = T(20)
movers = ["hood", "hl", "wing", "tll", "tlr", "fe", "fin", "fb", "ssf", "ssr", "rb"]
an = {}
for i, k in enumerate(movers):
    st = t0 + 0.05 * i
    a = {"off": Z, "deg": HOOD_OPEN} if k == "hood" else {"off": OFF[k]}
    h = {"off": Z, "deg": 0} if k == "hood" else {"off": Z}
    pts = [(t0, a), (st, a)]
    if k in VIA:
        pts.append((st + (LOCK - st) * 0.55, {"off": VIA[k]}))
    an[k] = keys(n, pts + [(LOCK, dict(h, ease="in"))])
SHOTS.append(shot(n, S.WITH_CAR, [(t0, cam(124, 13, 12.5, [0, 0.4, 1.2])), (LOCK - 0.3, cam(134, 12, 11.8, [0, 0.35, 1.15])), (LOCK, cam(146, 9, 9.2, [0, 0.15, 0.6])),
                                  (T(22), cam(158, 7, 6.6, [0, 0.2, 0.42], lin=True))], an,
                  visible={"base": (t0, LOCK), "car": (LOCK, None)}))

if __name__ == "__main__":
    os.makedirs(S.OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(S.OUT + name + ".json", "w"), indent=1)
        print(name, FR[name], d["fps"], "fps", round(d["seconds"] * d["fps"]), "frames")
