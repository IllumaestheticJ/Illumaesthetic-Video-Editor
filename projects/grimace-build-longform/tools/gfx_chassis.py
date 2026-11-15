"""Chassis explainers: sway bars (script lines 49-50) and steering (lines 52-53 tie rods, 55-56 rack bushings).
usage: gfx_chassis.py [still]   -> <media>/gfx/L49.mp4 ...   (still: writes one check frame per line to <media>/gfx/chk/)
Everything shown is a general illustration of how that kind of part works: no values, rates or measured results."""
import sys, math, os
from gfx import *
GS = 'swaybars'; CS = COL[GS]
GT = 'steering'; CT = COL[GT]


# ---------------------------------------------------------------- helpers
def dash(c, pts, col, width=2, on=2, off=2):
    """Dashed polyline through closely sampled points (on/off counted in samples)."""
    i = 0
    while i < len(pts) - 1:
        c.line(pts[i:i + on + 1], col, width); i += on + off


def rbox(c, cx, cy, w, h, ang, fill=None, outline=None, width=3):
    """Rectangle w x h centred on (cx, cy), rotated ang degrees (clockwise on screen)."""
    r = math.radians(ang); cs, sn = math.cos(r), math.sin(r)
    p = [(cx + x * cs - y * sn, cy + x * sn + y * cs) for x, y in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    if fill: c.poly(p, fill=fill)
    if outline: c.line(p + [p[0], p[1]], outline, width)


def swheel(c, x, y, r, ang, a=1.0, col=WHITE):
    """Steering wheel icon; ang in degrees (clockwise on screen)."""
    c.circle(x, y, r, outline=fade(col, a), width=6)
    for k in (-90, 30, 150):
        q = math.radians(ang + k + 180); c.line([(x, y), (x + (r - 3) * math.cos(q), y + (r - 3) * math.sin(q))], fade(col, a), 5)
    c.circle(x, y, r * 0.24, fill=fade(col, a))
    q = math.radians(ang - 90); c.circle(x + r * math.cos(q), y + r * math.sin(q), 5, fill=fade(CT, a))   # top marker


# ---------------------------------------------------------------- sway bars
def L49(c, u, t):   # the bar ties left to right; the body leans, the bar twists and pushes back
    c.header('HOW IT WORKS', 'What a sway bar does', GS, u)
    a = ease(seg(u, 0.02, 0.12)); cx, cy = 400, 420
    roll = 8 * ease(seg(u, 0.30, 0.56)) - 3 * ease(seg(u, 0.72, 0.97)); tw = clamp(roll / 8)
    r = math.radians(roll); cs, sn = math.cos(r), math.sin(r)
    def rot(x, y): return (cx + x * cs - y * sn, cy + x * sn + y * cs)
    c.line([(cx - 290, 562), (cx + 290, 562)], fade(DIM, a), 4)                                           # ground
    c.poly([rot(-190, -150), rot(190, -150), rot(190, -50), rot(-190, -50)], fill=fade(PANEL, a))
    c.line([rot(-190, -150), rot(190, -150), rot(190, -50), rot(-190, -50), rot(-190, -150), rot(190, -150)], fade(WHITE, a), 3)
    c.label(*rot(0, -100), 'CAR, FROM BEHIND', 16, DIM, a)
    for sx in (-1, 1):
        c.rect(cx + sx * 225 - 25, 440, cx + sx * 225 + 25, 560, fill=fade(PANEL, a), outline=fade(DIM, a), width=4, r=10)   # tyre
        c.line([(cx + sx * 140, 500), (cx + sx * 200, 500)], fade(DIM, a), 7)                              # suspension stub
        bx, by = rot(sx * 165, -50); c.spring(bx, by, 497, 5, 14, fade(DIM, a), 4)
    g = ease(seg(u, 0.06, 0.22)); gl = ease(seg(u, 0.16, 0.28))
    for sx in (-1, 1):
        c.line([rot(sx * 70, -50), rot(sx * 70, 10)], fade(DIM, a * g), 4)                                 # hangers on the body
        c.line([rot(sx * 110, 10), (cx + sx * 140, 500)], fade(CS, gl), 8)                                 # bar arm
        c.circle(cx + sx * 140, 500, 8, fill=fade(CS, gl))
    c.line([rot(-110 * g, 10), rot(110 * g, 10)], fade(CS, a), 10)                                         # centre section
    for sx in (-1, 1): c.circle(*rot(sx * 70, 10), 11, fill=fade(PANEL, g), outline=fade(WHITE, g), width=3)
    for k in range(-4, 5):                                                                                 # twist marks
        if abs(k) == 3 or abs(k) / 4.5 > g - 0.05: continue
        s = k / 4.5; px, py = rot(s * 110, 10); q = math.radians(roll + 90 + s * tw * 55)
        c.line([(px - 9 * math.cos(q), py - 9 * math.sin(q)), (px + 9 * math.cos(q), py + 9 * math.sin(q))], fade(WHITE, g), 3)
    c.label(cx, 598, 'SWAY BAR', 20, CS, g)
    p = ease(seg(u, 0.70, 0.84))                                                                           # bar pushes back
    c.arrow(*rot(140, -164), *rot(140, -224), fade(CS, p), 6, 18); c.arrow(*rot(-140, -224), *rot(-140, -164), fade(CS, p), 6, 18)
    for k, (s, col, w) in enumerate((('LEFT TIED TO RIGHT', WHITE, (0.10, 0.24)), ('BODY LEANS', WHITE, (0.32, 0.46)),
                                     ('BAR TWISTS', CS, (0.50, 0.62)), ('BAR FIGHTS THE LEAN', CS, (0.72, 0.84)))):
        c.label(940, 270 + 78 * k, s, 24, col, ease(seg(u, *w)))
    c.chip('Whiteline sway bars', GS, u=u)


def L50(c, u, t):   # front versus rear stiffness changes how the car rotates
    c.header('HOW IT WORKS', 'Front bar, rear bar', GS, u)
    a = ease(seg(u, 0.03, 0.14)); cx = 300
    kf = 0.5 + 0.5 * ease(seg(u, 0.16, 0.38)) - ease(seg(u, 0.50, 0.84))                                   # 1 = thick front, 0 = thick rear
    body = [(cx - 75, 250), (cx - 48, 186), (cx + 48, 186), (cx + 75, 250), (cx + 75, 572), (cx - 75, 572)]
    c.poly(body, fill=fade(PANEL, a)); c.line(body + body[:2], fade(WHITE, a), 3)
    for ya, k, name, d in ((278, kf, 'FRONT', 1), (500, 1 - kf, 'REAR', -1)):
        for sx in (-1, 1): c.rect(cx + sx * 92 - 14, ya - 36, cx + sx * 92 + 14, ya + 36, fill=fade(PANEL, a), outline=fade(DIM, a), width=3, r=6)
        col = fade(mix(mix(BG, CS, 0.55), CS, k), a); w = lerp(4, 17, k); yb = ya + 34 * d
        c.line([(cx - 60, ya), (cx - 60, yb), (cx + 60, yb), (cx + 60, ya)], col, w)
        for sx in (-1, 1): c.circle(cx + sx * 60, ya, w / 2 + 3, fill=col)
        c.label(cx - 170, ya + 17 * d, name, 22, mix(DIM, WHITE, k), a)
    # corner: the car's path runs wide with the thicker front bar, turns in more with the thicker rear bar
    L1, R, L3 = 170, 190, 210; arc = R * math.pi / 2; tot = L1 + arc + L3
    def centre(d):
        if d < L1: return (800, 600 - d), (-1, 0), -90
        if d < L1 + arc:
            q = (d - L1) / R; return (990 - R * math.cos(q), 430 - R * math.sin(q)), (-math.cos(q), -math.sin(q)), -90 + math.degrees(q)
        return (990 + d - L1 - arc, 240), (0, -1), 0
    def bump(d): return math.sin(math.pi * clamp((d - L1 * 0.7) / (tot * 0.97 - L1 * 0.7))) ** 2
    def path(d):
        (x, y), (nx, ny), hd = centre(d); o = lerp(-16, 36, kf) * bump(d)
        return (x + nx * o, y + ny * o), hd + lerp(15, -11, kf) * bump(d)
    for off in (-52, 52):                                                                                  # road edges
        c.line([(centre(d)[0][0] + centre(d)[1][0] * off, centre(d)[0][1] + centre(d)[1][1] * off) for d in [tot * i / 90 for i in range(91)]], fade(DIM, a * 0.7), 3)
    b = ease(seg(u, 0.10, 0.22))
    dash(c, [path(tot * i / 120)[0] for i in range(121)], fade(CS, b * 0.8), 3, 2, 2)
    s = (t * 0.17) % 1.0; ca = b * ease(seg(s, 0, 0.1)) * (1 - ease(seg(s, 0.9, 1.0))); (px, py), hd = path(tot * s)
    rbox(c, px, py, 66, 34, hd, fade(PANEL, ca), fade(WHITE, ca), 3)
    q = math.radians(hd); c.circle(px + 22 * math.cos(q), py + 22 * math.sin(q), 6, fill=fade(CS, ca))     # nose
    c.chip('Whiteline sway bars', GS, u=u)


# ---------------------------------------------------------------- tie rods / bump steer
LA, LT, HH = 340, 170, 110          # control arm length, tie rod length, height of the tie rod above the arm (picture units)


def corner(c, ox, oy, z, D, a, at=1.0, aa=1.0, labels=True):
    """Front view of one front corner. Chassis on the left (dropped by D), wheel on the right, pushed up by z.
    Returns the joints: arm inner A, rack end Rk, ball joint B, tie rod end S, effective tie rod length, tie-rod mismatch dx."""
    A = (ox, oy + D); Rk = (ox + LA - LT, oy - HH + D)
    def ball(zz): by = oy - zz; return (ox + math.sqrt(LA ** 2 - (by - A[1]) ** 2), by)
    B0 = ball(0); lt = math.hypot(B0[0] - Rk[0], B0[1] - HH - Rk[1])                                       # toe is set at ride height
    B = ball(z); S = (B[0], B[1] - HH); dx = Rk[0] + math.sqrt(lt ** 2 - (S[1] - Rk[1]) ** 2) - S[0]
    c.rect(ox - 170, oy - 200 + D, ox, oy + 50 + D, fill=fade(PANEL, a), outline=fade(DIM, a), width=3, r=10)
    c.label(ox - 85, oy - 160 + D, 'CHASSIS', 18, DIM, a)
    ty = B[1] - HH / 2
    c.rect(B[0] + 34, ty - 118, B[0] + 122, ty + 118, fill=fade(PANEL, a), outline=fade(WHITE, a), width=3, r=16)   # tyre
    c.line([(B[0], ty), (B[0] + 34, ty)], fade(DIM, a), 9); c.line([(B[0], B[1]), (B[0], S[1] - 26)], fade(DIM, a), 9)   # hub, upright
    c.line([A, B], fade(mix(DIM, WHITE, aa), a), 8)                                                       # control arm
    c.rect(ox - 6, Rk[1] - 10, Rk[0], Rk[1] + 10, fill=fade(PANEL, a), outline=fade(WHITE, a), width=3, r=5)   # rack
    c.line([Rk, S], fade(mix(DIM, CT, at), a), 6)                                                         # tie rod
    for p, col in ((A, WHITE), (B, WHITE), (Rk, CT), (S, CT)): c.circle(p[0], p[1], 8, fill=fade(BG, a), outline=fade(col, a), width=3)
    if labels:
        c.label(ox + 80, Rk[1] - 32, 'STEERING RACK', 17, DIM, a)
    return A, Rk, B0, B, S, lt, dx


def swing(c, cen, rad, y0, span, col, width=3):
    """Dashed arc about cen through the joint at height y0, drawn span px above and below it."""
    if span < 2: return
    n = max(4, int(span / 4)) * 2
    dash(c, [(cen[0] + math.sqrt(max(0, rad ** 2 - (y - cen[1]) ** 2)), y) for y in [y0 - span + 2 * span * i / n for i in range(n + 1)]], col, width, 2, 2)


def L52(c, u, t):   # tie rod: rack to wheel; it swings in an arc, and so does the control arm
    c.header('HOW IT WORKS', 'Tie rod and control arm', GT, u)
    a = ease(seg(u, 0.02, 0.12)); ox, oy = 400, 480
    at = ease(seg(u, 0.06, 0.2)); aa = ease(seg(u, 0.68, 0.8))
    z = 55 * ease(seg(u, 0.33, 0.5)) * math.sin(t * 1.5)
    A, Rk, B0, B, S, lt, dx = corner(c, ox, oy, z, 0, a, at, aa)
    swing(c, Rk, lt, B0[1] - HH, 92 * ease(seg(u, 0.4, 0.62)), fade(CT, 0.9))
    swing(c, A, LA, B0[1], 92 * ease(seg(u, 0.7, 0.9)), fade(WHITE, 0.9))
    c.label(Rk[0] + 85, 300, 'TIE ROD', 22, CT, at)
    c.label(ox + 150, 546, 'CONTROL ARM', 22, WHITE, aa)
    c.label(B0[0] + 150, 425, 'WHEEL', 22, WHITE, a, 'lm')
    m = ease(seg(u, 0.36, 0.48)); x = B0[0] + 170
    c.arrow(x, 480, x, 520, fade(DIM, m), 4, 12); c.arrow(x, 370, x, 330, fade(DIM, m), 4, 12)
    c.chip('SPL tie rods', GT, u=u)


def L53(c, u, t):   # arcs don't match -> toe changes over bumps (bump steer); lowering makes it worse
    c.header('HOW IT WORKS', 'Bump steer', GT, u)
    a = ease(seg(u, 0.0, 0.08)); ox, oy = 230, 480
    low = ease(seg(u, 0.62, 0.82)); D = 48 * low; z = 55 * math.sin(t * 1.5)
    A, Rk, B0, B, S, lt, dx = corner(c, ox, oy, z, D, a, labels=False)
    g = ease(seg(u, 0.05, 0.2)); wc = mix(CT, COL['bad'], low)
    swing(c, (A[0], A[1] - HH), LA, B0[1] - HH, 96 * g, fade(WHITE, 0.85))                                 # where the wheel carries the joint
    swing(c, Rk, lt, B0[1] - HH, 96 * g, fade(CT, 0.95))                                                   # where the tie rod wants it
    c.line([(S[0], S[1]), (S[0] + dx, S[1])], fade(wc, g), 6); c.circle(S[0] + dx, S[1], 5, fill=fade(wc, g))
    lo = ease(seg(u, 0.64, 0.76))
    c.label(ox - 85, 190, 'LOWERED', 20, WHITE, lo); c.arrow(ox - 85, 210, ox - 85, 252, fade(WHITE, lo), 5, 14)
    # top view of the same wheel: toe follows the mismatch, steering wheel never moves
    b = ease(seg(u, 0.18, 0.3)); tx, ty = 930, 350; toe = dx * 1.05
    dash(c, [(tx, 205 + 6 * i) for i in range(49)], fade(DIM, b), 2, 2, 2)
    rbox(c, tx, ty, 70, 200, toe, fade(PANEL, b), fade(WHITE, b), 3)
    q = math.radians(toe - 90)
    c.line([(tx - 140 * math.cos(q), ty - 140 * math.sin(q)), (tx + 140 * math.cos(q), ty + 140 * math.sin(q))], fade(wc, b), 4)
    c.label(tx, 178, 'TOP VIEW', 16, DIM, b)
    swheel(c, 1130, 330, 30, 0, b, DIM); c.label(1130, 388, 'HELD STILL', 16, DIM, b)
    c.label(tx + 60, 548, 'BUMP STEER', 30, wc, ease(seg(u, 0.44, 0.54)))
    c.chip('SPL tie rods', GT, u=u)


# ---------------------------------------------------------------- rack bushings
def rack(c, u, a, X, slack, mcol, am=1.0):
    """Top view. X = steering input (rack travel asked for); slack = how far the rack housing shifts on its mounts first.
    Returns housing shift, the pulse path from a tyre to the steering wheel (left, right)."""
    sg = 1 if X >= 0 else -1; hs = -sg * slack * (1 - math.exp(-abs(X) / slack)); b = X + hs    # housing gives first, then the bar moves
    ARM = 90; ph = math.asin(clamp(b / ARM, -1, 1)); y = 400
    c.rect(430, 456, 850, 492, fill=fade(PANEL, a), outline=fade(DIM, a), width=3, r=8); c.label(640, 474, 'CHASSIS', 16, DIM, a)
    dash(c, [(640, 376 + 4 * i) for i in range(19)], fade(DIM, a), 2, 2, 2)                                # fixed centre mark
    paths = []
    for sx in (-1, 1):
        px, py = 640 + sx * 390, 310; ex, ey = px + ARM * math.sin(ph), py + ARM * math.cos(ph)
        rbox(c, px, py, 58, 156, -math.degrees(ph), fade(PANEL, a), fade(WHITE, a), 3)
        c.line([(px, py), (ex, ey)], fade(DIM, a), 7)                                                     # steering arm
        c.line([(640 + sx * 240 + b, y), (ex, ey)], fade(CT, a), 5)                                        # tie rod
        c.circle(ex, ey, 7, fill=fade(BG, a), outline=fade(CT, a), width=3); c.circle(px, py, 6, fill=fade(DIM, a))
        paths.append([(ex, ey), (640 + sx * 240 + b, y), (640 + hs, y), (640, 252)])
    c.line([(400 + b, y), (880 + b, y)], fade(WHITE, a), 8)                                                # rack bar
    for sx in (-1, 1): c.circle(640 + sx * 240 + b, y, 7, fill=fade(BG, a), outline=fade(CT, a), width=3)
    for mx in (545, 735):                                                                                  # mounts: top follows the housing
        c.poly([(mx - 17 + hs, 414), (mx + 17 + hs, 414), (mx + 17, 456), (mx - 17, 456)], fill=fade(mix(PANEL, mcol, 0.35 + 0.65 * am), a))
        c.line([(mx - 17 + hs, 414), (mx + 17 + hs, 414), (mx + 17, 456), (mx - 17, 456), (mx - 17 + hs, 414)], fade(mcol, a), 2)
    c.rect(500 + hs, 386, 780 + hs, 414, fill=fade(PANEL, a), outline=fade(WHITE, a), width=3, r=8)        # rack housing
    c.poly([(640 + hs - 9, 386), (640 + hs + 9, 386), (640 + hs, 372)], fill=fade(WHITE, a))               # mark on the housing
    c.line([(640, 252), (640 + hs, 386)], fade(DIM, a), 6)                                                 # column
    swheel(c, 640, 200, 46, -X * 2.0, a)
    return hs, paths


def L55(c, u, t):   # the rack sits on rubber; it shifts sideways before the tyres do anything
    c.header('HOW IT WORKS', 'Rack bushings', GT, u)
    a = ease(seg(u, 0.02, 0.13)); am = ease(seg(u, 0.14, 0.28))
    rack(c, u, a, 62 * ease(seg(u, 0.42, 0.9)), 24, CT, am)
    c.label(505, 362, 'STEERING RACK', 16, DIM, a)
    c.label(640, 530, 'RUBBER MOUNTS', 22, CT, am)
    c.label(640, 580, 'RACK MOVES FIRST', 28, WHITE, ease(seg(u, 0.5, 0.62)))
    c.chip('SuperPro steering rack bushings', GT, u=u)


def L56(c, u, t):   # stiffer mounts: the wheels follow almost at once; a manual rack passes everything back
    c.header('HOW IT WORKS', 'Stiffer rack bushings', GT, u)
    a = ease(seg(u, 0.0, 0.1)); G = COL['good']
    X = 58 * math.sin(2 * math.pi * ease(seg(u, 0.12, 0.96)) ** 0.9)
    hs, paths = rack(c, u, a, X, 3, G)
    f = ease(seg(u, 0.52, 0.64))
    for pts in paths:                                                                                      # feel: tyres -> rods -> rack -> column -> hands
        ln = [math.dist(pts[i], pts[i + 1]) for i in range(3)]; tot = sum(ln)
        for k in range(3):
            s = (t * 0.45 + k / 3) % 1.0; d = s * tot; i = 0
            while i < 2 and d > ln[i]: d -= ln[i]; i += 1
            q = d / ln[i]; x, y = lerp(pts[i][0], pts[i + 1][0], q), lerp(pts[i][1], pts[i + 1][1], q)
            c.circle(x, y, 6, fill=fade(CT, f * ease(seg(s, 0, 0.12)) * (1 - ease(seg(s, 0.88, 1)))))
    c.label(505, 362, 'STEERING RACK', 16, DIM, a)
    c.label(640, 530, 'STIFFER MOUNTS', 22, G, ease(seg(u, 0.08, 0.2)))
    c.label(640, 580, 'WHEELS FOLLOW AT ONCE', 28, WHITE, ease(seg(u, 0.24, 0.38)))
    c.label(730, 186, 'MANUAL RACK', 16, DIM, f, 'lm'); c.label(730, 214, 'YOU FEEL IT ALL', 24, WHITE, f, 'lm')
    c.chip('SuperPro steering rack bushings', GT, u=u)


FN = {49: L49, 50: L50, 52: L52, 53: L53, 55: L55, 56: L56}
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        os.makedirs(f'{M}/gfx/chk', exist_ok=True)
        for k, f in FN.items(): still(lambda c, u, t, f=f: f(c, u, 2.3), 0.7, f'{M}/gfx/chk/L{k}.png')
    else:
        for k, f in FN.items(): render(k, f)
