"""Check every narration take: duration, pace (words/s) and words against the script (faster-whisper small.en).
usage: vocheck.py <media_dir>   reads vo/L<nn>.(wav|mp3) and vo_lines.json; writes vo/check.json; flags pace outside 2.6-4.3 w/s or word mismatches."""
import sys, os, re, json, glob, subprocess, difflib
import numpy as np
from faster_whisper import WhisperModel
M = sys.argv[1]; H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(f'{H}/vo_lines.json'))
m = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4)
norm = lambda s: re.sub(r"[^a-z0-9' ]", ' ', s.lower().replace('-', ' ')).split()
res = {}
for f in sorted(glob.glob(f'{M}/vo/L*.*')):
    k = re.search(r'L(\d+)\.', f)
    if not k or f.endswith(('.json', '.tsv')): continue
    k = str(int(k.group(1)))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    e = np.abs(a) > 0.01; idx = np.nonzero(e)[0]
    sp = (idx[-1] - idx[0]) / 16000 if len(idx) else 0
    segs, _ = m.transcribe(a, vad_filter=False, condition_on_previous_text=False)
    heard = ' '.join(s.text.strip() for s in segs)
    w, h = norm(L[k]), norm(heard)
    sm = difflib.SequenceMatcher(None, w, h)
    diff = [(' '.join(w[i1:i2]), ' '.join(h[j1:j2])) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
    wps = len(w) / sp if sp else 0
    res[k] = dict(file=os.path.basename(f), dur=round(len(a) / 16000, 2), speech=round(sp, 2), wps=round(wps, 2), diff=diff, heard=heard)
    flag = ('PACE ' if not 2.6 <= wps <= 4.3 else '') + ('WORDS ' + str(diff) if diff else '')
    print(f'L{int(k):02d} {sp:5.1f}s {wps:4.2f} w/s {flag}', flush=True)
json.dump(res, open(f'{M}/vo/check.json', 'w'), indent=1)
print('missing:', sorted(int(k) for k in L if k not in res))
