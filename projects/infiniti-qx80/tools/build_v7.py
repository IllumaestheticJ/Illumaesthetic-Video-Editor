"""Infiniti QX80 R-Spec v7 = v6 + reviewer notes (2026-11-14): theme in the illumaesthetic.com colours/type (bg #0b0c0b,
accent green #619f73, text #f2f3f1, Fjalla One headings with 0.15 em tracking, green monospace eyebrows - read from the
live site's CSS variables), floating motoIQ vent fixed (kitgroups.py FIX), kit in site green, GT-R BRAKES section (scanned
GT-R caliper + rotor ring with our CAD hat + caliper adapter, K_brakes) and the GT-R brakes on the car in the final render.
Timeline: scan day 3 -> 2 stills, concepts 8 -> 6 beats (12 images), brakes 6 beats before the final render; drop unchanged.

v6 notes: Sentra v6 build-story structure (knowledge/short-form.md, approved on the Sentra reel):
hook (one real article, full frame, 3 % push) -> answer card 'HERE'S HOW.' -> scan day -> 3D SCAN -> CONCEPTS -> NEW BODY PANELS
-> FINAL RENDER 360 (wrap sweep, Ecky's wheels/grille/T-spec lights, ends on the solved camera of photo 1702) -> 1:1 cut to the
real car ON THE DROP with cropped real headlines landing one per beat -> finished-car photos -> logo (all caps wordmark only).
Music: deadmau5 - Ghosts 'n' Stuff (Original Instrumental Mix), TikTok CML song_clip_id 6739936808198473729, 128.0 BPM;
video t0 = track 15.019 (kick); breakdown 30.02; DROP kick 45.019 = video 30.000 (beat 64).
"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

D = '/home/user/media/infiniti-qx80'; SEG = D + '/seg_v7'; os.makedirs(SEG, exist_ok=True)
WA = D + '/whatsapp/x'; EK = D + '/ecky'; PRESS = D + '/press'; R = D + '/renders/final'
# v7b (user: "reuse one of the songs in moosic folder, i dont like this song"): KMFDM - Megalomaniac from Dropbox /Moosic
# (also used on the Mazda Miata ND reel). Measured here (30-150 Hz attack): kick entry 15.52 s, riser ~42 s, drop 45.515 s
# = 64 beats of the 128.05 BPM kick grid -> video t0 = 15.52, drop on video 30.000 (the 1:1 cut), same structure as before.
MUSIC = '/home/user/media/work/music/megalomaniac.wav'; MUSIC_START = 15.52
LOGO = '/home/user/Illumaesthetic-Video-Editor/remotion/public/illumaesthetic_logo.png'
FPS, WD, HT = 30, 1080, 1920
ENC = ['-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-an']
F = lambda name, size: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/{name}.otf', size)
FONTS = '/home/user/media/work/fonts'   # Google Fonts TTFs (not in git): Fjalla One, Barlow - the site's --typeHeaderPrimary/--typeBasePrimary
HEAD = lambda size: ImageFont.truetype(f'{FONTS}/FjallaOne.ttf', size)
BODY = lambda size: ImageFont.truetype(f'{FONTS}/Barlowwght600.ttf', size)
MONO = lambda size: ImageFont.truetype('/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf', size)
# illumaesthetic.com :root (--ia-bg, --ia-accent, --ia-text, --ia-muted)
BG = (11, 12, 11); GREEN = (97, 159, 115); OFF = (242, 243, 241); MUTED = (167, 172, 166); RED = GREEN


def tracked(d, xy, text, font, fill, em=0.15, shadow=False):
    """Draw text with letter-spacing (CSS letter-spacing in em, like the site's 0.15em headings); returns the width."""
    x, y = xy; sp = font.size * em
    for ch in text:
        if shadow: d.text((x + 3, y + 3), ch, font=font, fill=(0, 0, 0))
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + sp
    return x - xy[0] - sp


def tracked_w(d, text, font, em=0.15):
    return sum(d.textlength(ch, font=font) for ch in text) + font.size * em * (len(text) - 1)


def lift(fr):
    """Render black (~7,7,9) -> site bg #0b0c0b: out = px + (BG - px) * (1 - px/255)^4 (only touches the darkest tones)."""
    f = fr.astype(np.float32); w = (1 - f / 255.0) ** 4
    return np.clip(f + (np.array(BG, np.float32) - f) * w, 0, 255).astype(np.uint8)

# cut frames = round(video t * 30) on the beat grid (direction.md v4 scene list)
BEAT = 60 / 128.05   # Megalomaniac kick grid; cut frames = round(beat * BEAT * 30)
# v7d (user: "0:36 shot feels held a little too long ... use online photos for more professional shots"): reveal 16 -> 8 beats;
# the shop phone photos after it -> the SEMA 2025 press gallery from Motor Illustrated (1920x1080), one per 4 beats.
_B = [0, 8, 12, 16, 20, 28, 34, 42, 48, 64, 72, 76, 80, 84, 88, 92, 96, 104]
_N = ['a_hook', 'b_answer', 'c1_scanday', 'c2_scanday', 'd_scan', 'e_concepts', 'f_panels', 'k_brakes', 'g_final360',
      'h_reveal', 'p1_press', 'p2_press', 'p3_press', 'p4_press', 'p5_press', 'p6_press', 'j_logo']
_F = [round(b * BEAT * 30) for b in _B]
CUTS = {n: _F[i + 1] - _F[i] for i, n in enumerate(_N)}
PHOTO_TOP = (HT - 810) // 2   # 1702 (4032x3024) shown full width 1080x810, centred; the final render ends on its solved camera


def pipe(name, frames):
    out = f'{SEG}/{name}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-'] + ENC + [out],
                         stdin=subprocess.PIPE)
    n = 0
    for im in frames:
        p.stdin.write(im.convert('RGB').tobytes()); n += 1
    p.stdin.close(); p.wait()
    assert n == CUTS[name], (name, n, CUTS[name])
    print(name, n, 'frames')


def wa(num):
    return glob.glob(f'{WA}/{num:08d}-PHOTO-*.jpg')[0]


def load(path):
    return ImageOps.exif_transpose(Image.open(path)).convert('RGB')


def blur_bg(src):
    a = src.width / src.height
    bg = src.resize((int(HT * a) + 1, HT)).crop((int(HT * a - WD) // 2, 0, int(HT * a - WD) // 2 + WD, HT)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.eval(bg, lambda v: int(v * 0.30))
    return Image.blend(bg, Image.new('RGB', bg.size, BG), 0.35)


def section_label(im, title, sub=None, y=300):
    """Site pattern: green monospace eyebrow (caps, tracked) above a Fjalla One title (caps, 0.15 em), left aligned."""
    d = ImageDraw.Draw(im)
    if sub:
        sz = 33
        while tracked_w(d, sub.upper(), MONO(sz), 0.16) > WD - 74 - 60: sz -= 1   # never clip at the frame edge
        tracked(d, (74, y - 50), sub.upper(), MONO(sz), GREEN, em=0.16, shadow=True)
    tracked(d, (72, y), title.upper(), HEAD(92), OFF, em=0.06, shadow=True)


def photo_frame(path, title=None, sub=None, max_w=1.0, max_h=0.74):
    """Whole photo, static, centred in the lower part of the frame on its own blurred fill; label band above it."""
    src = load(path); a = src.width / src.height
    pw = int(WD * max_w); ph = int(pw / a)
    if ph > HT * max_h: ph = int(HT * max_h); pw = int(ph * a)
    im = blur_bg(src); p = src.resize((pw, ph), Image.LANCZOS)
    top = max(520, (HT - ph) // 2 + 120) if title else (HT - ph) // 2
    top = min(top, HT - ph - 40)
    im.paste(p, ((WD - pw) // 2, top))
    if title: section_label(im, title, sub, y=max(120, top - 230))
    return im


def hold(name, im):
    pipe(name, (im for _ in range(CUTS[name])))


# ---------------- A: hook - finished car + cropped real headlines stacking, one per 2 beats ----------------
def seg_hook():
    top = load(wa(1701)); a = top.width / top.height; ph = int(WD / a)
    base = Image.new('RGB', (WD, HT), BG); base.paste(top.resize((WD, ph), Image.LANCZOS), (0, 60))
    P = lambda n: Image.open(f'{PRESS}/{n}.png').convert('RGB')
    strips = [('CARSCOOPS  ·  OCT 21, 2025', P('carscoops_teaser_headline').crop((0, 150, 1080, 515))),
              ('MOTOR ILLUSTRATED  ·  OCT 27, 2025', P('motorillustrated_headline').crop((0, 225, 1080, 455))),
              ('CARSCOOPS  ·  OCT 27, 2025', P('carscoops_headline').crop((0, 235, 1080, 515)))]
    CW = 940; x0 = (WD - CW) // 2; tagf = F('Inter-Bold', 28); cards = []; y = 0
    for tag, im in strips:
        h = int(im.height * CW / im.width); cards.append((tag, im.resize((CW, h), Image.LANCZOS), y)); y += h + 64
    y0 = 60 + ph + 70
    appear = [round(b * BEAT * 30) for b in (2, 5, 8)]   # kicks at beats 2 / 5 / 8
    def gen():
        for f in range(CUTS['a_hook']):
            im = base.copy(); d = ImageDraw.Draw(im)
            for k, (tag, c, cy) in enumerate(cards):
                if f < appear[k]: continue
                u = min(1.0, (f - appear[k] + 1) / 4); dy = int((1 - u) * 50)
                d.rectangle([x0, y0 + cy + dy - 30, x0 + 40, y0 + cy + dy - 25], fill=RED)
                d.text((x0 + 52, y0 + cy + dy - 44), tag, font=tagf, fill=OFF)
                im.paste(c, (x0, y0 + cy + dy))
            yield im
    pipe('a_hook', gen())


# ---------------- scan / kit renders ----------------
def render_seq(name, n_out, fps_in=15, start=1):
    tmp = f'{SEG}/_{name}_raw.mp4'
    vf = f'scale={WD}:{HT}:flags=lanczos' + (',minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1' if fps_in < 20 else ',fps=30')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps_in), '-start_number', str(start), '-i', f'{R}/{name}/f_%04d.png', '-vf', vf,
                    '-frames:v', str(n_out)] + ENC + [tmp], check=True)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', tmp, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, HT, WD, 3)
    assert len(fr) >= n_out, (name, len(fr), n_out)
    return fr


def labelled(name, src, n_out, labels, fps_in=15):
    """labels: [(f0, f1, title, sub)] in output frames; drawn in the clear black above the car."""
    fr = render_seq(src, n_out, fps_in)
    def gen():
        for f in range(n_out):
            im = Image.fromarray(lift(fr[f]))
            for f0, f1, t, s in labels:
                if f0 <= f < f1: section_label(im, t, s, y=300)
            yield im
    pipe(name, gen())


# ---------------- C: concepts flipbook - Ecky's renders + WhatsApp iterations, chronological, whole frames ----------------
CONCEPTS = [('wa', 109), ('wa', 166), ('wa', 241), ('wa', 326),   # one per beat (12 beats)
            ('ek', 'Render/2.png'), ('ek', 'Render/5.png'), ('ek', 'Presentation_Render/1.png'), ('ek', 'Presentation_Render/7.png'),
            ('ek', 'Presentation_Render/9.png'), ('ek', 'Presentation_Render/11.png'), ('wa', 595), ('wa', 870)]


def seg_concepts():
    n = CUTS['c_concepts']; k = len(CONCEPTS); edges = [round(i * n / k) for i in range(k + 1)]
    def gen():
        for i, (kind, ref) in enumerate(CONCEPTS):
            path = wa(ref) if kind == 'wa' else f'{EK}/{ref}'
            im = photo_frame(path, 'CONCEPTS', 'design iterations, May - Aug 2025', max_w=1.0, max_h=0.6)
            for _ in range(edges[i + 1] - edges[i]): yield im
    pipe('c_concepts', gen())


# ---------------- end card ----------------
def seg_end():
    logo = Image.open(LOGO).convert('RGBA'); bb = logo.getbbox(); logo = logo.crop(bb)
    lw = 720; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    n = CUTS['h_end']
    def gen():
        for f in range(n):
            al = min(1.0, f / 8) * min(1.0, (n - 1 - f) / 12 + 0.0001) if f > n - 13 else min(1.0, f / 8)
            im = Image.new('RGB', (WD, HT), BG); d = ImageDraw.Draw(im)
            l = logo.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * al))); y = 820
            im.paste(l, ((WD - lw) // 2, y), l)
            a2 = max(0.0, min(1.0, (f - 10) / 8)) * (al if f > n - 13 else 1)
            fnt = F('InterDisplay-Medium', 54); t = 'Customize everything'
            d.text(((WD - d.textlength(t, font=fnt)) // 2, y + logo.height + 70), t, font=fnt, fill=tuple(int(v * a2) for v in OFF))
            yield im
    pipe('h_end', gen())


HOOK_LINES = [("NISSAN BROKE", OFF), ("THE INTERNET", OFF), ("FOR A WEEK", GREEN), ("IN 2025.", GREEN)]   # user copy (v7e)


def seg_hook():
    """One real article, full frame, slow 3 % push (Sentra v6 hook). v7e (user): title card "Nissan broke the internet for a
    week in 2025" over the article text - site hero style on a dark panel over the body copy, one line per kick (beats 0-3)."""
    src = Image.open(f'{PRESS}/carscoops_page.png').convert('RGB').resize((WD, HT), Image.LANCZOS); n = CUTS['a_hook']
    f0 = HEAD(10); size = 150
    probe = ImageDraw.Draw(src)
    while max(tracked_w(probe, t, HEAD(size), 0.04) for t, _ in HOOK_LINES) > WD - 140: size -= 4
    f0 = HEAD(size); lh = int(size * 1.06); y0 = HT - 140 - lh * len(HOOK_LINES); top = y0 - 70
    land = [round(b * BEAT * 30) for b in range(len(HOOK_LINES))]
    def gen():
        for f in range(n):
            z = 1.0 + 0.03 * f / (n - 1); cw, ch = int(WD / z), int(HT / z)
            im = src.crop(((WD - cw) // 2, (HT - ch) // 2, (WD + cw) // 2, (HT + ch) // 2)).resize((WD, HT), Image.BICUBIC)
            ov = Image.new('RGBA', (WD, HT), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            for yy in range(top - 160, HT):                               # dark panel over the article body, soft top edge
                al = int(255 * min(1.0, max(0.0, (yy - (top - 160)) / 160)))
                od.line([(0, yy), (WD, yy)], fill=(*BG, al))
            im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); d = ImageDraw.Draw(im)
            for k, (t, c) in enumerate(HOOK_LINES):
                if f < land[k]: continue
                u = min(1.0, (f - land[k] + 1) / 4); dy = int((1 - u) * 40)
                tracked(d, (70, y0 + k * lh + dy), t, f0, c, em=0.04)
            yield im
    pipe('a_hook', gen())


def seg_answer():
    im = Image.new('RGB', (WD, HT), BG); d = ImageDraw.Draw(im); size = 230
    while tracked_w(d, "HERE'S", HEAD(size), 0.06) > 900: size -= 4
    f = HEAD(size); lh = int(size * 1.08); y = HT // 2 - lh
    for i, (t, c) in enumerate((("HERE'S", OFF), ("HOW.", GREEN))):
        w = tracked_w(d, t, f, 0.06); tracked(d, ((WD - w) // 2, y + i * lh), t, f, c, em=0.06)
    hold('b_answer', im)


CONCEPTS6 = [('wa', 109), ('wa', 135), ('wa', 166), ('wa', 216), ('wa', 241), ('wa', 249), ('wa', 257), ('wa', 326), ('wa', 360),
             ('wa', 375), ('wa', 395), ('ek', 'Render/2.png'), ('ek', 'Render/1.png'), ('ek', 'Render/5.png'), ('ek', 'Presentation_Render/1.png'),
             ('ek', 'Presentation_Render/2.png'), ('ek', 'Presentation_Render/7.png'), ('ek', 'Presentation_Render/9.png'),
             ('ek', 'Presentation_Render/11.png'), ('wa', 543), ('wa', 595), ('wa', 870)]


# v7: 6 beats -> 12 images (~7 frames each); chronological, WhatsApp iterations then the designer's renders
CONCEPTS7 = [('wa', 109), ('wa', 166), ('wa', 241), ('wa', 326), ('wa', 375), ('ek', 'Render/2.png'), ('ek', 'Render/5.png'),
             ('ek', 'Presentation_Render/1.png'), ('ek', 'Presentation_Render/7.png'), ('ek', 'Presentation_Render/11.png'),
             ('wa', 595), ('wa', 870)]


def seg_concepts6():
    n = CUTS['e_concepts']; k = len(CONCEPTS7); edges = [round(i * n / k) for i in range(k + 1)]
    def gen():
        for i, (kind, ref) in enumerate(CONCEPTS7):
            path = wa(ref) if kind == 'wa' else f'{EK}/{ref}'
            im = photo_frame(path, 'CONCEPTS', 'design iterations, May - Aug 2025', max_w=1.0, max_h=0.6)
            for _ in range(edges[i + 1] - edges[i]): yield im
    pipe('e_concepts', gen())


def seg_reveal():
    """1:1 cut from the final render (solved camera of 1702) to the real car ON THE DROP; cropped real headlines land around
    the photo one per beat from beat 2, in the fill bands (never on the photo)."""
    src = load(wa(1702)); im0 = blur_bg(src); ph = 810; im0.paste(src.resize((WD, ph), Image.LANCZOS), (0, PHOTO_TOP))
    P = lambda nm: Image.open(f'{PRESS}/{nm}.png').convert('RGB')
    cards = [('CARSCOOPS', P('carscoops_headline').crop((0, 235, 1080, 515)), 'top'),
             ('MOTOR ILLUSTRATED', P('motorillustrated_headline').crop((0, 225, 1080, 455)), 'top'),
             ('CARSCOOPS', P('carscoops_teaser_headline').crop((0, 150, 1080, 515)), 'bottom')]
    CW = 960; x0 = (WD - CW) // 2; tagf = MONO(28); placed = []
    y_top = 70
    for tag, c, band in cards:
        h = int(c.height * CW / c.width); c = c.resize((CW, h), Image.LANCZOS)
        if band == 'top': y = y_top; y_top += h + 58
        else: y = PHOTO_TOP + ph + 70
        placed.append((tag, c, y))
    beat = BEAT * 30; appear = [round(b * beat) for b in (2, 3, 4)]
    def gen():
        for f in range(CUTS['h_reveal']):
            im = im0.copy(); d = ImageDraw.Draw(im)
            for k, (tag, c, y) in enumerate(placed):
                if f < appear[k]: continue
                u = min(1.0, (f - appear[k] + 1) / 4); dy = int((1 - u) * 50)
                tracked(d, (x0, y + dy - 46), tag, tagf, GREEN, em=0.18)
                im.paste(c, (x0, y + dy))
            yield im
    pipe('h_reveal', gen())


MOTOIQ = D + '/logo/motoiq/motoiq_white.png'   # v7e: wordmark rasterised from Ecky's Print__Nismo_QX80_motoiq_logo.stl


def seg_logo():
    """ILLUMAESTHETIC wordmark, a thin green x, the motoiq wordmark (user v7e: "needs a MotoIQ logo")."""
    logo = Image.open(LOGO).convert('RGBA'); logo = logo.crop(logo.getbbox())
    lw = 720; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS); n = CUTS['j_logo']
    mq = Image.open(MOTOIQ).convert('RGBA'); mw = 470; mq = mq.resize((mw, int(mw * mq.height / mq.width)), Image.LANCZOS)
    gap = 70; xs = 46; total = logo.height + gap + xs + gap + mq.height; y0 = (HT - total) // 2
    def gen():
        for f in range(n):
            al = min(1.0, f / 8, (n - 1 - f) / 20 + 0.05); a2 = max(0.0, min(1.0, (f - 6) / 8)) * min(1.0, (n - 1 - f) / 20 + 0.05)
            im = Image.new('RGB', (WD, HT), BG)
            for img, y, a in ((logo, y0, al), (mq, y0 + logo.height + 2 * gap + xs, a2)):
                l = img.copy(); l.putalpha(l.getchannel('A').point(lambda v, a=a: int(v * a))); im.paste(l, ((WD - img.width) // 2, y), l)
            d = ImageDraw.Draw(im); cx, cy = WD // 2, y0 + logo.height + gap + xs // 2; h = xs // 2
            col = tuple(int(BG[i] + (GREEN[i] - BG[i]) * a2) for i in range(3))
            d.line([(cx - h, cy - h), (cx + h, cy + h)], fill=col, width=5); d.line([(cx - h, cy + h), (cx + h, cy - h)], fill=col, width=5)
            yield im
    pipe('j_logo', gen())


CREDIT = ('INFINITI QX80 R-SPEC', 'for Nissan / Nismo  ·  SEMA 2025')
WEB = D + '/web'   # motorillustrated.com/wp-content/uploads/2025/10/2025-SEMA-INFINITI-QX80-R-Spec-8xx.jpg (not in git)


def press(n, title='INFINITI QX80 R-SPEC'):
    """Press photo whole and static (full width), site-style label above, small muted source credit under the photo."""
    im = photo_frame(f'{WEB}/2025-SEMA-INFINITI-QX80-R-Spec-{n}.jpg', title, CREDIT[1], max_w=1.0)
    d = ImageDraw.Draw(im); top = min(max(520, (HT - 608) // 2 + 120), HT - 608 - 40)
    tracked(d, (74, top + 608 + 22), 'PHOTO VIA MOTORILLUSTRATED.COM', MONO(22), MUTED, em=0.16)
    return im
SEGS = {
    'a_hook': seg_hook,
    'b_answer': seg_answer,
    'c1_scanday': lambda: hold('c1_scanday', photo_frame(wa(13), 'SCAN DAY', 'stock QX80, prepped for the scanner', max_w=1.0)),
    'c2_scanday': lambda: hold('c2_scanday', photo_frame(wa(45), 'SCAN DAY', 'stock QX80, prepped for the scanner', max_w=1.0)),
    'd_scan': lambda: labelled('d_scan', 'N0_open', CUTS['d_scan'], [(4, CUTS['d_scan'] - 4, '3D SCAN', 'the stock car, scanned in-house')]),
    'e_concepts': seg_concepts6,
    'f_panels': lambda: labelled('f_panels', 'D_kit', CUTS['f_panels'], [(4, CUTS['f_panels'] - 4, 'NEW BODY PANELS', 'designed on our scan')], fps_in=30 * 0.65 / BEAT),
    'k_brakes': lambda: labelled('k_brakes', 'K_brakes_car', CUTS['k_brakes'], [(3, CUTS['k_brakes'], 'GT-R BRAKES', 'GT-R scans + our adapters')], fps_in=30),
    'g_final360': lambda: labelled('g_final360', 'G_final360', CUTS['g_final360'],
                                   [(6, 64, 'MIDNIGHT PURPLE', 'colour-shift wrap'), (72, 165, 'FINAL RENDER', 'kit, wheels, brakes and wrap in 3D')]),
    'h_reveal': seg_reveal,
    'p1_press': lambda: hold('p1_press', press(801)),
    'p2_press': lambda: hold('p2_press', press(802)),
    'p3_press': lambda: hold('p3_press', press(804, 'GT-R BRAKES')),
    'p4_press': lambda: hold('p4_press', press(810, 'GT-R ENGINE')),
    'p5_press': lambda: hold('p5_press', press(806)),
    'p6_press': lambda: hold('p6_press', press(809)),
    'j_logo': seg_logo,
}
OUT = D + '/out/infiniti_qx80_v7e.mp4'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'mux']
    for k in (args or ([] if 'mux' in sys.argv else list(SEGS))): SEGS[k]()
    if not args or 'mux' in sys.argv:
        lst = SEG + '/list.txt'; open(lst, 'w').write(''.join(f"file '{SEG}/{k}.mp4'\n" for k in SEGS))
        T = sum(CUTS.values()) / FPS
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-ss', str(MUSIC_START), '-i', MUSIC,
                        '-filter_complex', f'[1:a]volume=-4dB,afade=t=in:d=0.02,afade=t=out:st={T - 2.2:.3f}:d=2.2[a]', '-map', '0:v', '-map', '[a]',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                        '-t', f'{T:.3f}', '-movflags', '+faststart', OUT], check=True)
        print(OUT, T)
