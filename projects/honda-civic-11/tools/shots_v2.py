"""v2 shot specs (director.md / direction.md) -> JSON for projects/honda-civic-11/tools/shot.py (persistent data off).

    python projects/honda-civic-11/tools/shots_v2.py preview|final [shot ...]

Order: N1 whole car front-left (0-k24) -> s3 wheel (v1, reversed) -> s4 lamp (v1) -> N2 right doors out (Door Open state)
-> N3 trunk opens + lid lifts off (Trunk Open state) -> N4 reassembly (lock k80, clean car from frame 53) -> logo.
Plate-bearing meshes are the deplated ones (tools/deplate.py): car4f_dp, lid_dp.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import BEAT, CLOSED, HINGE, K, OUT, P, SPECS, orbit  # noqa: E402

CAR = f"{P}/car4f_dp.blend"
LID = {"blend": f"{P}/lid_dp.blend", "pivot": HINGE["pivot_prepped"]}
OPEN = {"loc": [0, 0, 0], "rot": [0, 0, 0]}
SECS = {"N1_open": K(24) + 0.2,   # k17 has no hit (+2.9 dB); first real accent k24 (+16.6 dB)
        "N2_doors": K(42) - K(31) + 0.2, "N3_trunk": K(72) - K(42) + 0.2,
        "N4_reassemble": K(88) - K(72) + 0.2}
DRIFT = 1.03


def add(a, b, s=1.0):
    return [x + s * y for x, y in zip(a, b)]


# N2 doors: translate only (no scanned inner faces): lift up + slightly out so the Door Open jambs, sill and cabin show
FD_OUT, RD_OUT = [0.25, 0.05, 1.0], [0.25, -0.05, 1.0]   # up into the black above the car (v2 preview: out toward the lens hid the jambs)
Z3 = [0, 0, 0]


def door_keys(out, t0, t1, secs):
    return [dict(t=0, loc=Z3, rot=Z3), dict(t=t0, loc=Z3, rot=Z3), dict(t=t1, loc=out, rot=Z3, ease="out"),
            dict(t=secs, loc=[DRIFT * v for v in out], rot=Z3, ease="lin")]


# N3 lid: closed -> opens on its fitted hinge (k44 -> k49) -> holds -> lifts off on k52 (up + toward the camera, tips 20 deg)
LIFT_LOC, LIFT_ROT = [0, -0.30, 0.55], [20, 0, 0]

SHOTS = {
    "N1_open": {"base": [CAR], "cam": [orbit(0, 8.6, 30, 1.0, c=(0, 0.3, 0.6), focal=30, ease="lin"),
                                       orbit(SECS["N1_open"], 7.6, 34, 1.3, c=(0, 0.3, 0.6), focal=30, ease="out2")],
                "fps": 10},   # slow near-linear push: 10 fps + minterpolate (director.md budget note)
    "N2_doors": {"base": [f"{P}/doors_base_ns.blend"],
                 "parts": [{"blend": f"{P}/front_door.blend", "keys": door_keys(FD_OUT, 0.0, 2 * BEAT, SECS["N2_doors"])},
                           {"blend": f"{P}/rear_door.blend", "keys": door_keys(RD_OUT, 3 * BEAT, 5 * BEAT, SECS["N2_doors"])}],
                 "cam": [{"t": 0, "loc": [3.4, 2.9, 1.3], "target": [0.8, 0.0, 0.95], "focal": 30},
                         {"t": SECS["N2_doors"] - 0.2, "loc": [2.95, 2.3, 1.3], "target": [0.75, -0.1, 1.0], "focal": 30,
                          "ease": "inout"}]},
    "N3_trunk": {"base": [f"{P}/trunk_base_ns.blend"],
                 "parts": [dict(LID, keys=[dict(t=0, **CLOSED), dict(t=2 * BEAT, **CLOSED),
                                           dict(t=7 * BEAT, ease="inout", **OPEN), dict(t=10 * BEAT, **OPEN),
                                           dict(t=12 * BEAT, loc=LIFT_LOC, rot=LIFT_ROT, ease="out"),
                                           dict(t=SECS["N3_trunk"], loc=[DRIFT * v for v in LIFT_LOC],
                                                rot=[DRIFT * v for v in LIFT_ROT], ease="lin")])],
                 # v2 preview: car sat high with black below and the lifted lid left the top -> car low, lid stacked above
                 "cam": [{"t": 0, "loc": [-0.5, -5.4, 1.6], "target": [0, -1.9, 1.15], "focal": 35},
                         {"t": 10 * BEAT, "loc": [-0.4, -4.9, 1.9], "target": [0, -1.9, 1.3], "focal": 35, "ease": "inout"},
                         {"t": 20 * BEAT, "loc": [-0.4, -5.5, 2.1], "target": [0, -2.0, 1.6], "focal": 35, "ease": "inout"},
                         {"t": 30 * BEAT, "loc": [-0.25, -3.3, 2.1], "target": [0, -1.5, 0.55], "focal": 35, "ease": "inout"}]},
}

# N4: parts start at their N2/N3 end poses, drift to k76, fly home and LOCK on k80; from frame 53 the clean car alone.
S4 = SECS["N4_reassemble"]
T_RET, T_LOCK = 4 * BEAT, 8 * BEAT


def back(end, home):
    return [dict(t=0, **end), dict(t=T_RET, loc=add(home["loc"], add(end["loc"], home["loc"], -1), 1.02),
                                   rot=end["rot"], ease="lin"), dict(t=T_LOCK, ease="in", **home)]


N4_CAM = [orbit(0, 7.0, -145, 4.3, c=(0.1, -0.5, 0.9), focal=30, ease="lin"),   # v2 preview: lid clipped at r 6.4
          orbit(S4, 6.2, -140, 4.0, c=(0.1, -0.3, 0.6), focal=30, ease="out2")]
LID_END = {"loc": [DRIFT * v for v in LIFT_LOC], "rot": [DRIFT * v for v in LIFT_ROT]}
HOME0 = {"loc": Z3, "rot": Z3}
SHOTS["N4_reassemble"] = {
    "base": [f"{P}/explode_base_ns.blend"],
    "parts": [{"blend": f"{P}/front_door.blend", "keys": back({"loc": [DRIFT * v for v in FD_OUT], "rot": Z3}, HOME0)},
              {"blend": f"{P}/rear_door.blend", "keys": back({"loc": [DRIFT * v for v in RD_OUT], "rot": Z3}, HOME0)},
              dict(LID, keys=back(LID_END, CLOSED))],
    "cam": N4_CAM, "frame_range": [1, 52]}
SHOTS["N4b_clean"] = {"base": [CAR], "cam": N4_CAM, "frame_range": [53, int(round(S4 * 15))], "secs": S4,
                      "out": "N4_reassemble"}


def spec(name, mode):
    s = SHOTS[name]
    secs = s.get("secs", SECS.get(name))
    o = s.get("out", name)
    fps = s.get("fps", 15)
    out = {"base": s["base"], "parts": s.get("parts", []), "camera": {"keys": s["cam"], "sensor": 20.25},
           "seconds": secs, "fps": fps, "res": "1080x1920", "persist": False}
    if mode == "preview":
        fr = s.get("frame_range")
        n = int(round(secs * 15))
        pick = [fr[0], (fr[0] + fr[1]) // 2, fr[1]] if fr else ["first", "mid", "last"]
        out.update(res_pct=30, samples=8, frames=pick, out=f"{OUT}/preview2/{o}")
    else:
        out.update(res_pct=75, samples=12, out=f"{OUT}/final/{o}")
        if s.get("frame_range"):
            out["frame_range"] = s["frame_range"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(out, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in (sys.argv[2:] or SHOTS):
        print(spec(n, mode))
