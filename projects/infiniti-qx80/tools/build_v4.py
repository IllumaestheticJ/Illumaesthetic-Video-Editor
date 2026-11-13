"""Infiniti QX80 R-Spec v4 - "how it was made" reel (Sentra SEMA build.py pattern: exact-frame segments, concat, music under).
  python build_v4.py [segment ...] [mux]      (no args = all segments + mux)
Scene list: projects/infiniti-qx80/direction.md "## v4". Video t = music t - 0.66; cuts on the 0.650 s beat grid.
Rules applied: cropped real headlines stacking (Sentra), whole static photos on a blurred fill with the section label in the
band ABOVE the photo (never on it), labels on scan renders only in clear black, no triangle counts, logo 720 px +
'Customize everything'."""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

D = '/home/user/media/infiniti-qx80'; SEG = D + '/seg_v4'; os.makedirs(SEG, exist_ok=True)
WA = D + '/whatsapp/x'; EK = D + '/ecky'; PRESS = D + '/press'; R = D + '/renders/final'
MUSIC = '/home/user/media/work/music/infiniti-qx80_track.mp3'; MUSIC_START = 0.66
LOGO = '/home/user/Illumaesthetic-Video-Editor/remotion/public/illumaesthetic_logo.png'
FPS, WD, HT = 30, 1080, 1920
ENC = ['-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-an']
F = lambda name, size: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/{name}.otf', size)
MONO = lambda size: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', size)
RED = (214, 31, 38); OFF = (232, 236, 242); BG = (7, 7, 9)

# cut frames = round(video t * 30) on the beat grid (direction.md v4 scene list)
CUTS = {'a_hook': 159, 'b1_stock': 39, 'b2_scan': 117, 'c_concepts': 156, 'd_kit': 156, 'e_wrap': 156,
        'f1_eng': 39, 'f2_print': 39, 'f3_fit_wing': 39, 'f4_fit_rear': 20, 'f5_fit_front': 19,
        'g1_finished': 78, 'g2_vent': 39, 'g3_rear': 39, 'h_end': 70}


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
    appear = [42, 81, 120]   # beats at video 1.402 / 2.702 / 4.002
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
    vf = f'scale={WD}:{HT}:flags=lanczos' + (',minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1' if fps_in == 15 else '')
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
CONCEPTS = [('wa', 109), ('wa', 135), ('wa', 166), ('wa', 216), ('wa', 241), ('wa', 257), ('wa', 326),
            ('ek', 'Render/2.png'), ('ek', 'Render/5.png'), ('ek', 'Presentation_Render/1.png'), ('ek', 'Presentation_Render/7.png'),
            ('ek', 'Presentation_Render/9.png'), ('ek', 'Presentation_Render/11.png'), ('wa', 543), ('wa', 595), ('wa', 870)]


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


SEGS = {
    'a_hook': seg_hook,
    'b1_stock': lambda: hold('b1_stock', photo_frame(wa(46), 'STOCK QX80', 'before', max_w=1.0)),
    'b2_scan': lambda: labelled('b2_scan', 'N0_open', CUTS['b2_scan'], [(4, 112, '3D SCAN', 'the stock car, scanned in-house')]),
    'c_concepts': seg_concepts,
    'd_kit': lambda: labelled('d_kit', 'D_kit', CUTS['d_kit'], [(4, 150, 'DESIGNED ON THE SCAN', 'body kit, modelled on our scan')], fps_in=30),
    'e_wrap': lambda: labelled('e_wrap', 'E_paint', CUTS['e_wrap'], [(20, 150, 'MIDNIGHT PURPLE', 'colour-shift wrap')]),
    'f1_eng': lambda: hold('f1_eng', photo_frame(wa(1129), 'ENGINEERED', 'trans adapter plate, on our engine scans', max_w=1.0)),
    'f2_print': lambda: hold('f2_print', photo_frame(wa(1388), '3D PRINTED', 'exhaust shroud', max_w=0.86, max_h=0.70)),
    'f3_fit_wing': lambda: hold('f3_fit_wing', photo_frame(wa(1402), 'TEST FIT', 'wing', max_w=0.86, max_h=0.70)),
    'f4_fit_rear': lambda: hold('f4_fit_rear', photo_frame(wa(1423), 'TEST FIT', 'rear kit', max_w=1.0)),
    'f5_fit_front': lambda: hold('f5_fit_front', photo_frame(wa(1424), 'TEST FIT', 'front lip', max_w=1.0)),
    'g1_finished': lambda: hold('g1_finished', photo_frame(wa(1702), 'FINISHED', 'QX80 R-Spec  ·  SEMA 2025', max_w=1.0)),
    'g2_vent': lambda: hold('g2_vent', photo_frame(wa(1629), 'FINISHED', 'QX80 R-Spec  ·  SEMA 2025', max_w=1.0)),
    'g3_rear': lambda: hold('g3_rear', photo_frame(wa(1690), 'FINISHED', 'QX80 R-Spec  ·  SEMA 2025', max_w=1.0)),
    'h_end': seg_end,
}
OUT = D + '/out/infiniti_qx80_v4.mp4'

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != 'mux']
    for k in (args or ([] if 'mux' in sys.argv else list(SEGS))): SEGS[k]()
    if not args or 'mux' in sys.argv:
        lst = SEG + '/list.txt'; open(lst, 'w').write(''.join(f"file '{SEG}/{k}.mp4'\n" for k in SEGS))
        T = sum(CUTS.values()) / FPS
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-ss', str(MUSIC_START), '-i', MUSIC,
                        '-filter_complex', f'[1:a]afade=t=in:d=0.02,afade=t=out:st={T - 0.4:.3f}:d=0.4[a]', '-map', '0:v', '-map', '[a]',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                        '-t', f'{T:.3f}', '-movflags', '+faststart', OUT], check=True)
        print(OUT, T)
