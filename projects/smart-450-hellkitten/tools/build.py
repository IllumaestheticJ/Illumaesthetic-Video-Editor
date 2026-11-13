"""One command that rebuilds the whole reel (resumable; cached steps are skipped, finished scan renders are picked up).

    python projects/smart-450-hellkitten/tools/build.py [--force-prep] [--no-assemble]

1 music v2  2 shot clips (prep_video: IRL crops, stills, logo, scan shots/placeholders)  3 HUD overlays (Remotion)
4 audio mix + stems  5 project.yaml  6 concat_assemble.py (hard cuts, exact frames; `ive assemble` drops a frame per cut)  7 mux AAC 256k -> OUT/smart450_v6.mp4  8 build report
"""
import json, os, subprocess, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
SM = Path("/home/user/media/work/smart-450")
PY = sys.executable

def run(cmd, **kw):
    print("+", " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, check=True, **kw)

def main():
    force = "--force-prep" in sys.argv
    run([PY, HERE / "music_v2.py"])
    run([PY, HERE / "prep_video.py"] + (["--force"] if force else []))
    for name in ("hud_body", "hud_a4", "hud_final"):
        j, m = HERE.parent / "hud" / f"{name}.json", SM / "build" / f"{name}.mov"
        if not m.exists() or m.stat().st_mtime < j.stat().st_mtime:
            run([PY, "-m", "ive", "hud", j, m], cwd=REPO)
    run([PY, HERE / "memes.py", "--build"])
    run([PY, HERE / "meows.py"])
    run([PY, HERE / "audio_mix.py"])
    run([PY, HERE / "gen_project.py"])
    if "--no-assemble" in sys.argv:
        return
    run([PY, HERE / "concat_assemble.py", HERE.parent / "project.yaml"], cwd=REPO)   # not `ive assemble`: it drops each shot's first frame (see concat_assemble.py)
    out = SM / "out" / "smart450_v6.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", SM / "build" / "smart450_v6_video.mp4", "-i", SM / "out" / "smart450_mix.wav",
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out])
    st = json.loads((SM / "build" / "status.json").read_text()) if (SM / "build" / "status.json").exists() else {}
    print("DONE", out, "scan shots:", {k: v for k, v in st.items() if k in ("S3", "S10", "S18")})

if __name__ == "__main__":
    main()
