"""Shot specs for the RX-7 FC3S Temerario-style reel -> JSON for tools/shot.py.

    python projects/mazda-rx7-fc/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Prepped frame (m): front = +Y, car's right = +X, car 4.30 x 1.79 (mirrors) x ~1.28 m, wheels touch ~z 0.10.
Shots are rendered a little long; project.yaml trims them to the music's accents.
"""
import json
import math
import os
import sys

P = "/home/user/media/work/rx7/prep"
OUT = "/home/user/media/work/rx7/renders"
SPECS = "/home/user/media/work/rx7/specs"
HINGE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hinge.json")))
CAR = f"{P}/car4.blend"
EXPO = -0.5
BEAT = 0.5661  # mazda-rx7-fc_track.mp3: 106.0 BPM, grid 9.067 + k*BEAT (snare/hit flux peaks, see editlog)   # huracan-evo measured: -0.5 EV puts car-pixel luma at the Temerario ref's (median ~200)

SECS = {"s1_front34": 5.0, "s2_rear34": 5.0, "s3_wheel": 3.6, "s4_nose": 3.6, "s5_mirror": 3.6,
        "s6_hood": 4.0, "s7_top": 2.9}


def orbit(t, r, ang_deg, h, c=(0, 0, 0.6), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (+Y); +90 = car's right (+X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] + r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


S = SECS
SHOTS = {
    # 1. slow front 3/4 turntable, low; moving from frame 1
    "s1_front34": {"base": [CAR], "cam": [orbit(0, 6.4, 18, 0.65, c=(0, 0.2, 0.6), focal=30, ease="lin"),
                                          orbit(S["s1_front34"], 6.2, 40, 0.9, c=(0, 0.1, 0.6), focal=30, ease="out2")]},
    # 2. rear 3/4 orbit on the car's left, slight rise
    "s2_rear34": {"base": [CAR], "cam": [orbit(0, 6.4, -158, 0.7, c=(0, -0.2, 0.6), focal=30, ease="lin"),
                                         orbit(S["s2_rear34"], 6.2, -136, 1.15, c=(0, -0.1, 0.6), focal=30, ease="out2")]},
    # 3. extreme close-up: front right wheel (5-spoke rim scanned), slow slide toward the nose
    "s3_wheel": {"base": [f"{P}/fr_2mm.blend"], "cam": [
        {"t": 0, "loc": [1.6, 0.75, 0.78], "target": [0.8, 1.05, 0.64], "focal": 48},
        {"t": S["s3_wheel"], "loc": [1.6, 1.4, 0.78], "target": [0.8, 1.22, 0.68], "focal": 48, "ease": "inout"}]},
    # 4. nose detail: right pop-up lid, indicator, bumper; slide across the front
    "s4_nose": {"base": [f"{P}/fr_2mm.blend"], "cam": [
        {"t": 0, "loc": [1.75, 3.3, 0.95], "target": [0.5, 1.9, 0.62], "focal": 38},
        {"t": S["s4_nose"], "loc": [0.45, 3.65, 0.85], "target": [0.25, 2.0, 0.58], "focal": 38, "ease": "inout"}]},
    # 5. right mirror / A-pillar / door glide (tail lamps are scan holes - not featured)
    "s5_mirror": {"base": [f"{P}/fr_2mm.blend"], "cam": [
        {"t": 0, "loc": [1.75, 1.5, 1.2], "target": [0.85, 0.45, 0.95], "focal": 40},
        {"t": S["s5_mirror"], "loc": [1.85, 0.9, 1.05], "target": [0.85, 0.2, 0.9], "focal": 40, "ease": "inout"}]},
    # 6. hood opens on its fitted hinge to the captured 'Hood Up' angle; engine bay from 'Hood Off Bumper Off'
    "s6_hood": {"base": [f"{P}/comp_hood.blend"],
                "parts": [{"blend": f"{P}/hood.blend", "pivot": HINGE["p"],
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 5 * BEAT, "loc": [0, 0, 0], "rot": [HINGE["open_deg"], 0, 0], "ease": "inout"}]}],
                "cam": [orbit(0, 3.9, 34, 2.0, c=(0, 1.0, 0.6), focal=30, ease="lin"),
                        orbit(S["s6_hood"], 3.4, 18, 2.4, c=(0, 1.1, 0.6), focal=30, ease="out2")]},
    # 7. top-down: from a high rear 3/4 up and over to straight down (front at the top of the frame), slow spin
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [2.0, -4.0, 3.6], "target": [0, -0.3, 0.5], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, -0.2, 6.4], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}


def spec(name, mode):
    s = SHOTS[name]
    d = {"base": s["base"], "parts": s.get("parts", []), "camera": {"keys": s["cam"], "sensor": 20.25},
         "seconds": SECS[name], "fps": 15, "res": "1080x1920", "exposure": EXPO}
    if mode == "preview":
        d.update(res_pct=30, samples=8, frames=["first", "mid", "last"], out=f"{OUT}/preview/{name}")
    else:
        d.update(res_pct=75, samples=12, out=f"{OUT}/{s.get('out', name)}")
        if s.get("frames"):
            d["frames"] = s["frames"]
    return d


# 8. exploded view over comp_explode (car minus hood / front face / rear bumper + the bumper-off/hood-off state
# scans). Panels stack ABOVE and out from the car (portrait-friendly), drift while the camera orbits front-right ->
# right-rear, then fly home and lock. Times (s from shot start) are set from the music: EXPL = (sep, out, back, lock, end).
EXPL = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "explode_times.json"))) \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "explode_times.json")) \
    else {"sep": 0.6, "out": 2.4, "back": 7.0, "lock": 8.6, "end": 10.4}


def explode(off, rot=(0, 0, 0), delay=0.0, drift=1.06):
    E = EXPL
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": E["sep"] + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": E["out"] + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            {"t": E["back"], "loc": [o * drift for o in off], "rot": list(rot), "ease": "lin"},
            {"t": E["lock"], "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


SECS["s8_explode"] = EXPL["end"]
SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_explode.blend"],
    "parts": [
        {"blend": f"{P}/hood.blend", "keys": explode((0, 0.25, 1.25), (-10, 0, 0))},
        {"blend": f"{P}/fbumper.blend", "keys": explode((0, 0.55, 0.75), (8, 0, 0), delay=0.15)},
        {"blend": f"{P}/rbumper.blend", "keys": explode((0, -0.55, 0.75), (-8, 0, 0), delay=0.3)},
    ],
    # sampled along the arc (keys interpolate loc linearly -> a 2-key 70 deg move cuts the chord and crops the car)
    "cam": [orbit(EXPL["end"] * u, 7.6 + 0.3 * e, 30 + 34 * e, 2.6 + 0.4 * e, c=(0.15, 0.5 - 0.1 * e, 0.75), focal=30, ease="lin", tz=1.05)
            for u, e in [(i / 10, (1 - math.cos(math.pi * i / 10)) / 2) for i in range(11)]],
}


# ---- v2 (director.md 2026-11-11): one section at a time, front -> side -> rear, then reassembly ----
CARDP = f"{P}/car4_dp.blend"            # rear plate flattened (tools/deplate.py), same transform (--like car4.json)
EXPDP = f"{P}/comp_explode_dp.blend"    # comp_explode with the rear plate flattened
HP = HINGE["p"]; HO = HINGE["open_deg"]
def K(t, loc=(0, 0, 0), rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}
def C(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": list(loc), "target": list(tgt), "focal": focal, "ease": ease}
SECS.update({"s9_hoodoff": 4.2, "s10_fbumper": 2.4, "s11_fsupport": 3.0, "s12_rbumper": 4.7,
             "s13_reassemble": 4.7, "s13b_clean": 4.7})
# c4: the CAPTURED open hood (hood_up.blend, cut from the Hood Up scan, stored closed -> rot X = HO is its scanned pose)
# lifts off the hinge; camera starts on s6's last pose and moves over the engine bay (Hood Off Bumper Off)
SHOTS["s9_hoodoff"] = {"base": [f"{P}/comp_hood.blend"],
    "parts": [{"blend": f"{P}/hood_up.blend", "pivot": HP, "keys": [
        K(0, rot=(HO, 0, 0)), K(0.567, rot=(HO, 0, 0)), K(1.699, (0, -0.10, 0.60), (HO, 0, 0), "out"),
        K(2.831, (0, -0.30, 1.70), (25, 0, 0)), K(4.2, (0, -0.40, 2.40), (18, 0, 0), "in")]}],   # lifts clean out of the top of frame
    "cam": [C(0, (1.076, 4.331, 2.391), (0, 1.098, 0.60)), C(0.567, (1.076, 4.331, 2.391), (0, 1.098, 0.60), ease="lin"),
            C(3.963, (0.70, 3.80, 2.75), (0.12, 1.25, 0.80)), C(4.2, (0.70, 3.80, 2.75), (0.12, 1.25, 0.80), ease="lin")]}
# c5: front bumper (Front Face part scan; inner face scanned) straight off its mounts toward the lens, tips to show inside
SHOTS["s10_fbumper"] = {"base": [EXPDP],
    "parts": [{"blend": f"{P}/fbumper.blend", "keys": [
        K(0), K(0.10, ease="lin"), K(1.133, (0, 0.55, 0), ease="out"), K(2.265, (0, 0.85, -0.25), (-110, 0, 0)),
        K(2.4, (0, 0.86, -0.26), (-110, 0, 0), "lin")]}],
    "cam": [C(0, (1.25, 5.90, 1.40), (0.0, 2.30, 0.70)), C(2.265, (0.50, 5.85, 1.95), (0.0, 2.60, 0.60)),
            C(2.4, (0.50, 5.85, 1.95), (0.0, 2.60, 0.60), ease="lin")]}
# c6: hero beat - what is behind the front bumper (Hood Off Bumper Off): radiator support, crash beam, brackets
SHOTS["s11_fsupport"] = {"base": [EXPDP],
    "parts": [{"blend": f"{P}/fbumper.blend", "keys": [
        K(0, (0, 0.86, -0.26), (-110, 0, 0)), K(1.3, (0, 0.95, -1.10), (-112, 0, 0)), K(3.0, (0, 0.95, -1.15), (-112, 0, 0), "lin")]}],
    "cam": [C(0, (1.15, 3.95, 1.05), (0.10, 1.88, 0.62)), C(2.83, (0.45, 3.45, 0.95), (0.30, 1.90, 0.58)),
            C(3.0, (0.45, 3.45, 0.95), (0.30, 1.90, 0.58), ease="lin")]}
# c9: rear bumper (outer skin only -> translate, no flip) back off its mounts, then push onto the crash beam (Rear Bumper Removed)
SHOTS["s12_rbumper"] = {"base": [EXPDP],
    "parts": [{"blend": f"{P}/rbumper.blend", "keys": [
        K(0), K(1.132, ease="lin"), K(2.264, (0, -0.60, 0), ease="out"), K(3.396, (0.10, -1.00, -1.20)),
        K(4.7, (0.10, -1.02, -1.25), ease="lin")]}],
    "cam": [C(0, (2.60, -4.60, 1.15), (0.10, -1.55, 0.75)), C(2.264, (2.30, -4.55, 1.05), (0.20, -1.75, 0.72)),
            C(4.30, (1.10, -4.45, 0.80), (0.30, -2.05, 0.70)), C(4.7, (1.10, -4.45, 0.80), (0.30, -2.05, 0.70), ease="lin")]}
# c10: all three fly home (rear first - we are at the rear), hood locks on the 32.277 hit; frames >= 52 (t >= 3.40) are
# the clean full car (s13b_clean renders those frames into the same folder with the same camera)
CAM13 = [C(0, (-4.70, 5.30, 5.40), (0.0, 0.10, 0.70), 30), C(4.53, (-3.90, 4.40, 4.30), (0.0, 0.0, 0.55), 30),
         C(4.7, (-3.90, 4.40, 4.30), (0.0, 0.0, 0.55), 30, "lin")]   # high front-LEFT: s1 opener is low front-right
SHOTS["s13_reassemble"] = {"base": [EXPDP], "frames": list(range(1, 52)), "cam": CAM13,
    "parts": [{"blend": f"{P}/rbumper.blend", "keys": [K(0, (0.10, -1.00, -1.20)), K(0.566, (0.10, -1.00, -1.20), ease="lin"), K(1.698)]},
              {"blend": f"{P}/fbumper.blend", "keys": [K(0, (0, 0.95, -1.15), (-112, 0, 0)), K(1.132, (0, 0.95, -1.15), (-112, 0, 0), "lin"),
                                                         K(2.264, (0, 0.55, 0)), K(2.830, ease="in")]},
              {"blend": f"{P}/hood.blend", "pivot": HP, "keys": [K(0, (0, -0.20, 1.05), (23, 0, 0)),
                                                                  K(1.698, (0, -0.20, 1.05), (23, 0, 0), "lin"), K(3.396)]}]}
SHOTS["s13b_clean"] = {"base": [CARDP], "frames": list(range(52, 72)), "cam": CAM13, "out": "s13_reassemble"}


if __name__ == "__main__":
    mode = sys.argv[1]
    names = sys.argv[2:] or list(SHOTS)
    os.makedirs(SPECS, exist_ok=True)
    for n in names:
        p = f"{SPECS}/{mode}_{n}.json"
        json.dump(spec(n, mode), open(p, "w"), indent=1)
        print(p)
