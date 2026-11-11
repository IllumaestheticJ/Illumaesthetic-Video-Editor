"""Contact strip of a final v2 shot with its label overlay composited: labsheet.py shot out.png [n]"""
import json, os, subprocess, sys
from PIL import Image
s, out = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
d = f"/home/user/media/work/frontier/renders/final/{s}"; fs = sorted(os.listdir(d))
nf = json.load(open(os.path.join(os.path.dirname(__file__), "..", os.environ.get("TIMING", "timing_v2.json"))))["frames"][s]
mov = f"/home/user/media/work/frontier/out/labels_{s}.mov"
tiles = []
for k in range(n):
    f = fs[round(k * (len(fs) - 1) / (n - 1))]; fi = int(f[2:6])
    b = Image.open(f"{d}/{f}").convert("RGBA").resize((1080, 1920))
    if os.path.exists(mov):
        i = min(nf - 1, int(round((fi - 1) / 15 * 30)))
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mov, "-vf", f"select=eq(n\\,{i})", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True).stdout
        b.alpha_composite(Image.frombytes("RGBA", (1080, 1920), raw))
    tiles.append(b.convert("RGB").resize((270, 480)))
c = Image.new("RGB", (270 * n, 480))
for k, t in enumerate(tiles): c.paste(t, (k * 270, 0))
c.save(out); print(out)
