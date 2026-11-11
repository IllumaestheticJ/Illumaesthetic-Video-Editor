"""v2 shot specs (direction.md): progressive disassembly travelling rear -> left side -> front, bumper-removed hero on bar 16,
exploded state + reassembly + fade, small logo. -> JSON for tools/shot.py (persistent data off by default).

    python projects/subaru-sti-blobeye/tools/shots_v2.py preview|final [shot ...]

Frame: prepped metres, nose -Y, car's right -X, ground z 0. Keys in shot fractions u (0..1).
Removed parts stay at PARK offsets in every later shot (state carries across cuts); no part flips (no scanned inner faces);
the hood LIFTS OFF (translate) - we have a 'hood removed' state, not a hood-open scan.
"""
import json
import math
import os
import sys

P = "/home/user/media/work/sti/prep"
OUT = "/home/user/media/work/sti/renders"
SPECS = "/home/user/media/work/sti/specs"

OPEN = f"{P}/base_open_dp.blend"   # rear plate flattened (tools/deplate.py)
HOOD, BUMP, WING, SKIRT = (f"{P}/{n}.blend" for n in ("hood_skin", "bumper_skin", "wing", "skirt"))

PARK = {"wing": (0, 0.10, 2.05), "skirt": (0.70, 0, -0.30), "hood": (0, 0.25, 2.00), "bump": (0, -0.70, 1.30)}   # stacked above the car (Temerario), skirt out to the side
BLEND = {"wing": WING, "skirt": SKIRT, "hood": HOOD, "bump": BUMP}

# whole-frame shot lengths (30 fps cut frames from direction.md: 0|97|239|333|381|665|902|949|1044)
SECS = {"S2_wing": 142 / 30, "S3_skirt": 94 / 30, "S4_wheel": 48 / 30, "S5_hood": 284 / 30, "S6_bumper": 237 / 30,
        "S7a_explode": 47 / 30, "S7b_reassemble": 95 / 30}
FPS = {"S5_hood": 12}


def pk(u, loc=(0, 0, 0), ease="inout"):
    return {"u": u, "loc": list(loc), "rot": [0, 0, 0], "ease": ease}


def cam(u, loc, tgt, focal, ease="inout"):
    return {"u": u, "loc": list(loc), "target": list(tgt), "focal": focal, "ease": ease}


def orbit(u, r, ang_deg, h, c, focal=30, ease="inout"):
    a = math.radians(ang_deg)
    return cam(u, (c[0] + r * math.sin(a), c[1] - r * math.cos(a), h), c, focal, ease)


def parts(seated=(), parked=(), moving=None):
    out = [{"blend": BLEND[n]} for n in seated]
    out += [{"blend": BLEND[n], "keys": [pk(0, PARK[n])]} for n in parked]
    for n, keys in (moving or {}).items():
        out.append({"blend": BLEND[n], "keys": keys})
    return out


def addz(v, dz):
    return (v[0], v[1], v[2] + dz)


SHOTS = {
    # rear: wing on (1 bar), lifts on the bar-3 lift (u .333), camera tilts down onto the wing-off trunk lid / mount pads
    "S2_wing": {"parts": parts(seated=("hood", "bump", "skirt"), moving={"wing": [
        pk(0), pk(0.333), pk(0.5, (0, 0.10, 0.45), "out"), pk(0.667, (0, 0.10, 0.60), "lin"), pk(0.85, PARK["wing"])]}),
        "cam": [cam(0, (1.35, 4.55, 1.95), (0.15, 1.95, 1.35), 30), cam(0.333, (1.25, 4.40, 2.05), (0.15, 1.95, 1.40), 30),
                cam(1, (0.85, 3.70, 2.30), (0.05, 1.80, 1.05), 32)]},
    # left side: skirt slides out toward the camera and down out of frame, camera tracks forward along the bare sill
    "S3_skirt": {"parts": parts(seated=("hood", "bump"), parked=("wing",), moving={"skirt": [
        pk(0), pk(0.125), pk(0.25, (0.30, 0, 0.0), "in2"), pk(0.55, (0.60, 0, -1.60), "out")]}),   # drops out of the bottom of frame
        # higher, steeper: door bottom + bare sill fill the frame (v2 final #1 left the lower half black)
        "cam": [cam(0, (2.55, 1.15, 1.45), (0.85, 0.30, 0.80), 30), cam(1, (2.40, 0.30, 1.40), (0.85, -0.30, 0.80), 30)]},
    # front-left wheel: spokes, caliper, disc; slow arc from the front-left
    "S4_wheel": {"parts": parts(seated=("hood", "bump"), parked=("wing", "skirt")),
                 "cam": [cam(0, (1.60, -2.60, 0.45), (0.85, -1.25, 0.36), 40), cam(1, (2.00, -1.95, 0.40), (0.82, -1.25, 0.36), 40)]},
    # hood + scoop (1 bar), hood lifts straight off on bar 9 (u .167), long held descent over the engine bay
    "S5_hood": {"parts": parts(seated=("bump",), parked=("wing", "skirt"), moving={"hood": [
        pk(0), pk(0.167), pk(0.25, (0, 0, 0.30), "out"), pk(0.333, PARK["hood"])]}),
        "cam": [cam(0, (-1.05, -4.30, 1.80), (0, -1.55, 0.85), 35), cam(0.167, (-0.85, -3.95, 1.85), (0, -1.55, 0.85), 35),
                cam(0.333, (-0.70, -3.55, 2.00), (0, -1.40, 0.80), 35), cam(0.667, (-0.35, -2.85, 1.75), (0, -1.30, 0.68), 34),
                cam(1, (0.20, -2.45, 1.55), (0, -1.05, 0.60), 32)]},
    # HERO: bumper intact (bar 14), out from bar 15 (dog-leg past the headlights), clear on bar 16 (u .4); push into the
    # intercooler core, slide to the piping
    "S6_bumper": {"parts": parts(parked=("wing", "skirt", "hood"), moving={"bump": [
        pk(0), pk(0.2), pk(0.3, (0, -0.32, 0.03), "in2"), pk(0.35, (0, -0.60, 0.40), "lin"), pk(0.4, PARK["bump"], "out")]}),
        "cam": [cam(0, (1.20, -4.70, 0.55), (0.05, -2.10, 0.48), 35), cam(0.2, (1.05, -4.45, 0.55), (0.05, -2.10, 0.48), 35),
                cam(0.4, (0.70, -4.00, 0.55), (0, -2.05, 0.45), 35), cam(0.6, (0.30, -3.25, 0.55), (0, -2.00, 0.42), 38),
                cam(0.8, (-0.20, -3.15, 0.50), (-0.30, -1.98, 0.38), 38), cam(1, (-0.60, -3.05, 0.42), (-0.62, -1.95, 0.30), 38)]},
    # whole exploded car, new angle (high left), slow common drift so nothing is dead
    "S7a_explode": {"parts": [{"blend": BLEND[n], "keys": [pk(0, PARK[n]), pk(1, addz(PARK[n], 0.04), "lin")]} for n in PARK],
                    "cam": [orbit(0, 8.7, 118, 3.30, (0.10, -0.20, 1.40)), orbit(1, 8.5, 95, 3.15, (0.10, -0.25, 1.40))]},
    # reassembly in reverse order, 2.5-beat flights staggered half a beat; last lock (wing) on bar 21 (u .5); fade in post
    "S7b_reassemble": {"parts": [
        {"blend": HOOD, "keys": [pk(0, PARK["hood"]), pk(0.313, (0, 0, 0), "in")]},
        {"blend": BUMP, "keys": [pk(0, PARK["bump"]), pk(0.063, PARK["bump"]), pk(0.20, (0, -0.60, 0.40), "inout"),
                                 pk(0.27, (0, -0.32, 0.03), "lin"), pk(0.375, (0, 0, 0), "in")]},
        {"blend": SKIRT, "keys": [pk(0, PARK["skirt"]), pk(0.125, PARK["skirt"]), pk(0.36, (0.30, 0, 0.0), "inout"), pk(0.438, (0, 0, 0), "in")]},
        {"blend": WING, "keys": [pk(0, PARK["wing"]), pk(0.188, PARK["wing"]), pk(0.5, (0, 0, 0), "in")]}],
        "cam": [orbit(0, 7.8, 42, 2.25, (0.10, -0.40, 1.35)), orbit(1, 6.2, 28, 1.40, (0, -0.25, 0.65))]},
}


def to_t(keys, T):
    return [{**{k: v for k, v in key.items() if k != "u"}, "t": key["u"] * T} for key in keys]


def spec(name, mode):
    s, T = SHOTS[name], SECS[name]
    sp = {"base": [OPEN], "camera": {"keys": to_t(s["cam"], T)}, "seconds": T, "fps": FPS.get(name, 15),
          "res": "1080x1920", "out": f"{OUT}/{mode}/{name}", "exposure": -0.5, "persistent": False,
          "parts": [{**p, "keys": to_t(p["keys"], T)} if p.get("keys") else p for p in s["parts"]]}
    if mode == "preview":
        sp.update(res_pct=30, samples=8, frames=["first", "mid", "last"])
    else:
        sp.update(res_pct=75, samples=12)
    return sp


if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(SPECS, exist_ok=True)
    for n in sys.argv[2:] or list(SHOTS):
        p = f"{SPECS}/{mode}_{n}.json"
        json.dump(spec(n, mode), open(p, "w"), indent=1)
        print(p)
