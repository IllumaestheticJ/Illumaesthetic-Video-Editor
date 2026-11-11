"""Quick check still via tools/shot.py.
  still.py out.png --base a.blend b.blend --parts red:x.blend cyan:y.blend --loc x,y,z --target x,y,z [--focal 30] [--pct 30] [--spp 8]"""
import argparse, json, subprocess, os
ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--base", nargs="+", default=[]); ap.add_argument("--parts", nargs="*", default=[])
ap.add_argument("--loc", required=True); ap.add_argument("--target", required=True); ap.add_argument("--focal", type=float, default=30)
ap.add_argument("--pct", type=int, default=30); ap.add_argument("--spp", type=int, default=8); ap.add_argument("--grey", action="store_true")
a = ap.parse_args()
f = lambda s: [float(v) for v in s.split(",")]
parts = []
for p in a.parts:
    col, b = p.split(":", 1) if ":" in p else (None, p)
    parts.append({"blend": b, **({"color": col} if col else {})})
sp = {"base": a.base, "parts": parts, "camera": {"sensor": 20.25, "keys": [{"t": 0, "loc": f(a.loc), "target": f(a.target), "focal": a.focal}]},
      "seconds": 0, "fps": 15, "res": "1080x1920", "res_pct": a.pct, "samples": a.spp, "out": os.path.abspath(a.out)}
if a.grey: sp["base_color"] = "grey"
js = "/home/user/media/nissan-frontier/specs/_still.json"; json.dump(sp, open(js, "w"))
r = subprocess.run(["blender", "-b", "-P", os.path.join(os.path.dirname(__file__), "shot.py"), "--", js], capture_output=True, text=True)
print([l for l in r.stdout.splitlines() if "IVE_RENDER_DONE" in l or "Error" in l][-3:], r.returncode)
