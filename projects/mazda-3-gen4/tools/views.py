"""Quick orthographic-ish check stills of prepared blends (side/front/rear/top) via the shared shot renderer.
    python projects/mazda-3-gen4/tools/views.py out_dir base.blend [part.blend:color ...] [--res 25] [--views side,front,top]
Renders one 1-frame shot per view (long lens from far away) and tiles them into out_dir/views.jpg."""
import json, os, subprocess, sys
from PIL import Image
SHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shot.py")
VIEWS = {"side_l": ([0, 25, 0.7], [0, 0, 0.7]), "side_r": ([0, -25, 0.7], [0, 0, 0.7]),
         "front": ([25, 0, 0.8], [0, 0, 0.7]), "rear": ([-25, 0, 0.8], [0, 0, 0.7]),
         "top": ([0, 0.001, 25], [0, 0, 0]), "q34": ([14, -14, 7], [0, 0, 0.6])}
def main():
    a = sys.argv[1:]
    res = 25; views = ["side_r", "front", "rear", "top"]; focal = 120; ctr = [0, 0, 0]
    if "--res" in a: i = a.index("--res"); res = int(a[i + 1]); del a[i:i + 2]
    if "--views" in a: i = a.index("--views"); views = a[i + 1].split(","); del a[i:i + 2]
    if "--focal" in a: i = a.index("--focal"); focal = float(a[i + 1]); del a[i:i + 2]
    if "--center" in a: i = a.index("--center"); ctr = [float(v) for v in a[i + 1].split(",")]; del a[i:i + 2]
    out, base, parts = a[0], a[1], a[2:]
    os.makedirs(out, exist_ok=True)
    tiles = []
    for v in views:
        loc, tgt = VIEWS[v]
        loc = [l + c for l, c in zip(loc, ctr)]; tgt = [l + c for l, c in zip(tgt, ctr)]
        sp = {"base": [base], "parts": [{"blend": p.split(":")[0], "color": p.split(":")[1]} if ":" in p else {"blend": p} for p in parts],
              "camera": {"keys": [{"t": 0, "loc": loc, "target": tgt, "focal": focal}]},
              "seconds": 0, "fps": 15, "res": "1080x1920" if v not in ("side_l", "side_r", "top") else "1920x1080",
              "res_pct": res, "samples": 6, "out": f"{out}/{v}.png"}
        if v == "top": sp["res"] = "1080x1920"
        p = f"{out}/{v}.json"; json.dump(sp, open(p, "w"))
        subprocess.run(["blender", "-b", "-P", SHOT, "--", p], check=True, stdout=subprocess.DEVNULL)
        tiles.append(Image.open(f"{out}/{v}.png").convert("RGB"))
    h = 600
    tiles = [t.resize((int(t.width * h / t.height), h)) for t in tiles]
    W = sum(t.width for t in tiles); im = Image.new("RGB", (W, h)); x = 0
    for t in tiles: im.paste(t, (x, 0)); x += t.width
    im.save(f"{out}/views.jpg", quality=88); print(f"{out}/views.jpg")
main()
