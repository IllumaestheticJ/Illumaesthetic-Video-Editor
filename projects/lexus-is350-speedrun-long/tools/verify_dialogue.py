"""Verify that no sync line is clipped in the v2 dialogue stem.

    python verify_dialogue.py [stem.wav]

Per sync event of timeline_v2.json: (1) transcribe the stem span (+-0.3 s) with faster_whisper medium.en and align the
intended words (edl_v2 audio.hear) with difflib; report missing words at the start/end; (2) speech-band energy in the
first/last 40 ms of the event vs the line's median: a cut inside a word shows as a loud edge.
Writes out/qa_v2/dialogue_check.json.
"""
import difflib
import json
import re
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt

sys.path.insert(0, str(Path(__file__).parent))
import assemble_long as al  # noqa: E402

STEM = Path(sys.argv[1]) if len(sys.argv) > 1 else al.OUT / "stems_v2/is350_long_v2_stem_dialogue.wav"
Q = al.OUT / "qa_v2"


def norm(s):
    s = s.lower().replace("’", "'")
    s = re.sub(r"\b(\d+)\b", lambda m: {"8": "eight", "32": "thirty-two", "20": "twenty", "15": "fifteen", "30": "thirty",
                                        "10": "ten", "2": "two", "5": "five"}.get(m.group(1), m.group(1)), s)
    s = s.replace("-", " ")
    return re.findall(r"[a-z']+", s)


def main():
    Q.mkdir(parents=True, exist_ok=True)
    tl = json.load(open(al.P / "timeline_v2.json"))
    edl = {e["id"]: e for e in json.load(open(al.P / "edl_v2.json"))["events"]}
    sr, x = wavfile.read(STEM)
    x = x.astype(np.float32)
    x = x[:, 0] if x.ndim > 1 else x
    from faster_whisper import WhisperModel
    model = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=2)
    sos = butter(4, [300, 3400], btype="band", fs=sr, output="sos")
    res = []
    for e in tl["events"]:
        if not e["sync_speech"]:
            continue
        a, b = e["tl_in"], e["tl_out"]
        seg = x[max(0, int((a - 0.3) * sr)):int((b + 0.3) * sr)]
        from scipy.signal import resample_poly
        y16 = resample_poly(seg, 1, 3).astype(np.float32)
        segs, _ = model.transcribe(y16, language="en", beam_size=5, vad_filter=False, condition_on_previous_text=False)
        heard = " ".join(s.text for s in segs)
        hear = edl[e["id"]]["audio"]["hear"] or ""
        if e["id"] == "CON_01":
            hear = hear.split(" 10 minutes")[0]
        want, got = norm(hear), norm(heard)
        sm = difflib.SequenceMatcher(a=want, b=got, autojunk=False)
        blocks = [m for m in sm.get_matching_blocks() if m.size]
        first_ok = bool(blocks) and blocks[0].a <= 1
        last_ok = bool(blocks) and blocks[-1].a + blocks[-1].size >= len(want) - 1
        # edge energy
        z = sosfiltfilt(sos, x[int(a * sr):int(b * sr)])
        n = int(0.04 * sr)
        rms = lambda v: float(np.sqrt(np.mean(v ** 2)) + 1e-9)
        win = int(0.05 * sr)
        frames = [rms(z[i:i + win]) for i in range(0, len(z) - win, win)]
        med = float(np.median(frames)) if frames else 1e-9
        top = float(np.percentile(frames, 90)) if frames else 1e-9
        head_db, tail_db = 20 * np.log10(rms(z[:n]) / top), 20 * np.log10(rms(z[-n:]) / top)
        r = {"id": e["id"], "intended": hear, "heard": heard.strip(), "ratio": round(sm.ratio(), 2),
             "first_word_ok": first_ok, "last_word_ok": last_ok,
             "edge_db_vs_p90": [round(head_db, 1), round(tail_db, 1)],
             "edge_suspect": bool(head_db > -12 or tail_db > -12)}
        r["verdict"] = "OK" if (first_ok and last_ok and not r["edge_suspect"]) else "CHECK"
        res.append(r)
        print(f"{e['id']:7s} {r['verdict']:5s} ratio {r['ratio']:.2f} edges {r['edge_db_vs_p90']} | {r['heard'][:110]}", flush=True)
    al.atomic_json(Q / "dialogue_check.json", res)


if __name__ == "__main__":
    main()
