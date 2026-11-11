"""Turn a camera solved on a 16:9 landscape frame (W x H) into the camera of a 9:16 crop window.
  python portrait.py cam_land.json x0 cam_out.json [--out-size 1080x1920]
x0 = left edge of the crop window in the landscape frame's pixels (window width = H*9/16).
Focal (mm) is unchanged; sensor width shrinks to the window; the window offset becomes lens shift_x."""
import json, sys
c = json.load(open(sys.argv[1])); x0 = float(sys.argv[2]); out = sys.argv[3]
W, H = c["image_size"]; ow, oh = 1080, 1920
if len(sys.argv) > 5: ow, oh = map(int, sys.argv[5].split("x"))
win = H * 9 / 16; s = oh / H
sensor = c["sensor_width_mm"] * win / W
cx_p = (W / 2 - x0) * s
o = dict(c)
o.update({"image_size": [ow, oh], "sensor_width_mm": sensor, "fx_px": c["fx_px"] * s,
          # scan_render uses sensor_fit HORIZONTAL: Blender shift is a fraction of the image WIDTH (measured: /max(w,h) left 46-121 px errors)
          "shift_x": (ow / 2 - cx_p) / ow,
          "shift_y": c.get("shift_y", 0.0),
          "crop": {"from": sys.argv[1], "x0": x0, "window_w": win, "landscape": [W, H]}})
json.dump(o, open(out, "w"), indent=2); print(out, "sensor", round(sensor, 3), "shift_x", round(o["shift_x"], 4))
