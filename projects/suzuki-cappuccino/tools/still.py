"""Quick look / framing still via tools/shot.py.
  still.py out.png 'name=path.blend,...' az el dist tx,ty,tz lens [res_pct] [samples]"""
import json, os, subprocess, sys, tempfile, shutil
out, objs, az, el, dist, tgt, lens = sys.argv[1:8]
pct = sys.argv[8] if len(sys.argv) > 8 else "30"; spp = sys.argv[9] if len(sys.argv) > 9 else "8"
o = dict(kv.split("=") for kv in objs.split(","))
d = tempfile.mkdtemp()
spec = dict(objects=o, seconds=0.0667, fps=15, res=[1080, 1920], out=d, exposure=-0.5,
            camera=[dict(t=0, az=float(az), el=float(el), dist=float(dist), target=[float(v) for v in tgt.split(",")], lens=float(lens))])
json.dump(spec, open(d + "/s.json", "w"))
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run(["blender", "-b", "-P", here + "/shot.py", "--", d + "/s.json", "--res-pct", pct, "--samples", spp, "--frames", "1"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
shutil.move(d + "/f_0001.png", out); print(out)
