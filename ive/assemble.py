"""Assemble a timeline from project.yaml into a finished video with ffmpeg.

Timeline items are either clips or transitions (see projects/_template/project.yaml):

  - id: s03
    src: footage/A014.mov          # video file, or a directory of PNGs (Blender render)
    in: 4.20                        # seconds (video only)
    out: 6.10
    speed: 1.0                      # <1 = slow motion (use high-fps sources)
    grade: true                     # apply project LUT (IRL footage only)
    hold_start: 0                   # freeze first frame (s)
    hold_end: 0                     # freeze last frame (s)
  - transition: {type: scanline, duration: 0.6, direction: right, hold: true}

Transition types: cut, dissolve, flash, scanline, ghost, dip
`hold: true` freezes A's last frame and B's first frame for the transition so a 1:1
match pose stays locked while the wipe happens (use for every IRL->scan match cut).
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import tempfile
from pathlib import Path

import yaml

from .media import probe, run

ACCENT_GBR = (217, 255, 0)  # cyan in gbrp plane order (G, B, R)


def _xfade_expr(t: dict) -> tuple[str, str | None]:
    """Return (xfade transition name, custom expr or None). P runs 1 -> 0 over the transition."""
    kind = t.get("type", "cut")
    if kind == "dissolve":
        return "fade", None
    if kind == "dip":
        return "fadeblack", None
    if kind == "flash":
        # hard switch at midpoint with a white bloom peaking on the cut frame
        g = "max(0,1-abs(P-0.5)*6)"
        return "custom", f"clip(if(gt(P,0.5),A,B)+255*{g}*0.85,0,255)"
    if kind == "ghost":
        # scan fades in additively over IRL, then hard switch for the final 10%
        return "custom", "if(lt(P,0.1),B,clip(A*(0.6+0.4*P)+B*(1-P)*0.9,0,255))"
    if kind == "scanline":
        d = t.get("direction", "right")
        w = float(t.get("line_px", 4))
        pos, coord, size = {
            "right": ("(1-P)*W", "X", "W"), "left": ("P*W", "X", "W"),
            "down": ("(1-P)*H", "Y", "H"), "up": ("P*H", "Y", "H"),
        }[d]
        revealed = f"lt({coord},{pos})" if d in ("right", "down") else f"gt({coord},{pos})"
        glow = f"exp(-pow(({coord}-{pos})/{w},2))"
        halo = f"exp(-pow(({coord}-{pos})/{w * 12},2))*0.35"
        g, b, r = ACCENT_GBR
        accent = f"if(eq(PLANE,0),{g},if(eq(PLANE,1),{b},{r}))"
        base = f"if({revealed},B,A)"
        return "custom", f"clip({base}*(1-{glow})+{accent}*{glow}+{accent}*{halo},0,255)"
    return "cut", None


def _clip_inputs(clip: dict, root: Path, fps: float) -> list[str]:
    src = (root / clip["src"]).resolve()
    if src.is_dir():
        files = sorted(glob.glob(str(src / "*.png"))) or sorted(glob.glob(str(src / "*.exr")))
        if not files:
            raise FileNotFoundError(f"no frames in {src}")
        ext = Path(files[0]).suffix
        return ["-framerate", str(clip.get("src_fps", fps)), "-pattern_type", "glob", "-i", str(src / f"*{ext}")]
    if src.suffix.lower() in (".png", ".jpg", ".jpeg", ".tif", ".tiff"):
        return ["-loop", "1", "-framerate", str(fps), "-t", str(clip.get("duration", 2.0)), "-i", str(src)]
    args = []
    if "in" in clip:
        args += ["-ss", str(clip["in"])]
    if "out" in clip:
        args += ["-to", str(clip["out"])]
    return args + ["-i", str(src)]


TONEMAP_HLG = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
               "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


def _needs_tonemap(clip: dict, root: Path) -> bool:
    if "tonemap" in clip:
        return bool(clip["tonemap"])
    src = (root / clip["src"]).resolve()
    if src.is_dir() or src.suffix.lower() in (".png", ".jpg", ".jpeg", ".tif", ".tiff"):
        return False
    return probe(str(src)).get("color_transfer") in ("arib-std-b67", "smpte2084")  # iPhone HLG / HDR10


def _render_clip(clip: dict, root: Path, out: Path, cfg: dict) -> float:
    W, H, fps = cfg["width"], cfg["height"], cfg["fps"]
    vf = [TONEMAP_HLG] if _needs_tonemap(clip, root) else []
    if clip.get("trim_start") or clip.get("trim_end"):  # trims for image sequences (seconds)
        a = float(clip.get("trim_start", 0))
        vf.append(f"trim=start={a}" + (f":end={clip['trim_end']}" if clip.get("trim_end") else "") + ",setpts=PTS-STARTPTS")
    if clip.get("interpolate"):  # low-fps renders -> motion-compensated up to timeline fps
        vf.append(f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1")
    vf += [f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}"]
    sp = float(clip.get("speed", 1.0))
    if sp != 1.0:
        vf.append(f"setpts=PTS/{sp}")
    vf.append(f"fps={fps}")
    if clip.get("grade") and cfg.get("lut"):
        vf.append(f"lut3d='{(root / cfg['lut']).resolve()}'")
    if clip.get("vf"):
        vf.append(clip["vf"])  # escape hatch for per-clip ffmpeg filters
    hs, he = float(clip.get("hold_start", 0)), float(clip.get("hold_end", 0))
    if hs or he:
        vf.append(f"tpad=start_mode=clone:start_duration={hs}:stop_mode=clone:stop_duration={he}")
    vf.append("format=yuv444p")
    run(["ffmpeg", "-y", "-v", "error", *_clip_inputs(clip, root, fps), "-an", "-vf", ",".join(vf),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "8", "-pix_fmt", "yuv444p", str(out)])
    return probe(str(out))["duration"]


def assemble(project_yaml: str, out_override: str | None = None, keep_temp: bool = False) -> dict:
    pfile = Path(project_yaml).resolve()
    root = pfile.parent
    proj = yaml.safe_load(pfile.read_text())
    o = proj.get("output", {})
    cfg = {"width": o.get("width", 1920), "height": o.get("height", 1080), "fps": o.get("fps", 24),
           "lut": (proj.get("grade") or {}).get("lut")}
    out_path = Path(out_override or (root / o.get("path", "out/edit.mp4")))
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Pair clips with the transition that precedes them; apply automatic holds.
    clips, trans = [], []
    pending = {"type": "cut"}
    for item in proj["timeline"]:
        if "transition" in item:
            pending = item["transition"]
            continue
        c = dict(item)
        if clips:
            trans.append(pending)
            if pending.get("hold") and pending.get("type", "cut") != "cut":
                d = float(pending.get("duration", 0.5))
                clips[-1]["hold_end"] = float(clips[-1].get("hold_end", 0)) + d
                c["hold_start"] = float(c.get("hold_start", 0)) + d
        clips.append(c)
        pending = {"type": "cut"}

    tmp = Path(tempfile.mkdtemp(prefix="ive_"))
    try:
        durs, files = [], []
        for i, c in enumerate(clips):
            f = tmp / f"c{i:03d}.mp4"
            durs.append(_render_clip(c, root, f, cfg))
            files.append(f)

        inputs = []
        for f in files:
            inputs += ["-i", str(f)]
        # xfade silently truncates the output unless every input shares timebase/fps/zero start.
        norm = f"settb=AVTB,setpts=PTS-STARTPTS,fps={cfg['fps']},"
        fc, last, t_end = [f"[0:v]{norm}null[n0]"], "[n0]", durs[0]
        for i, t in enumerate(trans, start=1):
            name, expr = _xfade_expr(t)
            d = float(t.get("duration", 0.5)) if name != "cut" else 1.0 / cfg["fps"]
            d = min(d, durs[i] - 1e-3, t_end - 1e-3)
            off = t_end - d
            lbl = f"[x{i}]"
            if name == "cut":
                # a 1-frame 'fade' is visually a hard cut but keeps the chain uniform
                fc.append(f"{last}format=gbrp[a{i}];[{i}:v]{norm}format=gbrp[b{i}];[a{i}][b{i}]xfade=transition=fade:duration={d:.4f}:offset={off:.4f}{lbl}")
            elif expr:
                fc.append(f"{last}format=gbrp[a{i}];[{i}:v]{norm}format=gbrp[b{i}];[a{i}][b{i}]xfade=transition=custom:duration={d:.4f}:offset={off:.4f}:expr='{expr}'{lbl}")
            else:
                fc.append(f"{last}format=gbrp[a{i}];[{i}:v]{norm}format=gbrp[b{i}];[a{i}][b{i}]xfade=transition={name}:duration={d:.4f}:offset={off:.4f}{lbl}")
            last, t_end = lbl, off + durs[i]
        vlast = last
        # Overlays (Remotion HUD .mov with alpha, logos...) at absolute timeline times.
        n_in = len(files)
        for k, ov in enumerate(proj.get("overlays", [])):
            inputs += ["-i", str((root / ov["src"]).resolve())]
            st = float(ov.get("start", 0))
            fc.append(f"[{n_in}:v]format=yuva444p,setpts=PTS+{st}/TB[ov{k}]")
            fc.append(f"{vlast}format=yuv444p[base{k}];[base{k}][ov{k}]overlay=eof_action=pass:format=auto[o{k}]")
            vlast = f"[o{k}]"
            n_in += 1
        fc.append(f"{vlast}format=yuv420p[vout]")

        cmd = ["ffmpeg", "-y", "-v", "error", *inputs]
        music = proj.get("music")
        amap = []
        if music and music.get("path"):
            cmd += ["-ss", str(music.get("start", 0)), "-i", str((root / music["path"]).resolve())]
            fo = float(music.get("fade_out", 1.5))
            fc.append(f"[{n_in}:a]atrim=0:{t_end:.3f},afade=t=out:st={max(0, t_end - fo):.3f}:d={fo},volume={music.get('gain', 1.0)}[aout]")
            amap = ["-map", "[aout]", "-c:a", "aac", "-b:a", "320k"]
        cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", *amap,
                "-c:v", o.get("codec", "libx264"), "-crf", str(o.get("crf", 16)), "-preset", o.get("preset", "slow"),
                "-movflags", "+faststart", "-t", f"{t_end:.3f}", str(out_path)]
        run(cmd)
        result = {"output": str(out_path), "duration": t_end, "clips": len(clips), "transitions": [t.get("type") for t in trans]}
        (out_path.with_suffix(".build.json")).write_text(json.dumps(result, indent=2))
        return result
    finally:
        if not keep_temp:
            shutil.rmtree(tmp, ignore_errors=True)
