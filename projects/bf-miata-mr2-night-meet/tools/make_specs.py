"""v1 shot specs: both cars start STOCK and the sale parts install one zone at a time (user feedback on v0.1).
15 fps renders, doubled to 30 fps at assembly. Cut times = attacks measured in Tokyo Midnight (specs/timeline.json)."""
import json, math, os
M = "/home/user/media/bf-miata-mr2-night-meet"
F30 = json.load(open("specs/timeline.json"))["f30"]
def n15(i): return math.ceil((F30[i + 1] - F30[i]) / 2) + 1
def cam(a, b, n, ta, tb=None, lens=30):
    return [{"f": 0, "loc": a, "target": ta, "lens": lens}, {"f": n - 1, "loc": b, "target": tb or ta, "lens": lens}]
def lerp(a, b, u): return [x + (y - x) * u for x, y in zip(a, b)]
def sw(zone, n, a=0.10, b=0.38, c=0.34, d=0.72, **k):       # swap timed as fractions of the shot
    return dict(zone=zone, off=[round(n * a), round(n * b)], on=[round(n * c), round(n * d)], **k)
S = {}
# MR2 ---------------------------------------------------------------------------------------------------------------
A, B = [3.3, -4.3, 0.6], [2.4, -3.2, 0.48]; T = [0.35, -0.55, 0.42]
n1, n2 = n15(0), n15(1); u = (n1 - 1) / (n1 + n2 - 2)
S["s01"] = {"mode": "cgi", "cars": [{"car": "mr2"}], "camera": cam(A, lerp(A, B, u), n1, T, lens=26)}
S["s02"] = {"mode": "scan", "cars": [{"car": "mr2", "swap": [sw("skirts", n2, dir=[0.9, 0, 0.5], dist=6, **{"from": [1.2, 0, 0.3]})]}],
            "camera": cam(lerp(A, B, u), B, n2, T, lens=26)}
n = n15(2)
S["s03"] = {"mode": "cgi", "cars": [{"car": "mr2", "on": ["skirts"], "swap": [sw("eyelids", n, dir=[0, -0.6, 0.8], dist=4, **{"from": [0, -0.5, 0.5]})]}],
            "camera": cam([1.45, -2.85, 0.95], [1.25, -2.95, 0.92], n, [0.55, -1.58, 0.63], lens=50)}
n = n15(3)
S["s04"] = {"mode": "cgi", "cars": [{"car": "mr2", "on": ["skirts", "eyelids"], "swap": [sw("hood", n, dir=[0, -0.3, 1], dist=5, **{"from": [0, 0, 0.8]})]}],
            "camera": cam([1.5, -3.4, 2.1], [1.1, -3.1, 1.95], n, [0, -1.45, 0.66], lens=42)}
n = n15(4)
S["s05"] = {"mode": "cgi", "cars": [{"car": "mr2", "on": ["skirts", "eyelids", "hood"],
                                     "swap": [sw("spats", n, 0.06, 0.24, 0.20, 0.44, dir=[0, 1, 0.2], dist=5, **{"from": [0, 1.0, 0.2]}),
                                              sw("duck", n, 0.46, 0.64, 0.60, 0.86, dir=[0, 0.4, 1], dist=5, **{"from": [0, 0.3, 0.8]})]}],
            "camera": cam([2.2, 5.0, 0.5], [2.0, 4.6, 1.0], n, [0, 1.5, 0.55], lens=28)}
# NC ----------------------------------------------------------------------------------------------------------------
A, B = [-3.5, -4.8, 0.6], [-2.8, -3.9, 0.5]; T = [0.0, -1.0, 0.42]
n6, n7 = n15(5), n15(6); u = (n6 - 1) / (n6 + n7 - 2)
S["s06"] = {"mode": "cgi", "cars": [{"car": "nc"}], "camera": cam(A, lerp(A, B, u), n6, T, lens=26)}
S["s07"] = {"mode": "scan", "cars": [{"car": "nc", "swap": [sw("bumper", n7, 0.08, 0.36, 0.40, 0.78, dir=[-0.3, -1, 0.3], dist=7, **{"from": [0, -1.5, 0.2]})]}],
            "camera": cam(lerp(A, B, u), B, n7, T, lens=26)}
n = n15(7)
S["s08"] = {"mode": "scan", "cars": [{"car": "nc", "on": ["bumper"], "swap": [sw("fender", n, dir=[-1, -0.2, 0.6], dist=6, **{"from": [-1.2, 0, 0.4]})]}],
            "camera": cam([-2.9, -2.9, 1.0], [-3.0, -2.2, 1.0], n, [-0.75, -0.95, 0.45], lens=34)}
n = n15(8)
S["s09"] = {"mode": "cgi", "cars": [{"car": "nc", "on": ["bumper", "fender"],
                                    "swap": [sw("skirts", n, 0.06, 0.24, 0.20, 0.46, dir=[-1, 0, 0.3], dist=5, **{"from": [-1.0, 0, 0.2]}),
                                             sw("spats", n, 0.48, 0.64, 0.60, 0.86, dir=[0, 1, 0.2], dist=5, **{"from": [0, 0.9, 0.2]})]}],
            "camera": cam([-3.9, 0.2, 0.75], [-3.7, 1.6, 0.75], n, [-0.6, -0.1, 0.35], [-0.5, 0.7, 0.35], lens=28)}
mr2s = {"car": "mr2", "offset": [1.1, 0.25, 0], "yaw": -14, "on": ["skirts", "eyelids", "hood", "spats", "duck"]}
ncs = {"car": "nc", "offset": [-1.1, 0.25, 0], "yaw": 14, "on": ["bumper", "fender", "skirts", "spats"]}
S["s10"] = {"mode": "scan", "cars": [mr2s, ncs], "camera": cam([0.5, -7.8, 2.8], [0.4, -7.2, 1.7], n15(9), [0, 0.1, 0.45], [0, 0.1, 0.55], lens=30)}
for k, s in S.items():
    i = int(k[1:]) - 1
    s.update({"out": f"{M}/work/{k}", "frames": n15(i), "fps": 15, "res": [540, 960], "samples": 16 if s["mode"] == "cgi" else 12})
    json.dump(s, open(f"specs/{k}.json", "w"), indent=1)
print({k: s["frames"] for k, s in S.items()}, "total", sum(s["frames"] for s in S.values()))
