"""Shot specs for the Ferrari 296 Temerario-style reel -> JSON for tools/shot.py.

    python projects/ferrari-296/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Timing: ferrari296_track.mp3 accent grid (103.4 BPM, beat 0.5803 s); cuts listed in project.yaml. Scan frame (normalised, metres):
front = -Y, car's right = -X, ground Z=0; length 4.56 m, width 2.22 m incl. mirrors.
"""
import json
import math
import os
import sys

P = "/home/user/media/ferrari-296/prep"
OUT = "/home/user/media/work/f296/renders"
SPECS = "/home/user/media/work/f296/specs"
BAR = 2.4  # (old 100 BPM plan; kept for s1 which was already rendered on it)
BEAT = 0.5803  # ferrari296_track.mp3: 103.4 BPM, see editlog
SECS = {"s1_turntable": 4.8, "s2_rear": 140 / 30, "s3_wheel": 69 / 30, "s4_nose": 70 / 30, "s5_hood": 122 / 30,
        "s6_engine": 69 / 30, "s7_top": 70 / 30, "s8_explode": 348 / 30}

CAR = f"{P}/car4.blend"        # 4 mm: full-car moves
CAR_HI = f"{P}/car3.blend"     # 3 mm: close-ups


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=35, ease="inout", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


# angle 0 = camera in front of the car (-Y); +90 = car's left (+X); -90 = car's right (-X); 180 = behind
SHOTS = {
    # 1. slow 3/4 front turntable, low, starts moving on frame 1 (hook)
    "s1_turntable": { "base": [CAR], "cam": [orbit(0, 5.3, -32, 1.0, focal=30, ease="lin"),
                                                      orbit(2 * BAR, 5.1, -62, 1.1, focal=30, ease="out2")]},
    # 2. rear 3/4 orbit, other side, slight rise
    "s2_rear": { "base": [CAR], "cam": [orbit(0, 5.2, 148, 0.85, focal=30, ease="lin"),
                                                 orbit(SECS["s2_rear"], 5.0, 120, 1.3, focal=30, ease="out2")]},
    # 3. extreme close-up: front right wheel / brake through the spokes, slow slide forward
    "s3_wheel": { "base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-2.25, -0.95, 0.42], "target": [-0.95, -1.42, 0.36], "focal": 40},
        {"t": SECS["s3_wheel"], "loc": [-2.15, -1.75, 0.40], "target": [-0.95, -1.47, 0.36], "focal": 40, "ease": "inout"}]},
    # 4. detail: front lamp + intake, slide across the nose (tail lamps are scan holes - not used)
    "s4_nose": { "base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.75, -3.35, 0.9], "target": [-0.6, -2.0, 0.62], "focal": 38},
        {"t": SECS["s4_nose"], "loc": [-0.55, -3.7, 0.8], "target": [-0.45, -2.1, 0.58], "focal": 38, "ease": "inout"}]},
    # 5. hood opens on its rear hinge (frunk from "Front Fully Removed"), camera eases in
    "s5_hood": { "base": [f"{P}/comp_hood.blend"],
                "parts": [{"blend": f"{P}/hood_combined.blend", "pivot": [0, -0.86, 0.88],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 4 * BEAT, "loc": [0, 0, 0], "rot": [-58, 0, 0], "ease": "inout"}]}],
                "cam": [orbit(0, 4.3, -30, 2.2, c=(0, -1.0, 0.5), focal=30, ease="lin"),
                        orbit(SECS["s5_hood"], 3.7, -16, 2.5, c=(0, -1.2, 0.5), focal=30, ease="out2")]},
    # 6. engine cover opens (louvred lid, "Engine Bay" scan under it), high rear 3/4
    "s6_engine": { "base": [f"{P}/comp_engine.blend"],
                  "parts": [{"blend": f"{P}/enginer_cover.blend", "pivot": [0, 1.63, 0.9],
                             "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                      {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                      {"t": 3 * BEAT, "loc": [0, 0, 0], "rot": [85, 0, 0], "ease": "inout"}]}],
                  "cam": [{"t": 0, "loc": [1.35, 3.6, 2.55], "target": [0, 1.7, 0.8], "focal": 30},
                          {"t": SECS["s6_engine"], "loc": [0.75, 3.35, 2.75], "target": [0, 1.75, 0.8], "focal": 30, "ease": "out2"}]},
    # 7. top-down: from a high rear 3/4 up and over to straight down (front at the top of frame)
    "s7_top": { "base": [CAR], "cam": [
        {"t": 0, "loc": [2.2, 4.6, 4.0], "target": [0, 0.3, 0.5], "focal": 30},
        {"t": SECS["s7_top"], "loc": [0.0, 0.25, 6.9], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}

# 8. exploded view: panels separate on the 23.066 s lift (loudest accent), drift while the camera orbits
# front-right -> rear-right, fly home and LOCK on the 32.350 s accent (heaviest bass), hold 4 beats -> logo
SEP, HOLD, BACK, LOCK = 0.0, 4 * BEAT, 13 * BEAT, 16 * BEAT


def explode(off, rot=(0, 0, 0), delay=0.0):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": HOLD, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": BACK, "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},  # slow drift outward
            {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_explode.blend"],
    "parts": [
        {"blend": f"{P}/x_hood.blend", "keys": explode((0, -0.25, 0.95), (-12, 0, 0))},
        {"blend": f"{P}/x_fbumper.blend", "keys": explode((0, -1.0, -0.05))},
        {"blend": f"{P}/x_fender.blend", "keys": explode((-0.75, 0, 0.18), (0, -8, 0), 0.05)},
        {"blend": f"{P}/x_skirt.blend", "keys": explode((-0.65, 0, -0.18), delay=0.05)},
        {"blend": f"{P}/x_ecover.blend", "keys": explode((0, 0.15, 0.85), (20, 0, 0), 0.1)},
        {"blend": f"{P}/x_rbumper.blend", "keys": explode((0, 0.95, 0.05))},
        {"blend": f"{P}/x_diffuser.blend", "keys": explode((0, 0.75, -0.35), delay=0.1)},
    ],
    # radius swells side-on (exploded length ~6.6 m spans the 9:16 width there); keyed every 1/12 of the move: linear loc interpolation between far-apart keys would cut a chord toward the car
    "cam": [orbit(SECS["s8_explode"] * k / 12, 7.5 + 1.8 * math.sin(math.pi * k / 12), -50 - 75 * (k / 12), 3.0 - 0.3 * (k / 12),
                  c=(0.1, -0.6 + 1.0 * (k / 12), 0.5), focal=28, ease="lin", tz=0.4) for k in range(13)]}


# ---------------------------------------------------------------- v2 (user: "starts too cropped, doesn't focus on the
# subsystems, doesn't zoom in on the bumpers/skirts") - wider opening; explode becomes progressive like the Temerario
# reference: one GLOBAL part timeline (video seconds) seen through three cameras cut on the track's accents.
SECS.update({"s1_wide": 152 / 30, "s8a_front": 139 / 30, "s8b_side": 70 / 30, "s8c_wide": 139 / 30})
T8 = {"s8a_front": 23.066, "s8b_side": 831 / 30, "s8c_wide": 901 / 30}  # sub-shot start times (video s)
G_DRIFT, G_HOME, G_LOCK = 31.189, 31.189, 32.350  # fly home 31.189 -> LOCK on the 32.350 accent

# part: (offset m, rot deg, separate start, separate end) in video seconds; staggered a beat apart
PARTS_G = {
    "x_fbumper": ((0, -1.0, -0.08), (0, 0, 0), 23.066, 24.807),
    "x_fender": ((-0.75, 0, 0.18), (0, -8, 0), 23.646, 25.387),
    "x_hood": ((0, -0.25, 0.95), (-12, 0, 0), 24.227, 25.967),
    "x_skirt": ((-0.65, 0, -0.18), (0, 0, 0), 27.708, 29.449),
    "x_rbumper": ((0, 0.95, 0.05), (0, 0, 0), 28.288, 30.029),
    "x_diffuser": ((0, 0.75, -0.35), (0, 0, 0), 28.868, 30.609),
    "x_ecover": ((0, 0.15, 0.85), (20, 0, 0), 29.449, 30.609),
}


def parts_for(shot):
    t0 = T8[shot]
    out = []
    for name, (off, rot, a, b) in PARTS_G.items():
        keys = [{"t": -100, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": a - t0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": b - t0, "loc": list(off), "rot": list(rot), "ease": "out"},
                {"t": G_HOME - t0, "loc": [o * 1.04 for o in off], "rot": list(rot), "ease": "lin"},
                {"t": G_LOCK - t0, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]
        out.append({"blend": f"{P}/{name}.blend", "keys": keys})
    return out


def arc(t1, n, r0, r1, a0, a1, h0, h1, c0, c1, focal, tz=None):
    """Orbit keyed every 1/n (linear loc between far keys would cut a chord toward the car)."""
    ks = []
    for k in range(n + 1):
        u = k / n
        c = tuple(x + (y - x) * u for x, y in zip(c0, c1))
        ks.append(orbit(t1 * u, r0 + (r1 - r0) * u, a0 + (a1 - a0) * u, h0 + (h1 - h0) * u, c=c, focal=focal,
                        ease="lin", tz=tz))
    return ks


SHOTS.update({
    # whole car in frame from frame 1 (v1 opened cropped into the doors/nose)
    "s1_wide": {"base": [CAR], "cam": arc(SECS["s1_wide"], 6, 7.4, 7.4, -36, -66, 1.25, 1.35, (0, 0, 0.55), (0, 0, 0.55), 30)},
    # front subsystem close: bumper slides forward-down, fender out, hood lifts - camera low front-right, slow arc
    "s8a_front": {"base": [f"{P}/comp_explode.blend"], "parts": parts_for("s8a_front"),
                  "cam": arc(SECS["s8a_front"], 6, 3.9, 4.3, -58, -38, 1.0, 1.35, (-0.25, -2.35, 0.5), (-0.2, -2.25, 0.6), 28)},
    # side subsystem close: skirt drops off the sill toward the lens, rear bumper + diffuser pull back behind it
    "s8b_side": {"base": [f"{P}/comp_explode.blend"], "parts": parts_for("s8b_side"), "cam": [
        {"t": 0, "loc": [-3.1, -0.95, 0.55], "target": [-0.7, 0.45, 0.35], "focal": 28},
        {"t": SECS["s8b_side"], "loc": [-3.1, 0.35, 0.6], "target": [-0.6, 1.55, 0.4], "focal": 28, "ease": "lin"}]},
    # wide: everything out, fly home and LOCK on 32.350, hold to the logo
    "s8c_wide": {"base": [f"{P}/comp_explode.blend"], "parts": parts_for("s8c_wide"),
                 "cam": arc(SECS["s8c_wide"], 6, 8.8, 7.6, -112, -130, 3.0, 2.6, (0.1, 0.0, 0.5), (0.1, 0.4, 0.5), 28, tz=0.4)},
})


# ---------------------------------------------------------------- v3 = director's plan (projects/ferrari-296/director.md)
# Reviewer on v2: "focus on specific sections; if you open the hood, hold that shot and also pull the front bumper out and
# show off the bumper"; "minimize redundant frames". Front = ONE held shot (lamp -> hood opens and stays -> bumper out,
# turned about the vertical axis to show its scanned inner face). Parts carry their pose across shots (video seconds).
SECS.update({"f5_front": 261 / 30, "x_side": 139 / 30, "x_lock": 139 / 30})
T8.update({"f5_front": 431 / 30, "x_side": 762 / 30, "x_lock": 901 / 30})
Z3 = [0, 0, 0]


def _k(t, loc=Z3, rot=Z3, ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}


def _out(off, rot, a, b):
    """translate out a->b (ease out), drift to x1.04 by 31.189, fly home + LOCK 32.350 (ease in)"""
    return [_k(-100), _k(a), _k(b, off, rot, "out"), _k(30.033, off, rot, "lin"),
            _k(31.189, [o * 1.04 for o in off], rot, "lin"), _k(32.350, Z3, Z3, "in")]


BUMP_OUT, BUMP_FAR = (0, -1.00, -0.10), (0, -1.70, -0.10)
PARTS_V3 = {
    "x_hood": ((0, -0.86, 0.88), [_k(-100), _k(14.940), _k(16.100, Z3, (-58, 0, 0)), _k(31.189, Z3, (-58, 0, 0), "lin"),
                                   _k(32.350, Z3, Z3, "in")]),
    "x_fbumper": ((0, -1.775, 0.475), [_k(-100), _k(16.681), _k(17.842, BUMP_OUT, Z3, "out"), _k(18.423, BUMP_OUT, Z3, "lin"),
                                        _k(20.164, BUMP_FAR, (0, 0, 65)), _k(23.067, BUMP_FAR, (0, 0, 80), "lin"),
                                        _k(31.189, BUMP_FAR, (0, 0, 80), "lin"), _k(31.770, BUMP_OUT, Z3),
                                        _k(32.350, Z3, Z3, "in")]),
    # all-reels addendum D: no engine-lid-OPEN scan exists, only "Engine Bay" with the lid OFF -> the louvre lifts straight
    # off (removed), never hinges open. Home through x_side (V3 time < 30.02), out for x_lock; x_rear animates the lift.
    "x_ecover": (None, [_k(-100), _k(30.02), _k(30.033, (0, 0.10, 0.80), Z3, "lin"), _k(31.189, (0, 0.10, 0.83), Z3, "lin"),
                        _k(32.350, Z3, Z3, "in")]),
    "x_fender": (None, _out((-0.50, 0, 0.45), (0, -10, 0), 25.400, 26.548)),
    "x_skirt": (None, _out((-0.40, 0, -0.28), Z3, 25.981, 27.129)),
    "x_rbumper": (None, _out((0, 0.95, 0.05), Z3, 27.708, 28.868)),
    "x_diffuser": (None, _out((0, 0.75, -0.35), Z3, 28.288, 29.449)),
}


def parts_v3(shot):
    t0 = T8[shot]
    out = []
    for name, (pivot, keys) in PARTS_V3.items():
        p = {"blend": f"{P}/{name}.blend", "keys": [dict(k, t=k["t"] - t0) for k in keys]}
        if pivot:
            p["pivot"] = list(pivot)
        out.append(p)
    return out


def _cam(rows, t0):
    return [{"t": round(t - t0, 4), "loc": list(l), "target": list(g), "focal": f, "ease": e} for t, l, g, f, e in rows]


F5 = [(14.367, (-1.60, -3.60, 0.85), (-0.55, -2.00, 0.68), 32, "inout"),
      (14.940, (-1.75, -3.85, 1.05), (-0.40, -1.90, 0.65), 32, "inout"),
      (16.100, (-2.05, -4.35, 1.90), (0.00, -1.40, 0.70), 30, "inout"),
      (16.681, (-2.25, -4.40, 1.85), (0.00, -1.50, 0.65), 30, "inout"),
      (17.842, (-2.80, -4.55, 1.35), (-0.05, -2.55, 0.50), 30, "inout"),
      (18.423, (-3.05, -4.45, 1.25), (-0.05, -2.75, 0.48), 30, "inout"),
      (19.003, (-3.35, -4.15, 1.15), (-0.05, -3.05, 0.46), 30, "lin"),
      (19.584, (-3.45, -3.55, 1.45), (-0.05, -3.25, 0.45), 30, "lin"),
      # raised ~20 deg (level camera made the turned bumper a flat strip); nose stays at screen-left for context
      (20.164, (-3.40, -3.10, 1.60), (-0.10, -3.25, 0.42), 30, "inout"),
      (21.326, (-2.95, -3.05, 1.50), (-0.10, -3.25, 0.42), 31, "inout"),
      (23.067, (-2.45, -3.00, 1.30), (-0.10, -3.25, 0.40), 34, "out")]
XS = [(25.400, (-3.30, -1.60, 0.95), (-0.70, -0.60, 0.40), 28, "inout"),
      (30.033, (-3.40, 1.20, 1.05), (-0.60, 1.90, 0.45), 28, "inout")]

SHOTS.update({
    "f5_front": {"base": [f"{P}/comp_explode.blend"], "parts": parts_v3("f5_front"), "cam": _cam(F5, T8["f5_front"])},
    "x_side": {"base": [f"{P}/comp_explode.blend"], "parts": parts_v3("x_side"), "cam": _cam(XS, T8["x_side"])},
    "x_lock": {"base": [f"{P}/comp_explode.blend"], "parts": parts_v3("x_lock"),
               # widened start (scene-director 4c / rule A: the 30 % preview clipped the pulled rear parts at frame-left)
               "cam": arc(SECS["x_lock"], 8, 8.8, 6.4, -95, -105, 4.5, 3.4, (0, 0.45, 0.5), (0, 0.1, 0.5), 30, tz=0.4)},
})


# ---------------------------------------------------------------- v4 = scene-director's order (direction.md) + rules A-D
# Front -> side -> rear travel; bumper-removed state scans get hero close-ups (rule C). Parts frozen at the pose the
# previous shot left them in (state_at), so every cut is continuous.
def _ease(u, kind):
    u = min(1.0, max(0.0, u))
    return {"in": u ** 3, "out": 1 - (1 - u) ** 3, "lin": u, "in2": u * u, "out2": 1 - (1 - u) ** 2}.get(kind, u * u * (3 - 2 * u))


def state_at(keys, t):
    """Same interpolation as tools/shot.py sample(): returns (loc, rot) at time t."""
    if t <= keys[0]["t"]:
        return keys[0]["loc"], keys[0]["rot"]
    for a, b in zip(keys, keys[1:]):
        if t <= b["t"]:
            k = _ease((t - a["t"]) / max(1e-9, b["t"] - a["t"]), b.get("ease", "inout"))
            return ([x + (y - x) * k for x, y in zip(a["loc"], b["loc"])], [x + (y - x) * k for x, y in zip(a["rot"], b["rot"])])
    return keys[-1]["loc"], keys[-1]["rot"]


def frozen_parts(v3_time, animate=None):
    """Every part held at its PARTS_V3 pose at v3_time; `animate` = {name: local key list} overrides."""
    out = []
    for name, (pivot, keys) in PARTS_V3.items():
        if animate and name in animate:
            ks = animate[name]
        else:
            loc, rot = state_at(keys, v3_time)
            ks = [_k(-100, loc, rot)]
        p = {"blend": f"{P}/{name}.blend", "keys": ks}
        if pivot:
            p["pivot"] = list(pivot)
        out.append(p)
    return out


SECS.update({"F_hero": 139 / 30, "R_hero": 139 / 30})
B = BEAT
SHOTS.update({
    # FRONT BUMPER REMOVED: f5's end state (hood open - scanned propped open in Front Fully Removed; bumper out + turned);
    # camera on the right side of the open nose, ~35 deg down, slow push on the exposed structure behind the bumper
    "F_hero": {"base": [f"{P}/comp_explode.blend"], "parts": frozen_parts(23.067), "cam": _cam([
        (0.0, (-1.55, -3.20, 1.55), (-0.25, -2.05, 0.80), 30, "inout"),  # aim raised 0.25: structure centred (rule A)
        (4 * B, (-1.10, -2.95, 1.30), (-0.20, -2.08, 0.77), 33, "inout"),
        (SECS["F_hero"], (-0.85, -2.80, 1.15), (-0.15, -2.10, 0.75), 36, "inout")], 0.0)},
    # REAR BUMPER REMOVED -> ENGINE BAY: x_side's end state; louvre lifts straight OFF on the 27.708 accent (local 4 beats)
    "R_hero": {"base": [f"{P}/comp_explode.blend"],
               "parts": frozen_parts(30.02, animate={"x_ecover": [_k(-100), _k(4 * B), _k(6 * B, (0, 0.10, 0.80), Z3, "out")]}),
               "cam": _cam([
                   (0.0, (-1.20, 4.60, 2.00), (-0.20, 2.15, 0.55), 30, "inout"),
                   (4 * B, (-0.95, 4.05, 1.85), (-0.15, 2.05, 0.60), 30, "inout"),
                   (SECS["R_hero"], (-0.70, 3.70, 2.80), (0.00, 1.75, 0.75), 32, "inout")], 0.0)},
})


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + (0 if name == "s1_turntable" else 1 / 15), "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
