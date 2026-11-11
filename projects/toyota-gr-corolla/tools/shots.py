"""Shot specs for the GR Corolla Temerario-style reel -> JSON for tools/shot.py (copied from ferrari-296).

    python projects/toyota-gr-corolla/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Prepped frame (metres, car4.json): front = -Y, car's right = -X, floor Z=0; 4.40 m long, 1.98 m wide incl. mirrors.
Real wheels: both fronts; rear-left (+X) filled from the 'rear' state scan; rear-right only partial ->
front views from the car's right, rear views from its left.
Timing: SECS (shot lengths) and the beat-locked keys come from timing.json (written from `ive beats`).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/grc/blend"
OUT = "/home/user/media/work/grc/renders"
SPECS = "/home/user/media/work/grc/specs"
T = json.load(open(os.path.join(HERE, "..", "timing.json")))
SECS, BEAT = T["secs"], T["beat"]

CAR = f"{B}/car4w.blend"     # 4 mm + real rear wheels: full-car moves
CAR_HI = f"{B}/car2w.blend"  # 2 mm: close-ups
BASE = f"{B}/x_base.blend"   # car leftovers (roof, pillars, quarters, sills, wheels) + Chassis Stripped scan
PANELS = ["p_hood", "p_fender_R", "p_fender_L", "p_door_FR", "p_door_FL", "p_door_RR", "p_door_RL", "p_hatch"]
SCANPARTS = ["fbumper", "rbumper", "rbinner", "diffuser"]  # real part scans
HOOD_PIVOT, HATCH_PIVOT = [0, -0.99, 0.98], [0, 1.32, 1.36]


def pb(k):
    return f"{B}/x_{k}.blend" if k.startswith("p_") else f"{B}/{k}.blend"


def still(k):
    return {"blend": pb(k)}


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, n, r0, r1, a0, a1, h0, h1, c=(0, 0, 0.55), focal=30, tz=None):
    """orbit keyed every 1/n of the move (linear loc between far keys would cut a chord toward the car)"""
    ks = []
    for k in range(n + 1):
        u = k / n
        s = u * u * (3 - 2 * u)
        ks.append(orbit(secs * u, r0 + (r1 - r0) * s, a0 + (a1 - a0) * s, h0 + (h1 - h0) * s, c=c, focal=focal, ease="lin", tz=tz))
    return ks


def all_home(skip=()):
    return [still(k) for k in PANELS + SCANPARTS if k not in skip]


S = SECS
SHOTS = {
    # 1. slow front 3/4 turntable from the car's right, low; moving from frame 1
    "s1_front": {"base": [CAR], "cam": arc(S["s1_front"], 8, 5.6, 4.9, -30, -62, 0.95, 1.05, c=(0, -0.15, 0.55), focal=30, tz=0.5)},
    # 2. rear 3/4 orbit from the car's left (real rear wheel), slight rise
    "s2_rear": {"base": [CAR], "cam": arc(S["s2_rear"], 8, 4.8, 4.6, 150, 122, 0.8, 1.35, focal=30, tz=0.5)},
    # 3. extreme close-up: front right wheel + brake through the spokes (2 mm), slow slide toward the nose
    "s3_wheel": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.95, -0.95, 0.40], "target": [-0.85, -1.45, 0.34], "focal": 38},
        {"t": S["s3_wheel"], "loc": [-1.95, -1.85, 0.42], "target": [-0.85, -1.38, 0.34], "focal": 38, "ease": "inout"}]},
    # 4. detail: right headlight + grille, slide across the nose
    "s4_nose": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.55, -3.35, 0.85], "target": [-0.55, -1.95, 0.70], "focal": 38},
        {"t": S["s4_nose"], "loc": [-0.35, -3.6, 0.80], "target": [-0.25, -2.0, 0.62], "focal": 38, "ease": "inout"}]},
    # 5. hood opens on its rear hinge, revealing the stripped shell's front structure (Chassis Stripped scan)
    "s5_hood": {"base": [BASE], "parts": all_home(["p_hood"]) + [
        {"blend": pb("p_hood"), "pivot": HOOD_PIVOT, "keys": [
            {"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": T["hood_open"][0], "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": T["hood_open"][1], "loc": [0, 0, 0], "rot": [-62, 0, 0], "ease": "inout"}]}],
        "cam": arc(S["s5_hood"], 6, 4.4, 3.9, -32, -14, 2.3, 2.6, c=(0, -1.0, 0.5), focal=30)},
    # 6. hatch lifts on its top hinge, high rear 3/4 from the left
    "s6_hatch": {"base": [BASE, f"{B}/cargo.blend"], "parts": all_home(["p_hatch"]) + [
        {"blend": pb("p_hatch"), "pivot": HATCH_PIVOT, "keys": [
            {"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": T["hatch_open"][0], "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": T["hatch_open"][1], "loc": [0, 0, 0], "rot": [75, 0, 0], "ease": "inout"}]}],
        "cam": arc(S["s6_hatch"], 6, 4.3, 4.0, 150, 165, 2.2, 2.5, c=(0, 1.2, 0.6), focal=30)},
    # 7. top-down: from a high front-right 3/4 up and over to straight down, nose at the top of frame
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [-2.6, -4.2, 4.2], "target": [0, -0.3, 0.5], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, -0.25, 7.6], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}

# 8. exploded view: every panel separates on the sep accent, drifts while the camera orbits front-right -> rear-left
# over the top, flies home and LOCKs on the lock accent, holds -> logo. Offsets go up/out and down/back, never at the lens.
SEP, HOLD, BACK, LOCK = T["sep"], T["sep"] + 3 * BEAT, T["lock"] - 3 * BEAT, T["lock"]


def explode(off, rot=(0, 0, 0), delay=0.0):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": HOLD + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": BACK, "loc": [o * 1.07 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


XP = {"p_hood": ((0, -0.15, 1.0), (-14, 0, 0), 0.0),
      "fbumper": ((0, -0.7, -0.2), (0, 0, 0), 0.0),
      "p_fender_R": ((-0.6, -0.05, 0.45), (0, -10, 0), 0.06),
      "p_fender_L": ((0.6, -0.05, 0.45), (0, 10, 0), 0.06),
      "p_door_FR": ((-0.7, 0, 0.55), (0, -6, 0), 0.12),
      "p_door_FL": ((0.7, 0, 0.55), (0, 6, 0), 0.12),
      "p_door_RR": ((-0.7, 0.1, 0.85), (0, -6, 0), 0.18),
      "p_door_RL": ((0.7, 0.1, 0.85), (0, 6, 0), 0.18),
      "p_hatch": ((0, 0.45, 1.0), (22, 0, 0), 0.24),
      "rbumper": ((0, 0.7, -0.15), (0, 0, 0), 0.3),
      "rbinner": ((0, 0.7, -0.15), (0, 0, 0), 0.3),
      "diffuser": ((0, 0.55, -0.35), (0, 0, 0), 0.36)}
SHOTS["s8_explode"] = {
    "base": [BASE],
    "parts": [{"blend": pb(k), "keys": explode(*v)} for k, v in XP.items()],
    # radius swells side-on (exploded length spans the 9:16 width there)
    "cam": [orbit(S["s8_explode"] * k / 14, 6.6 + 1.7 * math.sin(math.pi * (-48 + 183 * (k * k * (3 - 2 * k / 14) / 196)) / 180) ** 2,
                  -48 + 183 * (k * k * (3 - 2 * k / 14) / 196), 3.3 + 0.4 * k / 14, c=(0, 0, 0.6), focal=28, ease="lin", tz=0.55)
            for k in range(15)]}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if mode == "frames":
        sp["frames"] = ["first", "mid", "last"]
        sp["out"] = f"{OUT}/frames/{name}"
        sp["res_pct"], sp["samples"] = 30, 6
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
