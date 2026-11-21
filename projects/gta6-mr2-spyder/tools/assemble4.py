"""Assemble v4: shop4.mp4 + closing orbit, 9:16, with the game's own sounds.

    python projects/gta6-mr2-spyder/tools/assemble4.py [out.mp4]

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

W = Path("/home/user/media/work/gta6-mr2-spyder")
LOGO = Path("/home/user/Epsilon-Site/showroom/brand/eps-showroom-wordmark-white.png")
CARD_BG = Path("/home/user/media/gta6-mr2-spyder/endcard/bg_user.webp")   # end-card background supplied by the user (not in git)
ORBIT = W / "orbit"                                            # PNG sequence from kit_render (closing shot), optional
TONE = (1500 / 60, 1888 / 60)
TICKS = {"select": ("a", 274 / 60, 283 / 60), "back": ("a", 1158 / 60, 1164 / 60), "row": ("a", 1276 / 60, 1281 / 60),
         "tab": ("a", 618 / 60, 624 / 60), "step": ("a", 1276 / 60, 1281 / 60)}                       # tab change: the first capture's option-change tick
TONE_DB, SFX_PEAK = -43.0, 0.45
RADIO = Path("/home/user/media/gta6-mr2-spyder/radio/radio.wav")   # user's clip of the game's Honey FM (v10 review); optional
RADIO_IN, RADIO_DB, RADIO_DUCK_DB = 49.65, -44.0, -4.0     # v3: owner's recording (Dropbox /Moosic, 98.5 s). Start chosen so the music's own break (91.75 s) lands on the cut to the card
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/media/work/out/gta6-mr2-spyder_v4.mp4")


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


# GTA VI logo gradient, top to bottom: medians of the "VI" in the logo shown in the second capture (frame 110), ten bands
VI_GRADIENT = ["#445cc3", "#6f4ac2", "#a241c0", "#dc40be", "#f74fa4", "#fd6693", "#fe747e", "#fe8062", "#fd8e4e", "#fe984a"]
VI_OUTLINE = "#5a1f96"                                         # the logo's purple edge


def vice_card():
    """End card, 1080x1920 BGR float (user, v16/v17 reviews, with two GTA VI key-art references): palm silhouettes on the
    sunset sky of the second reference (violet down through pink to orange; stops sampled from it), the whole EPSILON+
    wordmark in white. Sky and palms are drawn here; nothing of the reference pictures is used but their colours."""
    hexbgr = lambda h: np.array([int(h[5:7], 16), int(h[3:5], 16), int(h[1:3], 16)], np.float32)
    Hc, Wc = 1920, 1080
    t = np.linspace(0, 1, Hc)
    stops = [(0.0, "#6f62a6"), (0.28, "#8f79b0"), (0.48, "#bd8bae"), (0.62, "#e39aa0"), (0.78, "#fbad8c"), (1.0, "#ffbc80")]
    sky = np.stack([np.interp(t, [p for p, _ in stops], [hexbgr(c)[k] for _, c in stops]) for k in range(3)], 1)[:, None, :].repeat(Wc, 1)
    K = 2; m = np.zeros((Hc * K, Wc * K), np.float32); rng = np.random.default_rng(11)
    P_ = lambda p: (int(p[0] * K), int(p[1] * K))

    def palm(base_x, crown, bend, scale):
        """A coconut palm: slim trunk on a gentle curve, a crown of long fronds that arch out and hang, leaflets hanging
        from each frond like a comb (v17's palms had stiff straight fronds and read as stars)."""
        b = np.array([base_x, Hc + 60.0]); c = np.array(crown, np.float32); ctrl = (b + c) / 2 + np.array([bend, 0])
        us = np.linspace(0, 1, 70)
        tr = [(1 - u) ** 2 * b + 2 * u * (1 - u) * ctrl + u ** 2 * c for u in us]
        for a_, b_, u in zip(tr[:-1], tr[1:], us):
            cv2.line(m, P_(a_), P_(b_), 1.0, max(2, int((30 - 16 * u) * scale * K)), cv2.LINE_AA)
        cv2.circle(m, P_(c), int(13 * scale * K), 1.0, -1, cv2.LINE_AA)
        angs = list(np.linspace(-222, 42, 12) + rng.uniform(-8, 8, 12)) + [-78, -108]
        for q, ang in enumerate(angs):
            short = q >= 12
            L = rng.uniform(300, 380) * scale * (0.55 if short else 1.0)
            a0 = np.radians(ang); flat = abs(np.cos(a0))
            droop = (0.10 + 0.42 * flat) * (0.4 if short else 1.0)
            n = 64; uu = np.linspace(0, 1, n)
            sp = [c + np.array([np.cos(a0), np.sin(a0)]) * L * u + np.array([0, droop * L * u ** 2.1]) for u in uu]
            for k_ in range(n - 1):
                a_, b_ = sp[k_], sp[k_ + 1]; u = uu[k_ + 1]
                cv2.line(m, P_(a_), P_(b_), 1.0, max(1, int(7 * scale * K * (1 - u) + 1)), cv2.LINE_AA)
                if u < 0.06:
                    continue
                td = (b_ - a_) / (np.linalg.norm(b_ - a_) + 1e-6); nr = np.array([-td[1], td[0]])
                dn = nr if nr[1] > 0 else -nr                                # the side of the frond that faces the ground
                ll = 0.12 * L * np.sin(np.pi * min(1, u * 1.02)) ** 0.5
                e1 = dn * 0.55 + np.array([0, 0.75]) + td * 0.35; e1 /= np.linalg.norm(e1)
                e2 = -dn * 0.8 + td * 0.75 + np.array([0, 0.25]); e2 /= np.linalg.norm(e2)
                th = max(2, int(4.0 * scale * K))
                cv2.line(m, P_(b_), P_(b_ + e1 * ll), 1.0, th, cv2.LINE_AA)
                cv2.line(m, P_(b_), P_(b_ + e2 * ll * 0.6), 1.0, th, cv2.LINE_AA)

    #      base x, crown (x, y),  bend, scale        two big ones frame the wordmark, smaller ones stand further off
    for bx, cr, bend, sc in ((-40, (215, 330), 150, 1.15), (1010, (900, 250), -170, 1.3), (360, (330, 1010), 60, 0.55),
                             (820, (880, 1180), -40, 0.5), (90, (70, 1260), 30, 0.42), (600, (640, 1420), 20, 0.3)):
        palm(bx, cr, bend, sc)
    m = cv2.resize(np.clip(m, 0, 1), (Wc, Hc), interpolation=cv2.INTER_AREA)[..., None]
    pal = np.stack([np.interp(t, [0, 0.5, 1], [hexbgr(c)[k] for c in ("#5c3b66", "#6f5486", "#6a4960")]) for k in range(3)], 1)[:, None, :]
    card = sky * (1 - 0.82 * m) + pal * (0.82 * m)                              # the reference's palms: mauve, slightly see-through
    if not CARD_BG.exists():                                                     # no stand-in picture: the owner's image or plain black
        print("END CARD: owner's background image missing -> white wordmark on black (placeholder)"); card = np.zeros_like(card)
    if CARD_BG.exists():                                                         # user, v18 review: "use exactly this" (their image)
        bgim = cv2.imread(str(CARD_BG)).astype(np.float32)
        k_ = max(Wc / bgim.shape[1], Hc / bgim.shape[0])
        bgim = cv2.resize(bgim, (round(bgim.shape[1] * k_), round(bgim.shape[0] * k_)), interpolation=cv2.INTER_CUBIC)
        oy, ox = (bgim.shape[0] - Hc) // 2, (bgim.shape[1] - Wc) // 2
        card = bgim[oy:oy + Hc, ox:ox + Wc].copy()
    # wordmark, all white, with a thin plum edge and a soft shadow so it holds against the bright lower sky
    logo = cv2.imread(str(LOGO), cv2.IMREAD_UNCHANGED).astype(np.float32)
    wl = 900; hl = round(logo.shape[0] * wl / logo.shape[1]); al = cv2.resize(logo[..., 3], (wl, hl), interpolation=cv2.INTER_AREA) / 255
    pad = 40; A = cv2.copyMakeBorder(al, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    edge = cv2.GaussianBlur(cv2.dilate(A, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))), (0, 0), 0.8)
    shadow = cv2.GaussianBlur(A, (0, 0), 16) * 0.4
    y0, x0 = 930 - A.shape[0] // 2, (Wc - A.shape[1]) // 2
    reg = card[y0:y0 + A.shape[0], x0:x0 + A.shape[1]]
    for col, mk in ((hexbgr("#4a2a5c"), shadow), (hexbgr("#5a2a78"), edge), (np.array([252, 252, 252], np.float32), A)):
        reg[:] = reg * (1 - mk[..., None]) + col * mk[..., None]
    return card


def closing():
    """Closing card as a clip: the Vice City card, up from black."""
    card = vice_card(); n = 75
    out = W / "closing.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30", "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    cv2.imwrite(str(W / "end_card.png"), np.clip(card, 0, 255).astype(np.uint8))
    for i in range(n):
        ff.stdin.write(np.clip(card * float(np.clip(i / 7.0, 0, 1)), 0, 255).astype(np.uint8).tobytes())
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
