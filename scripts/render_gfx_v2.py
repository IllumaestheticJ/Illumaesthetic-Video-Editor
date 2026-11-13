#!/usr/bin/env python3
"""Render v2 graphics from the props written by gen_gfx_v2.py.

  python scripts/render_gfx_v2.py [--only HUD,G03_v2,...] [--out DIR] [--concurrency 2]

HUD_v2.mov  : 1920x270 ProRes 4444 alpha, crop of the TOP of the frame (composite at x=0,y=0), whole timeline.
<cue>.mov   : 1920x1080 ProRes 4444 alpha, timeline start = cue "in" in gfx_v2_cues_props.json.
<cue>.mp4   : opaque black cards (H.264 crf 12).
"""
import argparse, glob, json, subprocess, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--project", default="projects/lexus-is350-speedrun-long")
ap.add_argument("--ver", default="v2")
ap.add_argument("--out", default=None)
ap.add_argument("--only", default=None)
ap.add_argument("--concurrency", default="2")
a = ap.parse_args()
P = REPO / a.project
OUT = Path(a.out or f"/home/user/media/work/is350-long/gfx/{a.ver}")
OUT.mkdir(parents=True, exist_ok=True)
hs = sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"))
B = [f"--browser-executable={hs[-1]}"] if hs else []
only = set(a.only.split(",")) if a.only else None
PRORES = ["--codec=prores", "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png"]
H264 = ["--codec=h264", "--crf=12", "--image-format=png"]


def render(comp, out, props, fmt):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(props, f)
    subprocess.run(["npx", "remotion", "render", comp, str(out), f"--props={f.name}", *fmt, f"--concurrency={a.concurrency}", *B], cwd=REPO / "remotion", check=True)


if only is None or "HUD" in only:
    render("HudV2", OUT / f"HUD_{a.ver}.mov", json.loads((P / f"gfx_{a.ver}_hud_props.json").read_text()), PRORES)
for c in json.loads((P / f"gfx_{a.ver}_cues_props.json").read_text()):
    if only is not None and c["cue"] not in only:
        continue
    render(c["comp"], OUT / c["file"], c["props"], PRORES if c["alpha"] else H264)
print("done")
