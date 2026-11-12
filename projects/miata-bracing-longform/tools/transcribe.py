import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
import wave, numpy as np
w=wave.open(sys.argv[1]); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
segs, info = m.transcribe(a, word_timestamps=False, vad_filter=True)
out=[]
for s in segs:
    out.append({"start":round(s.start,2),"end":round(s.end,2),"text":s.text.strip()})
    print(f"{s.start:7.2f} {s.end:7.2f} {s.text.strip()}", flush=True)
json.dump(out, open(sys.argv[2],"w"), indent=1)
