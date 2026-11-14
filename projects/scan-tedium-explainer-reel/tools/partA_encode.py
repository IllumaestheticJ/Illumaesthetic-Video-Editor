"""Check one rendered shot and encode it to a ProRes 422 intermediate, then delete its PNGs (disk is tight).

  python partA_encode.py --frames FRAMES_DIR --shot S3 --movs MOV_DIR [--timeline partA_timeline.json]

Exit codes: 0 encoded (or already encoded), 2 frames missing (re-run Blender), 3 bad frames found and deleted (re-run Blender).
Bad = black/unlit (lessons: Cycles can drop all lights mid-sequence): mean luma < 25, or < 55 % of the shot's median, or
peak luma < 60. Per-frame luma stats are kept next to the mov as <shot>_luma.json.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--frames", required=True)
ap.add_argument("--shot", required=True)
ap.add_argument("--movs", required=True)
ap.add_argument("--timeline", default=str(Path(__file__).resolve().parent.parent / "partA_timeline.json"))
a = ap.parse_args()
tl = json.loads(Path(a.timeline).read_text())
f0, f1 = next((s["f0"], s["f1"]) for s in tl["shots"] if s["id"] == a.shot)
d = Path(a.frames) / a.shot
movs = Path(a.movs)
movs.mkdir(parents=True, exist_ok=True)
mov = movs / f"{a.shot}.mov"


def nframes(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


if mov.exists() and nframes(mov) == f1 - f0:
    print(f"[encode] {a.shot}: already encoded ({f1 - f0} frames)")
    sys.exit(0)
missing = [f for f in range(f0, f1) if not (d / f"{f:04d}.png").exists()]
if missing:
    print(f"[encode] {a.shot}: {len(missing)} frames missing (first {missing[0]})")
    sys.exit(2)
stats = {}
for f in range(f0, f1):
    im = np.asarray(Image.open(d / f"{f:04d}.png").convert("L").reduce(8), dtype=np.float32)
    stats[f] = (float(im.mean()), float(im.max()))
med = float(np.median([m for m, _ in stats.values()]))
bad = [f for f, (m, mx) in stats.items() if m < 25 or m < 0.55 * med or mx < 60]
(movs / f"{a.shot}_luma.json").write_text(json.dumps(dict(median=med, frames={str(k): v for k, v in stats.items()}, bad=bad)))
if bad:
    for f in bad:
        (d / f"{f:04d}.png").unlink()
    print(f"[encode] {a.shot}: {len(bad)} dark/unlit frames deleted: {bad}")
    sys.exit(3)
tmp = movs / f"_{a.shot}.mov"
subprocess.run(["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", str(f0), "-i", str(d / "%04d.png"),
                "-frames:v", str(f1 - f0), "-c:v", "prores_ks", "-profile:v", "2", "-pix_fmt", "yuv422p10le",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", str(tmp)], check=True)
assert nframes(tmp) == f1 - f0, "frame count mismatch"
tmp.replace(mov)
shutil.rmtree(d)
print(f"[encode] {a.shot}: {f1 - f0} frames -> {mov} (luma median {med:.0f}, min {min(m for m, _ in stats.values()):.0f})")
