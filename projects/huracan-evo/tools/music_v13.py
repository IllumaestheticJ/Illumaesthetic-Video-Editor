"""v13 music edit (user: re-pace the whole video evenly, longer is fine): 3 s silence, then reel_track_a from k15 so the drop
(k32) lands on n17 = 13.278 s, and a 51-beat groove: k32-k56 | k40-k56 | k49-end (splices 60 ms before the kick, 15 ms xfade).
Output kicks n at 3.0768 + 0.60006 n; last kick n68 = 43.88 s; reverb tail after.   python tools/music_v13.py OUT.wav"""
import subprocess
import sys

import numpy as np

SRC = "/home/user/media/work/music/reel_track_a.mp3"
SR, K0, KP, PRE, XF = 48000, 0.0768, 0.60006, 0.060, 0.015


def main(out):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
    kt = lambda k: K0 + KP * k - PRE
    segs = [x[int(KP * 15 * SR): int(kt(56) * SR)].copy(), x[int(kt(40) * SR): int(kt(56) * SR)].copy(), x[int(kt(49) * SR):].copy()]
    fi = int(0.25 * SR); segs[0][:fi] *= np.linspace(0, 1, fi)[:, None]
    xf = int(XF * SR); r = np.linspace(0, 1, xf)[:, None]; y = segs[0]
    for s in segs[1:]:
        y[-xf:] = y[-xf:] * (1 - r) + s[:xf] * r; y = np.concatenate([y, s[xf:]])
    y = np.concatenate([np.zeros((3 * SR, 2), np.float32), y])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", out],
                   input=y.astype(np.float32).tobytes(), check=True)
    print(out, round(len(y) / SR, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1])
