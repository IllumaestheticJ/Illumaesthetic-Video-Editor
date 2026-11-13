"""Transcribe every wav/<stem>.wav that has no tx/<stem>.json yet (faster-whisper small.en, CPU).
usage: transcribe_all.py <media_dir> [threads]   Writes tx/<stem>.json (segments) and rewrites transcripts.txt (all clips with speech)."""
import sys, os, json, glob, wave
import numpy as np
from faster_whisper import WhisperModel
M = sys.argv[1]; T = int(sys.argv[2]) if len(sys.argv) > 2 else 2
os.makedirs(f'{M}/tx', exist_ok=True)
m = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=T)
for w in sorted(glob.glob(f'{M}/wav/*.wav')):
    stem = os.path.basename(w)[:-4]; o = f'{M}/tx/{stem}.json'
    if os.path.exists(o): continue
    f = wave.open(w); a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, vad_filter=True, condition_on_previous_text=False)
    out = [dict(start=round(s.start, 2), end=round(s.end, 2), text=s.text.strip(), nsp=round(s.no_speech_prob, 2)) for s in segs]
    json.dump(out, open(o, 'w'), indent=1); print(stem, len(out), flush=True)
with open(f'{M}/transcripts.txt', 'w') as f:
    for o in sorted(glob.glob(f'{M}/tx/*.json')):
        s = json.load(open(o))
        if not s: continue
        f.write(f'## {os.path.basename(o)[:-5]}\n' + ''.join(f"{x['start']:7.1f} {x['text']}\n" for x in s) + '\n')
