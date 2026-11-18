"""compose.py : assemble BF10 turkey-crossing at 1080x1920/30 from the Blender shot renders, the impact flash, the sale
text (Akira Expanded), the Epsilon+ end card (wordmark 720 px + WWW.EPSILON.PLUS in Unbounded 300) and the music.

python compose.py [--tag v0] [--renders DIR]
Cuts (global frames, measured hits of PhonkFlux 'TRANSFORMATION', video t0 = track 10.812 s):
  0 | 55 (12.650) | 108 (14.419) | 135 (15.322) | 162 (16.227 DROP, impact) | 216 (18.023, text over half-speed feathers) | 324 (21.630 logo) | end 420
Text: v0 default 'BLACK FRIDAY' (18.023) + 'SALE' (18.929, f243); no numbers (owner to choose the offer lines).
All text/logos inside x 48-920, y 285-1440 (knowledge/safe-zones.md); boxes exported for scripts/safezone_check.py.
"""
import argparse, json, os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser(); ap.add_argument('--tag', default='v0')
ap.add_argument('--renders', default='/home/user/media/bf-turkey-crossing/renders_v0'); args = ap.parse_args()
M = '/home/user/media/bf-turkey-crossing'; R = args.renders; FR = f'{M}/frames_{args.tag}'; os.makedirs(FR, exist_ok=True)
OUT = f'/home/user/media/work/out/bf-turkey-crossing_{args.tag}.mp4'
REPO = '/home/user/Illumaesthetic-Video-Editor'
W, H, FPS = 1080, 1920, 30
MUSIC = f'{M}/music/transformation.mp3'; T0 = 10.812
SHOTS = [('s1_cross', 0, 55), ('s2_look', 55, 108), ('s3_car', 108, 135), ('s4_eyes', 135, 162), ('s5_poof', 162, 216),
         ('s6_feath', 216, 445)]   # half-speed feather fall under the text (owner slow-reader rule)
LOGO_IN, END = 366, 445   # v0.4 (owner): logo + URL join the sale text in the same scene on the 22.982 hit; fade from the 25.239 hit (f433)
LOGO0 = END              # no separate black logo card any more
AK = f'{REPO}/assets/fonts/akira/AkiraExpanded-SuperBold.otf'   # owner licence, gitignored
UB = f'{REPO}/assets/fonts/unbounded/Unbounded-'
CX = 484                 # centre of the safe band x 48-920
TXT = (246, 246, 242)
RED = (226, 38, 43)


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def eout(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3


def fit(text, font_path, max_w, start):
    s = start
    while s > 10:
        f = ImageFont.truetype(font_path, s)
        if f.getlength(text) <= max_w:
            return f
        s -= 2
    return ImageFont.truetype(font_path, s)


boxes = []


def slam(img, text, font, cy, t, color=TXT, label='', key=True, f0=0):
    """Text slams in: 1.45x -> 1.0 over 4 frames with a short shake; drawn on its own layer with a dark drop shadow."""
    if t < 0:
        return
    k = eout(t / 4); sc = 1.45 - 0.45 * k; a = min(1.0, t / 2)
    bb = font.getbbox(text); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    lay = Image.new('RGBA', (tw + 80, th + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    sh = Image.new('RGBA', lay.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((40 - bb[0] + 6, 40 - bb[1] + 8), text, font=font, fill=(0, 0, 0, 200)); sh = sh.filter(ImageFilter.GaussianBlur(8))
    lay = Image.alpha_composite(sh, lay); d = ImageDraw.Draw(lay)
    d.text((40 - bb[0], 40 - bb[1]), text, font=font, fill=color + (255,))
    if sc != 1.0:
        lay = lay.resize((round(lay.width * sc), round(lay.height * sc)), Image.LANCZOS)
    if a < 1:
        al = lay.getchannel('A').point(lambda v: round(v * a)); lay.putalpha(al)
    jx = round(10 * math.sin(t * 2.6) * math.exp(-t / 2.5)) if t < 8 else 0
    x = round(CX - lay.width / 2) + jx; y = round(cy - lay.height / 2)
    img.alpha_composite(lay, (x, y))
    if t == 6 and not any(b['label'] == label for b in boxes):
        boxes.append(dict(label=label, key=key, x=CX - tw / 2, y=cy - th / 2, w=tw, h=th))


def plate(f):
    for s, a, b in SHOTS:
        if a <= f < b:
            p = f'{R}/{s}/f_{f:04d}.png'
            im = Image.open(p).convert('RGB').resize((W, H), Image.LANCZOS)
            return im.convert('RGBA')
    return Image.new('RGBA', (W, H), (0, 0, 0, 255))


logo = Image.open(f'{M}/logo/Epsilon+ Logo.png').convert('RGBA'); logo = logo.crop(logo.getbbox())
logo = logo.resize((720, round(logo.height * 720 / logo.width)), Image.LANCZOS)
f_bf = fit('FRIDAY', AK, 840, 200)
f_sale = fit('SALE', AK, 760, 260)
f_url = ImageFont.truetype(UB + '300.ttf', 44)
CARD_B = 311            # 21.181
UNTIL = os.environ.get('BF_UNTIL', 'UNTIL NOV 30')   # owner 2026-11-18: the sale ends Nov 30
f_wish = ImageFont.truetype(UB + '500.ttf', 50)
f_tg = fit('THANKSGIVING', AK, 840, 200)
f_until = fit(UNTIL, UB + '500.ttf', 820, 64)
# darkening gradient for the text plate (light sky behind white text)
grad = Image.new('L', (1, H))
for y in range(H):
    v = 150 * (1 - ease((y - 260) / 900)) if y > 260 else 150
    grad.putpixel((0, y), round(v))
grad = grad.resize((W, H)); shade = Image.new('RGBA', (W, H), (8, 6, 12, 255)); shade.putalpha(grad)

for f in range(END):
    if f < LOGO0:
        img = plate(f)
        # impact: 2 white frames on the drop, then a fast decay
        if 162 <= f < 168:
            k = 1.0 if f < 164 else 1 - (f - 163) / 5
            wl = Image.new('RGBA', (W, H), (255, 255, 255, round(255 * k))); img = Image.alpha_composite(img, wl)
        if f >= 216:
            t = f - 216
            sh = shade.copy(); sh.putalpha(grad.point(lambda v: round(v * ease(t / 3)))); img = Image.alpha_composite(img, sh)
            if f < CARD_B:      # card A: the owner's greeting (18.023 -> 21.181)
                ta = min(1.0, t / 4); d = ImageDraw.Draw(img); s0 = 'WISHING OUR DRIVERS A'; tw = d.textlength(s0, font=f_wish)
                sh0 = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh0).text((CX - tw / 2 + 4, 405), s0, font=f_wish, fill=(0, 0, 0, round(200 * ta)))
                img.alpha_composite(sh0.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(img)
                d.text((CX - tw / 2, 400), s0, font=f_wish, fill=TXT + (round(255 * ta),))
                if t == 6:
                    bb = f_wish.getbbox(s0); boxes.append(dict(label='WISHING', key=True, x=CX - tw / 2, y=400 + bb[1], w=tw, h=bb[3] - bb[1]))
                slam(img, 'HAPPY', f_tg, 560, t - 2, label='HAPPY')
                slam(img, 'THANKSGIVING', f_tg, 690, t - 4, label='THANKSGIVING')
            else:               # card B: sale (21.181 -> 25.239); SALE on 21.630, UNTIL on 22.091
                tb_ = f - CARD_B
                slam(img, 'BLACK', f_bf, 400, tb_, label='BLACK')
                slam(img, 'FRIDAY', f_bf, 570, tb_ - 2, label='FRIDAY')
                slam(img, 'SALE', f_sale, 780, f - 324, color=RED, label='SALE')
                slam(img, UNTIL, f_until, 960, f - 338, color=(255, 214, 90), label='UNTIL')
                tl = f - LOGO_IN   # Epsilon+ wordmark (720 px) + WWW.EPSILON.PLUS (Unbounded 300) in the same scene
                if tl >= 0:
                    a = min(1.0, tl / 4)
                    band = Image.new('L', (1, H))
                    for y in range(H):
                        band.putpixel((0, y), round(170 * a * max(0.0, 1 - abs(y - 1250) / 230)))
                    dk = Image.new('RGBA', (W, H), (8, 6, 12, 255)); dk.putalpha(band.resize((W, H))); img.alpha_composite(dk)
                    k = eout(tl / 6); lg = logo.resize((round(720 * (0.92 + 0.08 * k)), round(logo.height * (0.92 + 0.08 * k))), Image.LANCZOS)
                    lg.putalpha(lg.getchannel('A').point(lambda v: round(v * a)))
                    ly = 1200; img.alpha_composite(lg, (round(CX - lg.width / 2), round(ly - lg.height / 2)))
                    d = ImageDraw.Draw(img); s_ = 'WWW.EPSILON.PLUS'; tw = d.textlength(s_, font=f_url)
                    d.text((CX - tw / 2, 1290), s_, font=f_url, fill=(232, 236, 242, round(255 * a)))
                    if tl == 6:
                        boxes.append(dict(label='logo', key=True, x=CX - 360, y=ly - logo.height / 2, w=720, h=logo.height))
                        bb = f_url.getbbox(s_); boxes.append(dict(label='url', key=True, x=CX - tw / 2, y=1290 + bb[1], w=tw, h=bb[3] - bb[1]))
            if f > END - 12:
                img = Image.alpha_composite(img, Image.new('RGBA', (W, H), (0, 0, 0, round(255 * (f - (END - 12)) / 12))))
    else:
        img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); t = f - LOGO0
        k = eout(t / 6); lg = logo.resize((round(720 * (0.92 + 0.08 * k)), round(logo.height * (0.92 + 0.08 * k))), Image.LANCZOS)
        lg.putalpha(lg.getchannel('A').point(lambda v: round(v * min(1, t / 4))))
        ly = 760; img.alpha_composite(lg, (round(CX - lg.width / 2), round(ly - lg.height / 2)))
        if t == 6:
            boxes.append(dict(label='logo', key=True, x=CX - 360, y=ly - logo.height / 2, w=720, h=logo.height))
        tu = f - 439   # URL 6 frames after the logo lands
        if tu >= 0:
            d = ImageDraw.Draw(img); s = 'WWW.EPSILON.PLUS'; tw = d.textlength(s, font=f_url)
            d.text((CX - tw / 2, 900), s, font=f_url, fill=(232, 236, 242, round(255 * min(1, tu / 4))))
            if tu == 6:
                bb = f_url.getbbox(s); boxes.append(dict(label='url', key=True, x=CX - tw / 2, y=900 + bb[1], w=tw, h=bb[3] - bb[1]))
        if f > END - 12:
            img = Image.alpha_composite(img, Image.new('RGBA', (W, H), (0, 0, 0, round(255 * (f - (END - 12)) / 12))))
    img.convert('RGB').save(f'{FR}/f_{f:04d}.jpg', quality=93)

# text boxes with their on-screen windows (for scripts/safezone_check.py)
tb = []
for b in boxes:
    t0 = {'WISHING': 216, 'HAPPY': 218, 'THANKSGIVING': 220, 'BLACK': 311, 'FRIDAY': 313, 'SALE': 324, 'UNTIL': 338, 'logo': 366, 'url': 366}[b['label']] / FPS
    t1 = (CARD_B if b['label'] in ('WISHING', 'HAPPY', 'THANKSGIVING') else LOGO0 if b['label'] in ('BLACK', 'FRIDAY', 'SALE', 'UNTIL') else END) / FPS
    tb.append(dict(t0=round(t0, 3), t1=round(t1, 3), x=round(b['x']), y=round(b['y']), w=round(b['w']), h=round(b['h']), label=b['label'], key=b['key']))
json.dump(tb, open(f'{M}/text_boxes_{args.tag}.json', 'w'), indent=1)

# audio: the track from T0, fade the tail, loudness to -14 LUFS / TP < -1 dBFS (two-pass loudnorm)
dur = END / FPS
raw = f'{M}/music/cut_{args.tag}.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{T0}', '-t', f'{dur:.3f}', '-i', MUSIC, '-af', f'afade=t=out:st={dur - 0.8:.3f}:d=0.8',
                '-ar', '48000', raw], check=True)
m = subprocess.run(['ffmpeg', '-v', 'info', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                   capture_output=True, text=True).stderr
js = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
      f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{FR}/f_%04d.jpg', '-i', raw, '-af', ln + ',aresample=48000',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', '-c:a', 'aac', '-b:a', '256k', '-shortest',
                '-movflags', '+faststart', OUT], check=True)
print('WROTE', OUT)
