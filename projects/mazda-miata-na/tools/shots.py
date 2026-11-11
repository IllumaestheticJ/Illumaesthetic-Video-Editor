"""Shot specs for the Mazda Miata NA Temerario-style reel -> JSON for projects/ferrari-296/tools/shot.py.

    python projects/mazda-miata-na/tools/shots.py preview|final [shot ...]   # writes specs, prints paths

Scan frame (prepped, metres; see editlog): nose at -Y, car's right = -X, ground Z=0, centre x ~ 0.
Bumper tip y=-1.97, tail y=+1.97, width 1.79 m incl. mirrors, height 1.24 m (hardtop).
Durations (SECS) come from the music's accent grid (project.yaml); all moves start on frame 1.
"""
import json
import math
import os
import sys

P = "/home/user/media/mazda-miata-na/prep"
OUT = "/home/user/media/work/miata/renders"
SPECS = "/home/user/media/work/miata/specs"
TIMING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "timing.json")
TIM = json.load(open(TIMING)) if os.path.exists(TIMING) else {}
SECS = dict(TIM.get("secs", {}), **{k: v for k, v in TIM.items() if k.startswith("x_")})
BEAT = json.load(open(TIMING))["beat"] if os.path.exists(TIMING) else 0.6

CAR = f"{P}/car4.blend"      # 4 mm: full-car moves
FR2 = f"{P}/fr2.blend"       # 2 mm front-right quarter: wheel close-up
REAR2 = f"{P}/rear2.blend"   # 2 mm rear half: tail-lamp close-up
HH = json.load(open("/home/user/media/mazda-miata-na/reg/hinge_hood.json"))    # tools/hinge.py
HT = json.load(open("/home/user/media/mazda-miata-na/reg/hinge_trunk.json"))


def orbit(t, r, ang_deg, h, c=(0, 0, 0.5), focal=30, ease="inout", tz=None):
    """angle 0 = camera in front of the car (-Y); -90 = car's right (-X); +90 = car's left; 180 = behind."""
    a = math.radians(ang_deg)
    return {"t": t, "loc": [c[0] + r * math.sin(a), c[1] - r * math.cos(a), h],
            "target": [c[0], c[1], tz if tz is not None else c[2]], "focal": focal, "ease": ease}


def S(n, default):
    return SECS.get(n, default)


# ---- v2 (reviewer: same first-revision fixes as the siblings) -------------------------------------------------
# Order by area, no rotating camera moves: whole car (not cropped) -> FRONT: bumper comes off (only part that was
# physically removed and scanned on its own), turns once to show its scanned inside -> hood opens on its hinge over the
# real bumper-off front end -> close slide across that exposed front data -> REAR on the drop: trunk closed -> half ->
# open -> into the trunk well -> top-down: everything returns home -> dip to black -> small logo.
# Every camera move is a straight push / dolly / crane; parts translate (bumper turns once: its inside is scanned).
BASE = f"{P}/comp_explode.blend"   # car - bumper - hood - lid + 'Front End Bumper Off' + 'NA Trunk Open'
B_OUT = [0, -0.55, 0.75]           # bumper parked up and forward, in clear background above the nose line
B_ROT = [135, 0, 0]                # inside (mounting side) turned toward a front camera


def cam(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": list(loc), "target": list(tgt), "focal": focal, "ease": ease}


def still(loc=(0, 0, 0), rot=(0, 0, 0)):
    return [{"t": 0, "loc": list(loc), "rot": list(rot)}]


def bumper(state):
    return {"blend": f"{P}/fbumper_c.blend", "keys": state}


def hood(state):
    return {"blend": f"{P}/hood_full.blend", "pivot": HH["p"], "keys": state}


def lid(state):
    return {"blend": f"{P}/trunk_full.blend", "pivot": HT["p"], "keys": state}


B_AWAY = [0, -1.45, 0.0]           # s3-s6: bumper set aside (not loaded; it was shown in s2); s7 slides it home from here
H_OPEN = still(rot=(HH["open_deg"], 0, 0))
L_OPEN = still(rot=(HT["open_deg"], 0, 0))


def shots():
    sh = {}
    # 1. whole car, front-right 3/4, fully in frame with margin (v1 was cropped); straight push toward the front end
    d = S("s1_reveal", 5.07)
    sh["s1_reveal"] = {"base": [CAR], "cam": [cam(0, (-3.9, -5.9, 1.35), (0, -0.35, 0.5), ease="lin"),
                                               cam(d, (-2.9, -4.9, 1.15), (0, -0.9, 0.5), ease="out2")]}
    # 2. FRONT: bumper slides up/forward out of the car into clear background, then turns once to show its scanned inside
    d = S("s2_bumper", 4.43)
    sh["s2_bumper"] = {"base": [BASE], "parts": [
        bumper([{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
                {"t": 3.5 * BEAT, "loc": B_OUT, "rot": [0, 0, 0], "ease": "inout"},
                {"t": 4.0 * BEAT, "loc": B_OUT, "rot": [0, 0, 0], "ease": "lin"},
                {"t": 7.0 * BEAT, "loc": B_OUT, "rot": B_ROT, "ease": "inout"}]),
        hood(still()), lid(still())],
        "cam": [cam(0, (-2.05, -4.7, 0.95), (0, -1.75, 0.75), ease="lin"),
                cam(d, (-1.95, -4.6, 1.0), (0.15, -2.0, 0.92), ease="out2")]}
    # 3. FRONT: hood opens on its fitted cowl hinge over the real bumper-off front end (bumper stays parked)
    d = S("s3_hood", 4.43)
    sh["s3_hood"] = {"base": [BASE], "parts": [
        lid(still()),
        hood([{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": 0.5 * BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
              {"t": 3.5 * BEAT, "loc": [0, 0, 0], "rot": [HH["open_deg"], 0, 0], "ease": "inout"}])],
        "cam": [cam(0, (-2.6, -3.9, 2.3), (0, -1.45, 0.6), ease="lin"),
                cam(d, (-2.2, -3.4, 2.15), (0, -1.5, 0.55), ease="out2")]}
    # 4. FRONT detail: slow dolly along the car's right side, close, over the exposed front structure + engine bay
    d = S("s4_front_detail", 4.43)
    sh["s4_front_detail"] = {"base": [BASE], "parts": [hood(H_OPEN), lid(still())],
                             "cam": [cam(0, (-1.75, -1.0, 1.45), (-0.2, -1.55, 0.55), focal=32, ease="lin"),
                                     cam(d, (-1.55, -2.35, 1.3), (-0.1, -1.75, 0.5), focal=32, ease="out2")]}
    # 5. REAR, on the drop: trunk closed -> half open (37.5 deg capture) -> pause -> open (55.6 deg capture)
    d = S("s5_trunk", 4.47)
    sh["s5_trunk"] = {"base": [BASE], "parts": [
        hood(H_OPEN),
        lid([{"t": 0, "loc": [0, 0, 0], "rot": [0, 0, 0]}, {"t": 0.5 * BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0]},
             {"t": 2.0 * BEAT, "loc": [0, 0, 0], "rot": [HT["half_deg"], 0, 0], "ease": "inout"},
             {"t": 3.5 * BEAT, "loc": [0, 0, 0], "rot": [HT["half_deg"], 0, 0], "ease": "lin"},
             {"t": 5.0 * BEAT, "loc": [0, 0, 0], "rot": [HT["open_deg"], 0, 0], "ease": "inout"}])],
        "cam": [cam(0, (2.3, 4.6, 1.55), (0, 1.35, 0.65), ease="lin"),
                cam(d, (1.95, 4.0, 1.6), (0, 1.3, 0.65), ease="out2")]}
    # 6. REAR detail: crane up behind the open trunk and look down into the scanned trunk well + lid underside
    d = S("s6_trunk_well", 4.43)
    sh["s6_trunk_well"] = {"base": [BASE], "parts": [hood(H_OPEN), lid(L_OPEN)],
                           "cam": [cam(0, (0.55, 3.1, 1.5), (0, 1.3, 0.6), focal=30, ease="lin"),
                                   cam(d, (0.25, 2.75, 2.05), (0, 1.25, 0.5), focal=30, ease="out2")]}
    # 7. top-down (front at the top), slow push: everything goes home and locks on b52, then holds
    d = S("s7_top_home", 4.43)
    home = lambda frm: [{"t": 0, **frm}, {"t": BEAT, **frm}, {"t": 4 * BEAT, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "inout"}]
    sh["s7_top_home"] = {"base": [BASE], "parts": [
        bumper(home({"loc": B_AWAY, "rot": [0, 0, 0]})), hood(home({"loc": [0, 0, 0], "rot": [HH["open_deg"], 0, 0]})),
        lid(home({"loc": [0, 0, 0], "rot": [HT["open_deg"], 0, 0]}))],
        "cam": [cam(0, (0, -0.45, 6.3), (0, -0.5, 0.4), ease="lin"), cam(d, (0, -0.15, 5.6), (0, -0.2, 0.4), ease="out2")]}
    return sh


def spec(name, mode, frames=None):
    s = shots()[name]
    final = mode == "final"
    secs = s.get("secs", S(name, 2.4))
    sp = {"base": s["base"], "parts": s.get("parts", []),
          "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": secs + 1 / 15, "fps": 15, "res": "1080x1920",
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
    for n in sys.argv[2:] or list(shots()):
        print(spec(n, mode, ["first", "mid", "last"] if mode == "preview" else None))
