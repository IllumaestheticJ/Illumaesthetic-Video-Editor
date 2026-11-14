"""v3 shot specs (director_v3.md): the HertLife time-attack kit replaces every stock panel of the S5 scan.
Reuses v2 renders for the stock part of the reel (s1, s6, s9, s10, s11); this file only adds the kit shots.

    python projects/mazda-rx7-fc/tools/shots_v3.py preview|final [shot ...]

Frame: prepped scan frame (m), front = +Y, car's right = +X, z up. Kit parts: k_*.blend (tools/kitreg.py + kitparts.py,
prepped --like car4.json). Kit look: satin red paint skins + gunmetal aero (the KeyShot design's paint/CF split) over the
silver stock scan, so every replaced panel reads as new.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import P, OUT, SPECS, EXPO, HINGE, K, C  # noqa: E402

RED = [0.36, 0.010, 0.008]   # deeper cherry: 0.50/0.025 rendered salmon-pink under AgX
GUN = [0.06, 0.06, 0.065]
EXPDP = f"{P}/comp_explode_dp.blend"
HP = HINGE["p"]; HO = HINGE["open_deg"]
SECS = 5.533  # 80 frames to the cut + 3 spare
UP = 5.00     # parts start fully above the frame (3.6 peeked in at the top with the wider c6 camera)


def kp(name, color, keys=None, pivot=None):
    d = {"blend": f"{P}/{name}.blend", "paint": color, "keys": keys or [K(0)]}
    if pivot:
        d["pivot"] = pivot
    return d


def stock(name, keys=None, pivot=None):
    d = {"blend": f"{P}/{name}.blend", "keys": keys or [K(0)]}
    if pivot:
        d["pivot"] = pivot
    return d


FRONT_KIT = [kp("k_lights", GUN), kp("k_fbumper", RED), kp("k_splitter", GUN), kp("k_canards_l", GUN),
             kp("k_canards_r", GUN), kp("k_hood", RED, pivot=HP)]
SIDE_KIT = [kp("k_side_l", RED), kp("k_side_r", RED), kp("k_sidesplit_l", GUN), kp("k_sidesplit_r", GUN)]
REAR_KIT = [kp("k_rbumper", RED), kp("k_diffuser", GUN), kp("k_exhaust", GUN), kp("k_wing", GUN)]

SHOTS = {}
# c6: front kit goes on - lights, bumper, splitter, canards drop in front of the nose and slide back onto the mounts,
# vented hood comes down open on the stock hinge and closes on the 20.667 snare
SHOTS["k_front"] = {"base": [EXPDP], "parts": [
    stock("rbumper"),
    # headlights are mounted in the kit bumper: they travel with it as one assembly (pathcheck: sliding the bumper back
    # over separately-landed housings put 8.6 % of it through them)
    kp("k_lights", GUN, [K(0, (0, 0.60, UP)), K(0.667, (0, 0.60, UP), ease="lin"), K(1.333, (0, 0.60, 0), ease="out"), K(2.0)]),
    kp("k_fbumper", RED, [K(0, (0, 0.60, UP)), K(0.667, (0, 0.60, UP), ease="lin"), K(1.333, (0, 0.60, 0), ease="out"), K(2.0)]),
    kp("k_splitter", GUN, [K(0, (0, 0.70, UP)), K(1.333, (0, 0.70, UP), ease="lin"), K(2.0, (0, 0.70, -0.15), ease="out"),
                           K(2.4, (0, 0, -0.15)), K(2.667, ease="out")]),
    kp("k_canards_r", GUN, [K(0, (1.00, 0.40, UP)), K(2.0, (1.00, 0.40, UP), ease="lin"), K(2.5, (1.00, 0.40, 0), ease="out"), K(3.333)]),
    kp("k_canards_l", GUN, [K(0, (-1.00, 0.40, UP)), K(2.0, (-1.00, 0.40, UP), ease="lin"), K(2.5, (-1.00, 0.40, 0), ease="out"), K(3.333)]),
    kp("k_hood", RED, [K(0, (0, 0, UP), (HO, 0, 0)), K(2.667, (0, 0, UP), (HO, 0, 0), "lin"), K(3.667, (0, 0, 0), (HO, 0, 0), "out"),
                       K(4.667), K(SECS, ease="lin")], pivot=HP)],
    "cam": [C(0, (-3.70, 6.60, 2.10), (0.30, 1.25, 0.55), 30), C(SECS, (-2.90, 6.30, 2.70), (0.30, 1.30, 0.55), 30)]}
# c7: both overfender skins + side splitters come in along +-X; the car widens (high front-centre view)
SHOTS["k_sides"] = {"base": [EXPDP], "parts": [stock("rbumper")] + FRONT_KIT + [
    kp("k_sidesplit_r", GUN, [K(0, (1.60, 0, 0)), K(0.667, (1.60, 0, 0), ease="lin"), K(2.0)]),
    kp("k_sidesplit_l", GUN, [K(0, (-1.60, 0, 0)), K(0.667, (-1.60, 0, 0), ease="lin"), K(2.0)]),
    kp("k_side_r", RED, [K(0, (1.90, 0, 0)), K(2.0, (1.90, 0, 0), ease="lin"), K(3.333), K(SECS, ease="lin")]),
    kp("k_side_l", RED, [K(0, (-1.90, 0, 0)), K(2.0, (-1.90, 0, 0), ease="lin"), K(3.333), K(SECS, ease="lin")])],
    "cam": [C(0, (0.0, 6.40, 5.40), (0.0, -0.30, 0.50), 50), C(SECS, (0.45, 5.90, 5.00), (0.0, -0.35, 0.50), 50)]}
# c8: stock rear bumper off (outer skin -> translate), push onto the rear crash beam + mounts (Rear Bumper Removed)
CAM8_END = C(SECS, (0.30, -5.65, 0.95), (0.05, -2.05, 0.66), 30, "lin")   # v3 final: wider + centred (left rear corner was cut)
SHOTS["k_rbumper_off"] = {"base": [EXPDP], "parts": FRONT_KIT + SIDE_KIT + [
    stock("rbumper", [K(0), K(0.667, ease="lin"), K(1.333, (0, -0.60, 0), ease="out"), K(2.0, (0.10, -1.30, -3.20)),
                      K(SECS, (0.10, -1.32, -3.25), ease="lin")   # parks far below: -1.8 still showed at the bottom after the 94 % pad])],
    "cam": [C(0, (2.60, -4.60, 1.15), (0.10, -1.55, 0.72)), C(1.333, (2.35, -4.55, 1.05), (0.20, -1.75, 0.70)),
            C(3.333, (0.55, -5.30, 0.92), (0.10, -2.05, 0.68)), CAM8_END]}
# c9: rear kit on - bumper and diffuser slide in from below-behind, tips forward, GT wing drops onto the hatch mounts
SHOTS["k_rear"] = {"base": [EXPDP], "parts": FRONT_KIT + SIDE_KIT + [
    kp("k_rbumper", RED, [K(0, (0.10, -1.30, -3.20)), K(1.333, (0, -0.60, 0), ease="out"), K(2.0)]),
    kp("k_diffuser", GUN, [K(0, (0, -1.00, -3.20)), K(2.0, (0, -1.00, -3.20), ease="lin"), K(2.667, (0, 0, -0.35), ease="out"), K(3.333)]),
    kp("k_exhaust", GUN, [K(0, (0, -1.00, -3.20)), K(2.667, (0, -1.00, -3.20), ease="lin"), K(3.333, (0, -0.45, 0), ease="out"), K(4.0)]),
    kp("k_wing", GUN, [K(0, (0, 0, 3.40)), K(3.333, (0, 0, 3.40), ease="lin"), K(4.667), K(SECS, ease="lin")])],
    "cam": [dict(CAM8_END, t=0), C(2.0, (2.10, -5.00, 1.60), (0.15, -1.60, 0.72)), C(4.667, (2.90, -5.40, 2.30), (0.05, -1.20, 0.78)),
            C(SECS, (2.90, -5.40, 2.30), (0.05, -1.20, 0.78), ease="lin")]}
# c10: the finished widebody - rear-left orbit (never the opener's low front-right), ends near the listing viewer's
# rear-left 3/4 so the CTA dissolve into the phone reads
SHOTS["k_reveal"] = {"base": [EXPDP], "parts": FRONT_KIT + SIDE_KIT + REAR_KIT,
    "cam": [C(0, (-2.05, -7.60, 1.30), (0, -0.10, 0.60), 32), C(5.067, (-5.65, -5.75, 2.45), (0, -0.10, 0.55), 30),
            C(SECS, (-5.65, -5.75, 2.45), (0, -0.10, 0.55), 30, "lin")]}

# CTA: the listing's own scan (2025 'FC3S Full Car', stock, mesh wheels) in silver, a short orbit that ENDS on the
# listing 360 viewer's solved camera (tools/solve_listing.py, IoU 0.959) so cta_card.py --map shrinks it 1:1 onto the phone
LC = json.load(open("/home/user/media/work/rx7/cta/listing_cam.json"))
CTA_F = 24.0   # 32 mm cut the car's rear at the portrait frame edge (overlay vs the listing)
def lcam(da, t, ease="inout"):
    import math
    a, e, d = math.radians(LC["a"] + da), math.radians(LC["e"]), LC["d"]; c = LC["target"]
    loc = [c[0] + d * math.cos(e) * math.sin(a), c[1] - d * math.cos(e) * math.cos(a), c[2] + d * math.sin(e)]
    return {"t": t, "loc": loc, "target": c, "focal": CTA_F, "ease": ease}
SHOTS["cta_scan"] = {"base": [f"{P}/car2025.blend"], "parts": [], "cam": [lcam(-22, 0, "lin"), lcam(0, 1.333, "out")], "secs": 1.4}


def spec(name, mode):
    s = SHOTS[name]
    d = {"base": s["base"], "parts": s["parts"], "camera": {"keys": s["cam"], "sensor": 20.25},
         "seconds": s.get("secs", SECS), "fps": 15, "res": "1080x1920", "exposure": EXPO}
    if mode == "preview":
        d.update(res_pct=30, samples=8, frames=[1, 20, 30, 40, 50, 60, 70, 81], out=f"{OUT}/preview/{name}")
    else:
        d.update(res_pct=75, samples=12, out=f"{OUT}/{name}")
    return d


if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(SPECS, exist_ok=True)
    for n in sys.argv[2:] or list(SHOTS):
        p = f"{SPECS}/{mode}_{n}.json"
        json.dump(spec(n, mode), open(p, "w"), indent=1)
        print(p)
