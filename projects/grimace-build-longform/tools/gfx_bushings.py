"""Bushing explainers for script lines 21-24 and 30 (same structure as gfx_coilovers.py).
Lines 21, 23, 24 share one front view of a double-wishbone corner (two arms, two ball joints, upright); 22 and 30 are cross-sections.
usage: gfx_bushings.py [still]   -> <media>/gfx/L21.mp4 ... L24.mp4, L30.mp4   (still: one check frame per line in <media>/gfx/chk/)
Everything shown is a general illustration of how a suspension bushing works: no values, no measured results."""
import sys, math, os, random
from gfx import *
G = 'bushings'; C = COL[G]
RUB = (104, 110, 134)                 # neutral rubber grey
POLY = mix(PANEL, C, 0.6)             # polyurethane, in the group accent
ARM = mix(WHITE, DIM, 0.35)
CHIP = 'Whiteline polyurethane bushings'


def dash(c, x0, y0, x1, y1, col, width=2, on=11, off=9):
    n = math.hypot(x1 - x0, y1 - y0); k = 0.0
    while k < n:
        e = min(n, k + on)
        c.line([(lerp(x0, x1, k / n), lerp(y0, y1, k / n)), (lerp(x0, x1, e / n), lerp(y0, y1, e / n))], col, width)
        k += on + off


def bush(c, x, y, R, r, ring, a=1.0, sx=0.0, sy=0.0, shell=DIM):
    """Bushing cross-section: outer shell (R), elastic ring, inner sleeve (r) shifted by sx, sy from the centre."""
    c.circle(x, y, R, fill=fade(ring, a), outline=fade(shell, a), width=max(2.5, R * 0.1))
    c.circle(x + sx, y + sy, r, fill=fade(BG, a), outline=fade(WHITE, a), width=max(2, r * 0.22))
    c.circle(x + sx, y + sy, r * 0.38, fill=fade(DIM, a))


# Front view of one double-wishbone corner, in local units (x outboard, y down, origin on the chassis side).
PL, PU = (0.0, 85.0), (40.0, -75.0)            # lower / upper arm pivots on the chassis (bushing sleeves, bolted still)
LBJ0, UBJ0 = (290.0, 100.0), (268.0, -80.0)    # lower / upper ball joints on the upright: two different points
TX0, TX1, TY0, TY1 = 318.0, 408.0, -160.0, 170.0   # tyre section; the ground is at TY1
WX, HUBY = 363.0, 5.0                          # wheel centre plane, hub height
L_LO = math.hypot(LBJ0[0] - PL[0], LBJ0[1] - PL[1]); L_UP = math.hypot(UBJ0[0] - PU[0], UBJ0[1] - PU[1])
L_KN = math.hypot(UBJ0[0] - LBJ0[0], UBJ0[1] - LBJ0[1])
PHI0 = math.atan2(LBJ0[1] - PL[1], LBJ0[0] - PL[0]); KN0 = math.atan2(UBJ0[1] - LBJ0[1], UBJ0[0] - LBJ0[0])


def solve(d):
    """Linkage under bushing deflection d (local units). Cornering load at the contact patch pushes the lower arm inboard
    (compression) and pulls the upper arm outboard (tension), so the lower bushing shell moves in by d and the upper one out by
    0.55 d. Arms and upright stay rigid; the lower arm swings just enough to keep the tyre on the ground.
    Returns (lower shell centre, upper shell centre, lower ball joint, upper ball joint, upright rotation)."""
    sl = (PL[0] - d, PL[1]); su = (PU[0] + 0.55 * d, PU[1])
    def pose(phi):
        lb = (sl[0] + L_LO * math.cos(phi), sl[1] + L_LO * math.sin(phi))
        dx, dy = su[0] - lb[0], su[1] - lb[1]; D = math.hypot(dx, dy)
        q = (L_KN ** 2 - L_UP ** 2 + D * D) / (2 * D); h = math.sqrt(max(0.0, L_KN ** 2 - q * q))
        mx, my = lb[0] + q * dx / D, lb[1] + q * dy / D
        ub = (mx + h * dy / D, my - h * dx / D)                                              # the outboard intersection
        if ub[0] < mx - h * dy / D: ub = (mx - h * dy / D, my + h * dx / D)
        return lb, ub, math.atan2(ub[1] - lb[1], ub[0] - lb[0]) - KN0
    def patch_y(phi):
        lb, ub, th = pose(phi); y = TY1 - LBJ0[1]                                          # lowest tyre corner sits on the ground
        return lb[1] + max((x - LBJ0[0]) * math.sin(th) for x in (TX0, TX1)) + y * math.cos(th) - TY1
    phi = PHI0
    for _ in range(8):
        e = patch_y(phi); g = (patch_y(phi + 1e-4) - e) / 1e-4
        if abs(g) < 1e-9: break
        phi -= e / g
    lb, ub, th = pose(phi)
    return sl, su, lb, ub, th


def assembly(c, ox, oy, s, load, a=1.0, ring=RUB, k=1.0, wheelcol=C, setline=0.0, chassis_label=True):
    """Front view of one corner: chassis block, upper and lower A-arm each on its own bushing, upright (knuckle) between the two
    ball joints, hub and tyre on the upright. load 0..1 pushes at the contact patch; k = how much the bushings give.
    Returns a dict of screen points for labels."""
    sl, su, lb, ub, th = solve(13.0 * load * k); cs, sn = math.cos(th), math.sin(th)
    def F(x, y): return (ox + x * s, oy + y * s)                                            # fixed to the chassis
    def T(x, y):                                                                            # rigid with the upright
        x, y = x - LBJ0[0], y - LBJ0[1]; return F(lb[0] + x * cs - y * sn, lb[1] + x * sn + y * cs)
    c.rect(*F(-170, -150), *F(-55, 150), fill=fade(PANEL, a), outline=fade(DIM, a), width=2.5, r=10 * s)
    if chassis_label: c.label(*F(-112, 0), 'CHASSIS', 16, DIM, a)
    for p in (PL, PU): c.line([F(-57, p[1]), F(*p)], fade(DIM, a), 12 * s)                  # mounting brackets
    c.line([F(TX0 - 40, TY1 + 2), F(TX1 + 40, TY1 + 2)], fade(DIM, a * 0.8), 2)             # ground
    if setline > 0: dash(c, *F(WX, TY0 - 26), *F(WX, TY1), fade(WHITE, setline * a), 2)
    tyre = [T(TX0, TY0), T(TX1, TY0), T(TX1, TY1), T(TX0, TY1)]
    c.poly(tyre, fill=fade(PANEL, a)); c.line(tyre + tyre[:1], fade(WHITE, a), 2.5)
    for tx in (TX0 + 18, TX0 + 36, TX1 - 36, TX1 - 18):                                     # tread grooves, seen from the front
        c.line([T(tx, TY0 + 6), T(tx, TY1 - 6)], fade(GRID, a), 2)
    if wheelcol: c.line([T(WX, TY0 - 22), T(WX, TY1)], fade(wheelcol, a), 3)                # which way the wheel leans
    c.line([F(*sl), F(*lb)], fade(ARM, a), 13 * s); c.line([F(*su), F(*ub)], fade(ARM, a), 13 * s)   # the two arms
    hub = T(lerp(LBJ0[0], UBJ0[0], (LBJ0[1] - HUBY) / (LBJ0[1] - UBJ0[1])), HUBY)
    c.line([hub, T(WX, HUBY)], fade(WHITE, a), 9 * s)                                       # hub / spindle
    c.line([F(*lb), F(*ub)], fade(WHITE, a), 15 * s)                                        # upright
    c.circle(*T(WX, HUBY), 9 * s, fill=fade(BG, a), outline=fade(WHITE, a), width=3)
    for p in (lb, ub): c.circle(*F(*p), 11 * s, fill=fade(BG, a), outline=fade(ARM, a), width=3)     # ball joints
    for sh, fx in ((sl, PL), (su, PU)):
        bx, by = F(*sh); px, py = F(*fx); bush(c, bx, by, 40 * s, 12 * s, ring, a, px - bx, py - by)
    return dict(lo=F(*sl), up=F(*su), lbj=F(*lb), ubj=F(*ub), hub=hub, wheel=T(WX, HUBY), patch=T(TX1, TY1 - 22),
                top=T(WX, TY0), out=T(TX1, HUBY))


def L21(c, u, t):   # every arm joins the chassis through one of these
    c.header('HOW IT WORKS', 'Where the arms meet the car', G, u)
    a = ease(seg(u, 0.04, 0.2)); ox, oy = 380, 372
    p = assembly(c, ox, oy, 1.0, 0.0, a, wheelcol=None)
    la = ease(seg(u, 0.14, 0.28))
    c.label(ox + 172, oy - 112, 'UPPER ARM', 18, WHITE, la); c.label(ox + 160, oy + 128, 'LOWER ARM', 18, WHITE, la)
    ua = ease(seg(u, 0.2, 0.34)); hx, hy = p['hub']
    c.line([(hx - 62, hy), (hx - 12, hy)], fade(DIM, ua), 2); c.label(hx - 72, hy, 'UPRIGHT', 18, WHITE, ua, 'rm')
    c.label(p['out'][0] + 22, p['out'][1], 'WHEEL', 18, DIM, ease(seg(u, 0.24, 0.38)), 'lm')
    for k, ((bx, by), ly) in enumerate(((p['up'], oy - 150), (p['lo'], oy + 162))):
        h = ease(seg(u, 0.46 + 0.2 * k, 0.62 + 0.2 * k))
        if h > 0:
            q = 0.5 + 0.5 * math.sin(t * 2.0 - k * 1.2)                                     # slow breathing halo
            c.circle(bx, by, 47 + 7 * q, outline=fade(C, h * (0.9 - 0.4 * q)), width=3)
            c.circle(bx, by, 40, outline=fade(C, h), width=5)
            c.label(bx, ly, 'BUSHING', 20, C, h)
    c.chip(CHIP, G, u=u)


_rng = random.Random(7)
CRACKS = [(_rng.uniform(0, 6.283), _rng.uniform(0.55, 1.0), [_rng.uniform(-0.09, 0.09) for _ in range(6)], _rng.uniform(0, 0.55)) for _ in range(13)]


def L22(c, u, t):   # factory rubber: goes soft and cracks with age
    c.header('HOW IT WORKS', 'Factory rubber', G, u)
    a = ease(seg(u, 0.04, 0.18)); x, y, R, r = 420, 378, 170, 52
    age = seg(u, 0.38, 0.95); soft = ease(age)
    sy = 14 * soft + 3 * soft * math.sin(t * 1.4)                                           # tired rubber lets the sleeve sag
    c.circle(x, y, R, fill=fade(mix(RUB, (74, 74, 84), soft), a), outline=fade(DIM, a), width=14)
    for ang, ln, jit, start in CRACKS:                                                      # cracks creep outward from the sleeve
        g = ease(seg(age, start, start + 0.45))
        if g <= 0: continue
        n = 6; pts = []
        for i in range(n + 1):
            f = i / n
            if f > g + 1e-6: break
            rad = lerp(r + 4, r + 4 + (R - r - 22) * ln, f); aa = ang + (jit[i - 1] if 0 < i else 0)
            pts.append((x + rad * math.cos(aa), y + sy * (1 - f) + rad * math.sin(aa)))
        if len(pts) > 1: c.line(pts, fade(BG, a), 3.5)
    c.circle(x, y + sy, r, fill=fade(BG, a), outline=fade(WHITE, a), width=9)
    c.circle(x, y + sy, 18, fill=fade(DIM, a))
    for k, (name, col, size, px, py, ly) in enumerate((('OUTER SHELL', DIM, 20, x + R * 0.78, y - R * 0.62, 250),
                                                       ('RUBBER', WHITE, 30, x + 112, y - 20, 360),
                                                       ('INNER SLEEVE', DIM, 20, x + r * 0.8, y + r * 0.6 + sy, 470))):
        b = ease(seg(u, 0.14 + 0.08 * k, 0.28 + 0.08 * k))
        if b > 0:                                                                           # leader grows in from the label
            c.line([(720, ly), (lerp(720, px, b), lerp(ly, py, b))], DIM, 2); c.circle(lerp(720, px, b), lerp(ly, py, b), 5 * b, fill=WHITE)
        c.label(736, ly, name, size, col, b, 'lm')
    c.label(736, 398, 'SOFT AND CRACKED', 20, C, ease(seg(u, 0.6, 0.8)), 'lm')
    c.chip(CHIP, G, u=u)


def L23(c, u, t):   # load it up in a corner: the rubber squishes and the wheel moves
    c.header('HOW IT WORKS', 'Rubber squishes under load', G, u)
    a = ease(seg(u, 0.04, 0.18)); ox, oy = 300, 368
    load = ease(seg(u, 0.26, 0.56)) * (0.86 + 0.14 * math.sin(t * 1.5))
    sl = ease(seg(u, 0.1, 0.24))
    p = assembly(c, ox, oy, 1.0, load, a, setline=sl)
    c.label(ox + WX, oy + TY0 - 44, 'WHERE YOU SET IT', 18, WHITE, sl)
    la = ease(seg(u, 0.2, 0.34)); ax, ay = p['patch'][0] + 10, oy + TY1 - 22                 # the arrow leans on the contact patch
    c.arrow(ax + 170, ay, ax, ay, fade(C, la), 7, 20)
    c.label(ax + 24, ay - 30, 'CORNERING LOAD', 19, WHITE, la, 'lm')
    c.label(ox + 20, 580, 'RUBBER SQUISHES', 20, C, ease(seg(u, 0.42, 0.6)))
    c.label(ox + WX, 580, 'WHEEL TILTS AND MOVES', 20, C, ease(seg(u, 0.6, 0.78)))
    c.chip(CHIP, G, u=u)


def L24(c, u, t):   # same load: rubber gives a lot, polyurethane gives a little
    c.header('HOW IT WORKS', 'Rubber vs polyurethane', G, u)
    load = ease(seg(u, 0.3, 0.58)) * (0.86 + 0.14 * math.sin(t * 1.5)); s, oy = 0.62, 340
    for k, (ox, name, sub, col, give) in enumerate(((190, 'RUBBER', 'WHEEL MOVES AROUND', COL['bad'], 1.0),
                                                    (800, 'POLYURETHANE', 'WHEEL STAYS CLOSE', COL['good'], 0.22))):
        a = ease(seg(u, 0.05 + 0.1 * k, 0.2 + 0.1 * k)); sl = ease(seg(u, 0.16 + 0.06 * k, 0.3 + 0.06 * k))
        p = assembly(c, ox, oy, s, load, a, mix(PANEL, col, 0.62), give, col, sl, chassis_label=False)
        la = ease(seg(u, 0.22, 0.36)); ax, ay = p['patch'][0] + 8, oy + (TY1 - 22) * s
        c.arrow(ax + 100, ay, ax, ay, fade(WHITE, la), 6, 17)
        c.label(ax + 16, ay - 24, 'SAME LOAD', 16, DIM, la, 'lm')
        c.label(ox + WX * s, oy + (TY0 - 44) * s, 'AS SET', 16, DIM, sl)
        c.label(ox + 80, 520, name, 26, col, a)
        c.label(ox + 80, 554, sub, 17, WHITE, ease(seg(u, 0.56 + 0.1 * k, 0.72 + 0.1 * k)))
    c.chip(CHIP, G, u=u)


def pivot(c, x, y, ang, a, kind):
    """Side view of one bushing with its arm swung by ang (radians). The sleeve is bolted still; the shell swings with the arm.
    kind: 'rubber' (bonded, shears), 'poly' (turns on a grease film), 'dry' (no grease)."""
    R, r = 80, 27; ring = RUB if kind == 'rubber' else mix(PANEL, COL['bad'], 0.55) if kind == 'dry' else POLY
    cs, sn = math.cos(ang), math.sin(ang)
    c.line([(x + (R - 4) * cs, y + (R - 4) * sn), (x + 196 * cs, y + 196 * sn)], fade(ARM, a), 22)       # arm
    c.circle(x + 196 * cs, y + 196 * sn, 15, fill=fade(BG, a), outline=fade(ARM, a), width=5)
    c.circle(x, y, R, fill=fade(ring, a), outline=fade(ARM, a), width=9)
    for k in range(12):
        p = k * math.pi / 6 + 0.26; q = p + ang; pi_ = p if kind == 'rubber' else q        # rubber: inner end stays with the sleeve
        r0 = r + (3 if kind == 'rubber' else 12)
        c.line([(x + r0 * math.cos(pi_), y + r0 * math.sin(pi_)), (x + (R - 12) * math.cos(q), y + (R - 12) * math.sin(q))], fade(BG, a * 0.85), 3)
    if kind == 'poly': c.circle(x, y, r + 7, outline=fade(WHITE, a), width=3.5)             # grease film
    c.circle(x, y, r, fill=fade(BG, a), outline=fade(WHITE, a), width=6)
    for p in (0.0, math.pi / 2):                                                            # bolt flats: the sleeve does not turn
        c.line([(x - 13 * math.cos(p), y - 13 * math.sin(p)), (x + 13 * math.cos(p), y + 13 * math.sin(p))], fade(DIM, a), 4)


def L30(c, u, t):   # rubber twists, polyurethane has to rotate; dry it sticks and squeaks
    c.header('HOW IT WORKS', 'Why the grease', G, u)
    A = math.radians(19); sw = A * math.sin(t * 1.5); y = 365
    a1 = ease(seg(u, 0.08, 0.22)); a2 = ease(seg(u, 0.24, 0.38)); a3 = ease(seg(u, 0.58, 0.72))
    pivot(c, 150, y, sw, a1, 'rubber')
    c.label(215, 520, 'RUBBER TWISTS', 20, WHITE, a1); c.label(215, 550, 'BONDED, SO IT SHEARS', 15, DIM, ease(seg(u, 0.14, 0.28)))
    pivot(c, 545, y, sw, a2, 'poly')
    c.label(610, 520, 'POLYURETHANE ROTATES', 20, C, a2); c.label(610, 550, 'SLEEVE TURNS INSIDE', 15, DIM, ease(seg(u, 0.3, 0.44)))
    g = ease(seg(u, 0.36, 0.5))
    c.line([(545 - 22, y - 26), (500, 232)], fade(DIM, g * 0.8), 2); c.label(500, 214, 'GREASE FILM', 17, WHITE, g)
    step = math.radians(9.5); q = sw / step; f = math.floor(q); fr = q - f                 # stick, then let go, then stick
    dry = step * (f + ease(seg(fr, 0.62, 1.0)))
    if a3 > 0:
        gx, gy = 940 + 196 * math.cos(sw), y + 196 * math.sin(sw)
        dash(c, 940 + 84 * math.cos(sw), y + 84 * math.sin(sw), gx, gy, fade(DIM, a3 * 0.7), 2, 8, 8)   # where the arm wants to be
    pivot(c, 940, y, dry, a3, 'dry')
    c.label(1005, 520, 'DRY: STICKS AND BINDS', 20, COL['bad'], a3); c.label(1005, 550, 'NO GREASE', 15, DIM, ease(seg(u, 0.64, 0.78)))
    c.chip('Silicone grease from Good-Win Racing', G, u=u)


FN = {21: L21, 22: L22, 23: L23, 24: L24, 30: L30}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        os.makedirs(f'{M}/gfx/chk', exist_ok=True)
        for k, f in FN.items(): still(lambda c, u, t, f=f: f(c, u, 2.3), 0.7, f'{M}/gfx/chk/L{k}.png')
    else:
        for k, f in FN.items(): render(k, f)
