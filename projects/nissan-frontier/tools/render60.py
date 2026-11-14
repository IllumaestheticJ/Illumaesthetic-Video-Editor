"""60 fps raw renders (user: "render this in 60fps, raw"): no interpolation, every frame rendered at 60 fps.
Takes the final spec of a shot (same keys, which are in seconds, so motion and cut timing are unchanged), sets fps=60, writes it to
renders/final60/<shot>, and lists only the frames still missing (resumable).
  python render60.py <shot>   -> prints the spec path (empty line when the shot is complete)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
R = "/home/user/media/work/frontier/renders/final60"; SPECS = "/home/user/media/nissan-frontier/specs"
# the opening scan shots are used only for their first 2.4 s after a trim (timeline trim_start), so only those frames are needed
NEED_OPEN = {"v2_s1_wide": 204, "v2_s2_grille": 288, "v4_s3_bumper": 144}
name = sys.argv[1]
if name.startswith("m"):
    import shots_v11
    sp_path = shots_v11.spec(name, "final")
else:
    sp_path = f"{SPECS}/{name}_final.json"
sp = json.load(open(sp_path))
sp["fps"] = 60; sp["out"] = f"{R}/{name}"; sp["anchors_out"] = f"{SPECS}/{name}_60_anchors.json"
sp["res_pct"] = 75; sp["samples"] = 12
n = NEED_OPEN.get(name, int(round(sp["seconds"] * 60)))
os.makedirs(sp["out"], exist_ok=True)
missing = [f for f in range(1, n + 1) if not (os.path.exists(f"{sp['out']}/f_{f:04d}.png") and os.path.getsize(f"{sp['out']}/f_{f:04d}.png") > 1000)]
if not missing:
    print(""); sys.exit(0)
sp["frames"] = missing
out = f"{SPECS}/{name}_60.json"; json.dump(sp, open(out, "w"), indent=1)
print(out)
