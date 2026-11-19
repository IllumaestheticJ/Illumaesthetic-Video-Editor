"""Assemble v4: shop4.mp4 + closing orbit, 9:16, with the game's own sounds.

    python projects/gta6-customs/tools/assemble4.py [out.mp4]

Sound (user, v3 review: "fix the audio", "the repeating 'need anything else' is annoying, should only do it at the end"):
  * The clip used as the purchase sound in v2/v3 (second capture, 213.8-215.45 s) is the game's purchase chime with the
    mechanic's line starting 0.25 s into it. I cannot hear; the channels show it: the chime is centred (left = right,
    correlation 0.98, bright up to 12 kHz, 213.80-214.72 s); from 214.05 s a speech-band sound comes in 10-15 dB
    louder on the right, with nothing above 4.5 kHz: the mechanic, standing to the right of the camera. He goes on
    after a pause (216.10-216.75, 216.90-217.75, 218.20-219.30 s: three more lines, content unknown to me).
  * Purchase sound now = the two button ticks (213.56-213.80) + the chime: whole until the voice starts, then only its
    part above 4.5 kHz. (v4's first build used left-minus-right for the rest, which is exactly where a right-panned
    voice lives; caught by measuring before delivery.)
  * The mechanic's line (214.00-215.55 s, low-passed at 4.5 kHz to leave the chime out) plays once, at the exit.
  * Room tone bed (first capture, looped with equal-power crossfades) sits 9 dB lower than in v3.
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np, cv2
from scipy import signal

W = Path("/home/user/media/work/gta6-customs")
LOGO = Path("/home/user/Epsilon-Site/showroom/brand/eps-showroom-wordmark-white.png")
ORBIT = W / "orbit"                                            # PNG sequence from kit_render (closing shot), optional
TONE = (1500 / 60, 1888 / 60)
TICKS = {"select": ("a", 274 / 60, 283 / 60), "back": ("a", 1158 / 60, 1164 / 60), "row": ("a", 1276 / 60, 1281 / 60),
         "tab": ("a", 618 / 60, 624 / 60)}                       # tab change: the first capture's option-change tick
TONE_DB, SFX_PEAK = -43.0, 0.45
RADIO = Path("/home/user/media/gta6-customs/radio/radio.wav")   # user's clip of the game's Honey FM (v10 review); optional
RADIO_IN, RADIO_DB, RADIO_DUCK_DB = 2.0, -33.0, -4.0             # start in the clip (music begins there), bed level (RMS), dip under the mechanic's line
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/gta6-customs_v4.mp4")


def read(p):
    w = wave.open(str(p)); sr = w.getframerate(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, ch) / 32768
    return (np.repeat(x, 2, 1) if ch == 1 else x), sr


def purchase_sfx(xb, sr):
    cut = lambda t0, t1: xb[round(t0 * sr):round(t1 * sr)].copy()
    ticks = cut(213.56, 213.80)
    body = cut(213.80, 214.72)
    hp = signal.sosfiltfilt(signal.butter(6, 4500, "highpass", fs=sr, output="sos"), body, axis=0)
    lo = signal.sosfiltfilt(signal.butter(6, 4500, "lowpass", fs=sr, output="sos"), body[:, :1].repeat(2, 1), axis=0)   # left channel: voice-poor
    t = np.arange(len(body)) / sr + 213.80
    lo *= np.clip((214.08 - t) / 0.10, 0, 1)[:, None]            # out before the voice comes in at 214.05-214.10
    chime = hp * 1.3 + lo
    f = int(0.12 * sr); chime[-f:] *= np.linspace(1, 0, f)[:, None] ** 2
    return np.vstack([ticks, chime])


def voice_line(xb, sr):
    v = xb[round(214.00 * sr):round(215.55 * sr)].copy()
    return signal.sosfiltfilt(signal.butter(6, 4500, "lowpass", fs=sr, output="sos"), v, axis=0)


def radio_bed(sr, n, line_t):
    """The in-game radio as the shop would have it: one unbroken piece (never cut inside music), from where the song starts
    in the clip, band-limited like a small speaker, narrowed, with a short room tail, well under the menu sounds."""
    x, rsr = read(RADIO); assert rsr == sr
    x = x[round(RADIO_IN * sr):]
    live = np.nonzero(np.abs(x).max(1) > 0.003)[0]               # the clip ends in silence: fade the music itself, not the silence
    x = x[:live.max() + 1]
    x = signal.sosfiltfilt(signal.butter(2, [180, 4200], "bandpass", fs=sr, output="sos"), x, axis=0)
    mid, side = x.mean(1, keepdims=True), (x[:, :1] - x[:, 1:]) / 2
    x = np.hstack([mid + 0.3 * side, mid - 0.3 * side])
    rng = np.random.default_rng(3); L = int(0.28 * sr)
    ir = rng.standard_normal((L, 2)).astype(np.float32) * np.exp(-np.arange(L) / (0.07 * sr))[:, None]
    ir /= np.sqrt((ir ** 2).sum(0, keepdims=True))
    wet = np.stack([signal.fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in (0, 1)], 1)
    x = x + 0.35 * wet
    x *= 10 ** (RADIO_DB / 20) / np.sqrt((x ** 2).mean())
    x = x[:n]; m = len(x)
    env = np.ones(m, np.float32)
    fi, fo = int(0.5 * sr), int(1.2 * sr)
    env[:fi] *= np.linspace(0, 1, fi); env[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    if line_t is not None:                                         # dip under the mechanic's line
        t = np.arange(m) / sr; d = 10 ** (RADIO_DUCK_DB / 20)
        duck = 1 - (1 - d) * np.clip(np.minimum((t - (line_t - 0.25)) / 0.25, (line_t + 1.9 - t) / 0.4), 0, 1)
        env *= duck
    out = np.zeros((n, 2), np.float32); out[:m] = x * env[:, None]
    return out, m / sr


def audio(extra_s):
    xa, sr = read(W / "a.wav"); xb, _ = read(W / "b.wav")
    meta = json.load(open(W / "shop4_segments.json")); fps = meta["fps"]
    n = round((meta["frames"] / fps + extra_s) * sr); y = np.zeros((n, 2), np.float32)

    def lay(t, src, fin=0.004, fout=0.004):
        src = src.copy(); i0 = max(0, round(t * sr)); src = src[:max(0, n - i0)]
        a, b = min(int(fin * sr), len(src)), min(int(fout * sr), len(src))
        if a: src[:a] *= np.linspace(0, 1, a)[:, None]
        if b: src[-b:] *= np.linspace(1, 0, b)[:, None]
        y[i0:i0 + len(src)] += src

    sfx = purchase_sfx(xb, sr)
    ev = np.zeros_like(y); y, bed = ev, y                         # events first, on their own, to set their level
    for g, name in meta["events"]:
        if name == "purchase":
            lay(g / fps - 0.24, sfx, 0.002, 0.01)                 # the ticks lead in; the chime starts on the purchase frame
        elif name == "line":
            lay(g / fps, voice_line(xb, sr), 0.05, 0.10)
        elif name in TICKS:
            w_, t0, t1 = TICKS[name]; lay(g / fps - 0.01, xa[round(t0 * sr):round(t1 * sr)])
    ev = y * (SFX_PEAK / np.abs(y).max())
    tone = xa[round(TONE[0] * sr):round(TONE[1] * sr)].copy()
    tone *= 10 ** (TONE_DB / 20) / np.sqrt((tone ** 2).mean())
    xf = int(0.4 * sr); k = np.linspace(0, np.pi / 2, xf)[:, None]
    tone[:xf] *= np.sin(k); tone[-xf:] *= np.cos(k)               # equal-power loop joins
    t = 0
    while t < n:
        seg = tone[:n - t]; bed[t:t + len(seg)] += seg; t += len(tone) - xf
    out_y = bed + ev
    if RADIO.exists():
        line_t = next((g / fps for g, nm in meta["events"] if nm == "line"), None)
        rb, rlen = radio_bed(sr, n, line_t); out_y = out_y + rb
        print(f"radio: {rlen:.1f} s from {RADIO_IN:.1f} s of the clip, bed {RADIO_DB:.0f} dB RMS")
    fo = int(1.5 * sr); out_y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    fi = int(0.05 * sr); out_y[:fi] *= np.linspace(0, 1, fi)[:, None]
    out = W / "reel4_audio.wav"
    ww = wave.open(str(out), "w"); ww.setnchannels(2); ww.setsampwidth(2); ww.setframerate(sr)
    ww.writeframes((np.clip(out_y, -1, 1) * 32767).astype(np.int16).tobytes()); ww.close()
    return out, n / sr


def closing():
    """Closing shot, 1080x1920: the orbit render (camera moves, car stands still) with the EPSILON+ wordmark fading in;
    without an orbit render, the plain wordmark card."""
    logo = cv2.imread(str(LOGO), cv2.IMREAD_UNCHANGED).astype(np.float32)
    wl = 760; hl = round(logo.shape[0] * wl / logo.shape[1]); logo = cv2.resize(logo, (wl, hl), interpolation=cv2.INTER_AREA)
    import os                                         # ORBIT=1 to use the orbit render; off by default (user, v5 review:
    frames = sorted(ORBIT.glob("*.png")) if (ORBIT.exists() and os.environ.get("ORBIT") == "1") else []   # a studio orbit on black is not wanted)
    out = W / "closing.mp4"
    n = len(frames) if frames else 75
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    y0, x0 = 330, (1080 - wl) // 2
    for i in range(n):
        if frames:
            im = cv2.resize(cv2.imread(str(frames[i])), (1080, 1920), interpolation=cv2.INTER_CUBIC).astype(np.float32)
            op = float(np.clip((i - n * 0.35) / 20.0, 0, 1))
        else:
            im = np.zeros((1920, 1080, 3), np.float32); op = 1.0; y0 = 920 - hl // 2
        im *= float(np.clip(i / 6.0, 0, 1))                       # up from black
        a = logo[..., 3:] / 255 * op
        im[y0:y0 + hl, x0:x0 + wl] = im[y0:y0 + hl, x0:x0 + wl] * (1 - a) + logo[..., :3] * a
        ff.stdin.write(np.clip(im, 0, 255).astype(np.uint8).tobytes())
    ff.stdin.close(); ff.wait()
    return out, n / 30.0


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    clip, extra = closing(); wav, dur = audio(extra)
    fc = ("[0:v]fps=30,split[a][b];[a]scale=1080:608:flags=lanczos[fg];"
          "[b]scale=-2:1920,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.20:saturation=0.9[bg];"
          "[bg][fg]overlay=0:656,format=yuv420p,setsar=1[reel];"
          "[2:v]fps=30,format=yuv420p,setsar=1[end];[reel][end]concat=n=2:v=1[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "shop4.mp4"), "-i", str(wav), "-i", str(clip),
                    "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
    print(OUT, "seconds", round(dur, 2))


if __name__ == "__main__":
    main()
