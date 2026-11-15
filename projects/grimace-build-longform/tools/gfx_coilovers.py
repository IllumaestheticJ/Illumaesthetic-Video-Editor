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


def L14(c, u, t):   # compression / rebound
    c.header('HOW IT WORKS', 'Compression and rebound', G, u)
    ph = (t * 0.55) % 2; comp = ph < 1; tr = ease(ph) if comp else 1 - ease(ph - 1)
    coilover(c, 640, 150, 560, tr, ease(seg(u, 0, 0.1)))
    a1, a2 = (1.0, 0.25) if comp else (0.25, 1.0)
    c.arrow(430, 450, 430, 290, fade(C, a1), 6, 18); c.label(430, 480, 'COMPRESSION', 24, WHITE, a1); c.label(430, 508, 'wheel pushed up', 16, DIM, a1)
    c.arrow(850, 290, 850, 450, fade(COL['steering'], a2), 6, 18); c.label(850, 480, 'REBOUND', 24, WHITE, a2); c.label(850, 508, 'wheel comes back down', 16, DIM, a2)
    c.chip('MCS double-adjustable coilovers', G, u=u)


def knobs(c, u, t, double):
    c.header('HOW IT WORKS', 'Two knobs: one for each' if double else 'One knob', G, u)
    a = ease(seg(u, 0.02, 0.14)); coilover(c, 300, 170, 560, 0.35 + 0.25 * math.sin(t * 2.2), a)
    k1 = 0.5 + 0.4 * math.sin(t * 1.3); k2 = 0.5 + 0.4 * math.sin(t * 0.9 + 1.7)
    if double:
        c.knob(620, 300, 44, k1 * 270 - 135, COL['steering'], a, 'REBOUND'); c.knob(620, 480, 44, k2 * 270 - 135, C, a, 'COMPRESSION')
        c.bar(760, 290, 380, 22, k1, COL['steering'], 'REBOUND  (set on its own)', a); c.bar(760, 470, 380, 22, k2, C, 'COMPRESSION  (set on its own)', a)
    else:
        c.knob(620, 390, 50, k1 * 270 - 135, COL['steering'], a, 'ONE KNOB')
        c.bar(760, 320, 380, 22, k1, COL['steering'], 'REBOUND  (mostly what the knob changes)', a)
        c.bar(760, 450, 380, 22, 0.5, DIM, 'COMPRESSION  (whatever you get)', a)
    c.chip('MCS double-adjustable coilovers', G, u=u)


def L15(c, u, t): knobs(c, u, t, False)
def L16(c, u, t): knobs(c, u, t, True)


def L17(c, u, t):   # springs (with the sway bars) decide how much it leans; dampers control how fast
    c.header('HOW IT WORKS', 'How much, and how fast', G, u)
    a = ease(seg(u, 0.03, 0.15)); roll = 7 * ease(seg(u, 0.2, 0.55)); cx, cy = 400, 360
    import math as m
    r = m.radians(roll); cs, sn = m.cos(r), m.sin(r)
    def rot(x, y): return (cx + (x * cs - y * sn), cy + (x * sn + y * cs))
    c.poly([rot(-170, -60), rot(170, -60), rot(170, 20), rot(-170, 20)], fill=fade(PANEL, a), outline=fade(WHITE, a))
    c.label(*rot(0, -20), 'CAR, FROM BEHIND', 16, DIM, a)
    for sx in (-1, 1):
        bx, by = rot(sx * 130, 20); c.spring(bx, by, 480, 5, 20, fade(C, a), 5); c.circle(cx + sx * 150, 500, 30, outline=fade(DIM, a), width=8)
    c.line([(cx - 230, 532), (cx + 230, 532)], fade(DIM, a), 4)
    b = ease(seg(u, 0.25, 0.45)); d = ease(seg(u, 0.55, 0.75))
    c.label(900, 270, 'HOW MUCH it leans and dives', 24, WHITE, b); c.label(900, 304, 'springs + sway bars', 20, C, b)
    c.label(900, 420, 'HOW FAST it gets there', 24, WHITE, d); c.label(900, 454, 'dampers', 20, COL['steering'], d)
    c.chip('Eibach springs on the MCS coilovers', G, u=u)


FN = {13: L13, 14: L14, 15: L15, 16: L16, 17: L17}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        os.makedirs(f'{M}/gfx/chk', exist_ok=True)
        for k, f in FN.items(): still(lambda c, u, t, f=f: f(c, u, 2.3), 0.7, f'{M}/gfx/chk/L{k}.png')
    else:
        for k, f in FN.items(): render(k, f)
