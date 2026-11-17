"""Fit the take's last frame to Ron's render 7 as it appears in the 9:16 frame (car scaled to 940 px wide, centred,
car centre at y=1000): iterate lens + shift on a workbench silhouette (car + kit, no rain/mascots).
    python fit_end.py   -> kit/end_cam.json
Render-7 car bbox on the 1920 square (honda-civic-11 v5, re-checked): x 430-1610, y 713-1172.
"""
import json, subprocess, numpy as np
from PIL import Image
M = "/home/user/media/bf-civic-parts-rain"; T = "/home/user/Illumaesthetic-Video-Editor/projects/bf-civic-parts-rain/tools/take.py"
s = 940 / 1180; TW, TCX, TCY = 940, 540, 1000; TH = 459 * s
end = {"lens": 105.0, "shift_x": 0.0, "shift_y": 0.0, "dist_scale": 1.0}
for it in range(4):
    json.dump(end, open(f"{M}/kit/end_cam.json", "w"))
    subprocess.run(["blender", "-b", "-P", T, "--", "--out", f"{M}/renders/fit", "--engine", "workbench", "--res-pct", "25",
                    "--rain", "0", "--nochars", "--mblur", "0", "--still", "487", "--end-cam", f"{M}/kit/end_cam.json"],
                   capture_output=True)
    a = np.asarray(Image.open(f"{M}/renders/fit/still_0487.png").convert("RGB")).astype(int)
    bg = a[0, 0]; m = np.abs(a - bg).sum(2) > 30
    ys, xs = np.where(m); sc_ = 1080 / a.shape[1]
    x0, x1, y0, y1 = xs.min() * sc_, xs.max() * sc_, ys.min() * sc_, ys.max() * sc_
    w, cx, cy = x1 - x0, (x0 + x1) / 2, (y0 + y1) / 2
    print(f"it{it}: lens {end['lens']:.1f} shift {end['shift_x']:.3f},{end['shift_y']:.3f} -> bbox w {w:.0f} h {y1-y0:.0f} (target {TW} x {TH:.0f}) centre {cx:.0f},{cy:.0f}")
    k = TW / w
    # zoom about the frame centre, then shift (units of frame width; +x moves the image left, +y moves it down)
    ncx, ncy = 540 + (cx - 540) * k, 960 + (cy - 960) * k
    end["lens"] *= k
    end["shift_x"] = end["shift_x"] * k + (ncx - TCX) / 1080
    end["shift_y"] = end["shift_y"] * k + (TCY - ncy) / 1080
json.dump(end, open(f"{M}/kit/end_cam.json", "w")); print("END", end)
