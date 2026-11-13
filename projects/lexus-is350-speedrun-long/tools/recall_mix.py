"""Speech recall on the full mix vs the dialogue stem, per sync line (faster_whisper medium.en).
    IS350_VER=v5 python recall_mix.py  -> out/qa_<ver>/recall_mix.json"""
import json, os, re, sys
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
sys.path.insert(0, str(Path(__file__).parent))
import assemble_long as al
VER = os.environ.get("IS350_VER", "v5")
tl = json.load(open(al.P / f"timeline_{VER}.json"))
def load(p):
    sr, x = wavfile.read(p); x = x.astype(np.float32)
    if x.dtype != np.float32 or np.abs(x).max() > 2: pass
    x = x.mean(1) if x.ndim > 1 else x
    if np.abs(x).max() > 2: x = x / 8388608.0 if np.abs(x).max() > 40000 else x / 32768.0
    return sr, x
srs, stem = load(al.OUT / f"stems_{VER}/is350_long_{VER}_stem_dialogue.wav")
srm, mix = load(al.OUT / f"is350_long_{VER}_mix.wav")
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=3)
def words(sr, x, a, b):
    seg = x[max(0, int((a - 0.2) * sr)):int((b + 0.2) * sr)]
    y = resample_poly(seg, 1, sr // 16000).astype(np.float32)
    s, _ = m.transcribe(y, language="en", beam_size=5, condition_on_previous_text=False)
    return re.findall(r"[a-z0-9']+", " ".join(t.text for t in s).lower())
res = []
for e in tl["events"]:
    if not e["sync_speech"] or (os.environ.get("ONLY") and e["id"] not in os.environ["ONLY"].split(",")):
        continue
    ws, wm = words(srs, stem, e["tl_in"], e["tl_out"]), words(srm, mix, e["tl_in"], e["tl_out"])
    from collections import Counter
    cs, cm = Counter(ws), Counter(wm)
    hit = sum(min(cs[w], cm[w]) for w in cs)
    r = hit / max(1, len(ws))
    res.append({"id": e["id"], "stem_words": len(ws), "mix_recall": round(r, 2), "stem": " ".join(ws), "mix": " ".join(wm)})
    print(f"{e['id']:7s} recall {r:.2f} ({hit}/{len(ws)})", flush=True)
tot = sum(x["stem_words"] for x in res); rec = sum(x["mix_recall"] * x["stem_words"] for x in res) / tot
print("OVERALL word recall mix vs stem", round(rec, 3))
al.atomic_json(al.OUT / f"qa_{VER}/recall_mix{'_' + os.environ['ONLY'].replace(',', '_') if os.environ.get('ONLY') else ''}.json", {"overall": rec, "lines": res})
