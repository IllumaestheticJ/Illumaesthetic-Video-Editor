# Huracan Evo scan reel v1 - self-review (training/rubric.md)

Output: `/home/user/media/work/out/huracan_evo_v1.mp4` - 1080x1920, 30 fps, yuv420p, AAC 48 kHz, faststart, 40.0 s.
Format: Temerario-style scan-only reel + (user request) Hot Pursuit-style car-select intro: V10 roar + female narrator.

| # | Criterion | Score | Evidence / gap |
|---|---|---|---|
| 1 | Hook | 4 | Engine roar on frame 0 under the fade-up, narrator from 1.8 s, car tracking from the first second. Not a "transformation" hook - this format has no IRL to cut from. |
| 2 | Beat sync | 5 | 8 hard cuts measured on the delivered file (frame diff vs 40-120 Hz kicks in its own audio): +11 +12 +4 +2 +9 +11 -4 +14 ms. Logo lands on the music stop (36.07 s, kick 36.068). Explode starts on the lift (19.28). |
| 3 | 1:1 match | n/a | No IRL in this format. Part-state continuity across s5->s6->s7 checked (bumper off, hood open carried through). |
| 4 | Scan quality | 3 | Silver on black, levelled, ground cropped, no debris islands. Gaps: **hollow wheels** (rims never captured in either the 2026 or 2023 full-car scan), some ragged edges on the composite base under the removed panels, the 3 mm exploded base is softer than the 2 mm hero car. |
| 5 | Story | 4 | Select -> spec sheet -> turntables -> brake/hub detail -> front end opens -> top-down -> explode on the lift -> float -> reassemble -> logo. Follows the Temerario order. |
| 6 | Grade | 4 | One look throughout, car-pixel luma matched to the Temerario crop (median 198 vs 200). n/a for IRL. |
| 7 | Text | 5 | No on-screen text. Narration numbers are sourced (Jan 2019 EVO press release figures; 25M = Full Car STL header 24,999,942); 0-200 left out (unverified). Assumes AWD EVO - flagged to the user. |
| 8 | Ending | 5 | Assembled car fades out, ILLUMAESTHETIC logo (560 px, ref size) on the music stop, track's reverb tail under it, 0.6 s audio fade at the end. |
| 9 | Technical | 4 | Specs correct; every frame lit (scanned all 581 renders for black frames after the persistent-data bug). One cloned frame before each cut (assembler cut hold, as in 240SX). Shots are time-stretched 1.4-5.6 % to fill their slots, so beat-locked part moves drift up to ~0.1 s late by the end of the long shots. |

## Not verified
- I could not listen to the narration (no ASR in the box): length (16.1 s) matches the script, wording/pronunciation unchecked.
- Engine roar is a generated V10 sound, not a recording of this car.

## What the next agent should know
- Cycles `use_persistent_data` drops all lights mid-sequence when objects animate (s5 at the hood swing, s8 during a pure
  translate drift). Scan every rendered frame's max luma before assembling; turn it off for animated-part shots.
- `minterpolate` returns 2N-3 frames from N; set `src_fps = 30*N/(slot+4)` or the assembler clone-pads 3-4 frozen frames before every cut.
- Spherical camera keys through el ~90 deg: keep the top-down branch's image-up identical to the track_quat branch (s6 flipped 180 deg).
