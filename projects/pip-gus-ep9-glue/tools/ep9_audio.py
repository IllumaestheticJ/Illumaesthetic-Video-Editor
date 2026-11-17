"""Ep 9 audio: dialogue (approved take, unaltered) + the series music bed (inquisitive_A, Higgsfield 077bbd23) -> mix.

Timeline (output seconds, 30 fps):
  Part A cartoon   0.000 - 37.967   take  0.000 - 37.967   (frames    0 - 1138)
  Part B real     37.967 - 42.967   no dialogue           (frames 1139 - 1288)  timelapse 3.4 s + 350Z 1.6 s
  Finale tag      42.967 - 46.767   take 37.967 - 41.767  (frames 1289 - 1402)
  Logo card       46.767 - 49.767                         (frames 1403 - 1492)

Music (100.00 BPM, beat b at 0.0203 + 0.6 b s in the track, bars of 4 beats, Gm/F alternating bars): the bass entry (lift,
bar 8 = beat 32) lands on the cut to Part B. The 8-bar intro is extended with 2-bar back-jumps (even, so the Gm/F phase holds,
as in the pilot): 0->10 | 2->14 | 6->22 | 14->30 | 22->32 = 64 beats, started 0.46 s in so the lift sits at 37.967 s. After the
lift: bars 8-9, jump end of bar 9 -> bar 14 (the pilot's seamless 4-bar route), final chord bar 16 at 47.57 s, inside the logo
card; ring-out then a 0.6 s tail fade to the end.
Ducking: under Part A / tag lines -13 dB, between lines -8 dB, 0 dB in Part B and on the logo card (150 ms ramps).
Master: -14 LUFS integrated, <= -1.5 dBTP (ffmpeg loudnorm, two-pass, linear).

Usage: python ep9_audio.py OUT_DIR   -> OUT_DIR/ep9_dialogue.wav, ep9_music.wav, ep9_mix.wav
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

SR = 48000
FPS = 30
HERE = Path(__file__).resolve().parent
VL = json.loads((HERE.parent / "voice_lines.json").read_text())
TAKE = "/home/user/media/pip-gus-ep9-glue/voice/ep9_take1.mp3"
TRACK = "/home/user/media/work/music/077bbd23-cc16-4c61-a5b8-8ca12d30e386.mp3"
A_END = 1139 / FPS            # 37.967: Part A ends (phone full-frame on frame 1138)
B_LEN = 150 / FPS             # 5.0
TAG_LEN = 114 / FPS           # 3.8
LOGO_LEN = 90 / FPS           # 3.0
TOTAL = A_END + B_LEN + TAG_LEN + LOGO_LEN
B0 = 0.0203
BEAT = 0.6


def load(path):
    x = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"])
    return np.frombuffer(x, np.float32).reshape(-1, 2).copy()


def beat(b):
    return B0 + BEAT * b


def splice(segs, xf=0.008):
    """Concatenate track segments [(t0, t1), ...] with short equal-power crossfades."""
    tr = load(TRACK)
    n = int(xf * SR)
    out = None
    for a, b in segs:
        s = tr[int(a * SR):int(b * SR) + n].copy()
        if out is None:
            out = s
            continue
        w = np.linspace(0, np.pi / 2, n)[:, None]
        out[-n:] = out[-n:] * np.cos(w) + s[:n] * np.sin(w)
        out = np.concatenate([out, s[n:]])
    return out


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    N = int(round(TOTAL * SR))
    # dialogue
    take = load(TAKE)
    dia = np.zeros((N, 2), np.float32)
    a = take[:int(A_END * SR)]
    dia[:len(a)] = a
    tag = take[int(A_END * SR):int((A_END + TAG_LEN) * SR)]
    t0 = int((A_END + B_LEN) * SR)
    dia[t0:t0 + len(tag)] = tag[:N - t0]
    # music
    segs = [(0.46, beat(10)), (beat(2), beat(14)), (beat(6), beat(22)), (beat(14), beat(30)), (beat(22), beat(40)),
            (beat(56), 42.0)]
    mus = splice(segs)
    lift_out = (beat(10) - 0.46) + (beat(14) - beat(2)) + (beat(22) - beat(6)) + (beat(30) - beat(14)) + (beat(32) - beat(22))
    print(f"music lift at {lift_out:.3f} s (Part B cut {A_END:.3f} s); final chord at {lift_out + 8 * BEAT + 8 * BEAT:.3f} s")
    m = np.zeros((N, 2), np.float32)
    k = min(N, len(mus))
    m[:k] = mus[:k]
    # duck envelope from the line spans (take time -> output time)
    t = np.arange(N) / SR
    g_db = np.where(t < A_END, -8.0, 0.0)
    tag_lo, tag_hi = A_END + B_LEN, A_END + B_LEN + TAG_LEN
    g_db = np.where((t >= tag_lo) & (t < tag_hi), -8.0, g_db)
    for L in VL["lines"]:
        for (lo, hi) in ([(L["t0"], L["t1"])] if L["t1"] <= A_END else [(L["t0"] + B_LEN, L["t1"] + B_LEN)]):
            g_db = np.where((t >= lo - 0.1) & (t <= hi + 0.15), -13.0, g_db)
    # 150 ms ramps
    w = int(0.15 * SR)
    g = 10 ** (np.convolve(g_db, np.ones(w) / w, mode="same") / 20)
    fade = np.clip((TOTAL - t) / 0.6, 0, 1)
    fin = np.clip(t / 0.25, 0, 1)
    m *= (g * fade * fin)[:, None]
    write(out / "ep9_dialogue.wav", dia)
    write(out / "ep9_music.wav", m)
    mix = dia * 1.0 + m * 0.55
    write(out / "ep9_mix_raw.wav", mix)
    # two-pass loudnorm to -14 LUFS, -1.5 dBTP
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out / "ep9_mix_raw.wav"), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
          f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,aresample={SR}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "ep9_mix_raw.wav"), "-af", af, "-c:a", "pcm_s16le",
                    str(out / "ep9_mix.wav")], check=True)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out / "ep9_mix.wav"), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    print("\n".join(l for l in r.stderr.splitlines()[-12:] if any(k in l for k in ("I:", "Peak:", "LRA:"))))
    print(f"total {TOTAL:.3f} s = {round(TOTAL * FPS)} frames")


def write(p, x):
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", str(p)], input=y.tobytes(),
                   check=True)


if __name__ == "__main__":
    main()
