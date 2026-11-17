"""Assemble BF5 v0: shot PNG sequences (rendered every 2nd frame) -> 30 fps 1080x1920, overlays, music.

Cuts land on the track's bar kicks (measured: 2.56 / 5.00 / 7.44 / 9.88 / 12.32 s).
Overlays are PIL PNGs (stand-in for the Remotion layer in v0); all text comes from store_snapshot.json.
"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont

P = "/home/user/Illumaesthetic-Video-Editor/projects/bf-clearance-shelf-drop"
M = "/home/user/media/bf-clearance-shelf-drop"
R = f"{M}/renders_v03"
W = f"{M}/work_v0"
OUT = "/home/user/media/work/out/bf-clearance-shelf-drop_v0.3.mp4"
os.makedirs(W, exist_ok=True); os.makedirs(os.path.dirname(OUT), exist_ok=True)
snap = json.load(open(f"{P}/store_snapshot.json"))
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FM = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
OFF = (232, 236, 242)

SHOTS = [("s1", 77), ("s2", 73), ("s3", 73), ("s4", 73), ("s5", 74)]
END_FR = 80                     # end card 12.33-15.0 s
TOTAL = sum(n for _, n in SHOTS) + END_FR


def run(cmd):
    print(" ".join(cmd)[:200]); subprocess.run(cmd, check=True)


# ---- overlays
def text_png(path, lines, y0, size=64, font=FB, spacing=1.25, align="center"):
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = y0
    for t, sz, f in lines:
        fnt = ImageFont.truetype(f, sz)
        d.text((540, y), t, font=fnt, fill=(*OFF, 255), anchor="mt")
        y += int(sz * spacing)
    im.save(path)


def placeholder_png(path):
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FM, 26)
    d.text((80, 1920 - 120), "v0 DRAFT - placeholder characters (model-sheet cutouts)", font=f, fill=(255, 255, 255, 150))
    im.save(path)


def endcard(path):
    im = Image.new("RGB", (1080, 1920), (1, 1, 1))
    logo = Image.open(f"{M}/logo/Epsilon+ Logo.png").convert("RGBA")
    w = 720; h = int(logo.height * w / logo.width)
    logo = logo.resize((w, h), Image.LANCZOS)
    im.paste(logo, ((1080 - w) // 2, 820 - h // 2), logo)
    d = ImageDraw.Draw(im)
    d.text((540, 960), "BLACK FRIDAY CLEARANCE", font=ImageFont.truetype(FB, 54), fill=OFF, anchor="mt")
    d.text((540, 1040), "EPSILON.PLUS", font=ImageFont.truetype(FM, 46), fill=OFF, anchor="mt")
    im.save(path)


count = snap["tags"]["grv1"]["stock_line"]
text_png(f"{W}/count.png", [(count, 66, FB)], 330)   # safe zones: text inside y 285-1440
placeholder_png(f"{W}/placeholder.png")
endcard(f"{W}/endcard.png")

# ---- per-shot clips (15 fps renders -> 30 fps by frame doubling, exact frame counts)
clips = []
for s, n in SHOTS:
    c = f"{W}/{s}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-framerate", "15", "-pattern_type", "glob", "-i", f"{R}/{s}/f_*.png",
         "-vf", "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p", "-frames:v", str(n),
         "-c:v", "libx264", "-crf", "16", "-preset", "fast", c])
    clips.append(c)
c = f"{W}/end.mp4"
run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-i", f"{W}/endcard.png",
     "-vf", "format=yuv420p", "-frames:v", str(END_FR), "-c:v", "libx264", "-crf", "16", "-preset", "fast", c])
clips.append(c)
with open(f"{W}/list.txt", "w") as f:
    f.writelines(f"file '{x}'\n" for x in clips)
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{W}/list.txt", "-c", "copy", f"{W}/cut.mp4"])

# ---- overlays + music
s5_start = (77 + 73 * 3) / 30          # 9.867 s
t_count0, t_count1 = 10.45, 12.20      # count enters on the snare, leaves before the end-card cut
end_start = sum(n for _, n in SHOTS) / 30
fc = (f"[0:v][3:v]overlay=0:0:enable='between(t,{t_count0},{t_count1})'[v]")
dur = TOTAL / 30
run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/cut.mp4", "-i", f"{M}/music/luxury.wav",
     "-loop", "1", "-i", f"{W}/placeholder.png", "-loop", "1", "-i", f"{W}/count.png",
     "-filter_complex", fc + f";[1:a]atrim=0:{dur:.3f},afade=t=out:st={dur-0.6:.3f}:d=0.6,"
     "loudnorm=I=-14:TP=-1.5:LRA=11[aud]",
     "-map", "[v]", "-map", "[aud]", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "slow",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", OUT])
print("OUT", OUT, "frames", TOTAL, "dur", dur)
