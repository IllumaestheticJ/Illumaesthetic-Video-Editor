"""Camera for a static view of the mod-shop capture, in the Civic's own frame (Z up, nose at -Y, left = +X).

    python projects/gta6-customs/tools/camfit.py M      -> projects/gta6-customs/cam_M.json

What is measured from the frame:
  * focal length and pitch from the room's vanishing points (tools/vps.py): f = 1757 px on 2560 for every
    view (the game keeps one field of view), horizon row per view, no roll.
  * where the game car's wheels touch the floor (picked on a zoomed, gridded crop).
What is assumed: the game car's wheelbase (2.95 m, a 1970 El Camino / Ranchero; the tyre radius that follows,
0.33 m, is right for that car, which is the check) and that the Civic stands on the same spot: same heading,
wheelbase midpoints together, same centreline.
"""
import json, sys
from pathlib import Path
import numpy as np

SIZE = (2560, 1440); F = 1757.0
CIVIC_MID_Y = -0.02            # wheelbase midpoint of the Civic GLB (nose at -Y)
VIEWS = {
    # horizon row, floor contact of two wheels (front, rear) on the visible side, which side that is,
    # game car: wheelbase and half width at the tyres' outer faces
    "M": dict(horizon=394.0, front=(1229, 1250), rear=(1920, 915), side="left", wheelbase=2.95, half_width=0.90),
    # Rear view (Spoiler screen): no wheel is visible, so the game car's rear bumper is the reference: its two
    # ends, 1.92 m apart (1970 El Camino width) at 0.50 m above the floor, and a rear overhang of 1.35 m.
    "A": dict(horizon=75.0, bumper=((690, 1160), (1785, 1015)), bumper_width=1.92, bumper_z=0.50, wheelbase=2.95, rear_overhang=1.35),
}


def fit(v, shift=(0.0, 0.0)):
    c = np.array(SIZE) / 2; pitch = np.arctan((c[1] - v["horizon"]) / F)
    up = np.array([0, -np.cos(pitch), -np.sin(pitch)])          # world up in camera coords (x right, y down, z forward)
    ray = lambda p: np.array([(p[0] - c[0]) / F, (p[1] - c[1]) / F, 1.0])
    hit = lambda p: ray(p) * (-1.0 / (ray(p) @ up))             # floor point for camera height 1
    if "bumper" in v:                                           # seen from behind: left end, right end of the rear bumper
        bl, br = ray(v["bumper"][0]), ray(v["bumper"][1])
        bl, br = bl * (-1.0 / (bl @ up)), br * (-1.0 / (br @ up))       # on a plane 1 below the camera
        k = v["bumper_width"] / np.linalg.norm(bl - br)                   # = camera height above the bumper
        h = k + v["bumper_z"]
        bl, br = bl * k, br * k
        left = (bl - br) / np.linalg.norm(bl - br)
        u = np.cross(left, up)                                            # forward = left x up
        tail = (bl + br) / 2 + up * (-v["bumper_z"])                      # floor point under the middle of the bumper
        centre = tail + u * (v["rear_overhang"] + v["wheelbase"] / 2)     # wheelbase midpoint of the game car
    else:
        gf, gr = hit(v["front"]), hit(v["rear"])
        h = v["wheelbase"] / np.linalg.norm(gf - gr)            # camera height in metres
        gf, gr = gf * h, gr * h
        u = (gf - gr) / np.linalg.norm(gf - gr)                 # car's forward
        left = np.cross(up, u)
        centre = (gf + gr) / 2 + left * (-v["half_width"] if v["side"] == "left" else v["half_width"])
    centre = centre + u * shift[0] + left * shift[1]            # optional nudge of the Civic: forward, left (m)
    R_cw = np.stack([left, -u, up], 1)                          # world axes (X left, Y back, Z up) in camera coords
    origin_c = centre - R_cw @ np.array([0, CIVIC_MID_Y, 0])    # Civic origin in camera coords
    R_wc = R_cw.T
    loc = R_wc @ (-origin_c)
    M = np.stack([R_wc @ [1, 0, 0], R_wc @ [0, -1, 0], R_wc @ [0, 0, -1]], 1)   # Blender camera axes in world
    return {"image_size": list(SIZE), "fx_px": F, "focal_mm": 36.0 * F / SIZE[0], "sensor_width_mm": 36.0, "shift_x": 0.0, "shift_y": 0.0,
            "blender": {"location": loc.round(5).tolist(), "rotation_matrix": M.round(8).tolist()},
            "notes": {"camera_height_m": round(float(h), 3), "pitch_deg": round(float(np.degrees(pitch)), 2),
                      "distance_to_car_m": round(float(np.linalg.norm(origin_c)), 2)}}


if __name__ == "__main__":
    name = sys.argv[1]; shift = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (0.0, 0.0)
    cam = fit(VIEWS[name], shift)
    out = Path(__file__).resolve().parents[1] / f"cam_{name}.json"
    json.dump(cam, open(out, "w"), indent=1); print(out, cam["notes"], cam["blender"]["location"])
