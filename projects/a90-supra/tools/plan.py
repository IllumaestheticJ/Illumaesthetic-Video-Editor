"""Write the A90 shot JSONs (projects/a90-supra/shots/*.json) for tools/shots.py.

96 BPM, bar = 2.5 s. Frame: nose = +X, right side (fender side) = -Y, floor z = 0 (body lowest point;
the car has no wheels). az = camera angle around the look point from +X (az -90 = right side).
    python projects/a90-supra/tools/plan.py
"""
import json
import os

B = "/home/user/media/work/a90/blend/"
OUT = os.path.join(os.path.dirname(__file__), "..", "shots")
BAR = 2.5
CAR = {"blend": B + "car.blend"}
FR = {"blend": B + "fr_2mm.blend"}
RR = {"blend": B + "rr_2mm.blend"}

SHOTS = {
    # bars 1-2: slow front 3/4 turntable, crops into the car (9:16 lesson: tighten by cropping)
    "s01_front34": {"seconds": 2 * BAR, "lens": 32, "ease": "sine", "objects": [CAR],
                    "cam": [{"t": 0, "az": -20, "dist": 3.5, "z": 0.95, "look": [0.75, 0, 0.5]},
                            {"t": 1, "az": -50, "dist": 3.6, "z": 1.15, "look": [0.45, 0, 0.5]}]},
    # bars 3-4: low rear 3/4 orbit toward the side
    "s02_rear34": {"seconds": 2 * BAR, "lens": 30, "ease": "sine", "objects": [CAR],
                   "cam": [{"t": 0, "az": -150, "dist": 3.2, "z": 0.55, "look": [-0.75, 0, 0.5]},
                           {"t": 1, "az": -120, "dist": 3.3, "z": 0.7, "look": [-0.5, 0, 0.5]}]},
    # bar 5: front wheel arch - hub, brake, suspension (no wheels in the scan)
    "s03_arch": {"seconds": BAR, "lens": 35, "ease": "sine", "objects": [FR],
                 "cam": [{"t": 0, "az": -62, "dist": 1.55, "z": 0.62, "look": [1.28, -0.8, 0.36]},
                         {"t": 1, "az": -88, "dist": 1.35, "z": 0.48, "look": [1.18, -0.8, 0.34]}]},
    # bar 6: headlight glide
    "s04_headlight": {"seconds": BAR, "lens": 40, "ease": "sine", "objects": [FR],
                      "cam": [{"t": 0, "az": -25, "dist": 0.78, "z": 0.86, "look": [1.88, -0.62, 0.71]},
                              {"t": 1, "az": -50, "dist": 0.7, "z": 0.8, "look": [1.82, -0.68, 0.71]}]},
    # bar 7: tail light glide
    "s05_taillight": {"seconds": BAR, "lens": 40, "ease": "sine", "objects": [RR],
                      "cam": [{"t": 0, "az": -150, "dist": 1.0, "z": 0.95, "look": [-2.0, -0.6, 0.8]},
                              {"t": 1, "az": -128, "dist": 0.9, "z": 0.9, "look": [-1.98, -0.66, 0.8]}]},
    # bar 8: side glide along the right flank, low, cropping bumpers
    "s06_side": {"seconds": BAR, "lens": 28, "ease": "linear", "objects": [CAR],
                 "cam": [{"t": 0, "pos": [1.0, -2.3, 0.45], "look": [0.6, 0, 0.45]},
                         {"t": 1, "pos": [-0.7, -2.3, 0.5], "look": [-0.9, 0, 0.45]}]},
    # bars 9-10: top-down - rise from high rear 3/4 to straight overhead, nose to the top of frame
    "s07_topdown": {"seconds": 2 * BAR, "lens": 30, "ease": "sine", "objects": [CAR],
                    "cam": [{"t": 0, "az": -140, "dist": 4.6, "z": 3.2, "look": [-0.1, 0, 0.4]},
                            {"t": 0.55, "az": -165, "dist": 2.0, "z": 6.0, "look": [0, 0, 0.4], "up": [0.6, 0, 0.8]},
                            {"t": 1, "az": -180, "dist": 0.02, "z": 7.4, "look": [0, 0, 0.4], "up": [1, 0, 0]}]},
}

# bars 11-13 (7.5 s): exploded view. Out on the hit at 25.0 s (ease_out: fast start), spin to show the
# other face, fly home with ease_in so the panels LAND at t = 2/3 (30.0 s, bar 13 impact), then settle.
LAND = 2 / 3
OFF = 1.0
def part(blend, out, rot, t0=0.0):
    rot = rot if isinstance(rot, list) else [0, 0, rot]
    return {"blend": B + blend, "keys": [
        {"t": t0}, {"t": t0 + 0.2, "loc": out, "ease": "ease_out"},
        {"t": 0.42, "loc": out, "rot": rot},
        {"t": 0.5, "loc": out, "rot": rot},
        {"t": LAND, "loc": [0, 0, 0], "rot": [0, 0, 0], "ease": "ease_in"}]}
# Camera high on the right side looking down ~60 deg, nose to the top of frame (car length along the 9:16
# height). Bumpers tip 90 deg about the car-width axis (Y) so their scanned inner faces look straight up at
# the lens (240SX lesson: flip about the width axis), fender turns 180 about Z; all fly home and land on bar 13.
EX = {"seconds": 3 * BAR, "lens": 30, "ease": "sine",
      "objects": [{"blend": B + "base_explode.blend"},
                  part("fbump.blend", [OFF, -0.1, 0.55], [0, 90, 0]),
                  part("rbump.blend", [-OFF, -0.1, 0.55], [0, -90, 0]),
                  part("fender.blend", [0.1, -0.8, 0.25], 180, 0.03)],
      "cam": [{"t": 0, "az": -115, "dist": 2.5, "z": 3.95, "look": [0, -0.1, 0.3], "up": [1, 0, 0]},
              {"t": 1, "az": -62, "dist": 2.3, "z": 3.6, "look": [0, -0.1, 0.3], "up": [1, 0, 0]}]}
SHOTS["s08_explode"] = EX

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    t = 0.0
    for k, v in SHOTS.items():
        json.dump(v, open(os.path.join(OUT, k + ".json"), "w"), indent=1)
        print(f"{k:16s} {t:6.2f} -> {t + v['seconds']:6.2f} s")
        t += v["seconds"]
    print("logo", t, "->", t + 2 * BAR)
