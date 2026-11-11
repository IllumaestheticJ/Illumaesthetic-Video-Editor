"""v2 shot specs (plan: projects/subaru-wrx-vb/director.md, order: direction.md) -> JSON for tools/shot.py.

    python projects/subaru-wrx-vb/tools/shots_v2.py preview|final [shot ...]

Travel: whole car (front-right) -> scoop (reused v1 s4) -> FRONT OFF (hero, on the 11.191 drop) -> SIDE OFF (right
cladding, one part per bar) -> REAR OFF -> REASSEMBLE (rear -> side -> front, lock 30.736) -> fade -> small logo.
Reel times are on the broadband grid 11.1910 + 1.39609 n; shot keys below are seconds from each shot's start.
Scan frame: front = -Y, car's right = -X, Z up, metres. Persistent data is off automatically (keyed parts).
"""
import json
import os
import sys

P = "/home/user/media/subaru-wrx-vb/prep"
OUT = "/home/user/media/work/wrx/renders"
SPECS = "/home/user/media/work/wrx/specs"
CAR = f"{P}/car4np.blend"
XB = f"{P}/base_xnp.blend"
FBUMP, PLATE = f"{P}/p_front_bumper_inside_parts_included.blend", f"{P}/plate_xnp.blend"
GARN = f"{P}/p_front_bumper_lower_garnish.blend"
RBUMP = f"{P}/p_rear_bumper_updated.blend"
FFL, DFL, RFL, SKIRT = (f"{P}/p_front_flare.blend", f"{P}/p_door_flare.blend", f"{P}/p_rear_flare.blend",
                        f"{P}/p_side_skirt_only.blend")
# shared pivots = bbox centres (prep json) so the plate stays on the bumper through the flip
PIV_F = [-0.006, -2.007, 0.466]
PIV_R = [0.0065, 1.952, 0.548]
# off poses (director.md table)
OFF = {FBUMP: ((0, -0.55, 2.00), (0, 0, 0)), PLATE: ((0, -0.55, 2.00), (0, 0, 0)), GARN: ((0, -0.45, 1.45), (0, 0, 0)),
       FFL: ((-0.45, 0, 0.90), (0, -8, 0)), DFL: ((-0.45, 0, 0.90), (0, -8, 0)), RFL: ((-0.45, 0, 0.90), (0, -8, 0)),
       SKIRT: ((-0.60, 0, -0.12), (0, 0, 0)), RBUMP: ((0, 0.40, 1.70), (0, 0, 0))}
PIVOT = {FBUMP: PIV_F, PLATE: PIV_F, RBUMP: PIV_R}
# preview v1 of v2: parts resting at OFF sat half-clipped at the frame edges of the close section shots. Inside the
# section shots removed parts leave the frame for good (AWAY); the reassembly starts from the visible OFF poses.
AWAY = dict(OFF)
AWAY.update({FBUMP: ((0, -0.55, 6.0), (0, 0, 0)), PLATE: ((0, -0.55, 6.0), (0, 0, 0)), GARN: ((0, -0.45, 5.5), (0, 0, 0)),
             FFL: ((-0.40, 0, 2.0), (0, -8, 0)), DFL: ((-0.40, 0, 2.0), (0, -8, 0)), RFL: ((-0.40, 0, 2.0), (0, -8, 0)),
             RBUMP: ((0, 0.40, 2.9), (0, 0, 0))})

SHOT_START = {"v2_opener": 0.0, "v2_front_off": 8.707, "v2_side_off": 16.775, "v2_rear_off": 22.360,
              "v2_reassemble": 27.944}
SECS = {"v2_opener": 5.224, "v2_front_off": 8.068, "v2_side_off": 5.585, "v2_rear_off": 5.584, "v2_reassemble": 4.188}


def K(t, loc=(0, 0, 0), rot=(0, 0, 0), ease="inout"):
    return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}


def C(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": list(loc), "target": list(tgt), "focal": focal, "ease": ease}


def part(b, keys):
    d = {"blend": b, "keys": keys}
    if b in PIVOT:
        d["pivot"] = PIVOT[b]
    return d


def parked(b, end):  # already removed: out of frame (AWAY) for the whole shot
    o, r = AWAY[b]
    return part(b, [K(0, o, r), K(end + 1, o, r, "lin")])


def rt(name, reel_t):  # reel time -> shot time
    return round(reel_t - SHOT_START[name], 3)


SHOTS = {}

# 1. whole car, elevated front-right 3/4, moving from frame 1
SHOTS["v2_opener"] = {"base": [CAR], "parts": [], "cam": [
    C(0, (-1.10, -5.90, 2.80), (0.40, -0.30, 0.60), 38, "lin"),
    C(SECS["v2_opener"], (-2.15, -5.89, 2.40), (0.25, -0.50, 0.60), 38)]}

# 3. FRONT OFF (hero): bumper + plate leave forward on the drop, flip to show the scanned inner face, rise away;
# garnish slides forward on the floor then lifts; camera ends low and close on the scanned crash structure.
n = "v2_front_off"
fb_keys = [K(0), K(rt(n, 11.191)), K(rt(n, 11.715), (0, -0.75, 0.25), ease="out"),
           K(rt(n, 12.587), (0, -0.85, 0.95), (-160, 0, 0)), K(rt(n, 13.983), (0, -0.85, 1.03), (-160, 0, 0), "lin"),
           K(rt(n, 14.681), *AWAY[FBUMP]), K(SECS[n] + 1, *AWAY[FBUMP], ease="lin")]
g_keys = [K(0), K(rt(n, 12.587)), K(rt(n, 13.285), (0, -0.60, -0.02)), K(rt(n, 13.983), (0, -0.65, 0.60)),
          K(rt(n, 14.681), *AWAY[GARN]), K(SECS[n] + 1, *AWAY[GARN], ease="lin")]
SHOTS[n] = {"base": [XB, RBUMP, FFL, DFL, RFL, SKIRT],
            "parts": [part(FBUMP, fb_keys), part(PLATE, fb_keys), part(GARN, g_keys)],
            "cam": [C(0, (-2.10, -5.30, 1.20), (-0.10, -2.05, 0.60), 42),
                    C(2.484, (-1.90, -4.90, 1.10), (-0.10, -2.05, 0.62), 42),
                    C(3.880, (-2.10, -6.40, 1.55), (-0.05, -2.90, 1.30), 30),
                    C(5.276, (-1.90, -6.00, 1.55), (-0.05, -2.90, 1.35), 30),
                    C(8.068, (-1.30, -3.80, 1.05), (-0.05, -2.00, 0.66), 28)]}

# 4. SIDE OFF: front-right wheel, then front flare / door flare / rear flare / skirt, one per bar, travelling rearward
n = "v2_side_off"


def lift(b, go):
    o, r = AWAY[b]
    first = (-0.35, 0, 0.10) if b != SKIRT else None
    ks = [K(0), K(go)]
    if first:
        ks.append(K(go + 0.349, first, r, "out"))
    ks += [K(go + 1.047, o, r, "out" if not first else "inout"), K(SECS[n] + 1, o, r, "lin")]
    return part(b, ks)


SHOTS[n] = {"base": [XB, RBUMP],
            "parts": [parked(b, SECS[n]) for b in (FBUMP, PLATE, GARN)]
            + [lift(FFL, 0.0), lift(DFL, 1.396), lift(RFL, 2.793), lift(SKIRT, 4.189)],
            "cam": [C(0, (-2.70, -0.30, 1.45), (-0.95, -1.30, 0.55), 30),
                    C(1.396, (-3.00, -0.90, 1.10), (-0.90, -0.60, 0.70), 30, "lin"),
                    C(2.792, (-3.20, 0.40, 1.10), (-0.90, 0.40, 0.65), 30, "lin"),
                    C(4.188, (-3.00, 1.60, 1.05), (-0.90, 1.25, 0.60), 30, "lin"),
                    C(5.585, (-7.40, 0.40, 2.20), (-0.60, 0.30, 0.90), 26)]}

# 5. REAR OFF: same grammar as the front
n = "v2_rear_off"
rb_keys = [K(0), K(0.0), K(0.524, (0, 0.70, 0.20), ease="out"), K(1.396, (0, 0.80, 0.90), (160, 0, 0)),
           K(2.792, (0, 0.80, 0.98), (160, 0, 0), "lin"), K(3.490, *AWAY[RBUMP]), K(SECS[n] + 1, *AWAY[RBUMP], ease="lin")]
SHOTS[n] = {"base": [XB],
            "parts": [parked(b, SECS[n]) for b in (FBUMP, PLATE, GARN, FFL, DFL, RFL, SKIRT)] + [part(RBUMP, rb_keys)],
            "cam": [C(0, (-1.50, 5.40, 0.95), (0.0, 1.95, 0.60), 30),
                    C(1.396, (-1.60, 6.60, 1.45), (0.0, 2.75, 1.30), 30),
                    C(2.792, (-1.45, 6.30, 1.50), (0.0, 2.75, 1.35), 30),
                    C(5.584, (-1.10, 4.00, 1.00), (-0.05, 2.05, 0.64), 28)]}

# 6. REASSEMBLE: rear -> side -> front, front bumper locks on 30.736 (shot t 2.792 = frame 43); frames 43+ re-rendered
# with the clean car (v2_reassemble_car) so no composite seams show after the lock
n = "v2_reassemble"


def home(b, t0, t1, ease="inout"):
    o, r = OFF[b]
    return part(b, [K(0, o, r), K(t0, o, r, "lin"), K(t1, (0, 0, 0), (0, 0, 0), ease), K(SECS[n] + 1, ease="lin")])


RCAM = [C(0, (-1.79, 6.32, 3.40), (0.40, 0.30, 0.90), 28, "lin"), C(SECS[n], (-2.75, 5.61, 2.60), (0.20, 0.50, 0.60), 28)]
SHOTS[n] = {"base": [XB],
            "parts": [home(RBUMP, 0.0, 0.698), home(RFL, 0.698, 1.396), home(DFL, 0.873, 1.571), home(SKIRT, 0.873, 1.571),
                      home(FFL, 1.047, 1.745), home(GARN, 1.745, 2.443), home(FBUMP, 2.094, 2.792, "in"),
                      home(PLATE, 2.094, 2.792, "in")],
            "cam": RCAM, "frame_range": [1, 42]}
SHOTS["v2_reassemble_car"] = {"base": [CAR], "parts": [], "cam": RCAM, "frame_range": [43, 64],
                              "secs": SECS[n], "out": "v2_reassemble"}

PREVIEW = {"v2_opener": ["first", "last"],
           "v2_front_off": [1, 38, 46, 59, 75, 90, 122], "v2_side_off": [1, 12, 33, 54, 75, 85],
           "v2_rear_off": [1, 9, 22, 43, 53, 85], "v2_reassemble": [1, 15, 30, 42], "v2_reassemble_car": [43, 64]}


def spec(name, mode):
    s = SHOTS[name]
    final = mode == "final"
    secs = s.get("secs", SECS.get(name))
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": secs + 1 / 15, "fps": 15, "res": "1080x1920",
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{s.get('out', name)}"}
    if final and s.get("frame_range"):
        sp["frame_range"] = s["frame_range"]
    if not final:
        sp["frames"] = PREVIEW.get(name, ["first", "mid", "last"])
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for nm in sys.argv[2:] or list(SHOTS):
        print(spec(nm, mode))
