"""v7 (user notes on v6): NO bumper bar; bumper cutaway follows the CAD grille's own silhouette (bumper_cut / bumper_cutpiece);
order = cutaway -> new grille shown in front -> lights go INTO the grille -> grille + lights go onto the cut bumper -> lights on;
wheels v3 are solid and sit on a wider track at lifted height only (no clipping: 0 body/fender/bumper points inside the tyre
ring at |x| 0.98, z 0.09 and below), scanned hub/suspension inside the wheel volume carved (c7_body_w).
v6 Ronin section (user notes on v5): grille install no longer clips the old parts (the stock bumper's grille window
leaves with the stock grille), grille LIGHTS go in and switch on, front BUMPER BAR, more accurate wheels, higher lift,
and the livery shot ENDS on the camera solved against the real SEMA footage (match/cam_3223*.json) for a 1:1 cut.
    python projects/nissan-frontier/tools/shots_v7.py preview|final|check [shot ...]
Stand-ins, not data: wheels/tyres (make_wheel.py), bar + skid + hooks + LED bars (make_bar.py) - modelled from the footage.
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shots_v4 import P, OUT, SPECS, cam, k, still, keyed_orbit

HERE = os.path.dirname(__file__)
T = json.load(open(os.path.join(HERE, "..", "timing_v7.json")))
SECS = {n: f / 30 for n, f in T["frames"].items()}
MC = json.load(open(os.path.join(HERE, "..", "match", "cam_3223_lookat.json")))
WX_R, WX_L, WZ0, LIFT = -1.022, 0.938, 0.09, 0.06   # roll in at 0.09 (clear), lift to 0.03
WY = (-1.782, 1.433)
CAD = ("Upper_Grille_V1", "Lower_Grille_V1", "Fender_FrontRight", "Fender_RearRight", "Fender_FrontLeft", "Fender_RearLeft")


def part(blend, keys, name=None, mat=None, pivot=None):
    p = {"blend": f"{P}/{blend}.blend", "keys": keys}
    if name: p["name"] = name
    if mat: p["mat"] = mat
    if pivot: p["pivot"] = pivot
    return p


def cad_static(which=CAD):
    return [part("rd_" + c, still(), {"Upper_Grille_V1": "rgrille", "Fender_FrontRight": "rfender"}.get(c), "black") for c in which]


def wheels(keyfn):
    ps = []
    for i, y in enumerate(WY):
        ps.append(part("wheel_r3", keyfn(WX_R, y, -1), "wheel" if i == 0 else None, pivot=[0, 0, 0]))
        ps.append(part("wheel_r3", [dict(q, rot=[0, 0, 180]) for q in keyfn(WX_L, y, 1)], pivot=[0, 0, 0]))
    return ps


def shots():
    S = SECS; sh = {}
    body = [f"{P}/c3_body.blend", f"{P}/c3_flarefill.blend"]
    front = lambda mat=None: [part("x_hood", still(), mat=mat), part("bumper_cut", still(), mat=mat)]
    flares = lambda kR, kL: [part("flare_rf", kR), part("flare_rr", kR), part("flare_lf", kL), part("flare_lr", kL)]
    # Q1 RONIN GRILLE + LIGHTS: stock grille and the bumper's grille window leave together (0.3-1.0); LED bars slide in
    # (0.9-1.5); CAD upper + lower grille slide in over them (home 2.42 = onset); lights switch on at 3.04 (onset)
    n = "q1_grille"
    out = [k(0, (0, 0, 0)), k(0.2, (0, 0, 0)), k(0.5, (0, -0.45, 0)), k(0.95, (0, -0.7, 2.6), ease="in2")]
    G = (0, -1.25, 0.0)                         # the new grille parks 1.25 m in front of the cut bumper
    gin = [k(0, (0, -1.25, 2.6)), k(0.6, (0, -1.25, 2.6)), k(1.21, G, ease="out2"), k(1.9, G), k(2.42, (0, 0, 0))]
    lin = [k(0, (0, -0.45, 2.6)), k(1.0, (0, -0.45, 2.6)), k(1.45, (0, -0.45, 0), ease="out2"), k(1.81, G), k(1.9, G), k(2.42, (0, 0, 0))]
    sh[n] = {"base": body, "parts": front() + flares(still(), still()) + [
                 part("x_grille", out), part("bumper_cutpiece", out), part("r_lights", lin),
                 part("rd_Upper_Grille_V1", gin, "rgrille", "black"), part("rd_Lower_Grille_V1", gin, None, "black")],
             "led": [[0, 0], [3.0, 0], [3.1, 1]],
             "cam": cam((0, (-3.0, -5.9, 1.25), (-0.06, -3.1, 0.66), 30, "lin"), (S[n] + 0.2, (-2.2, -6.0, 1.1), (-0.06, -3.0, 0.66), 30, "inout"))}
    # Q2 WIDE FENDERS: stock flares drop away, the CAD fenders arrive (home 1.215). (v6 bumper bar removed: not accurate)
    n = "q2_bar"
    offR = [k(0, (0, 0, 0)), k(0.35, (0, 0, 0)), k(0.75, (-0.7, 0, -0.5)), k(1.1, (-0.7, 0, -14.0), ease="in2")]
    offL = [k(0, (0, 0, 0)), k(0.35, (0, 0, 0)), k(0.75, (0.7, 0, -0.5)), k(1.1, (0.7, 0, -14.0), ease="in2")]
    inR = [k(0, (-1.6, 0, 0.5)), k(0.7, (-1.6, 0, 0.5)), k(1.215, (0, 0, 0), ease="out2")]
    inL = [k(0, (1.6, 0, 0.5)), k(0.7, (1.6, 0, 0.5)), k(1.215, (0, 0, 0), ease="out2")]
    sh[n] = {"base": body, "parts": front() + cad_static(CAD[:2]) + [part("r_lights", still())] + flares(offR, offL) + [
                 part("rd_Fender_FrontRight", inR, "rfender", "black"), part("rd_Fender_RearRight", inR, None, "black"),
                 part("rd_Fender_FrontLeft", inL, None, "black"), part("rd_Fender_RearLeft", inL, None, "black")],
             "cam": keyed_orbit(S[n] + 0.2, 7.0, 7.0, -40, -62, 1.3, 1.3, (-0.3, -0.5, 0.5), (-0.3, -0.3, 0.45), focal=26)}
    done = lambda mat=None: front(mat) + cad_static() + [part("r_lights", still())]
    # Q3 35-INCH WHEELS roll in at lifted height (home 0.63), then the LIFT: wheels drop a further 0.06 m, camera follows
    n = "q3_lift"
    wk = lambda x, y, s: [k(0, (x + s * 2.2, y, WZ0)), k(0.05, (x + s * 2.2, y, WZ0)), k(0.63, (x, y, WZ0), ease="out2"), k(1.16, (x, y, WZ0)), k(1.81, (x, y, WZ0 - LIFT))]
    c3 = keyed_orbit(S[n] + 0.2, 7.0, 7.0, -62, -76, 1.2, 1.1, (-0.3, -0.3, 0.3), (-0.3, -0.2, 0.3), focal=26)
    for q in c3:
        u = min(1.0, max(0.0, (q["t"] - 1.16) / 0.65)); u = u * u * (3 - 2 * u)
        q["loc"][2] -= LIFT * u; q["target"][2] -= LIFT * u
    sh[n] = {"base": [{"blend": f"{P}/c7_body_w.blend", "name": "body"}, body[1]], "parts": done() + wheels(wk), "cam": c3}
    # Q4 RONIN LIVERY sweeps nose -> tail on the crash while the camera swings across the nose and LANDS on the camera
    # solved against IMG_3223 @ 2.4 s (loc/target/roll/focal from match/cam_3223_lookat.json) on the last used frame
    n = "q4_livery"
    ws = lambda x, y, s: still((x, y, WZ0 - LIFT))
    Tend = S[n] - 1 / 30
    c0 = (-4.9, -5.4, 0.95); t0 = (-0.2, -1.2, 0.3)
    ks = []
    for i in range(11):
        u = i / 10; s_ = u * u * (3 - 2 * u)
        # swing the camera on an arc about the final target so it never cuts through the nose
        tg = [t0[j] + (MC["target"][j] - t0[j]) * s_ for j in range(3)]
        a0 = math.atan2(c0[0] - t0[0], -(c0[1] - t0[1])); a1 = math.atan2(MC["loc"][0] - MC["target"][0], -(MC["loc"][1] - MC["target"][1]))
        r0 = math.hypot(c0[0] - t0[0], c0[1] - t0[1]); r1 = math.hypot(MC["loc"][0] - MC["target"][0], MC["loc"][1] - MC["target"][1])
        a = a0 + (a1 - a0) * s_; r = r0 + (r1 - r0) * s_
        ks.append({"t": Tend * u, "loc": [tg[0] + r * math.sin(a), tg[1] - r * math.cos(a), c0[2] + (MC["loc"][2] - c0[2]) * s_],
                   "target": tg, "focal": 26 + (MC["focal"] - 26) * s_, "roll": MC["roll"] * s_, "ease": "lin"})
    ks.append(dict(ks[-1], t=S[n] + 0.3))
    sh[n] = {"base": [{"blend": f"{P}/c7_body_w.blend", "name": "body", "mat": "livery"}, body[1]], "parts": done("livery") + wheels(ws),
             "livery": {"sweep": [[0, -3.2], [0.05, -3.2], [1.5, 3.4]]}, "cam": ks}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]; final = mode == "final"
    sp = {"base": s["base"], "parts": s["parts"], "camera": {"sensor": 20.25, "keys": s["cam"]},
          "anchors_out": f"{SPECS}/{name}_{mode}_anchors.json", "seconds": SECS[name] + 0.2, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6, "exposure": -0.5, "persistent": False,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    for f in ("livery", "led"):
        if s.get(f): sp[f] = s[f]
    if frames: sp["frames"] = frames
    p = f"{SPECS}/{name}_{mode}.json"; json.dump(sp, open(p, "w"), indent=1); return p


if __name__ == "__main__":
    mode = sys.argv[1]; fr = None
    if mode == "check": mode, fr = "preview", ["first", "mid", "last"]
    for n in sys.argv[2:] or list(shots()): print(spec(n, mode, fr))
