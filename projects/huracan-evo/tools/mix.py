"""Premix the Huracan soundtrack: car-select intro (engine roar + female narrator, Hot Pursuit-style car-select
homage, original script/voice) over reel_track_a, music ducked under the voice. Output is set as project music.

  python projects/huracan-evo/tools/mix.py OUT.wav
Stems (not in git, see clips.md): music = reel_track_a.mp3; engine.mp3 (Higgsfield Mirelo SFX, generated);
narration4.wav (Higgsfield Seed Audio, preset voice 'Imogen' - NOT a clone of the game's narrator), car-only script.
"""
import subprocess
import sys

MUSIC = "/home/user/media/work/music/reel_track_a.mp3"
ENGINE = "/home/user/media/huracan-evo/vo/engine.mp3"
VO_RAW = "/home/user/media/huracan-evo/vo/narration4.wav"   # v2 script: car only (user: "don't talk about the scan")
VO = "/home/user/media/huracan-evo/vo/narration4_tight.wav"
VO_AT = 0.9          # s: file has 0.44 s lead-in, so speech starts ~1.3 s as the roar peaks
GAP_KEEP = 0.24      # s: sentence pauses trimmed to this (take had 0.5-0.8 s pauses)
TEMPO = 1.08         # pitch-preserving speed-up so the read ends before the lift
DUCK_DB = -9.0       # music under the voice
RAMP = 0.6
LIFT = 19.279        # music lift / explode start - voice must be done and music back to full by here


def tighten(src, dst):
    """Trim pauses longer than GAP_KEEP to GAP_KEEP (cut in the middle of the silence, 10 ms crossfade), then atempo."""
    import numpy as np
    sr = 48000
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
    m = x.mean(1); w = int(0.03 * sr)
    e = np.sqrt(np.convolve(m ** 2, np.ones(w) / w, "same")); on = e > 0.06 * e.max()
    idx = np.flatnonzero(np.diff(on.astype(int)))  # transitions
    keep, last = [], 0
    starts = [i for i in idx if not on[i]]          # silence -> speech
    ends = [i for i in idx if on[i]]                # speech -> silence
    for a in ends:
        b = next((s_ for s_ in starts if s_ > a), None)
        if b is None or (b - a) / sr <= GAP_KEEP:
            continue
        h = int(GAP_KEEP / 2 * sr)
        keep.append((last, a + h)); last = b - h
    keep.append((last, len(x)))
    xf = int(0.01 * sr); out = x[keep[0][0]:keep[0][1]].copy()
    for a, b in keep[1:]:
        seg = x[a:b].copy(); r = np.linspace(0, 1, xf)[:, None]
        out[-xf:] = out[-xf:] * (1 - r) + seg[:xf] * r; out = np.concatenate([out, seg[xf:]])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-",
                    "-af", f"atempo={TEMPO}", dst], input=out.astype(np.float32).tobytes(), check=True)
    n = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst],
                             capture_output=True, text=True).stdout)
    return n


def main(out):
    VO_LEN = tighten(VO_RAW, VO)
    print("voice", round(VO_LEN, 2), "s, ends at", round(VO_AT + VO_LEN, 2))
    d0, d1 = VO_AT - RAMP, VO_AT + VO_LEN + 0.2
    g = 10 ** (DUCK_DB / 20)
    assert d1 + RAMP < LIFT, "voice runs into the lift"
    # piecewise-linear duck envelope as an ffmpeg volume expression (eval per frame)
    env = (f"if(lt(t,{d0}),1,if(lt(t,{d0 + RAMP}),1-(1-{g})*(t-{d0})/{RAMP},"
           f"if(lt(t,{d1}),{g},if(lt(t,{d1 + RAMP}),{g}+(1-{g})*(t-{d1})/{RAMP},1))))")
    fc = (
        f"[0:a]aresample=48000,volume='{env}':eval=frame[m];"
        # engine: full at the 'select', then tucks under the first line
        f"[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=0.9,afade=t=out:st=2.6:d=2.6[e];"
        # voice: clean announcer chain - HPF, gentle comp, short room
        f"[2:a]aresample=48000,highpass=f=110,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
        f"aecho=0.85:0.5:38|71:0.18|0.10,volume=2.4,alimiter=limit=0.8:level=disabled,adelay={int(VO_AT * 1000)}|{int(VO_AT * 1000)}[v];"
        f"[m][e][v]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95:level=disabled[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", MUSIC, "-i", ENGINE, "-i", VO, "-filter_complex", fc,
                    "-map", "[out]", "-c:a", "pcm_s24le", out], check=True)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
