"""Assemble the AESUB spray-gun comment reply (1080x1920, 30 fps).

    python projects/aesub-spray-gun-reply/tools/assemble.py [--out v1.mp4]

Timeline = shots (tools/shots.py) + a compare card + the logo card. Captions are the host's own words (owner OK'd
captions over IRL for this reply), drawn on a dark plate inside the safe zones. Music = the IS350 speed-run music
stem (owner-supplied); its re-entry hit (stem 226.58 s) lands on the cut into the spray montage, and the montage
cuts every 2 beats (0.8 s at 150 BPM). Music ducks under the host's lines.
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

M = Path("/home/user/media/aesub-spray-gun-reply")
SH = M / "shots"
F = M / "fonts"
REPO = Path(__file__).resolve().parents[3]
FPS = 30
W, H = 1080, 1920
BG = (11, 12, 11)          # illumaesthetic.com --bg #0b0c0b
GREEN = (97, 159, 115)     # #619f73
TEXT = (242, 243, 241)     # #f2f3f1
MUTED = (167, 172, 166)    # #a7aca6

MUSIC_HIT = 226.58         # stem time of the re-entry hit
MONTAGE_START = 105        # frame of the cut into the montage (= end of s01)

# (kind, id/name, frames, extra)
TIMELINE = [
    ("shot", "s01_go", None, {"duck": True}),
    ("shot", "s02_front", None, {}),
    ("shot", "s03_mirror", None, {}),
    ("shot", "s04_door", None, {}),
    ("shot", "s05_side", None, {}),
    ("shot", "s07_done", None, {}),
    ("shot", "s08_watch", None, {"hold": 36}),
    ("card", "compare", 108, {}),
    ("shot", "s10_can", None, {"duck": True}),
    ("shot", "s11_civic_gun", None, {}),
    ("shot", "s12_296_can", None, {}),
    ("shot", "s13_296_scan", None, {}),
    ("shot", "s14_cleanup", None, {"duck": True}),
    ("shot", "s15_hood", None, {"duck": True}),
    ("shot", "s16_payoff", None, {"duck": True}),
    ("logo", "logo", 75, {}),
]

# captions: shot id -> [(t0, t1, text)] in shot-local seconds (from the long-form transcript, captions_source_v4.json)
CAPS = {
    "s01_go": [(1.15, 3.50, "Three, two, one, go.")],
    "s10_can": [(0.05, 3.30, "For harder-to-reach areas,\nI'll use the can.")],
    "s14_cleanup": [(0.11, 3.30, "So one thing to note is\nalso cleanup time.")],
    "s15_hood": [(0.11, 5.42, "In that 20 minute span right here,\nmost of the spray is\nalready off the hood")],
    "s16_payoff": [(0.06, 4.05, "20 minutes for the whole car,\n10 minutes if I just\ndid the exterior,"),
                   (4.12, 7.66, "with the power of a spray gun,\nAESUB Violet, and the Artec Leo.")],
}


def font(name, size):
    return ImageFont.truetype(str(F / name), size)


def ease(u):
    u = min(1.0, max(0.0, u))
    return 1 - (1 - u) ** 3


def compare_card(n, out):
    """Two-row comparison, owner's numbers: spray gun 1:55 (stopwatch in the footage), cans only ~9 min."""
    fh = font("FjallaOne.ttf", 64)
    fbig = font("FjallaOne.ttf", 200)
    flab = font("FjallaOne.ttf", 70)
    fsub = font("Barlow-600.ttf", 46)
    tmp = M / "card_frames"
    tmp.mkdir(exist_ok=True)
    for i in range(n):
        t = i / FPS
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)

        def put(txt, f, y, fill, appear, x=None, track=0, anchor="mt"):
            a = ease((t - appear) / 0.25)
            if a <= 0:
                return
            fade = tuple(int(BG[k] + (fill[k] - BG[k]) * a) for k in range(3))
            dy = int((1 - a) * 30)
            d.text((W // 2 if x is None else x, y + dy), txt, font=f, fill=fade, anchor=anchor)

        put("SPRAYING THE WHOLE CAR", fh, 330, MUTED, 0.0)
        # row 1: spray gun
        put("SPRAY GUN", flab, 480, TEXT, 0.15)
        put("1:55", fbig, 570, GREEN, 0.25)
        d.line([(200, 850), (880, 850)], fill=(40, 44, 40), width=3) if t > 0.4 else None
        # row 2: cans
        put("CANS ONLY", flab, 900, TEXT, 0.55)
        put("~9 MIN", fbig, 990, MUTED, 0.65)
        put("AESUB Violet  ·  no wipe-down after", fsub, 1290, MUTED, 0.95)
        im.save(tmp / f"c_{i:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "c_%04d.png"),
                    "-vf", f"fade=t=out:st={n / FPS - 0.2:.3f}:d=0.2:color=0x0b0c0b",
                    "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(out)], check=True)


def caption_png(text):
    f = font("FjallaOne.ttf", 58)
    lines = text.split("\n")
    pad_x, pad_y, gap = 34, 22, 10
    widths = [f.getbbox(l)[2] - f.getbbox(l)[0] for l in lines]
    lh = 70
    bw = max(widths) + 2 * pad_x
    bh = len(lines) * lh + (len(lines) - 1) * gap + 2 * pad_y
    assert bw <= 860, (text, bw)  # x 48..920 safe band, centred plate
    im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=18, fill=(11, 12, 11, 200))
    for k, l in enumerate(lines):
        d.text((bw // 2, pad_y + k * (lh + gap) + lh // 2), l, font=f, fill=TEXT + (255,), anchor="mm")
    return im


def frames_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return int(out.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(M / "out" / "aesub_spray_gun_reply_v1.mp4"))
    a = ap.parse_args()
    out = Path(a.out)
    out.parent.mkdir(exist_ok=True)
    work = M / "build"
    work.mkdir(exist_ok=True)

    # 1. build each segment as a 1080x1920 30 fps video-only file + note its audio source
    segs, boxes = [], []
    t_frame = 0
    for kind, name, n, ex in TIMELINE:
        seg = work / f"{name}.mp4"
        if kind == "shot":
            src = SH / f"{name}.mp4"
            n0 = frames_of(src)
            hold = ex.get("hold", 0)
            vf = "setsar=1"
            if hold:
                vf += f",tpad=stop_mode=clone:stop={hold}"
            n = n0 + hold
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", vf, "-frames:v", str(n), "-an",
                            "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(seg)], check=True)
        elif kind == "card":
            compare_card(n, seg)
        else:
            subprocess.run(["python", str(REPO / "projects/ferrari-296/tools/logo_card.py"),
                            str(REPO / "remotion/public/illumaesthetic_logo.png"), str(seg),
                            "--secs", f"{n / FPS}", "--width", "720", "--bg", "11,12,11"], check=True,
                           capture_output=True)
            n = frames_of(seg)
        segs.append(dict(kind=kind, name=name, path=seg, start=t_frame, n=n, duck=ex.get("duck", False)))
        t_frame += n
    total = t_frame
    print("total frames", total, "=", total / FPS, "s")

    # 2. concat video
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{s['path']}'\n" for s in segs))
    vid = work / "video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vid)],
                   check=True)

    # 3. captions overlay (PNG plates, one overlay per caption with enable windows)
    inputs, filt, last = ["-i", str(vid)], "", "[0:v]"
    k = 0
    for s in segs:
        for (t0, t1, txt) in CAPS.get(s["name"], []):
            png = work / f"cap_{k}.png"
            im = caption_png(txt)
            im.save(png)
            x = (W - im.width) // 2
            x = min(x, 920 - im.width) if x + im.width > 920 else x
            x = max(48, (48 + 920 - im.width) // 2)
            y = 1420 - im.height  # bottom edge at y 1420 (< 1440 safe line)
            g0 = s["start"] / FPS + t0
            g1 = s["start"] / FPS + t1
            boxes.append(dict(t0=round(g0, 3), t1=round(g1, 3), x=x, y=y, w=im.width, h=im.height, text=txt,
                              readable=round(t1 - t0, 2)))
            inputs += ["-loop", "1", "-i", str(png)]
            filt += (f"{last}[{k + 1}:v]overlay={x}:{y}:enable='between(t,{g0:.3f},{g1:.3f})'"
                     f"[v{k}];")
            last = f"[v{k}]"
            k += 1
    # card text boxes for the safe-zone check
    for s in segs:
        if s["kind"] == "card":
            boxes.append(dict(t0=s["start"] / FPS, t1=(s["start"] + s["n"]) / FPS, x=180, y=320, w=720, h=1040,
                              text="compare card", key=True))
    json.dump(boxes, open(work / "text_boxes.json", "w"), indent=1)

    # 4. audio: dialogue bed (shot audio at its place) + music with ducking
    sr = 48000
    nsamp = int(round(total / FPS * sr))
    dia = np.zeros((nsamp, 2), np.float32)
    duck = np.zeros(nsamp, np.float32)
    for s in segs:
        if s["kind"] == "shot":
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SH / f"{s['name']}.mp4"), "-vn", "-ac", "2",
                                  "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
            i0 = int(round(s["start"] / FPS * sr))
            if raw:
                x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
                x = x[: int(round(s["n"] / FPS * sr))]
                # 10 ms fades at the shot edges to avoid clicks
                f = min(480, len(x) // 2)
                ramp = np.linspace(0, 1, f, dtype=np.float32)[:, None]
                x[:f] *= ramp
                x[-f:] *= ramp[::-1]
                dia[i0:i0 + len(x)] += x
            if s["duck"]:
                duck[i0:i0 + int(round(s["n"] / FPS * sr))] = 1
    # dialogue gain: normalise speech peaks to about -3 dBFS
    pk = np.max(np.abs(dia)) + 1e-9
    dia *= 10 ** (-3 / 20) / pk
    # music
    m_start = MUSIC_HIT - MONTAGE_START / FPS
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{m_start:.4f}", "-t", f"{total / FPS + 0.5:.3f}", "-i",
                          str(M / "src" / "is350_music.wav"), "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True).stdout
    mus = np.frombuffer(raw, np.float32).reshape(-1, 2)[:nsamp].copy()
    if len(mus) < nsamp:
        mus = np.vstack([mus, np.zeros((nsamp - len(mus), 2), np.float32)])
    # smooth duck envelope (150 ms ramps); ducked = -13 dB
    w = int(0.15 * sr)
    duck_s = np.convolve(duck, np.ones(w) / w, "same")
    g = 10 ** ((-13 * duck_s) / 20)
    # logo: fade the music out over the logo card
    logo = segs[-1]
    l0 = int(round(logo["start"] / FPS * sr))
    fade = np.ones(nsamp, np.float32)
    fade[l0:] = np.linspace(1, 0, nsamp - l0) ** 1.5
    mus *= (g * fade)[:, None] * 0.9
    mix = dia + mus
    wav = work / "mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_f32le", str(wav)], input=mix.astype(np.float32).tobytes(), check=True)
    # loudness: measure, then one static gain to about -14 LUFS with true peak < -1 dBFS
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", "ebur128=peak=true", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    I = float(meas.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])
    TP = float(meas.split("True peak:")[1].split("Peak:")[1].split("dBFS")[0])
    gain = -14 - I  # peaks handled by the limiter below
    print(f"mix {I:.1f} LUFS, TP {TP:.1f} dBFS -> gain {gain:+.1f} dB")

    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-i", str(wav), "-filter_complex",
                                                      filt + f"{last}null[vout];[{k + 1}:a]volume={gain:.2f}dB,alimiter=limit=0.79:attack=3:release=60:level=disabled[aout]",
                                                      "-map", "[vout]", "-map", "[aout]", "-frames:v", str(total),
                                                      "-c:v", "libx264", "-crf", "16", "-preset", "slow",
                                                      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                                                      "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    json.dump([{k2: (str(v) if isinstance(v, Path) else v) for k2, v in s.items()} for s in segs],
              open(work / "segments.json", "w"), indent=1)
    print(out)


if __name__ == "__main__":
    main()
