"""compose.py : assemble BF gr-corolla-track v0.2 at 1080x1920/30 from the shot renders, offer cards (text over the Blender
plates; owner 2026-11-17: no Del & Eps, typical branding only), the Epsilon+ end card and the music.

python compose.py [--out ...]
Cuts are on measured kick onsets of 'Electric Youth' (music/kicks.json), windows as in shot.py WIN.
v0.2 (user): game-GLB studio shots instead of scan, V2 parts highlighted + labelled, carbon canards "BACK IN STOCK".
"""
import argparse, json, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/home/user/media/work/out/bf-gr-corolla-track_v0.6.mp4')
ap.add_argument('--tag', default='v0.6'); args = ap.parse_args()
M = '/home/user/media/bf-gr-corolla-track'; R = f'{M}/renders_v06'; RC = R; FR = f'{M}/frames_{args.tag}'; os.makedirs(FR, exist_ok=True)
W, H, FPS = 1080, 1920, 30
kicks = json.load(open(f'{M}/music/kicks.json'))
CUTK = [4, 6, 10, 12, 14, 22, 28, 36, 42, 44]   # v0.6 (user: slow readers): cards 8 kicks, side 6, canards 6
cuts = [round(kicks[k] * FPS) for k in CUTK]
END = round(kicks[50] * FPS) + 30          # logo holds 6 kicks (to kick 50), then a 1 s fade
ORDER = ['s1_hook', 's2_push', 's3_hl', 's4_lip', 's5_liphl', 's6_cardv2', 's7_side', 's8_cardv1', 's9_canards', 's10_pass', 'logo']
starts = [0] + cuts; ends = cuts + [END]
FONT = '/usr/share/fonts/opentype/inter/'
# owner font rule (knowledge/fonts.md): Akira for headlines/offers - not supplied yet, so Unbounded 700 stands in;
# Unbounded 500 for part labels, 300-400 for the URL next to the logo
UB = '/home/user/Illumaesthetic-Video-Editor/assets/fonts/unbounded/Unbounded-'
f_bf = ImageFont.truetype(UB + '700.ttf', 40)
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
f_ver = ImageFont.truetype(UB + '700.ttf', 200)
f_kit = ImageFont.truetype(UB + '700.ttf', 72)
f_pct = ImageFont.truetype(UB + '700.ttf', 134)
f_upto = ImageFont.truetype(UB + '700.ttf', 52)


def card_overlay(img, shot, i, n):
    """v0.5 (user): 'V2' / 'V1' big -> a red slash strikes through it -> the percent off punches in bigger.
    Band between the lip (top) and the skirt (bottom) of the line-up plate; all inside x 48-920, y 285-1440."""
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    out = 1 - ease((i - (n - 5)) / 4)
    ver, word = ('V2', 'KIT') if shot == 's6_cardv2' else ('V1', '')
    pct, pre = ('30% OFF', '') if shot == 's6_cardv2' else ('45% OFF', 'UP TO')
    text_c(d, 330, 'BLACK FRIDAY', f_bf, round(255 * ease(i / 5) * out), tracking=6, cx=484)
    F0, F1 = round(0.28 * n), round(0.52 * n)   # lift window, same as shot.py card_lineup
    # 1) version, big, over the car (top band); slashed; gone as the parts lift
    a_v = ease(i / 4) * (1 - ease((i - (F0 - 2)) / 5))
    if a_v > 0:
        wv = d.textlength(ver, font=f_ver); wk = d.textlength(word, font=f_kit) if word else 0; gap = 24 if word else 0
        x0 = 484 - (wv + gap + wk) / 2; y0 = 385
        d.text((x0, y0), ver, font=f_ver, fill=TXT + (round(255 * a_v),))
        if word:
            d.text((x0 + wv + gap, y0 + 128), word, font=f_kit, fill=TXT + (round(255 * a_v),))
        # 2) the slash: a thick red bar drawn lower-left -> upper-right across the version (frames 9-15)
        k = ease((i - 10) / 6)
        if k > 0:
            xa, ya, xb, yb = x0 - 30, y0 + 225, x0 + wv + gap + wk + 30, y0 + 40
            xe, ye = xa + (xb - xa) * k, ya + (yb - ya) * k
            d.line((xa, ya, xe, ye), fill=RED + (round(255 * min(1, a_v * 1.4)),), width=26)
    # 3) percent off punches in (scale 1.35 -> 1.0) from frame 20
    a_p = ease((i - (F1 - 3)) / 4) * out
    if a_p > 0:
        sc_ = 1.0 + 0.15 * (1 - ease((i - (F1 - 3)) / 5))   # small punch so the word never leaves the safe zone
        lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        if pre:
            text_c(dl, 700, pre, f_upto, round(255 * a_p), cx=484)
        text_c(dl, 770 if pre else 745, pct, f_pct, round(255 * a_p), cx=484)
        if sc_ > 1.001:
            cx_, cy_ = 484, 860; big = lay.resize((round(W * sc_), round(H * sc_)), Image.LANCZOS)
            lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); lay.alpha_composite(big, (round(cx_ - cx_ * sc_), round(cy_ - cy_ * sc_)))
        ov.alpha_composite(lay)
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
    's4_lip': [('V2', 'FRONT LIP', 1190, 4, 40)],          # v0.6: one label held across the lip shot and its 1:1 highlight (~1.8 s)
    's5_liphl': [('V2', 'FRONT LIP', 1190, -12, None)],
    's7_side': [('V2', 'SIDE SKIRTS', 1190, 3, 44), ('V2', 'REAR SPATS', 1190, 44, None)],
    's9_canards': [('CARBON CANARDS', 'BACK IN STOCK', 1190, 8, None)],
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
