"""Registration check renders: each state scan in red over the silver full car, and the state scan alone, same camera.
   python projects/nissan-400z/tools/regcheck.py NAME AZ_DEG DIST HEIGHT TX,TY,TZ   -> check/reg_NAME.jpg
Uses projects/ferrari-296/tools/shot.py (keyed camera + colored parts)."""
import json, math, subprocess, sys
from PIL import Image
B = "/home/user/media/work/z400/blend"; C = "/home/user/media/work/z400/check"
n, az, r, h, tgt = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), [float(v) for v in sys.argv[5].split(",")]
a = math.radians(az)
cam = {"t": 0, "loc": [tgt[0] + r * math.sin(a), tgt[1] - r * math.cos(a), h], "target": tgt, "focal": 35}
ims = []
for tag, base, parts in (("ov", [f"{B}/car.blend"], [{"blend": f"{B}/{n}.blend", "color": "red"}]),
                         ("solo", [f"{B}/{n}.blend"], [])):
    s = {"base": base, "parts": parts, "camera": {"sensor": 20.25, "keys": [cam]}, "seconds": 0, "res": "1080x1920",
         "res_pct": 30, "samples": 8, "out": f"{C}/reg_{n}_{tag}.png"}
    json.dump(s, open(f"{C}/reg_{n}_{tag}.json", "w"))
    subprocess.run(["blender", "-b", "-P", "projects/ferrari-296/tools/shot.py", "--", f"{C}/reg_{n}_{tag}.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    ims.append(Image.open(f"{C}/reg_{n}_{tag}.png"))
w, hh = ims[0].size
s = Image.new("RGB", (w * 2, hh // 2))
for i, im in enumerate(ims):
    s.paste(im.crop((0, hh // 4, w, 3 * hh // 4)), (i * w, 0))
s.save(f"{C}/reg_{n}.jpg"); print(f"{C}/reg_{n}.jpg")
