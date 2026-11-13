"""Music v2 for the Smart 450 reel, built from harder.m4a as direction.md section 2 specifies (same content, same two edits:
8 beats removed from drop 1, 8 beats removed from the break-2 pad, 8 beats of drop 3 added at the end), with ONE correction.

Correction (measured, logged): the direction's grid T(m) = 1.499 + 0.37583 m is 0.22 % slower than the track. The hi-band click
of every kick sits on an exact 160.00 BPM lattice, src L(j) = 0.1176 + 0.375 j s (checked on 125 hits, 35-70 s; drop 1 = j 97,
drop 2 = j 129, drop 3 = j 169). Cutting at the direction's grid times drifted -1 ms per beat (-45 ms by m 46) and the join phases
were off by 6-9 ms. Here every segment edge is snapped to the lattice and each segment is resampled by 0.37583/0.375 = 1.00222
(slower by 3.8 cents, inaudible) so every kick click lands on T(m) and the picture cuts stay as directed.

  seg 1  m -4..4   : src L(97) at T(0)      ->  join at T(4)  (beats j 97..101)
  seg 2  m 4..50   : src L(109) at T(4)     ->  join at T(50) (8 beats j 101..109 removed)
  seg 3  m 50..end : src L(163) at T(50)    ->  (8 beats j 155..163 removed; drop 3 = j 169 lands at m 56, beats up to j 177 at m 64)
12 ms equal-power crossfades centred on the joins; -6 dB; 1.0 s fade out from 25.59 s; true-peak limiter (level=disabled).
Output: music_v2_raw.wav, END/30 s (v3: 857 frames = 28.57 s; segment 3 simply runs 8 beats further, source up to ~69.5 s). Resumable: skips when it exists unless --force.
"""
import subprocess, sys, numpy as np
from pathlib import Path
from scipy.signal import resample_poly
SR = 44100
MD = Path("/home/user/media/work/smart-450/music")
SRC = MD / "harder.m4a"
OUT = MD / "music_v2_raw.wav"
P_SRC, L0 = 0.375, 0.1239            # lattice L(j) = L0 + P_SRC*j; 0.1176 measured + 4 ms (the detector reads the click 4-5 ms late)
P_OUT = 0.37583                      # direction grid period
R = P_OUT / P_SRC                    # 1.002213
UP, DOWN = 451, 450                  # 1.002222, 0.0009 % off R: < 0.3 ms over the reel
T = lambda m: 1.499 + P_OUT * m
L = lambda j: L0 + P_SRC * j
sys.path.insert(0, str(Path(__file__).parent))
from edit_shots import END
TOTAL = END / 30.0   # v3: 857 frames = 8 more beats of drop 3 under the longer logo hold
XF = 0.012
FADE_START, FADE_LEN = TOTAL - 1.0, 1.0
# (j anchor, m anchor, output start s, output end s)
SEGS = [(97, 0, 0.0, T(4)), (109, 4, T(4), T(50)), (163, 50, T(50), TOTAL)]


def decode():
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SRC), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def segment(x, j, m, o0, o1):
    """Output samples for output time [o0, o1): src time = L(j) + (t - T(m)) / R (resampled by UP/DOWN)."""
    n = int(round((o1 - o0) * SR))
    s0 = L(j) + (o0 - T(m)) / R                       # source time of the first output sample
    i0 = int(round(s0 * SR)) - 2000
    need = int(n * DOWN / UP) + 6000
    chunk = x[i0:i0 + need]
    y = resample_poly(chunk, UP, DOWN, axis=0)
    k = int(round(2000 * UP / DOWN))                  # drop the lead-in
    return y[k:k + n]


def main():
    here = Path(__file__).parent
    if OUT.exists() and "--force" not in sys.argv and OUT.stat().st_mtime > max((here / "music_v2.py").stat().st_mtime, (here / "edit_shots.py").stat().st_mtime):
        print("exists", OUT); return
    x = decode() * 0.5            # -6 dB
    h = int(round(XF / 2 * SR))   # 6 ms each side of a join
    total = int(round(TOTAL * SR))
    y = np.zeros((total, 2))
    n = len(SEGS)
    for k, (j, m, o0, o1) in enumerate(SEGS):
        lo = h if k > 0 else 0          # incoming side: start 6 ms early
        hi = h if k < n - 1 else 0      # outgoing side: run 6 ms late
        a = int(round(o0 * SR)) - lo
        seg = segment(x, j, m, o0 - lo / SR, o1 + hi / SR)
        if k > 0:
            seg[:2 * h] *= np.sin(np.linspace(0, np.pi / 2, 2 * h))[:, None]
        if k < n - 1:
            seg[-2 * h:] *= np.cos(np.linspace(0, np.pi / 2, 2 * h))[:, None]
        y[a:a + len(seg)] += seg[:total - a]
    f0 = int(round(FADE_START * SR)); fl = int(FADE_LEN * SR)
    g = np.ones(total); g[f0:f0 + fl] = np.linspace(1, 0, fl); g[f0 + fl:] = 0
    y *= g[:, None]
    tmp = MD / "music_v2_pre.f32"
    y.astype(np.float32).tofile(tmp)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(tmp),
                    "-af", "alimiter=limit=0.89:attack=5:release=50:level=disabled", "-c:a", "pcm_s16le", str(OUT)], check=True)
    tmp.unlink()
    print("wrote", OUT, total / SR, "s")


if __name__ == "__main__":
    main()
