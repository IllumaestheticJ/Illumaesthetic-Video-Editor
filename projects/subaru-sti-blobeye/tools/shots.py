"""Shot specs for the Subaru Impreza STI GD blobeye Temerario-style reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/subaru-sti-blobeye/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (prepped, metres): nose = -Y, car's right = -X, ground Z=0; length 4.40 m, width 1.95 m, height 1.39 m.
Shot lengths come from cues.json (seconds, cut on the music's accents); every move is written in shot fractions
(u in 0..1) so a re-timed shot keeps its shape.
"""
import json
import math
import os
import sys

P = "/home/user/media/work/sti/prep"
OUT = "/home/user/media/work/sti/renders"
SPECS = "/home/user/media/work/sti/specs"
HERE = os.path.dirname(os.path.abspath(__file__))
CUES = os.path.join(HERE, "..", "cues.json")

CAR = f"{P}/car4.blend"         # 4 mm full car
FR2 = f"{P}/fr_2mm.blend"       # 2 mm front half (close-ups)
RR2 = f"{P}/rr_2mm.blend"       # 2 mm rear half
OPEN = f"{P}/base_open.blend"   # car minus hood/bumper/wing/left skirt, openings filled with state scans
HOOD = f"{P}/hood_skin.blend"
BUMP = f"{P}/bumper_skin.blend"
WING = f"{P}/wing.blend"
SKIRT = f"{P}/skirt.blend"
HOOD_PIVOT = [0.0, -1.003, 0.931]   # hood rear edge (A y=1200 mm, z=850 mm), hinge axis X


def orbit(u, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front (-Y); -90 = car's right (-X); +90 = car's left (+X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"u": u, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def topdown(u, h, heading_deg, c=(0, 0, 0.5), focal=30, ease="inout", r=0.02):
    """Straight-down camera; the tiny offset circle sets the frame heading (nose up when heading=0)."""
    a = math.radians(heading_deg)
    return {"u": u, "loc": [c[0] - r * math.sin(a), c[1] - r * math.cos(a), h], "target": list(c), "focal": focal, "ease": ease}


def pk(u, loc=(0, 0, 0), rot=(0, 0, 0), ease="inout"):
    return {"u": u, "loc": list(loc), "rot": list(rot), "ease": ease}


SHOTS = {
    # 1. low front 3/4 turntable on the car's right, moving from frame 1 (hook)
    "s1_front34": {"base": [CAR], "cam": [orbit(0, 5.6, -22, 0.75, c=(0, -0.55, 0.55), focal=30, ease="lin"),
                                          orbit(1, 5.3, -46, 0.85, c=(0, -0.45, 0.55), focal=30, ease="out2")]},
    # 2. rear 3/4 orbit on the car's left, wing against black, slight rise
    "s2_rear34": {"base": [CAR], "cam": [orbit(0, 5.6, 160, 0.95, c=(0, 0.55, 0.65), focal=30, ease="lin"),
                                         orbit(1, 5.3, 136, 1.35, c=(0, 0.45, 0.65), focal=30, ease="out2")]},
    # 3. extreme close-up: front-right wheel (spokes, caliper, disc), slow slide toward the nose
    "s3_wheel": {"base": [FR2], "cam": [
        {"u": 0, "loc": [-2.05, -0.55, 0.42], "target": [-0.80, -1.20, 0.36], "focal": 40},
        {"u": 1, "loc": [-2.05, -1.70, 0.40], "target": [-0.80, -1.30, 0.36], "focal": 40, "ease": "inout"}]},
    # 4. detail: blobeye headlight -> hood scoop, crane up across the nose
    "s4_light": {"base": [FR2], "cam": [
        {"u": 0, "loc": [-1.55, -3.00, 0.70], "target": [-0.55, -1.75, 0.70], "focal": 40},
        {"u": 1, "loc": [-0.95, -3.05, 1.55], "target": [-0.10, -1.40, 0.90], "focal": 40, "ease": "inout"}]},
    # 8. detail: wing end plate + blobeye-era tail light, rear-left, slow slide (2 mm rear half)
    "s8_wing": {"base": [RR2], "cam": [
        {"u": 0, "loc": [1.85, 3.05, 1.65], "target": [0.60, 1.85, 1.12], "focal": 42},
        {"u": 1, "loc": [1.68, 3.28, 1.60], "target": [0.56, 1.90, 1.12], "focal": 42, "ease": "inout"}]},
    # 5. hood opens on its rear hinge over the engine bay (state scans), camera high front 3/4 easing in
    "s5_hood": {"base": [OPEN, BUMP, WING, SKIRT],
                "parts": [{"blend": HOOD, "pivot": HOOD_PIVOT,
                           "keys": [pk(0), pk(0.083), pk(0.6, rot=(-52, 0, 0))]}],   # starts 1 beat after the 12.69 s lift
                "cam": [orbit(0, 3.5, -30, 2.2, c=(0, -1.0, 0.6), focal=30, ease="lin"),
                        orbit(1, 3.0, -16, 2.5, c=(0, -1.15, 0.65), focal=30, ease="out2")]},
    # 6. top-down, slow spin (nose rotates from up to up-right), slight push in
    "s6_top": {"base": [CAR], "cam": [topdown(0, 7.2, -4, focal=30, ease="lin"),
                                      topdown(1, 6.4, -30, focal=30, ease="out2")]},
    # 7. exploded view: separate (u 0.12->0.36), drift/hold, fly home and lock (u 0.70->0.86), orbit front-left
    # 7. exploded view (12.63 s from 22.17 s): assembled 2 bars, separate on bar 16 (25.32 s, u .25) staggered 1 beat
    #    per panel, float/drift, fly home from bar 20 (u .75) and LOCK on bar 21 (33.22 s, u .875), hold 1 bar
    "s7_explode": {"base": [OPEN],
                   "parts": [
                       {"blend": HOOD, "pivot": HOOD_PIVOT,
                        "keys": [pk(0), pk(0.25), pk(0.38, (0, 0.35, 1.35), (-8, 0, 0), "out"), pk(0.75, (0, 0.35, 1.45), (-12, 0, 0), "lin"),
                                 pk(0.875, (0, 0, 0), (0, 0, 0), "in")]},
                       {"blend": BUMP,
                        "keys": [pk(0), pk(0.281), pk(0.41, (0, -0.25, 0.8), (0, 0, 0), "out"), pk(0.75, (0, -0.28, 0.88), (0, 0, 0), "lin"),
                                 pk(0.875, (0, 0, 0), (0, 0, 0), "in")]},
                       {"blend": WING,
                        "keys": [pk(0), pk(0.3125), pk(0.44, (0, -0.1, 0.8), (0, 0, 0), "out"), pk(0.75, (0, -0.1, 0.9), (0, 0, 0), "lin"),
                                 pk(0.875, (0, 0, 0), (0, 0, 0), "in")]},
                       {"blend": SKIRT,
                        "keys": [pk(0), pk(0.344), pk(0.47, (0.5, 0, 0.35), (0, 0, 0), "out"), pk(0.75, (0.55, 0, 0.4), (0, 0, 0), "lin"),
                                 pk(0.875, (0, 0, 0), (0, 0, 0), "in")]}],
                   "cam": [orbit(0, 6.3, 36, 3.0, c=(0, -0.35, 1.2), focal=30, ease="lin"),
                           orbit(1, 6.4, 60, 2.8, c=(0, -0.2, 1.05), focal=30, ease="inout")]},
}

DEFAULT_SECS = {"s1_front34": 4.8, "s2_rear34": 4.2, "s3_wheel": 2.6, "s4_light": 2.6, "s5_hood": 4.2,
                "s6_top": 3.4, "s7_explode": 9.6}


def secs():
    if os.path.exists(CUES):
        return {**DEFAULT_SECS, **json.load(open(CUES)).get("secs", {})}
    return DEFAULT_SECS


def to_t(keys, T):
    out = []
    for k in keys:
        k = dict(k)
        k["t"] = k.pop("u") * T
        out.append(k)
    return out


def spec(name, mode):
    s = SHOTS[name]
    T = secs()[name]
    sp = {"base": s["base"], "camera": {"keys": to_t(s["cam"], T)}, "seconds": T, "fps": 15,
          "res": "1080x1920", "out": f"{OUT}/{mode}/{name}"}
    sp["parts"] = [{**p, "keys": to_t(p["keys"], T)} for p in s.get("parts", [])]
    if mode == "preview":
        sp.update(res_pct=30, samples=8, frames=["first", "mid", "last"])
    else:
        sp.update(res_pct=75, samples=12)
    return sp


if __name__ == "__main__":
    mode = sys.argv[1]
    names = sys.argv[2:] or list(SHOTS)
    os.makedirs(SPECS, exist_ok=True)
    for n in names:
        p = f"{SPECS}/{mode}_{n}.json"
        json.dump(spec(n, mode), open(p, "w"), indent=1)
        print(p)
