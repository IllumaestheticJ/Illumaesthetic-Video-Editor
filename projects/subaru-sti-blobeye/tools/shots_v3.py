"""v3 shot specs: every shot shows ONE scan file exactly as captured - no carved panels, no composites, no flying parts.

    python projects/subaru-sti-blobeye/tools/shots_v3.py preview|final [shot ...]

User on v2: "a bunch of improperly cut and hallucinated scans" (panels carved out of the full car floated with ragged
edges; openings were patchworks of state scans). v3 instead does 1:1 STATE SWAPS: the camera move continues across a hard
cut from the full-car scan (x_a) to the registered removed-state scan (x_b), each rendered alone.

Frame: prepped metres, nose -Y, car's right -X, ground z 0. Plate kept as scanned (user rule: flatten only on the IS300).
"""
import json
import os
import sys

P = "/home/user/media/work/sti/prep"
OUT = "/home/user/media/work/sti/renders"
SPECS = "/home/user/media/work/sti/specs"

CAR = f"{P}/car4.blend"                    # Blobeye Full Car.stl, 4 mm
REAR = f"{P}/rear.blend"                   # Rear Wing data.stl (rear captured with the wing off)
SILL = f"{P}/sideskirt_removed.blend"      # Sideskirt removed.stl
HOODOFF = f"{P}/hood_removed_r.blend"      # Front bumper/hood removed.stl
BAY = f"{P}/engine_bay.blend"              # GD Scan Engine Bay.stl
BUMPOFF = f"{P}/bumper_removed_r.blend"    # Front bumper/bumper removed.stl
ALLOFF = f"{P}/all_removed_r.blend"        # Front bumper/all removed.stl


def cam(t, loc, tgt, focal, ease="lin"):
    return {"t": t, "loc": list(loc), "target": list(tgt), "focal": focal, "ease": ease}


F = 1 / 30
# name: (base, seconds, camera keys in shot-local seconds). x_a ends where x_b starts (same camera = 1:1 state swap).
# The swap happens once the camera is tight enough that the state scan fills the frame (preview 1: fragments sat small
# with their capture boundary showing). Skirt (thin strip) and 'hood removed' (scattered islands) are not shown.
R0, R1, R2 = ((1.35, 4.55, 1.95), (0.15, 1.95, 1.30), 30), ((0.90, 3.60, 2.00), (0.05, 1.95, 0.86), 50), ((0.45, 3.20, 2.10), (0.0, 1.95, 0.78), 55)
H0, H1, H2 = ((-1.05, -4.30, 1.80), (0, -1.55, 0.85), 35), ((-0.25, -2.90, 2.25), (0, -1.65, 0.75), 38), ((0.15, -2.50, 2.00), (0, -1.60, 0.65), 42)
B0, B1, B2, B3 = (((1.20, -4.70, 0.55), (0.05, -2.10, 0.48), 35), ((0.55, -3.60, 0.55), (0.02, -2.03, 0.44), 37),
                  ((0.30, -3.20, 0.55), (0, -2.00, 0.42), 38), ((-0.25, -3.10, 0.48), (-0.35, -1.97, 0.36), 38))
SHOTS = {
    "O1_open": (CAR, 97 * F, [cam(0, (1.916, 5.812, 0.95), (0, 0.55, 0.65), 30), cam(97 * F, (3.682, 4.262, 1.35), (0, 0.45, 0.65), 30, "out2")]),
    "R_a": (CAR, 60 * F, [cam(0, *R0), cam(60 * F, *R1)]),
    "R_b": (REAR, 84 * F, [cam(0, *R1), cam(84 * F, *R2, "out")]),
    "H_a": (CAR, 60 * F, [cam(0, *H0), cam(60 * F, *H1)]),
    "E_bay": (BAY, 168 * F, [cam(0, *H1), cam(168 * F, *H2, "out")]),
    "B_a": (CAR, 48 * F, [cam(0, *B0), cam(48 * F, *B1)]),
    "B_b": (BUMPOFF, 144 * F, [cam(0, *B1), cam(144 * F, *B2, "out")]),
    "B_c": (ALLOFF, 144 * F, [cam(0, *B2), cam(144 * F, *B3, "inout")]),
}


def spec(name, mode):
    base, T, keys = SHOTS[name]
    sp = {"base": [base], "camera": {"keys": keys}, "seconds": T, "fps": 15, "res": "1080x1920",
          "out": f"{OUT}/{mode}/{name}", "exposure": -0.5, "persistent": True, "parts": []}
    if mode == "preview":
        sp.update(res_pct=30, samples=8, frames=["first", "mid", "last"])
    else:
        sp.update(res_pct=75, samples=12)
    return sp


if __name__ == "__main__":
    mode = sys.argv[1]
    os.makedirs(SPECS, exist_ok=True)
    for n in sys.argv[2:] or list(SHOTS):
        p = f"{SPECS}/{mode}_{n}.json"
        json.dump(spec(n, mode), open(p, "w"), indent=1)
        print(p)
