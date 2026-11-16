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


def joint(c, x, y, R, ring, a=1.0, ex=0.0, ey=0.0, ang=None, twist=0.0, arm=0.0, ear=0.0, wall=False, cross=0.0, kind='rubber'):
    """One arm pivot seen along its bolt, the same drawing at any size (small on the corner view, big in the cutaway):
    chassis bracket ear, bolt (hex) with the inner sleeve clamped on it at (x, y), the elastic layer, and the arm's eye
    (outer shell) centred at (x + ex, y + ey) with the arm tube leaving at ang. The bolt and sleeve never move; the eye does.
    twist = how far the arm has swung (bonded rubber shears: its inner edge stays with the sleeve)."""
    r = 0.32 * R; cx, cy = x + ex, y + ey
    if ear > 0:                                                                             # bracket ear behind the eye
        c.poly([(x - ear, y - 0.92 * R), (x, y - 0.5 * R), (x, y + 0.5 * R), (x - ear, y + 0.92 * R)], fill=fade(PANEL, a))
        c.line([(x - ear, y - 0.92 * R), (x, y - 0.5 * R)], fade(DIM, a), max(1.5, R * 0.03))
        c.line([(x - ear, y + 0.92 * R), (x, y + 0.5 * R)], fade(DIM, a), max(1.5, R * 0.03))
    if wall: c.rect(x - ear - 0.24 * R, y - 1.3 * R, x - ear, y + 1.3 * R, fill=fade(PANEL, a), outline=fade(DIM, a), width=2.5, r=4)
    if arm > 0:                                                                             # arm tube, cut off square
        c.line([(cx, cy), (cx + arm * math.cos(ang), cy + arm * math.sin(ang))], fade(ARM, a), 0.5 * R)
    c.circle(cx, cy, R, fill=fade(ring, a), outline=fade(ARM, a), width=max(2.5, R * 0.13))
    if R >= 30:                                                                             # ribs make the squeeze and twist readable
        for k in range(12):
            p = k * math.pi / 6 + 0.26; q = p + twist; pi_ = p if kind == 'rubber' else q
            c.line([(x + (r + 2) * math.cos(pi_), y + (r + 2) * math.sin(pi_)), (cx + 0.85 * R * math.cos(q), cy + 0.85 * R * math.sin(q))],
                   fade(mix(ring, BG, 0.6), a), max(1.5, R * 0.032))
    if cross > 0:                                                                           # fixed centre cross + marks on the eye
        dash(c, x, y - 1.36 * R, x, y + 1.36 * R, fade(WHITE, cross * a), 2, 7, 6)
        dash(c, x - 0.6 * R, y, x + 0.6 * R, y, fade(WHITE, cross * a), 2, 7, 6)
        for sg in (-1, 1): c.line([(cx, cy + sg * 0.84 * R), (cx, cy + sg * 1.2 * R)], fade(C, cross * a), max(3, R * 0.05))
    c.circle(x, y, r, fill=fade(BG, a), outline=fade(WHITE, a), width=max(2, R * 0.075))
    hx = 0.19 * R
    c.poly([(x + hx * math.cos(i * math.pi / 3), y + hx * math.sin(i * math.pi / 3)) for i in range(6)], fill=fade(DIM, a))


# Front view of one double-wishbone corner, in local units (x outboard, y down, origin on the chassis side).
PL, PU = (0.0, 85.0), (40.0, -75.0)            # lower / upper arm pivots on the chassis (bolts and sleeves: these never move)
LBJ0, UBJ0 = (290.0, 100.0), (268.0, -80.0)    # lower / upper ball joints on the upright: two different points
TX0, TX1, TY0, TY1 = 318.0, 408.0, -160.0, 170.0   # tyre section; the ground is at TY1 at rest
WX, HUBY, BR = 363.0, 5.0, 40.0                # wheel centre plane, hub height, bushing radius
L_LO = math.hypot(LBJ0[0] - PL[0], LBJ0[1] - PL[1]); L_UP = math.hypot(UBJ0[0] - PU[0], UBJ0[1] - PU[1])
L_KN = math.hypot(UBJ0[0] - LBJ0[0], UBJ0[1] - LBJ0[1])
PHI0 = math.atan2(LBJ0[1] - PL[1], LBJ0[0] - PL[0]); KN0 = math.atan2(UBJ0[1] - LBJ0[1], UBJ0[0] - LBJ0[0])


def solve(d, z=0.0):
    """Linkage under bushing deflection d and wheel travel z (local units, z up). Cornering load at the contact patch pushes
    the lower arm inboard (compression) and pulls the upper arm outboard (tension), so the lower eye moves in by d and the upper
    one out by 0.55 d. Arms and upright stay rigid; the lower arm swings until the tyre sits on the ground (raised by z).
    Returns (lower eye centre, upper eye centre, lower ball joint, upper ball joint, upright rotation, lower arm angle)."""
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
        return lb[1] + max((x - LBJ0[0]) * math.sin(th) for x in (TX0, TX1)) + y * math.cos(th) - (TY1 - z)
    phi = PHI0
    for _ in range(8):
        e = patch_y(phi); g = (patch_y(phi + 1e-4) - e) / 1e-4
        if abs(g) < 1e-9: break
        phi -= e / g
    lb, ub, th = pose(phi)
    return sl, su, lb, ub, th, phi


def assembly(c, ox, oy, s, load, a=1.0, ring=RUB, k=1.0, wheelcol=C, setline=0.0, chassis_label=True, z=0.0):
    """Front view of one corner: chassis block, upper and lower A-arm each on its own bushing, upright (knuckle) between the two
    ball joints, hub and tyre on the upright. load 0..1 pushes at the contact patch; k = how much the bushings give; z = wheel
    travel. Returns a dict of screen points for labels plus the solved linkage ('st')."""
    st = solve(13.0 * load * k, z); sl, su, lb, ub, th, phi = st; cs, sn = math.cos(th), math.sin(th)
    def F(x, y): return (ox + x * s, oy + y * s)                                            # fixed to the chassis
    def T(x, y):                                                                            # rigid with the upright
        x, y = x - LBJ0[0], y - LBJ0[1]; return F(lb[0] + x * cs - y * sn, lb[1] + x * sn + y * cs)
    c.rect(*F(-170, -150), *F(-55, 135), fill=fade(PANEL, a), outline=fade(DIM, a), width=2.5, r=10 * s)
    if chassis_label: c.label(*F(-112, 0), 'CHASSIS', 16, DIM, a)
    c.line([F(TX0 - 40, TY1 - z + 2), F(TX1 + 40, TY1 - z + 2)], fade(DIM, a * 0.8), 2)     # ground
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
    for sh, fx in ((sl, PL), (su, PU)):                                                     # the pivots: small versions of the cutaway
        px, py = F(*fx); joint(c, px, py, BR * s, ring, a, (sh[0] - fx[0]) * s, (sh[1] - fx[1]) * s, ear=(fx[0] + 56) * s)
    return dict(lo=F(*sl), up=F(*su), lbj=F(*lb), ubj=F(*ub), hub=hub, wheel=T(WX, HUBY), patch=T(TX1, TY1 - 22),
                out=T(TX1, HUBY), st=st, F=F)


def cutaway(c, x, y, R, st, a=1.0, ring=RUB, cross=0.0, box=None, link=None, kind='rubber'):
    """Zoomed cutaway of the lower arm's chassis pivot, driven by the same solved linkage as the corner view (a true zoom:
    same offset in proportion, same arm angle). box = panel (x0, y0, x1, y1); link = F() of the corner view for the leader."""
    sl, phi = st[0], st[5]
    if box:
        c.rect(*box, fill=fade(mix(BG, PANEL, 0.35), a), outline=fade(GRID, a), width=2, r=14)
        if link:                                                                            # leader: pivot on the car -> its zoom
            s = (link(1, 0)[0] - link(0, 0)[0]); px, py = link(*PL); ey = link(0, 168)[1]
            c.circle(px, py, (BR + 9) * s, outline=fade(DIM, a), width=2)
            lx = px - 22 * s
            c.line([(lx, py + (BR + 3) * s), (lx, ey), (box[2], ey)], fade(DIM, a), 2); c.circle(box[2], ey, 4, fill=fade(DIM, a))
    arm = 2.25 * R if not box else min(2.6 * R, (box[2] - 3 - x - (sl[0] - PL[0]) / BR * R) / math.cos(phi))
    joint(c, x, y, R, ring, a, (sl[0] - PL[0]) / BR * R, (sl[1] - PL[1]) / BR * R, phi, phi - PHI0, arm, 1.7 * R, True, cross, kind)


def L21(c, u, t):   # every arm joins the chassis through one of these
    c.header('HOW IT WORKS', 'Where the arms meet the car', G, u)
    a = ease(seg(u, 0.04, 0.2)); ox, oy, s = 770, 368, 0.8
    z = 25 * ease(seg(u, 0.16, 0.4)) * math.sin(t * 1.7)                                    # wheel rides up and down: the arms hinge
    ia = ease(seg(u, 0.14, 0.3)); box = (64, 196, 520, 566); ix, iy, R = 262, 392, 90
    p = assembly(c, ox, oy, s, 0.0, a, wheelcol=None, z=z); F = p['F']
    cutaway(c, ix, iy, R, p['st'], ia, box=box, link=F)
    c.label(box[0] + 18, box[1] + 22, 'INSIDE A BUSHING', 15, DIM, ia, 'lm')
    for k, (name, lx, ly, px, py) in enumerate((('BOLT', ix - 78, iy - R - 38, ix - 4, iy - 5),
                                                ('SLEEVE', ix + 62, iy - R - 38, ix + 0.3 * R * 0.6, iy - 0.3 * R * 0.8),
                                                ('RUBBER', ix - 30, iy + R + 40, ix - 0.12 * R, iy + 0.62 * R),
                                                ('ARM', ix + 1.8 * R, iy + R + 40, ix + 1.7 * R, iy + 0.5 * R))):
        b = ease(seg(u, 0.24 + 0.06 * k, 0.36 + 0.06 * k)); dy = 13 if ly < iy else -13
        if b > 0 and name != 'ARM':
            c.line([(lx, ly + dy), (lerp(lx, px, b), lerp(ly + dy, py, b))], fade(DIM, a), 2); c.circle(lerp(lx, px, b), lerp(ly + dy, py, b), 4 * b, fill=WHITE)
        c.label(lx, ly, name, 18, WHITE, b)
    la = ease(seg(u, 0.1, 0.24))
    c.label(*F(192, -134), 'UPPER ARM', 17, WHITE, la); c.label(*F(226, 152), 'LOWER ARM', 17, WHITE, la)
    c.label(*F(205, 12), 'UPRIGHT', 17, WHITE, la, 'rm'); c.line([F(215, 12), (p['hub'][0] - 12, p['hub'][1])], fade(DIM, la), 2)
    c.label(F(TX1, 0)[0] + 16, oy, 'WHEEL', 17, DIM, la, 'lm')
    for k, ((bx, by), (lx, ly)) in enumerate(((F(*PU), F(PU[0], PU[1] - 72)), (F(*PL), F(62, 150)))):
        h = ease(seg(u, 0.46 + 0.2 * k, 0.62 + 0.2 * k))
        if h > 0:
            q = 0.5 + 0.5 * math.sin(t * 2.0 - k * 1.2)                                     # slow breathing halo
            c.circle(bx, by, (BR + 7) * s + 6 * q, outline=fade(C, h * (0.9 - 0.4 * q)), width=3)
            c.label(lx, ly, 'BUSHING', 19, C, h)
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
    a = ease(seg(u, 0.04, 0.18)); ox, oy, s = 720, 372, 0.8
    load = ease(seg(u, 0.26, 0.56)) * (0.86 + 0.14 * math.sin(t * 1.5))
    sl = ease(seg(u, 0.1, 0.24)); box = (64, 196, 500, 562); ix, iy, R = 258, 388, 90
    p = assembly(c, ox, oy, s, load, a, setline=sl); F = p['F']
    cutaway(c, ix, iy, R, p['st'], a, cross=sl, box=box, link=F)
    c.label(box[0] + 18, box[1] + 22, 'INSIDE THE BUSHING', 15, DIM, a, 'lm')
    qa = ease(seg(u, 0.4, 0.56)); ex = (p['st'][0][0] - PL[0]) / BR * R
    for name, lx, px in (('THICKER', ix - 96, ix + ex - 0.56 * R), ('THINNER', ix + 96, ix + 0.32 * R + 0.5 * (ex + 0.55 * R))):
        c.line([(lx, iy - R - 22), (px, iy - 0.14 * R)], fade(DIM, qa), 2); c.circle(px, iy - 0.14 * R, 4, fill=fade(WHITE, qa))
        c.label(lx, iy - R - 36, name, 16, WHITE, qa)
    c.label(F(WX, 0)[0], F(0, TY0 - 46)[1], 'WHERE YOU SET IT', 17, WHITE, sl)
    la = ease(seg(u, 0.2, 0.34)); ax, ay = p['patch'][0] + 10, F(0, TY1 - 22)[1]            # the arrow leans on the contact patch
    c.arrow(ax + 150, ay, ax, ay, fade(C, la), 7, 20)
    c.label(ax + 18, ay - 28, 'CORNERING LOAD', 17, WHITE, la, 'lm')
    c.label((box[0] + box[2]) / 2, 594, 'RUBBER SQUISHES', 20, C, ease(seg(u, 0.42, 0.6)))
    c.label(F(150, 0)[0], 594, 'ARMS SHIFT, WHEEL TILTS', 20, C, ease(seg(u, 0.6, 0.78)))
    c.chip(CHIP, G, u=u)


def L24(c, u, t):   # same load: rubber gives a lot, polyurethane gives a little
    c.header('HOW IT WORKS', 'Rubber vs polyurethane', G, u)
    load = ease(seg(u, 0.3, 0.58)) * (0.86 + 0.14 * math.sin(t * 1.5)); s, oy, R = 0.47, 340, 62
    for k, (hx, name, sub, col, give) in enumerate(((60, 'RUBBER', 'WHEEL MOVES AROUND', COL['bad'], 1.0),
                                                    (648, 'POLYURETHANE', 'WHEEL STAYS CLOSE', COL['good'], 0.22))):
        a = ease(seg(u, 0.05 + 0.1 * k, 0.2 + 0.1 * k)); sl = ease(seg(u, 0.16 + 0.06 * k, 0.3 + 0.06 * k)); ring = mix(PANEL, col, 0.62)
        ox = hx + 282; box = (hx, oy - 104, hx + 190, oy + 104)
        p = assembly(c, ox, oy, s, load, a, ring, give, col, sl, chassis_label=False)
        cutaway(c, hx + 106, oy, R * 0.92, p['st'], a, ring, sl, box, p['F'])
        la = ease(seg(u, 0.22, 0.36)); ax, ay = p['patch'][0] + 8, oy + (TY1 - 22) * s
        c.arrow(ax + 70, ay, ax, ay, fade(WHITE, la), 6, 17)
        c.label(ax, ay - 22, 'SAME LOAD', 15, DIM, la, 'lm')
        c.label(ox + WX * s, oy + (TY0 - 48) * s, 'AS SET', 15, DIM, sl)
        c.label(hx + 270, 502, name, 26, col, a)
        c.label(hx + 95, 538, 'SLEEVE OFF CENTRE' if k == 0 else 'SLEEVE STAYS PUT', 16, WHITE, ease(seg(u, 0.5 + 0.1 * k, 0.66 + 0.1 * k)))
        c.label(ox + 150 * s, 538, sub, 16, WHITE, ease(seg(u, 0.56 + 0.1 * k, 0.72 + 0.1 * k)))
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
