"""Infiniti QX80 R-Spec v6 - Sentra v6 build-story structure (knowledge/short-form.md, approved on the Sentra reel):
hook (one real article, full frame, 3 % push) -> answer card 'HERE'S HOW.' -> scan day -> 3D SCAN -> CONCEPTS -> NEW BODY PANELS
-> FINAL RENDER 360 (wrap sweep, Ecky's wheels/grille/T-spec lights, ends on the solved camera of photo 1702) -> 1:1 cut to the
real car ON THE DROP with cropped real headlines landing one per beat -> finished-car photos -> logo (all caps wordmark only).
Music: deadmau5 - Ghosts 'n' Stuff (Original Instrumental Mix), TikTok CML song_clip_id 6739936808198473729, 128.0 BPM;
video t0 = track 15.019 (kick); breakdown 30.02; DROP kick 45.019 = video 30.000 (beat 64).
"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

D = '/home/user/media/infiniti-qx80'; SEG = D + '/seg_v6'; os.makedirs(SEG, exist_ok=True)
WA = D + '/whatsapp/x'; EK = D + '/ecky'; PRESS = D + '/press'; R = D + '/renders/final'
MUSIC = '/home/user/media/work/music/ghosts_n_stuff.mp3'; MUSIC_START = 15.019
LOGO = '/home/user/Illumaesthetic-Video-Editor/remotion/public/illumaesthetic_logo.png'
FPS, WD, HT = 30, 1080, 1920
ENC = ['-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-an']
F = lambda name, size: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/{name}.otf', size)
MONO = lambda size: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', size)
RED = (214, 31, 38); OFF = (232, 236, 242); BG = (7, 7, 9)

# cut frames = round(video t * 30) on the beat grid (direction.md v4 scene list)
BEAT = 60 / 128.0   # 0.46875 s; cut frames = round(beat * BEAT * 30) on the track's kick grid
_B = [0, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 84, 88, 92, 96, 104]
_N = ['a_hook', 'b_answer', 'c1_scanday', 'c2_scanday', 'c3_scanday', 'd_scan', 'e_concepts', 'f_panels', 'g_final360',
      'h_reveal', 'i1_after', 'i2_after', 'i3_after', 'i4_after', 'j_logo']
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
    return Image.eval(bg, lambda v: int(v * 0.30))


def section_label(im, title, sub=None, y=300):
    """Section title (+ mono sub line) with a dark halo, in the band above the photo / in black above the car."""
    d = ImageDraw.Draw(im); f = F('InterDisplay-Bold', 76)
    d.rectangle([72, y - 24, 136, y - 16], fill=RED)
    for dx, dy in ((3, 3), (2, 2)): d.text((72 + dx, y + dy), title, font=f, fill=(0, 0, 0))
    d.text((72, y), title, font=f, fill=OFF)
    if sub:
        fm = MONO(32)
        d.text((76, y + 96), sub, font=fm, fill=(0, 0, 0)); d.text((74, y + 94), sub, font=fm, fill=OFF)


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
            im = Image.fromarray(fr[f])
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


def seg_hook():
    """One real article, full frame, slow 3 % push (Sentra v6 hook)."""
    src = Image.open(f'{PRESS}/carscoops_page.png').convert('RGB').resize((WD, HT), Image.LANCZOS); n = CUTS['a_hook']
    def gen():
        for f in range(n):
            z = 1.0 + 0.03 * f / (n - 1); cw, ch = int(WD / z), int(HT / z)
            yield src.crop(((WD - cw) // 2, (HT - ch) // 2, (WD + cw) // 2, (HT + ch) // 2)).resize((WD, HT), Image.BICUBIC)
    pipe('a_hook', gen())


def seg_answer():
    im = Image.new('RGB', (WD, HT), BG); d = ImageDraw.Draw(im); t = "HERE'S HOW."; size = 190
    while d.textlength(t, font=F('InterDisplay-Black', size)) > 900: size -= 4
    f = F('InterDisplay-Black', size); w = d.textlength(t, font=f); x = (WD - w) // 2; y = HT // 2 - size // 2
    d.rectangle([x, y - 40, x + 110, y - 28], fill=RED); d.text((x, y), t, font=f, fill=OFF)
    hold('b_answer', im)


CONCEPTS6 = [('wa', 109), ('wa', 135), ('wa', 166), ('wa', 216), ('wa', 241), ('wa', 249), ('wa', 257), ('wa', 326), ('wa', 360),
             ('wa', 375), ('wa', 395), ('ek', 'Render/2.png'), ('ek', 'Render/1.png'), ('ek', 'Render/5.png'), ('ek', 'Presentation_Render/1.png'),
             ('ek', 'Presentation_Render/2.png'), ('ek', 'Presentation_Render/7.png'), ('ek', 'Presentation_Render/9.png'),
             ('ek', 'Presentation_Render/11.png'), ('wa', 543), ('wa', 595), ('wa', 870)]


def seg_concepts6():
    n = CUTS['e_concepts']; k = len(CONCEPTS6); edges = [round(i * n / k) for i in range(k + 1)]
    def gen():
        for i, (kind, ref) in enumerate(CONCEPTS6):
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
    CW = 960; x0 = (WD - CW) // 2; tagf = F('Inter-Bold', 28); placed = []
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
                d.rectangle([x0, y + dy - 30, x0 + 40, y + dy - 25], fill=RED); d.text((x0 + 52, y + dy - 44), tag, font=tagf, fill=OFF)
                im.paste(c, (x0, y + dy))
            yield im
    pipe('h_reveal', gen())


def seg_logo():
    logo = Image.open(LOGO).convert('RGBA'); logo = logo.crop(logo.getbbox())
    lw = 720; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS); n = CUTS['j_logo']
    def gen():
        for f in range(n):
            al = min(1.0, f / 8, (n - 1 - f) / 20 + 0.05)
            im = Image.new('RGB', (WD, HT), BG); l = logo.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * al)))
            im.paste(l, ((WD - lw) // 2, (HT - logo.height) // 2), l); yield im
    pipe('j_logo', gen())


CREDIT = ('INFINITI QX80 R-SPEC', 'for Nissan / Nismo  ·  SEMA 2025')
SEGS = {
    'a_hook': seg_hook,
    'b_answer': seg_answer,
    'c1_scanday': lambda: hold('c1_scanday', photo_frame(wa(13), 'SCAN DAY', 'stock QX80, prepped for the scanner', max_w=1.0)),
    'c2_scanday': lambda: hold('c2_scanday', photo_frame(wa(45), 'SCAN DAY', 'stock QX80, prepped for the scanner', max_w=1.0)),
    'c3_scanday': lambda: hold('c3_scanday', photo_frame(wa(46), 'SCAN DAY', 'stock QX80, prepped for the scanner', max_w=1.0)),
    'd_scan': lambda: labelled('d_scan', 'N0_open', CUTS['d_scan'], [(4, CUTS['d_scan'] - 4, '3D SCAN', 'the stock car, scanned in-house')]),
    'e_concepts': seg_concepts6,
    'f_panels': lambda: labelled('f_panels', 'D_kit', CUTS['f_panels'], [(4, CUTS['f_panels'] - 4, 'NEW BODY PANELS', 'designed on our scan')], fps_in=30 * 0.65 / BEAT),
    'g_final360': lambda: labelled('g_final360', 'G_final360', CUTS['g_final360'],
                                   [(6, 64, 'MIDNIGHT PURPLE', 'colour-shift wrap'), (72, 165, 'FINAL RENDER', 'kit, wheels and wrap in 3D')]),
    'h_reveal': seg_reveal,
    'i1_after': lambda: hold('i1_after', photo_frame(wa(1701), *CREDIT, max_w=1.0)),
    'i2_after': lambda: hold('i2_after', photo_frame(wa(1690), *CREDIT, max_w=1.0)),
    'i3_after': lambda: hold('i3_after', photo_frame(wa(1629), *CREDIT, max_w=1.0)),
    'i4_after': lambda: hold('i4_after', photo_frame(wa(1693), *CREDIT, max_w=1.0)),
    'j_logo': seg_logo,
}
OUT = D + '/out/infiniti_qx80_v6.mp4'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'mux']
    for k in (args or ([] if 'mux' in sys.argv else list(SEGS))): SEGS[k]()
    if not args or 'mux' in sys.argv:
        lst = SEG + '/list.txt'; open(lst, 'w').write(''.join(f"file '{SEG}/{k}.mp4'\n" for k in SEGS))
        T = sum(CUTS.values()) / FPS
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-ss', str(MUSIC_START), '-i', MUSIC,
                        '-filter_complex', f'[1:a]afade=t=in:d=0.02,afade=t=out:st={T - 2.2:.3f}:d=2.2[a]', '-map', '0:v', '-map', '[a]',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                        '-t', f'{T:.3f}', '-movflags', '+faststart', OUT], check=True)
        print(OUT, T)
