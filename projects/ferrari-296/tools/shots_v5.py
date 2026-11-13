"""Ferrari 296 v5 shots: Buckshot Roulette "General Release" (user-supplied), 145 BPM, kick grid measured on the decoded track
(/home/user/media/work/music/buckshot_kicks.json). Times below are VIDEO seconds = music seconds (music starts at 0).

User on v4: "not enough of the parts are blown up or shown" + "learn from the GT3RS video editor". From GT3RS: every part
comes off where the camera is, on a beat, and STAYS off (progressive explode); every part gets a label from its scan file;
parts leave along a clear path (no clipping); all removed parts together, then the stack/blast on the drop and the lock.
New parts vs v4: FRONT WHEEL (cut from the car, arch filled from the wheel-off "Brake Disk" state scan: disc, caliper, hub,
liner - tools/wheel_off.py) and EXHAUST TIP. 9 moving parts in all.

    python3 projects/ferrari-296/tools/shots_v5.py preview|final [shot ...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import P, OUT, SPECS, Z3, _k, _cam, BUMP_FAR, arc  # noqa: E402,F401

KJ = json.load(open("/home/user/media/work/music/buckshot_kicks.json"))
_KK = {int(a): b for a, b in KJ["kicks"].items()}


def K(i):
    """measured kick attack of beat i (grid fit where no kick, e.g. the breakdown 41-56)"""
    return round(_KK.get(i, KJ["t0"] + i * KJ["period"]), 4)


BASE = [f"{P}/comp_v5.blend"]  # comp_explode minus the FR wheel + wheel-off arch fill
HOOD_OPEN = (Z3, (-58, 0, 0))  # f5_front opens the hood on its hinge (scanned propped-open state)
SPREAD, HOME_A, HOME_B = 1.05, K(69), K(71)  # slow drift x1.05 after the blast, fly home 69 -> LOCK on 71


def _end_cam():
    try:
        from cta import camera
        c = camera(os.environ.get("CTA_CAM", "/home/user/media/work/f296/web/fit/s4_best.json"))
        return tuple(c["loc"]), tuple(c["target"]), c["focal"]
    except FileNotFoundError:  # before the photo solve: the v5 drift end pose
        return (-4.20, -4.80, 2.40), (0.00, -0.30, 0.55), 26


END_CAM = _end_cam()


def part(name, keys, pivot=None):
    p = {"blend": f"{P}/{name}.blend", "keys": keys}
    if pivot:
        p["pivot"] = list(pivot)
    return p


def life(off_keys, blast, blast_rot=Z3):
    """off_keys (section motion) -> blast pose on the drop K57->K59 (ease out) -> drift -> home + lock (ease in)."""
    last = off_keys[-1]
    return off_keys + [_k(K(57), last["loc"], last["rot"], "lin"), _k(K(59), blast, blast_rot, "out"),
                       _k(HOME_A, [v * SPREAD for v in blast], blast_rot, "lin"), _k(HOME_B, Z3, Z3, "in")]


PARTS = {
    "x_hood": ((0, -0.86, 0.88), life([_k(-100, *HOOD_OPEN)], (0, -0.35, 1.45), (-20, 0, 0))),
    "x_fbumper": ((0, -1.775, 0.475), life([_k(-100, BUMP_FAR, (0, 0, 80))], (0, -2.25, 0.05), (0, 0, 60))),
    "x_wheel": ((-0.86, -1.132, 0.418), life([_k(-100), _k(K(27)), _k(K(29), (-0.95, 0, 0), Z3, "out")], (-1.75, -0.15, 0.05))),
    "x_fender": (None, life([_k(-100), _k(K(30)), _k(K(31) + 0.35, (-0.55, 0, 0.50), (0, -10, 0), "out")],
                            (-1.25, 0.05, 1.00), (0, -15, 0))),
    "x_skirt": (None, life([_k(-100), _k(K(35)), _k(K(36) + 0.3, (-0.45, 0, -0.25), Z3, "out")], (-1.15, 0.10, -0.10))),
    "x_rbumper": (None, life([_k(-100), _k(K(37)), _k(K(39), (0, 0.95, 0.05), Z3, "out")], (0, 1.95, 0.15))),
    "x_diffuser": (None, life([_k(-100), _k(K(38)), _k(K(40), (0, 0.75, -0.35), Z3, "out")], (0, 1.40, -0.40))),
    # no engine-lid-open scan exists, only the Engine Bay with the lid OFF -> it lifts straight off (rule D)
    "x_ecover": (None, life([_k(-100), _k(K(42)), _k(K(44), (0, 0.10, 0.80), Z3, "out")], (0, 0.50, 1.65))),
    # back out of its pipe first, then up over the pulled rear bumper (clear path)
    "x_exhaust": (None, life([_k(-100), _k(K(46)), _k(K(47) + 0.2, (0, 0.35, 0), Z3, "inout"),
                              _k(K(49), (0, 0.35, 0.62), Z3, "out")], (0, 2.40, 1.00))),
}


def parts_at(t0):
    return [part(n, [dict(k, t=round(k["t"] - t0, 4)) for k in keys], pv) for n, (pv, keys) in PARTS.items()]


SHOTS = {
    # FRONT WHEEL REMOVED -> BRAKE DISC + CALIPER, then the fender lifts off. Camera front-right, low; the wheel slides
    # out along its axle to screen-left, the camera pushes into the scanned arch.
    "v5_wheel": (K(26), K(34), [  # above-front-right, looking down onto the arch: the wheel slides out to screen-left
        (K(26), (-2.70, -3.40, 1.90), (-1.05, -1.20, 0.85), 28, "inout"),  # and stays in frame beside the opened arch
        (K(29), (-2.60, -3.10, 1.75), (-1.30, -1.15, 0.80), 28, "inout"),
        (K(31), (-2.75, -3.00, 2.05), (-1.30, -1.05, 1.00), 28, "inout"),
        (K(34), (-2.50, -2.90, 1.60), (-1.30, -1.15, 0.80), 30, "inout")]),
    # right flank, dolly rearward: skirt drops (35), rear bumper (37) + diffuser (38) pull back
    "v5_side": (K(34), K(40), [
        (K(34), (-3.30, -0.90, 0.85), (-0.80, 0.05, 0.35), 28, "inout"),
        (K(37), (-3.40, 1.40, 1.05), (-0.60, 1.30, 0.45), 28, "inout"),
        (K(40), (-3.70, 3.70, 1.60), (-0.20, 2.10, 0.55), 26, "inout")]),
    # breakdown (no kick): rear-right high; engine cover lifts off (42-44), exhaust tip out (46-49); the camera rises up
    # and over the tail to a high rear view with every part off, long axis vertical, waiting for the drop
    "v5_rear": (K(40), K(57), [
        (K(40), (-2.30, 4.90, 2.10), (0.00, 1.90, 0.60), 30, "inout"),
        (K(44), (-1.50, 4.40, 2.40), (0.00, 1.85, 0.85), 32, "inout"),
        (K(49), (-1.00, 4.70, 2.10), (0.00, 2.25, 0.75), 32, "inout"),
        (K(54), (-1.90, 5.40, 4.20), (0.00, 0.90, 0.50), 28, "inout"),
        (K(57), (-1.00, 4.70, 5.30), (0.00, -0.10, 0.40), 26, "inout")]),
    # THE DROP: every part blasts out (57->59), slow orbit front-right -> side over the floating parts, fly home 69 ->
    # LOCK on 71, then the whole car drifts to the fade (73-75)
    "v5_drop": (K(57), K(75), [  # high front-right looking down the car: the 8 m exploded length runs vertically in 9:16
        (K(57), (-2.60, -6.80, 3.60), (0.00, -1.60, 0.75), 24, "out"),
        (K(63), (-4.60, -5.60, 4.40), (-0.10, -1.20, 0.80), 24, "inout"),
        (K(69), (-5.40, -3.20, 4.60), (-0.50, 0.00, 0.70), 24, "inout"),
        (K(71), (-4.40, -4.60, 2.60), (0.00, -0.30, 0.55), 26, "inout"),
        # CTA (user: "mobile version CTA ... with the 1:1 transition of the website photos"): after the lock the camera
        # swings round the nose (k71 -> k73 accelerating, k73 -> k75 settling) onto the camera solved against the
        # listing's cover photo (tools/photo_search.py, cta.py), and k75 cuts 1:1 into that photo on the mobile page.
        (K(73), (0.00, -7.60, 3.30), (0.00, -0.25, 0.40), 30, "in"),
        (K(75), *END_CAM, "out")]),
}


def spec(name, mode, extra=None):
    t0, t1, cam = SHOTS[name]
    final = mode == "final"
    sp = {"base": BASE, "parts": parts_at(t0), "camera": {"sensor": 20.25, "keys": _cam(cam, t0)},
          "seconds": round(t1 - t0 + 3 / 15, 4), "fps": 15, "res": "1080x1920",  # +3 tail frames (lesson: 15 fps freeze)
          "res_pct": 75 if final else 30, "samples": 12 if final else 6,
          "out": f"{OUT}/{'final' if final else 'preview'}/{name}"}
    sp.update(extra or {})
    os.makedirs(SPECS, exist_ok=True)
    p = f"{SPECS}/{name}_{mode}.json"
    json.dump(sp, open(p, "w"), indent=1)
    return p


if __name__ == "__main__":
    mode = sys.argv[1]
    for n in sys.argv[2:] or list(SHOTS):
        print(spec(n, mode))
