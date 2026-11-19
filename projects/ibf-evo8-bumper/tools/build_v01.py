"""R2 ibf-evo8-bumper v0.1 (music swap; v0 used Blood Code, already used on toyota-gr-corolla): quick draft from the 2023 Evo 8 bumper footage.

Cards are drawn with PIL (Akira for prices/headline, Unbounded next to the logo), the cut and mix
are one ffmpeg graph. Prices come from projects/_illum-bf26/PRICES.md (owner's numbers, PENDING).
Usage: python projects/ibf-evo8-bumper/tools/build_v0.py [out.mp4]
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
M = "/home/user/media/ibf-evo8-bumper"
W_ = f"{M}/work"; os.makedirs(W_, exist_ok=True)
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{W_}/ibf-evo8-bumper_v0.1.mp4"
NOTEXT = f"{M}/dropbox/evo_notext.mov"      # "Evo bumper process without text.mov" (2023)
VO = f"{M}/dropbox/evo_voiceover.mov"       # "evo bumper voiceover.mov" (burned captions -> cropped off)
MUSIC = f"{M}/music/horizons.wav"            # "Electric Horizons" - Andre Marteen (TikTok CML 7420070383351056400)
MUSIC_START = 54.796                        # build, stop at 59.5, full re-entry 60.836 = street cut (6.04)
AKIRA = f"{REPO}/assets/fonts/akira/AkiraExpanded-SuperBold.otf"
UNB = lambda w: f"{REPO}/assets/fonts/unbounded/Unbounded-{w}.ttf"
LOGO = f"{REPO}/remotion/public/IllumaestheticLogoColor-01.png"
FPS = 30

# Prices (PRICES.md rows "Evo 8 front bumper"): owner's planned numbers, store shows $600/$650 -> PENDING OWNER.
OE_NOW, OE_WAS = "$450", "$750"
NC_NOW, NC_WAS = "$480", "$800"

# timeline: cuts 6.04 (track 60.836) and 11.056 (track 65.852)
T_END_CARD = 65.852 - MUSIC_START             # 12 beats (0.418 s) after the re-entry
SHOTS = [
    # A unwrap (the "unbox"): VO clip, crop above its burned captions (captions at y >= ~1390)
    dict(src=VO, t=0.10, dur=3.00, speed=1.0, crop="742:1320:200:0"),
    # B test fit on the car
    dict(src=NOTEXT, t=6.75, dur=3.04, speed=1.0),
    # C street drive-in, D front close, E slow walk-around (3/4 front)
    dict(src=NOTEXT, t=10.10, dur=0.76, speed=1.0),
    dict(src=NOTEXT, t=10.90, dur=0.56, speed=1.0),
]
used = sum(s["dur"] for s in SHOTS)
e_dur = T_END_CARD - used
SHOTS.append(dict(src=NOTEXT, t=12.50, dur=e_dur, speed=3.45 / e_dur))
END_DUR = 4.5
TOTAL = T_END_CARD + END_DUR

boxes = []  # text boxes for safezone_check


def font(path, size):
    return ImageFont.truetype(path, size)


def text_c(d, cx, y, s, f, fill, label, t0, t1, key=False, strike=False):
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    x = cx - (r - l) / 2 - l
    d.text((x, y - t), s, font=f, fill=fill)
    if strike:
        my = y + (b - t) * 0.5
        d.line([(cx - (r - l) / 2 - 6, my), (cx + (r - l) / 2 + 6, my)], fill=(230, 40, 40, 255), width=6)
    boxes.append(dict(t0=t0, t1=t1, x=int(cx - (r - l) / 2), y=int(y), w=int(r - l), h=int(b - t), label=label, key=key))
    return y + (b - t)


def open_card():
    """Price within the first 2 s, over the unwrap shot (owner OK for price text on IRL in this campaign)."""
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    t0, t1 = 0.20, 2.95
    d.rounded_rectangle((70, 330, 1010 - 90, 700), 28, fill=(0, 0, 0, 165))
    cx = (70 + 920) / 2
    y = text_c(d, cx, 370, "BLACK FRIDAY", font(UNB(600), 40), (230, 40, 40, 255), "bf", t0, t1)
    y = text_c(d, cx, y + 28, "EVO 8 BUMPER", font(AKIRA, 58), (255, 255, 255, 255), "title", t0, t1, key=True)
    text_c(d, cx, y + 30, f"FROM {OE_NOW}", font(AKIRA, 92), (255, 255, 255, 255), "price", t0, t1, key=True)
    im.save(f"{W_}/card_open.png")
    return t0, t1


def end_card():
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    t0, t1 = T_END_CARD, TOTAL
    y = text_c(d, 484, 400, "BLACK FRIDAY", font(AKIRA, 60), (230, 40, 40, 255), "bf", t0, t1)
    y = text_c(d, 484, y + 26, "EVO 8 FRONT BUMPER", font(UNB(600), 40), (255, 255, 255, 255), "title", t0, t1, key=True)
    top = y + 70
    for cx, lab, now, was in ((270, "OE REPLACEMENT", OE_NOW, OE_WAS), (700, "NOSE CHOP", NC_NOW, NC_WAS)):
        d.rounded_rectangle((cx - 205, top - 30, cx + 205, top + 330), 22, outline=(255, 255, 255, 70), width=3)
        yy = text_c(d, cx, top, lab, font(UNB(500), 30), (255, 255, 255, 230), lab, t0, t1, key=True)
        yy = text_c(d, cx, yy + 40, now, font(AKIRA, 96), (255, 255, 255, 255), lab + " now", t0, t1, key=True)
        text_c(d, cx, yy + 36, was, font(AKIRA, 50), (150, 150, 150, 255), lab + " was", t0, t1, key=True, strike=True)
    y = text_c(d, 484, top + 380, "ENDS NOV 30", font(UNB(500), 36), (255, 255, 255, 255), "ends", t0, t1, key=True)
    logo = Image.open(LOGO).convert("RGBA"); lw = 640
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    ly = y + 90; im.alpha_composite(logo, (484 - lw // 2, ly))
    boxes.append(dict(t0=t0, t1=t1, x=484 - lw // 2, y=ly, w=lw, h=logo.height, label="logo"))
    text_c(d, 484, ly + logo.height + 40, "WWW.ILLUMAESTHETIC.COM", font(UNB(400), 34), (255, 255, 255, 255), "url", t0, t1, key=True)
    im.convert("RGB").save(f"{W_}/card_end.png")


def main():
    o0, o1 = open_card(); end_card()
    json.dump(boxes, open(f"{W_}/text_boxes_v01.json", "w"), indent=1)
    inputs, fc, labels = [], [], []
    for i, s in enumerate(SHOTS):
        src_len = s["dur"] * s["speed"]
        inputs += ["-ss", f"{s['t']:.3f}", "-t", f"{src_len + 0.2:.3f}", "-i", s["src"]]
        v = f"[{i}:v]"
        chain = []
        if s.get("crop"): chain.append(f"crop={s['crop']}")
        chain.append("scale=1080:1920:flags=lanczos,setsar=1")
        if s["speed"] != 1.0: chain.append(f"setpts=PTS/{s['speed']:.5f}")
        chain += [f"fps={FPS}", f"trim=duration={s['dur']:.4f}", "setpts=PTS-STARTPTS", "format=yuv420p"]
        fc.append(f"{v}{','.join(chain)}[v{i}]"); labels.append(f"[v{i}]")
    n = len(SHOTS)
    inputs += ["-loop", "1", "-t", f"{END_DUR:.3f}", "-i", f"{W_}/card_end.png"]
    fc.append(f"[{n}:v]fps={FPS},scale=1080:1920,setsar=1,format=yuv420p,"
              f"zoompan=z='if(lt(on,5),0.94+0.012*on,1)':d=1:s=1080x1920:fps={FPS}[vend]")
    labels.append("[vend]")
    fc.append(f"{''.join(labels)}concat=n={n + 1}:v=1:a=0[vcat]")
    inputs += ["-loop", "1", "-i", f"{W_}/card_open.png"]
    fc.append(f"[{n + 1}:v]format=rgba,fade=t=in:st={o0}:d=0.12:alpha=1,fade=t=out:st={o1 - 0.12}:d=0.12:alpha=1[ov]")
    fc.append(f"[vcat][ov]overlay=0:0:shortest=1:enable='between(t,{o0},{o1})'[vout]")
    inputs += ["-ss", f"{MUSIC_START}", "-t", f"{TOTAL:.3f}", "-i", MUSIC]
    fc.append(f"[{n + 2}:a]afade=t=out:st={TOTAL - 0.8:.3f}:d=0.8,"
              f"loudnorm=I=-15:TP=-2:LRA=11,aresample=48000,volume=AGAIN[aout]")
    fc[-1] = fc[-1].replace("AGAIN", os.environ.get("AGAIN", "0dB"))
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
           "-t", f"{TOTAL:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", OUT]
    subprocess.run(cmd, check=True)
    print(OUT, f"{TOTAL:.2f}s", "end card at", f"{T_END_CARD:.3f}", "E speed", f"{SHOTS[-1]['speed']:.3f}")


if __name__ == "__main__":
    main()
