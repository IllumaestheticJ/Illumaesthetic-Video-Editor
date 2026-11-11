"""Shot specs for the Subaru WRX VB Temerario-style scan reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/subaru-wrx-vb/tools/shots.py preview|final [shot ...]   # writes specs, prints paths
    preview = first/mid/last frames at 30 % res; final = all frames, 75 % res, 12 spp, 15 fps

Scan frame (prepped from car4.json, metres): front = -Y, car's right = -X, ground Z=0.
Car 4.663 x 1.889 x 1.458 m. Front axle y ~ -1.36, rear axle y ~ +1.31.
SECS are the shot lengths cut on the music grid (see project.yaml); renders get +1 frame of slack.
"""
import json
import math
import os
import sys

P = "/home/user/media/subaru-wrx-vb/prep"
OUT = "/home/user/media/work/wrx/renders"
SPECS = "/home/user/media/work/wrx/specs"
TIMING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "timing.json")
SECS = {"s1_front34": 6.0, "s2_rear34": 5.5, "s3_wheel": 3.5, "s4_scoop": 3.5, "s5_front": 4.5, "s6_top": 4.0,
        "s7_explode": 10.0}
# event times inside the animated shots (seconds from the shot start); replaced by the music grid in timing.json
EV = {"s5_front": {"go": 0.6, "off": 2.4, "garnish": 0.9},
      "s7_explode": {"sep": 0.3, "out": 1.6, "back": 7.4, "lock": 8.6}}
if os.path.exists(TIMING):  # written once the music grid is known
    _t = json.load(open(TIMING))
    SECS.update(_t["secs"])
    for k, v in _t.get("events", {}).items():
        EV[k].update(v)

CAR = f"{P}/car4np.blend"    # 4 mm: full-car moves (licence plates flattened: tools/flatten_plates.py)
FRONT2 = f"{P}/front2np.blend"  # 2 mm front half (y < -0.6 m raw): close-ups


def orbit(t, r, ang_deg, h, c=(0, 0, 0.55), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); +90 = car's left (+X); -90 = car's right (-X); 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def arc(t0, t1, n, r0, r1, a0, a1, h0, h1, c=(0, 0, 0.55), focal=30, tz=None, ease=lambda u: u):
    """Orbit keyed every (t1-t0)/n so linear key interpolation never cuts a chord toward the car."""
    ks = []
    for k in range(n + 1):
        u = k / n
        e = ease(u)
        ks.append(orbit(t0 + (t1 - t0) * u, r0 + (r1 - r0) * e, a0 + (a1 - a0) * e, h0 + (h1 - h0) * e, c, focal,
                        "lin", tz))
    return ks


def smooth(u):
    return u * u * (3 - 2 * u)


def out2(u):
    return 1 - (1 - u) ** 2


S = SECS
SHOTS = {
    # 1. slow low front 3/4 turntable (car's left), moving from frame 1 - the hook
    "s1_front34": {"base": [CAR], "cam": arc(0, S["s1_front34"], 8, 5.0, 4.7, 32, 62, 0.85, 1.0, focal=30, tz=0.55)},
    # 2. rear 3/4 orbit on the other side (car's right), slight rise
    "s2_rear34": {"base": [CAR], "cam": arc(0, S["s2_rear34"], 8, 5.0, 4.8, -148, -120, 0.8, 1.25, focal=30,
                                            tz=0.6, ease=out2)},
    # 3. extreme close-up: front-right wheel, brake through the spokes, slow slide forward
    "s3_wheel": {"base": [FRONT2], "cam": [
        {"t": 0, "loc": [-2.05, -0.75, 0.42], "target": [-0.88, -1.30, 0.34], "focal": 40},
        {"t": S["s3_wheel"], "loc": [-2.0, -1.85, 0.40], "target": [-0.88, -1.42, 0.34], "focal": 40, "ease": "inout"}]},
    # 4. detail: hood scoop + headlights, high slide across the nose
    "s4_scoop": {"base": [FRONT2], "cam": [
        {"t": 0, "loc": [-1.35, -3.25, 1.55], "target": [-0.05, -1.25, 0.88], "focal": 38},
        {"t": S["s4_scoop"], "loc": [0.85, -3.3, 1.6], "target": [0.05, -1.3, 0.86], "focal": 38, "ease": "inout"}]},
    # 6. top-down: from a high front 3/4 up and over to straight down (front at the top of frame)
    "s6_top": {"base": [CAR], "cam": [
        {"t": 0, "loc": [2.6, -3.6, 3.9], "target": [0, -0.3, 0.5], "focal": 30},
        {"t": S["s6_top"], "loc": [0.0, -0.2, 6.6], "target": [0, 0.0, 0.5], "focal": 30, "ease": "inout"}]},
}


# 5. front end comes off: bumper (+ blank plate, grille) slides forward and drops, lower garnish follows; low
# front-right 3/4 pushing in on the scanned crash beam / radiator support (base = all-panels-off composite with
# the other panels parked in place)
XB = f"{P}/base_xnp.blend"
FB = [f"{P}/p_front_bumper_inside_parts_included.blend", f"{P}/plate_xnp.blend"]
IN_PLACE = [f"{P}/p_rear_bumper_updated.blend", f"{P}/p_front_flare.blend", f"{P}/p_door_flare.blend",
            f"{P}/p_rear_flare.blend", f"{P}/p_side_skirt_only.blend"]


def still(t):
    return {"t": t, "loc": [0, 0, 0], "rot": [0, 0, 0]}


def move(t, off, rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(off), "rot": list(rot), "ease": ease}


E5 = EV["s5_front"]
SHOTS["s5_front"] = {
    "base": [XB] + IN_PLACE,
    "parts": [{"blend": b, "keys": [still(0), still(E5["go"]), move(E5["off"], (1.35, -0.35, -0.1)),
                                    move(S["s5_front"] + 1, (1.48, -0.38, -0.11), ease="lin")]} for b in FB]
    + [{"blend": f"{P}/p_front_bumper_lower_garnish.blend",
        "keys": [still(0), still(E5["go"] + E5["garnish"] * 0.5), move(E5["off"] + E5["garnish"] * 0.5, (1.1, -0.25, -0.12)),
                 move(S["s5_front"] + 1, (1.2, -0.27, -0.13), ease="lin")]}],
    "cam": [{"t": 0, "loc": [-2.4, -4.7, 1.15], "target": [-0.1, -1.9, 0.72], "focal": 30},
            {"t": S["s5_front"], "loc": [-1.7, -4.25, 1.0], "target": [-0.05, -1.85, 0.68], "focal": 30, "ease": "inout"}]}

# 7. exploded view: every scanned panel separates (ease-out on an accent) into layers ABOVE the car (Temerario,
# portrait-friendly: uses the 9:16 height), drifts while the camera orbits the right side, then flies home (ease-in)
# and LOCKS on a later accent. Right-side flares/skirt also step out to -X, toward the camera side.
E7 = EV["s7_explode"]
X7 = [  # (blend(s), offset m, rotation deg, delay s) - layers above the car (Temerario 25-31 s)
    (FB, (0, 0.55, 1.35), (-8, 0, 0), 0.0),
    ([f"{P}/p_front_bumper_lower_garnish.blend"], (0, 0.25, 0.85), (0, 0, 0), 0.06),
    ([f"{P}/p_rear_bumper_updated.blend"], (0, -0.5, 1.2), (8, 0, 0), 0.03),
    ([f"{P}/p_front_flare.blend"], (-0.45, -0.05, 0.9), (0, -8, 0), 0.10),
    ([f"{P}/p_door_flare.blend"], (-0.45, 0.0, 0.9), (0, -8, 0), 0.13),
    ([f"{P}/p_rear_flare.blend"], (-0.45, 0.05, 0.9), (0, -8, 0), 0.16),
    ([f"{P}/p_side_skirt_only.blend"], (-0.55, 0, 0.35), (0, 0, 0), 0.08),
]


def xkeys(off, rot, delay):
    return [still(0), still(E7["sep"] + delay), move(E7["out"] + delay, off, rot, "out"),
            move(E7["back"], [o * 1.08 for o in off], rot, "lin"),  # slow drift outward
            {"t": E7["lock"], "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]


SHOTS["s7_explode"] = {
    "base": [XB],
    "parts": [{"blend": b, "keys": xkeys(off, rot, dl)} for bl, off, rot, dl in X7 for b in bl],
    # slow orbit on the car's right from rear 3/4 to front 3/4, keyed every 1/12 (no chords through the car)
    "cam": [orbit(S["s7_explode"] * k / 12, 7.0, -128 + 70 * smooth(k / 12), 2.4 + 0.4 * math.sin(math.pi * k / 12),
                  c=(0.0, 0.0, 1.1), focal=28, ease="lin", tz=1.1)
            for k in range(13)]}


PREVIEW_FRAMES = {"s5_front": [1, int(EV["s5_front"]["off"] * 0.6 * 15), "last"],
                  "s7_explode": [1, int(EV["s7_explode"]["out"] * 15) + 3, int(5.0 * 15), int(EV["s7_explode"]["back"] * 15),
                                 "last"]}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if not final:
        sp["frames"] = PREVIEW_FRAMES.get(name, ["first", "mid", "last"])
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
