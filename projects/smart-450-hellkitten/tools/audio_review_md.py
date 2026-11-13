"""Turn out/audio_review_raw.json (tools/audio_review.py) into projects/smart-450-hellkitten/audio_review.md.

Keyword flags are a convenience only: the transcription is machine output (faster-whisper medium.en on the shop-sound stem, quiet
speech is often missed or mangled), so the owner should still listen to every row marked 'speech' and to the 'no speech' spans.
"""
import json, os, re, sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from edit_shots import SM

OUT = Path(SM) / "out"
rows = json.loads((OUT / "audio_review_raw.json").read_text())
levels = json.loads((OUT / "audio_levels.json").read_text())["shots"]
PROFANITY = re.compile(r"\b(fuck\w*|shit\w*|bitch\w*|ass(hole)?|damn\w*|hell|crap|dick\w*|piss\w*|bastard)\b", re.I)
SLUR = re.compile(r"(n[i1]gg|f[a@]gg?[o0]t|retard|chink|spic\b|kike|tranny|dyke)", re.I)
PRICE = re.compile(r"(\$|dollar|bucks|grand\b|thousand|hundred|price|cost\w*|paid|\d{3,})", re.I)


def clean(words):
    t = " ".join(w["w"] for w in words)
    t = re.sub(r"(.)\1{5,}", "[hiss/noise]", t)
    return t.strip()


def flag(text):
    f = []
    if PROFANITY.search(text): f.append("profanity?")
    if SLUR.search(text): f.append("slur?")
    if PRICE.search(text): f.append("price?")
    return ", ".join(f) if f else "none detected"


def fmt(t):
    return f"{t:.2f}"


lines = ["# Audio review: speech audible in the CUT (smart450_v1.mp4)", "",
         "**Machine transcription.** faster-whisper `medium.en` (CPU, int8) run on the shop-sound stem "
         "(`/home/user/media/work/smart-450/out/stem_shopsound.wav`) span by span, each span normalised so quiet speech is not missed, "
         "plus the source clip over the same span for context. Quote marks are what it *sounds like*, not what was said; names are "
         "guesses. The flag column is a keyword scan of both transcripts. It can miss quiet or overlapped words, so listen to every "
         "row. Nothing was censored, cut or muted (owner's note in `feedback.jsonl`).", "",
         "Level in the cut: `under` = shop sound about 14 dB below the music, `up` = about 6 dB below (RMS per shot, see "
         "`audio_levels.json`). Scan shots (S3, S10, S18), the two design stills and the logo carry music only. "
         "Timeline times are seconds in the delivered file.", "",
         "## Rows with speech", "",
         "| timeline (s) | shot | source clip, time (s) | level | sounds like (stem span) | wider source context | profanity / slur / scanner price |",
         "|---|---|---|---|---|---|---|"]
quiet = []
for r in rows:
    stem = clean(r["stem_words"]); ctx = clean(r["src_words_in_span"]); wide = clean([{"w": w} for w in r["src_context"].split()])
    isnoise = lambda t: not re.sub(r"[A-Za-z]?\[hiss/noise\]", "", t).strip(" .,?!-")
    if isnoise(stem) and isnoise(ctx):
        quiet.append(r); continue
    t0, t1 = r["timeline_s"]
    ex = "" if not wide or "[hiss" in wide else f"...{wide[:170]}..."
    lv = levels[r["shot"]]
    lines.append(f"| {fmt(t0)}-{fmt(t1)} | {r['shot']} | {r['src']} {fmt(r['src_s'][0])}-{fmt(r['src_s'][1])} | {r['mode']} ({lv['gain_db']:+.0f} dB gain) | "
                 f"\"{stem or '(nothing)'}\" | {ex} | {flag(stem + ' ' + ctx + ' ' + wide)} |")
lines += ["", "## Spans where no speech was detected (spray hiss, shop noise, handling)", "",
          "| timeline (s) | shot | source clip, time (s) | what the machine heard |", "|---|---|---|---|"]
for r in quiet:
    t0, t1 = r["timeline_s"]
    lines.append(f"| {fmt(t0)}-{fmt(t1)} | {r['shot']} | {r['src']} {fmt(r['src_s'][0])}-{fmt(r['src_s'][1])} | {clean(r['stem_words']) or 'nothing'} (repeated letters = ASR reading noise) |")
lines += ["", "## Notes for the owner", "",
          "- No profanity, slur or price was detected by the keyword scan inside the used spans. That is a statement about this machine "
          "pass only: S9, S14, S15 and S16 come from the bystander-heavy glasses clips (`clips.md` marks them 'do not use' for talk), and "
          "words heard at 14 dB under music are easy to miss. Please listen to S9 (7.50-9.00) and S16 (16.53-18.03) first.",
          "- S16 contains a bystander talking to a named person (sounds like 'Guan' / 'Kwon').",
          "- S1, S2, S4, S5, S11, S12, S13, S17 carry the filmmaker's own narration fragments (a few words each, cut mid-sentence).",
          "- To remove or replace any of it, edit the span in `tools/edit_shots.py` (`audio: None` mutes a shot) and run "
          "`python projects/smart-450-hellkitten/tools/build.py`; the separate shop stem is delivered so it can also be edited in an audio editor."]
(Path(__file__).resolve().parent.parent / "audio_review.md").write_text("\n".join(lines) + "\n")
print("written", len(rows), "spans,", len(quiet), "without speech")
