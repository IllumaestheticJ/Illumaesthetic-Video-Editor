"""Word times of the full Ep 4 dialogue take (faster-whisper medium.en, word_timestamps) -> JSON list [{w,t0,t1,p}].
Usage: python ep4_words.py FULL_AUDIO OUT_JSON"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 capture_output=True).stdout, np.float32)
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, word_timestamps=True, vad_filter=False)
ws = [dict(w=w.word.strip(), t0=round(w.start, 3), t1=round(w.end, 3), p=round(w.probability, 3)) for s in segs for w in s.words]
json.dump(ws, open(sys.argv[2], "w"), indent=0)
print(len(ws), "words")
