"""Registration check renders: part (red) over the full car (silver), from two cameras, 30 % res.
    python regcheck.py <part> "<cx,cy,cz>" "<cam1 x,y,z>" "<cam2 x,y,z>" [focal]   -> /home/user/media/work/miata/regcheck/<part>.jpg
Uses projects/ferrari-296/tools/shot.py (keyed cameras, coloured parts)."""
import json, subprocess, sys, os
from PIL import Image
P = "/home/user/media/mazda-miata-na/prep"; R = "/home/user/media/work/miata/regcheck"; os.makedirs(R, exist_ok=True)
part, c, a, b = sys.argv[1:5]; f = float(sys.argv[5]) if len(sys.argv) > 5 else 30
V = lambda s: [float(x) for x in s.split(",")]
ims = []
for k, cam in enumerate((a, b)):
    for solo in (False, True):
        spec = {"base": [] if solo else [f"{P}/car4.blend"], "parts": [{"blend": f"{P}/{part}.blend", "color": None if solo else "red"}],
                "camera": {"sensor": 20.25, "keys": [{"t": 0, "loc": V(cam), "target": V(c), "focal": f}]},
                "seconds": 0, "fps": 15, "res": "1080x1920", "res_pct": 30, "samples": 8, "out": f"{R}/{part}_{k}{'s' if solo else ''}.png"}
        if solo:
            spec["base"] = [f"{P}/{part}.blend"]; spec["parts"] = []
        js = f"{R}/{part}_{k}{solo}.json"; json.dump(spec, open(js, "w"))
        subprocess.run(["blender", "-b", "-P", "projects/ferrari-296/tools/shot.py", "--", js], check=True, capture_output=True)
        ims.append(Image.open(spec["out"]))
w, h = ims[0].size; s = Image.new("RGB", (w * 4, h))
for i, im in enumerate(ims): s.paste(im, (i * w, 0))
s.save(f"{R}/{part}.jpg"); print(f"{R}/{part}.jpg")
