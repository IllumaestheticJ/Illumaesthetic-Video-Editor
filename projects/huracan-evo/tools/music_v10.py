"""v10 music edit (user: "the whole thing can take longer than 30 seconds if it helps with pacing"): 3 s silence for the engine
start, then reel_track_a k20-k56 | k40-end (splice 60 ms before the kick, 15 ms crossfade). Output kicks n at 3.0768 + 0.60006 n:
drop (k32) n12 = 10.278 s; groove n12-n56 (44 beats); last kick n56 = 36.68 s; reverb tail after.   python tools/music_v10.py OUT.wav"""
import subprocess
import sys

import numpy as np

SRC = "/home/user/media/work/music/reel_track_a.mp3"
SR, K0, KP, PRE, XF = 48000, 0.0768, 0.60006, 0.060, 0.015


def main(out):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
    kt = lambda k: K0 + KP * k - PRE
    a = x[int(KP * 20 * SR): int(kt(56) * SR)].copy()                # k20 lands at 0.0768 -> after the 3 s lead at 3.0768
    fi = int(0.25 * SR); a[:fi] *= np.linspace(0, 1, fi)[:, None]
    b = x[int(kt(40) * SR):].copy()
    xf = int(XF * SR); r = np.linspace(0, 1, xf)[:, None]
    a[-xf:] = a[-xf:] * (1 - r) + b[:xf] * r
    y = np.concatenate([np.zeros((3 * SR, 2), np.float32), a, b[xf:]])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", out],
                   input=y.astype(np.float32).tobytes(), check=True)
    print(out, round(len(y) / SR, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1])
