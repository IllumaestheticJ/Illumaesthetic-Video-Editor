"""Prepare an FX30 clip for the 9:16 timeline: S-Log3 LUT grade, 9:16 crop window, 30 fps.

    python tools/irl.py SRC IN OUT X0 OUTFILE [--zoom 1.0] [--y0 0] [--interp]

X0/Y0 = top-left of the crop window in source (3840x2160) pixels. The window is
(2160/zoom)*9/16 wide and 2160/zoom tall, scaled to 1080x1920. `--interp` = motion-compensated
24->30 (else frame duplication). The output frame k is at time IN + k/30 of the source timeline
(rounded to the source frame grid when not interpolating).
"""
import argparse, subprocess
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("tin", type=float); ap.add_argument("tout", type=float)
ap.add_argument("x0", type=float); ap.add_argument("out")
ap.add_argument("--zoom", type=float, default=1.0); ap.add_argument("--y0", type=float, default=0)
ap.add_argument("--interp", action="store_true")
ap.add_argument("--lut", default="/home/user/media/work/sera/slog3_709.cube")
ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--last", type=int, default=0, help="keep only the last N output frames (clip must END on the match frame; trim the start, never the end)")
a = ap.parse_args()
h = 2160 / a.zoom; w = h * 9 / 16
vf = [f"lut3d={a.lut}", f"crop={w:.0f}:{h:.0f}:{a.x0:.0f}:{a.y0:.0f}", "scale=1080:1920:flags=lanczos"]
if a.speed != 1.0:
    vf.append(f"setpts=PTS/{a.speed}")
vf.append("minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if a.interp else "fps=30")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{a.tin:.4f}", "-to", f"{a.tout:.4f}", "-i", a.src, "-an",
                "-vf", ",".join(vf), "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p", a.out], check=True)
if a.last:
    import json, os
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", a.out],
                           capture_output=True, text=True, check=True).stdout.strip())
    tmp = a.out + ".tmp.mp4"; os.replace(a.out, tmp)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-vf", f"trim=start_frame={n - a.last},setpts=PTS-STARTPTS",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p", a.out], check=True)
    os.remove(tmp)
print(a.out)
