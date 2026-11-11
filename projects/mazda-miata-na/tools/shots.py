"""Shot specs for the Mazda Miata NA Temerario-style reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/mazda-miata-na/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (prepped, metres; see editlog): nose at -Y, car's right = -X, ground Z=0, centre x ~ 0.
Bumper tip y=-1.97, tail y=+1.97, width 1.79 m incl. mirrors, height 1.24 m (hardtop).
Durations (SECS) come from the music's accent grid (project.yaml); all moves start on frame 1.
"""
import json
import math
import os
import sys

P = "/home/user/media/mazda-miata-na/prep"
OUT = "/home/user/media/work/miata/renders"
SPECS = "/home/user/media/work/miata/specs"
TIMING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "timing.json")
TIM = json.load(open(TIMING)) if os.path.exists(TIMING) else {}
SECS = dict(TIM.get("secs", {}), **{k: v for k, v in TIM.items() if k.startswith("x_")})
BEAT = json.load(open(TIMING))["beat"] if os.path.exists(TIMING) else 0.6

CAR = f"{P}/car4.blend"      # 4 mm: full-car moves
FR2 = f"{P}/fr2.blend"       # 2 mm front-right quarter: wheel close-up
REAR2 = f"{P}/rear2.blend"   # 2 mm rear half: tail-lamp close-up
HH = json.load(open("/home/user/media/mazda-miata-na/reg/hinge_hood.json"))    # tools/hinge.py
HT = json.load(open("/home/user/media/mazda-miata-na/reg/hinge_trunk.json"))


def orbit(t, r, ang_deg, h, c=(0, 0, 0.5), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def S(n, default):
    return SECS.get(n, default)


def shots():
    sh = {}
    d = S("s1_turntable", 5.0)
    sh["s1_turntable"] = {"base": [CAR], "cam": [orbit(0, 4.8, -28, 0.85, c=(0, -0.25, 0.5), focal=30, ease="lin", tz=0.45),
                                                orbit(d, 4.5, -55, 0.95, c=(0, -0.25, 0.5), focal=30, ease="out2", tz=0.45)]}
    d = S("s2_rear", 4.6)
    sh["s2_rear"] = {"base": [CAR], "cam": [orbit(0, 4.7, 152, 0.75, c=(0, 0.3, 0.5), focal=30, ease="lin", tz=0.5),
                                           orbit(d, 4.4, 128, 1.25, c=(0, 0.3, 0.5), focal=30, ease="out2", tz=0.5)]}
    d = S("s3_wheel", 2.4)
    sh["s3_wheel"] = {"base": [FR2], "cam": [
        {"t": 0, "loc": [-1.95, -0.75, 0.38], "target": [-0.75, -1.25, 0.30], "focal": 40},
        {"t": d, "loc": [-1.93, -1.05, 0.37], "target": [-0.75, -1.30, 0.30], "focal": 40, "ease": "out2"}]}
    d = S("s4_lamp", 2.4)
    sh["s4_lamp"] = {"base": [REAR2], "cam": [
        {"t": 0, "loc": [-1.55, 2.95, 0.85], "target": [-0.45, 1.85, 0.62], "focal": 40},
        {"t": d, "loc": [-1.15, 3.1, 0.83], "target": [-0.38, 1.87, 0.61], "focal": 40, "ease": "out2"}]}
    d = S("s7_top", 2.4)
    sh["s7_top"] = {"base": [CAR], "cam": [
        {"t": 0, "loc": [1.9, 3.9, 3.5], "target": [0, 0.3, 0.45], "focal": 30},
        {"t": d, "loc": [0.0, 0.2, 6.2], "target": [0, 0.0, 0.45], "focal": 30, "ease": "inout"}]}
    # 5. hood opens on its fitted cowl hinge to the captured angle; engine bay from 'Front End Hood Open'.
    # Camera on the car's right: the captured hood underside (ribs) covers the right 2/3 of the lid.
    d = S("s5_hood", 3.6)
    sh["s5_hood"] = {"base": [f"{P}/comp_hood.blend"],
                     "parts": [{"blend": f"{P}/hood_full.blend", "pivot": HH["p"],
                                "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                         {"t": 0.5 * BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                         {"t": min(d - 0.3, 3.5 * BEAT), "loc": [0, 0, 0], "rot": [HH["open_deg"], 0, 0], "ease": "inout"}]}],
                     "cam": [orbit(0, 4.0, -38, 2.0, c=(0, -0.9, 0.5), focal=30, ease="lin", tz=0.55),
                             orbit(d, 3.5, -22, 2.3, c=(0, -1.0, 0.5), focal=30, ease="out2", tz=0.55)]}
    # 6. trunk: closed -> half open (37.5 deg, the 'NA Trunk Half Open' capture) -> pause -> open (55.6 deg, 'NA Trunk Open')
    d = S("s6_trunk", 3.6)
    sh["s6_trunk"] = {"base": [f"{P}/comp_trunk.blend"],
                      "parts": [{"blend": f"{P}/trunk_full.blend", "pivot": HT["p"],
                                 "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                          {"t": 0.5 * BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                          {"t": 1.5 * BEAT, "loc": [0, 0, 0], "rot": [HT["half_deg"], 0, 0], "ease": "inout"},
                                          {"t": 2.5 * BEAT, "loc": [0, 0, 0], "rot": [HT["half_deg"], 0, 0], "ease": "lin"},
                                          {"t": min(d - 0.3, 3.5 * BEAT), "loc": [0, 0, 0], "rot": [HT["open_deg"], 0, 0], "ease": "inout"}]}],
                      "cam": [orbit(0, 4.0, 145, 2.1, c=(0, 0.9, 0.5), focal=30, ease="lin", tz=0.6),
                              orbit(d, 3.7, 160, 2.3, c=(0, 1.0, 0.5), focal=30, ease="out2", tz=0.6)]}
    sh["s8_explode"] = explode_shot()
    return sh


def explode_shot():
    """Bumper, hood and trunk lid lift off on the accent, hang stacked above/in front of the car while the camera
    orbits front-right -> rear-right, then fly home and lock on a later accent. Base: full car minus the three panels
    + 'Front End Bumper Off' (front structure, engine bay) + 'NA Trunk Open' (trunk well)."""
    d = S("s8_explode", 10.0)
    sep = S("x_sep", 0.0)          # separation starts (s from shot start)
    out = sep + 2 * BEAT           # parts reach their exploded pose
    back = S("x_back", d - 4 * BEAT)  # start flying home
    lock = S("x_lock", d - 1.5 * BEAT)  # parts seated (an accent)

    def ex(off, rot=(0, 0, 0), delay=0.0, pivot=None):
        k = [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
             {"t": sep + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
             {"t": out + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
             {"t": back, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},
             {"t": lock, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]
        return k
    parts = [
        {"blend": f"{P}/fbumper_c.blend", "keys": ex((0, -0.25, 1.05))},
        {"blend": f"{P}/hood_full.blend", "keys": ex((0, -0.05, 1.5), (-8, 0, 0), 0.08)},
        {"blend": f"{P}/trunk_full.blend", "keys": ex((0, 0.25, 1.1), (10, 0, 0), 0.16)},
    ]
    cam = [orbit(d * k / 12, 5.2 + 0.4 * math.sin(math.pi * k / 12), -40 - 85 * (k / 12), 4.4,
                 c=(0, -0.65 + 0.5 * (k / 12), 1.0), focal=28, ease="lin", tz=0.95) for k in range(13)]
    return {"base": [f"{P}/comp_explode.blend"], "parts": parts, "cam": cam}


def spec(name, mode, frames=None):
    s = shots()[name]
    final = mode == "final"
    secs = s.get("secs", S(name, 2.4))
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": secs + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if frames:
        sp["frames"] = frames
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(shots()):
        print(spec(n, mode, ["first", "mid", "last"] if mode == "preview" else None))
