"""R7 ibf-print-your-own v0: quick draft (~17.5 s, 1080x1920, 30 fps).

A 0.000-6.000  real duct STL (Design Market file) turntable + price hook (BLOBEYE DUCTS / $140 / $200 struck)
B 6.000-10.550 real Bambu printer timelapses (MR2 parts: placeholder until the duct print is filmed); cut on the drop
C 10.550-13.988 live store page (phone capture): gallery photos of the duct on the blobeye
D 13.988-17.500 end card: logo, $140 / $200 struck, WWW.ILLUMAESTHETIC.COM, ENDS NOV 30
Music: Roni Size "The Streets", track 146.950 -> video 0; drop 152.950 = video 6.000.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

M = "/home/user/media/ibf-print-your-own"
W, H, FPS = 1080, 1920, 30
REPO = "/home/user/Illumaesthetic-Video-Editor"
AKIRA = f"{REPO}/assets/fonts/akira/AkiraExpanded-SuperBold.otf"
UNB = lambda w: f"{REPO}/assets/fonts/unbounded/Unbounded-{w}.ttf"
OUT = f"{M}/v0"; os.makedirs(OUT, exist_ok=True)
T0 = 146.950
CUTS = [0.0, 6.0, 8.368, 10.550, 11.596, 12.618, 13.988, 17.5]   # track onsets 155.318, 157.501, 158.546, 159.568, 160.938
BOXES = []


def sh(c):
    print(" ".join(c)[:200]); subprocess.run(c, check=True)


def fit(font_path, text, max_w, size):
    while size > 10:
        f = ImageFont.truetype(font_path, size)
        if f.getbbox(text)[2] - f.getbbox(text)[0] <= max_w: return f
        size -= 2
    return f


def text_c(d, y, text, font, fill=(255, 255, 255), strike=False, name="", key=False, t=(0, 0)):
    bb = font.getbbox(text); w = bb[2] - bb[0]; h = bb[3] - bb[1]
    x = (W - w) // 2 - bb[0]
    d.text((x, y - bb[1]), text, font=font, fill=fill)
    if strike:
        sy = y + h // 2; d.line([(x - 10, sy), (x + bb[2] + 10, sy)], fill=(225, 40, 40), width=max(6, h // 9))
    BOXES.append({"name": name, "x0": x + bb[0], "y0": y, "x1": x + bb[2], "y1": y + h, "t0": t[0], "t1": t[1], "key": key})
    return y + h


def card_hook():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    t = (0.25, 5.8)
    y = text_c(d, 380, "BLOBEYE DUCTS", fit(AKIRA, "BLOBEYE DUCTS", 740, 74), name="headline", key=True, t=t)
    y = text_c(d, y + 40, "$140", ImageFont.truetype(AKIRA, 190), fill=(255, 255, 255), name="price", key=True, t=t)
    y = text_c(d, y + 36, "$200", ImageFont.truetype(AKIRA, 84), fill=(170, 170, 170), strike=True, name="was", key=True, t=t)
    im.save(f"{OUT}/txt_hook.png")


def card_end():
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    t = (CUTS[6] + 0.2, CUTS[7] - 0.3)
    logo = Image.open(f"{M}/logo/IllumaestheticLogoColor-01.png").convert("RGBA")
    lw = 720; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    ly = 400; im.paste(logo, ((W - lw) // 2, ly), logo)
    BOXES.append({"name": "logo", "x0": (W - lw) // 2, "y0": ly, "x1": (W + lw) // 2, "y1": ly + logo.height, "t0": t[0], "t1": t[1], "key": True})
    y = ly + logo.height + 110
    y = text_c(d, y, "BLOBEYE DUCTS", fit(AKIRA, "BLOBEYE DUCTS", 760, 60), name="end_headline", key=True, t=t)
    y = text_c(d, y + 34, "$140", ImageFont.truetype(AKIRA, 150), name="end_price", key=True, t=t)
    y = text_c(d, y + 30, "$200", ImageFont.truetype(AKIRA, 70), fill=(170, 170, 170), strike=True, name="end_was", key=True, t=t)
    y = text_c(d, y + 60, "WWW.ILLUMAESTHETIC.COM", fit(UNB(400), "WWW.ILLUMAESTHETIC.COM", 760, 44), fill=(225, 225, 225), name="url", key=True, t=t)
    y = text_c(d, y + 26, "SALE ENDS NOV 30", ImageFont.truetype(UNB(500), 34), fill=(190, 190, 190), name="ends", key=True, t=t)
    im.save(f"{OUT}/end_card.png")


def seg_a():
    n = 80; dur = CUTS[1] - CUTS[0]  # first 80 of 120 frames: -70 -> -42 deg, stays face-on
    sh(["ffmpeg", "-v", "error", "-y", "-framerate", f"{n / dur:.4f}", "-i", f"{M}/stlframes2/f%04d.png",
        "-loop", "1", "-i", f"{OUT}/txt_hook.png",
        "-filter_complex", f"[0]trim=end_frame=80,setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H},format=rgba[b];[1]format=rgba,fade=in:st=0.1:d=0.15:alpha=1[t];[b][t]overlay=0:0:shortest=1,format=yuv420p",
        "-t", f"{dur:.3f}", "-r", str(FPS), "-c:v", "libx264", "-crf", "16", f"{OUT}/a.mp4"])


def seg_tl(src, ss, dur_src, dur, cx, out):
    # 16:9 720p timelapse -> 9:16 crop around cx, sped to fit dur
    cw = 405
    sh(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(dur_src), "-i", f"{M}/raw/{src}",
        "-vf", f"setpts=PTS*{dur / dur_src:.5f},fps={FPS},crop={cw}:720:{cx - cw // 2}:0,scale={W}:{H}:flags=lanczos,eq=contrast=1.06:saturation=1.05,unsharp=5:5:0.6,format=yuv420p",
        "-t", f"{dur:.3f}", "-an", "-c:v", "libx264", "-crf", "16", out])


def seg_store():
    # gallery slides 0 -> 2 -> 1 as swipes; page crop rows 120-1400 (header..title, above the $100 file price)
    frames = []
    PH = 860  # header + gallery + dots only (store title and the $100 file price stay out of frame)
    pages = [Image.open(f"{M}/web/store_g{i}.png").convert("RGB").crop((0, 0, 1080, PH)) for i in (0, 2, 1)]
    seg_t = [CUTS[3], CUTS[4], CUTS[5], CUTS[6]]
    os.makedirs(f"{OUT}/store", exist_ok=True)
    k = 0
    for i in range(3):
        nfr = round((seg_t[i + 1] - seg_t[i]) * FPS)
        for f in range(nfr):
            can = Image.new("RGB", (W, H), (0, 0, 0))
            sw = 8  # swipe frames at the start of slides 2/3
            if i > 0 and f < sw:
                a = (f + 1) / sw; a = a * a * (3 - 2 * a)
                prev, cur = pages[i - 1], pages[i]
                gal = (140, 800)  # gallery band slides; rest stays
                base = cur.copy()
                band = Image.new("RGB", (W * 2, gal[1] - gal[0]))
                band.paste(prev.crop((0, gal[0], W, gal[1])), (0, 0)); band.paste(cur.crop((0, gal[0], W, gal[1])), (W, 0))
                base.paste(band.crop((int(a * W), 0, int(a * W) + W, gal[1] - gal[0])), (0, gal[0]))
                pg = base
            else:
                pg = pages[i]
            zoom = 1.06 + 0.05 * ((seg_t[i] - seg_t[0]) * FPS + f) / ((seg_t[3] - seg_t[0]) * FPS)
            pz = pg.resize((int(W * zoom), int(PH * zoom)), Image.LANCZOS)
            ox = (pz.width - W) // 2
            pz = pz.crop((ox, 0, ox + W, pz.height))
            can.paste(pz, (0, (H - pz.height) // 2 - 120))
            can.save(f"{OUT}/store/f{k:04d}.png"); k += 1
    sh(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{OUT}/store/f%04d.png", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "16", f"{OUT}/c.mp4"])


def seg_end():
    dur = CUTS[7] - CUTS[6]
    sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{OUT}/end_card.png", "-vf", f"fps={FPS},fade=in:st=0:d=0.2,fade=out:st={dur - 0.35:.3f}:d=0.35,format=yuv420p",
        "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "16", f"{OUT}/d.mp4"])


def assemble():
    parts = ["a.mp4", "b1.mp4", "b2.mp4", "c.mp4", "d.mp4"]
    open(f"{OUT}/list.txt", "w").write("".join(f"file '{OUT}/{p}'\n" for p in parts))
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/list.txt", "-c", "copy", f"{OUT}/video.mp4"])
    dur = CUTS[-1]
    # music: two-pass loudnorm to -14 LUFS, TP -1.5
    af = f"atrim={T0}:{T0 + dur},asetpts=PTS-STARTPTS,afade=in:d=0.03,afade=out:st={dur - 1.0}:d=1.0"
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{M}/music/streets.wav", "-af", af + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
          f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    sh(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video.mp4", "-i", f"{M}/music/streets.wav", "-filter_complex", f"[1]{af},{ln},aresample=48000[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-t", f"{dur:.3f}", f"{OUT}/out.mp4"])
    json.dump([{"t0": b["t0"], "t1": b["t1"], "x": b["x0"], "y": b["y0"], "w": b["x1"] - b["x0"], "h": b["y1"] - b["y0"],
                "label": b["name"], "key": b["key"]} for b in BOXES], open(f"{OUT}/overlay_boxes.json", "w"), indent=1)


if __name__ == "__main__":
    card_hook(); card_end()
    seg_a()
    seg_tl("actual_latch.avi", 0.4, 8.9, CUTS[2] - CUTS[1], 580, f"{OUT}/b1.mp4")
    seg_tl("actual_mr2.avi", 0.4, 8.9, CUTS[3] - CUTS[2], 640, f"{OUT}/b2.mp4")
    seg_store(); seg_end(); assemble()
