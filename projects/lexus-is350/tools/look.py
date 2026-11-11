"""Quick stills of a set of prepped blends: look.py out_dir name base.blend[,part.blend:color] view [view ...]
views: f34 r34 side top front rear or 'cam:x,y,z:tx,ty,tz:focal'. Writes a shot.py spec per view and renders at 30 %."""
import json, os, subprocess, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SHOT = f"{REPO}/projects/ferrari-296/tools/shot.py"
V = {"f34": ([-3.6, -4.6, 1.3], [0, -0.3, 0.6], 30), "r34": ([3.6, 4.6, 1.4], [0, 0.3, 0.6], 30),
     "side": ([-6.5, 0, 1.0], [0, 0, 0.6], 30), "top": ([0, 0.01, 8.5], [0, 0, 0.5], 30),
     "front": ([0, -6.5, 1.0], [0, 0, 0.6], 30), "rear": ([0, 6.5, 1.0], [0, 0, 0.6], 30),
     "fnose": ([-1.6, -4.3, 1.4], [0, -1.9, 0.6], 30)}
out, name, objs = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
pct = int(os.environ.get("PCT", 30))
base = [o for o in objs if ":" not in o]
parts = [{"blend": o.split(":")[0], "color": o.split(":")[1]} for o in objs if ":" in o]
os.makedirs(out, exist_ok=True)
for vi, v in enumerate(sys.argv[4:]):
    if v.startswith("cam:"):
        _, l, t, f = v.split(":"); loc = [float(x) for x in l.split(",")]; tgt = [float(x) for x in t.split(",")]; foc = float(f); tag = f"cam{vi}"
    else:
        (loc, tgt, foc), tag = V[v], v
    sp = {"base": base, "parts": parts, "camera": {"sensor": 20.25, "keys": [{"t": 0, "loc": loc, "target": tgt, "focal": foc}]},
          "seconds": 0, "fps": 15, "res": "1080x1920", "res_pct": pct, "samples": 8, "out": f"{out}/{name}_{tag}.png"}
    js = f"{out}/{name}_{tag}.json"; json.dump(sp, open(js, "w"))
    r = subprocess.run(["blender", "-b", "-P", SHOT, "--", js], capture_output=True, text=True)
    print(sp["out"] if "IVE_RENDER_DONE" in r.stdout else r.stdout[-1500:] + r.stderr[-1500:])
