"""v3 shot specs for the Nissan Frontier reel (reviewer notes on v2) -> JSON for tools/shot.py.

    python projects/nissan-frontier/tools/shots_v3.py preview|final|check [shot ...]

v3 changes: bases built with composite.py --remove-diff (no bumper skin left on the truck when the bumper is off);
hood OPENS ON ITS HINGE (hinge.json: fitted to the propped-open hood fragments in the state scans, 33.5 deg) and stays
open; flares cleaned to the four arch bands, each pulled out toward the lens and turned 180 deg to show its back.
S1/S2 are the v2 renders (v2_s1_wide, v2_s2_grille). Timing/labels: timing_v3.json (same cut frames as v2).
"""
import json
import math
import os
import sys

P = "/home/user/media/nissan-frontier/prep"
OUT = "/home/user/media/work/frontier/renders"
SPECS = "/home/user/media/nissan-frontier/specs"
HERE = os.path.dirname(__file__)
T = json.load(open(os.path.join(HERE, "..", "timing_v3.json")))
SECS = {k: v / 30 for k, v in T["frames"].items()}
LAB = {s: {l["id"]: l["t"] for l in ls} for s, ls in T["labels"].items()}
H = json.load(open(os.path.join(HERE, "..", "hinge.json")))["fla"]
HOOD_PIVOT = [-0.062, H["y0_mm"] / 1000 + 0.808, H["z0_mm"] / 1000 - 0.2]   # levelled mm -> prep m
HOOD_OPEN = (-H["theta_deg"], 0, 0)


def orbit(t, r, ang_deg, h, c=(0, 0, 0.7), focal=30, ease="lin"):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h], "target": list(c), "focal": focal, "ease": ease}


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


def k(t, loc, rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}


def still(loc=(0, 0, 0), rot=(0, 0, 0)):
    return [k(0, loc, rot)]


def part(blend, keys, name=None, hlk=None, pivot=None):
    p = {"blend": f"{P}/{blend}.blend", "keys": keys}
    if name:
        p["name"] = name
    if hlk:
        p["hl"] = hlk
    if pivot:
        p["pivot"] = pivot
    return p


GRILLE_PARK = (1.90, -0.45, 0.10)
BUMPER_PARK, BUMPER_ROT = (0, -0.95, -0.60), (120, 0, 0)
FLARE_OUT = (-0.55, 0, -0.95)    # right-side flares: out toward the lens and DOWN onto clear black under the truck
FLARE_OUT_L = (0.40, 0, 0.10)


def shots():
    S = SECS
    sh = {}
    parked_front = [part("x_bumper", still(BUMPER_PARK, BUMPER_ROT)), part("x_grille", still(GRILLE_PARK))]
    hood_open = part("x_hood", still((0, 0, 0), HOOD_OPEN), pivot=HOOD_PIVOT)

    # S3 FRONT BUMPER on the drop (as v2; base no longer carries bumper skin)
    n = "v3_s3_bumper"
    b1 = [k(0, (0, 0, 0)), k(0.60, (0, -0.70, -0.05), ease="out2"), k(1.19, BUMPER_PARK)]
    sh[n] = {"base": [f"{P}/c3_fbrhc.blend", f"{P}/c3_fbrhc_fill2.blend"],
             "parts": [part("x_bumper", b1 + [k(2.38, BUMPER_PARK), k(3.60, BUMPER_PARK, BUMPER_ROT)], "bumper", hl(n, "bumper")),
                       part("x_grille", b1 + [k(2.38, GRILLE_PARK)])],
             "cam": cam((0, (-1.4, -5.4, 1.0), (-0.1, -2.9, 0.55), 30, "lin"),
                        (1.2, (-1.3, -5.6, 1.3), (-0.06, -3.6, 0.15), 30, "inout"),
                        (3.6, (-0.6, -5.6, 2.2), (-0.06, -3.65, -0.1), 28, "inout"),
                        (S[n] + 0.2, (-0.4, -5.2, 1.9), (-0.06, -3.65, -0.1), 28, "inout"))}
    # S4 FRONT BUMPER REMOVED: low push-in on the bumper-off state
    n = "v3_s4_removed"
    sh[n] = {"base": [f"{P}/c3_fbrhc.blend", {"blend": f"{P}/c3_fbrhc_fill2.blend", "name": "fbrhc", "hl": hl(n, "fbrhc")}],
             "parts": [],
             "cam": cam((0, (0.6, -6.0, 1.15), (-0.06, -2.6, 0.78), 30, "lin"),
                        (S[n] + 0.2, (0.3, -4.4, 1.05), (-0.06, -2.55, 0.72), 32, "inout"))}
    # S5 HOOD opens on its hinge (lands 19.26); low front-right so the underside turns toward the lens
    n = "v3_s5_hood"
    sh[n] = {"base": [f"{P}/c3_front.blend", f"{P}/c3_struct.blend"],
             "parts": parked_front + [part("x_hood", [k(0, (0, 0, 0)), k(0.30, (0, 0, 0)), k(1.19, (0, 0, 0), HOOD_OPEN)],
                                           "hood", hl(n, "hood"), HOOD_PIVOT)],
             "cam": cam((0, (-2.3, -5.3, 1.35), (-0.06, -2.0, 1.05), 28, "lin"),
                        (S[n] + 0.2, (-1.7, -5.1, 1.15), (-0.06, -1.9, 1.15), 28, "inout"))}
    # S6 FRONT STRUCTURE under the open hood: front push-in at eye level
    n = "v3_s6_struct"
    sh[n] = {"base": [f"{P}/c3_front.blend", {"blend": f"{P}/c3_struct.blend", "name": "struct", "hl": hl(n, "struct")}],
             "parts": parked_front + [hood_open],
             "cam": cam((0, (-0.9, -5.6, 1.75), (-0.06, -2.3, 0.95), 30, "lin"),
                        (S[n] + 0.2, (-0.45, -4.5, 1.55), (-0.06, -2.2, 0.9), 32, "inout"))}
    # S7 FENDER FLARES: out toward the lens on 25.34, then each turns 180 deg about its own vertical axis to show its back
    n = "v3_s7_flares"
    fk = lambda out, d=0.0: [k(0, (0, 0, 0)), k(0.60 + d, (0, 0, 0)), k(1.18 + d, out), k(1.80 + d, out), k(2.95 + d, out, (0, 0, 180))]
    fl = lambda out: [k(0, (0, 0, 0)), k(0.60, (0, 0, 0)), k(1.18, out)]
    sh[n] = {"base": [f"{P}/c3_body.blend", f"{P}/c3_flarefill.blend"],
             "parts": parked_front + [hood_open,
                                      part("flare_rf", fk(FLARE_OUT), "flares", hl(n, "flares")),
                                      part("flare_rr", fk(FLARE_OUT, 0.0), None, hl(n, "flares")),
                                      part("flare_lf", fl(FLARE_OUT_L)), part("flare_lr", fl(FLARE_OUT_L))],
             "cam": keyed_orbit(S[n] + 0.2, 6.1, 5.9, -62, -76, 1.5, 1.3, (-0.3, -0.18, 0.4), (-0.3, -0.18, 0.3), focal=26)}
    # S8 home one per beat from the crash (lock 30.14); FULL TRUCK; clip fades out in the assembly
    n = "v3_s8_home"
    home = lambda park, rot, t0, t1: [k(0, park, rot), k(t0, park, rot), k(t1, (0, 0, 0), ease="in2")]
    sh[n] = {"base": [{"blend": f"{P}/c3_body.blend", "name": "body"}, f"{P}/c3_flarefill.blend"],
             "parts": [part("flare_rf", home(FLARE_OUT, (0, 0, 180), 0.0, 0.60)), part("flare_rr", home(FLARE_OUT, (0, 0, 180), 0.0, 0.60)),
                       part("flare_lf", home(FLARE_OUT_L, (0, 0, 0), 0.0, 0.60)), part("flare_lr", home(FLARE_OUT_L, (0, 0, 0), 0.0, 0.60)),
                       part("x_hood", home((0, 0, 0), HOOD_OPEN, 0.60, 1.17), pivot=HOOD_PIVOT),
                       part("x_bumper", home(BUMPER_PARK, BUMPER_ROT, 1.17, 1.77)),
                       part("x_grille", home(GRILLE_PARK, (0, 0, 0), 1.77, 2.37))],
             "hl_all": hl(n, "body"),
             "cam": keyed_orbit(S[n] + 0.2, 6.8, 6.4, -135, -150, 3.0, 1.8, (0, 0.2, 0.75), (0, 0.2, 0.75), focal=26)}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "hl_all": s.get("hl_all"), "anchors_out": f"{SPECS}/{name}_{mode}_anchors.json",
          "seconds": SECS[name] + 0.2, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6, "exposure": -0.5,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if any(len(p["keys"]) > 1 for p in sp["parts"]):
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
