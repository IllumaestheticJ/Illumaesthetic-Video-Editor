"""Hard-cut-only assembly without the duplicated cut frame.

`ive assemble` builds every cut as a 1-frame xfade over a cloned hold frame, so the frame AT each cut repeats clip A's
last frame and clip B's first frame is dropped (measured on v1: frame-diff 0.0 just before every cut). For a reel whose
transitions are all hard cuts, render each clip with ive's own _render_clip at an exact whole-frame length (`frames:`
in project.yaml, else round(dur*fps)) and concatenate - cut k lands exactly on sum(frames[:k]).
    python projects/honda-s2000/tools/concat_assemble.py projects/honda-s2000/project.yaml [--out x.mp4]"""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from ive.assemble import _render_clip  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--out")
a = ap.parse_args()
pf = Path(a.project).resolve(); root = pf.parent; proj = yaml.safe_load(pf.read_text())
o = proj["output"]; fps = o.get("fps", 30)
cfg = {"width": o["width"], "height": o["height"], "fps": fps, "lut": None}
clips = [c for c in proj["timeline"] if "transition" not in c]
assert all(t["transition"].get("type", "cut") == "cut" for t in proj["timeline"] if "transition" in t), "cuts only"
out = Path(a.out or o["path"]); out.parent.mkdir(parents=True, exist_ok=True)
tmp = Path(tempfile.mkdtemp(prefix="s2k_"))
try:
    files, frames = [], []
    for i, c in enumerate(clips):
        n = int(c.get("frames") or round(float(c["dur"]) * fps))
        c = dict(c); c["dur"] = n / fps; c.pop("frames", None)
        f = tmp / f"c{i:03d}.mp4"; _render_clip(c, root, f, cfg)
        got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                  "stream=nb_read_frames", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.strip())
        print(f"{c['id']:14s} {n} frames (got {got}) cut-in @ frame {sum(frames)}")
        assert got == n, (c["id"], got, n)
        files.append(f); frames.append(n)
    total = sum(frames) / fps
    lst = tmp / "list.txt"; lst.write_text("".join(f"file '{f}'\n" for f in files))
    m = proj["music"]; fo = float(m.get("fade_out", 1.0))
    # HUD overlays (Remotion .mov with alpha) at absolute times; inputs 2.. after concat (0) and music (1)
    vchain, last = "", "[0:v]"
    for k, ov in enumerate(proj.get("overlays") or []):
        vchain += (f"[{k + 2}:v]format=yuva444p,setpts=PTS+{float(ov.get('start', 0))}/TB[ov{k}];"
                   f"{last}format=yuv444p[b{k}];[b{k}][ov{k}]overlay=eof_action=pass:format=auto[o{k}];")
        last = f"[o{k}]"
    vchain += f"{last}format=yuv420p[v];"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-ss", str(m.get("start", 0)), "-i", str((root / m["path"]).resolve()),
                    *sum((["-i", str((root / ov["src"]).resolve())] for ov in proj.get("overlays") or []), []),
                    "-filter_complex", vchain + f"[1:a]atrim=0:{total:.4f},afade=t=out:st={total - fo:.4f}:d={fo}[a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", str(o.get("crf", 16)), "-preset", o.get("preset", "slow"),
                    "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-t", f"{total:.4f}", str(out)], check=True)
    cuts = [sum(frames[:k]) for k in range(1, len(frames))]
    res = {"output": str(out), "duration": total, "frames": sum(frames), "cut_frames": cuts}
    out.with_suffix(".build.json").write_text(json.dumps(res, indent=1)); print(json.dumps(res))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
