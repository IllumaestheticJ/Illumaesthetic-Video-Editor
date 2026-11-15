"""Brake explainers for script lines 34-37, 39 and 42 (same structure as gfx_coilovers.py).
usage: gfx_brakes.py [still]   -> <media>/gfx/L34.mp4 ... L42.mp4   (still: writes one check frame per line to <media>/gfx/chk/)
Everything shown is a general illustration of how brakes behave with heat: no temperatures, sizes or measured results."""
import sys, math, os
from gfx import *
G = 'brakes'; C = COL[G]; BAD = COL['bad']; GOOD = COL['good']
CHIP = 'Big brake kit from Fast Brakes'


def heatcol(h):
    """Cool -> hot colour ramp: DIM -> amber -> red."""
    h = clamp(h); return mix(DIM, C, h * 2) if h < 0.5 else mix(C, BAD, (h - 0.5) * 2)


def dashed(c, x0, y0, x1, y1, fill, width=2, dash=9, gap=7):
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) / (dash + gap)))
    for i in range(n + 1):
        s0 = i / (n + 1); s1 = s0 + dash / (dash + gap) / (n + 1)
        c.line([(lerp(x0, x1, s0), lerp(y0, y1, s0)), (lerp(x0, x1, s1), lerp(y0, y1, s1))], fill, width)


def brake(c, x, y, R, rot, heat=0.0, a=1.0, big=False, squeeze=0.0):
    """Brake seen from the side: disc face-on (rot = radians turned), caliper over the rim at the right.
    big = the kit caliper (longer, ribbed, more pistons, longer pad) on the SAME disc radius. squeeze 0..1 = pads clamping."""
    hc = heatcol(heat)
    c.circle(x, y, R, fill=fade(mix(PANEL, hc, 0.22 + 0.5 * heat), a), outline=fade(hc, a), width=4)        # friction ring
    for k in range(10):                                                                                      # holes show it turning
        t = rot + k * math.tau / 10; c.circle(x + 0.72 * R * math.cos(t), y + 0.72 * R * math.sin(t), R * 0.045, fill=fade(BG, a))
    c.circle(x, y, R * 0.44, fill=fade(PANEL, a), outline=fade(DIM, a), width=3)                             # hat
    for k in range(4):
        t = rot + k * math.tau / 4; c.circle(x + 0.24 * R * math.cos(t), y + 0.24 * R * math.sin(t), R * 0.05, fill=fade(DIM, a))
    c.circle(x, y, R * 0.09, fill=fade(DIM, a))
    ch = R * (1.5 if big else 0.82); ph = R * (1.16 if big else 0.5); col = C if big else WHITE
    x0, x1 = x + R * 0.5, x + R + R * 0.18
    c.rect(x0, y - ch / 2, x1, y + ch / 2, fill=fade(PANEL, a), outline=fade(col, a), width=4 if big else 2.5, r=R * 0.12)   # caliper
    px0, px1 = x + R * 0.60, x + R * 0.96
    c.rect(px0, y - ph / 2, px1, y + ph / 2, fill=fade(mix(GRID, hc if heat > 0.05 else DIM, 0.35 + 0.45 * squeeze), a), outline=fade(DIM, a), width=1.5, r=3)   # pad
    n = 3 if big else 1
    for k in range(n):                                                                                       # pistons
        py = y + (k - (n - 1) / 2) * ph / n
        c.circle((px0 + px1) / 2, py, R * 0.115, fill=fade(mix(PANEL, col, 0.25 + 0.6 * squeeze), a), outline=fade(col, a), width=2)
    if big:                                                                                                  # stiffening ribs
        for sy in (-1, 1):
            yy = y + sy * (ph / 2 + (ch - ph) / 4); c.line([(x0 + 8, yy), (x1 - 8, yy)], fade(C, a), 4)


def shimmer(c, x, y0, w, h, heat, t, n=5):
    """Wavy heat lines rising from y0 (bottom) over a width w; strength follows heat."""
    if heat <= 0.02: return
    for i in range(n):
        xi = x - w / 2 + w * (i + 0.5) / n; prev = None
        for j in range(15):
            s = j / 14; p = (xi + 7 * math.sin(s * 7 - t * 2.4 + i * 1.9), y0 - h * s)
            if prev: c.line([prev, p], fade(heatcol(heat), heat * (1 - s) * 0.9), 3)
            prev = p


def pedal(c, px, py, L, ang, a=1.0, col=WHITE):
    """Brake pedal from the side: pivot at the top, pad at the bottom; the foot pushes it to the right. Returns pad centre."""
    th = math.radians(ang); ex, ey = px + L * math.sin(th), py + L * math.cos(th)
    c.line([(px, py), (ex, ey)], fade(col, a), 7)
    c.line([(ex - 20 * math.cos(th), ey + 20 * math.sin(th)), (ex + 20 * math.cos(th), ey - 20 * math.sin(th))], fade(col, a), 10)   # pad
    c.rect(px - 22, py - 14, px + 22, py - 6, fill=fade(DIM, a), r=3); c.circle(px, py, 8, fill=fade(PANEL, a), outline=fade(DIM, a), width=3)
    return ex, ey


def L34(c, u, t):   # stock brakes do okay for one stop
    c.header('HOW IT WORKS', 'One stop is easy', G, u)
    a = ease(seg(u, 0.03, 0.15)); x, y, R = 400, 365, 150
    v = u if u < 0.42 else 0.42 + (min(u, 0.72) - 0.42) - (min(u, 0.72) - 0.42) ** 2 / 0.6              # spins, then slows to a stop
    sq = ease(seg(u, 0.38, 0.52))
    brake(c, x, y, R, v * 16, 0.0, a, False, sq)
    b = ease(seg(u, 0.12, 0.24))
    c.line([(x + R * 1.18 + 6, y - 40), (640, y - 70)], fade(DIM, b), 2); c.label(650, y - 70, 'CALIPER', 20, WHITE, b, 'lm')
    c.line([(x + R * math.cos(0.75) + 4, y + R * math.sin(0.75) + 3), (640, y + 110)], fade(DIM, b), 2); c.label(650, y + 110, 'DISC', 20, WHITE, b, 'lm')
    c.label(x, 572, 'STOCK BRAKE', 24, WHITE, a)
    d = ease(seg(u, 0.38, 0.5)); c.label(650, y + 20, 'PADS CLAMP', 20, C, d, 'lm')
    k = ease(seg(u, 0.66, 0.8)); kx, ky = 990, 340
    c.circle(kx, ky, 52, fill=fade(PANEL, k), outline=fade(C, k), width=3)
    p = seg(u, 0.72, 0.88); pts = [(kx - 24, ky + 2), (kx - 7, ky + 20), (kx + 26, ky - 18)]                  # tick draws on
    if p > 0:
        q = min(1, p * 2); c.line([pts[0], (lerp(pts[0][0], pts[1][0], q), lerp(pts[0][1], pts[1][1], q))], WHITE, 7)
        if p > 0.5:
            q = (p - 0.5) * 2; c.line([pts[1], (lerp(pts[1][0], pts[2][0], q), lerp(pts[1][1], pts[2][1], q))], WHITE, 7)
    c.label(kx, ky + 88, 'ONE STOP', 24, WHITE, k); c.label(kx, ky + 118, 'DOES OKAY', 18, DIM, k)
    c.chip(CHIP, G, u=u)


def L35(c, u, t):   # again and again: speed turns into heat
    c.header('HOW IT WORKS', 'Lap after lap', G, u)
    a = ease(seg(u, 0.03, 0.14)); x, y, R, N = 350, 405, 130, 8
    s = seg(u, 0.14, 0.92) * N; k = min(N - 1, int(s)); f = s - k if s < N else 1.0
    heat = (k + ease(f)) / N; sq = math.sin(math.pi * f) ** 2 if 0 < s < N else 0
    shimmer(c, x, y - R - 8, 2 * R, 95, heat, t)
    brake(c, x, y, R, t * 1.6, heat, a, False, sq)
    c.label(x + 12, 588, 'STOCK BRAKE', 22, WHITE, a)
    b = ease(seg(u, 0.08, 0.2)); px = 700
    c.label(px - 14, 262, 'STOP AFTER STOP', 20, WHITE, b, 'lm')
    for i in range(N):
        fill = ease(clamp(s - i)); hc = heatcol((i + 1) / N)
        c.circle(px + i * 56, 310, 15, fill=fade(mix(GRID, hc, fill), b), outline=fade(mix(DIM, hc, fill), b), width=2)
    d = ease(seg(u, 0.42, 0.56))
    c.label(px - 14, 440, 'SPEED', 30, WHITE, d, 'lm'); c.arrow(px + 112, 440, px + 196, 440, fade(heatcol(heat), d), 5, 16)
    c.label(px + 216, 440, 'HEAT', 30, heatcol(max(heat, 0.5)), d, 'lm')
    c.chip(CHIP, G, u=u)


def L36(c, u, t):   # stiffer caliper, bigger pad: takes much longer to fade
    c.header('HOW IT WORKS', 'Longer before it fades', G, u)
    R, y = 100, 290; fs = seg(u, 0.5, 0.82) * 0.97; fk = seg(u, 0.5, 1.0) * 0.42
    sq = (0.5 - 0.5 * math.cos(t * 2.6)) * seg(u, 0.46, 0.52)
    a0 = ease(seg(u, 0.03, 0.14)); a1 = ease(seg(u, 0.08, 0.2)); g = ease(seg(u, 0.14, 0.26)) * 0.5
    dashed(c, 250, y - R, 1000, y - R, fade(DIM, g), 1.5); dashed(c, 250, y + R, 1000, y + R, fade(DIM, g), 1.5)   # same disc size on both
    for x, name, big, frac, a in ((330, 'STOCK', False, fs, a0), (900, 'BIG BRAKE KIT', True, fk, a1)):
        brake(c, x, y, R, t * 1.6, frac, a, big, sq)
        c.label(x + 9, y + R + 38, name, 22, C if big else WHITE, a)
        b = ease(seg(u, 0.4, 0.5)); bx, bw, by = x - 161, 340, 500; zone = 0.78
        c.bar(bx, by, bw, 20, frac * b, heatcol(frac), 'HEAT BUILDS', b)
        infade = ease(seg(frac, zone - 0.04, zone + 0.06))
        c.rect(bx + bw * zone, by - 7, bx + bw + 5, by + 27, outline=fade(mix(DIM, BAD, infade), b), width=2, r=8)
        c.label(bx + bw * (1 + zone) / 2 + 2, by + 46, 'FADE', 18, mix(DIM, BAD, infade), b)
    p = ease(seg(u, 0.2, 0.32)); q = ease(seg(u, 0.3, 0.42)); lx = 1046
    c.line([(1022, y - 62), (lx - 6, y - 62)], fade(DIM, p), 2); c.label(lx, y - 62, 'STIFFER CALIPER', 16, WHITE, p, 'lm')
    c.line([(1000, y + 30), (lx - 6, y + 30)], fade(DIM, q), 2); c.label(lx, y + 30, 'BIGGER PAD', 16, WHITE, q, 'lm')
    c.chip(CHIP, G, u=u)


def L37(c, u, t):   # same pedal at the end of the session as at the start
    c.header('HOW IT WORKS', 'Same pedal, start to finish', G, u)
    REST, FIRM, L, px = -30, 5, 130, 500
    again = ease(seg(u, 0.80, 0.86)) * (1 - ease(seg(u, 0.88, 0.96)))                    # both lift and press again together
    stopx = px + L * math.sin(math.radians(FIRM)) + 9
    la = ease(seg(u, 0.3, 0.42)); dashed(c, stopx, 168, stopx, 568, fade(C, la), 2.5)
    for k, (py, name, a0, p0, heat) in enumerate(((185, 'START OF SESSION', 0.04, 0.2, 0.0), (398, 'END OF SESSION', 0.44, 0.58, 0.85))):
        a = ease(seg(u, a0, a0 + 0.12)); press = ease(seg(u, p0, p0 + 0.16)) * (1 - 0.8 * again)
        ex, ey = pedal(c, px, py, L, lerp(REST, FIRM, press), a)
        c.arrow(ex - 92, ey, ex - 28, ey, fade(C, a * (0.35 + 0.65 * press)), 5, 14)       # foot pushing
        c.label(80, py + 62, name, 22, WHITE, a, 'lm')
        bx, by = 900, py + 62
        if heat: shimmer(c, bx, by - 50, 90, 36, heat * a, t, 4)
        brake(c, bx, by, 44, t * 1.6, heat, a, True, press)
        c.label(bx + 78, by, 'HOT' if heat else 'COOL', 18, heatcol(heat) if heat else DIM, a, 'lm')
    m = ease(seg(u, 0.66, 0.8)); c.label(stopx + 22, 362, 'SAME FIRM PEDAL', 22, C, m, 'lm')
    c.chip(CHIP, G, u=u)


def hose(c, x0, x1, y, hh, bulge, a, braided):
    """Flexible brake hose from the side; bulge = how far the wall swells out (px) in the middle."""
    n = 40; top = []; bot = []
    for i in range(n + 1):
        s = i / n; b = hh + bulge * math.sin(math.pi * s) ** 1.5; x = lerp(x0, x1, s); top.append((x, y - b)); bot.append((x, y + b))
    c.poly(top + bot[::-1], fill=fade((52, 56, 74) if not braided else PANEL, a))
    if braided:
        for i in range(0, n, 2):
            j = min(n, i + 2); c.line([top[i], bot[j]], fade((170, 176, 196), a), 1.5); c.line([bot[i], top[j]], fade((170, 176, 196), a), 1.5)
    c.line(top, fade(WHITE if braided else DIM, a), 3); c.line(bot, fade(WHITE if braided else DIM, a), 3)
    for xx in (x0, x1): c.rect(xx - 9, y - hh - 5, xx + 9, y + hh + 5, fill=fade(DIM, a), r=3)                # end fittings


def L39(c, u, t):   # rubber line swells with every press; braided stainless barely moves
    c.header('HOW IT WORKS', 'Brake lines', G, u)
    press = 0.5 - 0.5 * math.cos(t * 2.3); age = seg(u, 0.25, 0.5); px, L, REST, FIRM = 182, 104, -28, 4
    stopx = px + L * math.sin(math.radians(FIRM)) + 9
    rows = ((262, 'RUBBER LINE', 'SWELLS EVERY PRESS', False, 0.04, 11 + 8 * age, 17 + 9 * age, 'LONGER PEDAL', BAD),
            (462, 'BRAIDED STAINLESS', 'BARELY MOVES', True, 0.46, 1.5, 0, 'FIRMER PEDAL', GOOD))
    for yc, name, sub, braided, a0, bulge, extra, plabel, pcol in rows:
        a = ease(seg(u, a0, a0 + 0.12)); py = yc - 78
        dashed(c, stopx, py + 8, stopx, yc + 46, fade(DIM, a), 2)
        ex, ey = pedal(c, px, py, L, lerp(REST, FIRM + extra, press), a)
        c.arrow(ex - 68, ey, ex - 26, ey, fade(C, a * (0.3 + 0.7 * press)), 5, 13)
        mx = px + L * 0.75 * math.sin(math.radians(lerp(REST, FIRM + extra, press))); rodx = 300 + (mx - px) * 0.5
        c.rect(292, yc - 17, 372, yc + 17, fill=fade(PANEL, a), outline=fade(DIM, a), width=2.5, r=5)        # master cylinder
        c.line([(mx, yc), (rodx + 22, yc)], fade(WHITE, a), 4); c.rect(rodx + 20, yc - 12, rodx + 30, yc + 12, fill=fade(C, a), r=2)
        c.line([(372, yc), (450, yc)], fade(DIM, a), 5); c.line([(830, yc), (872, yc)], fade(DIM, a), 5)
        hose(c, 450, 830, yc, 15, bulge * press, a, braided)
        c.rect(872, yc - 26, 912, yc + 26, fill=fade(PANEL, a), outline=fade(DIM, a), width=2.5, r=6)        # caliper end
        if not braided:
            for sy in (-1, 1):
                yy = yc + sy * (15 + bulge * press + 6); c.arrow(640, yy, 640, yy + sy * 20, fade(BAD, a * press), 4, 10)
        b = ease(seg(u, a0 + 0.08, a0 + 0.2))
        c.label(940, yc - 14, name, 21, WHITE, b, 'lm'); c.label(940, yc + 16, sub, 16, DIM, b, 'lm')
        if not braided: c.label(640, yc + 78, 'WORSE WITH AGE', 16, DIM, ease(seg(u, 0.28, 0.4)))
        c.label(px + 20, yc + 72, plabel, 17, pcol, ease(seg(u, a0 + 0.14, a0 + 0.26)))
    c.chip(CHIP, G, u=u)


BUB = [(744, -5, 12, 0.0), (712, 6, 10, 1.3), (680, -6, 11, 2.1), (646, 5, 9, 0.7), (612, -5, 10, 2.9), (578, 6, 8, 1.9),
       (544, -5, 8, 0.4), (790, -14, 12, 1.1), (814, 12, 11, 2.5), (790, 15, 9, 0.2), (822, -13, 9, 1.7)]


def L42(c, u, t):   # fluid boils -> bubbles compress -> long pedal
    c.header('HOW IT WORKS', 'Why the fluid matters', G, u)
    a = ease(seg(u, 0.03, 0.15)); heat = ease(seg(u, 0.2, 0.6)); bub = ease(seg(u, 0.36, 0.72))
    press = 0.5 - 0.5 * math.cos(t * 2.6); px, py, L, REST, FIRM, yc = 200, 240, 130, -24, 3, 340
    ang = lerp(REST, FIRM + 30 * bub, press); stopx = px + L * math.sin(math.radians(FIRM)) + 9
    dashed(c, stopx, py + 10, stopx, py + L + 34, fade(DIM, a), 2)
    ex, ey = pedal(c, px, py, L, ang, a)
    c.arrow(ex - 80, ey, ex - 28, ey, fade(C, a * (0.3 + 0.7 * press)), 5, 14)
    fluid = mix(PANEL, C, 0.62); mx = px + L * 0.72 * math.sin(math.radians(ang)); rod = 306 + (mx - (px - 44)) * 0.4
    c.rect(300, yc - 24, 420, yc + 24, fill=fade(PANEL, a), outline=fade(WHITE, a), width=2.5, r=5)          # master cylinder
    c.rect(rod + 8, yc - 19, 416, yc + 19, fill=fade(fluid, a))
    c.line([(mx, yc), (rod, yc)], fade(WHITE, a), 4); c.rect(rod, yc - 20, rod + 10, yc + 20, fill=fade(WHITE, a), r=2)
    c.rect(418, yc - 18, 772, yc + 18, fill=fade(fluid, a)); c.line([(420, yc - 18), (770, yc - 18)], fade(WHITE, a), 2.5); c.line([(420, yc + 18), (770, yc + 18)], fade(WHITE, a), 2.5)
    hc = heatcol(heat)
    shimmer(c, 912, 196, 70, 52, heat * a, t, 3)
    c.rect(770, yc - 88, 968, yc + 88, fill=fade(PANEL, a), outline=fade(WHITE, a), width=3, r=14)           # caliper body (cut open)
    pm = 5 * press * (1 - 0.7 * bub)                                                                        # piston barely moves once it boils
    c.rect(774, yc - 30, 836 + pm, yc + 30, fill=fade(fluid, a))                                            # fluid chamber
    c.rect(836 + pm, yc - 32, 880 + pm, yc + 32, fill=fade(DIM, a), r=4)                                    # piston
    c.rect(880 + pm, yc - 48, 896 + pm, yc + 48, fill=fade(mix(GRID, hc, 0.6), a), r=2)                     # pads
    c.rect(928, yc - 48, 944, yc + 48, fill=fade(mix(GRID, hc, 0.6), a), r=2)
    c.rect(901, 204, 923, 486, fill=fade(mix(PANEL, hc, 0.3 + 0.6 * heat), a), outline=fade(hc, a), width=2.5, r=3)   # disc, edge-on
    for bx, dy, r, ph in BUB:
        rr = r * bub * (1 - 0.42 * press) * (0.85 + 0.15 * math.sin(t * 3 + ph * 3))                         # bubbles squash when you press
        if rr > 0.8: c.circle(bx + 2 * math.sin(t * 1.7 + ph), yc + dy, rr, fill=fade(BG, a), outline=fade(WHITE, a), width=1.5)
    b = ease(seg(u, 0.1, 0.22)); c.label(596, yc + 48, 'BRAKE FLUID', 17, DIM, b)
    h = ease(seg(u, 0.22, 0.36)); c.label(1000, yc - 20, 'HEAT FROM', 18, heatcol(max(heat, 0.5)), h, 'lm'); c.label(1000, yc + 6, 'THE BRAKE', 18, heatcol(max(heat, 0.5)), h, 'lm')
    f = ease(seg(u, 0.44, 0.58)); c.label(640, yc - 68, 'FLUID BOILS', 26, BAD, f)
    c.label(640, yc - 40, 'BUBBLES SQUASH', 16, DIM, ease(seg(u, 0.56, 0.68)))
    p = ease(seg(u, 0.62, 0.76)); c.label(px + 40, py + L + 70, 'LONG PEDAL', 24, BAD, p)
    c.chip('CSG pads + Halo P1 fluid', G, u=u)


FN = {34: L34, 35: L35, 36: L36, 37: L37, 39: L39, 42: L42}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        os.makedirs(f'{M}/gfx/chk', exist_ok=True)
        for k, f in FN.items(): still(lambda c, u, t, f=f: f(c, u, 2.3), 0.7, f'{M}/gfx/chk/L{k}.png')
    else:
        for k, f in FN.items(): render(k, f)
