"""Shot specs for the Honda S2000 AP1 Temerario-style reel -> JSON for tools/shot.py (copied from ferrari-296).

    python projects/honda-s2000/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Prep frame (metres, car4.json): nose at -Y (front bumper y=-1.88), tail +Y (2.23), car's right = -X, width +-0.93,
roof 1.33, sills at z~0.12 (the car was scanned without wheels; nothing touches z=0). Car centre (0, 0.17).
SECS are the rendered lengths; they are cut to the music's accent grid in project.yaml (src_fps / in).
"""
import json
import math
import os
import sys

P = "/home/user/media/honda-s2000/prep"
OUT = "/home/user/media/work/s2k/renders"
SPECS = "/home/user/media/work/s2k/specs"
CAR = f"{P}/car4.blend"       # 4 mm full car
F2 = f"{P}/front2.blend"      # 2 mm crops for close-ups
R2 = f"{P}/rear2.blend"
C0 = (0.0, 0.17, 0.55)        # orbit centre

# rendered seconds (15 fps); the timeline may use less
# Music: honda-s2000_track.mp3, 138.05 BPM, beat B = 0.43463 s, first kick 0.0565 s (tools/music_grid.py + LS refit).
B = 0.43463
SECS = {"s1_front": 5.6,  # rendered before the track arrived; the timeline uses its first 3.53 s
        "s2_rear": 3.6, "s3_lamp": 1.9, "s4_tail": 1.9, "s4b_flank": 1.9, "s5_front_open": 3.6,
        "s6_trunk": 2.75, "s7_top": 2.75}
M2 = f"{P}/mid2.blend"

LID_HINGE = [0.0, 1.529, 0.874]   # match/lid_hinge.json (fitted to the open lid in the trunk scan)
LID_OPEN = 77.0
HOOD_HINGE = [0.0, -0.31, 0.83]   # rear edge of the hood (no open-hood capture exists)


def orbit(t, r, ang_deg, h, c=C0, focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(t0, t1, r0, r1, a0, a1, h0, h1, c=C0, focal=30, n=8, tz=None):
    """Orbit keyed every 1/n so linear loc interpolation never cuts a chord toward the car; eased overall."""
    keys = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u) if n > 1 else u
        keys.append(orbit(t0 + (t1 - t0) * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e,
                          c, focal, "lin", tz))
    return keys


SHOTS = {
    # 1. low front 3/4 turntable (car's left-front), moving from frame 1 (hook)
    "s1_front": {"base": [CAR], "cam": arc(0, SECS["s1_front"], 5.1, 4.8, 22, 48, 1.3, 1.2, c=(0, 0.0, 0.55), focal=30)},
    # 2. rear 3/4 orbit on the other side, slight rise
    "s2_rear": {"base": [CAR], "cam": arc(0, SECS["s2_rear"], 5.4, 5.1, -160, -132, 1.35, 1.6, c=(0, 0.4, 0.55), focal=30)},
    # 3. extreme close-up: left headlight, slide across it (2 mm crop)
    "s3_lamp": {"base": [F2], "cam": [
        {"t": 0, "loc": [1.45, -2.35, 0.78], "target": [0.55, -1.62, 0.62], "focal": 45},
        {"t": SECS["s3_lamp"], "loc": [0.75, -2.65, 0.74], "target": [0.5, -1.62, 0.62], "focal": 45, "ease": "inout"}]},
    # 4. close-up: right tail lamp + ducktail edge (2 mm crop)
    "s4_tail": {"base": [R2], "cam": [
        {"t": 0, "loc": [-1.55, 3.0, 1.3], "target": [-0.55, 2.12, 0.9], "focal": 45},
        {"t": SECS["s4_tail"], "loc": [-0.85, 3.3, 1.25], "target": [-0.45, 2.15, 0.9], "focal": 45, "ease": "inout"}]},
    # 4b. close-up glide along the left flank: mirror, door line, side marker (2 mm mid crop)
    "s4b_flank": {"base": [M2], "cam": [
        {"t": 0, "loc": [1.75, -0.95, 1.05], "target": [0.85, -0.35, 0.85], "focal": 40},
        {"t": SECS["s4b_flank"], "loc": [1.8, 0.2, 1.0], "target": [0.85, 0.75, 0.8], "focal": 40, "ease": "inout"}]},
    # 5. front opens: bumper (Bumper Only scan) slides forward/down off the Bumper Removed structure, then the hood lifts
    "s5_front_open": {"base": [f"{P}/comp_fronthood.blend"],
                      "parts": [
                          {"blend": f"{P}/bonly.blend",
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 0.5 * B, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 3.6 * B, "loc": [0, -1.05, -0.12], "rot": [0, 0, 0], "ease": "inout"},
                                    {"t": SECS["s5_front_open"], "loc": [0, -1.2, -0.14], "rot": [0, 0, 0], "ease": "lin"}]},
                          {"blend": f"{P}/hood.blend", "pivot": HOOD_HINGE,
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 4 * B, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 6.5 * B, "loc": [0, 0, 0], "rot": [-38, 0, 0], "ease": "out"},
                                    {"t": SECS["s5_front_open"], "loc": [0, 0, 0], "rot": [-40, 0, 0], "ease": "lin"}]}],
                      "cam": arc(0, SECS["s5_front_open"], 4.2, 4.5, -30, -14, 1.3, 1.75, c=(0, -1.45, 0.45), focal=30, n=6)},
    # 6. trunk lid opens on its fitted hinge, high rear 3/4
    "s6_trunk": {"base": [f"{P}/comp_trunk.blend"],
                 "parts": [{"blend": f"{P}/lid.blend", "pivot": LID_HINGE,
                            "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                     {"t": 1 * B, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                     {"t": 4 * B, "loc": [0, 0, 0], "rot": [LID_OPEN, 0, 0], "ease": "inout"}]}],
                 "cam": arc(0, SECS["s6_trunk"], 3.6, 3.3, 146, 164, 2.2, 2.5, c=(0, 1.8, 0.6), focal=30, n=6)},
    # 7. top-down: from high front 3/4 up and over to straight down (tail at the top of the frame; starting from the
    # front keeps the camera's up vector continuous - from behind it would flip 180 deg at the top)
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [-1.7, -3.4, 3.6], "target": [0, -0.1, 0.5], "focal": 28},
        {"t": SECS["s7_top"] * 0.6, "loc": [-0.5, -0.8, 5.4], "target": [0, 0.17, 0.5], "focal": 28, "ease": "inout"},
        {"t": SECS["s7_top"], "loc": [0.0, 0.15, 5.6], "target": [0, 0.17, 0.5], "focal": 28, "ease": "out2"}]},
}

# 8. exploded view. Times are set from the music in plan(): parts separate on SEP (accent), drift, fly home and LOCK on a
# later accent. Parts go UP/forward (portrait stacking, lesson: never at the lens).
EXP = {"secs": 14.0, "sep": 1 * B, "hold": 4 * B, "back": 24 * B, "lock": 28 * B}  # shot = beats 48..80


def explode(off, rot=(0, 0, 0), delay=0.0, e=EXP, drift=(6, 0, 4)):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": e["sep"] + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
            {"t": e["hold"] + delay, "loc": list(off), "rot": list(rot), "ease": "out"},
            # slow drift outward + a small extra tilt so the 8 s float never reads as a freeze (v1 frame diffs ~0)
            {"t": e["back"], "loc": [o * 1.16 for o in off], "rot": [r + d for r, d in zip(rot, drift)], "ease": "inout"},
            {"t": e["lock"], "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


def explode_shot(e=EXP):
    return {"base": [f"{P}/comp_explode.blend"],
            "parts": [
                {"blend": f"{P}/bonly.blend", "keys": explode((0.05, -0.5, 0.8), (-18, 0, 0), 0.0, e)},
                {"blend": f"{P}/hood.blend", "keys": explode((0.1, -0.2, 1.45), (12, 0, -6), 0.08, e)},
                {"blend": f"{P}/lid.blend", "keys": explode((0.1, 0.3, 1.25), (38, 0, 0), 0.16, e)}],
            # high front-left 3/4 looking down ~30 deg, slow orbit toward the side; panels float in layers above the car
            "cam": [orbit(e["secs"] * k / 12, 6.4 + 0.9 * (k / 12), 28 + 50 * (k / 12), 4.4 - 0.5 * (k / 12),
                          c=(0.3, -0.15 - 0.45 * (k / 12), 0.9), focal=28, ease="lin", tz=0.9)
                    for k in range(13)]}


SHOTS["s8_explode"] = explode_shot()
SECS["s8_explode"] = EXP["secs"]

# v4 (reviewer: "last scenes held too long"): the 32-beat explode is cut into 4-8 beat shots. Each sub-shot renders a window
# of the SAME part animation (t0 = its start within s8) from a new camera; e1 and e6 reuse the s8 render itself.
XPARTS = explode_shot()["parts"]
XB = f"{P}/comp_explode.blend"
SUB = {  # name: (t0 in s8 time, seconds, camera keys relative to the sub-shot)
    # b52-56 side view, panels floating in layers above the car (reference 25-31 s), slow track toward the nose
    "e2_side": (4 * B, 1.9, [{"t": 0, "loc": [6.2, 1.2, 4.4], "target": [0, 0.3, 1.25], "focal": 24},
                             {"t": 1.9, "loc": [6.3, 0.2, 4.2], "target": [0, 0.05, 1.25], "focal": 24, "ease": "inout"}]),
    # b56-60 low front, looking up at the bumper and hood hanging over the exposed structure
    "e3_low": (8 * B, 1.9, [{"t": 0, "loc": [-1.6, -5.6, 0.45], "target": [0, -1.2, 1.35], "focal": 24},
                            {"t": 1.9, "loc": [-0.7, -5.4, 0.4], "target": [0, -1.2, 1.4], "focal": 24, "ease": "inout"}]),
    # b60-64 close on the floating hood, sliding along it (4 mm hood skin)
    "e4_hood": (12 * B, 1.9, [{"t": 0, "loc": [2.4, -3.3, 3.2], "target": [0.1, -1.3, 2.15], "focal": 32},
                              {"t": 1.9, "loc": [2.6, -2.2, 3.4], "target": [0.1, -1.0, 2.15], "focal": 32, "ease": "inout"}]),
    # b64-68 high rear 3/4: the lid floating over the open trunk, outro begins
    "e5_rear": (16 * B, 1.9, [{"t": 0, "loc": [-2.7, 5.3, 3.5], "target": [0, 0.8, 1.25], "focal": 26},
                              {"t": 1.9, "loc": [-3.6, 4.6, 3.3], "target": [0, 0.7, 1.25], "focal": 26, "ease": "inout"}]),
    # b76-80 after the lock: push in on the assembled car, front 3/4 (fixes v3's small, off-centre end frame)
    "e8_locked": (28 * B, 1.9, [{"t": 0, "loc": [3.3, -4.9, 1.5], "target": [0, -0.2, 0.55], "focal": 30},
                                {"t": 1.9, "loc": [2.6, -4.0, 1.3], "target": [0, -0.3, 0.55], "focal": 30, "ease": "out2"}]),
}
for _n, (_t0, _s, _cam) in SUB.items():
    SHOTS[_n] = {"base": [XB], "parts": XPARTS, "cam": _cam, "t0": _t0}
    SECS[_n] = _s


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if mode == "preview":
        sp["frames"] = ["first", "mid", "last"]
    if name == "s8_explode" or name in SUB:
        sp["persistent"] = False
    if "t0" in s:
        sp["t0"] = s["t0"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
