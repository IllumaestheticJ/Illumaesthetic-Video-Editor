"""Assemble the Sentra SEMA reel v1 (30 s). Every segment is rendered to an mp4 with an exact frame count and
concatenated (no xfade cut tricks: lesson honda-s2000), then the music is laid under it.
  build.py [segment ...]     (no args = all segments + final mux)
Cut frames come from kick onsets measured on the track (tools/kicks.py), video t = music t - MUSIC_START."""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

D = '/home/user/media/sentra-sema'; W = '/home/user/media/work/sentra'; SEG = W + '/seg'; os.makedirs(SEG, exist_ok=True)
MUSIC = '/home/user/media/work/music/montagem_lunae.mp3'; MUSIC_START = 21.135
FPS, WD, HT = 30, 1080, 1920
TONEMAP = "zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
ENC = ['-c:v', 'libx264', '-crf', '12', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-an']
F = lambda name, size: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/{name}.otf', size)
RED = (214, 31, 38); OFF = (232, 236, 242)

HEADLINES = [  # real headlines (web search 2026-11-12); typographic stand-ins until real captures arrive
    ('TOP GEAR PHILIPPINES', "SEMA 2026: Nissan's Sentra Spec-V Concept is loaded with parts from the Nismo catalog"),
    ('CARSCOOPS', "Nissan's SEMA Sentra Spec-V Implies The Brand Still Cares About Small Car Performance"),
    ('TFLCAR', "This Nissan Sentra Spec-V Concept is the Hot Sentra We've Been Missing"),
    ('TOPSPEED', "Nissan Goes Full Beast Mode: Sentra Spec-V Officially Returns"),
    ('MOTORWEEK', "Nissan Sentra Spec-V is a Super Cool SEMA Concept"),
    ('AUTO123', "Nissan revives Spec-V nameplate with 300-hp Sentra Concept"),
    ('MOTORING RESEARCH', "SEMA Show: Nissan reveals turbocharged Sentra Spec-V concept"),
    ('MOTOR ILLUSTRATED', "Nissan Revives Sentra Spec-V Name With Turbocharged SEMA Concept"),
    ('PAKWHEELS', "Nissan Sentra Spec-V 300 HP Revealed for SEMA 2026"),
    ('AUTONEWSLINE', "Nissan Sentra Spec-V Concept: 300 HP, Manual, GT-R Brakes"),
    ('YAHOO AUTOS', "Nissan Just Turned the Sentra Into a 300-HP GT-R Wannabe"),
    ('YAHOO AUTOS', "Garbled Nissan badge raises AI suspicions over 300-horsepower Sentra concept photos"),
]


def pipe(name, frames):
    """frames: iterable of PIL RGB 1080x1920 images -> seg mp4"""
    out = f'{SEG}/{name}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{WD}x{HT}', '-r', str(FPS), '-i', '-'] + ENC + [out], stdin=subprocess.PIPE)
    n = 0
    for im in frames:
        p.stdin.write(im.tobytes()); n += 1
    p.stdin.close(); p.wait(); print(name, n, 'frames')


def clip(name, src, t_in, nframes, hdr=True, speed=1.0, extra=''):
    vf = (TONEMAP + ',' if hdr else '') + (f'setpts=PTS/{speed},' if speed != 1 else '') + f'fps={FPS},scale={WD}:{HT}:force_original_aspect_ratio=increase,crop={WD}:{HT}' + extra
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t_in), '-i', src, '-vf', vf, '-frames:v', str(nframes)] + ENC + [f'{SEG}/{name}.mp4'], check=True)
    print(name, nframes, 'frames')


def wrap(d, text, font, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]


def card(i, w=WD, h=HT, scale=1.0):
    outlet, head = HEADLINES[i]
    im = Image.new('RGB', (w, h), (10, 10, 12)); d = ImageDraw.Draw(im)
    fs = int((118 if len(head) < 60 else 100 if len(head) < 80 else 88) * scale * w / WD)
    fh, fo = F('InterDisplay-Bold', fs), F('Inter-Bold', int(40 * scale * w / WD))
    m = int(70 * w / WD); lines = wrap(d, head, fh, w - 2 * m); lh = int(fs * 1.12)
    y0 = (h - lh * len(lines)) // 2 + (-1, 0, 1)[i % 3] * int(h * 0.07)
    d.rectangle([m, y0 - int(86 * scale * w / WD), m + int(64 * w / WD), y0 - int(78 * scale * w / WD)], fill=RED)
    d.text((m, y0 - int(64 * scale * w / WD)), outlet, font=fo, fill=RED)
    for k, ln in enumerate(lines): d.text((m, y0 + k * lh), ln, font=fh, fill=OFF)
    return im


def seg_barrage1():
    cuts = [45, 55, 59, 69, 73, 83, 87, 97, 113, 129, 141, 153, 158]   # kick onsets, bar 1 of drop 1
    def gen():
        for i in range(12):
            c = card(i); n = cuts[i + 1] - cuts[i]
            for f in range(n):   # 3 % punch-in per card so no frame is static
                z = 1.03 - 0.03 * f / max(1, n - 1); cw, ch = int(WD / z), int(HT / z)
                yield c.crop(((WD - cw) // 2, (HT - ch) // 2, (WD + cw) // 2, (HT + ch) // 2)).resize((WD, HT), Image.BICUBIC)
    pipe('b_barrage1', gen())


def seg_wall():
    hits = [0, 10, 13, 24, 28, 38, 42, 52, 68, 84, 96]              # frames after 720 (kick onsets, bar 3 of drop 2)
    cols, rows, gap = 3, 4, 14; tw = (WD - gap * (cols + 1)) // cols; th = int(tw * 1.42)
    tiles = [card(i, tw * 2, th * 2, 1.25).resize((tw, th), Image.LANCZOS) for i in range(12)]
    y0 = (HT - rows * th - (rows - 1) * gap) // 2
    order = [5, 0, 7, 2, 10, 3, 8, 1, 11, 4, 6, 9]
    def gen():
        for f in range(113):
            im = Image.new('RGB', (WD, HT), (0, 0, 0)); n = sum(1 for h in hits if h <= f) + 1
            for k in order[:n]:
                im.paste(tiles[k], (gap + (k % cols) * (tw + gap), y0 + (k // cols) * (th + gap)))
            z = 1.10 - 0.10 * f / 112; cw, ch = int(WD / z), int(HT / z)
            yield im.crop(((WD - cw) // 2, (HT - ch) // 2, (WD + cw) // 2, (HT + ch) // 2)).resize((WD, HT), Image.BICUBIC)
    pipe('h_wall', gen())


def wa(num):
    return glob.glob(f'{D}/wa/x/0000{num}-PHOTO-*.jpg')[0]


def fill(photo, zoom0, zoom1, cx0, cx1, n, cy=0.5, bright=1.0):
    """Landscape photo in 9:16: blurred, darkened fill of itself + the photo zooming from zoom0 to zoom1
    (1.0 = photo width == frame width); cx = horizontal centre of the view in photo fractions."""
    src = Image.open(photo).convert('RGB'); a = src.width / src.height
    bg = src.resize((int(HT * a), HT)).crop((int(HT * a - WD) // 2, 0, int(HT * a - WD) // 2 + WD, HT)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.eval(bg, lambda v: int(v * 0.35))
    for f in range(n):
        u = f / max(1, n - 1); u = u * u * (3 - 2 * u); z = zoom0 + (zoom1 - zoom0) * u; cx = cx0 + (cx1 - cx0) * u
        pw = int(WD * z); ph = int(pw / a); im = bg.copy()
        p = src.resize((pw, ph), Image.LANCZOS)
        im.paste(p, (int(WD / 2 - cx * pw), int(HT * cy - ph / 2)))
        yield im


def seg_flip():
    nums = [3054, 3092, 3120, 3135, 3156, 3197, 3219, 3504, 3527, 3543, 3606, 3960, 3964, 4506]
    def gen():
        for n in nums:
            src = Image.open(wa(n)).convert('RGB'); a = src.width / src.height
            pw = int(WD * 1.5); ph = int(pw / a); p = src.resize((pw, ph), Image.LANCZOS)
            im = Image.new('RGB', (WD, HT), tuple(int(v) for v in np.asarray(src)[4, 4])); im.paste(p, ((WD - pw) // 2, (HT - ph) // 2))
            for _ in range(3): yield im
    pipe('e_flip', gen())


def label(d, y, title, sub, alpha):
    c = tuple(int(v * alpha) for v in OFF); r = tuple(int(v * alpha) for v in RED)
    d.rectangle([80, y - 18, 144, y - 12], fill=r)
    d.text((80, y), title, font=F('InterDisplay-Bold', 64), fill=c)
    d.text((80, y + 82), sub, font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 30), fill=c)


def seg_scan():
    """59+ renders at 15 fps -> 113 frames (minterpolate), then labels in the black band above the car."""
    n = len(glob.glob(f'{W}/renders/s1_scan/f_*.png')); tmp = f'{SEG}/_scan_raw.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '15', '-i', f'{W}/renders/s1_scan/f_%04d.png', '-vf',
                    f'scale={WD}:{HT}:flags=lanczos,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1', '-frames:v', '113'] + ENC + [tmp], check=True)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', tmp, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, HT, WD, 3); print('scan frames', len(fr), 'from', n, 'renders')
    def a(f, f0, f1): return max(0.0, min(1.0, (f - f0) / 5, (f1 - f) / 5))
    def gen():
        for f in range(113):
            im = Image.fromarray(fr[min(f, len(fr) - 1)]); d = ImageDraw.Draw(im)
            if a(f, 6, 48) > 0: label(d, 330, '3D SCAN', '24,996,032 TRIANGLES', a(f, 6, 48))
            if a(f, 54, 110) > 0: label(d, 330, 'DESIGNED ON THE SCAN', 'BOMEX WIDEBODY / NISSAN x MOTOIQ', a(f, 54, 110))
            yield im
    pipe('d_scan', gen())


def seg_timelapse():
    """Spray timelapse, 4.2x, ending exactly on source frame 780 (t=26.0 = the solved 1:1 frame)."""
    idx = np.round(np.linspace(540, 780, 57)).astype(int); sel = '+'.join(f'eq(n\\,{i})' for i in idx)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/dropbox/may11_1140.mov', '-vf', f"select='{sel}',setpts=N/{FPS}/TB,scale={WD}:{HT}", '-frames:v', '57'] + ENC + [f'{SEG}/c3_timelapse.mp4'], check=True)
    print('c3_timelapse 57 frames, last = src frame', idx[-1])


def seg_end():
    logo = Image.open(f'{D}/drive/IllumaestheticLogoColor-01.png').convert('RGBA'); lw = 720; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    def gen():
        for f in range(67):
            al = min(1.0, f / 8); im = Image.new('RGB', (WD, HT), (0, 0, 0)); d = ImageDraw.Draw(im)
            l = logo.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * al))); im.paste(l, ((WD - lw) // 2, 860), l)
            a2 = max(0.0, min(1.0, (f - 10) / 8)); fnt = F('InterDisplay-Medium', 54); t = 'Customize everything'
            d.text(((WD - d.textlength(t, font=fnt)) // 2, 860 + logo.height + 70), t, font=fnt, fill=tuple(int(v * a2) for v in OFF))
            yield im
    pipe('i_end', gen())


S = D + '/dropbox/'
SEGS = {
    'a_hook': lambda: clip('a_hook', S + 'IMG_3233.mov', 0.2, 45),
    'b_barrage1': seg_barrage1,
    'c1_badge': lambda: clip('c1_badge', S + 'IMG_3231.mov', 0.3, 28),
    'c2_front': lambda: clip('c2_front', S + 'IMG_3229.mov', 4.3, 27),
    'c3_timelapse': seg_timelapse,
    'd_scan': seg_scan,
    'e_flip': seg_flip,
    'f1_print': lambda: pipe('f1_print', fill(wa(5898), 1.75, 1.45, 0.5, 0.5, 35)),
    'f2_fender': lambda: pipe('f2_fender', fill(wa(5895), 1.6, 1.8, 0.45, 0.45, 35)),
    'g1_reveal': lambda: pipe('g1_reveal', fill(wa(5888), 2.05, 1.5, 0.36, 0.5, 52)),
    'g2_wheel': lambda: clip('g2_wheel', S + 'IMG_3236.mov', 3.9, 32),
    'g3_splitter': lambda: clip('g3_splitter', S + 'IMG_3230.mov', 3.2, 29),
    'g4_side': lambda: clip('g4_side', S + 'IMG_3233.mov', 12.5, 55),
    'g5_exhaust': lambda: clip('g5_exhaust', S + 'IMG_3237.mov', 3.6, 29),
    'g6_diffuser': lambda: clip('g6_diffuser', S + 'IMG_3235.mov', 10.0, 28),
    'h_wall': seg_wall,
    'i_end': seg_end,
}
if __name__ == '__main__':
    for k in ([a for a in sys.argv[1:] if a != 'mux'] or ([] if 'mux' in sys.argv else list(SEGS))): SEGS[k]()
    if not sys.argv[1:] or 'mux' in sys.argv:
        lst = SEG + '/list.txt'; open(lst, 'w').write(''.join(f"file '{SEG}/{k}.mp4'\n" for k in SEGS))
        out = W + '/out/sentra_sema_30s_v1.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-ss', str(MUSIC_START), '-i', MUSIC,
                        '-filter_complex', '[1:a]afade=t=in:d=0.03,afade=t=out:st=29.3:d=0.7[a]', '-map', '0:v', '-map', '[a]',
                        '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-t', '30', '-movflags', '+faststart', out], check=True)
        print(out)
