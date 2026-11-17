"""v0 shot specs (15 fps renders, doubled to 30 fps at assembly). Cut times = measured onsets of Tokyo Midnight."""
import json, math, os
M = "/home/user/media/bf-miata-mr2-night-meet"; D = f"{M}/dec"; KM = f"{M}/kit_mr2"; KN = f"{M}/kit_nc"
CUTS = [0, 2.043, 4.505, 5.341, 6.153, 7.779, 9.427, 11.912, 14.373, 16.022, 18.483, 21.78, 24.218, 25.8]
F30 = [round(t * 30) for t in CUTS]
def n15(i): return math.ceil((F30[i + 1] - F30[i]) / 2) + 1
def cam(a, b, n, tgt_a, tgt_b=None, lens=30):
    return [{"f": 0, "loc": a, "target": tgt_a, "lens": lens}, {"f": n - 1, "loc": b, "target": tgt_b or tgt_a, "lens": lens}]
def lerp(a, b, u): return [x + (y - x) * u for x, y in zip(a, b)]
S = {}
# s1 CGI MR2 -> hard 1:1 into s2 scan with the same camera path (continues)
A, B = [3.3, -4.3, 0.6], [2.4, -3.2, 0.48]; T = [0.35, -0.55, 0.42]
n1, n2 = n15(0), n15(1); u = (n1 - 1) / (n1 + n2 - 2)
S["s01"] = {"mode": "cgi", "cars": [{"car": "mr2"}], "camera": cam(A, lerp(A, B, u), n1, T, lens=26), "samples": 16}
S["s02"] = {"mode": "scan", "cars": [{"car": "mr2"}], "camera": cam(lerp(A, B, u), B, n2, T, lens=26),
            "anim": [{"car": 0, "cut": f"{D}/mr2_cut_skirts.stl", "off": [3, 11], "dir": [0.6, -0.1, 1], "dist": 7,
                      "part": [f"{KM}/part_side_skirts.stl"], "on": [10, 22], "from": [0, 0, 1.5]}]}
S["s03"] = {"mode": "cgi", "cars": [{"car": "mr2"}], "camera": cam([1.25, -2.75, 0.85], [0.55, -2.85, 0.85], n15(2), [0.75, -1.55, 0.62], [0.1, -1.6, 0.62], lens=50), "samples": 16}
S["s04"] = {"mode": "cgi", "cars": [{"car": "mr2"}], "camera": cam([1.5, -3.4, 2.1], [1.1, -3.1, 1.95], n15(3), [0, -1.45, 0.66], lens=42), "samples": 16}
S["s05"] = {"mode": "cgi", "cars": [{"car": "mr2"}], "camera": cam([2.6, 4.6, 0.38], [2.3, 4.2, 0.95], n15(4), [0, 1.55, 0.55], lens=28), "samples": 16}
# s6 CGI NC -> 1:1 into s7
A, B = [-3.3, -4.3, 0.6], [-2.4, -3.2, 0.5]; T = [-0.35, -0.75, 0.42]
n6, n7 = n15(5), n15(6); u = (n6 - 1) / (n6 + n7 - 2)
S["s06"] = {"mode": "cgi", "cars": [{"car": "nc"}], "camera": cam(A, lerp(A, B, u), n6, T, lens=26), "samples": 16}
S["s07"] = {"mode": "scan", "cars": [{"car": "nc", "static": [f"{D}/nc_cut_fender.stl"]}], "camera": cam(lerp(A, B, u), B, n7, T, lens=26),
            "anim": [{"car": 0, "cut": f"{D}/nc_cut_bumper.stl", "off": [3, 12], "dir": [-0.2, -1, 0.5], "dist": 7,
                      "part": [f"{KN}/part_front_bumper.stl", f"{KN}/part_front_lip.stl", f"{KN}/part_canards.stl"], "on": [11, 26], "from": [0, -1.4, 0.3]}]}
S["s08"] = {"mode": "scan", "cars": [{"car": "nc", "static": [f"{KN}/part_front_bumper.stl", f"{KN}/part_front_lip.stl", f"{KN}/part_canards.stl"]}],
            "camera": cam([-2.5, -2.6, 1.0], [-2.6, -1.9, 1.0], n15(7), [-0.75, -0.95, 0.45], lens=34),
            "anim": [{"car": 0, "cut": f"{D}/nc_cut_fender.stl", "off": [3, 11], "dir": [-1, -0.2, 0.8], "dist": 7,
                      "part": [f"{KN}/part_fender_cuts.stl"], "on": [10, 23], "from": [-1.2, 0, 0.6]}]}
S["s09"] = {"mode": "cgi", "cars": [{"car": "nc"}], "camera": cam([-2.7, 1.3, 0.38], [-2.7, -0.3, 0.38], n15(8), [-0.8, 0.35, 0.3], [-0.8, -1.25, 0.3], lens=30), "samples": 16}
mr2s = {"car": "mr2", "offset": [1.1, 0.25, 0], "yaw": -14, "static": [f"{KM}/part_side_skirts.stl"]}
ncs = {"car": "nc", "offset": [-1.1, 0.25, 0], "yaw": 14, "static": [f"{KN}/part_front_bumper.stl", f"{KN}/part_front_lip.stl", f"{KN}/part_canards.stl", f"{KN}/part_fender_cuts.stl"]}
S["s10"] = {"mode": "scan", "cars": [mr2s, ncs], "camera": cam([0.5, -7.8, 2.8], [0.4, -7.2, 1.7], n15(9), [0, 0.1, 0.45], [0, 0.1, 0.55], lens=30)}
os.makedirs("specs", exist_ok=True)
for k, s in S.items():
    i = int(k[1:]) - 1
    s.update({"out": f"{M}/work/{k}", "frames": n15(i), "fps": 15, "res": [540, 960], "samples": s.get("samples", 12)})
    json.dump(s, open(f"specs/{k}.json", "w"), indent=1)
json.dump({"cuts": CUTS, "f30": F30}, open("specs/timeline.json", "w"))
print({k: s["frames"] for k, s in S.items()}, "total", sum(s["frames"] for s in S.values()))
