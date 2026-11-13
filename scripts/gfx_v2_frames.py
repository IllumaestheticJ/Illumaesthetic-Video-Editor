"""Extract LUT-graded 1920x1080 frames (3 per visible IRL event) from edl_v2.json for HUD corner checks."""
import json, subprocess, sys
from pathlib import Path
P = Path("/home/user/Illumaesthetic-Video-Editor/projects/lexus-is350-speedrun-long")
LUT = "/home/user/Illumaesthetic-Video-Editor/projects/toyota-mr2-spyder-scan-process/grade/fx3a_slog3cine_to_709.cube"
OUT = Path("/home/user/media/work/is350-long/gfx/v2/frames")
d = json.load(open(P / "edl_v2.json"))
for e in d["events"]:
    if e["type"] not in ("irl", "irl_timelapse", "freeze") or not e["hud"].get("visible"):
        continue
    src = e["source"]
    if "FX305" not in src:
        continue
    if "FX30545" in src:
        src = src.replace("/dropbox/", "/dropbox_4k/")
        vf = "scale=1920:1080"  # stored landscape orientation (layout: decoded with -noautorotate)
    else:
        vf = "scale=1920:1080"
    a, b = e["src_in"], e["src_out"]
    for k, p in enumerate((0.1, 0.5, 0.9)):
        t = a + (b - a) * p
        out = OUT / f"{e['id']}_{k}.jpg"
        if out.exists():
            continue
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-noautorotate", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1",
                        "-vf", f"{vf},format=rgb48le,lut3d=file={LUT}:interp=tetrahedral", "-q:v", "3", str(out)], check=True)
print("done")
