"""The "epic journey" gag before the Miata Chop Shop visit (owner request, v9): a globe and a route build up as if the
trip is long, then a hard cut to the real map where a little car drives next door.
usage: python mapgag.py <media_dir> <frames> <out.mp4>      also writes <media_dir>/work/gag.wav (riser, swoosh, chime)
Needs <media_dir>/map/map_clean.png (owner's screenshot) and <media_dir>/sfx/riser.wav + swoosh.mp3 (Dropbox dump folder).
No distances or times on screen: nothing here is measured."""
import sys, os, math, subprocess, wave
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
M, NF, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
FPS = 24000/1001; W, H, SS = 1920, 1080, 2; TA = 2.6; SR = 48000           # TA: length of the build-up; the map gets the rest
BG, FG, DIM, RED, GOLD = '#0d0f12', '#e8ecf2', '#7b8088', '#e5484d', '#d6a419'
def F(sz, wt='Bold'):
    c = subprocess.run(['fc-match', '-f', '%{file}', f'Inter Display:style={wt}'], capture_output=True, text=True).stdout
    return ImageFont.truetype(c, int(sz*SS))
def ease(x): x = min(max(x, 0), 1); return x*x*(3 - 2*x)
def back(x, s=2.2): x = min(max(x, 0), 1) - 1; return x*x*((s + 1)*x + s) + 1          # overshoot pop
f_big, f_mid, f_sm, f_lab = F(64), F(34, 'SemiBold'), F(26, 'Medium'), F(30)
# ---------------------------------------------------------------- part A: globe
def globe(t):
    im = Image.new('RGB', (W*SS, H*SS), BG); d = ImageDraw.Draw(im)
    z = ease((t - (TA - 0.55))/0.55); R = (300 + 40*ease(t/TA))*(1 + 3.2*z*z); cx, cy = 960, 610 + 500*z*z; rot = 0.5*t + 2.2*z; tilt = math.radians(22)
    def P(lat, lon):
        x = math.cos(lat)*math.sin(lon + rot); y = math.sin(lat); zz = math.cos(lat)*math.cos(lon + rot)
        y, zz = y*math.cos(tilt) - zz*math.sin(tilt), y*math.sin(tilt) + zz*math.cos(tilt); return ((cx + R*x)*SS, (cy - R*y)*SS), zz
    def poly(pts, col, wd):
        seg = []
        for p, zz in pts + [((0, 0), -1)]:
            if zz > 0: seg.append(p)
            else:
                if len(seg) > 1: d.line(seg, fill=col, width=int(wd*SS), joint='curve')
                seg = []
    d.ellipse([(cx - R)*SS, (cy - R)*SS, (cx + R)*SS, (cy + R)*SS], fill='#12161b', outline='#3a424d', width=3*SS)
    for la in range(-75, 90, 15): poly([P(math.radians(la), math.radians(lo)) for lo in range(0, 365, 5)], '#2c343e', 1.5)
    for lo in range(0, 360, 15): poly([P(math.radians(la), math.radians(lo)) for la in range(-90, 95, 5)], '#2c343e', 1.5)
    # the "route": a long great-circle arc, lifted off the surface, drawn on while the globe turns
    a0, a1 = (math.radians(18), math.radians(-70) - 0.5*t), (math.radians(-12), math.radians(75) - 0.5*t); k = ease((t - 0.35)/1.5); n = 60; pts = []
    v0 = np.array([math.cos(a0[0])*math.sin(a0[1]), math.sin(a0[0]), math.cos(a0[0])*math.cos(a0[1])]); v1 = np.array([math.cos(a1[0])*math.sin(a1[1]), math.sin(a1[0]), math.cos(a1[0])*math.cos(a1[1])])
    om = math.acos(float(v0@v1))
    for i in range(int(n*k) + 1):
        u = i/n; v = (math.sin((1 - u)*om)*v0 + math.sin(u*om)*v1)/math.sin(om); h = 1 + 0.22*math.sin(math.pi*u)
        x, y, zz = v*h; lon = math.atan2(x, zz); lat = math.asin(max(-1, min(1, y/h))); (px, py), _ = P(lat, lon)
        px = cx*SS + (px - cx*SS)*h; py = cy*SS + (py - cy*SS)*h; pts.append((px, py))
    for i in range(0, len(pts) - 1, 2): d.line(pts[i:i+2], fill=GOLD, width=5*SS)
    if pts:
        r = 9*SS; d.ellipse([pts[0][0] - r, pts[0][1] - r, pts[0][0] + r, pts[0][1] + r], fill=FG)
        r = 11*SS; d.ellipse([pts[-1][0] - r, pts[-1][1] - r, pts[-1][0] + r, pts[-1][1] + r], fill=GOLD)
    al = ease(t/0.25)*(1 - z)
    if al > 0.02:
        ov = Image.new('RGB', im.size, BG); o = ImageDraw.Draw(ov); s = 'FINDING A STOCK MIATA'; w = o.textlength(s, font=f_big)
        o.text(((W*SS - w)/2, 96*SS), s, font=f_big, fill=FG)
        s = 'CALCULATING ROUTE' + '.'*(1 + int(t*3) % 3); w = o.textlength('CALCULATING ROUTE...', font=f_mid); o.text(((W*SS - w)/2, 184*SS), s, font=f_mid, fill=GOLD)
        mk = Image.new('L', im.size, 0); ImageDraw.Draw(mk).rectangle([0, 80*SS, W*SS, 240*SS], fill=int(255*al)); im.paste(ov, (0, 0), mk)
    return im.resize((W, H), Image.LANCZOS)
# ---------------------------------------------------------------- part B: the real map
src = cv2.imread(f'{M}/map/map_clean.png'); mk = np.zeros(src.shape[:2], np.uint8); cv2.circle(mk, (927, 975), 15, 255, -1)      # the owner's personal "home" pin does not go on YouTube
src = cv2.inpaint(src, mk, 5, cv2.INPAINT_TELEA); MW, MH = src.shape[1], src.shape[0]; MAP = Image.fromarray(src[:, :, ::-1])
START = (1065, 822); WAY = [START, (980, 802), (885, 802), (825, 722), (812, 602), (838, 502), (912, 402), (962, 316), (972, 266)]   # owner's red arrow, in map pixels
def spline(P, n=24):
    P = [P[0]] + P + [P[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = (np.array(q, float) for q in P[i-1:i+3])
        for j in range(n): u = j/n; out.append(0.5*((2*p1) + (-p0 + p2)*u + (2*p0 - 5*p1 + 4*p2 - p3)*u*u + (-p0 + 3*p1 - 3*p2 + p3)*u**3))
    return np.array(out + [np.array(P[-1], float)])
PATH = spline(WAY); CUM = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(PATH, axis=0).T))])
def car_sprite():
    L, Wd = 74*SS, 36*SS; im = Image.new('RGBA', (L + 8*SS, Wd + 8*SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im); o = 4*SS
    d.rounded_rectangle([o, o, o + L, o + Wd], radius=13*SS, fill='#c9302c', outline='#7d1512', width=2*SS)
    d.rounded_rectangle([o + L*0.30, o + 5*SS, o + L*0.72, o + Wd - 5*SS], radius=7*SS, fill='#20262d')                 # cabin (nose points +x)
    d.rounded_rectangle([o + L*0.40, o + 8*SS, o + L*0.60, o + Wd - 8*SS], radius=4*SS, fill='#a32420')                 # roof
    for y in (o + 3*SS, o + Wd - 9*SS): d.rounded_rectangle([o + L - 7*SS, y, o + L - 2*SS, y + 6*SS], radius=2*SS, fill='#fff3c4')
    return im
CAR = car_sprite()
def pill(d, xy, s, font, fill, fg='#ffffff', anchor='l', pad=(16, 9)):
    w = d.textlength(s, font=font); bb = font.getbbox(s); h = bb[3]; x, y = xy
    if anchor == 'c': x -= (w/2 + pad[0]*SS)
    d.rounded_rectangle([x, y, x + w + 2*pad[0]*SS, y + h + 2*pad[1]*SS], radius=(h/2 + pad[1]*SS), fill=fill); d.text((x + pad[0]*SS, y + pad[1]*SS - bb[1]/2), s, font=font, fill=fg)
    return w + 2*pad[0]*SS
T_GO, T_ARR = 0.45, 2.0                                                    # car leaves / arrives, seconds into the map
def mapframe(t):
    # 16:9 window on the map with a slow push towards the route
    z = 1.22 + 0.08*ease(t/3.5); cw = MW/z; ch = cw*9/16; x0 = 1010 - cw/2; y0 = max(500 - ch/2, 0); s = W*SS/cw
    im = MAP.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W*SS, H*SS), Image.LANCZOS).convert('RGB'); d = ImageDraw.Draw(im)
    X = lambda p: ((p[0] - x0)*s, (p[1] - y0)*s)
    k = ease((t - T_GO)/(T_ARR - T_GO)); dist = k*CUM[-1]; i = int(np.searchsorted(CUM, dist)); i = min(max(i, 1), len(PATH) - 1)
    u = (dist - CUM[i-1])/max(CUM[i] - CUM[i-1], 1e-6); pos = PATH[i-1] + (PATH[i] - PATH[i-1])*u
    j0, j1 = max(i - 4, 0), min(i + 4, len(PATH) - 1); hd = math.degrees(math.atan2(-(PATH[j1][1] - PATH[j0][1]), PATH[j1][0] - PATH[j0][0]))
    trail = [X(p) for p in PATH[:i]] + [X(pos)]
    if len(trail) > 1:
        d.line(trail, fill='#ffffff', width=13*SS, joint='curve'); d.line(trail, fill=RED, width=7*SS, joint='curve')
    sx, sy = X(START); r = 9*SS; d.ellipse([sx - r, sy - r, sx + r, sy + r], fill='#ffffff', outline=RED, width=4*SS)
    a = back(t/0.3)
    if a > 0: lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); pill(ImageDraw.Draw(lay), (sx + 34*SS, sy + 26*SS), 'OUR SHOP', f_lab, '#20262d'); im.paste(lay, (0, int((1 - a)*14*SS)), lay)
    spr = CAR.rotate(hd, resample=Image.BICUBIC, expand=True); px, py = X(pos); im.paste(spr, (int(px - spr.width/2), int(py - spr.height/2)), spr)
    ex, ey = X(PATH[-1] + np.array([6, -40])); ta = t - T_ARR      # pin lands just past the car, on the building
    if ta > -0.15:                                                         # destination pin drops in as the car pulls up
        b = back((ta + 0.15)/0.35, 3.0); drop = (1 - min(b, 1.0))*-140*SS; sc = 1 + 0.25*max(b - 1, 0); R = 26*SS*sc; ty = ey - 62*SS*sc + drop
        d.polygon([(ex - R*0.72, ty + R*0.62), (ex + R*0.72, ty + R*0.62), (ex, ey + drop)], fill=RED); d.ellipse([ex - R, ty - R, ex + R, ty + R], fill=RED); d.ellipse([ex - R*0.4, ty - R*0.4, ex + R*0.4, ty + R*0.4], fill='#ffffff')
    if ta > 0.1:
        a = back((ta - 0.1)/0.3); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        pill(ld, (ex + 44*SS, ey - 96*SS), 'MIATA CHOP SHOP', f_lab, RED)
        if ta > 0.45: pill(ld, (ex + 44*SS, ey - 30*SS), 'NEXT DOOR', f_big, '#20262d', GOLD, pad=(26, 16))
        im.paste(lay, (0, int((1 - min(a, 1))*14*SS)), lay)
    # navigation banner
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay); msg = 'You have arrived.' if ta > 0.1 else ('Head next door' if t > T_GO else 'Starting route')
    ld.rounded_rectangle([60*SS, 54*SS, 640*SS, 150*SS], radius=22*SS, fill='#0f5c3f'); ld.text((92*SS, 78*SS), msg, font=F(44), fill='#ffffff'); im.paste(lay, (0, 0), lay)
    return im.resize((W, H), Image.LANCZOS)
# ---------------------------------------------------------------- sound
def sfx():
    n = int(NF/FPS*SR) + 1; out = np.zeros(n, np.float32)
    def load(p):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout; return np.frombuffer(raw, np.float32).copy()
    def put(x, t0, peak):
        x = x*peak/(np.abs(x).max() + 1e-9); p = int(t0*SR); x = x[:n - p]; out[p:p + len(x)] += x
    r = load(f'{M}/sfx/riser.wav'); pk = int(np.argmax(np.convolve(np.abs(r), np.ones(2400)/2400, 'same'))); end = min(pk + int(.10*SR), len(r)); r = r[max(end - int(TA*SR), 0):end]
    r[:int(.3*SR)] *= np.linspace(0, 1, int(.3*SR)); r[-int(.04*SR):] *= np.linspace(1, 0, int(.04*SR)); put(r, TA - len(r)/SR, 0.42)              # the peak lands on the cut, then nothing
    s = load(f'{M}/sfx/swoosh.mp3'); k = np.nonzero(np.abs(s) > 0.02*np.abs(s).max())[0]; s = s[k[0]:k[-1]]; put(s, TA + T_GO, 0.30)
    tt = np.arange(int(.9*SR))/SR; ch = sum(a*np.sin(2*np.pi*f*np.maximum(tt - dl, 0))*np.exp(-np.maximum(tt - dl, 0)*6)*(tt >= dl) for f, a, dl in ((880, 1, 0), (1318.5, .8, .13)))
    put(ch.astype(np.float32), TA + T_ARR + 0.02, 0.22)                    # two-note "arrived" chime (synthesised)
    w = wave.open(f'{M}/work/gag.wav', 'w'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.repeat(out[:, None], 2, 1)*32767).astype(np.int16).tobytes())
if __name__ == '__main__':
    sfx()
    if OUT.endswith('.jpg'):                                               # contact sheet for checking
        ts = [0.3, 1.2, 2.0, 2.45, TA + 0.1, TA + 1.0, TA + 1.7, TA + 2.1, TA + 2.7, NF/FPS - 0.1]; sh = Image.new('RGB', (960*2, 540*5))
        for i, t in enumerate(ts): sh.paste((globe(t) if t < TA else mapframe(t - TA)).resize((960, 540)), (960*(i % 2), 540*(i//2)))
        sh.save(OUT, quality=88); sys.exit()
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24000/1001', '-i', '-', '-frames:v', str(NF), '-c:v', 'libx264', '-preset', 'veryfast',
                            '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '24000/1001', '-video_track_timescale', '24000', OUT], stdin=subprocess.PIPE)
    for i in range(NF): t = i/FPS; enc.stdin.write((globe(t) if t < TA else mapframe(t - TA)).tobytes())
    enc.stdin.close(); enc.wait()
