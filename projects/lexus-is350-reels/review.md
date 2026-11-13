# IS350 reels R1 / R2 / R3: editor review (v1, 2026-11-13)

Outputs `/home/user/media/work/is350-reels/out/`: `is350_reel_R1_crash.mp4`, `is350_reel_R2_real_to_scan.mp4`, `is350_reel_R3_how_long.mp4`
(1080x1920, 30 fps, H.264 High CRF 17 yuv420p bt709, AAC 256 kbit/s 48 kHz, faststart) + `*_stem_music.wav`, `*_stem_dialogue.wav`,
`*_stem_room.wav`, `*_mix.wav`, `*_contact.jpg`; QA in `out/qa/<R>/` (cut strips, 1:1 onions, qa.json with the whisper transcript).
Copies of the mp4s and contact sheets in `preview/`. Rebuild: `python projects/lexus-is350-reels/tools/build.py` (then `tools/qa.py`).
Direction: `direction.md` (plan) + "As built" below. Timelines are code: `tools/reels.py`; spans and crop keyframes: `spans.json`.

## As built (differences from direction.md)
- **R1 30.17 s (905 f)**: bet (4.45) -> "Three, two, one, go" (3.6) -> spray (1.2) -> scanning (1.6) -> crash (6.55) -> "Start a secondary timer. Now." (2.35)
  -> "20 minutes." (1.6) -> "And the other one, 32 minutes." (4.4) -> V_RES_FULL + result card (2.8) -> logo + CTA (1.6).
  Built to the music agent's P4 piece: the calm bars start 0.99 s in so the k46 bar line lands on "go" (7.39); the agent's wind-up stem (last 6.48 s
  of it) runs from "go" to its **dead stop exactly on "crashed" (13.87)**; 5.08 s of silence under the crash lines; the comeback drop lands on "Now." (18.95);
  8 extra beats from the same piece (P4 k286-294, RMS-matched) carry the result; the agent's built ending hits on the logo (28.55).
  "Done." (553 11.8) is cut out between "20 minutes." and "And the other one" (both cut points in measured silence).
- **R2 19.43 s (583 f)**: rear bumper -> rear quarter -> hood -> front walk-out (four 1:1 cuts) -> V_RES_FULL -> logo. Order changed: the rear-quarter lead-in
  opens on a pan blur in the 3D agent's window, the rear bumper is steady (first frame sharp). Music = the agent's R2 optB with one 8-beat groove block
  removed (9.73-12.97, its documented edit) so the 2-bar kick-out lull carries the 3.2 s front walk-out and **D2 lands on the front 1:1 cut (12.97)**.
- **R3 26.43 s (793 f)**: question (J-cut over the clean car) -> three answers with pills -> 7 one-beat process shots -> "Is this the most optimal scanning
  position?" -> "Time." -> front walk-out -> **muted beat, then the boom on the 1:1 cut (19.31)** -> V_RES_FULL with the answer card -> logo.
  Built from the agent's straight P6 stem with the mute + boom moved to bar 7 (19.31) and its built ending on the logo (24.83).
- Pair windows are the 3D agent's (`scan_shots.md`: x0 531 / 150 / 480 / 850), used unchanged on the IRL side; every lead-in ends on the solved frame
  (frame map `match_f - round((N-1-j)*23.976/30)`, verified: last IRL frame = source f264 / f5401 / f1135 / f5641).

## Measured (delivered files)
| | R1 | R2 | R3 |
|---|---|---|---|
| length | 30.17 s | 19.43 s | 26.43 s |
| loudness / true peak | -10.2 LUFS / -2.3 dBTP | -10.2 / -2.5 | -10.1 / -2.2 |
| first frame (Laplacian var.) | 194 (sharp) | 109 (sharp) | 282 (sharp) |
| overlays outside x 60-960, y 220-1500 | none | none | none |
| cut vs music lattice (by construction) | dialogue cuts free; go / crashed / Now / logo on anchors (<= 17 ms frame rounding) | all on bar/beat lines (<= 17 ms) | all on beat lines (<= 17 ms) |
| cut vs largest music onset +-80 ms (qa.json) | -47..+63 ms (most cuts are dialogue cuts) | -50..+77 ms; D1 -11, D2 +7, logo -2 | -64..+75 ms; answer hit -0.2 ms |
| dialogue re-transcribed (medium.en on the dialogue stem) | every kept line complete | no speech kept | every kept line complete |

Onset offsets on R2/R3 are measured on dense music (R3: swung 16ths, the agent rates its grid "weak"); I read them as measurement ambiguity, not drift:
the cuts sit on the agent's lattice to the frame. Nobody has listened to the mixes.

## Self-score (training/rubric.md)
| # | criterion | R1 | R2 | R3 | note |
|---|---|---|---|---|---|
| 1 | Hook | 4 | 5 | 4 | R1/R3 open on the question on screen + a face / the clean car; R2 transforms at 1.6 s |
| 2 | Beat sync | 3 | 5 | 4 | R1 is dialogue-led: only the music anchors are on beats |
| 3 | 1:1 match | - | 4 | 4 | front and hood checked in onions (grille, headlamp, hood edge coincide); rear and rear-quarter not yet seen with renders |
| 4 | Scan quality | ? | ? | ? | 3D agent's renders; V_RES_FULL not delivered at build time |
| 5 | Story | 4 | 4 | 4 | each stands alone: question, bet, crash, answer / real -> scan + result / question, guesses, process, answer |
| 6 | Grade | 4 | 4 | 4 | one LUT on all IRL (S-Log3 -> 709); 553/554 sun shots are hot |
| 7 | Text | 4 | 4 | 4 | only 32 / 20 / 15 and legible clock values; owner-approved overlays on IRL; content-sized plates |
| 8 | Ending | 4 | 4 | 4 | logo 780 px + CTA, 1.6 s, on the music's final hit |
| 9 | Technical | 5 | 5 | 5 | frame-exact assembler, no dropped/duplicated frames at cuts (intermediates verified against the proxies) |

## Weaknesses I can see
- R1 is 30.2 s (brief: 15-30). The answer shot (553) is a chaotic handheld: whip pans between the watch, the car and the phone.
- R1's wind-up starts mid-ramp at 1.1x speed on "go" (pitch step at the splice) - unheard.
- R3's answer shots (2H, 30 MIN, TIME) end on the camera whipping away (kept to land cuts on beats without clipping words).
- R1 and R3 both end on V_RES_FULL with the same result card (R3 uses more of it, 3.45 s vs 2.8 s).
- Clock 1 in the reboot shot (12:09) is derived from 542@24 (12:20.75 legible); all other clock values are legible or are the long-form's derivation.
- `ive director` does not fit this format (it reads each listed file whole, so it reports every shot as the same view); not used for decisions.

## Still placeholder (13:22 UTC)
The 3D agent's chain log ends `CHAIN_DONE` at 13:01 with V_MATCH_REAR 39/42 frames (no preview mp4), V_PAIR_2 0/42 and V_RES_FULL 0/64; no Blender
process is running. Placeholders (darkened matched IRL window / black, tagged "PLACEHOLDER <id>"): R1 V_RES_FULL; R2 V_MATCH_REAR, V_PAIR_2,
V_RES_FULL; R3 V_RES_FULL. When `renders/<id>/<id>_preview.mp4` exists, `python projects/lexus-is350-reels/tools/build.py && python projects/lexus-is350-reels/tools/qa.py`
swaps them in (graphics and intermediates are cached). Re-check the rear and rear-quarter onions (`out/qa/R2/onions.jpg`) then.
