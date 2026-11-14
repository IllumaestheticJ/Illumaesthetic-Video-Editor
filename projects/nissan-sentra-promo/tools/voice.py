"""Build the narration track from the Higgsfield take + two re-recorded lines, with planned gaps.
Writes voice.wav (48 kHz stereo) and timing.json (line windows in the output). Usage: voice.py <voice_dir> <project_dir>"""
import json, subprocess, sys, numpy as np
V, P = sys.argv[1], sys.argv[2]
SR = 48000
def load(f):
    a = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{V}/{f}', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(a, np.int16).astype(np.float32) / 32768
src = {k: load(k + '.wav') for k in ['take', 'hook2', 'brake2']}
# (text, source, t0, t1, gap after) - windows from the voiced-segment map + whisper check (see editlog)
L = [
 ("let's build a 2026 nissan sentra SR", 'hook2', 1.32, 5.20, 0.40),
 ("using nothing but scan data", 'take', 3.94, 5.90, 0.50),
 ("but to make parts that actually fit", 'take', 6.45, 8.44, 0.40),
 ("you need the real car, in 3D", 'take', 9.02, 11.16, 0.60),
 ("so first, we scan the whole car", 'take', 11.65, 13.97, 0.90),
 ("every body line", 'take', 14.48, 15.56, 0.50),
 ("every panel gap", 'take', 16.09, 17.18, 0.60),
 ("then the engine bay, on its own", 'take', 17.64, 19.81, 0.90),
 ("and the fog lights", 'take', 20.43, 21.41, 0.70),
 ("now we design on top of it", 'take', 21.77, 23.24, 0.60),
 ("a new front bumper", 'take', 23.76, 24.86, 0.50),
 ("with its own fog ducts", 'take', 25.35, 26.61, 0.60),
 ("wider fenders and a new hood", 'take', 27.06, 28.90, 0.60),
 ("side skirts", 'take', 29.60, 30.54, 0.50),
 ("rear quarter panels", 'take', 31.31, 32.45, 0.50),
 ("a diffuser", 'take', 32.93, 33.68, 0.50),
 ("and a wing", 'take', 34.48, 35.12, 0.80),
 ("even the brake adapters", 'brake2', 1.70, 3.20, 0.35),
 ("revised until they fit", 'take', 36.92, 38.30, 0.90),
 ("this is the sentra scan data", 'take', 38.92, 40.72, 0.60),
 ("get it on illumaesthetic.com", 'take', 41.23, 43.18, 0.0),
]
lead = 0.25
out = [np.zeros(int(lead * SR), np.float32)]; t = lead; timing = []
for text, s, a, b, gap in L:
    seg = src[s][int(a * SR):int(b * SR)].copy()
    f = int(0.008 * SR); r = np.linspace(0, 1, f, dtype=np.float32)
    seg[:f] *= r; seg[-f:] *= r[::-1]
    timing.append({'text': text, 'start': round(t, 3), 'end': round(t + len(seg) / SR, 3), 'src': s, 'in': a, 'out': b})
    out += [seg, np.zeros(int(gap * SR), np.float32)]; t += len(seg) / SR + gap
y = np.concatenate(out)
peak = np.abs(y).max(); print('peak', peak, 'dur', len(y) / SR)
pcm = (np.stack([y, y], 1) * 32767).astype(np.int16)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', f'{V}/voice.wav'], input=pcm.tobytes(), check=True)
json.dump({'voice_end': round(t, 3), 'lines': timing}, open(f'{P}/timing.json', 'w'), indent=1)
for x in timing: print(f"{x['start']:6.2f}-{x['end']:6.2f} {x['text']}")
