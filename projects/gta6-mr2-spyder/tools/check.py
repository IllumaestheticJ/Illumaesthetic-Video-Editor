"""Pre-send checks (knowledge doc section 10), from the finished reel at delivery size.
    python tools/check.py reel.mp4   -> $W/check/*.jpg + printed event list and audio levels
One frame per purchase (pop-up up), one per whip, the exit and the card; speech band after each purchase."""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np, cv2
from scipy import signal
W = Path("/home/user/media/work/gta6-mr2-spyder"); OUT = W / "check"; OUT.mkdir(exist_ok=True)
reel = sys.argv[1]; meta = json.load(open(W / "shop4_segments.json")); fps = meta["fps"]
cap = cv2.VideoCapture(reel); n = int(cap.get(7)); print("reel frames", n, "timeline frames", meta["frames"], "card", n - meta["frames"])


def grab(f):
    cap.set(1, f); return cap.read()[1]


buys = [g for g, nm in meta["events"] if nm == "purchase"]
for i, g in enumerate(buys):
    cv2.imwrite(str(OUT / f"buy_{i + 1:02d}_f{g + 22}.jpg"), grab(g + 22), [1, 92])
whips = [s for s in meta["segments"] if s["name"].startswith("whip_")]
for i in range(0, len(whips), 6):
    t = [grab(s["out_start"] + 4)[560:1320] for s in whips[i:i + 6]]
    while len(t) < 6: t.append(np.zeros_like(t[0]))
    cv2.imwrite(str(OUT / f"whips_{i // 6}.jpg"), np.vstack([np.hstack(t[:3]), np.hstack(t[3:])]), [1, 90])
ex = next(s for s in meta["segments"] if s["name"] == "exit")
cv2.imwrite(str(OUT / "exit.jpg"), grab(ex["out_start"] + 30), [1, 92]); cv2.imwrite(str(OUT / "card.jpg"), grab(n - 5), [1, 92])
strip = [cv2.resize(grab(f), (270, 480)) for f in np.linspace(5, n - 5, 16).astype(int)]
cv2.imwrite(str(OUT / "strip.jpg"), np.vstack([np.hstack(strip[:8]), np.hstack(strip[8:])]), [1, 88])
# audio
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", reel, "-ar", "48000", "-ac", "2", str(OUT / "a.wav")], check=True)
w = wave.open(str(OUT / "a.wav")); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768
db = lambda v: 20 * np.log10(np.sqrt((v ** 2).mean()) + 1e-9)
sp = signal.sosfiltfilt(signal.butter(4, [300, 3000], "bandpass", fs=sr, output="sos"), x, axis=0)
print("events:", [(round(g / fps, 2), nm) for g, nm in meta["events"]])
print("overall RMS %.1f dB, peak %.3f" % (db(x), np.abs(x).max()))
for g in buys:
    t = g / fps; a = lambda t0, t1: sp[int(t0 * sr):int(t1 * sr)]
    print("purchase %.2f s: speech band before %.1f  at %.1f  0.9-1.5 s after %.1f dB ; L-R at +0.3..0.9: %.1f / %.1f" % (
        t, db(a(t - 0.6, t - 0.3)), db(a(t, t + 0.3)), db(a(t + 0.9, t + 1.5)), db(a(t + 0.3, t + 0.9)[:, 0]), db(a(t + 0.3, t + 0.9)[:, 1])))
lt = next((g / fps for g, nm in meta["events"] if nm == "line"), None)
if lt:
    print("line %.2f s: speech band at line %.1f dB, 1 s before %.1f dB" % (lt, db(sp[int(lt * sr):int((lt + 1.5) * sr)]), db(sp[int((lt - 1.2) * sr):int((lt - 0.2) * sr)])))
