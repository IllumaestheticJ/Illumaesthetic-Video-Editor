"""v3 shot specs (scene-director plan: projects/mazda-miata-nd/direction.md + director.md) -> JSON for tools/shot.py.

    python projects/mazda-miata-nd/tools/shots_v3.py preview|final [shot ...]

Times in beats from the shot start (B = 0.51721 s). Frame: prepped metres, front -Y, car's right -X, ground z 0.
Every spec renders with Cycles persistent data OFF. N renders per slot follow the minterpolate rule (director.md).
"""
import json
import math
import os
import sys

W = "/home/user/media/work/miata"
P = f"{W}/prep"
OUT = f"{W}/renders"
SPECS = f"{W}/specs"
B = 0.51721
HOOD = [-0.1237, -0.458, 0.8887]
TRUNK = [-0.1237, 1.3358, 0.9865]
HOOD_OPEN, TRUNK_OPEN = -43.67, 85.69
Z = [0, 0, 0]


def orbit(t, r, a, h, c, focal=30, tz=None):
    a = math.radians(a)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": "lin"}


def arc(secs, r, a, h, c0, c1=None, focal=30, n=8, tz=None):
    """r/a/h are (start, end); smoothstep over the whole move, keyed every 1/n (no chords through the car)."""
    c1 = c1 or c0
    ks = []
    for k in range(n + 1):
        u = k / n
        e = u * u * (3 - 2 * u)
        L = lambda p: p[0] + (p[1] - p[0]) * e
        ks.append(orbit(secs * u, L(r), L(a), L(h), [x + (y - x) * e for x, y in zip(c0, c1)], focal, tz))
    return ks


def cam(b, loc, tgt, f, ease="inout"):
    return {"t": b * B, "loc": loc, "target": tgt, "focal": f, "ease": ease}


def k(b, loc=Z, rot=Z, ease="inout"):
    return {"t": b * B, "loc": list(loc), "rot": list(rot), "ease": ease}


def part(name, keys, pivot=None):
    d = {"blend": f"{P}/{name}.blend", "keys": keys}
    if pivot:
        d["pivot"] = pivot
    return d


def static(name, loc=Z, rot=Z, pivot=None):
    return part(name, [k(0, loc, rot), k(1, loc, rot)], pivot)


# Bumpers: show the inner face on the camera's line of sight below the nose/tail (in clear black, fully in frame),
# then sink fully out of frame while the camera pushes in on the structure behind (preview: v1 pose clipped at the edge).
FB_SHOW = ((-0.40, -0.58, -0.70), (150, 0, 0))
RB_SHOW = ((-0.60, 0.95, -0.55), (-150, 0, 0))
FB_END = ((-0.40, -0.58, -1.9), (150, 0, 0))
RB_END = ((-0.60, 0.95, -1.6), (-150, 0, 0))

SHOTS = {
    # 1. opener: the whole car, front-right 3/4, slow push + 12 deg orbit toward the nose, moving from frame 1
    "v3_a_open": {"N": 32, "base": ["car4np"], "parts": [],
                  "cam": arc(31 / 15, (6.4, 5.95), (-50, -38), (1.45, 1.3), (0, -0.2, 0.58), (0, -0.25, 0.58))},
    # 3. front bumper off -> inner face to the lens -> push in on the crash beam / structure behind it
    "v3_f_bumper": {"N": 63, "base": ["comp_front"],
                    "parts": [part("x_fbumper", [k(0), k(0.5), k(2, (0, -0.45, 0), ease="out"),
                                                 k(4, *FB_SHOW), k(4.75, *FB_SHOW), k(7, *FB_END), k(8, *FB_END)]),
                              static("x_hood", pivot=HOOD)],
                    "cam": [cam(0, [-1.75, -4.35, 1.35], [0, -1.60, 0.45], 30),
                            cam(4, [-1.68, -4.22, 1.30], [0, -1.62, 0.42], 30),
                            cam(4.5, [-1.68, -4.22, 1.30], [0, -1.62, 0.42], 30),
                            cam(7.5, [-0.85, -3.25, 0.85], [0, -1.75, 0.45], 28),
                            cam(8, [-0.85, -3.25, 0.85], [0, -1.75, 0.45], 29, "lin")]},
    # 4. hood swings to its captured open pose (lands on the lift, n16) -> engine bay; camera high (no hood underside)
    "v3_f_bay": {"N": 47, "base": ["comp_front"],
                 "parts": [part("x_hood", [k(0), k(2), k(4, rot=(HOOD_OPEN, 0, 0)), k(6, rot=(HOOD_OPEN, 0, 0))], HOOD),
                           ],  # front bumper is off and out of shot (not in the scene)
                 "cam": [cam(0, [-1.10, -2.50, 3.30], [0, -1.00, 0.60], 30),
                         cam(6, [-0.80, -2.05, 2.75], [0, -0.95, 0.62], 30)]},
    # 6. side: right mirror off (turned to show its mount plate), then the sill skirt slides out (translate only)
    "v3_s_side": {"N": 48, "base": ["comp_explode"],
                  "parts": [part("x_mirror_r", [k(0), k(0.5), k(2, (-0.38, -0.05, 0.18), ease="out"),
                                                k(3.5, (-0.38, -0.05, 0.18), (0, 0, -135)), k(6, (-0.38, -0.05, 0.18), (0, 0, -135))]),
                            part("x_skirt", [k(0), k(3.5), k(5, (-0.32, 0, -0.06)), k(6, (-0.32, 0, -0.06))]),
                            static("x_hood", rot=(HOOD_OPEN, 0, 0), pivot=HOOD),
                            static("x_rbumper"), static("x_trunk", pivot=TRUNK), static("x_mirror_l")],
                  "cam": [cam(0, [-2.15, -1.05, 1.30], [-0.85, -0.08, 0.85], 50),
                          cam(3.5, [-2.35, -1.00, 1.28], [-1.05, -0.10, 0.95], 50),
                          cam(6, [-3.35, -1.25, 0.95], [-0.85, -0.05, 0.45], 30)]},
    # 7. rear bumper off -> inner face (ribs/brackets) -> exhaust + rear structure
    "v3_r_bumper": {"N": 47, "base": ["comp_rear"],
                    "parts": [part("x_rbumper", [k(0), k(0.5), k(2, (0, 0.45, 0), ease="out"),
                                                 k(3.5, *RB_SHOW), k(4, *RB_SHOW), k(5.5, *RB_END), k(6, *RB_END)]),
                              static("x_trunk", pivot=TRUNK)],
                    "cam": [cam(0, [-1.65, 4.60, 1.45], [0.25, 1.75, 0.50], 30),
                            cam(3.5, [-1.58, 4.48, 1.40], [0.2, 1.77, 0.47], 30),
                            cam(5.5, [-0.75, 3.55, 0.85], [0, 1.95, 0.42], 28),
                            cam(6, [-0.75, 3.55, 0.85], [0, 1.95, 0.42], 29, "lin")]},
    # 8. trunk lid swings to its captured pose -> trunk interior; camera stays in front of the lid plane (y < 1.33)
    "v3_r_trunk": {"N": 32, "base": ["comp_rear"],
                   "parts": [part("x_trunk", [k(0), k(0.5), k(2.5, rot=(TRUNK_OPEN, 0, 0)), k(4, rot=(TRUNK_OPEN, 0, 0))], TRUNK),
                             ],  # rear bumper is off and out of shot
                   "cam": [cam(0, [-2.25, 1.00, 2.95], [-0.35, 1.40, 0.70], 30),
                           cam(4, [-1.75, 1.25, 2.60], [-0.35, 1.45, 0.66], 30)]},
}

# Finale: one part clock T (beats from n38); each explode shot renders its own window of it.
FIN = {  # name: (pivot, start offset (loc, rot), rise (T0, T1, loc, rot), return start T)
    "x_hood": (HOOD, (Z, Z), (0, 2, (0, -0.15, 0.85), (8, 0, 0)), 7.25),
    "x_fbumper": (None, ((0, -0.55, 0), Z), (0.5, 2.5, (0, -0.45, 1.35), (90, 0, 0)), 7),
    "x_mirror_r": (None, ((-0.38, -0.05, 0.18), Z), (1, 3, (-0.45, 0, 0.75), Z), 7.5),
    "x_mirror_l": (None, ((0.38, -0.05, 0.18), Z), (1, 3, (0.45, 0, 0.75), Z), 7.5),
    "x_skirt": (None, ((-0.32, 0, -0.06), Z), (1, 3, (-0.55, 0, 0.40), Z), 7.5),
    "x_trunk": (TRUNK, (Z, Z), (1.5, 3.5, (0, 0.10, 0.80), (-8, 0, 0)), 7.25),
    "x_rbumper": (None, ((0, 0.55, 0), Z), (2, 4, (0, 0.45, 1.30), (-90, 0, 0)), 7),
}
LOCK = 10


def finale_parts(T0):
    out = []
    for n, (pv, (l0, r0), (a, b, l1, r1), back) in FIN.items():
        drift = [v * 1.06 for v in l1]
        ks = [(0, l0, r0), (a, l0, r0), (b, l1, r1), (4, l1, r1), (7, drift, r1), (back, drift, r1), (LOCK, Z, Z), (14, Z, Z)]
        eases = ["inout", "inout", "inout", "inout", "lin", "lin", "in", "lin"]
        keys, last = [], None
        for (t, l, r), e in sorted(zip(ks, eases), key=lambda x: x[0][0]):
            if last is not None and t <= last:
                continue
            keys.append({"t": (t - T0) * B, "loc": list(l), "rot": list(r), "ease": e})
            last = t
        # shot.py samples from the first key; shift so keys before the window still interpolate correctly
        out.append(part(n, keys, pv))
    return out


SHOTS["v3_x_front"] = {"N": 32, "base": ["comp_explode"], "parts": finale_parts(0),
                       "cam": arc(31 / 15, (6.4, 6.0), (38, 52), (4.2, 3.9), (0, -0.6, 1.1), tz=1.1)}
SHOTS["v3_x_rear"] = {"N": 32, "base": ["comp_explode"], "parts": finale_parts(4),
                      "cam": arc(31 / 15, (6.4, 6.1), (142, 128), (4.2, 3.9), (0, 0.8, 1.1), tz=1.1)}
HOME_CAM = arc(22 / 15, (8.6, 7.4), (96, 104), (2.8, 2.3), (0, 0, 0.75), (0, 0, 0.6), n=4)
SHOTS["v3_x_home"] = {"N": 23, "base": ["comp_explode"], "parts": finale_parts(8), "cam": HOME_CAM,
                      "frames": list(range(1, 18))}       # parts land T10 = render 17 (t 1.067 s >= 1.034)
SHOTS["v3_x_home_clean"] = {"N": 23, "base": ["car4np"], "parts": [], "cam": HOME_CAM,
                            "frames": list(range(18, 24)), "out": "v3_x_home"}  # clean car swap after the lock


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    sp = {"base": [f"{P}/{b}.blend" for b in s["base"]], "parts": s["parts"],
          "camera": {"sensor": 20.25, "keys": s["cam"]}, "seconds": (s["N"] - 1) / 15, "fps": 15,
          "res": "1080x1920", "res_pct": 75 if final else 30, "samples": 12 if final else 6, "persistent": False,
          "out": f"{OUT}/{'final' if final else 'preview'}/{s.get('out', name)}"}
    if not final:
        n = s["N"]
        fr = s.get("frames")
        sp["frames"] = [fr[0], fr[len(fr) // 2], fr[-1]] if fr else [1, (n + 1) // 2, n]
    elif s.get("frames"):
        sp["frames"] = s["frames"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
