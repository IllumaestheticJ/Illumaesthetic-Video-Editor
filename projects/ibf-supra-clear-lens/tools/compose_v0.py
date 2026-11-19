"""R1 ibf-supra-clear-lens v0: quick first draft (about 19 s, 1080x1920, 30 fps).

Real footage only (Dropbox "Supra Tail Light Footage", Jul 7 + Jul 13 2026), music "Vanity" - Billy Ghost
(TikTok CML 7571577919118624784) from 20.712 s so its drop (23.661 s) lands on the frame the bench
lenses light up. Every cut sits on the beat grid (80.7 BPM, 0.743 s) after the drop.

    python projects/ibf-supra-clear-lens/tools/compose_v0.py [out.mp4]
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC = "/home/user/media/ibf-supra-clear-lens/dropbox"
WORK = "/home/user/media/work/ibf-supra/v0"
MUSIC = "/home/user/media/work/music/ibf-supra/vanity.mp3"
LOGO = "/home/user/media/work/ibf-supra/illum_logo.png"
AKIRA = f"{ROOT}/assets/fonts/akira/AkiraExpanded-SuperBold.otf"
UNB = f"{ROOT}/assets/fonts/unbounded/Unbounded-%d.ttf"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/ibf-supra-clear-lens_v0.mp4"
FPS, W, H = 30, 1080, 1920
MUSIC_T0 = 20.712
TONEMAP = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")

LIGHT_ON = 2.234  # j07_1634: first frame with the lenses lit (measured, red-minus-green in the lens band)
# (name, src, src_in, frames, speed, why)
SEGS = [
    ("A_bench_off", "j07_1634.mov", 0.0, 89, LIGHT_ON / (89 / FPS), "tinted lenses unlit on the bench, slowed so the light-on hits the drop and the price reads"),
    ("B_bench_on",  "j07_1634.mov", LIGHT_ON, 89, 1.0, "both lenses light on the drop"),
    ("C_close",     "j07_1635.mov", 1.10, 67, 1.0, "close-up, hearts light then sweep"),
    ("D_on_car",    "j07_1613.mov", 1.60, 66, 1.0, "fitted on the car in the shop, blinking"),
    ("E_road",      "j13_1940.mov", 8.00, 90, 1.0, "rolling 3/4 rear at 7:40 PM, hearts lit"),
    ("F_close_amb", "j13_1944.mov", 38.70, 66, 1.0, "close rear, amber signal"),
]
END_FRAMES = 112  # end card, 3.73 s (5 beats)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(d, y, text, f, fill=(255, 255, 255, 255), shadow=True):
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f)
    x = (W - (x1 - x0)) // 2 - x0
    if shadow:
        for dx, dy in ((0, 4), (2, 5), (-2, 5)):
            d.text((x + dx, y + dy), text, font=f, fill=(0, 0, 0, 150))
    d.text((x, y), text, font=f, fill=fill)
    return [x + x0, y + y0, x1 - x0, y1 - y0]


def strike(d, box, color=(225, 30, 40, 255), width=8):
    x, y, w, h = box
    d.line([(x - 8, y + h // 2), (x + w + 8, y + h // 2)], fill=color, width=width)


def make_text():
    boxes = []
    # opening price card over the bench shot (owner OK: price over IRL in these reels)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    b1 = centered(d, 430, "BLACK FRIDAY", font(AKIRA, 62))
    b2 = centered(d, 530, "$72", font(AKIRA, 230))
    b3 = centered(d, 820, "WAS $200", font(AKIRA, 64)); strike(d, b3)
    im.save(f"{WORK}/txt_open.png")
    t0, t1 = 4 / FPS, 140 / FPS
    for lab, b in (("BLACK FRIDAY", b1), ("$72", b2), ("WAS $200", b3)):
        boxes.append({"t0": t0, "t1": t1, "x": b[0], "y": b[1], "w": b[2], "h": b[3], "label": lab, "key": True})

    # end card on black
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    logo = Image.open(LOGO).convert("RGBA"); lw = 650; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    ly = 380; im.alpha_composite(logo, ((W - lw) // 2, ly)); lb = [(W - lw) // 2, ly, lw, logo.height]
    bu = centered(d, ly + logo.height + 40, "WWW.ILLUMAESTHETIC.COM", font(UNB % 400, 38), shadow=False)
    e1 = centered(d, 760, "SUPRA MKV", font(AKIRA, 58), shadow=False)
    e2 = centered(d, 840, "TINTED CLEAR LENSES", font(UNB % 600, 40), shadow=False)
    e3 = centered(d, 900, "& HOUSINGS", font(UNB % 600, 40), shadow=False)
    e4 = centered(d, 990, "$72", font(AKIRA, 210), shadow=False)
    e5 = centered(d, 1250, "WAS $200", font(AKIRA, 60), shadow=False); strike(d, e5)
    e6 = centered(d, 1345, "ENDS NOV 30", font(UNB % 500, 36), fill=(200, 200, 200, 255), shadow=False)
    im.convert("RGB").save(f"{WORK}/endcard.png")
    t0 = sum(s[3] for s in SEGS) / FPS
    for lab, b in (("logo", lb), ("URL", bu), ("SUPRA MKV", e1), ("TINTED CLEAR LENSES", e2), ("& HOUSINGS", e3),
                   ("$72", e4), ("WAS $200", e5), ("ENDS NOV 30", e6)):
        boxes.append({"t0": t0, "t1": t0 + END_FRAMES / FPS, "x": b[0], "y": b[1], "w": b[2], "h": b[3], "label": lab, "key": True})
    json.dump(boxes, open(f"{WORK}/text_boxes.json", "w"), indent=1)
    return boxes


def run(cmd):
    subprocess.run(cmd, check=True)


def segment(name, src, t_in, frames, speed):
    out = f"{WORK}/{name}.mp4"
    src_dur = frames / FPS * speed + 0.2
    vf = (f"{TONEMAP},scale={W}:{H}:flags=lanczos,setsar=1,setpts=(PTS-STARTPTS)/{speed:.6f},fps={FPS}")
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t_in:.3f}", "-t", f"{src_dur:.3f}", "-i", f"{SRC}/{src}",
         "-vf", vf, "-frames:v", str(frames), "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", out])
    return out


def main():
    os.makedirs(WORK, exist_ok=True); os.makedirs(os.path.dirname(OUT), exist_ok=True)
    make_text()
    parts = [segment(n, s, t, f, sp) for n, s, t, f, sp, _ in SEGS]
    end = f"{WORK}/G_endcard.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", f"{WORK}/endcard.png",
         "-vf", "fade=t=in:st=0:d=0.2,format=yuv420p", "-frames:v", str(END_FRAMES), "-c:v", "libx264", "-crf", "14", end])
    parts.append(end)
    with open(f"{WORK}/list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    total = (sum(s[3] for s in SEGS) + END_FRAMES) / FPS
    o0, o1 = 4 / FPS, 140 / FPS
    fc = (f"[1:v]format=rgba,fade=t=in:st={o0:.3f}:d=0.2:alpha=1,fade=t=out:st={o1 - 0.2:.3f}:d=0.2:alpha=1[t];"
          f"[0:v][t]overlay=0:0:enable='between(t,0,{o1:.3f})',format=yuv420p[v];"
          f"[2:a]atrim=start={MUSIC_T0},asetpts=PTS-STARTPTS,atrim=duration={total:.3f},"
          f"afade=t=out:st={total - 0.9:.3f}:d=0.9,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt",
         "-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", f"{WORK}/txt_open.png", "-i", MUSIC,
         "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
         "-movflags", "+faststart", OUT])
    print(OUT, f"{total:.3f}s")


if __name__ == "__main__":
    main()
