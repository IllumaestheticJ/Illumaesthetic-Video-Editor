"""bf-integra-385-combo v0 compositor.
Plates (Blender PNGs at 15 fps, 540x960) -> 30 fps 1080x1920, plus PIL overlays: Del & Eps stills (Higgsfield, model-sheet
reference), receipt, title, end card. C0222 (real gloss-black wing) cropped to 9:16. Music: "Get Low" from 0 s.
All prices from projects/_blackfriday/PRICES.md (BF liquidation sheet): wing $500, lip $100, combo $600 -> $385.
usage: python composite.py OUT.mp4
"""
import subprocess, sys, glob, os, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

M = '/home/user/media/bf-integra-385-combo'
R = f'{M}/work/render_v0'
TMP = f'{M}/work/comp_v0'; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1080, 1920, 30
LEN = [97, 70, 71, 71, 71, 70, 71, 71]          # shots 1-6 renders, 7 = C0222, 8 = end card
CUTS = np.cumsum([0] + LEN)                       # 0 97 167 238 309 380 450 521 592
OFFWHITE = (232, 236, 242, 255); ORANGE = (255, 122, 26, 255); YELLOW = (255, 210, 31, 255)
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


CH = {k: Image.open(f'{M}/chars/{k}.png').convert('RGBA') for k in ('eps_aim', 'eps_cheer', 'del_point')}


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
        char_layer(img, 'eps_aim', 300, 1700, 0.78, 6, fr)
        u = ease((fr - 4) / 10)
        if u > 0:
            ft = font(F_TITLE, 118)
            for i, line in enumerate(('WHAT $385', 'GETS YOU')):
                tracked(d, (W / 2, 250 + i * 135 + 30 * (1 - u)), line, ft, (232, 236, 242, int(255 * u)), track=6, anchor_center=True)
    elif shot == 2:
        char_layer(img, 'eps_cheer', 280, 1720, 0.72, 0, fr)
        receipt(img, fr, [(8, 'item', WING)], 500, 200)
    elif shot == 3:
        char_layer(img, 'eps_aim', 280, 1720, 0.72, 0, fr)
        receipt(img, fr + 100, [(0, 'item', WING), (108, 'item', LIP)], 500, 200)
    elif shot == 4:
        char_layer(img, 'del_point', 840, 1900, 0.80, 0, fr)
        receipt(img, fr + 200, [(0, 'item', WING), (0, 'item', LIP), (200, 'combo', {'name': 'COMBO', 'price': '$600', 'strike': 218}),
                                (236, 'bf', {'price': '$385'})], 40, 990, w=560)
        if fr >= 48:
            u = ease((fr - 48) / 8)
            tracked(d, (320, 1490), 'LESS THAN THE WING ALONE ($500)', font(F_MONO_R, 26), (232, 236, 242, int(230 * u)), track=1, anchor_center=True)
    elif shot == 8:
        logo = Image.open(f'{M}/logo/Epsilon+ Logo.png').convert('RGBA')
        u = ease(fr / 6)
        lw = 720; lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
        lg.putalpha(lg.split()[3].point(lambda v: int(v * u)))
        img.alpha_composite(lg, ((W - lw) // 2, 700))
        if fr >= 6:
            v = ease((fr - 6) / 8)
            tracked(d, (W / 2, 900), 'SPORT WING + TRUNK LIP', font(F_TITLE, 54), (232, 236, 242, int(255 * v)), track=5, anchor_center=True)
            tracked(d, (W / 2, 975), '$385', font(F_TITLE, 150), YELLOW[:3] + (int(255 * v),), track=4, anchor_center=True)
            tracked(d, (W / 2, 1160), 'BLACK FRIDAY', font(F_MONO, 40), (232, 236, 242, int(255 * v)), track=10, anchor_center=True)
            tracked(d, (W / 2, 1240), 'epsilon.plus', font(F_MONO_R, 40), (232, 236, 242, int(220 * v)), track=2, anchor_center=True)
    return img


def plate_frames(shot):
    """render PNGs (15 fps) -> list of 1080x1920 RGB arrays at 30 fps via ffmpeg minterpolate"""
    n = LEN[shot - 1]
    src = f'{R}/s{shot}'
    cmd = ['ffmpeg', '-v', 'error', '-framerate', '15', '-pattern_type', 'glob', '-i', f'{src}/f*.png',
           '-vf', 'minterpolate=fps=30:mi_mode=blend,scale=1080:1920:flags=lanczos,format=rgb24', '-frames:v', str(n),
           '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr


def c0222_frames():
    n = LEN[6]
    cmd = ['ffmpeg', '-v', 'error', '-i', f'{M}/footage/C0222.MP4', '-vf',
           'fps=30,scale=-2:1920:flags=lanczos,crop=1080:1920:iw*0.50-540:0,format=rgb24', '-frames:v', str(n), '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    if len(fr) < n: fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr


def main(out):
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                            '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', f'{TMP}/video.mp4'],
                           stdin=subprocess.PIPE)
    for shot in range(1, 9):
        if shot <= 6: plates = plate_frames(shot)
        elif shot == 7: plates = c0222_frames()
        else: plates = np.zeros((LEN[7], H, W, 3), np.uint8) + 3
        for i in range(LEN[shot - 1]):
            base = Image.fromarray(plates[i]).convert('RGBA')
            if shot != 7:  # never put anything over IRL footage
                base.alpha_composite(overlay(shot, i))
            enc.stdin.write(np.asarray(base.convert('RGB')).tobytes())
        print('shot', shot, 'frames', LEN[shot - 1], flush=True)
    enc.stdin.close(); enc.wait()
    dur = CUTS[-1] / FPS
    # music from the song's beginning, fade with the end card, -14 LUFS / TP < -1 (gain then limiter)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{TMP}/video.mp4', '-i', f'{M}/music/getlow.wav',
                    '-filter_complex', f'[1:a]atrim=0:{dur:.3f},afade=t=out:st={dur - 0.7:.3f}:d=0.7,'
                    'loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-ar', '48000', '-shortest', out], check=True)
    print('WROTE', out, dur)


if __name__ == '__main__':
    main(sys.argv[1])
