"""v4 shot specs (user on v3: music too intense -> GT2 'Going Up North'; the bay behind the under-bumper parts must be
real scan data; parts on a bumper never come off before the bumper) -> JSON for tools/shot.py.

    python projects/toyota-gr-corolla/tools/shots_v5.py frames|preview|final [shot ...]

Music: 'Going Up North' 102.9 BPM (beat 0.583 s, bar 2.332 s; grid 96.426 + 0.583k from 40-200 Hz spectral flux - the
sub band follows the bass line, not the kicks). Start 109.252; bass returns 112.75, first full downbeat 113.916 = video
4.664 s (frame 140) = the bumper. One bar per shot: cuts at frames 70/140/.../560, dip 630. Part moves render at native 30 fps (minterpolate smears fast parts - lessons); camera-only shots
render 15 fps and are interpolated. Each render carries +3 source frames past the cut (minterpolate tail - lessons).
Frame: car4.json (front -Y, car's right -X, floor z 0). Plates are kept (user rule: only the IS300 is flattened):
car4w_p / dbase_p / diffuser_p are the plate-intact preps; car2w was never deplated.
Front under-bumper data = Drive 'Front Bumper Underbody Data' (beams, ducts, intercooler) - all in the car frame
(colour check chk/under_*.png). Front-off base fbase3 = full car minus the front-bumper zone + Engine Bay Stripped (radiator, rails, engine front: the real
scan under the parts) + Chassis Stripped only where the bay scan has no data.
"""
import json
import os
import sys

B = "/home/user/media/work/grc/blend"
OUT = "/home/user/media/work/grc/renders5"
SPECS = "/home/user/media/work/grc/specs5"
CAR, CAR_HI = f"{B}/car4w_p.blend", f"{B}/car2w.blend"
FBASE, DBASE, XBASE, CBASE = f"{B}/fbase3.blend", f"{B}/dbase_p.blend", f"{B}/xbase.blend", f"{B}/cbase.blend"
FB, RB, RBI, DF = f"{B}/fbumper.blend", f"{B}/rbumper.blend", f"{B}/rbinner.blend", f"{B}/diffuser_p.blend"
UB, LB, FD, RD, RDV, IC = (f"{B}/{n}.blend" for n in ("ubeam", "lbeam", "fbducts", "raddu", "raddiv", "ic"))
RB_PIVOT = [0, 1.91, 0.52]
Z3 = [0, 0, 0]

# shot: (frames on screen at 30 fps, render fps). Renders add 3 source frames past the cut.
LEN = {"a1_whole": (70, 15), "a2_grille": (70, 15),
       "b1_fbumper": (70, 30), "b2_beams": (70, 30), "b3_ducts": (70, 30), "b4_ic": (70, 30),
       "c1_rbumper": (70, 30), "c2_crash": (70, 15), "d1_clean": (70, 15)}


def cam(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": loc, "target": tgt, "focal": focal, "ease": ease}


def k(t, loc=Z3, rot=Z3, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def part(blend, keys, pivot=None):
    d = {"blend": blend, "keys": keys}
    if pivot:
        d["pivot"] = pivot
    return d


E = 2.45  # end of a one-bar shot incl. tail
C1_END = cam(E, [1.15, 4.2, 0.75], [0, 2.05, 0.6], 32)
SHOTS = {
    # BUILD (breakdown, kick on every beat): whole car push -> grille (intercooler behind the mesh)
    "a1_whole": {"base": [CAR], "cam": [cam(0, [-4.4, -6.3, 1.6], [0, -0.3, 0.6]),
                                        cam(E, [-3.0, -4.75, 1.08], [0, -0.55, 0.55], ease="out")]},
    "a2_grille": {"base": [CAR_HI], "cam": [cam(0, [-1.5, -4.2, 0.72], [-0.05, -2.05, 0.38], 40),
                                            cam(E, [-0.7, -3.82, 0.5], [0, -2.05, 0.33], 40)]},
    # GROOVE (112.44): bumper first, then what was behind it, one removal per bar; the bay scan stays put behind them
    "b1_fbumper": {"base": [FBASE], "parts": [part(UB, []), part(LB, []), part(FD, []), part(RD, []), part(RDV, []),
                                                part(IC, []),
                                                part(FB, [k(0), k(0.1), k(0.7, [0, -0.55, 0.12], ease="out"),
                                                          k(1.65, [0, -0.85, 2.9], [150, 0, 0], ease="in2")])],
                   "cam": [cam(0, [-2.3, -4.75, 0.85], [0, -1.85, 0.4], 30), cam(E, [-1.95, -4.35, 0.72], [0, -1.9, 0.36], 30)]},
    "b2_beams": {"base": [FBASE], "parts": [part(FD, []), part(RD, []), part(RDV, []), part(IC, []),
                                              part(UB, [k(0), k(0.15), k(0.65, [0, -0.45, 0], ease="out"),
                                                        k(1.4, [0, -0.6, 1.5], ease="in2")]),
                                              part(LB, [k(0), k(0.7), k(1.15, [0, -0.45, 0], ease="out"),
                                                        k(1.95, [0, -0.6, -0.9], ease="in2")])],
                 "cam": [cam(0, [-0.35, -4.4, 0.55], [0, -1.9, 0.37], 30), cam(E, [-0.22, -4.05, 0.5], [0, -1.9, 0.35], 30)]},
    "b3_ducts": {"base": [FBASE], "parts": [part(IC, []),
                                              part(FD, [k(0), k(0.15), k(0.7, [0, -0.5, 0], ease="out"),
                                                        k(1.3, [0, -0.6, -2.0], ease="in2")]),
                                              part(RDV, [k(0), k(0.6), k(1.1, [0, -0.5, 0], ease="out"),
                                                         k(1.7, [0, -0.6, 1.3], ease="in2")]),
                                              part(RD, [k(0), k(0.75), k(1.3, [0, -0.55, 0], ease="out"),
                                                        k(1.95, [0, -0.65, 1.5], ease="in2")])],
                 "cam": [cam(0, [1.75, -4.1, 0.7], [0, -1.95, 0.38], 32), cam(E, [1.4, -3.75, 0.6], [0, -1.95, 0.36], 32)]},
    "b4_ic": {"base": [FBASE], "parts": [part(IC, [k(0), k(0.15), k(0.8, [0, -0.5, 0.12], ease="out"),
                                                    k(1.6, [0, -0.55, 0.2], [0, 0, -20])])],
              "cam": [cam(0, [-0.75, -4.6, 0.9], [0, -2.3, 0.3], 32), cam(E, [-0.5, -4.25, 0.78], [0, -2.3, 0.3], 32)]},
    # REAR: the diffuser is mounted on the bumper -> they come off TOGETHER (user rule), then the crash beam state swap
    "c1_rbumper": {"base": [XBASE], "parts": [part(b, [k(0), k(0.15), k(0.85, [0, 0.55, 0.15], ease="out"),
                                                        k(1.85, [0, 0.8, 1.8], [150, 0, 0], ease="in2")], RB_PIVOT)
                                               for b in (RB, RBI, DF)],
                   "cam": [cam(0, [2.0, 6.0, 0.93], [0, 2.25, 0.88]), C1_END]},
    # same camera as c1's end: swap to 'crash bar removed' on the kick
    "c2_crash": {"base": [CBASE], "cam": [cam(0, C1_END["loc"], C1_END["target"], 32),
                                          cam(E, [0.75, 4.05, 0.74], [-0.05, 2.03, 0.6], 32)]},
    "d1_clean": {"base": [CAR], "cam": [cam(0, [3.85, 4.95, 1.4], [0, 0.4, 0.58], 30),
                                        cam(E, [3.68, 4.78, 1.29], [0, 0.4, 0.55], 30, ease="out")]},
}


def spec(name, mode):
    s = SHOTS[name]
    frames30, fps = LEN[name]
    fps = 15 if mode != "final" else fps
    n = -(-frames30 * fps // 30) + 3
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
