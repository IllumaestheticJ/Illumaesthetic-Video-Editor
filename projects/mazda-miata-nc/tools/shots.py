"""Shot specs for the Mazda Miata NC Temerario-style reel -> JSON for tools/shot.py (copied from ferrari-296).

    python projects/mazda-miata-nc/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (prepped, metres): nose = -Y, car's right = -X, ground Z=0; length 3.99 m, width 1.86 m (2.0 m with
mirrors), height 1.18 m. Shots are rendered a little long at 15 fps; project.yaml trims/retimes them to the music.
"""
import json
import math
import os
import sys

P = "/home/user/media/mazda-miata-nc/prep"
OUT = "/home/user/media/work/miata/renders"
SPECS = "/home/user/media/work/miata/specs"
CAR = f"{P}/car4.blend"        # 4 mm: full-car moves
CAR_HI = f"{P}/car3.blend"     # 3 mm: close-ups
HOOD_PIVOT = [-0.024, -0.757, 0.772]   # hood rear edge (cowl seam) - tools/polycut.py hood4.stl
# music grid (tools/accents.py): beat n at -0.524 + 0.58241 n; bars on odd beats; drop = beat 33 = 18.696 s.
# Rendered ~0.2-0.9 s longer than the cut lengths in project.yaml (s1 was queued before the music arrived).
BEAT = 0.58241
SECS = {"s1_front": 5.6, "s2_rear": 4.4, "s3_wheel": 1.4, "s4_lamp": 1.4, "s5_hood": 3.1, "s6_trunk": 2.5,
        "s7_top": 2.5, "s8_explode": 20 * BEAT + 0.2, "s9_hero": 6 * BEAT + 0.2}
HINGE_LID = json.load(open("/home/user/media/mazda-miata-nc/work/hinge_lid.json")) if os.path.exists(
    "/home/user/media/mazda-miata-nc/work/hinge_lid.json") else None


def orbit(t, r, ang_deg, h, c=(0, 0, 0.5), focal=30, ease="inout", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def sweep(n, secs, f):
    """n+1 keys along f(u) (u 0..1) so long arcs don't cut chords (linear loc between far keys)."""
    return [dict(f(k / n), t=secs * k / n) for k in range(n + 1)]


S = SECS
# angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind
SHOTS = {
    # 1. slow low front 3/4 turntable (car's right), opens the reel
    "s1_front": {"base": [CAR], "cam": sweep(8, S["s1_front"], lambda u: orbit(
        0, 4.7 - 0.3 * u, -24 - 24 * u, 0.85 + 0.2 * u, c=(0, -0.25, 0.5), focal=30, ease="lin", tz=0.45))},
    # 2. rear 3/4 orbit on the car's left, slight rise
    "s2_rear": {"base": [CAR], "cam": sweep(8, S["s2_rear"], lambda u: orbit(
        0, 4.6 - 0.2 * u, 154 - 22 * u, 0.8 + 0.4 * u, c=(0, 0.3, 0.5), focal=30, ease="lin", tz=0.45))},
    # 3. extreme close-up: front-right wheel, slide forward along the flank
    "s3_wheel": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.95, -0.95, 0.72], "target": [-0.80, -1.34, 0.46], "focal": 40},
        {"t": S["s3_wheel"], "loc": [-1.90, -1.30, 0.69], "target": [-0.80, -1.35, 0.45], "focal": 40, "ease": "inout"}]},
    # 4. detail: headlight + nose, slide across the front
    "s4_lamp": {"base": [CAR_HI], "cam": [
        {"t": 0, "loc": [-1.55, -2.85, 0.80], "target": [-0.55, -1.75, 0.62], "focal": 38},
        {"t": S["s4_lamp"], "loc": [-0.95, -3.05, 0.79], "target": [-0.45, -1.78, 0.60], "focal": 38, "ease": "inout"}]},
    # 5. hood opens on the cowl seam over the real engine bay (Hood and Bumper Removed + Hood Open scans)
    "s5_hood": {"base": [f"{P}/comp_hood.blend"],
                "parts": [{"blend": f"{P}/hood4.blend", "pivot": HOOD_PIVOT,
                           "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 0.25, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                    {"t": 2.3, "loc": [0, 0, 0], "rot": [-55, 0, 0], "ease": "inout"}]}],
                "cam": sweep(6, S["s5_hood"], lambda u: orbit(
                    0, 3.4 - 0.4 * u, -38 + 14 * u, 1.75 + 0.3 * u, c=(0, -1.1, 0.55), focal=30, ease="lin", tz=0.5))},
    # 7. top-down: high rear 3/4 rising to straight down, nose to the top of frame
    "s7_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [2.0, 4.2, 3.6], "target": [0, 0.3, 0.45], "focal": 30},
        {"t": S["s7_top"], "loc": [0.0, 0.2, 6.6], "target": [0, 0.0, 0.45], "focal": 30, "ease": "inout"}]},
}
if HINGE_LID:
    # 6. trunk lid opens on its fitted hinge (lid closed -> 2023 'Trunk Open' capture), trunk interior from that scan
    SHOTS["s6_trunk"] = {"base": [f"{P}/comp_trunk.blend"],
                         "parts": [{"blend": f"{P}/lid4.blend", "pivot": HINGE_LID["p"],
                                    "axis": HINGE_LID["axis"],
                                    "keys": [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                             {"t": 0.15, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                                             {"t": 1.9, "loc": [0, 0, 0], "rot": [HINGE_LID["open_deg"], 0, 0], "ease": "inout"}]}],
                         "cam": sweep(6, S["s6_trunk"], lambda u: orbit(
                             0, 3.4 - 0.3 * u, 150 - 16 * u, 1.75 + 0.3 * u, c=(0, 1.35, 0.55), focal=30, ease="lin", tz=0.55))}


# 8. exploded view: bumper / hood / trunk lid separate ON the drop (shot t=0), drift while the camera orbits the
# car's left from front 3/4 to rear 3/4, bumper flips about its width axis to show its scanned inside, flips back,
# everything flies home and LOCKS on the 28.014 s bar (16 beats), assembled orbit continues to the cut.
SEP, OUT_, FLIP0, FLIP1, UNFLIP0, UNFLIP1, BACK, LOCK = 0.0, 1.4, 1.6, 3.9, 4.7, 6.4, 7.0, 16 * BEAT


def explode(off, rot=(0, 0, 0), delay=0.0, flip=None):
    k = [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
         {"t": SEP + delay, "loc": [0, 0, 0], "rot": [0, 0, 0]},
         {"t": OUT_ + delay, "loc": list(off), "rot": list(rot), "ease": "out"}]
    if flip:
        fr = [r + f for r, f in zip(rot, flip)]
        k += [{"t": FLIP0, "loc": list(off), "rot": list(rot), "ease": "lin"},
              {"t": FLIP1, "loc": list(off), "rot": fr, "ease": "inout"},
              {"t": UNFLIP0, "loc": list(off), "rot": fr, "ease": "lin"},
              {"t": UNFLIP1, "loc": list(off), "rot": list(rot), "ease": "inout"}]
    k += [{"t": BACK, "loc": [o * 1.05 for o in off], "rot": list(rot), "ease": "lin"},
          {"t": LOCK, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]
    return k


SHOTS["s8_explode"] = {
    "base": [f"{P}/comp_explode.blend"],
    "parts": [
        {"blend": f"{P}/bumper.blend", "keys": explode((0, -0.30, 1.45), flip=(180, 0, 0))},
        {"blend": f"{P}/hood4.blend", "keys": explode((0, 0.05, 0.75), (-8, 0, 0), 0.08)},
        {"blend": f"{P}/lid4.blend", "keys": explode((0, 0.10, 0.95), (12, 0, 0), 0.16)},
    ],
    "cam": sweep(16, S["s8_explode"], lambda u: orbit(
        0, 6.3 + 1.0 * math.sin(math.pi * u), 38 + 104 * u, 2.6 - 0.4 * u, c=(0, -0.2 + 0.4 * u, 1.0), focal=28,
        ease="lin", tz=1.05 - 0.25 * u))}

# 9. assembled hero: low front-left 3/4 (the one quarter not seen yet), slow push-in, then the logo
SHOTS["s9_hero"] = {"base": [CAR], "cam": sweep(6, S["s9_hero"], lambda u: orbit(
    0, 4.6 - 0.5 * u, 30 + 12 * u, 0.55 + 0.1 * u, c=(0, -0.3, 0.5), focal=32, ease="lin", tz=0.45))}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name], "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if mode == "frames":
        sp["frames"] = ["first", "mid", "last"] if name != "s8_explode" else [1, 22, 40, 60, 80, 100, 130, 150, 178]
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
