"""Quick still: python quick.py out.png "camx,camy,camz" "tx,ty,tz" base.blend[,..] [red.blend[,..]] [--grey] [--pct 30]
(prep any STL first; red parts drawn in the check colour)."""
import json, subprocess, sys, os
a = sys.argv[1:]; grey = "--grey" in a; a = [x for x in a if x != "--grey"]
pct = 30
if "--pct" in a: i = a.index("--pct"); pct = int(a[i + 1]); del a[i:i + 2]
out, cam, tgt, base = a[:4]; red = a[4].split(",") if len(a) > 4 and a[4] else []
s = {"base": base.split(","), "base_color": "grey" if grey else "silver",
     "parts": [{"blend": r, "color": "red"} for r in red],
     "camera": {"keys": [{"t": 0, "loc": [float(v) for v in cam.split(",")], "target": [float(v) for v in tgt.split(",")], "focal": 28}]},
     "seconds": 0, "res": "1080x1920", "res_pct": pct, "samples": 8, "out": out}
j = out[:-4] + ".json"; json.dump(s, open(j, "w"))
subprocess.run(["blender", "-b", "-P", os.path.join(os.path.dirname(os.path.abspath(__file__)), "shot.py"), "--", j], capture_output=True)
print(out, os.path.exists(out))
