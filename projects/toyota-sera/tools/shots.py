"""Shot specs for the Toyota Sera Temerario-style reel -> JSON for tools/shot.py.

    python projects/toyota-sera/tools/shots.py preview|final [shot ...]   # writes specs, prints their paths

Scan frame (prepped, metres): nose = -Y, car's right = -X, ground z = 0; 3.84 x 1.72 x 1.24 m. Front axle ~y -1.15.
Timing: toyota-sera_track.mp3, 100.0 BPM; cuts in project.yaml. Shots render a little longer than they play.
Camera moves use linear / ease-out segments so any sub-window still moves from frame 1.
"""
import json
import math
import os
import sys

P = "/home/user/media/toyota-sera/prep"
C = "/home/user/media/toyota-sera/clean"
OUT = "/home/user/media/work/sera/renders"
SPECS = "/home/user/media/work/sera/specs"
BEAT = 0.59999  # toyota-sera_track.mp3 kick grid: 0.0355 + 0.59999 n (100.0 BPM), tools/accents.py
EXPOSURE = -0.35  # measured: 0 EV clipped 9 % of car pixels in a front 3/4 (p90 249); Temerario ref p90 ~231

CAR = f"{P}/car4.blend"      # 4 mm: full-car moves
CAR_HI = f"{P}/car3.blend"   # 3 mm: close-ups
SECS = {"s1_turntable": 6.0, "s2_rear": 5.0, "s3_wheel": 3.0, "s4_nose": 3.0, "s5_hood": 3.4, "s6_doors": 4.6,
        "s7_top": 2.8, "s8_explode": 11.0}


def hinge(name):
    return json.load(open(f"{C}/{name}_hinge.json"))


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(t0, t1, r0, r1, a0, a1, h0, h1, c=(0, 0, 0.55), focal=30, n=8, ease_last="out2", tz=None):
    """Orbit keyed every 1/n of the move (linear loc between far-apart keys would cut a chord toward the car)."""
    ks = []
    for k in range(n + 1):
        u = k / n
        if ease_last == "out2":
            w = 1 - (1 - u) ** 2
        elif ease_last == "inout":
            w = u * u * (3 - 2 * u)
        else:
            w = u
        ks.append(orbit(t0 + (t1 - t0) * u, r0 + (r1 - r0) * w, a0 + (a1 - a0) * w, h0 + (h1 - h0) * w, c, focal,
                        "lin", tz))
    return ks


def swing(name, t0, t1, frac=1.0, hold_from=0.0):
    h = hinge(name)
    return {"blend": f"{P}/{name}_panel.blend", "pivot": h["pivot"], "axis": h["axis"],
            "keys": [{"t": 0, "loc": [0, 0, 0], "ang": 0}, {"t": t0, "loc": [0, 0, 0], "ang": 0},
                     {"t": t1, "loc": [0, 0, 0], "ang": h["open_deg"] * frac, "ease": "inout"}]}


S = SECS
SHOTS = {
    # 1. slow low front 3/4 turntable (car's right), moving from frame 1 - the hook
    "s1_turntable": {"base": [CAR], "cam": arc(0, S["s1_turntable"], 3.9, 3.7, -28, -62, 0.95, 1.05, focal=30, ease_last="lin")},
    # 2. rear 3/4 orbit on the other side, slight rise
    "s2_rear": {"base": [CAR], "cam": arc(0, S["s2_rear"], 3.8, 3.6, 150, 122, 0.85, 1.25, focal=30, ease_last="lin")},
    # 3. extreme close-up: front-right wheel + arch, slide toward the nose
    "s3_wheel": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.95, -0.45, 0.42], "target": [-0.80, -1.10, 0.32], "focal": 40},
        {"t": S["s3_wheel"], "loc": [-1.90, -1.75, 0.40], "target": [-0.80, -1.20, 0.32], "focal": 40, "ease": "lin"}]},
    # 4. detail: slide across the nose - headlamp, grille slot, bumper vents (the tail panel read flat: blank plate)
    "s4_nose": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.15, -2.95, 0.80], "target": [-0.45, -1.85, 0.62], "focal": 38},
        {"t": S["s4_nose"], "loc": [0.55, -3.10, 0.74], "target": [0.25, -1.85, 0.60], "focal": 38, "ease": "lin"}]},
    # 5. hood opens on its fitted hinge (engine bay from 'Hood open'), camera drifts in and up
    "s5_hood": {"base": [f"{P}/hood_base.blend"], "parts": [swing("hood", BEAT, 4 * BEAT)],
                "cam": arc(0, S["s5_hood"], 3.6, 3.2, -34, -16, 1.9, 2.25, c=(0, -0.95, 0.55), focal=30, ease_last="lin")},
    # 6. both butterfly doors swing up on their fitted hinges (interior from 'Door Open'); front-right 3/4
    "s6_doors": {"base": [f"{P}/doors_base.blend"], "parts": [swing("door", BEAT, 5 * BEAT), swing("door2", BEAT, 5 * BEAT)],
                 "cam": arc(0, S["s6_doors"], 4.5, 4.1, -62, -38, 1.25, 1.6, c=(0, -0.1, 0.7), focal=30, ease_last="lin")},
    # 7. top-down: high rear 3/4 up and over to straight down (front at the top of frame)
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [1.6, 3.2, 2.9], "target": [0, 0.3, 0.5], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, 0.18, 5.0], "target": [0, 0.0, 0.5], "focal": 30, "ease": "out2"}]},
}

# 8. exploded view on the music: the shot starts ON the 24.035 s phrase downbeat and the panels separate right there,
# ease out over 3 beats, drift through the kick break (25.2-27.6 s), fly home from beat 12 and LOCK on the 33.635 s
# phrase downbeat (beat 16), hold 2 beats -> logo.
EXPLODE = {"SEP": 0.0, "HOLD": 3 * BEAT, "BACK": 12 * BEAT, "LOCK": 16 * BEAT}
OFFSETS = {  # panels stack in layers ABOVE the car (Temerario 25-31 s; portrait-friendly, never at the lens); doors also swing open as they lift
    "hood": ((0, 0.05, 1.35), None),
    "front_bumper_3mm": ((0, -0.35, 0.75), None),
    "rear_bumper_only_3mm": ((0, 0.35, 0.85), None),
    "door": ((-0.45, 0.05, 0.65), 0.35),
    "door2": ((0.45, 0.05, 0.65), 0.35),
}


def explode_keys(off, delay, E):
    return [{"t": 0, "loc": [0, 0, 0]}, {"t": E["SEP"] + delay, "loc": [0, 0, 0]},
            {"t": E["HOLD"], "loc": list(off), "ease": "out"},
            {"t": E["BACK"], "loc": [o * 1.06 for o in off], "ease": "lin"},
            {"t": E["LOCK"], "loc": [0, 0, 0], "ease": "in"}]


def explode_shot(E=EXPLODE, secs=S["s8_explode"]):
    parts = []
    for i, (n, (off, swing_frac)) in enumerate(OFFSETS.items()):
        blend = f"{P}/{n}.blend" if n.endswith("mm") else f"{P}/{n}_panel.blend"
        keys = explode_keys(off, 0.05 * (i % 3), E)
        p = {"blend": blend, "keys": keys}
        if swing_frac:
            h = hinge(n); p.update(pivot=h["pivot"], axis=h["axis"])
            a = h["open_deg"] * swing_frac
            for k, ang in zip(keys, [0, 0, a, a, 0]):
                k["ang"] = ang
        else:
            for k in keys:
                k["rot"] = [0, 0, 0]
        parts.append(p)
    n = 12  # orbit front-right -> right side -> rear-right, radius swells side-on
    cam = [orbit(secs * k / n, 5.2 + 1.7 * math.sin(math.pi * k / n), -35 - 110 * (k / n), 3.2 - 0.4 * (k / n),
                 c=(0, -0.2 + 0.4 * (k / n), 0.95), focal=28, ease="lin", tz=0.95) for k in range(n + 1)]
    return {"base": [f"{P}/explode_base.blend"], "parts": parts, "cam": cam}


SHOTS["s8_explode"] = explode_shot()


# ===================================================================================== v3 (director.md, 2026-11-11)
# User v2 brief: order by this car's scan features, travel front -> side -> rear, one section per shot, show parts off,
# progressive explode over several angles, whole car at the open, small logo. Plan: projects/toyota-sera/director.md.
def keys(*ks, focal=30):
    out = []
    for k in ks:
        t, loc, tgt = k[0], k[1], k[2]
        out.append({"t": t, "loc": list(loc), "target": list(tgt), "focal": focal, "ease": k[3] if len(k) > 3 else "lin"})
    return out


def arc2(t0, t1, r0, r1, a0, a1, h0, h1, c0, c1, tz0, tz1, n=8, ease="lin"):
    """arc() with the centre and target height lerped too."""
    ks = []
    for k in range(n + 1):
        u = k / n
        w = 1 - (1 - u) ** 2 if ease == "out2" else u
        c = tuple(a + (b - a) * w for a, b in zip(c0, c1))
        ks.append(orbit(t0 + (t1 - t0) * u, r0 + (r1 - r0) * w, a0 + (a1 - a0) * w, h0 + (h1 - h0) * w, c, 30, "lin",
                        tz0 + (tz1 - tz0) * w))
    return ks


def part(n, keys_, hinge_name=None):
    blend = f"{P}/{n}.blend" if n.endswith("mm") else f"{P}/{n}_panel.blend"
    d = {"blend": blend, "keys": keys_}
    if hinge_name:
        h = hinge(hinge_name); d.update(pivot=h["pivot"], axis=h["axis"])
    return d


def lk(t, loc=(0, 0, 0), rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}


SECS.update({"v3_s1_whole": 5.0, "v3_s3_front": 7.4, "v3_s4_doors": 5.0, "v3_s5_rear": 5.0,
             "v3_g1_front_lift": 3.8, "v3_g2_side_rear_lift": 3.8, "v3_g3a_home": 2.6, "v3_g3b_clean": 2.6})

# S1 whole car, front-right 3/4 push-in (car 79-84 % of the width), moving from frame 1
SHOTS["v3_s1_whole"] = {"base": [CAR], "cam": arc2(0, 5.0, 6.8, 5.6, -42, -30, 1.25, 1.05, (0, -0.10, 0.60),
                                                  (0, -0.35, 0.55), 0.60, 0.55)}
# S3 front section, one held shot: hood opens (b13-16), front bumper slides toward camera (b16-18), tips its inner face up (b18-21)
SHOTS["v3_s3_front"] = {"base": [f"{P}/front_base.blend"],
    "parts": [swing("hood", BEAT, 4 * BEAT),
              part("front_bumper_3mm", [lk(0), lk(4 * BEAT), lk(6 * BEAT, (0, -1.20, -0.10), ease="out"),
                                        lk(9 * BEAT, (0, -1.20, -0.10), (90, 0, 0)), lk(12 * BEAT, (0, -1.20, -0.10), (90, 0, 0))])],
    "cam": keys((0, (-2.6, -4.3, 2.0), (0, -1.3, 0.65)), (2.4, (-2.2, -4.6, 2.3), (0, -1.6, 0.6)),
                (4.2, (-1.5, -4.9, 2.9), (0, -2.3, 0.45), "inout"), (7.4, (-1.0, -4.66, 2.97), (0, -2.7, 0.35), "out2"))}
# S4 side: both butterfly doors (b25-29), side-on from slightly behind, pushing toward the cabin
SHOTS["v3_s4_doors"] = {"base": [f"{P}/doors_base.blend"],
    "parts": [swing("door", BEAT, 5 * BEAT), swing("door2", BEAT, 5 * BEAT)],
    "cam": keys((0, (-4.0, -0.9, 1.25), (-0.3, -0.2, 0.85)), (3.0, (-3.6, 0.3, 1.6), (-0.2, -0.2, 0.95)),
                (5.0, (-3.0, 0.9, 1.9), (-0.1, -0.15, 0.85), "out2"))}
# S5 rear: rear bumper slides toward camera (b33-35), tips inner face up (b35-37), camera rises to straight behind
SHOTS["v3_s5_rear"] = {"base": [f"{P}/rear_base.blend"],
    "parts": [part("rear_bumper_only_3mm", [lk(0), lk(BEAT), lk(3 * BEAT, (0, 1.20, -0.10), ease="out"),
                                            lk(5 * BEAT, (0, 1.20, -0.10), (-90, 0, 0)), lk(8.4 * BEAT, (0, 1.20, -0.10), (-90, 0, 0))])],
    "cam": keys((0, (-2.5, 4.1, 1.1), (0, 1.5, 0.6)), (1.8, (-1.9, 4.5, 2.2), (0, 2.2, 0.5)),
                (5.0, (0.0, 4.75, 2.9), (0, 2.7, 0.35), "out2"))}

# Progressive explode: one global timeline T (s from b40 = 24.035), translate only; each shot = a window of it.
def xkeys(home_until, out_t, off, drift_t, back0, back1, ang=None):
    ks = [{"t": -10, "loc": [0, 0, 0]}, {"t": home_until, "loc": [0, 0, 0]},
          {"t": out_t, "loc": list(off), "ease": "out"},
          {"t": drift_t, "loc": [o * 1.06 for o in off], "ease": "lin"},
          {"t": back0, "loc": [o * 1.06 for o in off], "ease": "lin"},
          {"t": back1, "loc": [0, 0, 0], "ease": "in"}, {"t": 20, "loc": [0, 0, 0], "ease": "lin"}]
    for k in ks:
        if ang is None:
            k["rot"] = [0, 0, 0]
        else:
            k["ang"] = 0.0
    if ang is not None:
        for k in ks[2:5]:
            k["ang"] = ang
    return ks


def explode_parts(shift):
    hd, d1, d2 = hinge("door"), hinge("door2"), None
    specs = [("hood", xkeys(0.0, 1.2, (0, 0.05, 1.35), 7.2, 8.4, 9.6), None),
             ("front_bumper_3mm", xkeys(0.6, 1.8, (0, -0.35, 0.75), 7.2, 8.4, 9.6), None),
             ("door2", xkeys(3.6, 4.8, (0.45, 0.05, 0.65), 7.8, 7.8, 9.0, hinge("door2")["open_deg"] * 0.35), "door2"),
             ("door", xkeys(4.2, 5.4, (-0.45, 0.05, 0.65), 7.8, 7.8, 9.0, hinge("door")["open_deg"] * 0.35), "door"),
             ("rear_bumper_only_3mm", xkeys(4.8, 6.0, (0, 0.35, 0.85), 7.2, 7.2, 8.4), None)]
    out = []
    for n, ks, hn in specs:
        for k in ks:
            k["t"] = round(k["t"] - shift, 4)
        out.append(part(n, ks, hn))
    return out


SHOTS["v3_g1_front_lift"] = {"base": [f"{P}/explode_base.blend"], "parts": explode_parts(0.0),
    "cam": arc2(0, 3.8, 4.6, 4.3, 35, 50, 2.9, 2.7, (0, -1.0, 1.0), (0, -1.0, 1.0), 1.1, 1.1)}
SHOTS["v3_g2_side_rear_lift"] = {"base": [f"{P}/explode_base.blend"], "parts": explode_parts(3.6),
    "cam": arc2(0, 3.8, 5.8, 5.5, 80, 100, 2.4, 2.6, (0, 0.55, 1.0), (0, 0.55, 1.0), 1.15, 1.15)}
_g3cam = arc2(0, 5.0, 6.4, 5.9, 140, 150, 3.0, 2.3, (0, 0.10, 0.70), (0, 0.10, 0.70), 0.9, 0.6, ease="out2")
SHOTS["v3_g3a_home"] = {"base": [f"{P}/explode_base.blend"], "parts": explode_parts(7.2), "cam": _g3cam}
# G3b: the clean car from the lock (T 9.6 = b56) on, same camera continued (t offset 2.4)
SHOTS["v3_g3b_clean"] = {"base": [CAR], "cam": [dict(k, t=round(k["t"] - 2.4, 4)) for k in _g3cam]}


def spec(name, mode, frames=None):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name], "fps": 15, "res": "1080x1920", "res_pct": 75 if final else 30,
          "samples": 12 if final else 6, "exposure": EXPOSURE,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if frames:
        sp["frames"] = frames
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode, ["first", "mid", "last"] if mode == "preview" else None))
