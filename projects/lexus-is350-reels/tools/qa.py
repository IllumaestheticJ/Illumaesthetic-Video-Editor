"""QA of the delivered reels (looks at the delivered mp4, not the plan).

    python tools/qa.py [R1 R2 R3]

Writes to /home/user/media/work/is350-reels/out/qa/<rid>/: contact sheet (first/mid/last frame of every shot), +-2-frame strips at every
cut, onion overlays of every 1:1 cut (last IRL frame vs first scan frame), a safe-area report of the graphics overlay (alpha bbox per
second vs x 60-960 / y 220-1500, logo card exempt), first-frame sharpness, loudness (ebur128 on the mp4), cut-to-beat error of the
music stem (largest broadband onset within +-80 ms of each cut), and a faster_whisper transcript of the delivered dialogue.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reels import REELS, OUT, BUILD, NAMES, CAPS, captions, FPS  # noqa: E402

SR = 48000


def frames(mp4, idx):
    idx = sorted(set(i for i in idx if i >= 0))
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-vf", f"select='{sel}'", "-fps_mode", "passthrough", "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, 1920, 1080, 3)
    return dict(zip(idx, arr))


def label(im, txt, scale=1.6):
    im = im.copy(); cv2.putText(im, txt, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), 8); cv2.putText(im, txt, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 255, 255), 3)
    return im


def grid(ims, cols, w=270):
    h = int(w * 1920 / 1080)
    ims = [cv2.resize(i, (w, h), interpolation=cv2.INTER_AREA) for i in ims]
    while len(ims) % cols:
        ims.append(np.zeros_like(ims[0]))
    return np.vstack([np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)])


def music_onsets(wav):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    n = 48  # 1 ms
    e = np.sqrt(np.convolve(x ** 2, np.ones(n) / n, "same") + 1e-12)
    return x, e


def cut_err(e, t):
    """Largest rise of the 1 ms envelope in t-80..t+80 ms: returns (ms offset of the onset, rise dB)."""
    a, b = int((t - 0.08) * SR), int((t + 0.08) * SR)
    seg = 20 * np.log10(e[a:b] + 1e-9)
    d = seg[24:] - seg[:-24]          # rise over 0.5 ms*... 24 samples
    i = int(np.argmax(d))
    return round((a + i + 12) / SR * 1000 - t * 1000, 1), round(float(d[i]), 1)


def qa(rid):
    r = REELS[rid]()
    mp4 = OUT / f"{NAMES[rid]}.mp4"
    q = OUT / "qa" / rid; q.mkdir(parents=True, exist_ok=True)
    rep = {"reel": rid, "file": str(mp4)}
    b = json.loads((BUILD / rid / "build.json").read_text())
    shots = b["shots"]
    cuts = [s["frame"] for s in shots[1:]]
    want = []
    for s in shots:
        want += [s["frame"], s["frame"] + s["frames"] // 2, s["frame"] + s["frames"] - 1]
    for c in cuts:
        want += list(range(c - 2, c + 3))
    F = frames(mp4, want)
    # contact sheet
    ims = []
    for s in shots:
        for k, f in (("first", s["frame"]), ("mid", s["frame"] + s["frames"] // 2), ("last", s["frame"] + s["frames"] - 1)):
            ims.append(label(F[f], f"{s['src']} {k} f{f}", 1.1))
    sheet = grid(ims, 6)
    cv2.imwrite(str(OUT / f"{NAMES[rid]}_contact.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 82])
    # cut strips
    rows = []
    for c in cuts:
        rows.append(grid([label(F[i], f"f{i}" + (" CUT" if i == c else "")) for i in range(c - 2, c + 3)], 5, 216))
    cv2.imwrite(str(q / "cut_strips.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 80])
    # 1:1 onions
    onions = []
    for i, s in enumerate(shots[1:], 1):
        p = shots[i - 1]
        if s["kind"] == "scan" and p["kind"] == "irl":
            A, B = F[s["frame"] - 1], F[s["frame"]]
            ea, eb = cv2.Canny(cv2.cvtColor(A, cv2.COLOR_BGR2GRAY), 60, 160), cv2.Canny(cv2.cvtColor(B, cv2.COLOR_BGR2GRAY), 60, 160)
            ed = np.zeros_like(A); ed[ea > 0] = (0, 0, 255); ed[eb > 0] = (255, 255, 0); ed[(ea > 0) & (eb > 0)] = (255, 255, 255)
            onions.append(np.hstack([cv2.resize(x, (540, 960)) for x in (A, B, cv2.addWeighted(A, 0.5, B, 0.5, 0), ed)]))
    if onions:
        cv2.imwrite(str(q / "onions.jpg"), np.vstack(onions), [cv2.IMWRITE_JPEG_QUALITY, 82])
    # first frame sharpness (variance of Laplacian on the 1080x1920 frame)
    f0 = cv2.cvtColor(F[0], cv2.COLOR_BGR2GRAY)
    rep["first_frame_laplacian_var"] = round(float(cv2.Laplacian(f0, cv2.CV_64F).var()), 1)
    # safe area of the overlay (alpha), sampled every 5 frames, logo card exempt
    gm = BUILD / rid / b["gfx"]
    raw = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(gm), "-vf", "select=not(mod(n\\,5))", "-fps_mode", "passthrough",
                            "-f", "rawvideo", "-pix_fmt", "rgba", "-"], stdout=subprocess.PIPE)
    viol, n = [], 0
    logo = [(it["t0"], it["t1"]) for it in r["items"] if it["kind"] in ("logo", "tease")]  # opaque cards: checked by eye
    while True:
        buf = raw.stdout.read(1080 * 1920 * 4)
        if len(buf) < 1080 * 1920 * 4:
            break
        n0 = n * 5; t = n0 / FPS; n += 1
        if any(round(a * FPS) <= n0 < round(b_ * FPS) for a, b_ in logo):
            continue
        al = np.frombuffer(buf, np.uint8).reshape(1920, 1080, 4)[:, :, 3]
        ys, xs = np.nonzero(al > 8)
        if len(xs):
            bb = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
            if bb[0] < 60 - 6 or bb[2] > 960 + 6 or bb[1] < 220 - 6 or bb[3] > 1500 + 6:   # 6 px: text shadow blur
                viol.append((round(t, 2), bb))
    rep["safe_area_violations"] = viol[:20]; rep["safe_area_checked_frames"] = n
    # loudness of the delivered file
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = o[o.rfind("Summary:"):]
    rep["lufs"] = float(tail.split("I:")[1].split("LUFS")[0]); rep["true_peak_dbfs"] = float(tail.split("Peak:")[1].split("dBFS")[0])
    # cut-to-beat on the music stem (delivered timing = frame of the cut / 30)
    _, e = music_onsets(OUT / f"{NAMES[rid]}_stem_music.wav")
    rep["cuts"] = [{"frame": c, "t": round(c / FPS, 3), "onset_ms": cut_err(e, c / FPS)} for c in cuts]
    # dialogue: transcribe the delivered audio (mix) and list the caption text for comparison
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=2)
        wav = q / "mix16k.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(OUT / f"{NAMES[rid]}_stem_dialogue.wav"), "-ac", "1", "-ar", "16000", str(wav)], check=True)
        aud = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
        segs, _ = m.transcribe(aud, word_timestamps=True, language="en", vad_filter=False)
        words = [(round(w.start, 2), round(w.end, 2), w.word.strip()) for s in segs for w in s.words]
        rep["whisper_dialogue"] = " ".join(w[2] for w in words)
        rep["whisper_words"] = words
    except Exception as ex:  # noqa
        rep["whisper_error"] = repr(ex)
    rep["captions"] = [(c["t0"], c["t1"], " ".join(c["lines"])) for c in captions(r)]
    (q / "qa.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({k: v for k, v in rep.items() if k not in ("whisper_words",)}, indent=1))


if __name__ == "__main__":
    for rid in [a for a in sys.argv[1:] if a in REELS] or list(REELS):
        qa(rid)
