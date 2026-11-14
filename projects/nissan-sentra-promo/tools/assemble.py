"""Frame-exact assembly of the Sentra promo (no xfade cuts: ive assemble duplicates a frame at every hard cut - lessons).
Segments are cut at round(t*30) frames from timing.json; scan renders are 15 fps PNGs interpolated to 30 with minterpolate
(output frame k = render time k/30, so the first `n` frames are taken). Captions (PromoCaption ProRes 4444) are overlaid
from the cut on, never over the IRL hook. Audio = the narration only (owner: no music), loudness-normalised.
    python projects/nissan-sentra-promo/tools/assemble.py out.mp4
"""
import json, subprocess, sys
W = "/home/user/media/work/sentra"
P = "/home/user/Illumaesthetic-Video-Editor/projects/nissan-sentra-promo"
FPS = 30
out = sys.argv[1]
cut = {"scan": 130, "brake": round(37.1 * FPS), "final": round(41.23 * FPS), "logo": round(43.43 * FPS), "end": round(47.0 * FPS)}
segs = [  # (name, source, frames)
    ("irl", f"{W}/clips/irl.mp4", cut["scan"]),
    ("main", f"{W}/render/main", cut["brake"] - cut["scan"]),
    ("brake", f"{W}/render/brake", cut["final"] - cut["brake"]),
    ("final", f"{W}/render/final", cut["logo"] - cut["final"]),
    ("logo", f"{W}/clips/logo.mp4", cut["end"] - cut["logo"]),
]
MI = "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
parts = []
for name, src, n in segs:
    seg = f"{W}/clips/seg_{name}.mp4"
    if src.endswith(".mp4"):
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src]
        vf = "scale=1080:1920:flags=lanczos,fps=30"
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", "15", "-pattern_type", "glob", "-i", f"{src}/f_*.png"]
        vf = f"{MI},scale=1080:1920:flags=lanczos"
    cmd += ["-vf", vf + f",tpad=stop_mode=clone:stop=60,format=yuv420p", "-frames:v", str(n), "-an",
            "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-r", "30", seg]
    subprocess.run(cmd, check=True)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", seg],
                             capture_output=True, text=True).stdout.strip())
    print(name, "frames", got, "want", n)
    assert got == n, name
    parts.append(seg)
lst = f"{W}/clips/list.txt"
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
dur = cut["end"] / FPS
caps = f"{W}/clips/caps.mov"
cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", caps,
       "-i", "/home/user/media/nissan-sentra-promo/voice/voice.wav",
       "-filter_complex",
       f"[1:v]format=yuva420p,trim=start_frame={cut['scan']},setpts=PTS-STARTPTS+{cut['scan']}/30/TB[c];"
       f"[0:v][c]overlay=0:0:eof_action=pass,format=yuv420p[v];"
       f"[2:a]apad,atrim=0:{dur},loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000[a]",
       "-map", "[v]", "-map", "[a]", "-t", f"{dur}", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p",
       "-profile:v", "high", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-r", "30", out]
subprocess.run(cmd, check=True)
print("OUT", out)
