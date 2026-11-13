"""Cut every span of one clip (all three reels) from the 4K original into graded full-width intermediates.

    python tools/cut_src.py FX30541 [--force]

Output per span: /home/user/media/work/is350-reels/src/<id>.mov (H.264 CRF 12, 3414x1920 = the whole 16:9 frame at 1920 px tall,
native 23.976 fps, 0.5 s handles, source audio PCM) + <id>.json {clip, f0 (source frame of intermediate frame 0), n, fps}.
Grade = the long-form's: S-Log3 -> 709 LUT (fx3a_slog3cine_to_709.cube), tetrahedral, applied in rgb48. -noautorotate always
(FX30545 carries a -90 flag on an upright frame; harmless elsewhere). Frame k of the intermediate = source frame f0 + k (seek to (f0-0.5)/fps).
"""
import json, subprocess, sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPANS = json.loads((HERE.parent / "spans.json").read_text())["spans"]
LUT = "/home/user/Illumaesthetic-Video-Editor/projects/toyota-mr2-spyder-scan-process/grade/fx3a_slog3cine_to_709.cube"
K4 = Path("/home/user/media/lexus-is350/dropbox_4k")
OUT = Path("/home/user/media/work/is350-reels/src")
FPS = Fraction(24000, 1001)
HANDLE = 0.5
W, H = 3414, 1920


def nframes(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def cut(sid, s, force=False):
    OUT.mkdir(parents=True, exist_ok=True)
    mov, meta = OUT / f"{sid}.mov", OUT / f"{sid}.json"
    f0 = max(0, int((s["a"] - HANDLE) * FPS))
    f1 = int(-(-(s["b"] + HANDLE) * FPS // 1))  # ceil
    n = f1 - f0
    if mov.exists() and meta.exists() and not force:
        m = json.loads(meta.read_text())
        if m.get("f0") == f0 and m.get("n") == n and nframes(mov) == n:
            print("cached", sid); return
    src = K4 / f"{s['clip']}.MP4"
    vf = f"format=rgb48le,lut3d=file={LUT}:interp=tetrahedral,scale={W}:{H}:flags=lanczos,format=yuv420p"
    cmd = ["nice", "-n", "5", "ffmpeg", "-v", "error", "-y", "-threads", "3", "-noautorotate", "-ss", f"{(f0 - 0.5) / FPS:.5f}", "-i", str(src),
           "-frames:v", str(n), "-fps_mode", "passthrough", "-vf", vf, "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-profile:v", "high",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "pcm_s24le", "-af", f"atrim=0:{float(n / FPS):.4f}", str(mov)]
    print("+", sid, s["clip"], f0, n, flush=True)
    subprocess.run(cmd, check=True)
    got = nframes(mov)
    assert got == n, (sid, got, n)
    meta.write_text(json.dumps({"id": sid, "clip": s["clip"], "f0": f0, "n": n, "fps": "24000/1001", "w": W, "h": H,
                                "t0": float(f0 / FPS), "lut": Path(LUT).name}, indent=1))


def main():
    clip = sys.argv[1]
    force = "--force" in sys.argv
    ids = [k for k, s in SPANS.items() if s["clip"] == clip]
    for k in ids:
        cut(k, SPANS[k], force)
    print("done", clip, ids)


if __name__ == "__main__":
    main()
