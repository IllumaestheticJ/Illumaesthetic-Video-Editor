"""compose.py : assemble BF gr-corolla-track v0 at 1080x1920/30 from the shot renders, offer cards (text over the Blender
plates; owner 2026-11-17: no Del & Eps, typical branding only), the Epsilon+ end card and the music.

python compose.py [--out /home/user/media/work/out/bf-gr-corolla-track_v0.mp4]
Cuts are on measured kick onsets of 'Electric Youth' (music/kicks.json): kicks 4,6,10,12,14,18,22,26,30 ->
frames 59,87,144,172,201,258,315,371,428 (round(t*30)); the first clip is one frame short of kick 4 by construction.
"""
import argparse, json, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/home/user/media/work/out/bf-gr-corolla-track_v0.1.mp4')
ap.add_argument('--tag', default='v0.1'); args = ap.parse_args()
M = '/home/user/media/bf-gr-corolla-track'; R = f'{M}/renders_v0'; FR = f'{M}/frames_{args.tag}'; os.makedirs(FR, exist_ok=True)
W, H, FPS = 1080, 1920, 30
kicks = json.load(open(f'{M}/music/kicks.json'))
CUTK = [4, 6, 10, 12, 14, 18, 22, 26, 30]
cuts = [round(kicks[k] * FPS) for k in CUTK]
END = round(kicks[36] * FPS) + 30          # logo holds to kick 36, then a 1 s fade
ORDER = ['s1_hook', 's2_push', 's3_scan', 's4_lip', 's5_lipscan', 's6_cardv2', 's7_side', 's8_cardv1', 's9_pass', 'logo']
starts = [0] + cuts; ends = cuts + [END]
FONT = '/usr/share/fonts/opentype/inter/'
f_bf = ImageFont.truetype(FONT + 'InterDisplay-Bold.otf', 36)
f_big = ImageFont.truetype(FONT + 'InterDisplay-Black.otf', 76) if os.path.exists(FONT + 'InterDisplay-Black.otf') else ImageFont.truetype(FONT + 'Inter-Black.otf', 76)
f_mid = ImageFont.truetype(FONT + 'InterDisplay-Bold.otf', 60)
f_url = ImageFont.truetype(FONT + 'InterDisplay-Medium.otf', 44)
TXT = (232, 236, 242)
CYAN = (111, 195, 214)
logo = Image.open(f'{M}/logo/Epsilon+ Logo.png').convert('RGBA'); logo = logo.crop(logo.getbbox())
logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


CX = 487   # centre of the gap between the skirts in the card plates (measured on s6/s8 renders)


def text_c(d, y, s, font, alpha, tracking=0, cx=CX):
    if tracking:
        widths = [d.textlength(ch, font=font) for ch in s]; tw = sum(widths) + tracking * (len(s) - 1); x = cx - tw / 2
        for ch, w_ in zip(s, widths):
            d.text((x, y), ch, font=font, fill=TXT + (alpha,)); x += w_ + tracking
    else:
        tw = d.textlength(s, font=font); d.text((cx - tw / 2, y), s, font=font, fill=TXT + (alpha,))


def card_overlay(img, shot, i, n):
    d = ImageDraw.Draw(img)
    a_in = ease(i / 6); a_out = 1 - ease((i - (n - 6)) / 5); al = round(255 * min(a_in, a_out))
    if shot == 's6_cardv2':
        text_c(d, 770, 'BLACK FRIDAY', f_bf, al, tracking=6)
        text_c(d, 838, 'V2 KIT', f_mid, al)
        text_c(d, 925, '30% OFF', f_big, al)
    else:
        text_c(d, 770, 'BLACK FRIDAY', f_bf, al, tracking=6)
        text_c(d, 838, 'V1 UP TO', f_mid, al)
        text_c(d, 925, '45% OFF', f_big, al)


def logo_frame(i, n):
    img = Image.new('RGBA', (W, H), (2, 2, 3, 255))
    a = ease(i / 8) * (1 - ease((i - (n - 30)) / 28))
    lg = logo.copy(); lg.putalpha(lg.split()[-1].point(lambda v: round(v * a)))
    img.alpha_composite(lg, ((W - lg.width) // 2, 880 - lg.height // 2))
    d = ImageDraw.Draw(img); tw = d.textlength('EPSILON.PLUS', font=f_url)
    d.text(((W - tw) / 2, 1010), 'EPSILON.PLUS', font=f_url, fill=TXT + (round(200 * a),))
    return img


fno = 0
for shot, s0, e0 in zip(ORDER, starts, ends):
    n = e0 - s0
    for i in range(n):
        if shot == 'logo':
            img = logo_frame(i, n)
        else:
            src = f'{R}/{shot}/f_{i + 1:04d}.png'
            img = Image.open(src).convert('RGBA').resize((W, H), Image.LANCZOS)
            if shot in ('s6_cardv2', 's8_cardv1'):
                card_overlay(img, shot, i, n)
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
