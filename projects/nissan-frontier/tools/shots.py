"""Shot specs for the Nissan Frontier Pro-4X Temerario-style reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/nissan-frontier/tools/shots.py preview|final [shot ...]

Prep frame (metres, from car4.json): nose -Y (y=-2.68), tail +Y (2.69), car's right = -X, z=0 is the frame bottom
(lift-pad cut at 200 mm; the real ground is z=-0.2). levelled mm -> prep m: x/1000-0.062, y/1000+0.808, z/1000-0.2.
SECS are render lengths; they are a little longer than the planned holds so the edit can be cut to the music.
"""
import json, math, os, sys

P = "/home/user/media/nissan-frontier/prep"
OUT = "/home/user/media/work/frontier/renders"
SPECS = "/home/user/media/nissan-frontier/specs"
CAR = f"{P}/car4.blend"
FRONT_HI = f"{P}/front2.blend"
TIMING = json.load(open(os.path.join(os.path.dirname(__file__), "..", "timing.json")))  # per-shot seconds + beat marks
SECS = {k: v["secs"] for k, v in TIMING["shots"].items()}


def orbit(t, r, ang_deg, h, c=(0, 0, 0.7), focal=30, ease="inout", tz=None):
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def keyed_orbit(T, r0, r1, a0, a1, h0, h1, c0, c1, focal=30, n=8, tz=None):
    """many keys so the camera follows the arc instead of a chord"""
    ks = []
    for k in range(n + 1):
        u = k / n; s = u * u * (3 - 2 * u)
        c = [c0[i] + (c1[i] - c0[i]) * s for i in range(3)]
        ks.append(orbit(T * u, r0 + (r1 - r0) * s, a0 + (a1 - a0) * s, h0 + (h1 - h0) * s, c=c, focal=focal, ease="lin", tz=tz))
    return ks


# angle 0 = camera in front of the truck (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind
HOOD_PIVOT = [-0.062, -1.462, 1.04]   # hood rear shut line (levelled y -2270, z ~1240)


def hold_then(keys_after, t0):
    return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": t0, "loc": [0, 0, 0], "rot": [0, 0, 0]}] + keys_after


def shots():
    S = SECS; B = TIMING.get("beat", 0.6)
    sh = {
        # 1. low front-right 3/4 turntable; the bed runs out of frame on the right (crop for 9:16)
        "s1_front34": {"base": [CAR], "cam": keyed_orbit(S["s1_front34"], 5.0, 4.7, -28, -58, 0.75, 0.95,
                                                          (0, -1.1, 0.62), (0, -1.0, 0.65))},
        # 2. low rear-left 3/4 orbit (car's left), tailgate + bed, cab cropped at the B-pillar
        "s2_rear34": {"base": [CAR], "cam": keyed_orbit(S["s2_rear34"], 5.0, 4.8, 148, 122, 0.9, 1.25,
                                                         (0, 1.2, 0.6), (0, 1.0, 0.62))},
        # 3. extreme close-up: grille + right headlamp, slow slide across the nose (2 mm)
        "s3_grille": {"base": [FRONT_HI], "cam": [
            {"t": 0, "loc": [-1.35, -3.75, 0.95], "target": [-0.35, -2.62, 0.78], "focal": 40},
            {"t": S["s3_grille"], "loc": [-0.15, -3.95, 0.88], "target": [-0.2, -2.62, 0.74], "focal": 40, "ease": "inout"}]},
        # 4. extreme close-up: front-right wheel arch (no wheel on the lift - the scanned suspension is the detail)
        "s4_arch": {"base": [FRONT_HI], "cam": [
            {"t": 0, "loc": [-2.45, -3.0, 0.55], "target": [-0.8, -1.95, 0.42], "focal": 34},
            {"t": S["s4_arch"], "loc": [-2.35, -1.6, 0.5], "target": [-0.8, -2.0, 0.42], "focal": 34, "ease": "inout"}]},
        # 5. front opens: bumper (+grille) slides forward and down, hood lifts on its rear shut line
        "s5_open": {"base": [f"{P}/comp_front.blend"], "parts": [
            {"blend": f"{P}/x_hood.blend", "pivot": HOOD_PIVOT,
             "keys": hold_then([{"t": TIMING["open"]["hood"][1], "loc": [0, 0, 0], "rot": [-60, 0, 0], "ease": "inout"}],
                               TIMING["open"]["hood"][0])},
            {"blend": f"{P}/x_bumper.blend",
             "keys": hold_then([{"t": TIMING["open"]["bumper"][1], "loc": [0, -0.9, -0.12], "rot": [0, 0, 0], "ease": "inout"}],
                               TIMING["open"]["bumper"][0])},
            {"blend": f"{P}/x_grille.blend",
             "keys": hold_then([{"t": TIMING["open"]["bumper"][1], "loc": [0, -0.9, -0.12], "rot": [0, 0, 0], "ease": "inout"}],
                               TIMING["open"]["bumper"][0])}],
            "cam": keyed_orbit(S["s5_open"], 5.2, 4.6, -38, -22, 1.9, 2.3, (0, -1.9, 0.55), (0, -2.1, 0.55))},
        # 6. top-down: high rear-right 3/4 rising over to straight down, nose at the top of the frame
        "s6_top": {"base": [CAR], "cam": [
            {"t": 0, "loc": [-2.6, 4.4, 3.6], "target": [0, 0.4, 0.55], "focal": 30},
            {"t": S["s6_top"], "loc": [0.0, 0.25, 6.3], "target": [0, 0.0, 0.55], "focal": 30, "ease": "inout"}]},
    }
    E = TIMING["explode"]  # sep_start, sep_end, back_start, lock (seconds from shot start)

    def ex(off, rot=(0, 0, 0), d=0.0):
        return [{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": E[0] + d, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": E[1] + d, "loc": list(off), "rot": list(rot), "ease": "out"},
                {"t": E[2], "loc": [o * 1.06 for o in off], "rot": list(rot), "ease": "lin"},
                {"t": E[3], "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "in"}]
    sh["s7_explode"] = {"base": [f"{P}/comp_explode.blend"], "parts": [
        {"blend": f"{P}/x_hood.blend", "keys": ex((0, -0.2, 1.05), (-10, 0, 0))},
        {"blend": f"{P}/x_bumper.blend", "keys": ex((0, -0.95, -0.05), d=0.06)},
        {"blend": f"{P}/x_grille.blend", "keys": ex((0, -1.55, 0.25), d=0.12)},
        {"blend": f"{P}/x_flares.blend", "keys": ex((0, 0, 0.55), d=0.18)}],
        # high front-right, orbiting toward the side; radius swells while the parts are out
        "cam": [orbit(S["s7_explode"] * k / 12, 7.0 + 1.2 * math.sin(math.pi * k / 12), -42 - 50 * (k / 12),
                      3.4 - 0.4 * (k / 12), c=(0, -0.9 + 0.7 * (k / 12), 0.6), focal=28, ease="lin", tz=0.5)
                for k in range(13)]}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]
    final = mode == "final"
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": SECS[name] + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    if frames:
        sp["frames"] = frames
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    fr = None
    if mode == "check":
        mode, fr = "preview", ["first", "mid", "last"]
    for n in sys.argv[2:] or list(shots()):
        print(spec(n, mode, fr))
