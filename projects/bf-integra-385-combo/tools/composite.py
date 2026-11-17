"""bf-integra-385-combo v0 compositor.
Plates (Blender PNGs at 15 fps, 540x960) -> 30 fps 1080x1920, plus PIL overlays: receipt, title, end card
(no characters: owner removed Del & Eps from the BF videos). C0222 (real gloss-black wing) cropped to 9:16. Music: "Get Low" from 0 s.
All prices from projects/_blackfriday/PRICES.md (BF liquidation sheet): wing $500, lip $100, combo $600 -> $385.
usage: python composite.py OUT.mp4
"""
import subprocess, sys, glob, os, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = '/home/user/media/bf-integra-385-combo'
R = f'{M}/work'
TMP = f'{M}/work/comp_v0'; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 30
# v0.2 timeline (user: both parts on the car at the end; scan shows the stock spoiler coming off)
# (kind, source, overlay shot id, frames) - cuts on measured kick attacks: 97 168 239 310 380 451 522 593, end 664
# v0.3: coloured opening + DE4 wingless deck fill (render_v03), kitted CGI orbit (render_v0/s9), stabilised C0240
TIMELINE = [('render', 'render_v03/s1', 1, 97), ('render', 'render_v03/s2', 2, 71), ('render', 'render_v03/s3', 3, 71),
            ('render', 'render_v06/s4', 4, 141), ('render', 'render_v04/s7', 0, 71), ('render', 'render_v04/s8', 0, 71),
            ('render', 'render_v04/s9', 0, 71), ('irl', 'c0240_stab', 0, 71), ('card', None, 8, 142)]  # v0.6: price shot and end card one bar longer each (user: deal numbers easier to read)
LEN = [t[3] for t in TIMELINE]
CUTS = np.cumsum([0] + LEN)                       # 0 97 167 238 309 380 450 521 592
OFFWHITE = (232, 236, 242, 255); ORANGE = (232, 89, 149, 255); YELLOW = (1, 222, 226, 255)  # v0.3: Epsilon+ palette (pink strike, cyan price)
F_TITLE = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
F_MONO = '/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf'
F_MONO_R = '/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf'


def font(p, s): return ImageFont.truetype(p, s)


def ease(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def tracked(d, xy, text, f, fill, track=6, anchor_center=False):
    """draw text with letter tracking; returns width"""
    widths = [d.textlength(c, font=f) for c in text]; tw = sum(widths) + track * (len(text) - 1)
    x, y = xy
    if anchor_center: x -= tw / 2
    for c, w_ in zip(text, widths):
        d.text((x, y), c, font=f, fill=fill); x += w_ + track
    return tw


CH = {}  # Del & Eps removed from all BF videos (owner, 2026-11-17)


def char_layer(img, name, x, y, scale, t_in, fr, dim=0.88):
    """paste a character still with a slide/scale-in starting at frame t_in (8 frames) and a slow 2 % breathe"""
    if fr < t_in: return
    u = ease((fr - t_in) / 8)
    c = CH[name]; s = scale * (0.92 + 0.08 * u) * (1 + 0.02 * math.sin(fr / 14))
    c = c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)
    if dim < 1:
        a = c.split()[3]; c = Image.eval(c.convert('RGB'), lambda v: int(v * dim)).convert('RGBA'); c.putalpha(a)
    if u < 1:
        a = c.split()[3].point(lambda v: int(v * u)); c.putalpha(a)
    # soft contact glow so they don't float on pure black
    img.alpha_composite(c, (int(x - c.width / 2), int(y - c.height)))


def receipt(img, fr, lines, x0, y0, w=520):
    """lines: list of (start_frame, kind, payload)"""
    d = ImageDraw.Draw(img)
    vis = [l for l in lines if fr >= l[0]]
    if not vis: return
    h = 120 + 70 * len([l for l in lines if l[1] in ('item', 'combo')]) + (150 if any(l[1] == 'bf' for l in lines) else 0)
    panel = Image.new('RGBA', (w, h), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle((0, 0, w - 1, h - 1), 18, fill=(14, 15, 17, 225), outline=(232, 236, 242, 70), width=2)
    pd.text((28, 26), 'INTEGRA DE4 / DE5', font=font(F_MONO_R, 26), fill=(170, 176, 186, 255))
    pd.line((28, 76, w - 28, 76), fill=(232, 236, 242, 60), width=2)
    y = 96
    fm = font(F_MONO, 34)
    for st, kind, pay in lines:
        on = fr >= st; u = ease((fr - st) / 6) if on else 0
        if kind in ('item', 'combo'):
            if on:
                name, price = pay['name'], pay['price']
                col = tuple(int(v * u) if i < 3 else 255 for i, v in enumerate(OFFWHITE)) if kind == 'item' else OFFWHITE
                pd.text((28, y), name, font=fm, fill=OFFWHITE if u >= 1 else (232, 236, 242, int(255 * u)))
                pw = pd.textlength(price, font=fm)
                pd.text((w - 28 - pw, y), price, font=fm, fill=(232, 236, 242, int(255 * u)))
                if kind == 'combo' and fr >= pay['strike']:
                    su = ease((fr - pay['strike']) / 5)
                    x1 = w - 28 - pw - 6; x2 = x1 + (pw + 12) * su
                    pd.line((x1, y + 22, x2, y + 22), fill=ORANGE, width=6)
            y += 70
        elif kind == 'bf' and on:
            k = fr - st; pop = 1 + 0.25 * math.exp(-k / 3) * (1 if k < 12 else 0)
            fb = font(F_TITLE, int(110 * pop))
            txt = pay['price']; tw = pd.textlength(txt, font=fb)
            pd.text((w - 28 - tw, y + 8 - (pop - 1) * 40), txt, font=fb, fill=YELLOW)
            pd.text((28, y + 40), 'BLACK\nFRIDAY', font=font(F_MONO, 30), fill=OFFWHITE, spacing=6)
    slide = ease((fr - vis[0][0]) / 8)
    a = panel.split()[3].point(lambda v: int(v * slide)); panel.putalpha(a)
    img.alpha_composite(panel, (int(x0 + 30 * (1 - slide)), int(y0)))


def overlay(shot, fr):
    """fr = frame within shot (0-based). returns RGBA overlay"""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    WING = {'name': 'SPORT WING', 'price': '$500'}
    LIP = {'name': 'TRUNK LIP', 'price': '$100'}
    if shot == 1:
        u = ease((fr - 4) / 10)
        if u > 0:
            ft = font(F_TITLE, 118)
            tracked(d, (W / 2, 330 + 30 * (1 - u)), 'EPSILON+  BLACK FRIDAY', font(F_MONO, 34), (1, 222, 226, int(255 * u)), track=8, anchor_center=True)
            for i, line in enumerate(('WHAT $385', 'GETS YOU')):
                tracked(d, (W / 2, 390 + i * 135 + 30 * (1 - u)), line, ft, (232, 236, 242, int(255 * u)), track=6, anchor_center=True)
    elif shot == 2:
        receipt(img, fr, [(8, 'item', WING)], 280, 330)
    elif shot == 3:
        receipt(img, fr + 100, [(0, 'item', WING), (108, 'item', LIP)], 280, 330)
    elif shot == 4:
        receipt(img, fr + 200, [(0, 'item', WING), (0, 'item', LIP), (200, 'combo', {'name': 'COMBO', 'price': '$600', 'strike': 218}),
                                (236, 'bf', {'price': '$385'})], 260, 880, w=560)
        if fr >= 48:
            u = ease((fr - 48) / 8)
            tracked(d, (540, 1385), 'LESS THAN THE WING ALONE ($500)', font(F_MONO_R, 26), (232, 236, 242, int(230 * u)), track=1, anchor_center=True)
    elif shot == 8:
        logo = Image.open(f'{M}/logo/Epsilon+ Logo.png').convert('RGBA')
        u = ease(fr / 6)
        lw = 720; lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
        lg.putalpha(lg.split()[3].point(lambda v: int(v * u)))
        img.alpha_composite(lg, ((W - lw) // 2, 700))
        if fr >= 6:
            v = ease((fr - 6) / 8)
            tracked(d, (W / 2, 900), 'SPORT WING + TRUNK LIP', font(F_TITLE, 46), (232, 236, 242, int(255 * v)), track=4, anchor_center=True)
            tracked(d, (W / 2, 975), '$385', font(F_TITLE, 150), YELLOW[:3] + (int(255 * v),), track=4, anchor_center=True)
            tracked(d, (W / 2, 1160), 'BLACK FRIDAY', font(F_MONO, 40), (232, 236, 242, int(255 * v)), track=10, anchor_center=True)
            tracked(d, (W / 2, 1240), 'www.epsilon.plus', font(F_MONO_R, 40), (232, 236, 242, int(220 * v)), track=2, anchor_center=True)
    return img


def plate_frames(src, n):
    """render PNGs (15 fps) -> 1080x1920 RGB arrays at 30 fps via ffmpeg minterpolate"""
    cmd = ['ffmpeg', '-v', 'error', '-framerate', '15', '-pattern_type', 'glob', '-i', f'{R}/{src}/f*.png',
           '-vf', 'minterpolate=fps=30:mi_mode=blend,scale=1080:1920:flags=lanczos,format=rgb24', '-frames:v', str(n),
           '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr


def irl_frames(name, n, start=0.5, cx0=0.46, cx1=0.60):  # c0240_stab.mp4 = C0240 11.8-15.2 s, vidstab shakiness 10, smoothing 90 (car jitter 9.5 -> 1.3 px)
    """C0240 (finished car, Sport Wing + trunk lip, flat profile): grade, a 45 %-wide crop that follows the car,
    on a blurred, darkened fill of itself (no text ever goes on this shot)"""
    dur = n / FPS
    fc = (f'[0:v]fps=30,eq=contrast=1.3:saturation=1.2:gamma=0.9,split[a][b];'
          f"[a]crop=iw*0.52:ih:x='iw*({cx0}+{cx1 - cx0}*t/{dur:.3f})-ow/2':y=0,scale=1080:1150:flags=lanczos[fg];"
          f'[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:2,eq=brightness=-0.22[bg];'
          f'[bg][fg]overlay=0:285,format=rgb24')
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', f'{M}/footage/{name}.mp4', '-filter_complex', fc,
           '-frames:v', str(n), '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr


def main(out):
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{TMP}/video.mp4'],
                           stdin=subprocess.PIPE)
    for kind, src, ov, n in TIMELINE:
        if kind == 'render': plates = plate_frames(src, n)
        elif kind == 'irl': plates = irl_frames(src, n)
        else: plates = np.zeros((n, H, W, 3), np.uint8) + 3
        for i in range(n):
            base = Image.fromarray(plates[i]).convert('RGBA')
            if kind != 'irl' and ov:  # never put anything over IRL footage
                o = overlay(ov, i)
                if kind == 'card':  # slow 3 % push-in so the longer end card isn't a dead hold
                    z = 1 + 0.03 * i / n; o = o.resize((int(W * z), int(H * z)), Image.LANCZOS)
                    o = o.crop(((o.width - W) // 2, (o.height - H) // 2, (o.width - W) // 2 + W, (o.height - H) // 2 + H))
                base.alpha_composite(o)
            enc.stdin.write(np.asarray(base.convert('RGB')).tobytes())
        print(kind, src, 'frames', n, flush=True)
    enc.stdin.close(); enc.wait()
    dur = CUTS[-1] / FPS
    # music from the song's beginning, fade with the end card, -14 LUFS / TP < -1 (gain then limiter)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{TMP}/video.mp4', '-i', f'{M}/music/getlow.wav',
                    '-filter_complex', f'[1:a]atrim=0:{dur:.3f},afade=t=out:st={dur - 0.7:.3f}:d=0.7,'
                    'loudnorm=I=-14.5:TP=-2:LRA=11,alimiter=limit=0.79:attack=1:release=60:level=disabled[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-ar', '48000', '-shortest', out], check=True)
    print('WROTE', out, dur)


if __name__ == '__main__':
    main(sys.argv[1])
