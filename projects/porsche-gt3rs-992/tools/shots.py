"""Shot specs for the Porsche 911 GT3 RS (992) Temerario-style reel -> JSON for tools/shot.py (copied from ferrari-296).

    python projects/porsche-gt3rs-992/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (prepped, metres): front = -Y, car's left = +X, ground Z=0; length 4.58 m, width 1.98 m incl. mirrors.
Orbit angle 0 = camera in front of the car (-Y); +90 = car's left (+X); -90 = car's right (-X); 180 = behind.
Timed shots (s6_lift, s8_explode) read the beat grid from TIMING (set from the music, see project.yaml).
"""
import json
import math
import os
import sys

P = "/home/user/media/porsche-gt3rs-992/prep"
OUT = "/home/user/media/work/gt3/renders"
SPECS = "/home/user/media/work/gt3/specs"
CAR = f"{P}/car4.blend"       # 4 mm: full-car moves
CAR_HI = f"{P}/car2p5.blend"  # 2.5 mm: close-ups
TIMING = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "timing.json")))
BEAT = TIMING["beat"]
SECS = TIMING["secs"]


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, r0, r1, a0, a1, h0, h1, c0=(0, 0, 0.55), c1=None, focal=30, n=8, tz=None, shape="inout"):
    """Orbit keyed every 1/n of the shot (linear interpolation between far keys would cut a chord toward the car)."""
    c1 = c1 or c0
    keys = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if shape == "inout" else (1 - (1 - u) ** 2 if shape == "out" else u)
        c = [c0[i] + (c1[i] - c0[i]) * e for i in range(3)]
        keys.append(orbit(secs * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal,
                          ease="lin", tz=tz))
    return keys


S = SECS
SHOTS = {
    # 1. slow low front 3/4 turntable (car's left), moving from frame 1 (hook)
    "s1_turntable": {"base": [CAR], "cam": arc(S["s1_turntable"], 4.9, 4.7, 24, 52, 0.9, 1.0, c0=(0, -0.15, 0.55), focal=30, shape="out")},
    # 2. rear 3/4 orbit on the car's right, rising: swan-neck wing + diffuser
    "s2_rear": {"base": [CAR], "cam": arc(S["s2_rear"], 5.0, 4.8, -158, -134, 0.9, 1.55, c0=(0, 0.2, 0.6), focal=30)},
    # 3. extreme close-up: front left wheel / centre-lock / brake through the spokes, slide back along the arch
    "s3_wheel": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [2.15, -2.35, 0.42], "target": [0.9, -1.5, 0.36], "focal": 40},
        {"t": S["s3_wheel"], "loc": [2.25, -1.1, 0.45], "target": [0.92, -1.42, 0.36], "focal": 40, "ease": "inout"}]},
    # 4. extreme close-up: right front fender louvres (fender vent), slide over the top of the fender
    "s4_vent": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-2.0, -1.6, 1.3], "target": [-0.82, -1.2, 0.78], "focal": 40},
        {"t": S["s4_vent"], "loc": [-1.85, -0.35, 1.5], "target": [-0.82, -1.1, 0.8], "focal": 40, "ease": "inout"}]},
    # 5. close-up: swan-neck wing + mounts, from high behind, sliding across
    "s5_wing": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [1.6, 3.9, 1.95], "target": [0.1, 2.05, 1.15], "focal": 38},
        {"t": S["s5_wing"], "loc": [-1.2, 4.0, 2.05], "target": [-0.1, 2.05, 1.15], "focal": 38, "ease": "inout"}]},
    # 7. top-down: from a high front 3/4 up and over to straight down (nose at the bottom of frame -> reads as driving up)
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [2.6, -4.6, 3.6], "target": [0, -0.2, 0.5], "focal": 30},
        {"t": S["s7_top"] * 0.5, "loc": [1.0, -2.0, 6.0], "target": [0, -0.1, 0.5], "focal": 30, "ease": "lin"},
        {"t": S["s7_top"], "loc": [0.0, -0.25, 7.2], "target": [0, 0.0, 0.5], "focal": 30, "ease": "out2"}]},
}

# 6. front aero lifts (the brief's "panels open": no hood/door/DRS state scans exist, so the scanned aero pieces on the
# nose lift off their mounts instead): fender vent + left hood vent top rise, lip and strakes ease forward. Holds open.
L0, L1 = TIMING.get("lift_start", BEAT), TIMING.get("lift_end", 3 * BEAT)


def lift(off, rot=(0, 0, 0)):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": L0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": L1, "loc": list(off), "rot": list(rot), "ease": "inout"}]


SHOTS["s6_lift"] = {"base": [f"{P}/comp_explode4.blend", f"{P}/x_fender_vent.blend", f"{P}/x_hood_vent_interface_assembled_left.blend", f"{P}/x_side_skirt_upper.blend", f"{P}/x_sideskirt_lower.blend",
                             f"{P}/x_side_skirt_strake.blend", f"{P}/x_rear_qpanel_intake_1.blend",
                             f"{P}/x_rear_qpanel_intake_2.blend", f"{P}/x_rear_bumper_strake.blend",
                             f"{P}/x_rear_diffuser_1.blend", f"{P}/x_rear_diffuser_trim_outer.blend"],
                    "parts": [
                              {"blend": f"{P}/x_hood_vent_top_warped.blend", "keys": lift((0, 0, 0.36))},
                              {"blend": f"{P}/x_front_lower_lip.blend", "keys": lift((0, -0.32, -0.04))},
                              {"blend": f"{P}/x_front_bumper_strake.blend", "keys": lift((0, -0.18, 0.04))},
                              {"blend": f"{P}/x_front_grille_trim.blend", "keys": lift((0, -0.12, 0.0))}],
                    "cam": arc(S["s6_lift"], 3.6, 3.3, 28, 10, 1.45, 1.7, c0=(0, -1.5, 0.45), c1=(0, -1.7, 0.45), focal=30)}

# 8. exploded view: every scanned aero piece separates on SEP, drifts while the camera orbits from the car's left front
# across the nose to the right, flies home and LOCKS on LOCK, holds.
SEP, HOLD, BACK, LOCK = (TIMING.get(k, d) for k, d in (("sep", 0.5), ("hold", 2.5), ("back", 7.0), ("lock", 9.0)))


def explode(off, rot=(0, 0, 0), delay=0.0):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": HOLD + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": BACK, "loc": [o * 1.08 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


XPARTS = [  # (part, offset m, rot deg, delay s) - front pieces stacked forward/up, side pieces out, rear pieces back
    ("front_lower_lip", (0, -0.75, -0.08), (0, 0, 0), 0.0),
    ("front_grille_trim", (0, -0.5, 0.1), (0, 0, 0), 0.04),
    ("front_bumper_strake", (0, -0.28, 0.5), (0, 0, 0), 0.08),
    ("fender_vent", (-0.3, 0, 0.7), (0, -15, 0), 0.04),
    ("hood_vent_top_warped", (0.05, 0, 0.85), (0, 0, 0), 0.08),
    ("side_skirt_upper", (0.55, 0, 0.05), (0, 0, 0), 0.04),
    ("sideskirt_lower", (0.9, 0, -0.08), (0, 0, 0), 0.08),
    ("side_skirt_strake", (0.5, -0.1, 0.4), (0, 0, 0), 0.06),
    ("rear_qpanel_intake_1", (-0.45, 0, 0.2), (0, 0, 0), 0.06),
    ("rear_qpanel_intake_2", (0.45, 0, 0.2), (0, 0, 0), 0.06),
    ("rear_bumper_strake", (0.45, 0.3, 0.0), (0, 0, 0), 0.08),
    ("rear_diffuser_1", (0, 0.65, -0.18), (0, 0, 0), 0.0),
    ("rear_diffuser_trim_outer", (0, 0.9, 0.12), (0, 0, 0), 0.04),
]
SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_explode4.blend", f"{P}/x_hood_vent_interface_assembled_left.blend"],
    "parts": [{"blend": f"{P}/x_{n}.blend", "keys": explode(o, r, d)} for n, o, r, d in XPARTS],
    "cam": arc(S["s8_explode"], 5.2, 5.6, 48, -36, 4.6, 4.2, c0=(0.1, -0.3, 0.45), c1=(-0.1, -0.1, 0.45),
               focal=30, n=14, shape="lin")}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": S[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if mode == "preview":
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
