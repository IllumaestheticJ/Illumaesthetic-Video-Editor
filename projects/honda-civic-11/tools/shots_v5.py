"""v5 reshoot (director_v5.md): S1_open (rolled near-top, doors + trunk open and shut) and L_build (ONE continuous take around
the car's left: lip -> skirts -> apron -> wheels -> wing -> the camera of Ron's render 7).

    python projects/honda-civic-11/tools/shots_v5.py preview|final|inb [S1_open|L_build] [leg ...]

Parts: prep/kit2 (Ron's design scene, kit_parts2.py). Hidden parts are parked at z -30 and jump in between two frames, in
black, 0.62 s before they seat. Times are shot-local seconds; seats land on the hits listed in director_v5.md.
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import CLOSED, HINGE  # noqa: E402

P = "/home/user/media/honda-civic-11/prep"
K = f"{P}/kit2"
OUT = "/home/user/media/work/civic/renders"
SPECS = "/home/user/media/work/civic/specs"
Z3 = [0, 0, 0]
HID = [0, 0, -30]
CX = 0.09                       # the scan's centreline in the prepped frame
HG = json.load(open("/home/user/media/honda-civic-11/doors/hinges.json"))
R7 = json.load(open("/home/user/media/work/civic/match/ron7_cam.json"))["key"]
SECS = {"S1_open": 5.19 + 0.14, "L_build": 15.945 + 0.14}


def part(blend, mat=None, keys=None, pivot=None):
    d = {"blend": blend}
    for k, v in (("mat", mat), ("keys", keys), ("pivot", pivot)):
        if v:
            d[k] = v
    return d


def pop(start, t_pop, t_seat, secs):
    """hidden -> appears at `start` (offset from home) at t_pop -> seated (ease out) at t_seat -> stays."""
    k = [] if t_pop <= 0 else [dict(t=0, loc=HID, rot=Z3), dict(t=t_pop - 0.002, loc=HID, rot=Z3)]
    return k + [dict(t=max(t_pop, 0), loc=start, rot=Z3, ease="lin"), dict(t=t_seat, loc=Z3, rot=Z3, ease="out"), dict(t=secs, loc=Z3, rot=Z3)]


def az(t, tgt, d, a, h=None, elev=None, focal=35, ease="inout"):
    """a: 0 = in front (+Y), +90 = the car's left (-X), 180 = behind."""
    r = math.radians(a)
    if elev is not None:
        e = math.radians(elev); loc = [tgt[0] - d * math.cos(e) * math.sin(r), tgt[1] + d * math.cos(e) * math.cos(r), tgt[2] + d * math.sin(e)]
    else:
        loc = [tgt[0] - d * math.sin(r), tgt[1] + d * math.cos(r), h]
    return {"t": t, "loc": loc, "target": list(tgt), "focal": focal, "ease": ease}


def key(t, loc, tgt, focal=35, ease="inout"):
    return {"t": t, "loc": list(loc), "target": list(tgt), "focal": focal, "ease": ease}


# ---------------------------------------------------------------- S1: open-up from a rolled near-top view
DIR = np.array([0.343, -0.152, 0.927]); DIR /= np.linalg.norm(DIR)   # target -> camera: edge-on to the open doors


def top(t, tgt, d, extra_roll=0.0, ease="inout"):
    tgt = np.array(tgt, float); loc = tgt + d * DIR; fwd = -DIR
    r0 = np.cross(fwd, [0, 0, 1.0]); r0 /= np.linalg.norm(r0); u0 = np.cross(r0, fwd)
    want = np.array([0, 1.0, 0]); want = want - (want @ fwd) * fwd; want /= np.linalg.norm(want)    # nose up the frame
    roll = math.degrees(math.atan2(-want @ r0, want @ u0)) + extra_roll
    return {"t": t, "loc": loc.tolist(), "target": tgt.tolist(), "focal": 35, "roll": roll, "ease": ease}


S1 = SECS["S1_open"]
FD = dict(blend=f"{P}/front_door.blend", pivot=HG["front_door"]["pivot"] + [0.8])
RD = dict(blend=f"{P}/rear_door.blend", pivot=HG["rear_door"]["pivot"] + [0.8])
FDO, RDO = [0, 0, HG["front_door"]["deg"]], [0, 0, HG["rear_door"]["deg"]]
OPEN = {"loc": Z3, "rot": Z3}
SHOTS = {"S1_open": {
    "base": [f"{P}/explode_base_ns.blend"],
    "parts": [dict(FD, keys=[dict(t=0, loc=Z3, rot=Z3), dict(t=1.269, loc=Z3, rot=Z3), dict(t=1.89, loc=Z3, rot=FDO, ease="out"),
                             dict(t=4.574, loc=Z3, rot=FDO), dict(t=5.16, loc=Z3, rot=Z3, ease="in"), dict(t=S1, loc=Z3, rot=Z3)]),
              dict(RD, keys=[dict(t=0, loc=Z3, rot=Z3), dict(t=1.89, loc=Z3, rot=Z3), dict(t=2.516, loc=Z3, rot=RDO, ease="out"),
                             dict(t=4.574, loc=Z3, rot=RDO), dict(t=5.09, loc=Z3, rot=Z3, ease="in"), dict(t=S1, loc=Z3, rot=Z3)]),
              dict(blend=f"{P}/lid.blend", pivot=HINGE["pivot_prepped"],
                   keys=[dict(t=0, **CLOSED), dict(t=2.52, **CLOSED), dict(t=3.332, ease="out", **OPEN), dict(t=4.574, **OPEN),
                         dict(t=5.16, ease="in", **CLOSED), dict(t=S1, **CLOSED)])],
    "cam": [top(0, (0.45, 0.05, 0.6), 7.3, 8.0, "lin"), top(1.269, (0.45, 0.05, 0.6), 6.4, 0, "out"), top(3.332, (0.45, 0.05, 0.6), 6.3, 0, "lin"),
            top(4.574, (0.5, -0.15, 0.55), 6.1, 0, "inout"), top(5.19, (0.4, 0.25, 0.55), 6.1, 0, "in"), top(S1, (0.38, 0.33, 0.55), 6.1, 0, "lin")],   # v5 preview: d 5.7 + drift cut the tail off
    "motion": [(1.2, 3.4), (4.5, S1)], "exposure": -0.9}}   # top lights hit the roof square-on: 26 % of the car > 235 at 0

# ---------------------------------------------------------------- L_build: one take
L = SECS["L_build"]
T_OFF, T_NEW, T_SEATW = 7.884, 8.69, 9.305
parts = [part(f"{K}/front_lip.blend", "kit", pop([0, 0.50, -0.12], 0, 0.635, L)),
         part(f"{K}/skirt_L.blend", "kit", pop([-0.40, 0, -0.06], 2.09, 2.707, L)),
         part(f"{K}/skirt_R.blend", "kit", pop([0.40, 0, -0.06], 2.09, 2.707, L)),
         part(f"{K}/rear_apron.blend", "kit", pop([0, -0.50, -0.12], 5.39, 6.011, L)),
         part(f"{K}/wing.blend", "kit", pop([0, -0.10, 0.65], 12.0, 12.631, L))]
for w in ("FL", "FR", "RL", "RR"):
    sx = -1 if w[1] == "L" else 1
    parts.append(part(f"{K}/scanwheel_{w}.blend", None, [dict(t=0, loc=Z3, rot=Z3), dict(t=T_OFF, loc=Z3, rot=Z3),
                                                         dict(t=T_OFF + 0.5, loc=[0.9 * sx, 0, 0], rot=Z3, ease="in"),
                                                         dict(t=T_OFF + 0.502, loc=HID, rot=Z3, ease="lin"), dict(t=L, loc=HID, rot=Z3)]))
    for n, m in (("rim", "gold"), ("tyre", "rubber"), ("brake", None)):
        parts.append(part(f"{K}/{n}_{w}.blend", m, pop([0.9 * sx, 0, 0], T_NEW, T_SEATW, L)))
e9 = az(7.884, (-0.25, -0.1, 0.6), 9.6, 140, elev=35)
k12_loc, k12_tgt = np.array([-2.0, -2.4, 0.70]), np.array([-0.93, -1.31, 0.36])
v = k12_loc - k12_tgt; a5 = math.radians(5); k13_loc = k12_tgt + np.array([v[0] * math.cos(a5) - v[1] * math.sin(a5), v[0] * math.sin(a5) + v[1] * math.cos(a5), v[2]])
SHOTS["L_build"] = {
    "base": [f"{K}/car_nowheels.blend"], "parts": parts,
    "cam": [az(0, (CX, 2.25, 0.45), 4.3, 10, h=0.50, ease="lin"), az(0.635, (CX, 2.25, 0.42), 3.8, 12, h=0.45, ease="out"),
            az(1.459, (CX, 2.25, 0.42), 3.65, 12, h=0.45, ease="lin"),
            key(2.05, (-1.9, 3.3, 0.30), (-0.75, 2.25, 0.22)),
            key(2.707, (-2.1, 3.0, 0.32), (-0.98, 0.0, 0.30)), key(3.943, (-2.1, 2.7, 0.34), (-0.98, -0.3, 0.30), ease="lin"),
            key(5.0, (-2.3, -2.6, 0.45), (-0.8, -1.6, 0.40)),
            az(6.011, (CX, -2.15, 0.45), 3.7, 168, h=0.45, ease="out"), az(6.632, (CX, -2.15, 0.45), 3.5, 168, h=0.45, ease="lin"),
            e9, az(9.305, (-0.25, -0.1, 0.6), 9.2, 140, elev=35, ease="lin"), az(9.955, (-0.25, -0.1, 0.6), 9.0, 140, elev=35, ease="lin"),
            key(10.567, k12_loc, k12_tgt), key(11.396, k13_loc, k12_tgt, ease="lin"),
            az(12.631, (CX, -1.95, 1.15), 3.4, 155, h=2.2), az(13.238, (CX, -1.95, 1.15), 3.3, 155, h=2.2, ease="lin"),
            key(13.872, (-1.9, -2.9, 1.35), (-0.6, -2.0, 1.12)),
            dict(R7, t=15.55, ease="out"), dict(R7, t=L, ease="lin")],
    # creep holds (camera only, slow): blended in-betweens are fine there
    "holds": [(0.70, 1.40), (2.78, 3.90), (6.08, 6.60), (9.37, 9.90), (10.63, 11.35), (12.70, 13.20), (15.60, L)],
    "legs": {"1": (0, 2.05), "2": (2.05, 5.0), "3": (5.0, 7.884), "4": (7.884, 11.396), "5": (11.396, 13.872), "6": (13.872, L)}}
for k in SHOTS["L_build"]["cam"]:
    k.setdefault("roll", 0.0)


def spec(name, mode, legs=None):
    s = SHOTS[name]; secs = SECS[name]; n15 = int(round(secs * 15))
    out = {"base": s["base"], "parts": s["parts"], "camera": {"keys": s["cam"], "sensor": 20.25}, "seconds": secs,
           "fps": 15, "res": "1080x1920", "persist": False, "exposure": s.get("exposure", 0.0)}
    rng = (0, secs)
    if legs:
        rng = (min(s["legs"][l][0] for l in legs), max(s["legs"][l][1] for l in legs))
    tag = name + ("_legs" + "".join(legs) if legs else "")
    if mode == "preview":
        ts = sorted({k["t"] for k in s["cam"]} | {(a + b) / 2 for a, b in zip([k["t"] for k in s["cam"]][:-1], [k["t"] for k in s["cam"]][1:])})
        out.update(res_pct=25, samples=6, out=f"{OUT}/preview5/{name}",
                   frames=sorted({min(n15, int(t * 15) + 1) for t in ts if rng[0] <= t <= rng[1]}))
    elif mode == "final":
        out.update(res_pct=75, samples=12, out=f"{OUT}/final5/{name}",
                   frames=[f for f in range(1, n15 + 1) if rng[0] - 0.07 <= (f - 1) / 15 <= rng[1] + 0.07])
    else:
        if "holds" in s:
            mov = lambda t: not any(a <= t <= b for a, b in s["holds"])
        else:
            mov = lambda t: any(a <= t <= b for a, b in s["motion"])
        out.update(res_pct=75, samples=12, fps=30, out=f"{OUT}/final5/{name}_30",
                   frames=[j for j in range(2, 2 * n15, 2) if mov((j - 1) / 30) and rng[0] <= (j - 1) / 30 <= rng[1]])
    p = f"{SPECS}/{tag}_v5{mode}.json"
    json.dump(out, open(p, "w"), indent=1)
    return p, len(out["frames"])


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in ([sys.argv[2]] if len(sys.argv) > 2 else list(SHOTS)):
        print(spec(n, mode, sys.argv[3:] or None))
