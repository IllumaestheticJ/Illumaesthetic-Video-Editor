"""v6 shot specs: the user's v5 notes - edit from the BEGINNING of Megalomaniac (trending side), drop the wheel close-up,
and stay on the side skirt after it comes off (v5 cut away right after it moved).

    python projects/mazda-miata-nd/tools/shots_v6.py preview|final [shot ...]

Reuses every v5 spec helper (shots_v5.py, same beat B = 0.46864 s). New renders only:
  v6_a_open   whole-car opener, 8 beats over the song's intro (v3 opener was 4 beats at 116 BPM)
  v6_f_struct slow close pass along the exposed crash beam / front structure, 8 beats (the intro needs 8 more beats before
              the hood lands on the kick entry; it is the "move in on what's behind the bumper" beat)
  v6_s_side   mirror off -> skirt slides out -> camera stays on the skirt and the exposed sill for 4 more beats (10 beats)
N = ceil((slot+3)/2) renders at 15 fps (src_fps 15).
"""
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec5 = importlib.util.spec_from_file_location("shots_v5", os.path.join(HERE, "shots_v5.py"))
v5 = importlib.util.module_from_spec(spec5)
sys.argv, _argv = [sys.argv[0]], sys.argv  # shots_v5 only defines things at import
spec5.loader.exec_module(v5)
sys.argv = _argv

B, P, W = v5.B, v5.P, v5.W
cam, k, part, static, arc = v5.cam, v5.k, v5.part, v5.static, v5.arc
HOOD, TRUNK, HOOD_OPEN = v5.HOOD, v5.TRUNK, v5.HOOD_OPEN
OUT = f"{W}/renders_v6"
SPECS = f"{W}/specs"


def n_for(beats):
    slot = round(30 * beats * B)
    return math.ceil((slot + 3) / 2), slot


SHOTS = {}
N, slot = n_for(8)
SHOTS["v6_a_open"] = {"N": N, "base": ["car4np"], "parts": [],
                      "cam": arc(slot / 30, (6.5, 5.95), (-54, -32), (1.5, 1.3), (0, -0.2, 0.58), (0, -0.25, 0.58))}

N, slot = n_for(8)
FB_END = v5.FB_END
SHOTS["v6_f_struct"] = {"N": N, "base": ["comp_front_v5"],
                        "parts": [static("x_hood_v5", pivot=HOOD)],   # front bumper is off and out of shot
                        "cam": [cam(0, [-0.95, -3.15, 0.82], [-0.25, -1.75, 0.45], 34),
                                cam(4, [-0.05, -3.0, 0.72], [0.05, -1.72, 0.42], 38),
                                cam(8, [0.95, -3.05, 0.78], [0.35, -1.74, 0.44], 36)]}

N, slot = n_for(10)
MIR = (-0.38, -0.05, 0.18)
SKIRT_OUT = (-0.42, 0, -0.04)
SHOTS["v6_s_side"] = {"N": N, "base": ["comp_explode_v5"],
                      "parts": [part("x_mirror_r", [k(0), k(0.5), k(2, MIR, ease="out"), k(3.5, MIR, (0, 0, -135)), k(10, MIR, (0, 0, -135))]),
                                part("x_skirt", [k(0), k(5), k(6.5, SKIRT_OUT), k(10, SKIRT_OUT)]),
                                static("x_hood_v5", rot=(HOOD_OPEN, 0, 0), pivot=HOOD),
                                static("x_rbumper"), static("x_trunk", pivot=TRUNK), static("x_mirror_l")],
                      "cam": [cam(0, [-2.15, -1.05, 1.30], [-0.85, -0.08, 0.85], 50),
                              cam(3.5, [-2.35, -1.00, 1.28], [-1.05, -0.10, 0.95], 50),
                              cam(5.5, [-3.15, -0.95, 0.78], [-0.85, 0.0, 0.36], 32),
                              cam(10, [-2.85, 0.70, 0.62], [-0.85, 0.30, 0.32], 36)]}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": [f"{P}/{b}.blend" for b in s["base"]], "parts": s["parts"],
          "camera": {"sensor": 20.25, "keys": s["cam"]}, "seconds": s["N"] / 15, "fps": 15,
          "res": "1080x1920", "res_pct": 75 if final else 30, "samples": 12 if final else 6, "persistent": False,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if not final:
        n = s["N"]
        sp["frames"] = [1, n // 3, 2 * n // 3, n]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
