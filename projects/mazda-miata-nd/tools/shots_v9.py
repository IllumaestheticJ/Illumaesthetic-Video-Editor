"""v9 shot specs (user v8: "the rear trunk is not cut right"): lid = what MOVED in the trunk-open scan incl. its wrapped rear face (tools/lid_from_state.py + fill_panel_holes.py), comps rebuilt (comp_rear_v9, comp_explode_v9). Was: v7 shot specs: the v5/v6 trunk-lid shots re-pointed at the refined lid (x_trunk_v6: tail-light pieces that stay on the body
in the trunk-open state scan removed, tools/refine_lid.py) and the rebuilt composites (comp_rear_v6, comp_explode_v6 with a
6 mm cut around the lid). Same cameras/timing as shots_v5 (B 0.46864).
    python projects/mazda-miata-nd/tools/shots_v7.py preview|final [shot ...]"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("shots_v5", os.path.join(HERE, "shots_v5.py"))
v5 = importlib.util.module_from_spec(sp); _a = sys.argv; sys.argv = [_a[0]]; sp.loader.exec_module(v5); sys.argv = _a
SWAP = {"x_trunk": "x_trunk_v9", "comp_rear": "comp_rear_v9", "comp_explode_v5": "comp_explode_v9"}
v5.OUT = f"{v5.W}/renders_v9"
for name in ("v3_r_trunk", "v3_x_front", "v3_x_rear", "v3_x_home"):
    s = v5.SHOTS[name]
    s["base"] = [SWAP.get(b, b) for b in s["base"]]
    for p in s["parts"]:
        stem = os.path.basename(p["blend"])[:-6]
        p["blend"] = f"{v5.P}/{SWAP.get(stem, stem)}.blend"
v5.SHOTS["v3_r_trunk"]["N"] = 30            # slot 56 frames at B 0.46864 (v3 render was 116 BPM)
v5.SHOTS["v3_r_trunk"]["cam"] = [v5.cam(0, [-2.25, 1.00, 2.95], [-0.35, 1.40, 0.70], 30), v5.cam(4, [-1.75, 1.25, 2.60], [-0.35, 1.45, 0.66], 30)]
v5.SHOTS["v3_r_trunk"]["parts"][0]["keys"] = [v5.k(0), v5.k(0.5), v5.k(2.5, rot=(v5.TRUNK_OPEN, 0, 0)), v5.k(4, rot=(v5.TRUNK_OPEN, 0, 0))]
if __name__ == "__main__" and False:
    mode = sys.argv[1]
    for n in sys.argv[2:]:
        print(v5.spec(n, mode))

# v10 (user: "27/28 has a weird cut in it"): the x_rear -> x_home cut was a jump cut (x_home started ~2 deg / 1.3 m away from
# where x_rear ended, same subject). x_home now starts EXACTLY on x_rear's end camera (r 6.6, az 226, h 4.1, target (0,0.7,1.15),
# 30 mm) and eases to the listing camera, so the two read as one continuous move.
import math as _m
def _home_cam(secs, n=8):
    L = v5.LIST
    a0 = dict(r=6.6, a=226.0, h=4.1, c=(0, 0.7, 1.15), tz=1.15, f=30.0)
    a1 = dict(r=L["r_h"], a=L["a"], h=L["h"], c=(0, 0, 0.55), tz=0.55, f=L["focal_render"])
    ks = []
    for i in range(n + 1):
        u = i / n; e = u * u * (3 - 2 * u)
        mix = lambda p, q: p + (q - p) * e
        r, a, h, f = mix(a0["r"], a1["r"]), _m.radians(mix(a0["a"], a1["a"])), mix(a0["h"], a1["h"]), mix(a0["f"], a1["f"])
        c = [mix(p, q) for p, q in zip(a0["c"], a1["c"])]
        ks.append({"t": secs * u, "loc": [c[0] + r * _m.sin(a), c[1] - r * _m.cos(a), h], "target": [c[0], c[1], mix(a0["tz"], a1["tz"])],
                   "focal": f, "ease": "lin"})
    return ks
_HC = _home_cam(56 / 30)
v5.SHOTS["v3_x_home"]["cam"] = _HC
v5.SHOTS["v3_x_home_clean"]["cam"] = _HC
v5.OUT = f"{v5.W}/renders_v10"

if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:]:
        print(v5.spec(n, mode))
