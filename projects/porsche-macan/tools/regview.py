"""Registration check render: parts in colour over the grey full car, 4 fixed views in one Blender run.

    python projects/porsche-macan/tools/regview.py out_dir base.blend part1.blend[:color] ... [--views fl,fr,rl,top]

Frame convention (prepped, m): front = -Y, car's right = -X, ground Z=0. Writes a spec for tools/shot.py
with fps=1 and one camera key per view, renders frames 1..N at 30 % res, then tiles them into sheet.jpg.
"""
import json, math, os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
VIEWS = {  # camera loc, target
    "fl": ([3.6, -5.2, 2.0], [0, -0.3, 0.7]), "fr": ([-3.6, -5.2, 2.0], [0, -0.3, 0.7]),
    "rl": ([3.6, 5.2, 2.0], [0, 0.3, 0.7]), "rr": ([-3.6, 5.2, 2.0], [0, 0.3, 0.7]),
    "top": ([0.01, 0.0, 9.0], [0, 0, 0.6]), "left": ([6.5, 0, 1.0], [0, 0, 0.8]), "right": ([-6.5, 0, 1.0], [0, 0, 0.8]),
    "lclose": ([3.6, 0, 0.9], [0, 0, 0.8]), "rclose": ([-3.6, 0, 0.9], [0, 0, 0.8]),
    "front": ([0, -7.5, 1.2], [0, 0, 0.8]), "rear": ([0, 7.5, 1.2], [0, 0, 0.8]),
}
COLS = ["red", "cyan", "green", "yellow", "magenta"]


def main():
    a = sys.argv[1:]
    views = "fl,fr,rl,top".split(",")
    if "--views" in a:
        i = a.index("--views"); views = a[i + 1].split(","); del a[i:i + 2]
    out, base, parts = a[0], a[1], a[2:]
    os.makedirs(out, exist_ok=True)
    ps = []
    for k, p in enumerate(parts):
        b, _, c = p.partition(":")
        ps.append({"blend": b, "color": c or COLS[k % len(COLS)]})
    keys = [{"t": float(i), "loc": VIEWS[v][0], "target": VIEWS[v][1], "focal": 28, "ease": "lin"} for i, v in enumerate(views)]
    spec = {"base": [base], "parts": ps, "camera": {"sensor": 20.25, "keys": keys}, "seconds": len(views), "fps": 1,
            "res": "1080x1920", "res_pct": 30, "samples": 8, "base_color": "grey", "out": out,
            "frames": list(range(1, len(views) + 1))}
    sp = os.path.join(out, "spec.json"); json.dump(spec, open(sp, "w"), indent=1)
    subprocess.run(["blender", "-b", "-P", os.path.join(HERE, "shot.py"), "--", sp], check=True, stdout=subprocess.DEVNULL)
    ims = [Image.open(os.path.join(out, f"f_{i:04d}.png")) for i in range(1, len(views) + 1)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w * len(ims), h))
    for i, im in enumerate(ims):
        sheet.paste(im.convert("RGB"), (i * w, 0))
    sheet.save(os.path.join(out, "sheet.jpg"), quality=88)
    print(os.path.join(out, "sheet.jpg"))


if __name__ == "__main__":
    main()
