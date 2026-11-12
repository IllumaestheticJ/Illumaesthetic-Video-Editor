"""v5 additions (reviewer: "a bunch of underbody/aero scans not highlighted/shown"; new music Alkitran from 2:51.65).

    python projects/porsche-gt3rs-992/tools/shots_v5.py preview|final [shot ...]

New shots:  v5_wheel  FL wheel ("Underbody Wheels") slides off, camera pushes into the scanned wheel house
                      ("Underbody front and rear wheel house", wheels-off state) through the track's breakdown,
                      wheel seats again on the kick return.
            v5_under  camera under the car: "Underbody underbody" floor scan, lit from below.
Mask passes (matte) for in-place highlights of aero parts that cannot come off (hollow cut-outs):
            m_sh3 front bumper strakes, m_sh4 fender vent, m_sh6 rear diffuser + diffuser trim + rear bumper strake.
Beat grid: 127.0 BPM, beat 0.47244 s, reel beat b at b*0.47244 s (music start 171.651 s = a kick onset).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv, sys.argv = sys.argv, ["x"]
import shots_v3 as v3  # noqa: E402
sys.argv = _argv

P, OUT, SPECS = v3.P, v3.OUT, v3.SPECS
BEAT = 0.47244
ALL_OFF = [v3.still_off(n) for n in v3.FRONT + v3.REAR + v3.SIDE]

# wheel: out along the axle (+X), then forward into the black beside the nose; back the same way, seats on b54
W0 = 44 * BEAT
t = lambda b: round(b * BEAT - W0, 4)
WHEEL = v3.part("wheel_fl", [
    {"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
    {"t": t(45), "loc": [0.45, 0, 0], "rot": [0, 0, 0], "ease": "inout"},
    {"t": t(47), "loc": [0.60, -1.05, 0.05], "rot": [0, 0, 0], "ease": "inout"},
    {"t": t(51), "loc": [0.60, -1.05, 0.05], "rot": [0, 0, 0]},
    {"t": t(53), "loc": [0.45, 0, 0], "rot": [0, 0, 0], "ease": "inout"},
    {"t": t(54), "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}])
SECS = {"v5_wheel": 4.95, "v5_under": 4.0}
SHOTS = {
    "v5_wheel": {"base": [f"{P}/comp_v5.blend"], "parts": ALL_OFF + [WHEEL],
                 "cam": v3.cam((0, (3.3, -0.35, 0.85), (0.85, -1.30, 0.42), 30),
                               (t(47), (2.9, -0.55, 0.75), (0.85, -1.30, 0.42), 30),
                               (t(52), (2.15, -0.85, 0.6), (0.80, -1.30, 0.40), 30),
                               (4.95, (2.3, -0.8, 0.62), (0.80, -1.30, 0.40), 30))},
    "v5_under": {"base": [f"{P}/comp_v3.blend", f"{P}/x_underbody_new.blend"], "parts": ALL_OFF, "underlight": 0.4,
                 # constant camera-to-target offset (looking up and slightly rearward): a changing offset rolls the frame
                 "cam": v3.cam((0, (0.0, -1.9, -3.8), (0.0, -0.75, 0.2), 30),
                               (4.0, (0.0, -0.45, -3.8), (0.0, 0.70, 0.2), 30, "lin"))},
}


def spec(name, mode, frames=None):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s["parts"], "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name], "fps": 15, "res": "1080x1920", "res_pct": 75 if final else 30,
          "samples": 12 if final else 6, "persist": False, "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if s.get("underlight"):
        sp["underlight"] = s["underlight"]
    if not final:
        sp["frames"] = frames or ["first", "mid", "last"]
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


# mask passes: same camera + part motion as the beauty render; base = comp_explode4 (every aero part cut out, so the
# emitting part scan is not coincident with the car skin); everything except the "emit" parts is a holdout.
MATTES = {"m_sh3": ("v3_sh3_final.json", ["front_bumper_strake"]),
          "m_sh4": ("v2_sh4_final.json", ["fender_vent"]),
          "m_sh6": ("v3_sh6_final.json", ["rear_diffuser_trim_outer", "rear_bumper_strake", "rear_diffuser_1"])}


def matte_spec(name, mode="final"):
    src, emit = MATTES[name]
    sp = json.load(open(f"{SPECS}/{src}"))
    sp["base"] = [f"{P}/comp_explode4.blend"]
    have = {os.path.basename(p["blend"])[2:-6] for p in sp["parts"]}
    for p in sp["parts"]:
        if os.path.basename(p["blend"])[2:-6] in emit:
            p["emit"] = True
    for n in emit:
        if n not in have:
            sp["parts"].append({"blend": f"{P}/x_{n}.blend", "emit": True})
    sp.update({"matte": True, "samples": 4, "res_pct": 75 if mode == "final" else 30, "out": f"{OUT}/final/{name}"})
    sp.pop("frames", None)
    if mode != "final":
        sp["frames"] = ["mid"]; sp["out"] = f"{OUT}/preview/{name}"
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS) + list(MATTES):
        print(matte_spec(n, mode) if n in MATTES else spec(n, mode))
