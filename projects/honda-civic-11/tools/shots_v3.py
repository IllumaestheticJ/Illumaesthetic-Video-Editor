"""v3 shot specs: user feedback on v2 = "You hallucinated the doors coming off... they should just open. Same with rear trunk."

    python projects/honda-civic-11/tools/shots_v3.py preview|final [shot ...]

Parts only move the way the state scans show them: the right doors swing on vertical hinges to the angle measured in
the Door Open scan (its open-door inner strips, tools output doors/hinges.json: front 68 deg, rear 64 deg), the trunk lid
opens on its fitted hinge (Trunk Open scan) and STAYS on the car. Nothing detaches. The ending closes them (lock k80).
Cameras stay on the outer-skin side of the open doors (their inner faces have no scan data).
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import BEAT, CLOSED, K, OUT, P, SPECS, orbit  # noqa: E402
from shots_v2 import CAR, LID, OPEN, SECS, Z3  # noqa: E402

HG = json.load(open("/home/user/media/honda-civic-11/doors/hinges.json"))
FD = {"blend": f"{P}/front_door.blend", "pivot": HG["front_door"]["pivot"] + [0.8]}
RD = {"blend": f"{P}/rear_door.blend", "pivot": HG["rear_door"]["pivot"] + [0.8]}
FD_OPEN = {"loc": Z3, "rot": [0, 0, HG["front_door"]["deg"]]}
RD_OPEN = {"loc": Z3, "rot": [0, 0, HG["rear_door"]["deg"]]}
SHUT = {"loc": Z3, "rot": Z3}


def side(t, r, az, h, tgt, ease="inout"):
    """az: 0 = straight at the car's right side, + = toward the front."""
    a = math.radians(az)
    return {"t": t, "loc": [tgt[0] + r * math.cos(a), tgt[1] + r * math.sin(a), h], "target": list(tgt), "focal": 30,
            "ease": ease}


S2, S3, S4 = SECS["N2_doors"], SECS["N3_trunk"], SECS["N4_reassemble"]
SHOTS = {
    "N2_doors": {"base": [f"{P}/doors_base_ns.blend"],
                 "parts": [dict(FD, keys=[dict(t=0, **SHUT), dict(t=2 * BEAT, ease="out", **FD_OPEN), dict(t=S2, **FD_OPEN)]),
                           dict(RD, keys=[dict(t=0, **SHUT), dict(t=3 * BEAT, **SHUT), dict(t=5 * BEAT, ease="out", **RD_OPEN),
                                          dict(t=S2, **RD_OPEN)])],
                 "cam": [side(0, 4.3, 32, 1.35, (0.95, 0.1, 0.9)), side(S2 - 0.2, 4.6, 4, 1.5, (1.0, -0.05, 0.85))]},
    # frames 1-63 (to 10 beats) are identical to v2 (lid opens k44-k49); after that the lid stays open, camera dives in
    "N3_trunk": {"base": [f"{P}/trunk_base_ns.blend"],
                 "parts": [dict(LID, keys=[dict(t=0, **CLOSED), dict(t=2 * BEAT, **CLOSED),
                                           dict(t=7 * BEAT, ease="inout", **OPEN), dict(t=S3, **OPEN)])],
                 "cam": [{"t": 0, "loc": [-0.5, -5.4, 1.6], "target": [0, -1.9, 1.15], "focal": 35},
                         {"t": 10 * BEAT, "loc": [-0.4, -4.9, 1.9], "target": [0, -1.9, 1.3], "focal": 35, "ease": "inout"},
                         {"t": 20 * BEAT, "loc": [-0.5, -4.4, 1.7], "target": [0, -1.8, 1.0], "focal": 35, "ease": "inout"},
                         {"t": 30 * BEAT, "loc": [-0.2, -3.3, 1.5], "target": [0, -1.5, 0.6], "focal": 35, "ease": "inout"}],
                 "frame_range": [64, int(round(S3 * 15))], "persist": True},
}
# N4: doors + trunk open, wide from the front-right (outer skins); rear door, front door, lid close; all shut on k80
N4_CAM = [orbit(0, 7.0, -50, 3.4, c=(0.3, -0.2, 0.8), focal=30, ease="lin"),
          orbit(S4, 6.2, -42, 3.0, c=(0.1, -0.1, 0.6), focal=30, ease="out2")]


def close(start, t0, t1):
    return [dict(t=0, **start), dict(t=t0, **start), dict(t=t1, ease="in", **(CLOSED if start is OPEN else SHUT))]


SHOTS["N4_reassemble"] = {
    "base": [f"{P}/explode_base_ns.blend"],
    "parts": [dict(RD, keys=close(RD_OPEN, 4 * BEAT, 6 * BEAT)), dict(FD, keys=close(FD_OPEN, 5 * BEAT, 7 * BEAT)),
              dict(LID, keys=close(OPEN, 6 * BEAT, 8 * BEAT))],
    "cam": N4_CAM, "frame_range": [1, 52]}
SHOTS["N4b_clean"] = {"base": [CAR], "cam": N4_CAM, "frame_range": [53, int(round(S4 * 15))], "secs": S4,
                      "out": "N4_reassemble", "persist": True}


def spec(name, mode):
    s = SHOTS[name]
    secs = s.get("secs", SECS.get(name))
    o = s.get("out", name)
    out = {"base": s["base"], "parts": s.get("parts", []), "camera": {"keys": s["cam"], "sensor": 20.25},
           "seconds": secs, "fps": 15, "res": "1080x1920", "persist": s.get("persist", False)}
    fr = s.get("frame_range") or [1, int(round(secs * 15))]
    if mode == "preview":
        out.update(res_pct=30, samples=8, persist=False, out=f"{OUT}/preview3/{o}",
                   frames=[fr[0], (fr[0] * 2 + fr[1]) // 3, (fr[0] + 2 * fr[1]) // 3, fr[1]])
    else:
        out.update(res_pct=75, samples=12, out=f"{OUT}/final3/{o}")
        if s.get("frame_range"):
            out["frame_range"] = s["frame_range"]
    p = f"{SPECS}/{name}_v3{mode}.json"
    json.dump(out, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    for n in (sys.argv[2:] or SHOTS):
        print(spec(n, sys.argv[1]))
