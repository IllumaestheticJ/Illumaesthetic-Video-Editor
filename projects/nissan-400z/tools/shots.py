"""Shot specs for the Nissan 400Z Temerario-style reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/nissan-400z/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Prepped scan frame (metres): nose at -Y, car's right = -X, ground Z=0; length 4.40 m (y -2.17..2.23),
height 1.32 m. Front wheels y~-1.25, rear y~1.40, track x~+-0.8. Durations come from projects/nissan-400z/cues.json
("secs": {shot: seconds}) once the track is measured; renders carry 1 extra frame so the cut never runs dry.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/z400/blend"
OUT = "/home/user/media/work/z400/renders"
SPECS = "/home/user/media/work/z400/specs"
HINGE = json.load(open(os.path.join(HERE, "..", "hinge.json")))
CUES = json.load(open(os.path.join(HERE, "..", "cues.json")))
SECS = CUES["secs"]
CAR = f"{B}/car.blend"          # 3 mm: full-car moves
FRONT = f"{B}/front2.blend"     # 2 mm crops for close-ups (seam outside frame)
REAR = f"{B}/rear2.blend"
SIDE = f"{B}/side2.blend"    # right side, rear of the A-pillar


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, r0, r1, a0, a1, h0, h1, c0=(0, 0, 0.55), c1=None, focal=30, n=8, ease_out=True, tz=None):
    """Smooth orbit sampled every 1/n (linear chords between far keys would cut toward the car)."""
    c1 = c1 or c0
    keys = []
    for k in range(n + 1):
        u = k / n
        e = 1 - (1 - u) ** 2 if ease_out else u * u * (3 - 2 * u)
        c = [a + (b - a) * e for a, b in zip(c0, c1)]
        keys.append(orbit(secs * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c=c, focal=focal, ease="lin", tz=tz))
    return keys


def slide(secs, p0, t0, p1, t1, focal):
    return [{"t": 0, "loc": p0, "target": t0, "focal": focal},
            {"t": secs, "loc": p1, "target": t1, "focal": focal, "ease": "inout"}]


S = SECS
SHOTS = {
    # 1. slow low front 3/4 turntable (fade up from black in the edit)
    "s1_front34": {"base": [CAR], "cam": arc(S["s1_front34"], 5.3, 5.0, -22, -50, 0.95, 1.05, c0=(0, -0.15, 0.55), focal=30)},
    # 2. rear 3/4 orbit on the other side, slight rise
    "s2_rear34": {"base": [CAR], "cam": arc(S["s2_rear34"], 5.2, 5.0, 162, 138, 0.8, 1.2, c0=(0, 0.15, 0.55), focal=30)},
    # 3. close-up glide along the right rear haunch / door shut line toward the C-pillar (2 mm right-rear crop).
    #    (Wheel close-up dropped: the dark rims scanned as hollow spoke fragments - see editlog.)
    "s3_haunch": {"base": [SIDE], "cam": slide(S["s3_haunch"], [-1.08, 2.75, 1.55], [-0.8, 0.9, 0.85],
                                                [-1.28, 1.55, 1.5], [-0.75, -0.3, 0.85], 35)},
    # 4. extreme close-up: headlight + grille edge, slide across the nose
    "s4_lamp": {"base": [FRONT], "cam": slide(S["s4_lamp"], [-1.55, -2.95, 0.95], [-0.55, -1.85, 0.68],
                                              [-0.45, -3.3, 0.85], [-0.35, -1.95, 0.62], 40)},
    # 5. extreme close-up: full-width tail lamp bar + badge, slow lateral slide
    "s5_tail": {"base": [REAR], "cam": slide(S["s5_tail"], [1.35, 3.5, 1.05], [0.25, 2.15, 0.85],
                                             [-0.6, 3.6, 1.0], [-0.25, 2.15, 0.85], 38)},
    # 6. hood opens on the fitted hinge (engine bay from 'Hood Open'), high front 3/4, camera eases in
    "s6_hood": {"base": [f"{B}/comp_hood.blend"],
                "parts": [{"blend": f"{B}/p_hood.blend", "pivot": HINGE["pivot"],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": CUES.get("hood_start", 0.5), "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": CUES.get("hood_open", 2.4), "loc": [0, 0, 0], "rot": [HINGE["open_deg"], 0, 0], "ease": "inout"}]}],
                "cam": arc(S["s6_hood"], 3.9, 3.4, -34, -20, 2.2, 2.4, c0=(0, -1.0, 0.6), c1=(0, -1.15, 0.65), focal=30)},
    # 7. top-down: from a high rear 3/4 up and over to straight down, nose to the top of the frame
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [1.9, 4.4, 3.8], "target": [0, 0.3, 0.5], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, 0.15, 6.8], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}

# 8. exploded view: panels separate on an accent, drift while the camera orbits, fly home and lock on a later accent.
SEP, HOLD, BACK, LOCK = (CUES.get("ex_" + k, v) for k, v in (("sep", 0.25), ("hold", 2.2), ("back", 6.0), ("lock", 8.0)))


def explode(off, rot=(0, 0, 0), delay=0.0):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": HOLD + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": BACK, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


# portrait-friendly: panels mostly stack UP (Temerario 25-31 s) and only modestly fore/aft/out
PARTS = [
    (f"{B}/p_hood.blend", (0, -0.05, 1.45), (-8, 0, 0), 0.0),
    (f"{B}/bumper_shell.blend", (0, -0.22, 0.62), (0, 0, 0), 0.05),
    (f"{B}/p_grille.blend", (0, -0.22, 0.62), (0, 0, 0), 0.05),  # v4: grille rides in the bumper (user: nothing comes off the bumper before the bumper)
    (f"{B}/p_wing.blend", (0, 0.25, 1.15), (14, 0, 0), 0.08),
    (f"{B}/p_mirror_r.blend", (-0.45, 0, 0.35), (0, 0, -20), 0.1),
    (f"{B}/p_mirror_l.blend", (0.45, 0, 0.35), (0, 0, 20), 0.1),
]


def parts(offset=0.0):
    """One explode timeline across both explode shots; shot B samples it from `offset` s (its cut)."""
    out = []
    for blend, off, rot, delay in PARTS:
        keys = explode(off, rot, delay)
        for k in keys:
            k["t"] -= offset
        out.append({"blend": blend, "keys": keys})
    return out


# A: separate on the 19.32 s accent, fully out on 23.01 s; high front-right 3/4 looking down
SHOTS["s8a_explode"] = {"base": [f"{B}/comp_explode.blend"], "parts": parts(),
    "cam": arc(S["s8a_explode"], 5.3, 5.6, -18, -55, 4.4, 3.9, c0=(0, -0.55, 0.75), c1=(0, -0.4, 0.75), focal=28, n=12,
               ease_out=False, tz=0.7)}
# B (cut on 26.70 s): high rear-left 3/4; panels fly home and LOCK on 30.40 s (heaviest kick), car rests to the logo
SHOTS["s8b_explode"] = {"base": [f"{B}/comp_explode.blend"], "parts": parts(BACK),
    "cam": arc(S["s8b_explode"], 5.6, 5.0, 148, 112, 4.0, 2.6, c0=(0, 0.45, 0.75), c1=(0, 0.1, 0.6), focal=28, n=12,
               ease_out=True, tz=0.6)}


# ---------------- v2 (direction.md / director.md, 2026-11-11): section-focused, front -> side -> rear -------------
EXP = f"{B}/comp_explode.blend"
STACK = {  # v1 explode offsets x1.06 = s8b's first frame; parts already off wait here (out of frame)
    "p_hood": ((0, -0.053, 1.537), (-8, 0, 0)), "bumper_shell": ((0, -0.233, 0.657), (0, 0, 0)),
    "p_grille": ((0, -0.233, 0.657), (0, 0, 0)), "p_wing": ((0, 0.265, 1.219), (14, 0, 0)),
    "p_mirror_r": ((-0.477, 0, 0.371), (0, 0, -20)), "p_mirror_l": ((0.477, 0, 0.371), (0, 0, 20))}


def held(name, at_stack=True):
    loc, rot = STACK[name] if at_stack else ((0, 0, 0), (0, 0, 0))
    return {"blend": f"{B}/{name}.blend", "keys": [{"t": 0, "loc": list(loc), "rot": list(rot)}]}


def k(t, loc, rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}


def cam2(secs, p0, t0, f0, p1, t1, f1):
    return [{"t": 0, "loc": p0, "target": t0, "focal": f0},
            {"t": secs, "loc": p1, "target": t1, "focal": f1, "ease": "inout"}]


# N0: whole car, motion from frame 1, never touching an edge (s1 clipped the nose)
SHOTS["N0_open"] = {"base": [CAR], "cam": arc(S["N0_open"], 6.6, 6.4, -18, -35, 1.20, 1.38, c0=(0, -0.10, 0.80),
                                                focal=30, n=10, ease_out=False)}  # v3: 7.45 s intro (was 3.8 s, -24..-34)
# H: the real Hood Open scan (captured open hood on comp_hood) - no animated closed hood (addendum D)
SHOTS["H_hoodopen"] = {"base": [f"{B}/comp_hood.blend"],  # bay from the Hood Open scan; its captured hood is only ragged flaps (read as noise)
                       "cam": cam2(S["H_hoodopen"], [-1.35, -4.55, 2.60], [0, -1.00, 0.75], 30,  # v3: 6.85 s push from further back
                                   [-0.80, -3.80, 2.25], [0.05, -0.95, 0.68], 30)}  # v3 preview: end touched the right edge
# N1a (hero, on the drop): grille out toward the lens and up out of frame, then the bumper shell; camera moves in
SHOTS["N1a_bumper_off"] = {"base": [EXP], "parts": [
    # v4 (user): nothing comes off the bumper until the bumper itself comes off -> grille + shell leave as ONE unit,
    # home until the 14.971 kick (0.94 s in), out toward the lens, then up out of frame top by ~2.8 s (16.846 kick)
    *[{"blend": f"{B}/{n}.blend", "keys": [k(0, (0, 0, 0)), k(0.94, (0, 0, 0)), k(1.60, (0, -0.85, 0.15), ease="out"),
                                           k(2.10, (0, -0.88, 0.18), ease="lin"), k(2.80, (0, -0.60, 1.8), ease="in")]}
      for n in ("bumper_shell", "p_grille")],
    held("p_wing", False), held("p_mirror_r", False), held("p_mirror_l", False)],
    "cam": cam2(S["N1a_bumper_off"], [-2.25, -4.70, 1.30], [-0.10, -1.70, 0.55], 30,
                [-1.25, -3.55, 0.80], [-0.10, -1.95, 0.50], 30)}
# N1b (hero hold): slow lateral slide across the 2 mm 'Bumper and hood removed' scan, right lamp -> beam centre
SHOTS["N1b_structure"] = {"base": [f"{B}/bhr2.blend"],
                          "cam": cam2(S["N1b_structure"], [-1.05, -3.30, 0.80], [-0.50, -2.00, 0.45], 35,
                                      [0.20, -3.40, 0.85], [0.05, -2.00, 0.45], 35)}
# N2: right mirror lifts off outboard/up, camera settles on the scanned mount (Side Mirrors Removed)
_mr, _rr = STACK["p_mirror_r"]; _ml, _rl = STACK["p_mirror_l"]
SHOTS["N2_mirror"] = {"base": [EXP], "parts": [
    {"blend": f"{B}/p_mirror_r.blend", "keys": [k(0, (0, 0, 0)), k(0.25, (0, 0, 0)), k(1.00, _mr, _rr, ease="out")]},
    {"blend": f"{B}/p_mirror_l.blend", "keys": [k(0, (0, 0, 0)), k(0.25, (0, 0, 0)), k(1.00, _ml, _rl, ease="out")]},
    held("p_wing", False)],  # front parts left out: they exited the top in N1a and cluttered the frame
    "cam": cam2(S["N2_mirror"], [-1.95, 0.85, 1.40], [-1.00, -0.40, 1.05], 40,
                [-2.30, 0.45, 1.45], [-1.10, -0.35, 1.05], 35)}
# N3: duck-tail wing lifts straight up/back (no flip), camera rises over the Rear Wing Removed deck
_mw, _rw = STACK["p_wing"]
SHOTS["N3_wing"] = {"base": [EXP], "parts": [
    {"blend": f"{B}/p_wing.blend", "keys": [k(0, (0, 0, 0)), k(0.30, (0, 0, 0)), k(1.60, (0, 0.10, 0.42), (8, 0, 0)),
                                           k(4.60, (0, 0.14, 0.55), (10, 0, 0), ease="lin")]},
    ],  # other parts left out: off-section clutter at the frame top. v2 render lifted to the full stack (1.2 m) and the
    # wing left the top of frame for ~2 s mid-shot -> small lift + slow drift so the subject never leaves the frame
    "cam": cam2(S["N3_wing"], [-0.60, 3.60, 1.00], [-0.25, 2.15, 0.85], 38,
                [-1.10, 4.15, 2.25], [0.05, 1.85, 0.95], 27)}  # f35 cut the wing's left tip + right quarter (v3 frames check)


FPS = {"N2_mirror": 30, "N1a_bumper_off": 30}  # fast part exits tear under minterpolate (N2 f706-722, N1a f491-503) -> native 30 fps


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / FPS.get(name, 15), "fps": FPS.get(name, 15), "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}", "persist": False}
    if mode == "frames":
        sp["frames"] = ["first", "mid", "last"]
        sp["out"] = f"{OUT}/frames/{name}"
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
