"""A90 v3 shot generator: direction_v3.md -> shots_v3/*.json (never hand-edit the JSONs).

Reel: 20 bars of the supplied track from 13.930 s, 89.58 BPM, bar 2.679 s, hard cuts on bar lines.
hb = half-beat (0.3349 s). Scene frame (m): nose +X, car-right -Y, up +Z (= raw mm / 1000 + prep root).
Shots at 30 fps render every reel frame; shots at 15 fps render every second frame (+3 tail) and are interpolated.

    python projects/a90-supra/tools/plan_v3.py            -> projects/a90-supra/shots_v3/*.json + timeline_v3.json
"""
import json
import math
import os

import numpy as np

import kin_v3 as kin

D = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
B3 = "/home/user/media/work/a90/blend3/"
B2 = "/home/user/media/work/a90/blend/"
BB = json.load(open(D + "/match/bbox_v3.json"))
BEAT = 2.6773 / 4            # measured on the kick attacks of the excerpt (89.64 BPM)
BAR, HB = 4 * BEAT, BEAT / 2
TRACK0 = 0.527                 # the song's beginning (standing reviewer rule): kick attack of riff bar 1
F = [int(round(k * BAR * 30)) for k in range(22)]   # 21 bars   # reel frame of each bar line
LIGHT = [[-2.19, -1.015, 0.0], [2.19, 1.015, 1.174]]  # light rig pinned to the car bbox in every shot
LOOK, EXPOSURE = "AgX - Medium High Contrast", -0.7   # v3 grade: flat white washed the scan detail out at exposure 0
SHOTS = {}


class Shot:
    def __init__(self, name, bar, fps, bars=1, **kw):
        self.name, self.bar, self.fps = name, bar, fps
        self.n = F[bar - 1 + bars] - F[bar - 1]          # reel frames
        self.m = self.n if fps == 30 else self.n // 2 + 3  # rendered frames
        self.spec = dict(_bar=bar, _reel_frames=[F[bar - 1], F[bar - 1 + bars]], fps=fps, seconds=self.m / fps,
                         ease="linear", light_bbox=LIGHT, objects=[], cam=[], **{"lens": 35, "look": LOOK, "exposure": EXPOSURE, **kw})
        SHOTS[name] = self

    def t(self, hb):
        """shot fraction of a half-beat count from the bar line"""
        return min(1.0, hb * HB * self.fps / (self.m - 1))

    def obj(self, blend, keys=None, vis=None, **kw):
        o = dict(blend=blend if blend.startswith("/") else B3 + blend + ".blend", **kw)
        if keys:
            o["keys"] = [dict(t=round(self.t(h), 5), **k) for h, k in keys]
        if vis:
            o["vis"] = [[self.t(a), self.t(b)] for a, b in vis]
        self.spec["objects"].append(o)
        return o

    def cam(self, *keys):
        self.spec["cam"] = [dict(t=round(self.t(h), 5), **k) for h, k in keys]


def ry(deg, v):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [c * v[0] + s * v[2], v[1], -s * v[0] + c * v[2]]


def add(a, b):
    return [round(x + y, 4) for x, y in zip(a, b)]


PARTS = ["fbump", "fender", "dtrim", "uskirt", "lskirt", "rbump"]


def home(s, off=(), hero=()):
    """body + every panel still on the car (1.5 mm copy unless hero) + ALL state fills: under a fitted panel the fill backs
    the seams with real geometry (without it the kept-skin islands dropped as scrap left dark gaps along the panel edges)"""
    s.obj("body_s")      # cut edges smoothed (tools/smooth_body_v3.py)
    for p in PARTS:
        if p in off:
            continue
        s.obj("skin_" + p)   # fitted panel = the car scan's own skin (seamless); the panel scan takes over when it moves
    for f in ("fill_fbump", "fill_fender", "fill_dtrim", "fill_skirts", "fill_rbump"):
        s.obj(f)


def corners(s, skip=(), fr_off=None, rr_off=None):
    """assembled corners (merged 1.5 mm mesh); fr_off / rr_off = parts already removed -> that corner part by part"""
    for c in ("FR", "FL", "RR", "RL"):
        off = fr_off if c == "FR" else rr_off if c == "RR" else None
        if c in skip:
            continue
        if off is None:
            s.obj(f"k_{c}_all")
        else:
            for p in kin.PARTS[c]:
                if p not in off:
                    s.obj(f"k_{c}_{p}")


# ---------------------------------------------------------------- s01 whole car
s = Shot("s01_whole", 1, 15)
home(s); corners(s)
s.cam((0, dict(az=-35, dist=4.6, z=1.5, look=[0.15, 0, 0.55])), (8.6, dict(az=-55, dist=4.7, z=0.30, look=[0.30, -0.1, 0.35])))

# ---------------------------------------------------------------- s02/s03 underbody (one move, two clips)
for name, bar, x0, x1 in (("s02_under_r", 2, -1.75, -0.45), ("s03_under_f", 3, -0.45, 1.2)):
    s = Shot(name, bar, 15, underlight=0.4, lens=32)
    home(s); corners(s)
    s.cam((0, dict(pos=[x0, 0, -0.85], look=[x0 + 0.25, 0, 0.2], up=[1, 0, 0])),
          (8.6, dict(pos=[x1, 0, -0.85], look=[x1 + 0.25, 0, 0.2], up=[1, 0, 0])))

# ---------------------------------------------------------------- s04 front bumper off (A->B)
FB_PIV = BB["part_fbump"]["c"]
FB_PARK, FB_ROT = [1.05, 0, -0.55], [0, 105, 0]
s = Shot("s04_fb_off", 4, 30)
home(s, off=("fbump",)); corners(s)
s.obj("part_fbump", pivot=FB_PIV, keys=[(0, dict(loc=[0, 0, 0])), (2, dict(loc=[0.45, 0, 0], ease="ease_out")),
                                        (3.5, dict(loc=[0.75, 0, -0.10], rot=[0, 35, 0], ease="linear")),
                                        (5, dict(loc=FB_PARK, rot=FB_ROT, ease="ease_out")), (8.1, dict(loc=FB_PARK, rot=FB_ROT))])
s.cam((0, dict(az=-10, dist=2.45, z=1.7, look=[2.25, 0, 0.12])), (8.1, dict(az=-10, dist=2.1, z=1.5, look=[2.6, 0, -0.15])))

# ---------------------------------------------------------------- s05 radar cover + mounting frame nest (bumper alone, park pose)
s = Shot("s05_fb_sub", 5, 30, lens=40)
up_in = ry(105, [-1, 0, 0])      # bumper-local "inside" direction in the park pose (points up at the lens)
s.obj("part_fbump_norad", pivot=FB_PIV, keys=[(0, dict(loc=FB_PARK, rot=FB_ROT)), (8.1, dict(loc=FB_PARK, rot=FB_ROT))])
G1, G2 = add(FB_PARK, [0.30 * v for v in up_in]), add(add(FB_PARK, [0.30 * v for v in up_in]), [0, -0.10, 0])
C1 = add(FB_PARK, [0.13 * v for v in up_in])
# both clip in from the INSIDE of the bumper: the mounting frame lifts off first, then the grille cover follows it out
s.obj("radar_grille", pivot=FB_PIV, keys=[(0, dict(loc=FB_PARK, rot=FB_ROT)), (2, dict(loc=FB_PARK, rot=FB_ROT)),
                                          (3.5, dict(loc=G1, rot=FB_ROT, ease="ease_out")), (8.1, dict(loc=G1, rot=FB_ROT))])
s.obj("radar_cover", pivot=FB_PIV, keys=[(0, dict(loc=FB_PARK, rot=FB_ROT)), (4, dict(loc=FB_PARK, rot=FB_ROT)),
                                         (5.5, dict(loc=C1, rot=FB_ROT, ease="ease_out")), (8.1, dict(loc=C1, rot=FB_ROT))])
s.cam((0, dict(az=-10, dist=2.1, z=1.5, look=[2.6, 0, -0.15])), (2.5, dict(az=-30, dist=1.35, z=0.95, look=[2.70, -0.50, -0.28])),
      (8.1, dict(az=-42, dist=1.1, z=0.60, look=[2.74, -0.62, -0.22])))

# ---------------------------------------------------------------- s06 / s07 what the bumper hid; ducts-removed state swap
s = Shot("s06_fb_beam", 6, 15)
home(s, off=("fbump",)); corners(s)
s.cam((0, dict(az=-35, dist=1.0, z=0.60, look=[2.0, -0.45, 0.36])), (8.6, dict(az=-5, dist=0.85, z=0.60, look=[2.0, 0.0, 0.36])))
s = Shot("s07_fb_duct", 7, 15)
home(s, off=("fbump",)); corners(s)
for o in s.spec["objects"]:
    if o["blend"].endswith("fill_fbump.blend"):
        o["blend"] = B3 + "fill_fduct.blend"
s.cam((0, dict(az=-5, dist=0.85, z=0.60, look=[2.0, 0.0, 0.36])), (8.6, dict(az=-28, dist=0.70, z=0.50, look=[1.95, -0.50, 0.32])))


# ================================================================ corners: solved mechanisms (corners3.json via kin_v3)
def prof(pts, h):
    """piecewise smooth profile [(hb, value), ...] evaluated at hb h"""
    if h <= pts[0][0]:
        return pts[0][1]
    for (h0, v0), (h1, v1) in zip(pts, pts[1:]):
        if h <= h1:
            u = (h - h0) / (h1 - h0); u = u * u * (3 - 2 * u)
            return v0 + (v1 - v0) * u
    return pts[-1][1]


def mech(s, c, pose, pts, extra_keys=None, hidden=(), step=0.2):
    """one corner, every part driven by the solved pose(value) along profile pts; extra_keys = {part: (keys, kwargs)}"""
    hs = [round(x, 3) for x in np.arange(pts[0][0], pts[-1][0] + 1e-6, step)]
    poses = [pose(prof(pts, h)) for h in hs]
    spring = "strut_spring" if c == "FR" else "spring"
    for p in kin.PARTS[c]:
        if p in hidden:
            continue
        k, kw = (extra_keys or {}).get(p, (None, {}))
        if p == spring:
            st = dict(kin.FRONT_SPRING if c == "FR" else kin.REAR_SPRING)
            st["keys"] = [dict(t=round(s.t(h), 5), **po[1]) for h, po in zip(hs, poses)]
            s.obj(f"k_{c}_{p}", stretch=st)
            continue
        o = s.obj(f"k_{c}_{p}", keys=k, **kw)
        if p in poses[0][0]:
            o["mats"] = [dict(t=round(s.t(h), 5), m=po[0][p]) for h, po in zip(hs, poses)]


FRA, RRA = kin.J["FR"]["articulation"], kin.J["RR"]["articulation"]
FWC, FAX = kin.pt(FRA["wheel_centre"]), FRA["spin_axis_outboard"]
RWC, RAX = kin.pt(RRA["wheel_centre"]), RRA["spin_axis_outboard"]
out = lambda ax, d: [round(ax[i] * d, 4) for i in range(3)]     # d metres outboard along the axle
OFF_FRONT = ("fbump",)
FR_OFF = ("wheel", "caliper", "rotor", "dust_shield", "bearing")   # off the car after s09
RR_OFF = ("wheel", "caliper", "rotor")                             # off the car after s14

# ---------------------------------------------------------------- s08 steering sweep, then wheel -> caliper -> rotor off the hub
s = Shot("s08_fc_brake", 8, 30, lens=32)
home(s, off=OFF_FRONT); corners(s, skip=("FR",))
mech(s, "FR", lambda v: kin.front(rack=v), [(0, 0), (1.2, -45), (2.5, 35), (3.3, 0)], {
    "wheel": ([(0, dict()), (3.4, dict()), (4.0, dict(loc=out(FAX, 0.30), ease="ease_out")), (4.8, dict(loc=out(FAX, 0.95))),
               (8.1, dict(loc=out(FAX, 0.95)))], {}),
    "caliper": ([(0, dict()), (4.8, dict()), (5.3, dict(loc=[-0.07, 0, 0.06], ease="ease_out")),
                 (6.1, dict(loc=add([-0.07, 0, 0.06], out(FAX, 0.55)))), (8.1, dict(loc=add([-0.07, 0, 0.06], out(FAX, 0.55))))], {}),
    "rotor": ([(0, dict()), (6.2, dict()), (7.5, dict(loc=out(FAX, 0.33))), (8.1, dict(loc=out(FAX, 0.33)))], {})})
s.cam((0, dict(az=-52, dist=1.75, z=1.05, look=[1.22, -0.95, 0.28])), (3.3, dict(az=-52, dist=1.7, z=1.05, look=[1.22, -1.0, 0.26])),
      (8.1, dict(az=-46, dist=1.9, z=1.15, look=[1.22, -1.25, 0.24])))

# ---------------------------------------------------------------- s09 bump / droop travel, then dust shield and hub bearing off
s = Shot("s09_fc_strut", 9, 30)
home(s, off=OFF_FRONT); corners(s, skip=("FR",))
mech(s, "FR", lambda v: kin.front(travel=v), [(0, 0), (1.1, 38), (2.7, -76), (3.7, 0)], {
    "dust_shield": ([(0, dict()), (4.2, dict()), (5.3, dict(loc=out(FAX, 0.30), ease="ease_out")), (8.1, dict(loc=out(FAX, 0.30)))], {}),
    "bearing": ([(0, dict()), (5.6, dict()), (6.8, dict(loc=out(FAX, 0.15), ease="ease_out")), (8.1, dict(loc=out(FAX, 0.15)))], {})},
     hidden=("wheel", "rotor", "caliper"))
s.cam((0, dict(az=-78, dist=1.05, z=0.50, look=[1.22, -0.80, 0.36])), (8.1, dict(az=-66, dist=0.95, z=0.50, look=[1.22, -0.85, 0.34])))

# ---------------------------------------------------------------- s10 fender section
OFF_SIDE0 = ("fbump",)
s = Shot("s10_fender", 10, 30)
home(s, off=("fbump", "fender")); corners(s, fr_off=FR_OFF)
EXIT = [0, -0.45, -1.05]
s.obj("part_fender", keys=[(0, dict()), (1, dict(loc=[0, -0.12, 0], ease="ease_out")), (2, dict(loc=[0, -0.35, -0.15], ease="linear")),
                           (3.2, dict(loc=EXIT, ease="ease_in"))], vis=[(0, 3.2)])
s.cam((0, dict(az=-90, dist=1.6, z=0.75, look=[0.55, -0.90, 0.55])), (8.1, dict(az=-90, dist=1.0, z=0.75, look=[0.60, -0.85, 0.50])))

# ---------------------------------------------------------------- s11 skirts + door trim unclip from the sill
s = Shot("s11_skirts", 11, 30)
home(s, off=("fbump", "fender", "dtrim", "uskirt", "lskirt")); corners(s, fr_off=FR_OFF)
for part, h0 in (("part_lskirt", 0), ("part_uskirt", 1.2), ("part_dtrim", 2.4)):
    if h0:
        s.obj(part.replace("part_", "skin_"), vis=[(0, h0 - 0.02)])
    s.obj(part, keys=[(0, dict()), (h0, dict()), (h0 + 0.4, dict(loc=[0, -0.10, 0], ease="ease_out")),
                      (h0 + 1.9, dict(loc=[0, -0.55, -0.95], ease="ease_in"))], vis=[(h0, h0 + 1.9)])
s.cam((0, dict(az=-104, dist=2.5, z=0.50, look=[-0.10, -0.90, 0.28])), (4.3, dict(az=-98, dist=2.1, z=0.45, look=[-0.10, -0.90, 0.26])),
      (8.1, dict(az=-94, dist=1.75, z=0.42, look=[-0.20, -0.90, 0.25])))
s = Shot("s11b_sill", 12, 15)            # stay on the section: travel along the exposed sill and door-trim structure
home(s, off=("fbump", "fender", "dtrim", "uskirt", "lskirt")); corners(s, fr_off=FR_OFF)
s.cam((0, dict(pos=[-1.25, -1.95, 0.42], look=[-0.80, -0.85, 0.30])), (8.6, dict(pos=[0.45, -1.80, 0.26], look=[0.35, -0.85, 0.12])))
OFF_SIDE = ("fbump", "fender", "dtrim", "uskirt", "lskirt")

# ---------------------------------------------------------------- s12 interior x-ray (two layers, one camera) / s13 console
XCAM = ((0, dict(pos=[-1.25, 0, 3.05], look=[-0.62, 0, 0.5], up=[1, 0, 0])), (8.6, dict(pos=[-0.75, 0, 2.45], look=[-0.35, 0, 0.5], up=[1, 0, 0])))
s = Shot("s12a_shell", 13, 15)           # layer a: only the first frames are rendered (crossfade ends on hb2)
home(s, off=OFF_SIDE); corners(s, fr_off=FR_OFF); s.obj("interior"); s.obj("console"); s.cam(*XCAM)
s.spec["_render_frames"] = "1-8"
s = Shot("s12_int_xray", 13, 15)
s.obj("interior"); s.obj("console"); s.cam(*XCAM)
s = Shot("s13_int_console", 14, 30)
s.obj("interior")
CPARK = [-0.15, 0, 0.50]
s.obj("console", keys=[(0, dict()), (1, dict()), (2, dict(loc=[0, 0, 0.08], ease="ease_out")), (2.8, dict(loc=[-0.10, 0, 0.25], ease="linear")),
                       (3.6, dict(loc=CPARK, ease="ease_out")), (8.1, dict(loc=CPARK))])
s.cam((0, dict(pos=[0.9, 0, 1.55], look=[0.2, 0, 0.55])), (4.5, dict(pos=[0.75, 0, 1.5], look=[0.0, 0, 0.5])),
      (8.1, dict(pos=[-0.6, 0, 1.45], look=[-1.35, 0, 0.55])))

# ---------------------------------------------------------------- s14 rear: wheel -> caliper -> rotor off, then the five-link works
s = Shot("s14_rc", 15, 30, lens=32)
home(s, off=OFF_SIDE); corners(s, skip=("RR",), fr_off=FR_OFF)
mech(s, "RR", lambda v: kin.rear(travel=v), [(3.8, 0), (4.8, 45), (6.3, -75), (7.4, 0)], {
    "wheel": ([(0, dict()), (0.8, dict(loc=out(RAX, 0.30), ease="ease_out")), (1.6, dict(loc=out(RAX, 0.95))), (3.3, dict(loc=out(RAX, 0.95))),
               (4.5, dict(loc=add(out(RAX, 1.1), [1.5, 0, -0.5]), ease="ease_in"))], dict(vis=[(0, 4.5)])),   # leaves the frame before the push-in
    "caliper": ([(0, dict()), (1.6, dict()), (2.1, dict(loc=[0.07, 0, 0.05], ease="ease_out")), (2.8, dict(loc=add([0.07, 0, 0.05], out(RAX, 0.55)))),
                 (8.1, dict(loc=add([0.07, 0, 0.05], out(RAX, 0.55))))], {}),
    "rotor": ([(0, dict()), (2.6, dict()), (3.7, dict(loc=out(RAX, 0.33))), (8.1, dict(loc=out(RAX, 0.33)))], {})})
for o in s.spec["objects"]:      # parts already off the hub must not ride the suspension travel
    if o["blend"].split("/")[-1] in ("k_RR_wheel.blend", "k_RR_caliper.blend", "k_RR_rotor.blend"):
        o.pop("mats", None)
s.cam((0, dict(az=-128, dist=1.8, z=1.05, look=[-1.24, -0.95, 0.26])), (3.7, dict(az=-126, dist=1.85, z=1.0, look=[-1.24, -1.2, 0.24])),
      (8.1, dict(az=-112, dist=1.35, z=0.62, look=[-1.26, -0.95, 0.24])))

# ---------------------------------------------------------------- s15 rear bumper off / s16 what it hid
RB_PIV = BB["part_rbump"]["c"]
RB_PARK, RB_ROT = [-1.05, 0, -0.55], [0, -105, 0]
OFF_ALL = OFF_SIDE + ("rbump",)
s = Shot("s15_rb_off", 16, 30)
home(s, off=OFF_ALL); corners(s, fr_off=FR_OFF, rr_off=RR_OFF); s.obj("interior"); s.obj("console")
s.obj("part_rbump", pivot=RB_PIV, keys=[(0, dict(loc=[0, 0, 0])), (2, dict(loc=[-0.45, 0, 0], ease="ease_out")),
                                        (3.5, dict(loc=[-0.75, 0, -0.10], rot=[0, -35, 0], ease="linear")),
                                        (5, dict(loc=RB_PARK, rot=RB_ROT, ease="ease_out")), (8.1, dict(loc=RB_PARK, rot=RB_ROT))])
s.cam((0, dict(az=-162, dist=2.45, z=1.7, look=[-2.25, 0, 0.12])), (8.1, dict(az=-162, dist=2.1, z=1.5, look=[-2.6, 0, -0.15])))
s = Shot("s16_rb_beam", 17, 15)
home(s, off=OFF_ALL); corners(s, fr_off=FR_OFF, rr_off=RR_OFF); s.obj("interior"); s.obj("console")
s.cam((0, dict(az=-155, dist=1.25, z=0.62, look=[-2.0, -0.45, 0.40])), (8.6, dict(az=-185, dist=1.0, z=0.62, look=[-2.0, 0.25, 0.36])))

# ---------------------------------------------------------------- s17 line-up / s18 reassembly / s19 clean car
TILT = [-70, 0, 0]   # thin side panels: outer face up toward the overhead lens
LINE = {  # part: (pivot or None, loc, rot)
    "part_fbump": (FB_PIV, [0.60, 0, 0], [0, 105, 0]), "part_rbump": (RB_PIV, [-0.60, 0, 0], [0, -105, 0]),
    "part_fender": (None, [-0.05, -0.75, 0], TILT), "part_dtrim": (None, [0, -0.62, 0], TILT),
    "part_uskirt": (None, [0, -1.10, 0], TILT), "part_lskirt": (None, [0, -1.48, 0], TILT),
    "k_FR_wheel": (None, out(FAX, 1.05), [0, 0, 0]), "k_FR_caliper": (None, add([-0.07, 0, 0.06], out(FAX, 0.66)), [0, 0, 0]),
    "k_FR_rotor": (None, out(FAX, 0.46), [0, 0, 0]), "k_FR_dust_shield": (None, out(FAX, 0.30), [0, 0, 0]),
    "k_FR_bearing": (None, out(FAX, 0.15), [0, 0, 0]),
    "k_RR_wheel": (None, out(RAX, 1.05), [0, 0, 0]), "k_RR_caliper": (None, add([0.07, 0, 0.05], out(RAX, 0.62)), [0, 0, 0]),
    "k_RR_rotor": (None, out(RAX, 0.38), [0, 0, 0]),
}
SEAT = {"k_FR_bearing": 1.5, "k_FR_dust_shield": 2.2, "k_FR_rotor": 3, "k_RR_rotor": 3, "k_FR_caliper": 4, "k_RR_caliper": 4,
        "k_FR_wheel": 5, "k_RR_wheel": 5, "part_fender": 6, "part_dtrim": 6, "part_uskirt": 6, "part_lskirt": 6.5, "part_rbump": 7, "part_fbump": 8}
s = Shot("s17_lineup", 18, 15, lens=31)
home(s, off=OFF_ALL); corners(s, fr_off=FR_OFF, rr_off=RR_OFF); s.obj("interior"); s.obj("console")
for n, (piv, loc, rot) in LINE.items():
    kw = dict(pivot=piv) if piv else {}
    s.obj(n, keys=[(0, dict(loc=loc, rot=rot)), (8.6, dict(loc=loc, rot=rot))], **kw)
s.cam((0, dict(pos=[-0.5, -0.55, 3.75], look=[0.0, -0.55, 0.3], up=[1, 0, 0])), (8.6, dict(pos=[-0.45, -0.55, 3.55], look=[0.0, -0.55, 0.3], up=[1, 0, 0])))
s = Shot("s18_reasm", 19, 30)
home(s, off=OFF_ALL); corners(s, fr_off=FR_OFF, rr_off=RR_OFF); s.obj("interior"); s.obj("console")
for n, (piv, loc, rot) in LINE.items():
    kw = dict(pivot=piv) if piv else {}
    h = SEAT[n]
    s.obj(n, keys=[(0, dict(loc=loc, rot=rot)), (max(0, h - 2.2), dict(loc=loc, rot=rot)), (h, dict(loc=[0, 0, 0], rot=[0, 0, 0], ease="ease_in")),
                   (8.1, dict(loc=[0, 0, 0], rot=[0, 0, 0]))], vis=[(0, h - 0.02)] if n.startswith("part_") and h < 8 else None, **kw)
    if n.startswith("part_") and h < 8:
        s.obj(n.replace("part_", "skin_"), vis=[(h, 8.2)])     # seated: back to the car's own seamless skin
s.cam((0, dict(az=-55, dist=6.6, z=3.0, look=[0.2, -0.3, 0.40])), (8.1, dict(az=-55, dist=5.2, z=2.3, look=[0.2, 0, 0.45])))
s = Shot("s19_clean", 20, 15)
home(s); corners(s)
s.cam((0, dict(az=-55, dist=5.2, z=2.3, look=[0.2, 0, 0.45])), (8.6, dict(az=-58, dist=4.7, z=1.9, look=[0.2, 0, 0.45])))


if __name__ == "__main__":
    os.makedirs(D + "/shots_v3", exist_ok=True)
    tl = []
    for n, s in SHOTS.items():
        json.dump(s.spec, open(f"{D}/shots_v3/{n}.json", "w"), indent=1)
        tl.append(dict(shot=n, bar=s.bar, fps=s.fps, reel_frames=s.spec["_reel_frames"], rendered=s.m))
    tl.sort(key=lambda x: x["bar"])
    json.dump(dict(track_start=TRACK0, bar=BAR, bars=F, shots=tl), open(D + "/timeline_v3.json", "w"), indent=1)
    print(len(SHOTS), "shots,", sum(s.m for s in SHOTS.values()), "frames")
