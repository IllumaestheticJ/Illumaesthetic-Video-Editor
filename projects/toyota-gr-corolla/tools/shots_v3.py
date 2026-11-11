"""v2-final shot specs, implementing projects/toyota-gr-corolla/direction.md (scene-director) -> JSON for tools/shot.py.

    python projects/toyota-gr-corolla/tools/shots_v3.py frames|final [shot ...]

Travel front -> side -> rear; each section one continuous sequence; the rear removed-state data is the hero run in the
physical order the parts came off (diffuser -> rear bumper -> crash beam). Frame: car4.json (front -Y, car's right -X,
floor z 0). Shot lengths are whole frames on the 140 BPM accents (direction.md section 2). Keys are shot-relative seconds.
Bases: car4w/car2w (deplated, real rear-left wheel), xbase (bumpers + diffuser zones -> 'rear bumper removed' /
'diffuser removed' / Chassis Stripped as captured), dbase (diffuser zone -> 'diffuser removed', rear bumper on),
cbase (bumper zones -> 'crash bar removed' + Chassis Stripped front).
"""
import json
import os
import sys

B = "/home/user/media/work/grc/blend"
OUT = "/home/user/media/work/grc/renders3"
SPECS = "/home/user/media/work/grc/specs3"
CAR, CAR_HI = f"{B}/car4w.blend", f"{B}/car2w.blend"
XBASE, DBASE, CBASE = f"{B}/xbase.blend", f"{B}/dbase.blend", f"{B}/cbase.blend"
FB, RB, RBI, DF = f"{B}/fbumper.blend", f"{B}/rbumper.blend", f"{B}/rbinner.blend", f"{B}/diffuser.blend"
RB_PIVOT = [0, 1.91, 0.52]  # shared so the outer and inner skins stay one bumper
FB_OUT, FB_TIP = [-0.45, -0.7, 0.95], [160, 0, 0]
RB_OUT, RB_TIP = [0, 0.9, 1.25], [165, 0, 0]
DF_OUT = [0, 0.55, -0.32]
Z3 = [0, 0, 0]
SECS = {"s1_whole": 105 / 30, "s2_wheel": 103 / 30, "s3_hood": 103 / 30, "s4_nose": 103 / 30, "s5_fbumper": 154 / 30,
        "s6_side": 52 / 30, "s7_diffuser": 103 / 30, "s8_rbumper": 102 / 30, "s9_mounts": 103 / 30,
        "s10_reassemble": 52 / 30, "s11_clean": 51 / 30}


def cam(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": loc, "target": tgt, "focal": focal, "ease": ease}


def k(t, loc=Z3, rot=Z3, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def still(blend, pivot=None):
    d = {"blend": blend}
    if pivot:
        d["pivot"] = pivot
    return d


S = SECS
SHOTS = {
    "s1_whole": {"base": [CAR], "cam": [cam(0, [-4.9, -6.9, 1.8], [0, -0.15, 0.6]), cam(S["s1_whole"], [-3.95, -6.05, 1.32], [0, -0.42, 0.55], ease="out")]},
    "s2_wheel": {"base": [CAR_HI], "cam": [cam(0, [-2.55, -0.45, 0.45], [-0.85, -1.05, 0.36], 34), cam(S["s2_wheel"], [-2.55, -1.85, 0.45], [-0.85, -1.36, 0.34], 34)]},
    "s3_hood": {"base": [CAR_HI], "cam": [cam(0, [-0.9, 0.2, 2.35], [-0.1, -1.2, 0.95], 32), cam(S["s3_hood"], [-0.55, -1.0, 2.0], [0, -1.85, 0.8], 32)]},
    "s4_nose": {"base": [CAR_HI], "cam": [cam(0, [-1.75, -3.1, 0.85], [-0.65, -1.95, 0.72], 38), cam(S["s4_nose"], [0.0, -3.65, 0.80], [0, -2.0, 0.62], 38)]},
    # DROP 1 (shot start = beat 32): bumper forward into clear black, hold, tip to show the scanned inner face, hold
    "s5_fbumper": {"base": [XBASE], "parts": [still(RB, RB_PIVOT), still(RBI, RB_PIVOT), still(DF),
                   {"blend": FB, "keys": [k(0), k(0.0667), k(1.7, FB_OUT, ease="out"), k(2.4, FB_OUT), k(3.6, FB_OUT, FB_TIP)]}],
                   "cam": [cam(0, [-2.9, -5.6, 1.5], [-0.1, -1.7, 0.7], 30), cam(S["s5_fbumper"], [-2.6, -6.0, 1.85], [-0.35, -2.4, 0.95], 30)]},
    # the side once, whole car from rear-left, front bumper already off (progressive)
    "s6_side": {"base": [XBASE], "parts": [still(RB, RB_PIVOT), still(RBI, RB_PIVOT), still(DF)],
                "cam": [cam(0, [4.08, 5.98, 1.58], [0, 0.18, 0.6]), cam(S["s6_side"], [4.15, 6.1, 1.75], [0, 0.2, 0.6])]},
    # rear 1: diffuser off on the 'diffuser removed' state (rear bumper still on)
    "s7_diffuser": {"base": [DBASE], "parts": [{"blend": DF, "keys": [k(0), k(0.0667), k(1.8, DF_OUT, ease="out")]}],
                    "cam": [cam(0, [2.4, 6.7, 0.7], [-0.1, 1.9, 0.45]), cam(S["s7_diffuser"], [1.0, 4.75, 0.6], [0, 2.0, 0.38])]},
    # rear 2: rear bumper (outer + inner) up and tipped to show the inner face; camera pushes in onto the crash beam
    "s8_rbumper": {"base": [XBASE], "parts": [
        {"blend": b, "pivot": RB_PIVOT, "keys": [k(0), k(0.0667), k(1.4, RB_OUT, ease="out"), k(1.5, RB_OUT), k(2.6, RB_OUT, RB_TIP)]}
        for b in (RB, RBI)],
        "cam": [cam(0, [2.2, 6.4, 0.95], [0, 2.3, 0.95], 30), cam(1.7, [2.0, 6.0, 0.93], [0, 2.25, 0.88], 30),
                cam(S["s8_rbumper"], [1.1, 4.1, 0.75], [0, 2.05, 0.6], 32)]},
    # DROP 2: same camera, state swap to 'crash bar removed' - mounting points; slow slide across the rear panel
    "s9_mounts": {"base": [CBASE], "cam": [cam(0, [1.1, 4.1, 0.75], [0, 2.05, 0.6], 32), cam(S["s9_mounts"], [-0.35, 4.25, 0.85], [-0.1, 2.0, 0.6], 32)]},
    # reassembly from high rear-left: parts home on successive kicks, lock on b76
    "s10_reassemble": {"base": [XBASE], "parts": [
        {"blend": b, "pivot": RB_PIVOT, "keys": [k(0, RB_OUT, RB_TIP), k(0.0667, RB_OUT, RB_TIP), k(0.87, Z3, Z3, "in")]} for b in (RB, RBI)] + [
        {"blend": DF, "keys": [k(0, DF_OUT), k(0.43, DF_OUT), k(1.30, Z3, Z3, "in")]},
        {"blend": FB, "keys": [k(0, FB_OUT, FB_TIP), k(0.87, FB_OUT, FB_TIP), k(1.70, Z3, Z3, "in")]}],
        "cam": [cam(0, [4.5, 4.2, 8.1], [0, -0.1, 0.6], 28), cam(S["s10_reassemble"], [4.3, 4.05, 7.8], [0, -0.1, 0.6], 28)]},
    "s11_clean": {"base": [CAR], "cam": [cam(0, [4.3, 4.05, 7.8], [0, -0.1, 0.6], 28), cam(S["s11_clean"], [4.15, 3.92, 7.5], [0, -0.1, 0.6], 28)]},
}


def spec(name, mode):
    s = SHOTS[name]
    sp = {"base": s["base"], "parts": s.get("parts", []), "camera": {"sensor": 20.25, "keys": s["cam"]},
          "seconds": S[name] + 1 / 15, "fps": 15, "res": "1080x1920",
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
