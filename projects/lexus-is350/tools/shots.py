"""Shot specs for the Lexus IS350 2026 facelift Temerario-style scan reel -> JSON for
projects/lexus-is350/tools/shot.py (copy of the ferrari-296 keyframed renderer: house silver look, camera keys, pivoted parts).

    python projects/lexus-is350/tools/shots.py preview|final [shot ...]    # writes specs, prints their paths

FACELIFT CAR ONLY. The root 'Full Car' scan is an older IS350 (different grille, wheels, plate 9JTY488) - a different
car, not used (see editlog). The facelift set covers the front 1.6 m only (bumper -> A-pillar base, z <= 1.02 m), so
every shot is the facelift front clip, cameras kept forward of its cut-off rear edge.
Prepped frame (metres, same transform as car4.json): nose = -Y, car's right = -X, ground Z=0; clip y -2.37..-0.76.
Durations come from timing.json (the track's kick grid); each shot renders one extra 15 fps frame.
"""
import json
import math
import os
import sys

M = "/home/user/media/lexus-is350"
P = f"{M}/prep"
OUT = f"{M}/renders"
SPECS = f"{M}/specs"
HERE = os.path.dirname(os.path.abspath(__file__))
HINGE = json.load(open(os.path.join(HERE, "..", "hinge.json")))

FE = f"{P}/fe_front_end_hood_closed.blend"   # facelift 'Front End Hood Closed', 3 mm (no hood skin captured)
FE2 = f"{P}/fl_fe2.blend"                     # same, 2 mm: close-ups
HOOD = f"{P}/fl_hood_closed.blend"            # facelift hood from 'Hood Open', rotated shut on the fitted hinge
CLIP = [FE, HOOD]                             # assembled facelift front clip
CLIP2 = [FE2, HOOD]

TIMING = {"s1_front34R": 4.6, "s2_front34L": 4.0, "s3_grille": 1.5, "s4_lamp": 1.5, "s5_hood": 3.0, "s6_top": 2.0,
          "s7_explode": 10.0, "s8_hero": 4.0, "x_sep": 0.0, "x_out": 1.5, "x_back": 6.0, "x_lock": 8.0}
_tj = os.path.join(HERE, "..", "timing.json")
if os.path.exists(_tj):
    TIMING.update(json.load(open(_tj)))


def orbit(t, r, ang_deg, h, c=(0, -1.75, 0.45), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(secs, r0, r1, a0, a1, h0, h1, c0, c1, focal=30, tz=None, n=8, ease="inout"):
    """Orbit sampled in n segments (linear keys between far-apart points would cut a chord toward the car);
    the easing is applied to the whole move by remapping the parameters."""
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
    # 1. low front-right 3/4 turntable of the facelift front end, moving from frame 1
    "s1_front34R": {"base": CLIP, "cam": arc(S["s1_front34R"], 3.15, 2.95, -26, -46, 0.6, 0.7,
                                              (-0.05, -1.95, 0.42), (-0.05, -1.85, 0.42), focal=30, ease="out")},
    # 2. front-left 3/4 orbit, higher, swinging toward the nose
    "s2_front34L": {"base": CLIP, "cam": arc(S["s2_front34L"], 3.3, 3.15, 52, 36, 1.15, 1.0,
                                              (0.12, -1.75, 0.42), (0.1, -1.8, 0.42), focal=30, ease="out")},
    # 3. extreme close-up: left grille corner + fog intake (dealer plate frame and the speckled hood top kept out)
    "s3_grille": {"base": CLIP2, "cam": [
        {"t": 0, "loc": [1.45, -3.3, 0.72], "target": [0.58, -2.3, 0.5], "focal": 45},
        {"t": S["s3_grille"], "loc": [1.2, -3.45, 0.68], "target": [0.48, -2.32, 0.5], "focal": 45, "ease": "inout"}]},
    # 4. extreme close-up: right headlamp + corner intake
    "s4_lamp": {"base": CLIP2, "cam": [
        {"t": 0, "loc": [-1.75, -3.15, 0.85], "target": [-0.66, -2.12, 0.6], "focal": 40},
        {"t": S["s4_lamp"], "loc": [-1.45, -3.35, 0.78], "target": [-0.58, -2.18, 0.56], "focal": 40, "ease": "inout"}]},
    # 5. hood opens on the fitted hinge; -60 deg lands exactly on the 'Hood Open' capture; bay from 'Bumper and Hood
    #    Removed'
    "s5_hood": {"base": [f"{P}/fl_comp_hood.blend"],
                "parts": [{"blend": HOOD, "pivot": HINGE["pivot"],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 0.5, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": S["s5_hood"] - 0.9, "loc": [0, 0, 0], "rot": [HINGE["open_deg"], 0, 0],
                                     "ease": "inout"}]}],
                "cam": arc(S["s5_hood"], 3.9, 3.5, -30, -16, 1.9, 2.15, (0, -1.6, 0.55), (0, -1.65, 0.55), focal=30,
                           ease="out")},
    # 6. top-down: from high in front, up and over to straight down (nose at the top of the frame)
    "s6_top": {"base": CLIP, "cam": [
        {"t": 0, "loc": [-1.2, -4.6, 2.9], "target": [0, -1.75, 0.4], "focal": 30},
        {"t": S["s6_top"], "loc": [0.0, -1.62, 4.6], "target": [0, -1.6, 0.4], "focal": 30, "ease": "inout"}]},
    # 8. hero closer: low, nose-on push-in toward the new grille
    "s8_hero": {"base": CLIP, "cam": arc(S["s8_hero"], 3.4, 2.75, 6, -3, 0.4, 0.44, (0, -1.85, 0.45), (0, -1.95, 0.45),
                                          focal=30, ease="out")},
}


def explode(off, rot=(0, 0, 0), delay=0.0, back_delay=0.0):
    """separate (ease-out) -> slow drift outward -> fly home (ease-in) and lock on x_lock."""
    sep, out, back, lock = S["x_sep"] + delay, S["x_out"] + delay, S["x_back"] + back_delay, S["x_lock"]
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": sep, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": out, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": back, "loc": [o * 1.07 for o in off], "rot": list(rot), "ease": "lin"},
            {"t": lock, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


# 7. exploded front end (all facelift scans): outer layers fly first (fog covers, bumper shell), then what was behind
# them (ducts, radar, top bracket), hood lifts on top; panels stack up/forward (portrait), then all lock home.
SHOTS["s7_explode"] = {
    "base": [f"{P}/fl_comp_explode.blend"],
    "parts": [
        {"blend": HOOD, "keys": explode((0, 0.1, 1.45), (-10, 0, 0), 0.10)},
        {"blend": f"{P}/fl_shell.blend", "keys": explode((0, -0.55, 0.5))},
        {"blend": f"{P}/x_fog_L.blend", "keys": explode((0.3, -0.85, 0.3), (0, 0, -12))},
        {"blend": f"{P}/x_fog_R.blend", "keys": explode((-0.3, -0.85, 0.3), (0, 0, 12))},
        {"blend": f"{P}/x_duct_L.blend", "keys": explode((0.3, -0.3, 0.2), delay=0.2, back_delay=0.15)},
        {"blend": f"{P}/x_duct_R.blend", "keys": explode((-0.3, -0.3, 0.2), delay=0.2, back_delay=0.15)},
        {"blend": f"{P}/x_radar.blend", "keys": explode((0, -0.25, 0.85), delay=0.25, back_delay=0.2)},
        {"blend": f"{P}/x_bracket.blend", "keys": explode((0, -0.15, 1.15), delay=0.3, back_delay=0.1)},
    ],
    "cam": arc(S["s7_explode"], 4.4, 4.15, -22, -48, 1.95, 1.75, (0, -2.0, 1.0), (0, -1.85, 0.9), focal=30,
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
