"""Render the SEMA build (car + all CAD) from a camera and onion it over the IRL cut frame.
onion.py loc_x,y,z target_x,y,z focal out.png [roll]"""
import json, subprocess, sys, glob
from PIL import Image, ImageChops
W = '/home/user/media/work/sentra'
loc = [float(v) for v in sys.argv[1].split(',')]; tgt = [float(v) for v in sys.argv[2].split(',')]; f = float(sys.argv[3]); out = sys.argv[4]
roll = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
cads = sorted(glob.glob(W + '/cad/Uncut_*.blend'))
spec = {"base": [W + '/car_nobump.blend'], "parts": [{"blend": c, "color": "red"} for c in cads],
        "camera": {"keys": [{"t": 0, "loc": loc, "target": tgt, "focal": f, "roll": roll}]}, "seconds": 0.0667, "fps": 15,
        "res_pct": 50, "samples": 6, "persistent": False, "exposure": -0.8, "out": W + '/match/onion_r.png'}
json.dump(spec, open(W + '/match/onion.json', 'w'))
subprocess.run(['blender', '-b', '-P', '/home/user/Illumaesthetic-Video-Editor/projects/nissan-sentra-promo/tools/shot.py', '--', W + '/match/onion.json'], capture_output=True)
r = Image.open(W + '/match/onion_r.png').convert('RGB').resize((540, 960)); p = Image.open(W + '/match/cut.png').convert('RGB').resize((540, 960))
on = Image.blend(p, r, 0.5)
c = Image.new('RGB', (1080, 960)); c.paste(on, (0, 0)); c.paste(r, (540, 0)); c.save(out); print(out)
