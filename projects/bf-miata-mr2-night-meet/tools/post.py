"""v0 assembly: 15 fps Blender renders -> 30 fps 1080x1920 frames with character composites, scan labels, sale card and
Epsilon+ wordmark; then mux the music (from its start), loudness to -14 LUFS / TP < -1 dBFS.

    python post.py            -> /home/user/media/work/out/bf-miata-mr2-night-meet_v0.mp4
"""
import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

M = "/home/user/media/bf-miata-mr2-night-meet"
OUT = f"{M}/work/frames"; os.makedirs(OUT, exist_ok=True)
FINAL = "/home/user/media/work/out/bf-miata-mr2-night-meet_v1.5.mp4"   # v1: stock first, zones install one by one; no characters
TL = json.load(open(os.path.join(os.path.dirname(__file__), "..", "specs", "timeline.json")))
F30 = TL["f30"]
W, H = 1080, 1920
FD = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FM = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf"
if not os.path.exists(FM):
    FM = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
OFF = (232, 236, 242)
CX = 484            # centre of the safe band x 48-920 (knowledge/safe-zones.md)
LOGO = Image.open(f"{M}/logo/Epsilon+ Logo.png").convert("RGBA")


def font(p, s): return ImageFont.truetype(p, s)


class Layer:
    """Text drawn with alpha must go on a transparent layer and be composited; ImageDraw on an opaque frame replaces
    pixels and ignores the fill alpha (v1.5 found the URL staying on while the wordmark faded)."""
    def __init__(self, base): self.base = base; self.im = Image.new("RGBA", base.size, (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.im)
    def __enter__(self): return self.d
    def __exit__(self, *a): self.base.alpha_composite(self.im)


def ease(t): t = min(max(t, 0), 1); return t * t * (3 - 2 * t)


def shot_frame(shot, i):
    d = f"{M}/work/{shot}"; fs = sorted(os.listdir(d)); fs = [f for f in fs if f.endswith(".png")]
    im = Image.open(os.path.join(d, fs[min(i // 2, len(fs) - 1)])).convert("RGB")
    return im.resize((W, H), Image.LANCZOS)


def put_char(base, img, h, cx, by, alpha=1.0, shadow=True):
    r = img.resize((int(img.width * h / img.height), h), Image.LANCZOS)
    if shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
        d.ellipse([cx - r.width * 0.42, by - h * 0.03, cx + r.width * 0.42, by + h * 0.03], fill=(0, 0, 0, int(150 * alpha)))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(h * 0.02)))
    if alpha < 1:
        a = r.getchannel("A").point(lambda v: int(v * alpha)); r.putalpha(a)
    base.alpha_composite(r, (int(cx - r.width / 2), int(by - h)))


def label(base, t, line1, line2, y=300):
    a = int(255 * ease(t * 4))
    with Layer(base) as d:
        d.text((90, y), line1, font=font(FD, 66), fill=(*OFF, a))
        d.text((92, y + 92), line2, font=font(FM, 34), fill=(*OFF, int(a * 0.8)))


# v1.3 (user: "for each clip of the parts, show the text so people know what part and the pricing/saving").
# name, car, was, now: Current Price -> BF 2026 Price from projects/_blackfriday/bf_liquidation_pricing.csv
PRICE = {"mr2_skirts": ("SIDE SKIRT / FENDER", "MR2 SPYDER", 700, 560), "mr2_eyelids": ("HEADLIGHT EYELIDS", "MR2 SPYDER", 100, 80),
         "mr2_hood": ("HOOD VENTS", "MR2 SPYDER", 400, 320), "mr2_spats": ("REAR SPATS", "MR2 SPYDER", 350, 280),
         "mr2_duck": ("REAR DUCKBILL", "MR2 SPYDER", 220, 176), "nc_bumper": ("FRONT BUMPER + LIP", "NC MIATA", 1100, 880),
         "nc_canards": ("CANARDS", "NC MIATA", 200, 160), "nc_fender": ("FENDER CUTS", "NC MIATA", 300, 240),
         "nc_skirts": ("SIDE SKIRTS", "NC MIATA", 500, 400), "nc_spats": ("REAR SPATS (NC1)", "NC MIATA", 250, 200)}
# shot -> [(key, start fraction, end fraction)]; a label enters as its part arrives
# shot -> [(key, start fraction, slot)]; v1.4 (user: "some of the text cuts away too fast, if there is two text you can put one
# above and another below"): every label stays up to the end of its shot; a second part's label stacks below the first.
LABELS = {"s02": [("mr2_skirts", 0.20, 0)], "s03": [("mr2_eyelids", 0.12, 0)], "s04": [("mr2_hood", 0.12, 0)],
          "s05": [("mr2_spats", 0.10, 0), ("mr2_duck", 0.40, 1)], "s07": [("nc_bumper", 0.20, 0), ("nc_canards", 0.45, 1)],
          "s08": [("nc_fender", 0.20, 0)], "s09": [("nc_skirts", 0.10, 0), ("nc_spats", 0.40, 1)]}
SLOT_DY = 834      # second label goes below the car (block y 1130-1400, inside the safe band y 285-1440)


def money(v): return f"${v:,}"


def price_label(base, key, t, plate, slot=0):
    """Part name + car, then was (struck) -> now and SAVE. All inside the safe zone (x 48-920, y 285-1440)."""
    name, car, was, now = PRICE[key]
    a = ease(t * 5); A = int(255 * a); dy = slot * SLOT_DY
    if plate:      # lot shots: a soft dark plate so the text reads over the car and lamps
        g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).rounded_rectangle([60, 296 + dy, 900, 566 + dy], 28, fill=int(150 * a))
        base.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 0)] * 3 + [g.filter(ImageFilter.GaussianBlur(18))]))
    with Layer(base) as d:
        d.text((90, 312 + dy), name, font=font(FD, 62), fill=(255, 255, 255, A))
        d.text((92, 396 + dy), f"{car} · 20% OFF", font=font(FM, 30), fill=(*OFF, int(A * 0.85)))
        fw, fn = font(FM, 44), font(FD, 64)
        ws = money(was); x = 92; yb = 452 + dy
        d.text((x, yb + 14), ws, font=fw, fill=(170, 174, 180, A)); bb = d.textbbox((x, yb + 14), ws, font=fw)
        d.line([(bb[0] - 4, (bb[1] + bb[3]) // 2), (bb[2] + 4, (bb[1] + bb[3]) // 2)], fill=(170, 174, 180, A), width=4)
        x = bb[2] + 28; ns = money(now); d.text((x, yb), ns, font=fn, fill=(255, 255, 255, A)); bb2 = d.textbbox((x, yb), ns, font=fn)
        d.text((bb2[2] + 28, yb + 18), f"SAVE {money(was - now)}", font=font(FM, 38), fill=(255, 210, 31, A))


def title(base, i, fade_out=False, n2=0, i2=0):
    """v1.4 opening title (user: "the beginning needs a title to show the deal/platforms"). Safe band x 48-920, y 285-1440."""
    a = ease(i / 5) * ((1 - ease((i2 - (n2 - 5)) / 5)) if fade_out else 1); A = int(255 * a)
    g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).rounded_rectangle([60, 300, 908, 700], 32, fill=int(165 * a))
    base.alpha_composite(Image.merge("RGBA", [Image.new("L", (W, H), 0)] * 3 + [g.filter(ImageFilter.GaussianBlur(22))]))
    with Layer(base) as d:
        d.text((CX, 352), "BLACK FRIDAY", font=font(FM, 40), fill=(255, 210, 31, A), anchor="mm")
        d.text((CX, 455), "20% OFF", font=font(FD, 150), fill=(255, 255, 255, A), anchor="mm")
        d.text((CX, 565), "MR2 SPYDER  ·  NC MIATA", font=font(FD, 52), fill=(*OFF, A), anchor="mm")
        d.text((CX, 640), "EPSILON+ FIBERGLASS AERO", font=font(FM, 32), fill=(*OFF, int(A * 0.85)), anchor="mm")


def card(base_img, i, n):
    bg = base_img.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.32)).convert("RGBA")
    lay = Image.new("RGBA", bg.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    a1 = int(255 * ease(i / 6)); a2 = int(255 * ease((i - 14) / 6))      # list lands on the next hit (+0.82 s)
    d.text((CX, 330), "BLACK FRIDAY", font=font(FM, 38), fill=(*OFF, a1), anchor="mm")
    d.text((CX, 445), "20% OFF", font=font(FD, 160), fill=(255, 255, 255, a1), anchor="mm")
    d.text((CX, 568), "MR2 SPYDER + NC MIATA AERO", font=font(FD, 44), fill=(*OFF, a1), anchor="mm")
    rows = [("MR2 SPYDER", None, None), ("Side Skirt / Fender Combo", "$700", "$560"), ("Rear Spats", "$350", "$280"),
            ("Headlight Eyelids", "$100", "$80"), ("Hood Vents", "$400", "$320"), ("Rear Duckbill", "$220", "$176"),
            ("NC MIATA", None, None), ("Front Bumper + Lip", "$1,100", "$880"), ("Fender Cuts", "$300", "$240"),
            ("Side Skirts", "$500", "$400"), ("Rear Spats (NC1)", "$250", "$200"), ("Canards", "$200", "$160")]
    y = 640; fr, fh, fp = font(FD, 36), font(FD, 40), font(FM, 34)   # safe zones: all text inside x 48-920, y 285-1440
    for name, was, now in rows:
        if was is None:
            y += 12; d.text((80, y), name, font=fh, fill=(255, 255, 255, a2)); y += 66; continue
        d.text((100, y), name, font=fr, fill=(*OFF, a2))
        wb = d.textbbox((0, 0), was, font=fp); nb = d.textbbox((0, 0), now, font=fp)
        xn = 900 - (nb[2] - nb[0]); xw = xn - 30 - (wb[2] - wb[0])
        d.text((xw, y + 2), was, font=fp, fill=(150, 154, 160, a2))
        d.line([(xw - 4, y + 22), (xw + wb[2] - wb[0] + 4, y + 22)], fill=(150, 154, 160, a2), width=3)
        d.text((xn, y + 2), now, font=fp, fill=(255, 255, 255, a2))
        y += 58
    bg.alpha_composite(lay)
    return bg


def logo(i, n):
    bg = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    a = ease(i / 4) * (1 - ease((i - (n - 14)) / 14))
    lw = 720; lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * a)))
    bg.alpha_composite(lg, (CX - lw // 2, H // 2 - lg.height // 2 - 40))
    with Layer(bg) as d:
        d.text((CX, H / 2 + 90), "WWW.EPSILON.PLUS", font=font(FM, 44), fill=(*OFF, int(255 * a)), anchor="mm")
    return bg


def main():
    shots = ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "s11", "s12"]
    k = 0; last10 = None
    for si, s in enumerate(shots):
        n = F30[si + 1] - F30[si] - (1 if si == 0 else 0) + (1 if si == 0 else 0)
        for i in range(n):
            if s == "s11":
                fr = card(last10, i, n)
            elif s == "s12":
                fr = logo(i, n)
            else:
                fr = shot_frame(s, i).convert("RGBA"); t = i / n
                for key, f0, slot in LABELS.get(s, []):
                    if i >= n * f0: price_label(fr, key, (i - n * f0) / n, plate=s in ("s03", "s04", "s05", "s07", "s08", "s09"), slot=slot)
                if s == "s01" or (s == "s02" and i < n * 0.22):
                    title(fr, i if s == "s01" else i + F30[1], fade_out=(s == "s02"), n2=round(n * 0.22), i2=i)
                if s == "s10":   # both kitted scans (owner: no characters, typical branding)
                    if i > 8: label(fr, (i - 8) / n, "MR2 SPYDER + NC MIATA", "EPSILON+ AERO · 20% OFF")
                    last10 = fr.convert("RGB")
            fr.convert("RGB").save(f"{OUT}/{k:05d}.jpg", quality=92); k += 1
    print("frames", k)
    dur = k / 30
    vid = f"{M}/work/v1_silent.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{OUT}/%05d.jpg", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", vid], check=True)
    seg = f"{M}/work/music_seg.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{M}/music/tokyo_midnight.wav", "-t", f"{dur:.3f}",
                    "-af", f"afade=t=out:st={dur - 1.4:.3f}:d=1.4", "-ar", "48000", seg], check=True)
    r = subprocess.run(["ffmpeg", "-nostats", "-i", seg, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float(r.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0]); TP = float(r.split("True peak:")[1].split("Peak:")[1].split("dBFS")[0])
    g = min(-14 - I, -1.2 - TP)            # static gain: -14 LUFS unless the true-peak ceiling wins (lesson: 'Going Up North')
    print("music I", I, "TP", TP, "gain", round(g, 2))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", seg, "-af", f"volume={g:.2f}dB,alimiter=limit=0.70:level=false:attack=1:release=50", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "256k", "-shortest", FINAL], check=True)
    print("OUT", FINAL)


if __name__ == "__main__":
    main()
