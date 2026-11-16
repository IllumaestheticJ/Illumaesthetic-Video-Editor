"""Coilover explainers for script lines 13-17 (reference explainer: copy its structure for the others).
usage: gfx_coilovers.py [still]   -> <media>/gfx/L13.mp4 ... L17.mp4   (still: writes one check frame per line to <media>/gfx/chk/)
Everything shown is a general illustration of how a damper works: no values, clicks or rates."""
import sys, math, os
from gfx import *
G = 'coilovers'; C = COL[G]


def coilover(c, x, top, bot, travel, a=1.0, piston=True):
    """Cutaway coilover: body tube, shaft, piston, spring. travel 0 = extended, 1 = compressed (shaft pushed into the body)."""
    body_top = lerp(top + 150, top + 95, 0)                      # body is the lower tube
    shaft_top = top + 70 * travel
    c.line([(x, shaft_top), (x, body_top + 60 + 70 * travel)], fade(WHITE, a), 7)                 # shaft
    c.rect(x - 46, shaft_top - 14, x + 46, shaft_top, fill=fade(DIM, a), r=4)                      # top mount
    c.rect(x - 30, body_top, x + 30, bot, fill=fade(PANEL, a), outline=fade(C, a), width=3, r=10)  # body
    if piston:
        py = body_top + 60 + 70 * travel
        c.rect(x - 26, py - 9, x + 26, py + 9, fill=fade(C, a), r=3)                               # piston
    c.spring(x, shaft_top, body_top + 26, 6, 52, fade(C, a * 0.9), 5)
    c.rect(x - 58, body_top + 20, x + 58, body_top + 32, fill=fade(DIM, a), r=4)                   # spring perch
    c.circle(x, bot + 16, 16, outline=fade(DIM, a), width=5)                                       # lower eye


def L13(c, u, t):   # spring holds the car up; the damper controls how fast it moves
    c.header('HOW IT WORKS', 'Spring and damper', G, u)
    for k, (x, name, damp) in enumerate(((400, 'SPRING ONLY', 0.25), (880, 'SPRING + DAMPER', 2.6))):
        a = ease(seg(u, 0.05 + 0.1 * k, 0.2 + 0.1 * k)); tt = max(0, t - 1.0)
        y = 70 * math.exp(-damp * tt) * math.cos(7.5 * tt) if t > 1.0 else 70 * ease(seg(t, 0.3, 1.0))   # push down, release
        yb = 300 + y * (1 if t <= 1.0 else 1)
        c.rect(x - 110, yb - 70, x + 110, yb, fill=fade(PANEL, a), outline=fade(WHITE, a), width=3, r=14); c.label(x, yb - 35, 'CAR', 22, WHITE, a)
        c.spring(x - 45, yb, 520, 6, 26, fade(C, a), 5)
        if damp > 1:
            c.rect(x + 30, 430, x + 62, 520, fill=fade(PANEL, a), outline=fade(C, a), width=3, r=6); c.line([(x + 46, yb), (x + 46, 450 + (yb - 300) * 0.6)], fade(WHITE, a), 6)
        c.line([(x - 140, 520), (x + 140, 520)], fade(DIM, a), 4)
        c.label(x, 570, name, 22, C if damp > 1 else DIM, a)
    c.chip('MCS double-adjustable coilovers', G, u=u)


def dyno(c, u, t, mode):
    """Shock dyno: the damper is stroked by a crank on the left; the right plots damping force against shaft speed.
    Rebound is drawn above the axis, compression below (the usual dyno layout). mode: 'both' = one live trace,
    'one' = one adjuster (rebound curve sweeps, compression stays), 'two' = both adjusters sweep on their own.
    Illustrative curves only: no scales, no values, not a dyno of these dampers."""
    title = {'both': 'On a shock dyno', 'one': 'One knob', 'two': 'Two knobs: one for each'}[mode]
    c.header('HOW IT WORKS', title, G, u); a = ease(seg(u, 0.02, 0.14)); RB, CP = COL['steering'], C
    # --- rig: frame, load cell on top, crank underneath ---
    w = t * 3.2; x0 = 250; tr = 0.5 - 0.5 * math.cos(w)             # 0 extended .. 1 compressed
    vel = math.sin(w)                                                # + = compressing
    c.rect(x0 - 120, 150, x0 - 104, 600, fill=fade(GRID, a)); c.rect(x0 + 104, 150, x0 + 120, 600, fill=fade(GRID, a))
    c.rect(x0 - 120, 150, x0 + 120, 166, fill=fade(GRID, a)); c.rect(x0 - 26, 166, x0 + 26, 186, fill=fade(DIM, a), r=3)
    c.label(x0 + 60, 176, 'LOAD CELL', 15, DIM, a, 'lm')
    lift = 46 * tr; coilover(c, x0, 190, 500 - lift, tr * 0.9, a)
    cx, cy = x0, 560; c.circle(cx, cy, 30, outline=fade(DIM, a), width=4)
    px, py = cx + 22 * math.sin(w), cy + 22 * math.cos(w); c.line([(px, py), (x0, 516 - lift)], fade(WHITE, a), 5); c.circle(px, py, 6, fill=fade(WHITE, a))
    c.label(x0, 628, 'SHOCK DYNO', 17, DIM, a)
    # --- plot ---
    X0, X1, Y0, Y1 = 520, 1180, 170, 590; ym = (Y0 + Y1) / 2
    c.rect(X0, Y0, X1, Y1, fill=fade(PANEL, a), outline=fade(GRID, a), width=1.5, r=8)
    for k in range(1, 6): c.line([(X0 + (X1 - X0) * k / 6, Y0 + 8), (X0 + (X1 - X0) * k / 6, Y1 - 8)], fade(GRID, a), 1)
    c.line([(X0 + 14, ym), (X1 - 14, ym)], fade(DIM, a), 2); c.line([(X0 + 40, Y0 + 12), (X0 + 40, Y1 - 12)], fade(DIM, a), 2)
    c.label(X1 - 16, ym + 16, 'SHAFT SPEED', 15, DIM, a, 'rm'); c.label(X0 + 52, Y0 + 22, 'FORCE', 15, DIM, a, 'lm')
    c.label(X1 - 20, Y0 + 26, 'REBOUND', 20, RB, a, 'rm'); c.label(X1 - 20, Y1 - 26, 'COMPRESSION', 20, CP, a, 'rm')

    def curve(gain, sign, col, wd=4, al=1.0):          # digressive damper curve: steep at low speed, flatter after the knee
        pts = []
        for i in range(41):
            v = i / 40; f = gain * (1 - math.exp(-4.2 * v)) * (0.72 + 0.28 * v)
            pts.append((X0 + 40 + v * (X1 - X0 - 70), ym - sign * f * (ym - Y0 - 30)))
        c.line(pts, fade(col, a * al, PANEL), wd); return pts
    if mode == 'both':
        r, k = curve(0.78, 1, RB), curve(0.5, -1, CP)
        v = abs(vel); i = int(v * 40); p = (k if vel > 0 else r)[i]; c.circle(p[0], p[1], 8, fill=fade(WHITE, a))
        c.label(X0, Y0 - 18, 'wheel pushed up = compression      wheel comes back down = rebound', 15, DIM, ease(seg(u, 0.2, 0.4)), 'lm')
    else:
        s1 = 0.5 + 0.5 * math.sin(t * 1.5); s2 = 0.5 + 0.5 * math.sin(t * 1.1 + 2.0)
        for g in (0.5, 0.64, 0.78, 0.92): curve(g, 1, RB, 1.5, 0.3)
        curve(lerp(0.5, 0.92, s1), 1, RB)
        if mode == 'two':
            for g in (0.3, 0.42, 0.54, 0.66): curve(g, -1, CP, 1.5, 0.3)
            curve(lerp(0.3, 0.66, s2), -1, CP)
            c.knob(430, 300, 34, s1 * 270 - 135, RB, a, 'REBOUND'); c.knob(430, 470, 34, s2 * 270 - 135, CP, a, 'COMPRESSION')
        else:
            curve(0.48, -1, DIM); c.knob(430, 385, 38, s1 * 270 - 135, RB, a, 'ONE KNOB')
            c.label(X1 - 20, Y1 - 52, 'whatever you get', 15, DIM, a, 'rm')
    c.label(X1, Y1 + 22, 'illustration, not a dyno of these dampers', 15, DIM, a, 'rm')
    c.chip('MCS double-adjustable coilovers', G, u=u)


def L14(c, u, t): dyno(c, u, t, 'both')
def L15(c, u, t): dyno(c, u, t, 'one')
def L16(c, u, t): dyno(c, u, t, 'two')


def L17(c, u, t):   # springs (with the sway bars) decide how much it leans; dampers control how fast
    c.header('HOW IT WORKS', 'How much, and how fast', G, u)
    a = ease(seg(u, 0.03, 0.15)); roll = 5.5 * ease(seg(u, 0.18, 0.55)); cx, gy = 380, 560
    c.line([(cx - 280, gy), (cx + 280, gy)], fade(DIM, a), 4)
    rot = car_rear(c, cx, gy, roll, a, xray=True)
    for sx in (-1, 1):                                    # a coilover each side, from the wheel up to the rolling body
        top = rot(sx * 104, 150)
        c.line([(cx + sx * 138, gy - 56), (cx + sx * 52, gy - 56)], fade(DIM, a), 5)          # lower arm, wheel to chassis
        c.spring(top[0], top[1], gy - 60, 5, 15, fade(C, a), 4.5); c.circle(top[0], top[1], 5, fill=fade(C, a))
    c.arrow(cx - 60, gy - 330, cx + 40 + roll * 6, gy - 330, fade(C, ease(seg(u, 0.2, 0.4))), 4, 12)
    b = ease(seg(u, 0.25, 0.45)); d = ease(seg(u, 0.55, 0.75))
    c.label(930, 290, 'HOW MUCH it leans and dives', 24, WHITE, b); c.label(930, 324, 'springs + sway bars', 20, C, b)
    c.label(930, 430, 'HOW FAST it gets there', 24, WHITE, d); c.label(930, 464, 'dampers', 20, COL['steering'], d)
    c.chip('Eibach springs on the MCS coilovers', G, u=u)


FN = {13: L13, 14: L14, 15: L15, 16: L16, 17: L17}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        os.makedirs(f'{M}/gfx/chk', exist_ok=True)
        for k, f in FN.items(): still(lambda c, u, t, f=f: f(c, u, 2.3), 0.7, f'{M}/gfx/chk/L{k}.png')
    else:
        for k, f in FN.items(): render(k, f)
