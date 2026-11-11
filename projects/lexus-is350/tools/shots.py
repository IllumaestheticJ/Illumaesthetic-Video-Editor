"""Shot specs for the Lexus IS350 (2026 facelift) Temerario-style scan reel -> JSON for
projects/ferrari-296/tools/shot.py (shared keyframed renderer: house silver look, camera keys, pivoted parts).

    python projects/lexus-is350/tools/shots.py preview|final [shot ...]    # writes specs, prints their paths

Scan frame (prepped, metres): nose = -Y, car's right = -X, ground Z=0; 4.72 m long, 1.94 m wide incl. mirrors.
Durations come from TIMING (seconds, set from the track's accent grid in project.yaml); each shot renders one
extra 15 fps frame so assemble can trim to the exact cut.
"""
import json
import math
import os
import sys

M = "/home/user/media/lexus-is350"
P = f"{M}/prep"
OUT = f"{M}/renders"
SPECS = f"{M}/specs"
HINGE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hinge.json")))

CAR = f"{P}/car4.blend"            # 4 mm full car: whole-car moves
FR = f"{P}/fr_corner.blend"        # 2 mm front-right corner: close-ups
RR = f"{P}/rr_corner.blend"        # 2 mm rear-right corner: close-ups

# shot lengths (s). Provisional until the track arrives; overwritten by timing.json if present.
TIMING = {"s1_front34": 4.6, "s2_rear34": 4.0, "s3_lamp": 3.0, "s4_tail": 2.6, "s5_hood": 4.4,
          "s6_top": 3.4, "s7_explode": 9.0,
          # explode beats (s from shot start): separate starts, fully out, start return, locked
          "x_sep": 0.4, "x_out": 2.2, "x_back": 6.2, "x_lock": 7.6}
_tj = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "timing.json")
if os.path.exists(_tj):
    TIMING.update(json.load(open(_tj)))


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, r0, r1, a0, a1, h0, h1, c0, c1, focal=30, tz=None, n=8, ease="inout"):
    """Orbit sampled in n segments (linear keys between far-apart points would cut a chord toward the car);
    the easing is applied to the whole move by remapping the sample times."""
    keys = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if ease == "inout" else (1 - (1 - u) ** 2 if ease == "out" else u)
        c = [c0[i] + (c1[i] - c0[i]) * e for i in range(3)]
        keys.append(orbit(secs * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal,
                          ease="lin", tz=tz))
    return keys


S = TIMING
SHOTS = {
    # 1. low front 3/4 turntable, car's right side, slow and continuous from frame 1
    "s1_front34": {"base": [CAR], "cam": arc(S["s1_front34"], 5.9, 5.6, -24, -44, 1.05, 1.15,
                                              (0, -0.2, 0.62), (0, -0.1, 0.62), focal=30, ease="out")},
    # 2. rear 3/4 orbit on the other (left) side, slight rise
    "s2_rear34": {"base": [CAR], "cam": arc(S["s2_rear34"], 5.8, 5.5, 152, 134, 1.1, 1.35,
                                             (0, 0.2, 0.62), (0, 0.1, 0.62), focal=30, ease="out")},
    # 3. extreme close-up: right headlamp -> grille mesh corner (plate stays out of frame)
    "s3_lamp": {"base": [FR], "cam": [
        {"t": 0, "loc": [-1.55, -3.25, 0.92], "target": [-0.62, -2.18, 0.72], "focal": 40},
        {"t": S["s3_lamp"], "loc": [-1.25, -3.5, 0.82], "target": [-0.56, -2.26, 0.64], "focal": 40, "ease": "inout"}]},
    # 4. extreme close-up: right tail lamp + IS350 badge, slide along the deck lid edge (plate out of frame)
    "s4_tail": {"base": [RR], "cam": [
        {"t": 0, "loc": [-2.05, 3.05, 1.12], "target": [-0.74, 2.15, 0.9], "focal": 40},
        {"t": S["s4_tail"], "loc": [-1.75, 3.3, 1.02], "target": [-0.7, 2.2, 0.86], "focal": 40, "ease": "inout"}]},
    # 5. hood opens on its fitted hinge (60 deg = the captured 'Hood Open' state); bay from 'Bumper and Hood Removed'
    "s5_hood": {"base": [f"{P}/comp_hood.blend"],
                "parts": [{"blend": f"{P}/hood3.blend", "pivot": HINGE["pivot"],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 0.5, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": S["s5_hood"] - 0.9, "loc": [0, 0, 0], "rot": [HINGE["open_deg"], 0, 0],
                                     "ease": "inout"}]}],
                "cam": arc(S["s5_hood"], 4.3, 3.8, -32, -18, 2.0, 2.3, (0, -1.0, 0.6), (0, -1.2, 0.6), focal=30,
                           ease="out")},
    # 6. top-down: from a high rear 3/4 up and over to straight down, nose to the top of the frame
    "s6_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [2.0, 4.4, 3.8], "target": [0, 0.3, 0.5], "focal": 30},
        {"t": S["s6_top"], "loc": [0.0, 0.2, 7.4], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}


def explode(off, rot=(0, 0, 0), delay=0.0, back_delay=0.0):
    """separate (ease-out) -> slow drift outward -> fly home (ease-in) and lock on x_lock."""
    sep, out, back, lock = S["x_sep"] + delay, S["x_out"] + delay, S["x_back"] + back_delay, S["x_lock"]
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": sep, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": out, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": back, "loc": [o * 1.07 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": lock, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


# 7. exploded front end: outer layers fly first (fog covers, bumper shell), then what was behind them (ducts,
# radar, top bracket), hood lifts on top; panels stack up/forward (portrait-friendly), then all lock home.
SHOTS["s7_explode"] = {
    "base": [f"{P}/comp_explode.blend"],
    "parts": [
        {"blend": f"{P}/hood3.blend", "keys": explode((0, 0.1, 1.55), (-10, 0, 0), 0.10)},
        {"blend": f"{P}/x_shell.blend", "keys": explode((0, -0.55, 0.5))},
        {"blend": f"{P}/x_fog_L.blend", "keys": explode((0.3, -0.85, 0.3), (0, 0, -12))},
        {"blend": f"{P}/x_fog_R.blend", "keys": explode((-0.3, -0.85, 0.3), (0, 0, 12))},
        {"blend": f"{P}/x_duct_L.blend", "keys": explode((0.3, -0.3, 0.2), delay=0.2, back_delay=0.15)},
        {"blend": f"{P}/x_duct_R.blend", "keys": explode((-0.3, -0.3, 0.2), delay=0.2, back_delay=0.15)},
        {"blend": f"{P}/x_radar.blend", "keys": explode((0, -0.25, 0.85), delay=0.25, back_delay=0.2)},
        {"blend": f"{P}/x_bracket.blend", "keys": explode((0, -0.15, 1.15), delay=0.3, back_delay=0.1)},
    ],
    "cam": arc(S["s7_explode"], 6.6, 6.3, -22, -48, 2.3, 2.0, (0, -1.7, 1.15), (0, -1.3, 1.0), focal=30,
               n=12, ease="inout")}


def spec(name, mode, frames=None):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": S[name] + 1 / 15, "fps": 15, "res": "1080x1920",
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
    names = sys.argv[2:] or list(SHOTS)
    for n in names:
        fr = ["first", "mid", "last"]
        if n == "s7_explode":
            fr = ["first", int(round(S["x_out"] * 15)) + 1, int(round((S["x_back"] + S["x_lock"]) / 2 * 15)), "last"]
        print(spec(n, mode, fr if mode == "preview" else None))
