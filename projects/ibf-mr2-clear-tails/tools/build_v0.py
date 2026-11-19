"""R4 ibf-mr2-clear-tails v0: quick draft. MR2 Spyder (ZZW30) clear tail lenses, Black Friday 2026.

BEFORE = real Kalvin FX30 footage (black ZZW30, stock red tails, daytime, S-Log3 -> LUT + hue).
AFTER  = the store's own product photos (real photos of the clear lenses on red / pink ZZW30s) as stills,
         because no video of the clear tails exists in Dropbox (owner must OK stills / film the shots).
NIGHT  = no footage with the clear tails at night exists -> the drop goes straight to the end card.
Prices from projects/_illum-bf26/PRICES.md: $198 (was $550), "only 12 sets" (owner's words, matches stock).
Usage: python projects/ibf-mr2-clear-tails/tools/build_v0.py [out.mp4]
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
M = "/home/user/media/ibf-mr2-clear-tails"
W_ = f"{M}/work"; os.makedirs(W_, exist_ok=True)
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{W_}/ibf-mr2-clear-tails_v0.mp4"
D = f"{M}/dropbox"; S = f"{M}/store"
LUT = f"{W_}/slog3.cube"            # projects/toyota-sera-scan-process/tools/slog3_lut.py --sat 1.15
MUSIC = f"{M}/music/saturday_night.wav"   # "Saturday Night" - Mhobold (TikTok CML 7397784931860039697)
MUSIC_START = 36.85                 # strong onset; drop at 44.722 -> 7.872 s into the reel
AKIRA = f"{REPO}/assets/fonts/akira/AkiraExpanded-SuperBold.otf"
UNB = lambda w: f"{REPO}/assets/fonts/unbounded/Unbounded-{w}.ttf"
LOGO = f"{M}/IllumaestheticLogoColor-01.png"
FPS = 30
NOW, WAS, STOCK = "$198", "$550", "ONLY 12 SETS"

# cut times = measured strong onsets of the track minus MUSIC_START
ON = [0.0, 40.588, 41.517, 42.446, 43.607, 44.722]
CUT = [0.0] + [round(t - MUSIC_START, 3) for t in ON[1:]]
END_DUR = 5.574                     # 3 bars at 129.2 BPM (end card has ~15 words)
TOTAL = CUT[-1] + END_DUR

FX = "lut3d={lut},hue=h=20,crop=1215:2160:{x}:0,scale=1080:1920:flags=lanczos,setsar=1"
SHOTS = [
    dict(kind="clip", src=f"{D}/FX30_4022.MP4", t=14.9, x=1120),   # stock tail, low rear 3/4, slow move (one 3.7 s shot under the price)
    dict(kind="still", src=f"{S}/s4.jpg", box=(430, 0, 430 + 822, 1462), z=(1.0, 1.08)),  # clear tail close
    dict(kind="still", src=f"{S}/s3.jpg", box=(490, 0, 490 + 822, 1462), z=(1.08, 1.0)),      # clear tail close, other side
    dict(kind="still", src=f"{S}/s2.jpg", box=(800, 0, 800 + 864, 1536), z=(1.0, 1.06)),  # pink ZZW30 rear, clear tails
    dict(kind="still", src=f"{S}/s5.jpg", box=(876, 0, 876 + 608, 1080), z=(1.0, 1.07)),    # the lens pair
]

boxes = []


def font(path, size):
    return ImageFont.truetype(path, size)


def text_c(d, cx, y, s, f, fill, label, t0, t1, key=False, strike=False):
    l, t, r, b = d.textbbox((0, 0), s, font=f)
    x = cx - (r - l) / 2 - l
    d.text((x, y - t), s, font=f, fill=fill)
    if strike:
        my = y + (b - t) * 0.5
        d.line([(cx - (r - l) / 2 - 8, my), (cx + (r - l) / 2 + 8, my)], fill=(230, 40, 40, 255), width=7)
    boxes.append(dict(t0=t0, t1=t1, x=int(cx - (r - l) / 2), y=int(y), w=int(r - l), h=int(b - t), label=label, key=key))
    return y + (b - t)


def open_card(t0, t1):
    """Price in the first 2 s (owner OK for price text on IRL in this campaign), low over the bumper."""
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = 484
    d.rounded_rectangle((90, 930, 878, 1400), 30, fill=(0, 0, 0, 170))
    y = text_c(d, cx, 970, "MR2 SPYDER CLEAR TAILS", font(UNB(600), 38), (255, 255, 255, 255), "title", t0, t1, key=True)
    y = text_c(d, cx, y + 34, NOW, font(AKIRA, 150), (255, 255, 255, 255), "price", t0, t1, key=True)
    text_c(d, cx, y + 34, f"WAS {WAS}", font(AKIRA, 52), (170, 170, 170, 255), "was", t0, t1, key=True, strike=True)
    im.save(f"{W_}/card_open.png")


def end_card(t0, t1):
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    y = text_c(d, 484, 380, "BLACK FRIDAY", font(AKIRA, 64), (230, 40, 40, 255), "bf", t0, t1)
    y = text_c(d, 484, y + 30, "MR2 SPYDER (ZZW30)", font(UNB(600), 40), (255, 255, 255, 255), "car", t0, t1, key=True)
    y = text_c(d, 484, y + 18, "CLEAR TAIL LIGHT LENSES", font(UNB(500), 34), (255, 255, 255, 230), "product", t0, t1, key=True)
    y = text_c(d, 484, y + 50, NOW, font(AKIRA, 170), (255, 255, 255, 255), "now", t0, t1, key=True)
    y = text_c(d, 484, y + 36, f"WAS {WAS}", font(AKIRA, 56), (160, 160, 160, 255), "was", t0, t1, key=True, strike=True)
    y = text_c(d, 484, y + 50, STOCK, font(AKIRA, 50), (230, 40, 40, 255), "stock", t0, t1, key=True)
    y = text_c(d, 484, y + 24, "ENDS NOV 30", font(UNB(500), 34), (255, 255, 255, 255), "ends", t0, t1, key=True)
    logo = Image.open(LOGO).convert("RGBA"); lw = 600
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    ly = y + 70; im.alpha_composite(logo, (484 - lw // 2, ly))
    boxes.append(dict(t0=t0, t1=t1, x=484 - lw // 2, y=ly, w=lw, h=logo.height, label="logo"))
    yy = text_c(d, 484, ly + logo.height + 36, "WWW.ILLUMAESTHETIC.COM", font(UNB(400), 32), (255, 255, 255, 255), "url", t0, t1, key=True)
    assert yy < 1440, yy
    im.convert("RGB").save(f"{W_}/card_end.png")


def still_png(s, i):
    im = Image.open(s["src"]).convert("RGB").crop(s["box"]).resize((1080, 1920), Image.LANCZOS)
    p = f"{W_}/still_{i}.png"; im.save(p); return p


def main():
    o0, o1 = 0.15, CUT[1] - 0.05
    open_card(o0, o1); end_card(CUT[-1], TOTAL)
    json.dump(boxes, open(f"{W_}/text_boxes_v0.json", "w"), indent=1)
    inputs, fc, labels = [], [], []
    for i, s in enumerate(SHOTS):
        dur = CUT[i + 1] - CUT[i]
        if s["kind"] == "clip":
            inputs += ["-ss", f"{s['t']:.3f}", "-t", f"{dur + 0.3:.3f}", "-i", s["src"]]
            chain = [FX.format(lut=LUT, x=s["x"]), f"fps={FPS}", f"trim=duration={dur:.4f}", "setpts=PTS-STARTPTS", "format=yuv420p"]
        else:
            n = int(round(dur * FPS)); z0, z1 = s["z"]
            inputs += ["-loop", "1", "-t", f"{dur + 0.3:.3f}", "-i", still_png(s, i)]
            chain = ["scale=2160:3840", f"zoompan=z='{z0}+({z1}-{z0})*on/{max(n - 1, 1)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps={FPS}",
                     f"trim=duration={dur:.4f}", "setpts=PTS-STARTPTS", "setsar=1", "format=yuv420p"]
        fc.append(f"[{i}:v]{','.join(chain)}[v{i}]"); labels.append(f"[v{i}]")
    n = len(SHOTS)
    inputs += ["-loop", "1", "-t", f"{END_DUR:.3f}", "-i", f"{W_}/card_end.png"]
    fc.append(f"[{n}:v]fps={FPS},scale=1080:1920,setsar=1,format=yuv420p,trim=duration={END_DUR:.3f}[vend]")
    labels.append("[vend]")
    fc.append(f"{''.join(labels)}concat=n={n + 1}:v=1:a=0[vcat]")
    inputs += ["-loop", "1", "-i", f"{W_}/card_open.png"]
    fc.append(f"[{n + 1}:v]format=rgba,fade=t=in:st={o0}:d=0.12:alpha=1,fade=t=out:st={o1 - 0.12}:d=0.12:alpha=1[ov]")
    fc.append(f"[vcat][ov]overlay=0:0:shortest=1:enable='between(t,{o0},{o1})'[vout]")
    inputs += ["-ss", f"{MUSIC_START}", "-t", f"{TOTAL:.3f}", "-i", MUSIC]
    fc.append(f"[{n + 2}:a]afade=t=out:st={TOTAL - 0.9:.3f}:d=0.9,aresample=48000,volume={os.environ.get('AGAIN', '0dB')},"
              f"alimiter=limit=0.82:level=false[aout]")
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
           "-t", f"{TOTAL:.3f}", "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", OUT]
    subprocess.run(cmd, check=True)
    print(OUT, f"{TOTAL:.2f}s", "cuts", CUT)


if __name__ == "__main__":
    main()
