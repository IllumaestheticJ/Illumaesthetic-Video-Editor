"""First / middle / last frame of every prepped shot (rule A), 8 shots per sheet -> OUT/contact_N.jpg
usage: contact.py [dir_with_S*.mp4] [out_prefix]"""
import subprocess, sys, json, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
from edit_shots import SHOTS
src = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/smart-450/build")
pre = sys.argv[2] if len(sys.argv) > 2 else "/home/user/media/work/smart-450/out/contact_shots"
TW, TH = 216, 384
def frame(f, i):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-vf", f"select=eq(n\\,{i}),scale={TW}:{TH}", "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return Image.frombytes("RGB", (TW, TH), r.stdout) if len(r.stdout) == TW * TH * 3 else Image.new("RGB", (TW, TH), (80, 0, 0))
for part in range(0, len(SHOTS), 8):
    group = SHOTS[part:part + 8]
    sheet = Image.new("RGB", (TW * 6 + 5 * 4 + 10, (TH + 22) * 4), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for k, s in enumerate(group):
        col, row = k % 2, k // 2
        for j, i in enumerate((0, s["n"] // 2, s["n"] - 1)):
            x = 5 + col * (3 * TW + 20) + j * TW; y = row * (TH + 22) + 20
            sheet.paste(frame(src / f"{s['id']}.mp4", i), (x, y))
        d.text((5 + col * (3 * TW + 20), row * (TH + 22) + 4), f"{s['id']} f{s['start']} n{s['n']}  {s.get('src') or s.get('scan') or s.get('img') or ''}", fill=(255, 255, 255))
    out = f"{pre}_{part // 8 + 1}.jpg"
    sheet.save(out, quality=88); print(out)
