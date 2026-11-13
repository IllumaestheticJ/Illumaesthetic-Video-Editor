"""2D explainer graphics for the 'All cars flex' intro VO (rough cut 13.98-28.78 s).
usage: python flexgfx.py <out.mp4>   Schematic only: motion is exaggerated and labelled so; no numbers."""
import sys, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
FPS = 24000/1001; W, H, SS = 1920, 1080, 2
T1, T2, T3 = 4.16, 8.72, 14.80          # scene ends (s), matched to the VO sentences
BG, FG, DIM, RED, GOLD = '#262626', '#e8ecf2', '#7b8088', '#e5484d', '#d6a419'
def F(sz, wt='Bold'):
    c = subprocess.run(['fc-match', '-f', '%{file}', f'Inter Display:style={wt}'], capture_output=True, text=True).stdout
    return ImageFont.truetype(c, sz*SS)
f_h, f_l, f_s = F(30, 'SemiBold'), F(40, 'Bold'), F(26, 'Medium')
def ease(x): x = min(max(x, 0), 1); return x*x*(3-2*x)
yaw, pit = math.radians(-38), math.radians(24)
def proj(p, cx, cy, s):
    x, y, z = p; x2 = x*math.cos(yaw) - y*math.sin(yaw); y2 = x*math.sin(yaw) + y*math.cos(yaw)
    return (cx + s*x2)*SS, (cy - s*(z*math.cos(pit) + y2*math.sin(pit)))*SS
def twist(p, a, L):
    x, y, z = p; t = a*x/L; return (x, y*math.cos(t) - z*math.sin(t), y*math.sin(t) + z*math.cos(t))
def tub(d, cx, cy, s, amp, roof, L=4.0, Wd=1.7, Hh=.75, col=FG):
    n = 16; xs = [-L/2 + L*i/n for i in range(n+1)]
    def line(pts, w=3, c=col): d.line([proj(twist(p, amp, L), cx, cy, s) for p in pts], fill=c, width=w*SS, joint='curve')
    for y in (-Wd/2, Wd/2):
        line([(x, y, -Hh/2) for x in xs], 5); line([(x, y, Hh/2) for x in xs], 5)
    for i, x in enumerate(xs):
        if i % 2 == 0:
            line([(x, -Wd/2, -Hh/2), (x, Wd/2, -Hh/2)], 2, DIM)                      # floor ribs
            for y in (-Wd/2, Wd/2): line([(x, y, -Hh/2), (x, y, Hh/2)], 2 if 0 < i < n else 5)
    for x in (-L/2, L/2): line([(x, -Wd/2, -Hh/2), (x, Wd/2, -Hh/2)], 5); line([(x, -Wd/2, Hh/2), (x, Wd/2, Hh/2)], 5)
    if roof:
        for i, x in enumerate(xs):
            if i % 2 == 0: line([(x, -Wd/2, Hh/2), (x, Wd/2, Hh/2)], 3)
        line([(-L/2, -Wd/2, Hh/2), (L/2, Wd/2, Hh/2)], 3); line([(-L/2, Wd/2, Hh/2), (L/2, -Wd/2, Hh/2)], 3)
    return lambda p: proj(twist(p, amp, L), cx, cy, s)
def arrow(d, a, b, c=RED, w=7):
    d.line([a, b], fill=c, width=w*SS); ang = math.atan2(b[1]-a[1], b[0]-a[0]); h = 26*SS
    d.polygon([b, (b[0]-h*math.cos(ang-.45), b[1]-h*math.sin(ang-.45)), (b[0]-h*math.cos(ang+.45), b[1]-h*math.sin(ang+.45))], fill=c)
def loads(d, P, k, L=4.0, Wd=1.7, Hh=.75):
    for x, y, sgn in ((L/2, -Wd/2, 1), (L/2, Wd/2, -1), (-L/2, -Wd/2, -1), (-L/2, Wd/2, 1)):
        a = P((x, y, -Hh/2 - sgn*.9*k - sgn*.15)); b = P((x, y, -Hh/2 - sgn*.15)) if sgn > 0 else P((x, y, Hh/2 + .15))
        if sgn < 0: a = P((x, y, Hh/2 + .15 + .9*k))
        if k > .05: arrow(d, a, b)
def frame(t):
    im = Image.new('RGB', (W*SS, H*SS), BG); d = ImageDraw.Draw(im)
    d.text((90*SS, 70*SS), 'CHASSIS FLEX', font=f_h, fill=DIM); d.text(((W-90)*SS, 70*SS), 'Illustration, movement exaggerated', font=f_s, fill=DIM, anchor='ra')
    if t < T1:      # load in -> shell twists
        k = ease((t-.5)/1.2); a = .55*k*(.75 + .25*math.sin((t-1.7)*2.2)) if t > .5 else 0
        P = tub(d, 960, 520, 235, a, False); loads(d, P, k)
        d.text((W/2*SS, 940*SS), 'LOAD GOES IN AT THE WHEELS  →  THE SHELL TWISTS', font=f_l, fill=FG, anchor='mm')
    elif t < T2:    # front view: towers move, geometry changes
        u = t - T1; k = ease((u-.4)/1.3)*(.8 + .2*math.sin(u*2.4)); cx, gy = 960, 760; sp = 16*k
        def P(x, y): return (cx + x)*SS, (gy - y)*SS
        d.line([P(-330, 60), P(330, 60)], fill=FG, width=6*SS)                                   # crossmember
        for s in (-1, 1):
            top = (s*(250 + sp), 420 + s*6*k); d.line([P(s*250, 60), P(*top)], fill=FG, width=6*SS)   # tower
            d.ellipse([P(top[0]-16, top[1]+16), P(top[0]+16, top[1]-16)], outline=GOLD, width=5*SS)
            hub = (s*470, 170); d.line([P(s*250, 90), P(hub[0], 110)], fill=DIM, width=5*SS); d.line([P(top[0], top[1]-90), P(hub[0], 250 + 5*k)], fill=DIM, width=5*SS)
            d.line([P(top[0], top[1]), P(hub[0]-s*30, 150)], fill=GOLD, width=4*SS)             # damper
            tl = math.radians(s*4*k); wx, wy = hub[0] + s*40, 175
            d.line([P(wx - 150*math.sin(tl), wy - 150*math.cos(tl)), P(wx + 150*math.sin(tl), wy + 150*math.cos(tl))], fill=FG, width=44*SS)
        y = 520; arrow(d, P(-40, y), P(-(250 + sp) + 14, y), GOLD, 5); arrow(d, P(40, y), P(250 + sp - 14, y), GOLD, 5)
        d.text(P(0, y + 52), 'TOWER TO TOWER', font=f_s, fill=GOLD, anchor='mm'); d.line([P(-700, 22), P(700, 22)], fill='#444', width=3*SS)
        d.text((W/2*SS, 940*SS), 'SUSPENSION MOUNTING POINTS MOVE  →  VAGUE STEERING', font=f_l, fill=FG, anchor='mm')
    else:           # closed roof vs open top, same load
        u = t - T2; k = ease((u-.5)/1.3)*(.8 + .2*math.sin(u*2.2))
        P1 = tub(d, 500, 560, 185, .14*k, True); loads(d, P1, k*.8); P2 = tub(d, 1420, 560, 185, .62*k, False); loads(d, P2, k*.8)
        d.text((500*SS, 880*SS), 'FIXED ROOF', font=f_l, fill=FG, anchor='mm'); d.text((500*SS, 935*SS), 'closed box resists twist', font=f_s, fill=DIM, anchor='mm')
        d.text((1420*SS, 880*SS), 'OPEN TOP', font=f_l, fill=GOLD, anchor='mm'); d.text((1420*SS, 935*SS), 'same load, no roof to help', font=f_s, fill=DIM, anchor='mm')
    return im.resize((W, H), Image.LANCZOS)
if __name__ == '__main__':
    out = sys.argv[1]; n = int(round(T3*FPS))
    if len(sys.argv) > 2:
        for t in map(float, sys.argv[2:]): frame(t).save(f'{out}_{t:.1f}.jpg')
        sys.exit()
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24000/1001', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n): ff.stdin.write(frame(i/FPS).tobytes())
    ff.stdin.close(); ff.wait(); print(out, n, 'frames')
