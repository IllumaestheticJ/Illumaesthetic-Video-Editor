"""Where does every frame of every shot land in an assembled file? Matches the prepped clip frames against the output (+-3 frames).
usage: cutpos.py out_video.mp4 [build_dir]   -> per shot: offset histogram (output index - expected index); all 0 = frame exact.
Near-duplicate frames (static holds, slow stills) can match a neighbour, so a few +-1 on static shots are matching noise."""
import subprocess, sys, os
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SHOTS, SM
f = sys.argv[1]; bd = sys.argv[2] if len(sys.argv) > 2 else f"{SM}/build"
def dec(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(r, np.uint8).reshape(-1, 192, 108).astype(np.float32)
out = dec(f); bad = 0
for s in SHOTS:
    c = dec(f"{bd}/{s['id']}.mp4"); offs = []
    for ci in range(len(c)):
        e = s["start"] + ci
        best = min(range(max(0, e - 3), min(len(out), e + 4)), key=lambda i: np.abs(out[i] - c[ci]).mean())
        offs.append(best - e)
    h = Counter(offs); frac0 = h[0] / len(offs)
    bad += frac0 < 0.9
    print(s["id"], "n", len(c), "start", s["start"], "exact frames %.0f%%" % (100 * frac0), dict(h), "" if frac0 >= 0.9 else "  <-- OFF")
print("frames", len(out), "shots not frame-exact:", bad)
