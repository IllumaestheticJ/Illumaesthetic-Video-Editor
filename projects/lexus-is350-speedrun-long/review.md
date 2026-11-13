# L1 rough assembly v1 - editor self-review (training/rubric.md)

Output: /home/user/media/work/is350-long/out/is350_long_v1_rough.mp4 (5:06.81, 7356 f @ 23.976, H.264 crf 18, AAC 320k),
mix WAV + stems (dialogue / music / fx_room, float32) in out/, QA in out/qa/. Rebuild: `python projects/lexus-is350-speedrun-long/tools/assemble_long.py`.

- Story/structure: EDL followed; E41 dropped (no cabin geometry), E71 = conclusion Version A. 4/5
- 1:1 cuts: E32|E33 and E66|E67 hard, last IRL frame = solved frame, crop_y 0; preview first frames align with the onion (outline overlay checked). Final renders pending. 3/5 until finals land.
- Pacing/music: 40/74 cuts on measured kick attacks; the rest are sync-word-bound, room-tone or anchors. Lift on the front 1:1 cut. Downbeats chosen from accent strength, not by ear. 3/5
- Blur: tracked plates in E12, E15, E21, E22, E32, E45, E61, E66; crop hides plates in E50 and CON_03. Checked frame by frame on tracker sheets plus final-file sheets out/qa/blur_*.jpg. 4/5
- Audio: -14.0 LUFS integrated, -1.8 dBTP, LRA 4.0; dialogue lines -10.4 to -15.3 LUFS each after the bus (E13 hottest); no silence over 0.3 s below -50 dB. 4/5
- Placeholders: every scan shot is a 4-key preview slideshow with a red PLACEHOLDER tag (no render done yet). 2/5 (expected)
- Known defects: see editlog / final report.

---

# FINAL (v3) - editor self-review, 2026-11-13 (training/rubric.md)

Delivered: /home/user/media/work/is350-long/out/final/ (1080p master, 1440p YouTube, 1080p no-captions, mix + 3 float stems, captions_v3.srt/.vtt, README.txt).
5:04.846, 7309 frames, -14.1 LUFS / -1.5 dBTP / LRA 6.1. Rebuild: `python projects/lexus-is350-speedrun-long/tools/assemble_long.py --edl edl_v2.json --ver v3 plan final`.

| # | criterion | score | evidence / why not 5 |
|---|---|---|---|
| 1 | Hook | 3 | Opens on the "two hours" guess (owner: scans only at the end), not on a transformation; first frame is a camera move. |
| 2 | Beat sync | 3 | 40 snapped cuts measured on the delivered file: median 0.59 frames off the kick, 31/40 within 1 frame, worst 2 frames. The hard-parts section (P4) has a weak grid (only 44 % of kicks on it), and dialogue-protected cuts can only grow, so some cuts are 1-2 frames off. Never verified by ear. |
| 3 | 1:1 match | 4 | All 4 montage pairs: delivered IRL frame = solved frame (PSNR 38.9-40.7 dB), first scan frame = render f1 (38.8-39.5 dB); cut on the kick. Rear solve is 5.9 px RMSE (3D agent). A one-frame seek bug (ffmpeg duplicated the first decoded frame) was found and fixed during v2 QA. |
| 4 | Scan quality | 3 | Finished renders everywhere (no placeholders). The ragged rear-left wheel well shows briefly in SC_RES_FULL; the mesh is as delivered. |
| 5 | Story | 4 | Bet -> spray (time-lapse to the 01:55 phone) -> scan -> crash set-piece -> restart -> hard parts -> time -> results card -> real-to-scan montage -> host's answer. |
| 6 | Grade | 3 | One LUT (FX3A S-Log3 -> 709) on every IRL shot, but sourced from 1080p proxies (4K only for 545); daylight shots run hot in places. |
| 7 | Text | 3 | Overlays on IRL by owner's explicit v2 choice; numbers are legible faces, the owner's 32/20, or flagged derived values. Open wording item: the scoreboard says "RESTARTED AFTER THE CRASH", the conclusion card says "WITHOUT THE CRASH" (owner's own phrase is "20 minutes without the crash"); left as rendered per the lead. |
| 8 | Ending | 4 | The P8 final hit lands on the end card (0 ms); the ring decays to silence over the logo (~3.9 s below -50 dB at the very end). |
| 9 | Technical | 4 | 16:9 long-form (rubric's 9:16 spec does not apply); High, yuv420p, bt709, 23.976, AAC 320k, faststart; all exports decode with 0 errors, 7309 frames each. |

Honest gaps:
- **Nobody has listened to the mix.** Music edits, the crash cue, the freeze SFX, ducking and dialogue clarity were all checked only by measurement (ebur128, onset detection, whisper transcripts).
- **The spray time-lapse is smeary**: a 20.8x frame-blended ramp (180-degree shutter) reads as motion blur rather than crisp steps.
- **Hard-parts music grid is weak** (see 2).
- **1080p-proxy sourcing**: all IRL except FX30545 comes from 1080p 10-bit proxies of the 4K originals; the 1440p deliverable is an upscale.
- Faint second-speaker replies ("Yeah, I know", "I do the same thing all the time") are present but quiet; per-line loudness spread is 0.2 LU at line level, not per speaker.
- Music licence (owner-supplied third-party mix) is not cleared for YouTube; it sits alone on the music stem.
