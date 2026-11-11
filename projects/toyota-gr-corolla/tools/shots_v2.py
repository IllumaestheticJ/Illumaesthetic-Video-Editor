"""v2 shot specs (reviewer: same standard v1 notes as the sibling reels) -> JSON for tools/shot.py.

    python projects/toyota-gr-corolla/tools/shots_v2.py preview|final|frames [shot ...]

v2 rules applied: whole car in frame for full-car shots (no crop); no turntables/orbits - every shot is a push, slide
or rise that shows something new; the removed areas carry the reel: front bumper comes off framed on the front, then
a close look at the scanned structure behind it, then the rear bumper (one 180 deg turn to show its scanned inner
side - the only spin, and it has a backside worth seeing), then the diffuser; parts move out into clear background;
drop 2 = all three parts out over the whole car from a new angle, then fly home and lock; swap to the clean car on
the lock, short hold, dip to black, small logo.
Frame: front -Y, car's right -X, floor z 0 (car4.json). Cut frames (30 fps) in timing_v2.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/home/user/media/work/grc/blend"
OUT = "/home/user/media/work/grc/renders2"
SPECS = "/home/user/media/work/grc/specs2"
T = json.load(open(os.path.join(HERE, "..", "timing_v2.json")))
S = T["secs"]
CAR, CAR_HI, XBASE = f"{B}/car4w.blend", f"{B}/car2w.blend", f"{B}/xbase.blend"
FB, RB, RBI, DF = f"{B}/fbumper.blend", f"{B}/rbumper.blend", f"{B}/rbinner.blend", f"{B}/diffuser.blend"
OFF = {"fb": [0, -0.75, 1.15], "rb": [0, 1.25, 1.15], "df": [0, 0.75, -0.25]}
RB_ROT = [0, 0, 180]  # one turn about the vertical: the scanned inner side faces the rear camera
Z3 = [0, 0, 0]


def cam(t, loc, tgt, focal=30, ease="inout"):
    return {"t": t, "loc": loc, "target": tgt, "focal": focal, "ease": ease}


def k(t, loc, rot=Z3, ease="inout"):
    return {"t": t, "loc": loc, "rot": rot, "ease": ease}


def at(blend, loc, rot=Z3):
    return {"blend": blend, "keys": [k(0, loc, rot)]}


SHOTS = {
    # whole car, front-right 3/4, slow push (no orbit)
    "a1_front": {"base": [CAR], "cam": [cam(0, [-4.3, -6.3, 1.55], [0, -0.15, 0.6]), cam(S["a1_front"], [-3.85, -5.65, 1.5], [0, -0.2, 0.6])]},
    # whole car, rear-left 3/4 (real rear wheel side), slow push + slight rise
    "a2_rear": {"base": [CAR], "cam": [cam(0, [4.3, 6.3, 1.4], [0, 0.15, 0.6]), cam(S["a2_rear"], [3.85, 5.65, 1.75], [0, 0.2, 0.6])]},
    # whole car from straight above, slow descent (nose at the bottom of frame)
    "a3_top": {"base": [CAR], "cam": [cam(0, [0, -0.02, 9.2], [0, 0, 0.5]), cam(S["a3_top"], [0, -0.02, 8.0], [0, 0, 0.5])]},
    # extreme close-ups (2 mm): front-right wheel, then headlight + grille - slides
    "a4_wheel": {"base": [CAR_HI], "cam": [cam(0, [-1.95, -0.95, 0.40], [-0.85, -1.45, 0.34], 38), cam(S["a4_wheel"], [-1.95, -1.85, 0.42], [-0.85, -1.38, 0.34], 38)]},
    "a5_nose": {"base": [CAR_HI], "cam": [cam(0, [-1.55, -3.35, 0.85], [-0.55, -1.95, 0.70], 38), cam(S["a5_nose"], [-0.35, -3.6, 0.80], [-0.25, -2.0, 0.62], 38)]},
    # DROP: front bumper comes off, camera framed on the front (front-right, high); bumper lifts up and forward above the nose into clear space
    "b1_fbumper": {"base": [XBASE], "parts": [at(RB, Z3), at(RBI, Z3), at(DF, Z3),
                   {"blend": FB, "keys": [k(0, Z3), k(T["fb_off"][0], Z3), k(T["fb_off"][1], OFF["fb"], ease="out")]}],
                   "cam": [cam(0, [-3.0, -6.4, 1.9], [0, -1.6, 0.85]), cam(S["b1_fbumper"], [-2.75, -6.0, 1.85], [0, -1.65, 0.85])]},
    # the scanned structure behind the bumper (Chassis Stripped front), slow slide across it
    "b2_front_detail": {"base": [XBASE], "parts": [at(RB, Z3), at(RBI, Z3), at(DF, Z3)],
                        "cam": [cam(0, [-1.7, -3.85, 1.05], [-0.45, -1.9, 0.45], 32), cam(S["b2_front_detail"], [0.9, -3.85, 1.0], [0.3, -1.9, 0.45], 32)]},
    # rear bumper off, framed on the rear (rear-left): back 1.25 m and up 1.15 m into clear space, then one turn to show its inner side
    "b3_rbumper": {"base": [XBASE], "parts": [at(DF, Z3)] + [
                   {"blend": b, "keys": [k(0, Z3), k(T["rb_off"][0], Z3), k(T["rb_off"][1], OFF["rb"], ease="out"),
                                         k(T["rb_turn"][0], OFF["rb"]), k(T["rb_turn"][1], OFF["rb"], RB_ROT)]} for b in (RB, RBI)],
                   "cam": [cam(0, [3.6, 7.3, 2.1], [0, 2.3, 0.9]), cam(S["b3_rbumper"], [3.3, 6.9, 2.0], [0, 2.4, 0.9])]},
    # diffuser drops away, low rear-left close (rear bumper already off, out of shot)
    "b4_diffuser": {"base": [XBASE], "parts": [
                    {"blend": DF, "keys": [k(0, Z3), k(T["df_off"][0], Z3), k(T["df_off"][1], OFF["df"], ease="out")]}],
                    "cam": [cam(0, [2.3, 5.4, 0.75], [0, 2.0, 0.3], 30), cam(S["b4_diffuser"], [2.0, 5.0, 0.7], [0, 2.05, 0.3], 30)]},
    # DROP 2: the whole exploded car from high rear-left looking down (new angle; length runs up the 9:16 frame), parts in clear space; fly home, LOCK on b76
    "c1_explode": {"base": [XBASE], "parts": [
        {"blend": FB, "keys": [k(0, OFF["fb"]), k(T["home"][0], OFF["fb"]), k(T["home"][1], Z3, ease="in")]}] + [
        {"blend": b, "keys": [k(0, OFF["rb"], RB_ROT), k(T["home"][0], OFF["rb"], RB_ROT), k(T["home"][1], Z3, Z3, ease="in")]} for b in (RB, RBI)] + [
        {"blend": DF, "keys": [k(0, OFF["df"]), k(T["home"][0], OFF["df"]), k(T["home"][1], Z3, ease="in")]}],
        "cam": [cam(0, [4.2, 4.0, 7.6], [0, -0.1, 0.6], 28), cam(S["c1_explode"], [3.95, 3.75, 7.1], [0, -0.1, 0.6], 28)]},
    # clean full car on the lock (frayed composite seams gone), whole car low front-left, short push -> dip to black
    "c2_hero": {"base": [CAR], "cam": [cam(0, [4.5, -6.0, 0.95], [0, -0.1, 0.55]), cam(S["c2_hero"], [4.15, -5.5, 0.95], [0, -0.1, 0.55])]},
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
