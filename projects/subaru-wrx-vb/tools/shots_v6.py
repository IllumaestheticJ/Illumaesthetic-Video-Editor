"""v4 shot specs -> JSON for tools/shot.py (reviewer v3 notes: the trunk was not cut correctly, the front bumper had
a ton of artifacts, remove the front bumper first and then pull the grille and other parts off).

    python projects/subaru-wrx-vb/tools/shots_v4.py preview|final [shot ...]

Music: Roni Size - The Streets, reel = track 146.799 -> ; 176.0 BPM (beat 0.34095 s). Cuts on measured broadband hits
(reel 6.152 drop, 13.633, 19.100, 25.900, 30.000).
Base b4 = car minus the mesh-smoothed front-bumper and trunk-lid regions + bumper-off / trunk-open state scans
(tools/seg_v4.py, tools/build_v4.py). Scan frame: front = -Y, car's right = -X, Z up, metres.
"""
import json
import os
import sys

P = "/home/user/media/subaru-wrx-vb/prep"
OUT = "/home/user/media/work/wrx/renders"
SPECS = "/home/user/media/work/wrx/specs"
CAR = f"{P}/car4np.blend"
B4 = f"{P}/b5.blend"
SHELL, PLATE, GRILLE = f"{P}/p_front_bumper_inside_parts_removed.blend", f"{P}/b5_plate.blend", f"{P}/p_front_grille.blend"
GARN = f"{P}/p_front_bumper_lower_garnish.blend"
RBUMP, LID = f"{P}/b5_rbump.blend", f"{P}/b5_lid.blend"
FFL, DFL, RFL, SKIRT = (f"{P}/p_front_flare.blend", f"{P}/p_door_flare.blend", f"{P}/p_rear_flare.blend",
                        f"{P}/p_side_skirt_only.blend")
RB6, REFL = f"{P}/b6_rbump.blend", f"{P}/b6_refl.blend"  # v6: bumper with the reflector pocket, reflector part
HINGE = json.load(open("/home/user/media/subaru-wrx-vb/comp/b3_hinge.json"))
OPEN = round(HINGE["open_deg"], 2)  # the captured open-lid pose (fit median 6.7 mm)
PIV_F = [-0.006, -2.007, 0.466]
PIV_R = [0.0065, 1.952, 0.548]
PIVOT = {SHELL: PIV_F, PLATE: PIV_F, RBUMP: PIV_R, RB6: PIV_R, LID: HINGE["pivot"]}
BAR = 1.3672
# visible "off" poses for the start of the reassembly (rear camera), out-of-frame poses inside section shots
OFF = {SHELL: ((0, -0.55, 2.00), (0, 0, 0)), PLATE: ((0, -0.55, 2.00), (0, 0, 0)),
       GRILLE: ((0, -0.60, 2.75), (0, 0, 0)), GARN: ((0, -0.45, 1.45), (0, 0, 0)),
       FFL: ((-0.45, 0, 0.90), (0, -8, 0)), DFL: ((-0.45, 0, 0.90), (0, -8, 0)), RFL: ((-0.45, 0, 0.90), (0, -8, 0)),
       SKIRT: ((-0.60, 0, -0.12), (0, 0, 0)), RBUMP: ((0, 0.40, 1.70), (0, 0, 0))}
OFF[RB6] = OFF[REFL] = OFF[RBUMP]
AWAY = {SHELL: ((0, -0.55, 6.0), (0, 0, 0)), PLATE: ((0, -0.55, 6.0), (0, 0, 0)), GRILLE: ((0, -0.60, 5.5), (0, 0, 0)),
        GARN: ((0, -0.45, 5.5), (0, 0, 0)), FFL: ((-0.40, 0, 2.0), (0, -8, 0)), DFL: ((-0.40, 0, 2.0), (0, -8, 0)),
        RFL: ((-0.40, 0, 2.0), (0, -8, 0)), SKIRT: OFF[SKIRT], RBUMP: ((0, 0.40, 2.9), (0, 0, 0))}

SHOT_START = {"v6_front": 6.152, "v6_side": 13.633, "v6_rear": 19.100, "v6_reassemble": 25.900}
SECS = {"v6_front": 7.481, "v6_side": 5.467, "v6_rear": 6.800, "v6_reassemble": 4.100}


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

# FRONT: on the drop the whole bumper assembly (shell + grille + lower garnish + plate) comes straight off the car and
# hangs in front of it (label). Then it comes apart: the grille pulls forward and up (label), the lower garnish forward
# and down (label), the shell rises and flips to show its scanned inner face. The parts leave upward while the camera
# pushes in low on the scanned structure behind.
n = "v6_front"
E = SECS[n] + 1
OUTP = (0, -0.95, 0.15)  # the assembly's hang pose
g0, ga0, s0, aw = 2.05, 3.42, 4.78, 6.00


def off_assembly(extra):
    ks = [K(0), K(0.55, (0, -0.55, 0.05), ease="out"), K(1.30, OUTP)]
    return ks + extra


add = lambda d: tuple(OUTP[i] + d[i] for i in range(3))
gr_keys = off_assembly([K(g0, OUTP, ease="lin"), K(g0 + 0.50, add((0, -0.45, 0.35)), ease="out"),
                        K(aw, add((0, -0.50, 0.38)), ease="lin"), K(aw + 0.75, add((0, -0.50, 5.4))),
                        K(E, add((0, -0.50, 5.4)), ease="lin")])
ga_keys = off_assembly([K(ga0, OUTP, ease="lin"), K(ga0 + 0.50, add((0, -0.40, -0.10)), ease="out"),
                        K(aw + 0.1, add((0, -0.43, -0.10)), ease="lin"), K(aw + 0.85, add((0, -0.43, 5.4))),
                        K(E, add((0, -0.43, 5.4)), ease="lin")])
sh_keys = off_assembly([K(s0, OUTP, ease="lin"), K(s0 + 0.85, add((0, 0, 0.85)), (-160, 0, 0)),
                        K(aw - 0.1, add((0, 0, 0.90)), (-160, 0, 0), "lin"), K(aw + 0.7, add((0, 0, 5.8)), (-160, 0, 0)),
                        K(E, add((0, 0, 5.8)), (-160, 0, 0), "lin")])
SHOTS[n] = {"base": [B4, RBUMP, LID, FFL, DFL, RFL, SKIRT],
            "parts": [part(GRILLE, gr_keys), part(GARN, ga_keys), part(SHELL, sh_keys), part(PLATE, sh_keys)],
            "cam": [C(0, (-2.10, -5.30, 1.20), (-0.10, -2.05, 0.60), 42),
                    C(1.10, (-4.60, -5.70, 1.60), (-0.10, -3.10, 0.62), 26),
                    C(s0, (-4.85, -6.20, 1.70), (-0.05, -3.20, 0.75), 26, "lin"),
                    C(aw, (-4.50, -6.45, 1.90), (-0.05, -3.15, 0.95), 26),
                    C(SECS[n], (-1.30, -3.80, 1.05), (-0.05, -2.00, 0.66), 28)]}

# SIDE: v2 grammar on the new bar (front flare, door flare, rear flare, skirt), ends on a wide of all four
n = "v6_side"
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


SHOTS[n] = {"base": [B4, RBUMP, LID],
            "parts": [lift(FFL, 0.0), lift(DFL, BAR), lift(RFL, 2 * BAR), lift(SKIRT, 3 * BAR)],
            # v5b (reviewer: "it says door flare but you can't see anything come off"): the door flare is the rear
            # door's part of the REAR arch (y 0.87..1.26), so the camera must be on the rear arch at BAR, not the door
            "cam": [C(0, (-2.70, -0.30, 1.45), (-0.95, -1.30, 0.55), 30),
                    C(0.50, (-2.75, -0.20, 1.40), (-0.95, -1.20, 0.58), 30, "lin"),
                    C(BAR, (-3.00, 0.45, 1.10), (-0.90, 1.02, 0.60), 30),
                    C(2 * BAR, (-3.20, 1.45, 1.10), (-0.90, 1.32, 0.62), 30, "lin"),
                    C(3 * BAR, (-3.40, 0.35, 1.05), (-0.90, 0.20, 0.50), 30, "lin"),
                    C(SECS[n], (-7.40, 0.40, 2.20), (-0.60, 0.30, 0.90), 26)]}

# REAR: the trunk lid swings up on its fitted hinge to the captured open pose, then the rear bumper comes off
# (forward, flip to its inner face, away); the camera ends on the scanned rear structure with the lid still open.
n = "v6_rear"
rb0 = 2 * BAR
lid_keys = [K(0), K(0.25), K(1.55, (0, 0, 0), (OPEN, 0, 0)), K(SECS[n] + 1, (0, 0, 0), (OPEN, 0, 0), "lin")]
# v6 (reviewer: "we did the fog lights and reflectors"): the bumper comes off and hangs, the reflector (own scan,
# registered by its two clips to the clip holes of the 'reflector removed' corner scan) pulls out of its pocket along
# the lens normal (label), then the bumper flips to its inner face and both leave.
rb_keys = [K(0), K(rb0), K(rb0 + 0.52, (0, 0.70, 0.20), ease="out"), K(rb0 + 1.55, (0, 0.72, 0.22), ease="lin"),
           K(rb0 + 2.35, (0, 0.80, 0.90), (160, 0, 0)), K(rb0 + 2.75, (0, 0.80, 0.98), (160, 0, 0), "lin"),
           K(rb0 + 3.35, *AWAY[RBUMP]), K(SECS[n] + 1, *AWAY[RBUMP], ease="lin")]
rf_keys = [K(0), K(rb0), K(rb0 + 0.52, (0, 0.70, 0.20), ease="out"), K(rb0 + 0.80, (0, 0.705, 0.205), ease="lin"),
           K(rb0 + 1.25, (-0.10, 0.92, 0.36), ease="out"), K(rb0 + 2.75, (-0.11, 0.96, 0.39), ease="lin"),
           K(rb0 + 3.35, (-0.11, 0.96, 2.9)), K(SECS[n] + 1, (-0.11, 0.96, 2.9), ease="lin")]
SHOTS[n] = {"base": [B4],
            "parts": [part(LID, lid_keys), part(RB6, rb_keys), part(REFL, rf_keys)],
            "cam": [C(0, (-1.85, 5.40, 1.00), (0.0, 1.75, 0.95), 30),
                    C(rb0 - 0.1, (-1.70, 5.70, 1.05), (0.0, 1.80, 1.00), 30),
                    C(rb0 + 0.85, (-1.12, 3.72, 0.98), (-0.68, 2.95, 0.78), 34),
                    C(rb0 + 1.65, (-1.16, 3.80, 1.02), (-0.70, 2.98, 0.84), 34, "lin"),
                    C(rb0 + 2.45, (-1.60, 6.70, 1.50), (0.0, 2.60, 1.30), 30),
                    C(rb0 + 3.0, (-1.45, 6.40, 1.50), (0.0, 2.60, 1.30), 30, "lin"),
                    C(SECS[n], (-1.60, 4.90, 1.25), (-0.25, 2.00, 0.85), 28)]}

# REASSEMBLE: rear -> side -> front, the grille locks last on reel 21 bars (shot t 2*BAR); frames after the lock are
# re-rendered with the clean car (v6_reassemble_car) so no composite seams show
n = "v6_reassemble"


def home(b, t0, t1, ease="inout", rot0=None):
    o, r = OFF.get(b, ((0, 0, 0), (0, 0, 0)))
    if rot0 is not None:
        o, r = (0, 0, 0), rot0
    return part(b, [K(0, o, r), K(t0, o, r, "lin"), K(t1, (0, 0, 0), (0, 0, 0), ease), K(SECS[n] + 1, ease="lin")])


LOCK = round(2 * BAR, 3)


def join(b, t0, t1):
    """front parts: from their stacked OFF pose onto the shell's OFF pose (t0..t1), then the whole bumper assembly
    goes home together and locks on LOCK"""
    o, r = OFF[b]
    so = OFF[SHELL][0]
    pre = [K(0, o, r), K(t0, o, r, "lin"), K(t1, so)] if t1 > 0 else [K(0, so)]
    return part(b, pre + [K(1.95, so, ease="lin"), K(LOCK, ease="in"), K(SECS[n] + 1, ease="lin")])
# v5: the reassembly ends on the listing 360-viewer's camera (tools/solve_listing.py -> cta/listing_cam.json: orbit az 55.5,
# el 14.4, d 10.98 m about (0,0,0.73), 42.05 mm on the 20.25 sensor, IoU 0.983) so the last frame shrinks 1:1 onto the
# car on the mobile listing (tools/cta_card.py). The viewer's -1.83 deg roll is applied in the CTA, not here.
LCAM = ((8.7624, -6.0321, 3.4607), (0.0, 0.0, 0.7295), 42.05)
RCAM = [C(0, (-1.79, 6.32, 3.40), (0.40, 0.30, 0.90), 28, "lin"),
        C(1.35, (7.20, 5.80, 3.60), (0.15, -0.30, 1.30), 29, "lin"),
        C(LOCK, (9.80, -2.60, 3.50), (0.0, 0.0, 0.75), 39, "lin"),
        C(SECS[n], *LCAM)]
SHOTS[n] = {"base": [B4],
            "parts": [home(LID, 0.0, 0.70, rot0=(OPEN, 0, 0)), home(RB6, 0.15, 0.80), home(REFL, 0.15, 0.80), home(RFL, 0.60, 1.20),
                      home(DFL, 0.75, 1.35), home(SKIRT, 0.75, 1.35), home(FFL, 0.90, 1.50),
                      join(GRILLE, 1.05, 1.75), join(GARN, 1.15, 1.75), join(SHELL, 0, 0), join(PLATE, 0, 0)],
            "cam": RCAM, "frame_range": [1, int(LOCK * 15)]}
SHOTS["v6_reassemble_car"] = {"base": [CAR], "parts": [], "cam": RCAM,
                              "frame_range": [int(LOCK * 15) + 1, int(round((SECS[n] + 1 / 15) * 15))],
                              "secs": SECS[n], "out": "v6_reassemble"}

PREVIEW = {"v6_front": [9, 20, 34, 45, 62, 84, 96, 104],
           "v6_side": [1, 6, 12, 21, 24, 27, 31, 41, 45, 50, 62, 66, 82],
           "v6_rear": [1, 41, 50, 54, 57, 60, 64, 70, 78, 90, 103],
           "v6_reassemble": [1, 12, 25, 33, 41], "v6_reassemble_car": [42, 62]}


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
