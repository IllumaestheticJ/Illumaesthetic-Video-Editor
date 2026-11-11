"""v2 shot list (direction.md, scene director + director): front -> left side -> rear sections, each part leaves into
clear black and the camera moves in on the structure each state scan exposes; mirror never moves (no mirror-removed
scan, rule D); the lid only swings on its fitted hinge (only a Hood Open scan exists, rule D).
  python projects/lamborghini-revuelto/shots_v2.py      # writes /home/user/media/work/revuelto/shots/v2_*.json
Each new shot renders round(dur*15)+3 frames (lesson: minterpolate eats the tail) - assembled with exact frame counts.
"""
import json
import os

import shots as S  # helpers, parts, hinge, CAR / EXPLODED_OBJS / WITH_CAR from v1

FPS = 15
PARTS = S.PARTS
MOVERS = [k for k in PARTS if k != "mir"]
Z = [0, 0, 0]
HOOD_OPEN = S.HINGE["open_deg"] * 0.85
HOME = {k: {"off": Z} for k in PARTS}
HOME["hood"] = {"off": Z, "deg": 0}
OPEN = dict(S.OPEN)  # v1 s6 end state: fb/hl out at the nose, lid up
# OFF: where each part waits once its section is done - clear black, translations only, never across the body
OFF = dict(HOME, fb={"off": [0, -0.6, 1.6]}, hl={"off": [0, -0.4, 1.9]}, hood={"off": Z, "deg": HOOD_OPEN},
           fe={"off": [0.35, 0, 0.75]}, ssf={"off": [0.60, 0, 0]}, ssr={"off": [0.60, 0, 0]}, fin={"off": [0.45, 0, 0.55]},
           wing={"off": [0, 0.10, 1.25]}, tll={"off": [0.15, 0.20, 1.65]}, tlr={"off": [-0.15, 0.20, 1.65]},
           rb={"off": [0, 0.35, 1.75]})
DRIFT = {k: (dict(v, off=[v["off"][0] * 1.06, v["off"][1] * 1.06, v["off"][2] * 1.06 + 0.04]) if k in MOVERS and k != "hood" else v)
         for k, v in OFF.items()}

DUR = {"v2_whole": 6.96, "v2_frontin": 4.6833, "v2_side": 3.5, "v2_rear": 7.0333, "v2_reassemble": 4.7}


def state_after(section):
    """pose of every part at the start of a section"""
    st = dict(HOME)
    if section in ("side", "rear", "reassemble"):
        st.update({k: OFF[k] for k in ("fb", "hl", "hood")})
    if section in ("rear", "reassemble"):
        st.update({k: OFF[k] for k in ("fe", "ssf", "ssr", "fin")})
    if section == "reassemble":
        st.update({k: DRIFT[k] for k in ("wing", "tll", "tlr", "rb")})
        st.update({k: DRIFT[k] for k in ("fb", "hl", "fe", "ssf", "ssr", "fin")})
    return st


def moves(start, windows, end):
    """keys: every part holds `start`, parts in `windows` move to `end` over (t0, t1)"""
    out = {}
    for k in PARTS:
        if k in windows:
            t0, t1 = windows[k][:2]
            ease = windows[k][2] if len(windows[k]) > 2 else None
            e = dict(t=t1, **end[k]); e.update({"ease": ease} if ease else {})
            out[k] = [dict(t=0, **start[k]), dict(t=t0, **start[k]), e, dict(t=1, **end[k])]
        else:
            out[k] = [dict(t=0, **start[k])]
    return out


def shot(name, objects, camera, anims=None, visible=None, extra_frames=3):
    n = round(DUR[name] * FPS) + extra_frames
    d = dict(objects=objects, seconds=round((n - 1) / FPS + 1 / FPS, 4), fps=FPS, res=[1080, 1920], res_pct=75,
             samples=12, camera=camera, out=S.RENDERS + name, anims=anims or {}, exposure=S.EXPOSURE,
             hinges={"hood": {"p": S.HINGE["p"], "axis": S.HINGE["axis"]}},
             light_ref="base" if "base" in objects else "car", persistent=False)
    if visible:
        d["visible"] = visible
    return name, d


def frac(t_abs, t0, name, extra_frames=3):
    """shot fraction of an absolute time; shot.py maps t over (n-1) frame steps"""
    n = round(DUR[name] * FPS) + extra_frames
    return round((t_abs - t0) / ((n - 1) / FPS), 4)


LOCK = frac(27.94, 25.687, "v2_reassemble")  # parts land on the climax taiko attack (27.93)
SHOTS = [
    # 1 whole car front-left 3/4, slow push + drift toward the front (no turntable); ends near s6's first pose
    shot("v2_whole", S.CAR, [dict(t=0, az=50, el=7, dist=7.1, target=[0, 0.1, 0.55], lens=40),
                             dict(t=1, az=36, el=10, dist=6.5, target=[0, -0.15, 0.55], lens=40, lin=True)]),
    # 3 front structure: fb + hl lift away from OPEN to OFF, camera moves in on what the bumper hid; lid stays open
    shot("v2_frontin", S.EXPLODED_OBJS,
         [dict(t=0, az=24, el=18, dist=5.0, target=[0, -1.8, 0.65], lens=40),
          dict(t=0.625, az=12, el=14, dist=2.4, target=[0, -2.1, 0.42], lens=40),
          dict(t=1, az=6, el=13, dist=2.2, target=[0, -2.12, 0.40], lens=40, lin=True)],
         moves(dict(HOME, fb=OPEN["fb"], hl=OPEN["hl"], hood=OFF["hood"]), {"fb": (0, 0.25), "hl": (0.03, 0.25)}, OFF)),
    # 4 left side: fender lifts, then skirts slide out and the fin lifts; lateral track along the side
    shot("v2_side", S.EXPLODED_OBJS,
         [dict(t=0, az=62, el=20, dist=4.0, target=[0.85, -1.25, 0.55], lens=40),
          dict(t=0.40, az=62, el=20, dist=4.0, target=[0.85, -1.25, 0.55], lens=40),
          dict(t=1, az=96, el=16, dist=5.2, target=[0.90, 0.10, 0.45], lens=40)],
         moves(state_after("side"), {"fe": (0.04, 0.30), "ssf": (0.50, 0.75), "ssr": (0.50, 0.75), "fin": (0.58, 0.83)}, OFF)),
    # 5 rear (phrase C, richest region): wing, tail lights, rear bumper lift straight up; push in on the rear structure
    shot("v2_rear", S.EXPLODED_OBJS,
         [dict(t=0, az=145, el=14, dist=6.4, target=[0, 1.5, 0.75], lens=40),
          dict(t=0.417, az=148, el=14, dist=6.2, target=[0, 1.55, 0.75], lens=40),
          dict(t=0.75, az=162, el=12, dist=2.6, target=[0, 2.2, 0.50], lens=40),
          dict(t=1, az=168, el=12, dist=2.4, target=[0, 2.22, 0.48], lens=40, lin=True)],
         moves(state_after("rear"), {"wing": (0.0, 0.167), "tll": (0.167, 0.25), "tlr": (0.167, 0.25), "rb": (0.25, 0.417)}, OFF)),
    # 6 everything home, slams in (ease-in) on the climax attack, lid closes on its hinge; rear 3/4 hero (v1 s10 keys)
    shot("v2_reassemble", S.WITH_CAR,
         [dict(t=0, az=128, el=16, dist=9.6, target=[0, 0.3, 1.4], lens=40),
          dict(t=LOCK, az=146, el=9, dist=7.6, target=[0, 0.15, 0.55], lens=40),
          dict(t=1, az=158, el=7, dist=6.6, target=[0, 0.2, 0.5], lens=40, lin=True)],
         moves(state_after("reassemble"), {k: (st, LOCK, "in") for k, st in
                                           zip(MOVERS, [0.0, 0.02, 0.03, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2])}, HOME),
         visible={"base": [0, LOCK], "car": [LOCK, 1.01]}),
]

if __name__ == "__main__":
    os.makedirs(S.OUT, exist_ok=True)
    for name, d in SHOTS:
        json.dump(d, open(S.OUT + name + ".json", "w"), indent=1)
        print(name, d["seconds"], "s", round(d["seconds"] * FPS), "frames")
