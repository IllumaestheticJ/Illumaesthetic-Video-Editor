"""Extended-canvas camera: a source window (x0,y0,w,h px of the solved frame) is scaled to the output WIDTH and centred
vertically on a taller canvas (rest = blurred fill for IRL, real scan for the render). Same focal, wider sensor.
usage: canvascam.py cam_src.json out.json --win x0,y0,w,h [--out 1080,1920] [--dy 0]
prints the scale and the window's y placement for the ffmpeg canvas."""
import json, argparse
ap = argparse.ArgumentParser(); ap.add_argument("cam"); ap.add_argument("out")
ap.add_argument("--win", required=True); ap.add_argument("--out-size", default="1080,1920"); ap.add_argument("--dy", type=float, default=0)
a = ap.parse_args()
c = json.load(open(a.cam)); W0, H0 = c["image_size"]
x0, y0, w, h = map(float, a.win.split(",")); OW, OH = map(int, a.out_size.split(","))
K = OW / w; top = (OH - K * h) / 2 + a.dy
ppx = W0 / 2 - c.get("shift_x", 0) * W0; ppy = H0 / 2 + c.get("shift_y", 0) * W0
px, py = K * (ppx - x0), K * (ppy - y0) + top
fn = c["fx_px"] * K
o = dict(c); o.update({"image_size": [OW, OH], "fx_px": fn, "focal_mm": fn * c["sensor_width_mm"] / OW,
                      "shift_x": (OW / 2 - px) / OW, "shift_y": (py - OH / 2) / OW,
                      "canvas": {"src_win": [x0, y0, w, h], "scale": K, "top": top}})
json.dump(o, open(a.out, "w"), indent=1); print(json.dumps(o["canvas"]))
