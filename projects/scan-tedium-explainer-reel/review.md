# Scan-tedium explainer reel - self-review, full reel v1 (2026-11-15)

File: `/home/user/media/work/scan-tedium/out/explainer_full_v1.mp4` (copy in `preview/`). Build: `tools/full_build.py --gfx --audio --video --mux`.
1080x1920, 30 fps, H.264 High yuv420p + AAC 256k 48 kHz, faststart. 1210 frames = 40.33 s.

| part | frames | time (s) | content |
|---|---|---|---|
| Part A | 0-988 (989) | 0.00-32.97 | partA_v5 as delivered, captions added |
| P2 | 989-1026 (38) | 32.97-34.23 | FX30541 src 7720-7750 (322.0-323.24 s), R1_SCAN 4K-graded intermediate, x0 600 -> ~640 (R1 keyframes) |
| P7 | 1027-1064 (38) | 34.23-35.50 | FX30554 src 234-264 (9.76-11.01 s), ends on the solved frame 264, x0 531 |
| P8 | 1065-1140 (76) | 35.50-38.03 | V_MATCH_FRONT vertical render (`_preview.mp4` frames 0-75), hard 1:1 cut |
| card | 1141-1209 (69) | 38.03-40.33 | HOW LONG / DID IT TAKE? + sage bar + FULL VIDEO ON OUR CHANNEL (R3 v3) |

Part B = 152 frames = 5.07 s (owner relaxed the 5.0 s cap to a target; the 2 extra frames put the card on a bar line).

| # | criterion | score | notes |
|---|---|---|---|
| 1 | Hook | 4 | unchanged Part A opening (Pip's question from 0.2 s, first caption at 0.2 s) |
| 2 | Beat sync | 5 | music P8 (mix_full.wav 1136.206-1176.540 s). Hand-off, P2->P7, 1:1 and card cuts all within 10 ms of the decoded onsets (broadband half-rise -0.1..+1.1 ms) |
| 3 | 1:1 match | 5 | the R2/R3 front pair (16:9 RMSE 0.4 px); onion of frames 1064/1065 (`preview/explainer_full_v1_match.jpg`): grille, plate, emblem, mirror, hood edges coincide; cut on bar 3 after the drop |
| 4 | Scan quality | 4 | approved render; grille mesh partly ragged as in R2/R3 |
| 5 | Story | 4 | cartoon problem -> phone -> real scanning -> real car -> its scan -> tease. No spray shot (cut for length) |
| 6 | Grade | 5 | hand-off invisible: frame 988 = src 7719 crop (MAD 1.99 vs the intermediate), 988->989 frame difference 5.7 = natural 989->990 (5.9); same LUT for both IRL shots |
| 7 | Text | 4 | only captions (Part A) + the card; none in Part B, none within 30 px of the phone screen (checked every frame), all inside x 55-945 / y 215-1500. Word-by-word, script wording, "Illumaesthetic". Plate behind captions was needed for sage-on-sage legibility |
| 8 | Ending | 4 | ends on the FULL VIDEO card as the owner asked (no logo card), 1.5 s music fade to the end |
| 9 | Technical | 5 | -14.0 LUFS integrated, true peak -2.1 dBTP, LRA 2.0 LU; dialogue -14.0 vs music -26.6 LUFS in Part A. Duplicate frames in P2/P7 are the 23.976 -> 30 cadence of the source (as in R1-R3), none at a cut |

Not verified: nobody (me included) has listened to the mix; music choice and duck depth are measured, not heard. P8's tonality/mood is from the earlier analysis (G/C major, bright), not by ear.
Left out on purpose: the "A DOT EVERY ~8 CM" label, any time/answer, the logo card, the spray shot (P1) and the full-scan hero (V_RES_FULL), Part B voice-over, room sound in Part B.

## explainer_full_v2 (2026-11-16, agent self-check)
- 1232 frames / 41.07 s. Part A 0-988 unchanged; Part B 989-1132 (4.8 s, re-timed to 18-frame beats); teaser card 1133-1231 (3.3 s).
- Music: inquisitive_A (100.00 BPM). Real lift = bass entry bar 8 (19.22 s), aligned to frame 989 (bass attack measured at 32.985 s in the stem).
  1:1 cut 1061 and card 1133 on bar downbeats. Intro lengthened with three 2-bar loops; post-lift unedited, 1.5 s fade (track ending not reachable
  seamlessly in 3 bars - see editlog).
- No text over IRL: overlay alpha max = 0 over P2/P7 and over the teaser window interior (automated, picture.json) + checked by eye.
- Card legible at 540 px wide; CTA cap ~57 px vs headline ~76 px.
- Loudness (final AAC): -14.1 LUFS integrated, -2.0 dBTP, LRA 2.3 LU.
- Not verified: by ear - the splice inaudibility and the dialogue/music balance are measured only (splice spectral scores, v1 ducking curve).
