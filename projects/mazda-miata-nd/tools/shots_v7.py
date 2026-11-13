"""v7 shot specs: the v5/v6 trunk-lid shots re-pointed at the refined lid (x_trunk_v6: tail-light pieces that stay on the body
in the trunk-open state scan removed, tools/refine_lid.py) and the rebuilt composites (comp_rear_v6, comp_explode_v6 with a
6 mm cut around the lid). Same cameras/timing as shots_v5 (B 0.46864).
    python projects/mazda-miata-nd/tools/shots_v7.py preview|final [shot ...]"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("shots_v5", os.path.join(HERE, "shots_v5.py"))
v5 = importlib.util.module_from_spec(sp); _a = sys.argv; sys.argv = [_a[0]]; sp.loader.exec_module(v5); sys.argv = _a
SWAP = {"x_trunk": "x_trunk_v6", "comp_rear": "comp_rear_v6", "comp_explode_v5": "comp_explode_v6"}
v5.OUT = f"{v5.W}/renders_v7"
for name in ("v3_r_trunk", "v3_x_front", "v3_x_rear", "v3_x_home"):
    s = v5.SHOTS[name]
    s["base"] = [SWAP.get(b, b) for b in s["base"]]
    for p in s["parts"]:
        stem = os.path.basename(p["blend"])[:-6]
        p["blend"] = f"{v5.P}/{SWAP.get(stem, stem)}.blend"
v5.SHOTS["v3_r_trunk"]["N"] = 30            # slot 56 frames at B 0.46864 (v3 render was 116 BPM)
v5.SHOTS["v3_r_trunk"]["cam"] = [v5.cam(0, [-2.25, 1.00, 2.95], [-0.35, 1.40, 0.70], 30), v5.cam(4, [-1.75, 1.25, 2.60], [-0.35, 1.45, 0.66], 30)]
v5.SHOTS["v3_r_trunk"]["parts"][0]["keys"] = [v5.k(0), v5.k(0.5), v5.k(2.5, rot=(v5.TRUNK_OPEN, 0, 0)), v5.k(4, rot=(v5.TRUNK_OPEN, 0, 0))]
if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:]:
        print(v5.spec(n, mode))
