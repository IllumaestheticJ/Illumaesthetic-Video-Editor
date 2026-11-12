"""Quick check still via projects/subaru-gd-trio/tools/shot.py (house look; colored parts for registration checks).
    python still.py out.png --base a.blend [b.blend] --part x.blend:red --part y.blend:cyan --cam "x,y,z" --tgt "x,y,z" [--focal 35] [--pct 30] [--spp 8]
"""
import argparse, json, subprocess, os, tempfile
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--base", nargs="+", default=[])
ap.add_argument("--part", action="append", default=[]); ap.add_argument("--cam", required=True); ap.add_argument("--tgt", required=True)
ap.add_argument("--focal", type=float, default=35); ap.add_argument("--pct", type=int, default=30); ap.add_argument("--spp", type=int, default=8)
a = ap.parse_args()
f3 = lambda s: [float(v) for v in s.split(",")]
spec = {"base": a.base, "parts": [{"blend": p.split(":")[0], **({"color": p.split(":")[1]} if ":" in p else {})} for p in a.part],
        "camera": {"keys": [{"t": 0, "loc": f3(a.cam), "target": f3(a.tgt), "focal": a.focal}]},
        "seconds": 0, "fps": 15, "res_pct": a.pct, "samples": a.spp, "out": os.path.abspath(a.out)}
fd, sp = tempfile.mkstemp(suffix=".json"); json.dump(spec, open(sp, "w"))
r = subprocess.run(["blender", "-b", "-P", "projects/subaru-gd-trio/tools/shot.py", "--", sp], capture_output=True, text=True)
print(r.stdout[-300:] if "IVE_RENDER_DONE" in r.stdout else r.stdout[-2000:] + r.stderr[-2000:])
