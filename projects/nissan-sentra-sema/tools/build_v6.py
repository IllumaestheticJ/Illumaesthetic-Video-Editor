"""Sentra SEMA reel v6 (47.5 s) - new structure and music (user 2026-11-13):
hook (Nissan-admits-AI post) -> IT WASN'T. -> scan day -> 3D scan -> concepts -> panels + livery -> 360 of the final render
-> 1:1 cut to the real car ON THE DROP with the headlines landing on it -> SEMA clips that show the whole car -> end card.
Music: Way Out West - Killa (user-supplied), music t = video t; 130 BPM, bar 1.846 s, drop at 29.873 s.
  build_v6.py [segment ...] [mux]"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import build as B
from build import D, W, SEG, FPS, WD, HT, ENC, F, RED, OFF, pipe, clip, wa, label, fade, section_label, ig_frames, render_seq, REC, S

MUSIC = '/home/user/media/work/music/killa.m4a'
BAR = 1.8462; DROP = 29.873
fr = lambda t: int(round(t * FPS))
CUT = {k: fr(DROP + b * BAR) for k, b in dict(wasnt=-14, spray=-13, scanner=-12, tl=-11, scan=-10, concepts=-8, livery=-6, turn=-4, reveal=0, sema=4, end=8).items()}
END = fr(47.5)


def seg_hook():
    """motor1com post 'NISSAN ADMITS IT USED AI IN ITS SENTRA SPEC V PICTURES' from the Instagram recording (t=171), slow 3 % push."""
    im = ig_frames(171.0, 1)[0]; n = CUT['wasnt']
    pipe('v6_a_hook', (B.punch(im, f, n, 1.03) for f in range(n)))


def seg_wasnt():
    n = CUT['spray'] - CUT['wasnt']; f1 = F('InterDisplay-Black', 190)
    def gen():
        for f in range(n):
            im = Image.new('RGB', (WD, HT), (0, 0, 0)); d = ImageDraw.Draw(im)
            if f >= 2:
                for k, (t, c) in enumerate((('IT', OFF), ("WASN'T.", OFF))):
                    d.text(((WD - d.textlength(t, font=f1)) // 2, 760 + k * 200), t, font=f1, fill=c)
                d.rectangle([(WD - 160) // 2, 1190, (WD + 160) // 2, 1202], fill=RED)
            yield im
    pipe('v6_b_wasnt', gen())


def frames_sel(name, src, idx):
    sel = '+'.join(f'eq(n\\,{i})' for i in idx)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f"select='{sel}',setpts=N/{FPS}/TB,scale={WD}:{HT}", '-frames:v', str(len(idx))] + ENC + [f'{SEG}/{name}.mp4'], check=True)
    print(name, len(idx), 'frames')


def seg_scan():
    n = CUT['concepts'] - CUT['scan']; frs = render_seq('s7_scan', n)
    def gen():
        for f in range(n):
            im = Image.fromarray(frs[min(f, len(frs) - 1)]); d = ImageDraw.Draw(im)
            if fade(f, 6, n - 6) > 0: label(d, 330, '3D SCAN', '24,996,032 TRIANGLES', fade(f, 6, n - 6))
            yield im
    pipe('v6_d1_scan', gen())


def seg_concepts():
    nums = [3054, 3092, 3120, 3127, 3135, 3144, 3156, 3192, 3197, 3206, 3219, 3475, 3504, 3527, 3536, 3543, 3572, 3591, 3606, 3956, 3960, 3964, 4067, 4506]
    n = CUT['livery'] - CUT['concepts']; edges = np.round(np.linspace(0, n, len(nums) + 1)).astype(int)
    def gen():
        for j, num in enumerate(nums):
            src = Image.open(wa(num)).convert('RGB'); a = src.width / src.height
            pw = int(WD * 1.5); ph = int(pw / a); p = src.resize((pw, ph), Image.LANCZOS)
            im = Image.new('RGB', (WD, HT), tuple(int(v) for v in np.asarray(src)[4, 4])); im.paste(p, ((WD - pw) // 2, (HT - ph) // 2))
            section_label(im, 'CONCEPTS', 430)
            for _ in range(edges[j + 1] - edges[j]): yield im
    pipe('v6_e_concepts', gen())


def seg_livery():
    n = CUT['turn'] - CUT['livery']; frs = render_seq('s6b_livery', n)
    def gen():
        for f in range(n):
            im = Image.fromarray(frs[min(f, len(frs) - 1)]); d = ImageDraw.Draw(im)
            if fade(f, 3, 74) > 0: label(d, 330, 'NEW BODY PANELS', 'BOMEX WIDEBODY / NISSAN x MOTOIQ', fade(f, 3, 74))
            if fade(f, 80, 109) > 0: label(d, 330, 'LIVERY', 'APPLIED IN 3D FIRST', fade(f, 80, 109))
            yield im
    pipe('v6_d2_livery', gen())


def seg_turn():
    n = CUT['reveal'] - CUT['turn']; frs = render_seq('s8_turn', n)
    def gen():
        for f in range(n):
            im = Image.fromarray(frs[min(f, len(frs) - 1)]); d = ImageDraw.Draw(im)
            if fade(f, 6, 150) > 0: label(d, 330, 'FINAL RENDER', 'SCAN + NEW PANELS + LIVERY', fade(f, 6, 150))
            yield im
    pipe('v6_d3_turn', gen())


def seg_reveal():
    """The real car (Nov 5 booth photo, the frame the 360 ends on) with eight real headlines landing on it, one per beat from beat 2."""
    A = lambda name, y0, y1, x0=0, x1=1080: Image.open(f'{D}/press/{name}.png').convert('RGB').crop((x0, y0, x1, y1))
    mt = subprocess.run(['ffmpeg', '-v', 'error', '-ss', '141', '-i', REC, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    mt = Image.fromarray(np.frombuffer(mt, np.uint8).reshape(2622, 1206, 3)).crop((60, 1465, 1140, 1615))
    top = [('CARSCOOPS', A('carscoops', 215, 500)), ('MOTORTREND', mt), ('MOTORWEEK', A('motorweek', 520, 700)), ('MOTORING RESEARCH', A('motoringresearch', 235, 510)), ('AUTO123', A('auto123', 460, 580))]
    bot = [('TOP GEAR PHILIPPINES', A('topgear_ph', 310, 610, 80, 1080)), ('TFLCAR', A('tflcar', 245, 460)), ('MOTOR ILLUSTRATED', A('motorillustrated', 255, 460))]
    CW = 620; tagf = F('Inter-Bold', 24); cards = []
    def lay(lst, y, xs):
        for k, (tag, im) in enumerate(lst):
            h = int(im.height * CW / im.width); cards.append([tag, im.resize((CW, h), Image.LANCZOS), xs[k % 2], y + 34]); y += h + 34 + 14
        return y
    print('top stack ends y', lay(top, 44, (50, 410))); print('bottom stack ends y', lay(bot, 1330, (410, 50)))
    order = [0, 5, 1, 6, 2, 7, 3, 4]                      # alternate top / bottom so the car stays clear in the middle
    beat = BAR / 4 * FPS; appear = {c: int(round((2 + i) * beat)) for i, c in enumerate(order)}
    base = Image.open(f'{W}/match/reveal.png').convert('RGB'); n = CUT['sema'] - CUT['reveal']
    def gen():
        for f in range(n):
            im = base.copy(); d = ImageDraw.Draw(im)
            for c, (tag, card, x, y) in enumerate(cards):
                if f < appear[c]: continue
                u = min(1.0, (f - appear[c] + 1) / 4); dy = int((1 - u) * 50)
                d.rectangle([x - 6, y - 36 + dy, x + CW + 6, y + card.height + 6 + dy], fill=(8, 8, 10))
                d.rectangle([x, y - 22 + dy, x + 30, y - 18 + dy], fill=RED); d.text((x + 40, y - 32 + dy), tag, font=tagf, fill=OFF)
                im.paste(card, (x, y + dy))
            yield im
    pipe('v6_r_reveal', gen())


def seg_end():
    logo = Image.open(f'{D}/logo/v2complete.png').convert('RGBA'); lw = 720; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS); n = END - CUT['end']
    def gen():
        for f in range(n):
            al = min(1.0, f / 8); im = Image.new('RGB', (WD, HT), (0, 0, 0)); d = ImageDraw.Draw(im)
            l = logo.copy(); l.putalpha(l.getchannel('A').point(lambda v: int(v * al))); im.paste(l, ((WD - lw) // 2, 860), l)
            a2 = max(0.0, min(1.0, (f - 10) / 8)); fnt = F('InterDisplay-Medium', 54); t = 'Customize everything'
            d.text(((WD - d.textlength(t, font=fnt)) // 2, 860 + logo.height + 70), t, font=fnt, fill=tuple(int(v * a2) for v in OFF))
            yield im
    pipe('v6_z_end', gen())


def seg_sema():
    """Four clips where the whole car stays in frame (user: earlier end shots cropped the car or cut too soon), one bar each."""
    n = (CUT['end'] - CUT['sema']); e = np.round(np.linspace(0, n, 5)).astype(int); L = [e[i + 1] - e[i] for i in range(4)]
    def gen():
        yield from ig_frames(151.4, L[0])                                  # motoiq: door lifts, car revealed
        yield from ig_frames(72.0, L[1])                                   # caranddriver: on track
        yield from ig_frames(88.0, L[2])                                   # eddiex616: whole car from the front
    pipe('v6_s1_reels', gen())                                             # (own IMG_3228 booth wide dropped: nose leaves the frame)
    clip('v6_s3_rear', S + 'IMG_3235.mov', 0.0, L[3])                      # rear wide, wing + diffuser


SEGS = {
    'v6_a_hook': seg_hook, 'v6_b_wasnt': seg_wasnt,
    'v6_c1_spray': lambda: frames_sel('v6_c1_spray', D + '/dropbox/may11_1135.mov', np.round(np.linspace(10, 280, CUT['scanner'] - CUT['spray'])).astype(int)),
    'v6_c2_scanner': lambda: clip('v6_c2_scanner', S + 'may11_1145.mov', 7.0, CUT['tl'] - CUT['scanner'], hdr=False),
    'v6_c3_timelapse': lambda: frames_sel('v6_c3_timelapse', D + '/dropbox/may11_1140.mov', np.round(np.linspace(540, 780, CUT['scan'] - CUT['tl'])).astype(int)),
    'v6_d1_scan': seg_scan, 'v6_e_concepts': seg_concepts, 'v6_d2_livery': seg_livery, 'v6_d3_turn': seg_turn,
    'v6_r_reveal': seg_reveal, 'v6_s': seg_sema, 'v6_z_end': seg_end,
}
ORDER = ['v6_a_hook', 'v6_b_wasnt', 'v6_c1_spray', 'v6_c2_scanner', 'v6_c3_timelapse', 'v6_d1_scan', 'v6_e_concepts', 'v6_d2_livery', 'v6_d3_turn',
         'v6_r_reveal', 'v6_s1_reels', 'v6_s3_rear', 'v6_z_end']
if __name__ == '__main__':
    print('cut frames', CUT, 'end', END)
    for k in [a for a in sys.argv[1:] if a != 'mux']: SEGS[k]()
    if 'mux' in sys.argv:
        lst = SEG + '/list_v6.txt'; open(lst, 'w').write(''.join(f"file '{SEG}/{k}.mp4'\n" for k in ORDER)); out = W + '/out/sentra_sema_v6.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', MUSIC, '-filter_complex', f'[1:a]afade=t=out:st={END / FPS - 1.2}:d=1.2[a]',
                        '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-t', str(END / FPS), '-movflags', '+faststart', out], check=True)
        print(out)
