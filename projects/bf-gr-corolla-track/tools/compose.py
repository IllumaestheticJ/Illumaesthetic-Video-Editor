"""compose.py : assemble BF gr-corolla-track v0.2 at 1080x1920/30 from the shot renders, offer cards (text over the Blender
plates; owner 2026-11-17: no Del & Eps, typical branding only), the Epsilon+ end card and the music.

python compose.py [--out ...]
Cuts are on measured kick onsets of 'Electric Youth' (music/kicks.json), windows as in shot.py WIN.
v0.2 (user): game-GLB studio shots instead of scan, V2 parts highlighted + labelled, carbon canards "BACK IN STOCK".
"""
import argparse, json, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/home/user/media/work/out/bf-gr-corolla-track_v1.0.mp4')
ap.add_argument('--tag', default='v1.0'); args = ap.parse_args()
M = '/home/user/media/bf-gr-corolla-track'; R = f'{M}/renders_v10'; RC = R; FR = f'{M}/frames_{args.tag}'; os.makedirs(FR, exist_ok=True)
W, H, FPS = 1080, 1920, 30
kicks = json.load(open(f'{M}/music/kicks.json'))
CUTK = [6, 14, 17, 21, 36, 44, 60, 68]   # v1.0 owner rule: text sections long enough for slow readers
cuts = [round(kicks[k] * FPS) for k in CUTK]
END = round(kicks[76] * FPS) + 45          # v1.0 (user): one end scene - car drives off, 3D logo rises, URL slides in; no fade to black
ORDER = ['s12_open', 's3_hl', 's4_lip', 's5_liphl', 's6_cardv2', 's7_side', 's8_cardv1', 's9_canards', 's10_end']
starts = [0] + cuts; ends = cuts + [END]
FONT = '/usr/share/fonts/opentype/inter/'
# owner font rule (knowledge/fonts.md): Akira Expanded Super Bold for headlines/offers (ASCII only - no arrows);
# Unbounded 500 for part labels, 300-400 for the URL next to the logo
UB = '/home/user/Illumaesthetic-Video-Editor/assets/fonts/unbounded/Unbounded-'
AK = '/home/user/Illumaesthetic-Video-Editor/assets/fonts/akira/AkiraExpanded-SuperBold.otf'   # owner licence (2026-11-18), gitignored
f_bf = ImageFont.truetype(AK, 38)
f_big = ImageFont.truetype(FONT + 'InterDisplay-Black.otf', 58) if os.path.exists(FONT + 'InterDisplay-Black.otf') else ImageFont.truetype(FONT + 'Inter-Black.otf', 58)
f_mid = ImageFont.truetype(FONT + 'InterDisplay-Bold.otf', 50)
f_url = ImageFont.truetype(UB + '300.ttf', 40)
TXT = (232, 236, 242)
CYAN = (111, 195, 214)
logo = Image.open(f'{M}/logo/Epsilon+ Logo.png').convert('RGBA'); logo = logo.crop(logo.getbbox())
logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


CX = 487   # centre of the gap between the skirts in the card plates (measured on s6/s8 renders)
CXT = 514  # text centre in the gap after the 0.79 plate scale (measured skirts at x 363 / 670)


def text_c(d, y, s, font, alpha, tracking=0, cx=CX):
    if tracking:
        widths = [d.textlength(ch, font=font) for ch in s]; tw = sum(widths) + tracking * (len(s) - 1); x = cx - tw / 2
        for ch, w_ in zip(s, widths):
            d.text((x, y), ch, font=font, fill=TXT + (alpha,)); x += w_ + tracking
    else:
        tw = d.textlength(s, font=font); d.text((cx - tw / 2, y), s, font=font, fill=TXT + (alpha,))


RED = (226, 38, 43)
f_ver = ImageFont.truetype(AK, 190)
f_kit = ImageFont.truetype(AK, 58)
f_pct = ImageFont.truetype(AK, 122)
f_upto = ImageFont.truetype(AK, 44)


# v0.8 (user: "why is V2 crossed out and V1? shouldn't you cross out the retail price?"): the kit name stays clean;
# each part's RETAIL price (sheet "Current Price") is slashed in red and the BF price (sheet "BF 2026 Price") follows.
PRICES = {  # projects/_blackfriday/bf_liquidation_pricing.csv (owner: use the sheet)
    's6_cardv2': [('LIP', '$285', '$199.50'), ('SKIRTS', '$400', '$280'), ('SPATS', '$175', '$122.50')],
    's8_cardv1': [('LIP', '$215', '$129'), ('CARBON LIP', '$600', '$330'), ('SKIRTS', '$275', '$165'), ('SPATS', '$125', '$75')],
}
f_row = ImageFont.truetype(UB + '500.ttf', 32)
f_old = ImageFont.truetype(UB + '400.ttf', 36)
f_new = ImageFont.truetype(AK, 42)
f_pct2 = ImageFont.truetype(AK, 96)


f_kit2 = ImageFont.truetype(AK, 46)


def card_overlay(img, shot, i, n):
    """v1.0 (owner rule: slow readers). BLACK FRIDAY stays up the whole card. Over the dark car the kit glows (no new
    text). After the lift: 'V2 KIT' / 'V1 KIT UP TO' + the offer, then one row per part - retail price slashed in red,
    BF price (sheet). Rows are fully in by ~1.2 s into the price phase and then hold >= 3 s.
    Everything inside x 48-920, y 285-1440, between the lip (top) and the skirts (bottom)."""
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    out = 1 - ease((i - (n - 5)) / 4)
    v2 = shot == 's6_cardv2'
    text_c(d, 330, 'BLACK FRIDAY', f_bf, round(255 * ease(i / 5) * out), tracking=6, cx=484)
    F1 = 65                                   # end of the lift, same as shot.py card_lineup
    t0 = F1 - 4
    a_p = ease((i - t0) / 4) * out
    if a_p > 0:
        text_c(d, 668, 'V2 KIT' if v2 else 'V1 KIT  UP TO', f_kit2, round(255 * a_p), cx=484)
        text_c(d, 724, '30% OFF' if v2 else '45% OFF', f_pct2, round(255 * a_p), cx=484)
        y_rows = 846
        for r, (name, old, new) in enumerate(PRICES[shot]):
            tr = t0 + 6 + 7 * r                       # rows stagger in
            a_r = ease((i - tr) / 4) * out
            if a_r <= 0:
                continue
            y = y_rows + 50 * r
            d.text((112, y + 6), name, font=f_row, fill=TXT + (round(215 * a_r),))
            d.text((440, y + 3), old, font=f_old, fill=(170, 174, 182, round(255 * a_r)))
            k = ease((i - (tr + 4)) / 5)              # red strike across the retail price
            if k > 0:
                wo = d.textlength(old, font=f_old)
                d.line((432, y + 26, 432 + (wo + 16) * k, y + 26), fill=RED + (round(255 * a_r),), width=7)
            a_n = ease((i - (tr + 8)) / 4) * out      # BF price after the strike
            if a_n > 0:
                d.text((618, y), new, font=f_new, fill=TXT + (round(255 * a_n),))
    img.alpha_composite(ov)


f_lab = ImageFont.truetype(UB + '500.ttf', 52)
f_eye = ImageFont.truetype(UB + '400.ttf', 30)


def label(img, i, n, lines, y, start=6, stop=None):
    """highlight callout on CGI (never on real footage): eyebrow + title, cyan accent bar, fades in/out inside the shot"""
    stop = n if stop is None else stop
    a = min(ease((i - start) / 5), 1 - ease((i - (stop - 6)) / 5))
    if a <= 0:
        return
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    eyebrow, title = lines
    if eyebrow:
        text_c(d, y, eyebrow, f_eye, round(230 * a), tracking=5, cx=484)
    text_c(d, y + 48, title, f_lab, round(255 * a), cx=484)
    tw = d.textlength(title, font=f_lab); d.rectangle((484 - tw / 2, y + 124, 484 - tw / 2 + tw * ease((i - start) / 10), y + 130), fill=CYAN + (round(255 * a),))
    img.alpha_composite(ov)


LABELS = {  # shot -> list of (eyebrow, title, y, start, stop)
    's3_hl': [('EPSILON+', 'V2 AERO KIT', 1190, 8, None)],
    's4_lip': [('V2', 'FRONT LIP', 1190, 4, 60)],          # one label held across the lip shot and its 1:1 highlight (~2.8 s readable)
    's5_liphl': [('V2', 'FRONT LIP', 1190, -12, None)],
    's7_side': [('V2', 'SIDE SKIRTS + REAR SPATS', 1190, 3, None)],   # v1.0: one label, 3.3 s readable (5 words)
    's9_canards': [('CARBON CANARDS', 'BACK IN STOCK', 1190, 3, None)],
}


def logo_frame(i, n):
    img = Image.new('RGBA', (W, H), (2, 2, 3, 255))
    a = ease(i / 8) * (1 - ease((i - (n - 30)) / 28))
    lg = logo.copy(); lg.putalpha(lg.split()[-1].point(lambda v: round(v * a)))
    img.alpha_composite(lg, (484 - lg.width // 2, 760 - lg.height // 2))
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); tw = d.textlength('WWW.EPSILON.PLUS', font=f_url)
    d.text((484 - tw / 2, 860), 'WWW.EPSILON.PLUS', font=f_url, fill=TXT + (round(200 * a),))
    img.alpha_composite(ov)
    return img


fno = 0
for shot, s0, e0 in zip(ORDER, starts, ends):
    n = e0 - s0
    for i in range(n):
        if shot == 'logo':
            img = logo_frame(i, n)
        else:
            src = f'{RC if shot in ("s6_cardv2", "s8_cardv1") else R}/{shot}/f_{i + 1:04d}.png'
            img = Image.open(src).convert('RGBA').resize((W, H), Image.LANCZOS)
            if shot in ('s6_cardv2', 's8_cardv1'):
                card_overlay(img, shot, i, n)
            for eb, tt, y, st, sp in LABELS.get(shot, []):
                label(img, i, n, (eb, tt), y, st, sp)
        img.convert('RGB').save(f'{FR}/o_{fno:04d}.png', compress_level=1); fno += 1
print('FRAMES', fno, 'cuts', cuts, 'end', END)

dur = fno / FPS
os.makedirs(os.path.dirname(args.out), exist_ok=True)
# music from the song's beginning; 1 s fade; gain set from a measured first pass to ~-14 LUFS, true peak < -1 dBFS
gain = float(os.environ.get('GAIN_DB', '0'))
af = f"atrim=0:{dur:.3f},afade=t=out:st={dur - 1.0:.3f}:d=1.0,volume={gain}dB,alimiter=limit=0.85:level=disabled"
cmd = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{FR}/o_%04d.png', '-i', f'{M}/music/electric_youth.mp3',
       '-filter_complex', f'[1:a]{af}[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
       '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-shortest', args.out]
subprocess.run(cmd, check=True); print('OUT', args.out, round(dur, 3), 's')
