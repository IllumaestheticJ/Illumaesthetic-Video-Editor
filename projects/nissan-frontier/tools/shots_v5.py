"""v5 = v4 + the RONIN section (user: transition into how the truck became the Ronin Nissan Frontier).
    python projects/nissan-frontier/tools/shots_v5.py preview|final|check [shot ...]
Sources (clips.md): Ronin upper/lower grille + 4 wide fenders = the team's CAD from Drive 'Nissan Frontier (SEMA 2026)/STL',
registered to the scan (ronin_T.json); livery = the user's PSD/SVG files (tools/livery_tex.py); wheels/tyres = a generic
stand-in built to the published 35x12.50R17 / 17x9 beadlock spec (tools/make_wheel.py) - NOT scan data; lift shown as the
wheels dropping 0.10 m (published: 'over four inches') with the camera following; the turbo has no model - label only.
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import shots_v4 as v4
from shots_v4 import P, OUT, SPECS, cam, k, still, keyed_orbit

T = json.load(open(os.path.join(os.path.dirname(__file__), "..", "timing_v5.json")))
SECS = {n: f / 30 for n, f in T["frames"].items()}
WX_R, WX_L, WZ0, LIFT = -0.917, 0.833, 0.29, 0.10
WY = (-1.782, 1.433)
CAD = ("Upper_Grille_V1", "Lower_Grille_V1", "Fender_FrontRight", "Fender_RearRight", "Fender_FrontLeft", "Fender_RearLeft")


def part(blend, keys, name=None, mat=None, pivot=None):
    p = {"blend": f"{P}/{blend}.blend", "keys": keys}
    if name: p["name"] = name
    if mat: p["mat"] = mat
    if pivot: p["pivot"] = pivot
    return p


def cad_static(which=CAD, mat="black"):
    return [part("rd_" + c, still(), {"Upper_Grille_V1": "rgrille", "Fender_FrontRight": "rfender"}.get(c), mat) for c in which]


def wheels(keyfn):
    ps = []
    for i, y in enumerate(WY):
        ps.append(part("wheel_r", keyfn(WX_R, y, -1), "wheel" if i == 0 else None, pivot=[0, 0, 0]))
        ps.append(part("wheel_r", [dict(q, rot=[0, 0, 180]) for q in keyfn(WX_L, y, 1)], pivot=[0, 0, 0]))
    return ps


def shots():
    S = SECS; sh = {}
    body = [f"{P}/c3_body.blend", f"{P}/c3_flarefill.blend"]
    stock_flares = lambda keysR, keysL: [part("flare_rf", keysR), part("flare_rr", keysR), part("flare_lf", keysL), part("flare_lr", keysL)]
    # R1 RONIN GRILLE: stock grille lifts out, CAD upper + lower grille slide in from the lens side (home 1.21 = onset)
    n = "r1_grille"
    gin = [k(0, (0, -1.7, -0.1)), k(0.55, (0, -1.7, -0.1)), k(1.21, (0, 0, 0), ease="out2")]
    sh[n] = {"base": body, "parts": [part("x_hood", still()), part("x_bumper", still())] + stock_flares(still(), still()) + [
                 part("x_grille", [k(0, (0, 0, 0)), k(0.15, (0, 0, 0)), k(0.45, (0, -0.35, 0)), k(1.0, (0, -0.5, 1.9))]),
                 part("rd_Upper_Grille_V1", gin, "rgrille", "black"), part("rd_Lower_Grille_V1", gin, None, "black")],
             "cam": cam((0, (-1.9, -5.6, 1.1), (-0.06, -2.7, 0.62), 34, "lin"), (S[n] + 0.2, (-1.3, -5.3, 1.0), (-0.06, -2.7, 0.62), 34, "inout"))}
    # R2 WIDE FENDERS: stock flares drop away, CAD fenders arrive from outside (home 1.21)
    n = "r2_fenders"
    offR = [k(0, (0, 0, 0)), k(0.1, (0, 0, 0)), k(0.7, (-0.7, 0, -0.5)), k(1.15, (-0.7, 0, -14.0), ease="in2")]
    offL = [k(0, (0, 0, 0)), k(0.1, (0, 0, 0)), k(0.7, (0.7, 0, -0.5)), k(1.15, (0.7, 0, -14.0), ease="in2")]
    inR = [k(0, (-1.5, 0, 0.5)), k(0.5, (-1.5, 0, 0.5)), k(1.21, (0, 0, 0), ease="out2")]
    inL = [k(0, (1.5, 0, 0.5)), k(0.5, (1.5, 0, 0.5)), k(1.21, (0, 0, 0), ease="out2")]
    sh[n] = {"base": body, "parts": [part("x_hood", still()), part("x_bumper", still())] + cad_static(CAD[:2]) + stock_flares(offR, offL) + [
                 part("rd_Fender_FrontRight", inR, "rfender", "black"), part("rd_Fender_RearRight", inR, None, "black"),
                 part("rd_Fender_FrontLeft", inL, None, "black"), part("rd_Fender_RearLeft", inL, None, "black")],
             "cam": keyed_orbit(S[n] + 0.2, 7.2, 7.0, -58, -68, 1.4, 1.3, (-0.3, -0.2, 0.55), (-0.3, -0.2, 0.5), focal=26)}
    # R3 WHEELS + TIRES roll in (home 1.2), then LIFT: wheels drop 0.10 m and the camera follows (1.8 -> 2.4)
    n = "r3_lift"
    wk = lambda x, y, s: [k(0, (x + s * 2.2, y, WZ0)), k(0.55, (x + s * 2.2, y, WZ0)), k(1.2, (x, y, WZ0), ease="out2"), k(1.8, (x, y, WZ0)), k(2.4, (x, y, WZ0 - LIFT))]
    c3 = keyed_orbit(S[n] + 0.2, 7.0, 7.0, -68, -80, 1.3, 1.2, (-0.3, -0.2, 0.42), (-0.3, -0.2, 0.42), focal=26)
    for q in c3:   # follow the lift
        u = min(1.0, max(0.0, (q["t"] - 1.8) / 0.6)); u = u * u * (3 - 2 * u)
        q["loc"][2] -= LIFT * u; q["target"][2] -= LIFT * u
    sh[n] = {"base": [{"blend": body[0], "name": "body"}, body[1]], "parts": [part("x_hood", still()), part("x_bumper", still())] + cad_static() + wheels(wk), "cam": c3}
    # R4 RONIN LIVERY sweeps nose -> tail on the crash; orbit to the front-right hero; clip fades in the assembly
    n = "r4_livery"
    ws = lambda x, y, s: still((x, y, WZ0 - LIFT))
    sh[n] = {"base": [{"blend": body[0], "name": "body", "mat": "livery"}, body[1]],
             "parts": [part("x_hood", still(), mat="livery"), part("x_bumper", still(), mat="livery")] + cad_static() + wheels(ws),
             "livery": {"sweep": [[0, -3.2], [0.1, -3.2], [1.6, 3.4]]},
             "cam": keyed_orbit(S[n] + 0.2, 7.9, 7.0, -80, -36, 1.1, 1.35, (0, -0.2, 0.32), (0, -0.2, 0.35), focal=26)}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]; final = mode == "final"
    sp = {"base": s["base"], "parts": s["parts"], "camera": {"sensor": 20.25, "keys": s["cam"]},
          "anchors_out": f"{SPECS}/{name}_{mode}_anchors.json", "seconds": SECS[name] + 0.2, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6, "exposure": -0.5, "persistent": False,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if s.get("livery"): sp["livery"] = s["livery"]
    if frames: sp["frames"] = frames
    p = f"{SPECS}/{name}_{mode}.json"; json.dump(sp, open(p, "w"), indent=1); return p


if __name__ == "__main__":
    mode = sys.argv[1]; fr = None
    if mode == "check": mode, fr = "preview", ["first", "mid", "last"]
    for n in sys.argv[2:] or list(shots()): print(spec(n, mode, fr))
