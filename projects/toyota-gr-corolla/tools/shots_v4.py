"""v3 shot specs (user: "add the front under-bumper data" + sibling lessons) -> JSON for tools/shot.py.

    python projects/toyota-gr-corolla/tools/shots_v4.py frames|preview|final [shot ...]

Music: Le Castle Vania "Blood Code", start 114.605 s, 120 BPM, drop at video 6.0 s. Every shot is a whole number of
half-second kicks. Part moves render at native 30 fps (minterpolate smears fast parts - lessons); camera-only shots
render 15 fps and are interpolated. Each render carries +3 source frames past the cut (minterpolate tail - lessons).
Frame: car4.json (front -Y, car's right -X, floor z 0). Plates are kept (user rule: only the IS300 is flattened):
car4w_p / dbase_p / diffuser_p are the plate-intact preps; car2w was never deplated.
Front under-bumper data = Drive 'Front Bumper Underbody Data' (beams, ducts, intercooler) - all in the car frame
(colour check chk/under_*.png). Front-off base fbase = full car minus the front-bumper zone, filled from Chassis Stripped.
"""
import json
import os
import sys

B = "/home/user/media/work/grc/blend"
OUT = "/home/user/media/work/grc/renders4"
SPECS = "/home/user/media/work/grc/specs4"
CAR, CAR_HI = f"{B}/car4w_p.blend", f"{B}/car2w.blend"
FBASE, DBASE, XBASE, CBASE = f"{B}/fbase2.blend", f"{B}/dbase_p.blend", f"{B}/xbase.blend", f"{B}/cbase.blend"
FB, RB, RBI, DF = f"{B}/fbumper.blend", f"{B}/rbumper.blend", f"{B}/rbinner.blend", f"{B}/diffuser_p.blend"
UB, LB, FD, RD, RDV, IC = (f"{B}/{n}.blend" for n in ("ubeam", "lbeam", "fbducts", "raddu", "raddiv", "ic"))
RB_PIVOT = [0, 1.91, 0.52]
Z3 = [0, 0, 0]

# shot: (seconds on screen, fps). seconds are multiples of 0.5 (kicks); renders add 3 source frames.
LEN = {"a1_whole": (2.0, 15), "a2_grille": (2.0, 15), "a3_wheel": (2.0, 15),
       "b1_fbumper": (2.0, 30), "b2_beams": (2.0, 30), "b3_ducts": (2.0, 30), "b4_ic": (2.0, 30),
       "c1_diffuser": (2.0, 30), "c2_rbumper": (2.0, 30), "c3_mounts": (1.0, 15), "d1_clean": (2.0, 15)}


def cam(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": loc, "target": tgt, "focal": focal, "ease": ease}


def k(t, loc=Z3, rot=Z3, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def part(blend, keys, pivot=None):
    d = {"blend": blend, "keys": keys}
    if pivot:
        d["pivot"] = pivot
    return d


E = 2.1  # end of a 2 s shot incl. tail
SHOTS = {
    # BUILD (0-6 s): whole car push -> grille (intercooler behind the mesh) -> front wheel/arch
    "a1_whole": {"base": [CAR], "cam": [cam(0, [-4.4, -6.3, 1.6], [0, -0.3, 0.6]),
                                        cam(E, [-3.05, -4.8, 1.1], [0, -0.55, 0.55], ease="out")]},
    "a2_grille": {"base": [CAR_HI], "cam": [cam(0, [-1.5, -4.2, 0.72], [-0.05, -2.05, 0.38], 40),
                                            cam(E, [-0.75, -3.85, 0.52], [0, -2.05, 0.33], 40)]},
    "a3_wheel": {"base": [CAR_HI], "cam": [cam(0, [-2.55, -0.45, 0.45], [-0.85, -1.05, 0.36], 34),
                                           cam(E, [-2.55, -1.6, 0.45], [-0.85, -1.3, 0.34], 34)]},
    # DROP (6 s): front under-bumper sequence on fbase, one removal per shot, each part leaves the frame
    "b1_fbumper": {"base": [FBASE], "parts": [part(UB, []), part(LB, []), part(FD, []), part(RD, []), part(RDV, []),
                                                part(IC, []),
                                                part(FB, [k(0), k(0.1), k(0.75, [0, -0.55, 0.12], ease="out"),
                                                          k(1.75, [0, -0.85, 2.9], [150, 0, 0], ease="in2")])],  # fully out by the cut
                   "cam": [cam(0, [-2.3, -4.75, 0.85], [0, -1.85, 0.4], 30), cam(E, [-1.95, -4.35, 0.72], [0, -1.9, 0.36], 30)]},
    "b2_beams": {"base": [FBASE], "parts": [part(FD, []), part(RD, []), part(RDV, []), part(IC, []),
                                              part(UB, [k(0), k(0.1), k(0.55, [0, -0.45, 0], ease="out"),
                                                        k(1.2, [0, -0.6, 1.5], ease="in2")]),
                                              part(LB, [k(0), k(0.6), k(1.0, [0, -0.45, 0], ease="out"),
                                                        k(1.7, [0, -0.6, -0.9], ease="in2")])],
                 "cam": [cam(0, [-0.35, -4.4, 0.55], [0, -1.9, 0.37], 30), cam(E, [-0.25, -4.1, 0.5], [0, -1.9, 0.35], 30)]},
    "b3_ducts": {"base": [FBASE], "parts": [part(IC, []),
                                              part(FD, [k(0), k(0.1), k(0.6, [0, -0.5, 0], ease="out"),
                                                        k(1.1, [0, -0.6, -2.0], ease="in2")]),
                                              part(RDV, [k(0), k(0.5), k(0.95, [0, -0.5, 0], ease="out"),
                                                         k(1.45, [0, -0.6, 1.3], ease="in2")]),
                                              part(RD, [k(0), k(0.6), k(1.1, [0, -0.55, 0], ease="out"),
                                                        k(1.7, [0, -0.65, 1.5], ease="in2")])],
                 "cam": [cam(0, [1.75, -4.1, 0.7], [0, -1.95, 0.38], 32), cam(E, [1.45, -3.8, 0.6], [0, -1.95, 0.36], 32)]},
    "b4_ic": {"base": [FBASE], "parts": [part(IC, [k(0), k(0.1), k(0.7, [0, -0.5, 0.12], ease="out"),
                                                    k(1.4, [0, -0.55, 0.2], [0, 0, -20])])],
              "cam": [cam(0, [-0.75, -4.6, 0.9], [0, -2.3, 0.3], 32), cam(E, [-0.55, -4.3, 0.8], [0, -2.3, 0.3], 32)]},
    # REAR (diffuser -> rear bumper -> crash beam, the order the state scans were taken), from the car's left
    "c1_diffuser": {"base": [DBASE], "parts": [part(DF, [k(0), k(0.1), k(0.7, [0, 0.45, -0.05], ease="out"),
                                                          k(1.4, [0, 0.9, -3.2], ease="in2")])],
                    "cam": [cam(0, [2.4, 6.7, 0.7], [-0.1, 1.9, 0.45]), cam(E, [1.5, 5.5, 0.62], [0, 1.95, 0.4])]},
    "c2_rbumper": {"base": [XBASE], "parts": [part(b, [k(0), k(0.1), k(0.75, [0, 0.55, 0.15], ease="out"),
                                                        k(1.6, [0, 0.8, 1.8], [150, 0, 0], ease="in2")], RB_PIVOT)
                                               for b in (RB, RBI)],
                   "cam": [cam(0, [2.0, 6.0, 0.93], [0, 2.25, 0.88]), cam(E, [1.15, 4.2, 0.75], [0, 2.05, 0.6], 32)]},
    # same camera as c2's end: state swap to 'crash bar removed' on the kick
    "c3_mounts": {"base": [CBASE], "cam": [cam(0, [1.15, 4.2, 0.75], [0, 2.05, 0.6], 32),
                                           cam(1.2, [0.85, 4.1, 0.75], [-0.05, 2.03, 0.6], 32)]},
    "d1_clean": {"base": [CAR], "cam": [cam(0, [3.85, 4.95, 1.4], [0, 0.4, 0.58], 30),
                                        cam(E, [3.7, 4.8, 1.3], [0, 0.4, 0.55], 30, ease="out")]},
}


def spec(name, mode):
    s = SHOTS[name]
    secs, fps = LEN[name]
    fps = 15 if mode != "final" else fps
    n = int(round(secs * fps)) + 3
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": n / fps, "fps": fps, "res": "1080x1920",
          "res_pct": 75 if mode == "final" else 30, "samples": 12 if mode == "final" else 6,
          "out": f"{OUT}/{mode}/{name}"}
    if mode == "frames":
        sp["frames"] = ["first", "mid", "last"]
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
