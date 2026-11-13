"""Hard-cut assembly of the prepared shots + HUD overlays, video only (build.py muxes the audio).

Why not `ive assemble`: it builds each cut as a 1-frame xfade over a cloned hold frame. Measured on this reel's first full build:
every shot lost its own first frame (the scan's 'frame 1 = solved camera' never showed; S3[1] followed the IRL frame), the previous
shot's last frame (the solved IRL frame!) was shown twice, and the A2 state swap landed on frame 315 instead of 316. Same finding as
projects/honda-s2000/tools/concat_assemble.py. Every shot here is already an exact-length 1080x1920 30 fps clip (tools/prep_video.py),
so cut k lands on sum(frames[:k]) by construction.

    python projects/smart-450-hellkitten/tools/concat_assemble.py [project.yaml] [--out video.mp4] [--crf 17]
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import yaml

ap = argparse.ArgumentParser()
ap.add_argument("project", nargs="?", default=str(Path(__file__).resolve().parent.parent / "project.yaml"))
ap.add_argument("--out"); ap.add_argument("--crf", type=int)
a = ap.parse_args()
proj = yaml.safe_load(Path(a.project).read_text())
o = proj["output"]
clips = [c for c in proj["timeline"] if "id" in c]
assert all(t["transition"].get("type", "cut") == "cut" for t in proj["timeline"] if "transition" in t), "cuts only"
out = Path(a.out or o["path"]); out.parent.mkdir(parents=True, exist_ok=True)


def nframes(p):
    return int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                               "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


start, total = 0, 0
for c in clips:
    got = nframes(c["src"])
    assert got == c["frames"], (c["id"], got, c["frames"])
    assert c["start_frame"] == total, (c["id"], c["start_frame"], total)
    total += got
tmp = Path(tempfile.mkdtemp(prefix="smart_"))
lst = tmp / "list.txt"; lst.write_text("".join(f"file '{c['src']}'\n" for c in clips))
ovs = proj.get("overlays") or []
vchain, last = "", "[0:v]"
for k, ov in enumerate(ovs):
    vchain += (f"[{k + 1}:v]format=yuva444p,setpts=PTS+{float(ov['start'])}/TB[ov{k}];"
               f"{last}format=yuv444p[b{k}];[b{k}][ov{k}]overlay=eof_action=pass:format=auto[o{k}];")
    last = f"[o{k}]"
vchain += f"{last}format=yuv420p[v]"
cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), *sum((["-i", ov["src"]] for ov in ovs), []),
       "-filter_complex", vchain, "-map", "[v]", "-r", "30", "-c:v", "libx264", "-crf", str(a.crf or o.get("crf", 17)),
       "-preset", o.get("preset", "slow"), "-movflags", "+faststart", "-frames:v", str(total), str(out)]
subprocess.run(cmd, check=True)
got = nframes(out)
res = {"output": str(out), "frames": got, "duration": got / 30, "cut_frames": [c["start_frame"] for c in clips[1:]]}
assert got == total, (got, total)
out.with_suffix(".build.json").write_text(json.dumps(res, indent=1)); print(json.dumps(res))
