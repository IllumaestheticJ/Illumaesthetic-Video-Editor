"""Convert a camera solved in the full FX30 frame (3840x2160, sensor 23.3 mm) to the 9:16 crop
window used by tools/irl.py (same focal; sensor narrowed to the window; principal point moved
with Blender lens shift).

    python tools/crop_cam.py full_cam.json out.json --x0 2160 --y0 498 --zoom 1.3

Blender shift (sensor_fit HORIZONTAL) is in units of the image WIDTH - verified by rendering
full + crop and comparing (mean diff ~0).
"""
import argparse, json
ap = argparse.ArgumentParser()
ap.add_argument("full"); ap.add_argument("out")
ap.add_argument("--x0", type=float, required=True); ap.add_argument("--y0", type=float, default=0)
ap.add_argument("--zoom", type=float, default=1.0)
ap.add_argument("--W", type=int, default=3840); ap.add_argument("--H", type=int, default=2160)
a = ap.parse_args()
c = json.load(open(a.full))
h = a.H / a.zoom; w = h * 9 / 16
ow, oh = 1080, 1920
cx_full = a.W / 2 - c.get("shift_x", 0) * a.W
cy_full = a.H / 2 + c.get("shift_y", 0) * a.W
px = (cx_full - a.x0) / w * ow
py = (cy_full - a.y0) / h * oh
L = ow  # sensor_fit HORIZONTAL: Blender shift is in units of the image width (verified)
out = dict(c)
out["image_size"] = [ow, oh]
out["sensor_width_mm"] = c["sensor_width_mm"] * w / a.W
out["fx_px"] = c["focal_mm"] / out["sensor_width_mm"] * ow
out["shift_x"] = -(px - ow / 2) / L
out["shift_y"] = (py - oh / 2) / L
out["crop_window"] = {"x0": a.x0, "y0": a.y0, "w": w, "h": h, "from": a.full}
json.dump(out, open(a.out, "w"), indent=2)
print(json.dumps({k: out[k] for k in ("focal_mm", "sensor_width_mm", "shift_x", "shift_y")}))
