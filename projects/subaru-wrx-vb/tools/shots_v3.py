"""v3 shot specs -> JSON for tools/shot.py (v2 reviewer notes: new track, deeper front teardown, trunk opens,
clean bumper cut-out).

    python projects/subaru-wrx-vb/tools/shots_v3.py preview|final [shot ...]

Music: Roni Size - The Streets (user upload), reel = track 146.799 -> ; strong-beat grid (kick, beat 1 of each bar)
track 153.635 + 1.36720 n = reel 1.36720 n; the drop slams in half a bar early at track 152.951 = reel 6.152.
Travel: whole car -> scoop -> FRONT (grille, lower garnish, bumper shell come off one per beat on the drop) -> SIDE
(right cladding, one part per bar) -> REAR (trunk opens on its fitted hinge, then the rear bumper) -> REASSEMBLE
-> fade -> small logo.
Base b3 = car minus every removable panel (tools/build_v3.py); parts at home cover it.
Scan frame: front = -Y, car's right = -X, Z up, metres. Persistent data is off automatically (keyed parts).
"""
import json
import os
import sys

P = "/home/user/media/subaru-wrx-vb/prep"
OUT = "/home/user/media/work/wrx/renders"
SPECS = "/home/user/media/work/wrx/specs"
CAR = f"{P}/car4np.blend"
B3 = f"{P}/b3.blend"
SHELL, PLATE, GRILLE = f"{P}/p_front_bumper_inside_parts_removed.blend", f"{P}/b3_plate.blend", f"{P}/p_front_grille.blend"
GARN = f"{P}/p_front_bumper_lower_garnish.blend"
RBUMP, LID = f"{P}/p_rear_bumper_updated.blend", f"{P}/b3_lid.blend"
FFL, DFL, RFL, SKIRT = (f"{P}/p_front_flare.blend", f"{P}/p_door_flare.blend", f"{P}/p_rear_flare.blend",
                        f"{P}/p_side_skirt_only.blend")
HINGE = json.load(open("/home/user/media/subaru-wrx-vb/comp/b3_hinge.json"))
OPEN = round(HINGE["open_deg"], 2)  # the captured open-lid pose (fit median 6.7 mm)
PIV_F = [-0.006, -2.007, 0.466]
PIV_R = [0.0065, 1.952, 0.548]
PIVOT = {SHELL: PIV_F, PLATE: PIV_F, RBUMP: PIV_R, LID: HINGE["pivot"]}
BAR = 1.3672
# visible "off" poses for the start of the reassembly (rear camera), out-of-frame poses inside section shots
OFF = {SHELL: ((0, -0.55, 2.00), (0, 0, 0)), PLATE: ((0, -0.55, 2.00), (0, 0, 0)),
       GRILLE: ((0, -0.60, 2.75), (0, 0, 0)), GARN: ((0, -0.45, 1.45), (0, 0, 0)),
       FFL: ((-0.45, 0, 0.90), (0, -8, 0)), DFL: ((-0.45, 0, 0.90), (0, -8, 0)), RFL: ((-0.45, 0, 0.90), (0, -8, 0)),
       SKIRT: ((-0.60, 0, -0.12), (0, 0, 0)), RBUMP: ((0, 0.40, 1.70), (0, 0, 0))}
AWAY = {SHELL: ((0, -0.55, 6.0), (0, 0, 0)), PLATE: ((0, -0.55, 6.0), (0, 0, 0)), GRILLE: ((0, -0.60, 5.5), (0, 0, 0)),
        GARN: ((0, -0.45, 5.5), (0, 0, 0)), FFL: ((-0.40, 0, 2.0), (0, -8, 0)), DFL: ((-0.40, 0, 2.0), (0, -8, 0)),
        RFL: ((-0.40, 0, 2.0), (0, -8, 0)), SKIRT: OFF[SKIRT], RBUMP: ((0, 0.40, 2.9), (0, 0, 0))}

SHOT_START = {"v3_front": 6.152, "v3_side": 10 * BAR, "v3_rear": 14 * BAR, "v3_reassemble": 19 * BAR}
SECS = {"v3_front": round(10 * BAR - 6.152, 3), "v3_side": round(4 * BAR, 3), "v3_rear": round(5 * BAR, 3),
        "v3_reassemble": round(3 * BAR, 3)}


def K(t, loc=(0, 0, 0), rot=(0, 0, 0), ease="inout"):
    return {"t": round(t, 3), "loc": list(loc), "rot": list(rot), "ease": ease}


def C(t, loc, tgt, focal=30, ease="inout"):
    return {"t": round(t, 3), "loc": list(loc), "target": list(tgt), "focal": focal, "ease": ease}


def part(b, keys):
    d = {"blend": b, "keys": keys}
    if b in PIVOT:
        d["pivot"] = PIVOT[b]
    return d


def rt(name, reel_t):  # reel time -> shot time
    return round(reel_t - SHOT_START[name], 3)


SHOTS = {}

# FRONT: the drop (t 0) pulls the grille out toward the camera, the lower garnish follows on the next strong beat,
# the bumper shell (+ plate) on the one after: forward, flip to show its scanned inner face, rise away. The camera
# then moves low and close on the scanned structure behind (label).
n = "v3_front"
E = SECS[n] + 1
g0, ga0, s0 = 0.0, rt(n, 6 * BAR), rt(n, 7 * BAR)  # 0, 2.051, 3.418
gr_keys = [K(0), K(g0 + 0.30, (0, -0.32, 0.02), ease="out"), K(g0 + 1.10, (0, -0.70, 0.80), (-25, 0, 0)),
           K(g0 + 1.75, *AWAY[GRILLE]), K(E, *AWAY[GRILLE], ease="lin")]
ga_keys = [K(0), K(ga0), K(ga0 + 0.34, (0, -0.38, -0.03), ease="out"), K(ga0 + 1.00, (0, -0.70, 0.55)),
           K(ga0 + 1.60, *AWAY[GARN]), K(E, *AWAY[GARN], ease="lin")]
sh_keys = [K(0), K(s0), K(s0 + 0.52, (0, -0.75, 0.25), ease="out"), K(s0 + 1.37, (0, -0.85, 0.95), (-160, 0, 0)),
           K(s0 + 2.05, (0, -0.85, 1.03), (-160, 0, 0), "lin"), K(s0 + 2.70, *AWAY[SHELL]),
           K(E, *AWAY[SHELL], ease="lin")]
SHOTS[n] = {"base": [B3, RBUMP, LID, FFL, DFL, RFL, SKIRT],
            "parts": [part(GRILLE, gr_keys), part(GARN, ga_keys), part(SHELL, sh_keys), part(PLATE, sh_keys)],
            "cam": [C(0, (-2.10, -5.30, 1.20), (-0.10, -2.05, 0.60), 42),
                    C(s0 - 0.2, (-1.92, -4.95, 1.12), (-0.10, -2.05, 0.62), 42),
                    C(s0 + 1.0, (-2.10, -6.40, 1.55), (-0.05, -2.90, 1.30), 30),
                    C(s0 + 2.3, (-1.90, -6.00, 1.55), (-0.05, -2.90, 1.35), 30),
                    C(SECS[n], (-1.30, -3.80, 1.05), (-0.05, -2.00, 0.66), 28)]}

# SIDE: v2 grammar on the new bar (front flare, door flare, rear flare, skirt), ends on a wide of all four
n = "v3_side"
sc = BAR / 1.396


def lift(b, go):
    o, r = AWAY[b]
    ks = [K(0), K(go)]
    if b != SKIRT:
        ks.append(K(go + 0.342, (-0.35, 0, 0.10), r, "out"))
        ks.append(K(go + 1.025, o, r))
    else:
        ks.append(K(go + 1.025, o, r, "out"))
    return part(b, ks + [K(SECS[n] + 1, o, r, "lin")])


SHOTS[n] = {"base": [B3, RBUMP, LID],
            "parts": [lift(FFL, 0.0), lift(DFL, BAR), lift(RFL, 2 * BAR), lift(SKIRT, 3 * BAR)],
            "cam": [C(0, (-2.70, -0.30, 1.45), (-0.95, -1.30, 0.55), 30),
                    C(BAR, (-3.00, -0.90, 1.10), (-0.90, -0.60, 0.70), 30, "lin"),
                    C(2 * BAR, (-3.20, 0.40, 1.10), (-0.90, 0.40, 0.65), 30, "lin"),
                    C(3 * BAR, (-3.00, 1.60, 1.05), (-0.90, 1.25, 0.60), 30, "lin"),
                    C(SECS[n], (-7.40, 0.40, 2.20), (-0.60, 0.30, 0.90), 26)]}

# REAR: the trunk lid swings up on its fitted hinge to the captured open pose, then the rear bumper comes off
# (forward, flip to its inner face, away); the camera ends on the scanned rear structure with the lid still open.
n = "v3_rear"
rb0 = 2 * BAR
lid_keys = [K(0), K(0.25), K(1.55, (0, 0, 0), (OPEN, 0, 0)), K(SECS[n] + 1, (0, 0, 0), (OPEN, 0, 0), "lin")]
rb_keys = [K(0), K(rb0), K(rb0 + 0.52, (0, 0.70, 0.20), ease="out"), K(rb0 + 1.37, (0, 0.80, 0.90), (160, 0, 0)),
           K(rb0 + 2.05, (0, 0.80, 0.98), (160, 0, 0), "lin"), K(rb0 + 2.70, *AWAY[RBUMP]),
           K(SECS[n] + 1, *AWAY[RBUMP], ease="lin")]
SHOTS[n] = {"base": [B3],
            "parts": [part(LID, lid_keys), part(RBUMP, rb_keys)],
            "cam": [C(0, (-1.85, 5.40, 1.00), (0.0, 1.75, 0.95), 30),
                    C(rb0 - 0.1, (-1.70, 5.70, 1.05), (0.0, 1.80, 1.00), 30),
                    C(rb0 + 1.37, (-1.60, 6.70, 1.50), (0.0, 2.60, 1.30), 30),
                    C(rb0 + 2.4, (-1.45, 6.40, 1.50), (0.0, 2.60, 1.30), 30),
                    C(SECS[n], (-1.60, 4.90, 1.25), (-0.25, 2.00, 0.85), 28)]}

# REASSEMBLE: rear -> side -> front, the grille locks last on reel 21 bars (shot t 2*BAR); frames after the lock are
# re-rendered with the clean car (v3_reassemble_car) so no composite seams show
n = "v3_reassemble"


def home(b, t0, t1, ease="inout", rot0=None):
    o, r = OFF.get(b, ((0, 0, 0), (0, 0, 0)))
    if rot0 is not None:
        o, r = (0, 0, 0), rot0
    return part(b, [K(0, o, r), K(t0, o, r, "lin"), K(t1, (0, 0, 0), (0, 0, 0), ease), K(SECS[n] + 1, ease="lin")])


LOCK = round(2 * BAR, 3)
RCAM = [C(0, (-1.79, 6.32, 3.40), (0.40, 0.30, 0.90), 28, "lin"), C(SECS[n], (-2.75, 5.61, 2.60), (0.20, 0.50, 0.60), 28)]
SHOTS[n] = {"base": [B3],
            "parts": [home(LID, 0.0, 0.70, rot0=(OPEN, 0, 0)), home(RBUMP, 0.15, 0.80), home(RFL, 0.60, 1.20),
                      home(DFL, 0.75, 1.35), home(SKIRT, 0.75, 1.35), home(FFL, 0.90, 1.50),
                      home(SHELL, 1.45, 2.05), home(PLATE, 1.45, 2.05), home(GARN, 1.70, 2.30),
                      home(GRILLE, 2.05, LOCK, "in")],
            "cam": RCAM, "frame_range": [1, int(LOCK * 15)]}
SHOTS["v3_reassemble_car"] = {"base": [CAR], "parts": [], "cam": RCAM,
                              "frame_range": [int(LOCK * 15) + 1, int(round((SECS[n] + 1 / 15) * 15))],
                              "secs": SECS[n], "out": "v3_reassemble"}

PREVIEW = {"v3_front": [1, 8, 17, 31, 40, 52, 60, 70, 86, 113],
           "v3_side": [1, 12, 33, 54, 75, 82],
           "v3_rear": [1, 12, 24, 41, 52, 62, 82, 103],
           "v3_reassemble": [1, 12, 25, 33, 41], "v3_reassemble_car": [42, 62]}


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
