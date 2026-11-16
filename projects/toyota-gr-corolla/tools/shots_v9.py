"""v9 (user on v7: "the hood is cut wrong" -> hood traced on its shut lines along the hood normal: cowl seam,
fender shut lines, front crease; tools/hoodtrace.py).

v8 (user on v6: "please have the front bumper use the other full car scan - this one is missing a huge chunk of the
front bumper" [FARO stock bumper: farobumper.py; NOT the facelift Complete Car], "rear trunk isn't cut out correctly"
[hatch3 traced on its shut lines: hatchtrace.py], "we don't show the hood opening" [k1: hood hinges open on its rear
edge over the engine bay scan, then lifts off]). Every later shot keeps bumper/hood/hatch off.

v7: Short-form Temerario restart (user on v5: "completely start this over, using the short form temerario skill, and
graphify"). Shot specs -> JSON for tools/shot.py.

    python projects/toyota-gr-corolla/tools/shots_v7.py frames|preview|final [shot ...]

Music: GT2 'Going Up North' FROM ITS BEGINNING (skill), 102.95 BPM, bar 2.3312 s, downbeats 0.50 + 2.3312k; video
starts at music 0.47 so the first hit lands on frame 1. Ten one-bar shots, logo where the drums thin out (23.8 s).
Rules applied (graphify feedback index + lessons): bumper comes off FIRST and whole (user v5: the bumper part was
missing a chunk -> fbumper6 = bumper scan + every car face cut off as bumper skin that the scan lacks); nothing of a
removed part stays on the car; headlights stay (fbase5); the bay scan stays behind the under-bumper parts; the hatch
hinges open THEN comes off (GR86 rule) over the real cargo area of the 'trunk open' state; the diffuser leaves with
the rear bumper; every later rear shot keeps the hatch off; one action per bar; plates kept; labels from file names.
Reused renders (same base/camera/keys as here): a1/d1 = renders5, b2-b4 = renders6 (fbase5).
"""
import json
import os
import sys

B = "/home/user/media/work/grc/blend"
OUT = "/home/user/media/work/grc/renders9"
SPECS = "/home/user/media/work/grc/specs9"
CAR = f"{B}/car8.blend"   # car4w + FARO stock bumper (plate kept)
FBASE = f"{B}/fbase5.blend"
HBASE, XBASE_H, CBASE_H = f"{B}/hbase_all2.blend", f"{B}/xbase_h3.blend", f"{B}/cbase_h3.blend"
HOODBASE, HOOD = f"{B}/fbase5_nh2.blend", f"{B}/hood2f.blend"   # hood traced on its shut lines (hoodtrace.py)
HOOD_PIVOT = [0, -1.112, 0.924]   # traced hood's rear edge (raw y -2104, z 346)
FB = f"{B}/fbumper8.blend"
RB, RBI, DF, HATCH = f"{B}/rbumper.blend", f"{B}/rbinner.blend", f"{B}/diffuser_p.blend", f"{B}/hatch3.blend"
UB, LB, FD, RD, RDV, IC = (f"{B}/{n}.blend" for n in ("ubeam", "lbeam", "fbducts", "raddu", "raddiv", "ic"))
RB_PIVOT = [0, 1.91, 0.52]
HATCH_PIVOT = [0, 1.33, 1.41]   # top edge of the hatch (raw y 330-342, z 828), 75 deg = closed 47.6 deg down -> open 27.4 deg up
HATCH_OPEN = [75, 0, 0]
Z3 = [0, 0, 0]
E = 2.45
LEN = {"a1_whole": (70, 15), "d1_clean": (70, 15), "k1_hood": (70, 30), "b1_fbumper": (70, 30), "h1_hatch": (70, 30), "h2_hatchoff": (70, 30), "c1_rbumper": (70, 30), "c2_crash": (70, 15)}


def cam(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": loc, "target": tgt, "focal": focal, "ease": ease}


def k(t, loc=Z3, rot=Z3, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def part(blend, keys, pivot=None):
    d = {"blend": blend, "keys": keys}
    if pivot:
        d["pivot"] = pivot
    return d


H_CAM_END = cam(E, [2.35, 5.0, 2.15], [0, 1.35, 1.0], 28)
C1_END = cam(E, [1.15, 4.2, 0.75], [0, 2.05, 0.6], 32)
SHOTS = {
    # bumper first, whole, straight forward then up and out; everything behind it stays seated
    "b1_fbumper": {"base": [FBASE], "parts": [part(p, []) for p in (UB, LB, FD, RD, RDV, IC)] + [
        part(FB, [k(0), k(0.1), k(0.7, [0, -0.55, 0.12], ease="out"), k(1.65, [0, -0.85, 2.9], [150, 0, 0], ease="in2")])],
        "cam": [cam(0, [-2.3, -4.75, 0.85], [0, -1.85, 0.4], 30), cam(E, [-1.95, -4.35, 0.72], [0, -1.9, 0.36], 30)]},
    # whole car (FARO stock bumper), song opening
    "a1_whole": {"base": [CAR], "cam": [cam(0, [-4.4, -6.3, 1.6], [0, -0.3, 0.6]),
                                        cam(E, [-3.0, -4.75, 1.08], [0, -0.55, 0.55], ease="out")]},
    # hood hinges open on its rear edge over the engine bay scan, then lifts off (GR86 rule: open THEN off)
    "k1_hood": {"base": [HOODBASE], "parts": [part(HOOD, [k(0), k(0.2), k(1.1, Z3, [-62, 0, 0]), k(1.3, Z3, [-62, 0, 0]),
                                                          k(2.0, [0, 0.4, 2.6], [-80, 0, 0], ease="in2")], HOOD_PIVOT)],
                "cam": [cam(0, [-2.5, -4.7, 2.3], [0, -1.5, 0.75], 28), cam(E, [-2.2, -4.3, 2.1], [0, -1.5, 0.72], 28)]},
    "d1_clean": {"base": [CAR], "cam": [cam(0, [3.85, 4.95, 1.4], [0, 0.4, 0.58], 30),
                                        cam(E, [3.68, 4.78, 1.29], [0, 0.4, 0.55], 30, ease="out")]},
    # hatch hinges open on its top edge (rear-left, high), parks open
    "h1_hatch": {"base": [HBASE], "parts": [part(HATCH, [k(0), k(0.3), k(1.7, Z3, HATCH_OPEN)], HATCH_PIVOT)],
                 "cam": [cam(0, [2.6, 5.5, 2.3], [0, 1.3, 1.0], 28), H_CAM_END]},
    # same camera: the open hatch lifts up and back off the car, out of the top of the frame
    "h2_hatchoff": {"base": [HBASE], "parts": [part(HATCH, [k(0, Z3, HATCH_OPEN), k(0.15, Z3, HATCH_OPEN),
                                                            k(0.7, [0, 0.15, 0.35], HATCH_OPEN, ease="out"),
                                                            k(1.6, [0, 0.5, 3.0], [95, 0, 0], ease="in2")], HATCH_PIVOT)],
                    "cam": [cam(0, H_CAM_END["loc"], H_CAM_END["target"], 28), cam(E, [2.15, 4.7, 1.9], [0, 1.4, 0.95], 28)]},
    # rear bumper WITH its diffuser (user rule), hatch already off
    "c1_rbumper": {"base": [XBASE_H], "parts": [part(b, [k(0), k(0.15), k(0.85, [0, 0.55, 0.15], ease="out"),
                                                          k(1.85, [0, 0.8, 1.8], [150, 0, 0], ease="in2")], RB_PIVOT)
                                                 for b in (RB, RBI, DF)],
                   "cam": [cam(0, [2.0, 6.0, 0.93], [0, 2.25, 0.88]), C1_END]},
    # same camera as c1's end: swap to 'crash bar removed' on the kick
    "c2_crash": {"base": [CBASE_H], "cam": [cam(0, C1_END["loc"], C1_END["target"], 32),
                                            cam(E, [0.75, 4.05, 0.74], [-0.05, 2.03, 0.6], 32)]},
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
