"""v6 (user: "Rear trunk area is not cut correctly based on real trunk opening"): every shot that shows the trunk lid or the
opening it leaves is re-rendered on the v6 geometry - base comp_explode6 (tools/build_v6.py) and lid_v6 (tools/lid_v6.py).
Copies the existing v4/v5 specs, swapping only those two files; v4 shots are shortened to one bar (59 frames + 3).
Writes shots/<name>6.json (and <name>6_pv.json previews: 30 %, 8 spp, first/mid/last + extra frames).
  python projects/toyota-gr86/tools/respec_v6.py"""
import json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shots")
SHOTS = {"e1_lid_hinge": (0.45,), "e2_lid_off_cargo": (0.35, 1.2), "e3_rear_bumper_off": (), "e4_rear_beam": (),
         "f1_reverse_light": (), "x1_explode_fr": (0.30,), "x2_explode_rr": (), "x3_explode_high": (), "h1_reassemble_v5": (1.30,)}
for name, extra in SHOTS.items():
    s = json.load(open(os.path.join(D, name + ".json")))
    s["base"] = [b.replace("comp_explode4.blend", "comp_explode6.blend") for b in s["base"]]
    for p in s["parts"]:
        p["blend"] = p["blend"].replace("/lid_v4.blend", "/lid_v6.blend")
    if s["fps"] == 30:
        s["seconds"] = round(59 / 30 + 0.1, 4)
    s["out"] = s["out"].rstrip("/") + "6"
    json.dump(s, open(os.path.join(D, name + "6.json"), "w"), indent=1)
    pv = dict(s, res_pct=30, samples=8, out=s["out"].replace("/shots/", "/preview/"),
              frames=["first", "mid", "last", *[max(1, round(t * s["fps"])) for t in extra]])
    json.dump(pv, open(os.path.join(D, name + "6_pv.json"), "w"), indent=1)
    print(name + "6", s["seconds"], "s", s["fps"], "fps")
