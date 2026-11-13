"""Mix master + stems for the Smart 450 reel.

    python projects/smart-450-hellkitten/tools/audio_mix.py

music_v2_raw.wav (tools/music_v2.py) + the shop sound of every IRL shot (its own source span, first audio stream, 2-frame fades,
uncensored; scan shots, stills and the logo carry music only). Shop level per shot: 'under' = 14 dB below the music's RMS in that
window, 'up' = 6 dB below (direction.md); boost capped at +24 dB. Master = music + shop, gain-matched to -10 LUFS integrated,
true peak limited to <= -1 dBTP. Stems are written at the SAME gain (they sum to the master before the limiter).
Outputs in OUT: smart450_mix.wav, stem_music.wav, stem_shopsound.wav, audio_levels.json.
"""
import json, os, re, subprocess, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SHOTS, DB, SM, FPS

SR = 44100
OUT = Path(SM) / "out"; OUT.mkdir(exist_ok=True, parents=True)
MUSIC = Path(SM) / "music" / "music_v2_raw.wav"
TOTAL = 798


def read_wav_f32(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def write_wav(path, x):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", str(path)],
                   input=x.astype(np.float32).tobytes(), check=True)


def lufs(x):
    r = subprocess.run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", "ebur128=peak=true",
                        "-f", "null", "-"], input=x.astype(np.float32).tobytes(), capture_output=True)
    t = r.stderr.decode()
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", t)[-1]); tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", t)[-1])
    return I, tp


def rms_db(x):
    return 20 * np.log10(max(np.sqrt(np.mean(x ** 2)), 1e-9))


def main():
    music = read_wav_f32(MUSIC)
    nsamp = int(round(TOTAL / FPS * SR))
    if len(music) < nsamp:
        music = np.vstack([music, np.zeros((nsamp - len(music), 2))])
    music = music[:nsamp]
    shop = np.zeros((nsamp, 2))
    levels = {}
    fade = int(round(2 / FPS * SR))
    for s in SHOTS:
        if s["kind"] != "irl" or not s.get("audio"):
            continue
        a, b = int(round(s["start"] / FPS * SR)), int(round((s["start"] + s["n"]) / FPS * SR))
        dur = s["n"] / FPS
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s['ss']:.4f}", "-t", f"{dur:.4f}", "-i", f"{DB}/{s['src']}.mov",
                              "-map", "0:a:0", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
        x = x[:b - a]
        if len(x) < b - a:
            x = np.vstack([x, np.zeros((b - a - len(x), 2))])
        x[:fade] *= np.linspace(0, 1, fade)[:, None]
        x[-fade:] *= np.linspace(1, 0, fade)[:, None]
        target = rms_db(music[a:b]) - (14 if s["audio"] == "under" else 6)
        src_rms = rms_db(x)
        g_db = min(target - src_rms, 24.0)
        y = x * 10 ** (g_db / 20)
        c = 10 ** (rms_db(music[a:b]) / 20)           # soft ceiling at the music's RMS: handling thumps must not pump the master
        y = c * np.tanh(y / c)
        shop[a:b] += y
        levels[s["id"]] = dict(src=s["src"], ss=s["ss"], mode=s["audio"], src_rms_db=round(src_rms, 1), gain_db=round(g_db, 1),
                               music_rms_db=round(rms_db(music[a:b]), 1))
    mix = music + shop
    I, tp = lufs(mix)
    g = 10 ** ((-10.0 - I) / 20)
    mix *= g; music_s = music * g; shop_s = shop * g
    # true-peak limiter on the master only (level=disabled keeps the loudness)
    tmp = OUT / "_mix_pre.f32"; tmp.write_bytes(mix.astype(np.float32).tobytes())
    lim = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(tmp), "-af",
                          "alimiter=limit=0.84:attack=3:release=40:level=disabled", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-"],
                         capture_output=True, check=True).stdout
    tmp.unlink()
    master = np.frombuffer(lim, np.float32).reshape(-1, 2).astype(np.float64)
    I2, tp2 = lufs(master)
    write_wav(OUT / "smart450_mix.wav", master)
    write_wav(OUT / "stem_music.wav", music_s)
    write_wav(OUT / "stem_shopsound.wav", shop_s)
    info = dict(master_lufs=I2, master_true_peak_dbtp=tp2, premix_lufs=I, gain_db=20 * np.log10(g), shots=levels,
                note="stems carry the same gain as the master (pre-limiter)")
    (OUT / "audio_levels.json").write_text(json.dumps(info, indent=1))
    print(f"master {I2:.2f} LUFS, true peak {tp2:.2f} dBTP (pre-limit {I:.2f} / {tp:.2f}), gain {20*np.log10(g):.2f} dB")


if __name__ == "__main__":
    main()
