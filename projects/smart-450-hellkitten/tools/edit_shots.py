"""Shot table for the Smart 450 'Hellkitten' reel v3 ("Should we build this?"). v1's table is in git history (edit_shots v1).

Timeline positions are beats m on the fitted 160.00 BPM lattice, T(m) = 1.499 + 0.37583 m; a shot starts on frame F(m) = round(T*30)
(F(-4) = 0). The music (music_v2.py) is built on the same grid, the meows (meows.py) too.
IRL windows are source pixels on the upright frame (w, h) with keyed top-left corners [(fraction, x0, y0), ...].
Stills: mode 'win' (9:16 window cut from the 1440x1440 image, keys = (x0, y0, w) at t=0 and t=1) or 'fit' (image fitted to 1080 wide
on a blurred, darkened fill of itself: for studio renders whose car is wider than any 9:16 window; zoom z0 -> z1, centre cx, cy in image px).
"""
DB = "/home/user/media/smart-hellkitten/dropbox"
DESIGN = "/home/user/media/smart-hellkitten/design"
SM = "/home/user/media/work/smart-450"
FPS = 30
T = lambda m: 1.499 + 0.37583 * m
F = lambda m: 0 if m <= -4 else int(round(T(m) * FPS))

def S(id, m0, m1, **kw):
    d = dict(id=id, start=F(m0), n=F(m1) - F(m0), m0=m0, m1=m1)
    d.update(kw); return d

SHOTS = [
    S("H1", -4, 0, kind="scan", scan="a5_xray", t0=0.0, text=("THIS IS A", "SMART CAR?"), section="hook_render",
      focus="the Hellkitten with the Smart inside it as an x-ray: 'THIS IS A SMART CAR?'"),
    S("S5", 0, 2, kind="irl", src="v_1632_12", ss=0.000, win=(608, 1080), keys=[(0, 370, 0)], audio=None, section="whole_assembled",
      focus="here is the real car: black and intact"),
    S("S6", 2, 4, sharp=True, kind="irl", src="v_1634_19", ss=14.500, win=(608, 1080), keys=[(0, 560, 0), (1, 450, 0)], audio="up",
      section="assembled_front", focus="powder turns black paint matte grey"),
    S("S7", 4, 6, sharp=True, kind="irl", src="v_1634_19", ss=6.900, win=(608, 1080), keys=[(0, 500, 0)], audio="up", section="assembled_side",
      focus="the powder mist on the door"),
    S("S8", 6, 8, kind="irl", src="v_1634_51", ss=0.150, win=None, keys=None, audio="up", section="assembled_rear",
      focus="tail lamp goes matte"),
    S("S9", 8, 12, kind="irl", src="v_1724_26", ss=11.000, win=(990, 1760), keys=[(0, 85, 0)], audio=None, section="scanner",
      focus="the scanner: green = captured"),
    S("S1", 12, 14, sharp=True, kind="irl", src="v_1852_56", ss=20.800, win=(504, 896), keys=[(0, 736, 184), (0.5, 900, 184), (1, 1100, 184)],
      audio=None, section="parts_off", focus="the car comes apart: panels on the floor"),
    S("S13", 14, 16, kind="irl", src="v_1852_56", ss=6.000, win=(608, 1080), keys=[(0, 600, 0), (1, 630, 0)], audio=None,
      section="stripped_front", focus="front end off, nose on the jack"),
    S("S12", 16, 18, kind="irl", src="v_1712_33", ss=19.050, win=(608, 1080), keys=[(0, 540, 0)], audio=None, section="stripped_rear",
      focus="the bare rear"),
    S("S4", 18, 20, kind="irl", src="v_1857_58", ss=1.200, win=(608, 1080), keys=[(0, 520, 0), (1, 600, 0)], audio=None,
      section="stripped_side", focus="hand on the real door braces"),
    S("S17", 20, 22, kind="irl", src="v_1729_10", ss=0.480, win=(608, 1080), keys=[(0, 590, 0)], audio=None, section="scanner_result",
      focus="the scan is on the device"),
    S("S2", 22, 24, kind="irl", src="v_1852_56", ss=None, end_ss=26.0333, win=(608, 1080), keys=[(0, 760, 0)], audio=None,
      section="stripped_side", focus="the bare shell (ends on the solved 26.0 s frame)"),
    S("S3", 24, 28, kind="scan", scan="a1_match_str", t0=0.0, section="stripped_side", focus="the same frame as a 3D scan: proof this is real engineering (1:1 cut)"),
    S("S10a", 28, 32, kind="scan", scan="a2_body_on_off", t0=0.1, last_png=24, section="whole_scan", focus="scan, body on"),
    S("S10b", 32, 40, kind="scan", scan="a2_body_on_off", t0=1.6, speed=1.11, section="whole_scan", focus="body off on the drop; push to the structure"),
    S("S18", 40, 50, kind="scan", scan="a4_hellkitten", t0=0.0, speed=1.2, section="hellkitten_model",
      focus="same camera: the stripped scan becomes the textured Hellkitten body"),
    S("R1", 50, 52, kind="still", img="Blueprint.jpeg", mode="blueprint", section="payoff_design", focus="the new body drawn over this Smart"),
    S("R2", 52, 53, kind="still", img="drive/4.r.2/4.r.2.jpg", mode="fit", z=(1.3, 1.42), c=(720, 730), shift=(-30, 0), section="renders", focus="front"),
    S("R3", 53, 54, kind="still", img="4.r.4.jpg", mode="fit", z=(1.45, 1.3), c=(720, 700), shift=(40, 0), section="renders", focus="side, kitten decal"),
    S("R4", 54, 55, kind="still", img="drive/4.r.5/4.r.5.jpg", mode="fit", z=(1.3, 1.42), c=(750, 650), shift=(0, 30), section="renders", focus="from above"),
    S("R5", 55, 56, kind="still", img="drive/4.r.6/4.r.6.jpg", mode="fit", z=(1.42, 1.28), c=(780, 700), shift=(-30, 0), section="renders", focus="rear"),
    S("R6", 56, 58, kind="still", img="4.r.1.jpg", mode="fit", z=(1.2, 1.32), c=(742, 700), shift=(0, -40), yc=0.55, section="renders", focus="drop 3: front three-quarter"),
    S("R7", 58, 59, kind="still", img="RenderStreet2.jpeg", mode="win", w=(780, 640), x0=(367, 437), y0=(53, 100), section="renders", focus="on the street"),
    S("R7b", 59, 60, kind="still", img="RenderNight2.jpeg", mode="win", w=(640, 760), x0=(452, 392), y0=(91, 85), section="renders", focus="at night"),
    S("R8", 60, 64, kind="still", img="RenderDay1.jpeg", mode="win", w=(810, 778), x0=(310, 326), y0=(0, 44), plate=(12, 46, 100, 560, 0.62), section="payoff_render",
      focus="the render, and the question"),
    S("LOGO", 64, 72, kind="logo", section="logo", focus="logo card"),
]
END = F(72)

# frames of each scan shot's PNG sequence that must exist for the shot to count as finished (direction.md section 4)
SCAN_NEED = {"a1_match_str": 26, "a2_body_on_off": 75, "a4_hellkitten": 68, "a5_xray": 25}
