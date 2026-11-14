"""Render the Remotion ScanHUD composition (remotion/) as transparent ProRes 4444."""
from __future__ import annotations

import glob
import os
import shutil
import subprocess
from pathlib import Path

REMOTION = Path(__file__).resolve().parent.parent / "remotion"


def _browser() -> list[str]:
    hs = sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"))
    return [f"--browser-executable={hs[-1]}"] if hs else []


def render_hud(overlay_json: str, out: str, comp: str = "ScanHUD") -> str:
    """ScanHUD / PromoCaption -> transparent ProRes 4444 overlay; any other composition (e.g. WebZoom) -> opaque H.264 clip."""
    if not (REMOTION / "node_modules").exists():
        subprocess.run(["npm", "ci"], cwd=REMOTION, check=True)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if comp in ("ScanHUD", "PromoCaption"):
        fmt = ["--codec=prores", "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png"]
    else:
        fmt = ["--codec=h264", "--crf=12", "--image-format=jpeg", "--jpeg-quality=95"]
    cmd = ["npx", "remotion", "render", comp, os.path.abspath(out), f"--props={os.path.abspath(overlay_json)}",
           *fmt, "--concurrency=2", *_browser()]
    subprocess.run(cmd, cwd=REMOTION, check=True)
    return out
