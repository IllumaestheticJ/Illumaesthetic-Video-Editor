"""v2.2 (user: "can this be done entirely on game models? ... cutting back and forth between game/scan feels unnecessary"):
every shot is the lookbook model in the night lot. Scan data only supplies what the lookbook lacks (NC stock nose/fender,
what sits behind both bumpers, NC TC wing placement).
v1.9: re-timed for the owner text rule (every price label readable >= 3 s): longer bars on text shots, installs in seconds.
v1.5: shots lengthened (user: text longer for slow readers); two-part shots install both parts by ~60 %.
v1 shot specs: both cars start STOCK and the sale parts install one zone at a time (user feedback on v0.1).
15 fps renders, doubled to 30 fps at assembly. Cut times = attacks measured in Tokyo Midnight (specs/timeline.json)."""
import json, math, os
M = "/home/user/media/bf-miata-mr2-night-meet"
TLJ = json.load(open("specs/timeline.json")); F30 = TLJ["f30"]; ORDER = TLJ["order"]
def n15(i): return math.ceil((F30[i + 1] - F30[i]) / 2) + 1
def N(k): return n15(ORDER.index(k))
def cam(a, b, n, ta, tb=None, lens=30):
    return [{"f": 0, "loc": a, "target": ta, "lens": lens}, {"f": n - 1, "loc": b, "target": tb or ta, "lens": lens}]
def cam3(a, ta, b, tb, u, c, tc, n, lens=(30, 30)):    # 3 keys: a -> b at fraction u -> c at the end
    k = round((n - 1) * u)
    return [{"f": 0, "loc": a, "target": ta, "lens": lens[0]}, {"f": k, "loc": b, "target": tb, "lens": lens[1]},
            {"f": n - 1, "loc": c, "target": tc, "lens": lens[1]}]
def ss(zone, a, b, c, d, **k):   # v1.9: swap timed in SECONDS (owner text rule: parts land early, labels hold >= 3 s)
    return dict(zone=zone, off=[round(a * 15), round(b * 15)], on=[round(c * 15), round(d * 15)], **k)
A1, A2 = (0.10, 0.50, 0.40, 1.20), (1.30, 1.75, 1.65, 2.40)     # first / second install in a two-part shot
ONE = (0.15, 0.60, 0.50, 1.30)                                  # single-part shot
def camk(keys, n, lens=30):      # keys: (seconds | None = last frame, loc, target)
    return [{"f": (n - 1 if t is None else round(t * 15)), "loc": a, "target": b, "lens": lens} for t, a, b in keys]
def lerp(a, b, u): return [x + (y - x) * u for x, y in zip(a, b)]
def sw(zone, n, a=0.10, b=0.38, c=0.34, d=0.72, **k):       # swap timed as fractions of the shot
    return dict(zone=zone, off=[round(n * a), round(n * b)], on=[round(n * c), round(n * d)], **k)
S = {}
# MR2 ---------------------------------------------------------------------------------------------------------------
A, B = [3.3, -4.3, 0.6], [2.4, -3.2, 0.48]; T = [0.35, -0.55, 0.42]
n1, n2 = N("s01"), N("s02"); u = (n1 - 1) / (n1 + n2 - 2)
S["s01"] = {"mode": "cgi", "cars": [{"car": "mr2"}], "camera": cam(A, lerp(A, B, u), n1, T, lens=26)}
# v1.8 (user: "MR2 spyder doesn't show the front bumper"): the bumper installs after the skirts in the same front-3/4 scan shot
# v2.0 (user: "focus on the bumper on the Spyder ... when it gets removed/readded - currently doing it off-frame"):
# skirts first from the match-cut angle, then the camera moves to the nose and holds while the bumper swaps in view.
S["s02"] = {"mode": "cgi", "cars": [{"car": "mr2", "swap": [ss("skirts", *A1, dir=[0.9, 0, 0.5], dist=6, **{"from": [1.2, 0, 0.3]}),
                                                         ss("bumper", 1.9, 2.4, 2.3, 3.1, dir=[-0.5, -0.35, 1], dist=2.6, **{"from": [0, -1.2, 0.2]})]}],
            "camera": camk([(0, lerp(A, B, u), T), (1.2, B, T), (1.9, [1.8, -4.0, 0.85], [0.1, -1.75, 0.45]),
                            (None, [1.65, -4.05, 0.8], [0.1, -1.75, 0.45])], n2, lens=26)}
n = N("s03")
S["s03"] = {"mode": "cgi", "cars": [{"car": "mr2", "on": ["bumper", "skirts"], "swap": [ss("eyelids", *ONE, dir=[0, -0.6, 0.8], dist=4, **{"from": [0, -0.5, 0.5]})]}],
            "camera": cam([1.45, -2.85, 0.95], [1.25, -2.95, 0.92], n, [0.55, -1.58, 0.63], lens=50)}
n = N("s04")
S["s04"] = {"mode": "cgi", "cars": [{"car": "mr2", "on": ["bumper", "skirts", "eyelids"], "swap": [ss("hood", *ONE, dir=[0, -0.3, 1], dist=5, **{"from": [0, 0, 0.8]})]}],
            "camera": cam([1.5, -3.4, 2.1], [1.1, -3.1, 1.95], n, [0, -1.45, 0.66], lens=42)}
n = N("s05")
S["s05"] = {"mode": "cgi", "cars": [{"car": "mr2", "on": ["bumper", "skirts", "eyelids", "hood"],
                                     "swap": [ss("spats", *A1, dir=[0, 1, 0.2], dist=5, **{"from": [0, 1.0, 0.2]}),
                                              ss("duck", *A2, dir=[0, 0.4, 1], dist=5, **{"from": [0, 0.3, 0.8]})]}],
            # v1.8 (user: "the rear spats dont show up in the screen"): low close-up on the corner while they land, then pull back
            "camera": cam3([1.75, 2.75, 0.22], [0.75, 1.68, 0.30], [1.65, 2.85, 0.24], [0.75, 1.68, 0.30], 0.24,
                           [2.0, 4.6, 1.0], [0, 1.5, 0.55], n, lens=(32, 28))}
# NC ----------------------------------------------------------------------------------------------------------------
A, B = [-3.5, -4.8, 0.6], [-2.8, -3.9, 0.5]; T = [0.0, -1.0, 0.42]
n6, n7 = N("s06"), N("s07"); u = (n6 - 1) / (n6 + n7 - 2)
S["s06"] = {"mode": "cgi", "cars": [{"car": "nc"}], "camera": cam(A, lerp(A, B, u), n6, T, lens=26)}
S["s07"] = {"mode": "cgi", "cars": [{"car": "nc", "swap": [ss("bumper", 0.15, 0.70, 0.60, 1.50, dir=[-0.3, -1, 0.3], dist=7, **{"from": [0, -1.5, 0.2]})]}],
            "camera": cam(lerp(A, B, u), B, n7, T, lens=26)}
n = N("s08")
S["s08"] = {"mode": "cgi", "cars": [{"car": "nc", "on": ["bumper"], "swap": [ss("fender", *ONE, dir=[-1, -0.2, 0.6], dist=6, **{"from": [-1.2, 0, 0.4]})]}],
            "camera": cam([-2.9, -2.9, 1.0], [-3.0, -2.2, 1.0], n, [-0.75, -0.95, 0.45], lens=34)}
n = N("s09")
S["s09"] = {"mode": "cgi", "cars": [{"car": "nc", "on": ["bumper", "fender"],
                                    "swap": [ss("skirts", *A1, dir=[-0.2, -1, 0.15], dist=3.5, **{"from": [-0.8, 0, 0.1]}),
                                             ss("spats", 1.8, 2.3, 2.2, 3.0, dir=[0, 1, 0.2], dist=5, **{"from": [0, 0.9, 0.2]})]}],
            # v2.0 (user: "focus on ... the side skirt on the NC when it gets removed/readded"): hold a low side view on the
            # skirt until it has landed, then drop to the low rear-corner close-up for the spats (v1.8)
            "camera": camk([(0, [-3.9, -0.15, 0.5], [-0.75, -0.1, 0.28]), (1.3, [-3.8, 0.0, 0.5], [-0.75, -0.1, 0.28]),
                            (2.1, [-1.75, 2.75, 0.2], [-0.75, 1.6, 0.34]), (None, [-1.6, 2.6, 0.22], [-0.75, 1.6, 0.34])], n, lens=28)}
n = N("s05b")
S["s05b"] = {"mode": "cgi", "cars": [{"car": "mr2", "on": ["bumper", "skirts", "eyelids", "hood", "spats", "duck"],
                                      "swap": [ss("diffuser", *A1, dir=[0, 1, -0.2], dist=5, **{"from": [0, 1.2, -0.25]}),
                                               ss("wing", *A2, dir=[0, 0, 1], dist=5, **{"from": [0, 0.2, 1.4]})]}],
             "camera": cam([2.9, 5.4, 0.55], [2.4, 4.9, 0.85], n, [0, 1.65, 0.55], [0, 1.6, 0.68], lens=30)}
n = N("s09b")
S["s09b"] = {"mode": "cgi", "cars": [{"car": "nc", "on": ["bumper", "fender", "skirts", "spats"],
                                      "swap": [ss("wing", *ONE, dir=[0, 0, 1], dist=5, **{"from": [0, 0.2, 1.4]})]}],
             "camera": cam([-2.6, 5.4, 1.5], [-2.1, 4.8, 1.85], n, [0, 1.6, 0.8], lens=30)}
mr2s = {"car": "mr2", "offset": [0.85, 2.7, 0], "yaw": -8, "on": ["bumper", "skirts", "eyelids", "hood", "spats", "duck", "diffuser", "wing"]}
ncs = {"car": "nc", "offset": [-0.85, -1.7, 0], "yaw": 8, "on": ["bumper", "fender", "skirts", "spats", "wing"]}
S["s10"] = {"mode": "cgi", "cars": [mr2s, ncs], "camera": cam([4.6, -7.9, 1.5], [4.1, -7.1, 1.2], N("s10"), [-0.5, 0.3, 0.55], lens=26)}   # v1.3: cars staggered front/back, 0.5 m+ apart (they clipped side by side)
for k, s in S.items():
    s.update({"out": f"{M}/work/{k}", "frames": N(k), "fps": 15, "res": [540, 960], "samples": 16 if s["mode"] == "cgi" else 12})
    json.dump(s, open(f"specs/{k}.json", "w"), indent=1)
print({k: s["frames"] for k, s in S.items()}, "total", sum(s["frames"] for s in S.values()))
