"""Write the WRX VA shot JSONs (format: tools/shots.py). Frame = ive prep of car_4mm (m): nose +X (2.32),
tail -X (-2.29), left side +Y, ground z 0, roof 1.445. az = deg around +Z from +X (0 = at the nose, 90 = left).
    python projects/subaru-wrx-va/tools/plan.py   -> projects/subaru-wrx-va/shots/*.json
Durations are nominal; the cut list retimes each clip to the music (small setpts stretches on smooth moves).
"""
import json
import os

B = "/home/user/media/subaru-wrx-va/blend"
OUT = os.path.join(os.path.dirname(__file__), "..", "shots")
CAR4 = {"blend": f"{B}/car.blend"}
CAR2 = {"blend": f"{B}/car_2mm.blend"}


def K(t, loc=(0, 0, 0), rot=(0, 0, 0), ease=None):
    k = {"t": t, "loc": list(loc), "rot": list(rot)}
    if ease:
        k["ease"] = ease
    return k


def part(name, out_loc, rot=(0, 0, 0), t_out=(0.04, 0.24), t_back=(0.62, 0.82), spin=(0.26, 0.56)):
    """separate (ease_out) -> hold/spin -> reassemble (ease_in) -> rest; offsets in m, rot deg about the part centre."""
    a, b = t_out
    s0, s1 = spin
    c, d = t_back
    return {"blend": f"{B}/{name}.blend", "keys": [
        K(0), K(a), K(b, out_loc, ease="ease_out"), K(s0, out_loc), K(s1, out_loc, rot), K(c, out_loc, rot),
        K(d, (0, 0, 0), (0, 0, 0), ease="ease_in"), K(1.0)]}


SHOTS = {
    # 1. slow front 3/4 turntable, low, crops into the car (lesson: tight in 9:16)
    "s01_front34": {"seconds": 5.0, "lens": 32, "ease": "sine", "objects": [CAR4], "cam": [
        {"t": 0, "az": 22, "dist": 3.0, "z": 0.7, "look": [1.1, 0, 0.55]},
        {"t": 1, "az": 55, "dist": 3.2, "z": 0.9, "look": [0.8, 0, 0.55]}]},
    # 2. rear 3/4 orbit, STI wing against black
    "s02_rear34": {"seconds": 5.0, "lens": 32, "ease": "sine", "objects": [CAR4], "cam": [
        {"t": 0, "az": -155, "dist": 3.1, "z": 1.0, "look": [-1.0, 0, 0.7]},
        {"t": 1, "az": -122, "dist": 3.3, "z": 1.3, "look": [-0.8, 0, 0.65]}]},
    # 3-5. extreme close-ups (2 mm scan)
    "s03_wheel": {"seconds": 2.5, "lens": 50, "ease": "sine", "objects": [CAR2], "cam": [
        {"t": 0, "az": 62, "dist": 2.0, "z": 0.45, "look": [1.32, 0.78, 0.36]},
        {"t": 1, "az": 92, "dist": 1.8, "z": 0.40, "look": [1.32, 0.78, 0.34]}]},
    "s04_front": {"seconds": 2.5, "lens": 45, "ease": "sine", "objects": [CAR2], "cam": [
        {"t": 0, "az": 8, "dist": 1.75, "z": 0.75, "look": [2.05, 0.45, 0.55]},
        {"t": 1, "az": 32, "dist": 1.6, "z": 0.85, "look": [2.0, 0.55, 0.6]}]},
    "s05_wing": {"seconds": 2.5, "lens": 45, "ease": "sine", "objects": [CAR2], "cam": [
        {"t": 0, "az": -128, "dist": 1.8, "z": 1.55, "look": [-1.8, 0.55, 1.2]},
        {"t": 1, "az": -100, "dist": 2.1, "z": 1.5, "look": [-1.8, 0.45, 1.15]}]},
    # 6. hood open (captured state) - high front 3/4 craning over the engine bay
    "s06_hood": {"seconds": 3.75, "lens": 30, "ease": "sine", "objects": [{"blend": f"{B}/hood2_4mm.blend"}], "cam": [
        {"t": 0, "az": 40, "dist": 2.9, "z": 1.5, "look": [1.4, 0, 0.8]},
        {"t": 1, "az": 18, "dist": 2.6, "z": 2.1, "look": [1.4, 0, 0.75]}]},
    # 7. trunk open - high rear 3/4 push
    "s07_trunk": {"seconds": 3.75, "lens": 30, "ease": "sine", "objects": [{"blend": f"{B}/trunk_4mm.blend"}], "cam": [
        {"t": 0, "az": -162, "dist": 2.7, "z": 1.8, "look": [-1.7, 0, 1.0]},
        {"t": 1, "az": -136, "dist": 2.4, "z": 2.1, "look": [-1.7, 0, 0.95]}]},
    # 8. rise to straight overhead (nose up the frame), slow spin
    "s08_topdown": {"seconds": 5.0, "lens": 30, "ease": "sine", "objects": [CAR4], "cam": [
        {"t": 0, "az": -120, "dist": 4.0, "z": 3.4, "look": [0, 0, 0.5]},
        {"t": 0.65, "pos": [0.0, 0.001, 6.4], "look": [0, 0, 0.5], "up": [1, 0, 0]},
        {"t": 1, "pos": [0.0, 0.001, 6.1], "look": [0, 0, 0.5], "up": [1, 0.18, 0]}]},
    # 9. exploded view: panels separate in layers ABOVE the car (Temerario, portrait-friendly), bumper turns about Z, reassemble
    "s09_explode": {"seconds": 5.439, "lens": 30, "ease": "sine", "objects": [
        # timed to the track (b46 = 20.907 s start, 0.4533 s beats): out by b48 (0.167), bumper turns b48-b51,
        # everything locks home on the strong b54 kick (24.533 s = 0.667), assembled car holds to the logo at b58
        {"blend": f"{B}/explode_base_4mm.blend"},
        part("fbump_nofog_2mm", (-0.45, 0, 1.65), (0, 0, 180), t_out=(0.0, 0.167), spin=(0.18, 0.47), t_back=(0.5, 0.667)),
        part("fogL_2mm", (0.15, 0.3, 0.95), t_out=(0.03, 0.18), spin=(0.2, 0.2), t_back=(0.52, 0.667)),
        part("fogR_2mm", (0.15, -0.3, 0.95), t_out=(0.03, 0.18), spin=(0.2, 0.2), t_back=(0.52, 0.667)),
        part("scoop_2mm", (-0.15, 0, 0.5), t_out=(0.02, 0.17), spin=(0.2, 0.2), t_back=(0.54, 0.667)),
        part("wingfull_2mm", (-0.2, 0, 0.85), t_out=(0.05, 0.19), spin=(0.21, 0.21), t_back=(0.54, 0.667)),
    ], "cam": [
        {"t": 0, "az": 42, "dist": 4.7, "z": 2.1, "look": [0.5, 0, 1.25]},
        {"t": 1, "az": 70, "dist": 4.9, "z": 2.4, "look": [0.3, 0, 1.2]}]},
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, v in SHOTS.items():
        json.dump(v, open(os.path.join(OUT, k + ".json"), "w"), indent=1)
    print(len(SHOTS), "shots,", sum(v["seconds"] for v in SHOTS.values()), "s")
