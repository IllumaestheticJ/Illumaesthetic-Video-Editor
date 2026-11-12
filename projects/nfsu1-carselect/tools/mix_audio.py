"""Get Low with the game's car and menu sounds on top.   python mix_audio.py <getlow.wav> <out.wav> [music_start_s]
The capture audio (a.wav, 60 fps frame clock, reel starts at capture frame 966) carries the engine/menu sounds baked with the
capture's own menu music, so it is kept at full level only while a car is changing (menu flip -> drive-away -> drive-in ->
settle) and pulled down in the holds, where there is only menu music."""
import sys, subprocess, numpy as np, wave
WORK = "/home/user/media/work/nfsu1-carselect"
def rd(p):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "2", "-ar", "48000", "/tmp/_m.wav"], check=True)
    w = wave.open("/tmp/_m.wav"); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2) / 32768.0
SR = 48000; START = 966; N = int((653 + 60) / 30 * SR)
ss = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
g = rd(f"{WORK}/a.wav")[int(START / 60 * SR):][:N]; m = rd(sys.argv[1])[int(ss * SR):][:N]
HOLDS = [(1058, 1162), (1406, 1501), (1745, 1821), (2065, 2120)]            # capture frames: settled -> next menu flip
t = np.arange(N) / SR; env = np.ones(N); R = 0.12
for a, b in HOLDS:
    a = (a - START) / 60; b = (b - START) / 60
    env = np.minimum(env, 1 - 0.75 * np.clip((t - a) / R, 0, 1) * np.clip((b - t) / R, 0, 1))
env *= np.clip((653 / 30 + 0.3 - t) / 0.3, 0, 1)                             # game audio out as the logo card starts
rms = lambda x: np.sqrt((x ** 2).mean())
g = g * (0.9 * rms(m) / rms(g)); out = 0.8 * m + g * env[:, None]
out = np.tanh(out) * 0.97                                                  # soft limit, never past full scale
print("levels: music", rms(0.8 * m).round(3), "game", rms(g * env[:, None]).round(3), "peak", np.abs(out).max().round(3))
w = wave.open(sys.argv[2], "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
