"""Cut-only assembly with exact frame counts (no duplicated cut frame), per-clip fade-out, HUD overlay and music.

    python projects/ferrari-296/tools/assemble_cuts.py projects/ferrari-296/project.yaml [--out x.mp4]

Based on projects/honda-s2000/tools/concat_assemble.py (lesson: `ive assemble` builds a hard cut as a 1-frame xfade over a
cloned hold frame, so the frame at every cut repeats clip A). Each clip is rendered by ive's _render_clip at exactly
`frames:` (else round(dur*fps)) frames; cut k = sum(frames[:k]). Extras:
  fade_out: <s>    fade that clip to black over its last <s> seconds (ending: fade out, then the small logo)
  overlays: [{src: hud.mov, start: 0}]   transparent ScanHUD overlay(s) composited over the whole cut
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from ive.assemble import _render_clip  # noqa: E402


def nframes(f):
    return int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                               "stream=nb_read_frames", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--out")
    a = ap.parse_args()
    pf = Path(a.project).resolve()
    root = pf.parent
    proj = yaml.safe_load(pf.read_text())
    o = proj["output"]
    fps = o.get("fps", 30)
    cfg = {"width": o["width"], "height": o["height"], "fps": fps, "lut": None}
    clips = [c for c in proj["timeline"] if "transition" not in c]
    assert all(t["transition"].get("type", "cut") == "cut" for t in proj["timeline"] if "transition" in t), "cuts only"
    out = Path(a.out or o["path"])
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="f296_"))
    try:
        files, frames = [], []
        for i, c in enumerate(clips):
            n = int(c.get("frames") or round(float(c["dur"]) * fps))
            c = dict(c)
            c["dur"] = n / fps
            c.pop("frames", None)
            src = (root / c["src"]).resolve()
            if c.get("interpolate") and src.is_dir():
                # minterpolate turns N renders at r fps into (N-1)*fps/r - 1 distinct frames; ive pads the rest by
                # cloning the last frame (a visible stall before the cut). Stretch the input rate just enough instead.
                N = len(list(src.glob("*.png")))
                r = float(c.get("src_fps", fps))
                need = (N - 1) * fps / (n + 2)  # +1 frame margin: rounding left one clone
                if need < r:
                    c["src_fps"] = round(need, 4)
                    print(f"  {c['id']}: {N} renders -> src_fps {r} -> {c['src_fps']} ({100 * (1 - need / r):.1f}% slower, no clone pad)")
            f = tmp / f"c{i:03d}.mp4"
            _render_clip(c, root, f, cfg)
            if c.get("fade_out"):
                d = float(c["fade_out"])
                g = tmp / f"c{i:03d}_f.mp4"
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-vf", f"fade=t=out:st={n / fps - d:.4f}:d={d}",
                                "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(g)], check=True)
                f = g
            got = nframes(f)
            print(f"{c['id']:14s} {n} frames (got {got}) cut-in @ frame {sum(frames)}", flush=True)
            assert got == n, (c["id"], got, n)
            files.append(f)
            frames.append(n)
        total = sum(frames) / fps
        lst = tmp / "list.txt"
        lst.write_text("".join(f"file '{f}'\n" for f in files))
        m = proj["music"]
        fo = float(m.get("fade_out", 1.0))
        inputs = ["-f", "concat", "-safe", "0", "-i", str(lst), "-ss", str(m.get("start", 0)), "-i", str((root / m["path"]).resolve())]
        vf = "[0:v]format=yuv420p[base]"
        last = "[base]"
        for k, ov in enumerate(proj.get("overlays") or []):
            inputs += ["-itsoffset", str(ov.get("start", 0)), "-i", str((root / ov["src"]).resolve())]
            vf += f";{last}[{k + 2}:v]overlay=eof_action=pass:format=auto[o{k}]"
            last = f"[o{k}]"
        vf += f";{last}format=yuv420p[v];[1:a]atrim=0:{total:.4f},afade=t=out:st={total - fo:.4f}:d={fo}[a]"
        subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", vf, "-map", "[v]", "-map", "[a]",
                        "-c:v", "libx264", "-crf", str(o.get("crf", 16)), "-preset", o.get("preset", "slow"),
                        "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-t", f"{total:.4f}", str(out)], check=True)
        cuts = [sum(frames[:k]) for k in range(1, len(frames))]
        res = {"output": str(out), "duration": total, "frames": sum(frames), "cut_frames": cuts}
        out.with_suffix(".build.json").write_text(json.dumps(res, indent=1))
        print(json.dumps(res))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
