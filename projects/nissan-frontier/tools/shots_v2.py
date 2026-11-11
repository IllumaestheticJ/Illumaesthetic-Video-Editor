"""v2 shot specs (director.md, 2026-11-11) for the Nissan Frontier Pro-4X reel -> JSON for tools/shot.py.

    python projects/nissan-frontier/tools/shots_v2.py preview|final|check [shot ...]

One section per shot, travelling front -> side -> rear; every part that comes off STAYS OFF (parked) until S8 brings
them home. Cuts sit on broadband onsets measured from the track (onsets.json), frames 146 290 434 542 614 725 833 1015
(end 1151). Part keys are seconds from the SHOT start. Labels/highlights: timing_v2.json -> tools/labels.py.
Prep frame: nose -Y, car's right -X, z=0 = lift-pad cut (ground -0.2).
"""
import json
import math
import os
import sys

P = "/home/user/media/nissan-frontier/prep"
OUT = "/home/user/media/work/frontier/renders"
SPECS = "/home/user/media/nissan-frontier/specs"
T = json.load(open(os.path.join(os.path.dirname(__file__), "..", "timing_v2.json")))
FR = T["frames"]          # shot -> frames at 30 fps
SECS = {k: v / 30 for k, v in FR.items()}
LAB = {s: {l["id"]: l["t"] for l in ls} for s, ls in T["labels"].items()}


def orbit(t, r, ang_deg, h, c=(0, 0, 0.7), focal=30, ease="lin", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def keyed_orbit(Tt, r0, r1, a0, a1, h0, h1, c0, c1, focal=30, n=10):
    ks = []
    for k in range(n + 1):
        u = k / n; s = u * u * (3 - 2 * u)
        c = [c0[i] + (c1[i] - c0[i]) * s for i in range(3)]
        ks.append(orbit(Tt * u, r0 + (r1 - r0) * s, a0 + (a1 - a0) * s, h0 + (h1 - h0) * s, c=c, focal=focal))
    return ks


def cam(*keys):
    return [{"t": t, "loc": list(l), "target": list(g), "focal": f, "ease": e} for t, l, g, f, e in keys]


def hl(shot, i):
    if i not in LAB.get(shot, {}):
        return None
    a, b = LAB[shot][i]
    return [[a - 0.05, 0], [a + 0.2, 1], [b - 0.15, 1], [b + 0.05, 0]]


def still(loc, rot=(0, 0, 0)):
    return [{"t": 0, "loc": list(loc), "rot": list(rot)}]


def k(t, loc, rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}


# parked poses (director.md)
GRILLE_PARK = (1.90, -0.45, 0.10)
BUMPER_PARK, BUMPER_ROT = (0, -0.95, -0.60), (120, 0, 0)
HOOD_PARK = (0, 0.05, 1.25)
FL_R, FL_L = (-0.30, 0, 1.00), (0.30, 0, 1.00)


def part(name, blend, keys, shot=None, label=None):
    p = {"blend": f"{P}/{blend}.blend", "keys": keys}
    if label:
        p["name"] = label
        p["hl"] = hl(shot, label)
    return p


def shots():
    S = SECS
    sh = {}
    # S1 whole truck, front-right 3/4, moving from frame 1, bed + roof + rails inside the frame
    sh["v2_s1_wide"] = {"base": [f"{P}/car4.blend"], "parts": [],
                        "cam": keyed_orbit(S["v2_s1_wide"] + 0.2, 6.6, 6.2, -32, -46, 1.4, 1.6, (0, -0.2, 0.75), (0, -0.3, 0.75), focal=26)}
    # S2 grille close-up (v1 s3_grille move, stretched to the slot) - grille highlighted + labelled, stays ON (no scan of
    # the grille off with the bumper on)
    sh["v2_s2_grille"] = {"base": [f"{P}/comp_nogrille.blend"],
                          "parts": [part("grille", "x_grille", still((0, 0, 0)), "v2_s2_grille", "grille")],
                          "cam": cam((0, (-1.35, -3.75, 0.95), (-0.35, -2.62, 0.78), 40, "lin"),
                                     (S["v2_s2_grille"] + 0.2, (-0.15, -3.95, 0.88), (-0.2, -2.62, 0.74), 40, "inout"))}
    # S3 FRONT BUMPER on the drop: bumper (+grille riding on it) forward then down into black; grille lifts off the bumper
    # to its park on 12.04; bumper turns 120 deg about its width axis on 13.27 to show the scanned inside
    b1 = [k(0, (0, 0, 0)), k(0.60, (0, -0.70, -0.05), ease="out2"), k(1.19, BUMPER_PARK, ease="inout")]
    sh["v2_s3_bumper"] = {"base": [f"{P}/comp_fbrhc.blend", f"{P}/fbrhc_fill.blend"],
                          "parts": [part("bumper", "x_bumper", b1 + [k(2.38, BUMPER_PARK), k(3.60, BUMPER_PARK, BUMPER_ROT)], "v2_s3_bumper", "bumper"),
                                    part("grille", "x_grille", b1 + [k(2.38, GRILLE_PARK)])],
                          "cam": cam((0, (-1.4, -5.4, 1.0), (-0.1, -2.9, 0.55), 30, "lin"),
                                     (1.2, (-1.3, -5.6, 1.3), (-0.06, -3.6, 0.15), 30, "inout"),
                                     (3.6, (-0.6, -5.6, 2.2), (-0.06, -3.65, -0.1), 28, "inout"),
                                     (S["v2_s3_bumper"] + 0.2, (-0.4, -5.2, 1.9), (-0.06, -3.65, -0.1), 28, "inout"))}
    parked_front = [part("bumper", "x_bumper", still(BUMPER_PARK, BUMPER_ROT)), part("grille", "x_grille", still(GRILLE_PARK))]
    # S4 FRONT BUMPER REMOVED (hero): low straight-on push-in on the bumper-off state
    sh["v2_s4_removed"] = {"base": [f"{P}/comp_fbrhc.blend",
                                    {"blend": f"{P}/fbrhc_fill.blend", "name": "fbrhc", "hl": hl("v2_s4_removed", "fbrhc")}],
                           "parts": [],  # parked bumper/grille sit off-frame here (check: they filled the lower third under the hero hold)
                           "cam": cam((0, (0.6, -6.0, 1.15), (-0.06, -2.6, 0.78), 30, "lin"),
                                      (S["v2_s4_removed"] + 0.2, (0.3, -4.4, 1.05), (-0.06, -2.55, 0.72), 32, "inout"))}
    # S5 HOOD lifts straight off (hood-removed state exists, hood-open does not)
    sh["v2_s5_hood"] = {"base": [f"{P}/comp_front_body.blend", f"{P}/struct.blend"],
                        "parts": parked_front + [part("hood", "x_hood", [k(0, (0, 0, 0)), k(0.30, (0, 0, 0)), k(1.19, (0, 0.05, 1.15)),
                                                                         k(2.6, HOOD_PARK, ease="lin")], "v2_s5_hood", "hood")],
                        "cam": cam((0, (-2.6, -5.0, 2.9), (-0.06, -2.0, 1.35), 26, "lin"),
                                   (S["v2_s5_hood"] + 0.2, (-2.4, -4.8, 3.1), (-0.06, -1.9, 1.6), 26, "inout"))}
    parked_hood = parked_front + [part("hood", "x_hood", still(HOOD_PARK))]
    # S6 FRONT STRUCTURE (bumper + hood removed state): high push-in ~35 deg down, never overhead
    sh["v2_s6_struct"] = {"base": [f"{P}/comp_front_body.blend",
                                   {"blend": f"{P}/struct.blend", "name": "struct", "hl": hl("v2_s6_struct", "struct")}],
                          "parts": parked_hood,
                          "cam": cam((0, (-1.0, -5.2, 2.6), (-0.06, -2.6, 0.8), 30, "lin"),
                                     (S["v2_s6_struct"] + 0.2, (-0.5, -4.1, 2.2), (-0.06, -2.35, 0.75), 32, "inout"))}
    # S7 FENDER FLARES: side 3/4, flares rise above the body line on 25.34
    fl = lambda park: [k(0, (0, 0, 0)), k(0.60, (0, 0, 0)), k(1.18, park)]
    sh["v2_s7_flares"] = {"base": [f"{P}/comp_body.blend", f"{P}/struct.blend"],
                          "parts": parked_hood + [part("flares_r", "x_flares_r", fl(FL_R), "v2_s7_flares", "flares"),
                                                  {"blend": f"{P}/x_flares_l.blend", "keys": fl(FL_L), "hl": hl("v2_s7_flares", "flares")}],
                          "cam": keyed_orbit(S["v2_s7_flares"] + 0.2, 6.0, 5.8, -60, -75, 1.9, 1.8, (0, -0.2, 0.9), (0, -0.2, 0.9), focal=26)}
    # S8 home one per beat from the crash (lock 30.14), FULL TRUCK highlight + label, clip fades out (assembly)
    home = lambda park, rot, t0, t1: [k(0, park, rot), k(t0, park, rot), k(t1, (0, 0, 0), ease="in2")]
    sh["v2_s8_home"] = {"base": [f"{P}/comp_body.blend", f"{P}/struct.blend"],
                        "parts": [part("flares_r", "x_flares_r", home(FL_R, (0, 0, 0), 0.0, 0.60)),
                                  part("flares_l", "x_flares_l", home(FL_L, (0, 0, 0), 0.0, 0.60)),
                                  part("hood", "x_hood", home(HOOD_PARK, (0, 0, 0), 0.60, 1.17)),
                                  part("bumper", "x_bumper", home(BUMPER_PARK, BUMPER_ROT, 1.17, 1.77)),
                                  part("grille", "x_grille", home(GRILLE_PARK, (0, 0, 0), 1.77, 2.37))],
                        "hl_all": hl("v2_s8_home", "body"),
                        "cam": keyed_orbit(S["v2_s8_home"] + 0.2, 6.8, 6.4, -135, -150, 3.0, 1.8, (0, 0.2, 0.75), (0, 0.2, 0.75), focal=26)}
    sh["v2_s8_home"]["base"][0] = {"blend": f"{P}/comp_body.blend", "name": "body"}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "hl_all": s.get("hl_all"), "anchors_out": f"{SPECS}/{name}_{mode}_anchors.json",
          "seconds": SECS[name] + 0.2, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6, "exposure": -0.5,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if sp["parts"]:
        sp["persistent"] = False  # moving parts: persistent data dropped the lights (WRX VA, Cappuccino, huracan)
    if frames:
        sp["frames"] = frames
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    fr = None
    if mode == "check":
        mode, fr = "preview", ["first", "mid", "last"]
    for n in sys.argv[2:] or list(shots()):
        print(spec(n, mode, fr))
