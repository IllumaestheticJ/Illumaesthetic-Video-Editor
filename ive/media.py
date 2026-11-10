"""ffmpeg/ffprobe helpers: probing, exact frame grabs, scene detection, contact sheets."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], capture: bool = False) -> str:
    r = subprocess.run(cmd, check=False, text=True, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"command failed ({r.returncode}): {' '.join(cmd)}\n{r.stderr[-3000:]}")
    return r.stdout + (r.stderr if capture else "")


def probe(path: str) -> dict:
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    d = json.loads(out)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    info = {"path": path, "duration": float(d["format"].get("duration", 0)), "has_audio": any(s["codec_type"] == "audio" for s in d["streams"])}
    if v:
        num, den = (int(x) for x in v.get("avg_frame_rate", "0/1").split("/"))
        rot = 0
        for sd in v.get("side_data_list", []):
            rot = int(sd.get("rotation", rot))
        info.update(
            width=v["width"], height=v["height"], fps=(num / den if den else 0), codec=v["codec_name"],
            pix_fmt=v.get("pix_fmt"), color_transfer=v.get("color_transfer"), color_primaries=v.get("color_primaries"),
            bit_depth=v.get("bits_per_raw_sample"), rotation=rot,
            log_or_hdr=v.get("color_transfer") in ("arib-std-b67", "smpte2084") or "log" in json.dumps(d).lower(),
            nb_frames=int(v.get("nb_frames", 0) or 0),
        )
    return info


def grab_frame(video: str, t: float, out: str) -> str:
    """Frame-accurate still (seek after input) at time t seconds."""
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-ss", f"{t:.4f}", "-frames:v", "1", out])
    return out


def scenes(video: str, threshold: float = 0.3) -> list[float]:
    """Timestamps of hard cuts / big changes inside a clip (useful on long b-roll dumps)."""
    out = run(["ffmpeg", "-v", "info", "-i", video, "-vf", f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"], capture=True)
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", out)]


def contact_sheet(video: str, out: str, cols: int = 6, rows: int = 4, width: int = 320) -> str:
    """Grid of evenly spaced thumbnails with timecodes, for an agent to 'watch' footage."""
    info = probe(video)
    n = cols * rows
    step = max(info["duration"] / n, 0.04)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    vf = (f"fps=1/{step:.4f},scale={width}:-2,"
          f"drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6,"
          f"tile={cols}x{rows}")
    try:
        run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vf", vf, "-frames:v", "1", out])
    except RuntimeError:  # drawtext needs fontconfig; fall back without timecodes
        run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vf", f"fps=1/{step:.4f},scale={width}:-2,tile={cols}x{rows}", "-frames:v", "1", out])
    return out


def blender_cmd() -> list[str] | None:
    """Prefer a real Blender binary; fall back to the `bpy` pip module."""
    b = shutil.which("blender")
    if b:
        return [b, "-b", "-P"]
    try:
        import importlib.util

        if importlib.util.find_spec("bpy"):
            import sys

            return [sys.executable]
    except Exception:
        pass
    return None


def blender(script: str, args: list[str]) -> str:
    base = blender_cmd()
    if base is None:
        raise RuntimeError("Blender not found. Install Blender 4.2+ (on PATH as `blender`) or `pip install bpy`.")
    cmd = base + [script] + (["--"] if base[-1] == "-P" else []) + args
    return run(cmd, capture=True)


TONEMAP_HLG_RGB = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
                   "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=pc,format=rgb24")


def grab_frame_sdr(video: str, t: float, out: str) -> str:
    """Still for camera solving / QA. iPhone HLG is tonemapped so it matches the edit."""
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    info = probe(video)
    vf = ["-vf", TONEMAP_HLG_RGB] if info.get("color_transfer") in ("arib-std-b67", "smpte2084") else []
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.4f}", "-i", video, "-frames:v", "1", *vf, out])
    return out


def strip(video: str, times: list[float], out: str, height: int = 480) -> str:
    """Labelled frame strip at given times (ffmpeg decode - works on any codec). Use it to
    review every cut: e.g. times = [cut - 1/fps, cut, cut + 1/fps] for each cut."""
    import cv2
    import numpy as np
    import tempfile

    tiles = []
    with tempfile.TemporaryDirectory() as td:
        for k, t in enumerate(times):
            p = f"{td}/{k}.png"
            run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.4f}", "-i", video, "-frames:v", "1", "-vf", f"scale=-2:{height}", p])
            im = cv2.imread(p)
            if im is None:
                continue
            cv2.putText(im, f"{t:.2f}s", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            tiles.append(im)
    cv2.imwrite(out, np.hstack(tiles))
    return out
