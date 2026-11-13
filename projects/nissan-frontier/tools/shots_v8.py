"""v8 (user on v7): "instead of making this a 'what we scanned' video, turn the basis of this video into a 'how we modified this
truck' video. For the grille lights, we have 3D scans for that. We also have 3D scans for the fender lights."
The build, in order (timing_v8.json): stock scan -> stock grille -> bumper off -> mounts scanned [existing v2-v4 renders, new labels]
  m1_grille   trimmed bumper goes back on, Ronin grille (team CAD) parks in front, the three SCANNED grille lights drop into its
              pockets, grille + lights seat on the bumper, lights on
  m2_flares   stock flares come off              } one camera path, hidden cut on the beat
  m3_fenders  wide fenders on, push in on the front-right arch, SCANNED fender lights seat in the fender slots, lights on
  m4_wheels   35s roll in (lifted height, wider track - no clipping, see v7)   } one camera path, hidden cut
  m5_lift     the lift
  m6_livery   turbo label beat, livery sweeps on the crash, camera lands on the IMG_3223 solve -> 1:1 cut
Lights: tools/lights.py (lt_*.blend; lens = emissive 'led' / 'led2', housing black). v7's LED-bar stand-ins (r_lights) are gone.
    python projects/nissan-frontier/tools/shots_v8.py preview|final|check [shot ...]
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shots_v4 import P, OUT, SPECS, cam, k, still, keyed_orbit

HERE = os.path.dirname(__file__)
T = json.load(open(os.path.join(HERE, "..", "timing_v8.json")))
SECS = {n: f / 30 for n, f in T["frames"].items()}
MC = json.load(open(os.path.join(HERE, "..", "match", "cam_3223_lookat.json")))
WX_R, WX_L, WZ0, LIFT = -1.022, 0.938, 0.09, 0.06
WY = (-1.782, 1.433)
B = 0.6035  # beat


def part(blend, keys, name=None, mat=None, pivot=None, hl=None):
    p = {"blend": f"{P}/{blend}.blend", "keys": keys}
    if name: p["name"] = name
    if mat: p["mat"] = mat
    if pivot: p["pivot"] = pivot
    if hl: p["hl"] = hl
    return p


def grille(keys=None):
    keys = keys or still()
    return [part("rd_Upper_Grille_V1", keys, "rgrille", "black"), part("rd_Lower_Grille_V1", keys, None, "black")]


def glights(keys=None):
    keys = keys or still()
    return [part("lt_grille_body", keys, None, "black"), part("lt_grille_lens", keys, "glight", "led")]


def fenders(kR=None, kL=None):
    kR = kR or still(); kL = kL or still()
    return [part("rd_Fender_FrontRight", kR, "rfender", "black"), part("rd_Fender_RearRight", kR, None, "black"),
            part("rd_Fender_FrontLeft", kL, None, "black"), part("rd_Fender_RearLeft", kL, None, "black")]


def flights(kR=None, kL=None):
    kR = kR or still(); kL = kL or still()
    return [part("lt_fen_R_body", kR, None, "black"), part("lt_fen_R_lens", kR, "flight", "led2"),
            part("lt_fen_L_body", kL, None, "black"), part("lt_fen_L_lens", kL, None, "led2")]


def wheels(keyfn):
    ps = []
    for i, y in enumerate(WY):
        ps.append(part("wheel_r3", keyfn(WX_R, y, -1), "wheel" if i == 0 else None, pivot=[0, 0, 0]))
        ps.append(part("wheel_r3", [dict(q, rot=[0, 0, 180]) for q in keyfn(WX_L, y, 1)], pivot=[0, 0, 0]))
    return ps


def shots():
    S = SECS; sh = {}
    body = [f"{P}/c3_body.blend", f"{P}/c3_flarefill.blend"]
    front = lambda mat=None, bk=None: [part("x_hood", still(), mat=mat), part("bumper_cut", bk or still(), mat=mat)]
    # M1 grille + scanned grille lights
    n = "m1_grille"
    G = (0, -1.25, 0.0)
    bin_ = [k(0, (0, -2.6, -1.2)), k(0.1, (0, -2.6, -1.2)), k(0.75, (0, -0.5, 0), ease="out2"), k(2 * B, (0, 0, 0))]
    gin = [k(0, (0, -1.25, 2.6)), k(2 * B, (0, -1.25, 2.6)), k(3 * B, G, ease="out2"), k(5 * B, G), k(6 * B, (0, 0, 0))]
    HOV = (0, -1.25 - 0.22, 0.30)               # lights hover up-front of the parked grille, along the pocket normal
    lin = [k(0, (0, -1.47, 2.9)), k(3 * B, (0, -1.47, 2.9)), k(4 * B, HOV, ease="out2"), k(5 * B, G), k(6 * B, (0, 0, 0))]
    sh[n] = {"base": body, "parts": front(bk=bin_) + [part("flare_rf", still()), part("flare_rr", still()), part("flare_lf", still()), part("flare_lr", still())]
             + grille(gin) + glights(lin), "led": [[0, 0], [7 * B - 0.02, 0], [7 * B + 0.08, 1]],
             "cam": cam((0, (-3.0, -5.9, 1.25), (-0.06, -3.1, 0.66), 30, "lin"), (3 * B, (-2.4, -6.0, 1.3), (-0.06, -3.2, 0.72), 30, "inout"),
                        (6 * B, (-1.9, -5.3, 1.25), (-0.06, -2.9, 0.80), 32, "inout"), (S[n] + 0.2, (-1.0, -4.3, 1.3), (-0.06, -2.7, 0.86), 42, "inout"))}
    ronin_front = lambda mat=None: front(mat) + grille() + glights()
    # M2 stock flares off / M3 fenders + scanned fender lights: one camera path
    c_a, t_a = (-4.2, -6.2, 1.3), (-0.3, -0.8, 0.5)
    c_b, t_b = (-4.8, -5.9, 1.3), (-0.3, -0.5, 0.5)
    n = "m2_flares"
    hlf = [[0.55, 0], [0.8, 1], [1.6, 1], [1.85, 0]]
    offR = [k(0, (0, 0, 0)), k(2 * B, (0, 0, 0)), k(3 * B, (-0.7, 0, -0.3)), k(4 * B, (-0.7, 0, -14.0), ease="in2")]
    offL = [k(0, (0, 0, 0)), k(2 * B, (0, 0, 0)), k(3 * B, (0.7, 0, -0.3)), k(4 * B, (0.7, 0, -14.0), ease="in2")]
    sh[n] = {"base": body, "parts": ronin_front() + [part("flare_rf", offR, "sflare", hl=hlf), part("flare_rr", offR, hl=hlf), part("flare_lf", offL, hl=hlf), part("flare_lr", offL, hl=hlf)],
             "cam": cam((0, c_a, t_a, 26, "lin"), (S[n], c_b, t_b, 26, "lin"), (S[n] + 0.3, c_b, t_b, 26, "lin"))}
    n = "m3_fenders"
    inR = [k(0, (-1.6, 0, 0.5)), k(1 * B, (-1.6, 0, 0.5)), k(2 * B, (0, 0, 0), ease="out2")]
    inL = [k(0, (1.6, 0, 0.5)), k(1 * B, (1.6, 0, 0.5)), k(2 * B, (0, 0, 0), ease="out2")]
    lR = [k(0, (-1.8, 0, 2.4)), k(3 * B, (-1.8, 0, 2.4)), k(5 * B, (-0.20, 0, 0.23), ease="out2"), k(6 * B, (0, 0, 0))]
    lL = [k(0, (1.8, 0, 2.4)), k(3 * B, (1.8, 0, 2.4)), k(5 * B, (0.20, 0, 0.23), ease="out2"), k(6 * B, (0, 0, 0))]
    sh[n] = {"base": body, "parts": ronin_front() + fenders(inR, inL) + flights(lR, lL), "led2": [[0, 0], [7 * B - 0.02, 0], [7 * B + 0.08, 1]],
             "cam": cam((0, c_b, t_b, 26, "lin"), (2 * B, (-5.3, -5.2, 1.3), (-0.3, -0.4, 0.5), 26, "lin"),
                        (5 * B, (-2.8, -3.1, 1.4), (-1.0, -1.78, 0.68), 42, "inout"), (S[n] + 0.2, (-2.55, -2.8, 1.32), (-1.0, -1.78, 0.68), 42, "inout"))}
    done = lambda mat=None: ronin_front(mat) + fenders() + flights()
    # M4 wheels / M5 lift: one orbit, hidden cut
    Tw = S["m4_wheels"]; Ta = Tw + S["m5_lift"]
    orb = lambda t: keyed_orbit(Ta + 0.2, 7.0, 7.0, -62, -78, 1.2, 1.1, (-0.3, -0.3, 0.3), (-0.3, -0.2, 0.3), focal=26, n=16)
    n = "m4_wheels"
    wk = lambda x, y, s: [k(0, (x + s * 2.2, y, WZ0)), k(0.5 * B, (x + s * 2.2, y, WZ0)), k(2 * B, (x, y, WZ0), ease="out2")]
    sh[n] = {"base": [{"blend": f"{P}/c7_body_w.blend", "name": "body"}, body[1]], "parts": done() + wheels(wk),
             "cam": [q for q in orb(0) if q["t"] <= Tw + 0.6]}
    n = "m5_lift"
    wl = lambda x, y, s: [k(0, (x, y, WZ0)), k(0.5 * B, (x, y, WZ0)), k(2 * B, (x, y, WZ0 - LIFT))]
    c5 = [dict(q, t=round(q["t"] - Tw, 4), loc=list(q["loc"]), target=list(q["target"])) for q in orb(0) if q["t"] >= Tw - 0.6]
    # re-key so t=0 exists: interpolate the orbit at Tw
    full = orb(0)
    def at(t):
        for a, b in zip(full, full[1:]):
            if a["t"] <= t <= b["t"]:
                u = (t - a["t"]) / (b["t"] - a["t"])
                return {"t": 0, "loc": [a["loc"][i] + (b["loc"][i] - a["loc"][i]) * u for i in range(3)],
                        "target": [a["target"][i] + (b["target"][i] - a["target"][i]) * u for i in range(3)], "focal": 26, "ease": "lin"}
    c5 = [at(Tw)] + [q for q in c5 if q["t"] > 0.05]
    for q in c5:
        u = min(1.0, max(0.0, (q["t"] - 0.5 * B) / (1.5 * B))); u = u * u * (3 - 2 * u)
        q["loc"][2] -= LIFT * u; q["target"][2] -= LIFT * u
    sh[n] = {"base": [{"blend": f"{P}/c7_body_w.blend", "name": "body"}, body[1]], "parts": done() + wheels(wl), "cam": c5}
    sh["m4_wheels"]["cam"] = [q for q in full if q["t"] < Tw] + [dict(at(Tw), t=Tw)] + [dict(at(Tw + 0.25), t=Tw + 0.25)]
    # M6 livery: silver truck holds for the turbo label, livery sweeps on the crash (4 beats in), camera lands on the solve
    n = "m6_livery"
    ws = lambda x, y, s: still((x, y, WZ0 - LIFT))
    Tend = S[n] - 1 / 30; T0 = 3 * B
    c0 = (-4.9, -5.4, 0.95); t0 = (-0.2, -1.2, 0.3)
    pre = (-5.5, -4.6, 0.95)
    ks = [{"t": 0, "loc": list(pre), "target": list(t0), "focal": 26, "roll": 0, "ease": "lin"}]
    for i in range(11):
        u = i / 10; s_ = u * u * (3 - 2 * u)
        tg = [t0[j] + (MC["target"][j] - t0[j]) * s_ for j in range(3)]
        a0 = math.atan2(c0[0] - t0[0], -(c0[1] - t0[1])); a1 = math.atan2(MC["loc"][0] - MC["target"][0], -(MC["loc"][1] - MC["target"][1]))
        r0 = math.hypot(c0[0] - t0[0], c0[1] - t0[1]); r1 = math.hypot(MC["loc"][0] - MC["target"][0], MC["loc"][1] - MC["target"][1])
        a = a0 + (a1 - a0) * s_; r = r0 + (r1 - r0) * s_
        ks.append({"t": T0 + (Tend - T0) * u, "loc": [tg[0] + r * math.sin(a), tg[1] - r * math.cos(a), c0[2] + (MC["loc"][2] - c0[2]) * s_],
                   "target": tg, "focal": 26 + (MC["focal"] - 26) * s_, "roll": MC["roll"] * s_, "ease": "lin"})
    ks.append(dict(ks[-1], t=S[n] + 0.3))
    sw0 = 73 / 30                                # the crash (frame 1270) is 73 frames into the shot
    sh[n] = {"base": [{"blend": f"{P}/c7_body_w.blend", "name": "body", "mat": "livery"}, body[1]], "parts": done("livery") + wheels(ws),
             "livery": {"sweep": [[0, -3.2], [sw0, -3.2], [sw0 + 1.45, 3.4]]}, "cam": ks}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]; final = mode == "final"
    sp = {"base": s["base"], "parts": s["parts"], "camera": {"sensor": 20.25, "keys": s["cam"]},
          "anchors_out": f"{SPECS}/{name}_{mode}_anchors.json", "seconds": SECS[name] + 0.2, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6, "exposure": -0.5, "persistent": False,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    for f in ("livery", "led", "led2"):
        if s.get(f): sp[f] = s[f]
    if frames: sp["frames"] = frames
    p = f"{SPECS}/{name}_{mode}.json"; json.dump(sp, open(p, "w"), indent=1); return p


if __name__ == "__main__":
    mode = sys.argv[1]; fr = None
    if mode == "check": mode, fr = "preview", ["first", "mid", "last"]
    for n in sys.argv[2:] or list(shots()): print(spec(n, mode, fr))
