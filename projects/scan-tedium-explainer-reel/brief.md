# Scan-tedium explainer reel - production brief (2026-11-14)

Owner's ask (verbatim): "are you able to make a reel that does some outside research or even makes an animated section showing how tedious
it normally is to scan a full car (having to use markers or piece together multiple peices of the scan in software). You can do block-style
characters and voices, to frame the problem, and then cut to our scnas to show how fast it can be". Later: "free engine is fine - cartoonish voices".

Deliverable: one 9:16 reel, 1080x1920, 30 fps, 30-40 s (planned 34.0 s). This stage: research + script (2 dialogue versions) + storyboard +
voice test, for owner approval. **No animation or video render until the owner picks a version.**

## Structure
- Part A (0-15.5 s): block-character cartoon of "the usual way": markers stuck all over a car, scanning in overlapping sections, lining the
  pieces up on a laptop while a wall clock spins, peeling every marker off. Ends on "there's got to be a faster way" -> hard cut on a beat.
- Part B (15.5-34.0 s): real IS350 footage (spray, handheld scan), three hard 1:1 real-to-scan cuts (V_PAIR_2, V_PAIR_3, V_MATCH_FRONT),
  V_RES_FULL, logo card with SCANS AVAILABLE AT ILLUMAESTHETIC.COM. Reuses the IS350 reels' intermediates and renders unchanged.

## Facts and rules (use exactly; invent nothing)
- Every number in Part A comes from `research.md` (SOURCED rows only): ~8 cm marker spacing on a car panel, 4+ markers in view per frame,
  3+ matching points per manual alignment, markers random / never in rows. No time figure for the usual way (sources disagree).
- Part B does NOT show the IS350 times (32 min from go / 20 min without the crash): the owner asked that the real time not be given away
  (R3 note, 2026-11-14). "Minutes, not hours" or "the bet: 15 minutes" only if the owner picks it.
- No scanner brand named or mocked ("the usual way", "a lot of scanners"). The IS350 scanner is not named (brands are owner-only).
- No text over real footage beyond what the IS350 reels already do (captions of spoken lines, one top band, safe area: not in the top 220 px,
  bottom 420 px or right 120 px). Part A may carry text freely.
- IRL -> scan = hard 1:1 cut on a beat. Never a dissolve. No shot reused inside the reel.
- Voices: piper-tts, voices whose model-card licence allows commercial use (kristin, john: public domain; joe: CC0), pitch/formant shifted
  into cartoons. Never imitate a real person's voice.
- Music: one piece from the owner-supplied royalty-free mix (`/home/user/media/work/is350-long/music/mix_full.wav`, map in
  projects/lexus-is350-speedrun-long/music.md); one piece for the whole reel.
- Another agent may be rendering: one heavy job at a time, no parallel 4K decodes.

## Files
- `research.md` - sourced research on marker scanning, section alignment, photogrammetry targets, post-processing.
- `script.md` - two dialogue versions (dry / silly), owner decisions, voice licences, voice-test transcription check.
- `storyboard.md` - Part A shots S1-S10 in frames, Part B reuse P1-P10, build options and render estimate.
- `tools/voicetest.py` - voice test generator + faster-whisper check (outputs stay in the scratchpad, never in the repo).
