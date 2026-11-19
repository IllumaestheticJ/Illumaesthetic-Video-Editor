# Pip & Gus Ep 4 "Can't you just 3D print the scan?" - self-review, v1 (2026-11-18)

Output: `/home/user/media/pip-gus-ep4-print-the-scan/out/pip_gus_ep4_v1.mp4`, 1080x1920, 30 fps, 1309 frames (43.63 s).
Mix -14.0 LUFS, -2.0 dBTP (dialogue -13.5, music -21.8). QA: text over real footage alpha 0.0; caption pixels over the phone screen 0.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Opens on Pip bouncing at the scan on the laptop ("OK, it's scanned"); first visual gag (scan flies to the printer) at ~4.5 s |
| 2 | Beat sync | 4 | Real section cuts on beats from the hand-off (1052, 1070, 1106, 1160, logo 1196); bass lift measured 35.0-35.25 s vs hand-off 35.07 s; cartoon cuts sit on line gaps, not beats |
| 3 | 1:1 match | 2 | Not a 1:1: IMG_0770 is a close, steep 1440 px still of part of the corner and the solve didn't hold. Hard cut on the beat to the same corner (owner OK'd 2026-11-18) |
| 4 | Scan quality | 4 | Owner's GT350_Lip.blend renders in the owner's Blender look (lavender/green/tan), not house silver (owner's choice) |
| 5 | Story | 4 | Scan = skin -> can't print it -> remake or design on it -> GT350 for real (crash, scan, bumper, lip) -> Ep 5 question |
| 6 | Grade | 3 | Photos as shot (SDR JPEGs), 1.78x upscale from 1440x1080 with a light unsharp: softer than video |
| 7 | Text | 5 | Word-by-word captions on the cartoon only; no numbers; logo card plain (owner) |
| 8 | Ending | 4 | Final chord on the logo card; Pip's question runs ~1.5 s past the ring-out (deliberate beat) |
| 9 | Technical | 5 | yuv420p, AAC 256k, faststart, no missing frames |

Known weak spots for v2 (from my own frame review):
- E4: Gus's flick happens off frame; the cling-film wobble reads mostly on the wheel, not the body panel.
- E7: Gus's back hides the empty plate until he steps away at the end of the shot.
- E9: Pip and her sketch sit at the left edge of frame.
- E3: the scan lands half out of frame on the left.

# v2 (2026-11-19)
Output: `/home/user/media/pip-gus-ep4-print-the-scan/out/pip_gus_ep4_v2.mp4`, 1309 frames (43.63 s), -14.0 LUFS / -2.0 dBTP.
QA: text over real footage 0.0; caption pixels over the phone screen 0.

Owner v1 notes applied: Gus explains on a phone showing the real GT350 Blender scenes (E4, E8-E12); "remake the original" is
now curves traced over the scanned bumper, then the surface growing over them; scan (faceted) vs surface (smooth + clean
curves) wipe; recap on half-beats from crash to the real finished bumper. Own fixes: E3 wider, E7 from the right.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | unchanged |
| 2 | Beat sync | 4 | recap cuts every 9 or 18 frames from the hand-off; lift on the hand-off |
| 3 | 1:1 match | n/a | no real-to-scan match cut in v2 (recap montage of hard cuts) |
| 4 | Scan quality | 4 | owner's Blender look; real scan triangles shown |
| 5 | Story | 4 | retracing is now shown, not implied |
| 6 | Grade | 3 | photos upscaled from 1440x1080 |
| 7 | Text | 5 | captions sit under the phone, over the hats; none over the screen |
| 8 | Ending | 4 | finished bumper photos, then the plain logo with Pip's question |
| 9 | Technical | 5 | |

Weak spots: the GT350 sits small inside the phone screen (dark margin above and below); the triangle close-up is subtle at
phone size; the recap's 9-frame shots are quick to read; Gus's mitten doesn't visibly grip the phone.

## v3 self-review (2026-11-19) - 44.8 s
Owner notes on v2 and what changed:
- "he says 'print my bumper!' but it shows the entire car" / "use the gt350 bumper as reference": the laptop now shows the real
  GT350 original-bumper scan front-on, and that bumper scan is what Pip shoves onto the printer (E2) and Gus lifts off (E3).
  Checked on frames 120-245: reads as a bumper at a glance (grille opening, fog-light holes).
- "'no thickness' -> 'not necessarily solid'": line 4 re-voiced (Harrison, one line spliced into the approved take, level-matched);
  the phone shows the triangles close-up, then the scan from behind as a hollow shell. Episode is 35 frames longer.

Weak spots (looked at, not fixed):
- The triangles close-up on the phone (about 9.5-11 s) is a soft lavender texture; individual triangles are hard to see at phone size.
- The bumper scan in E2/E3 has no ink outline (the inverted-hull outline spikes on open scan meshes), so it is slightly flatter than the characters.
- The re-voiced line was not approved by ear before animating; it needs the owner's check.
- Carried over from v2: 0.3 s recap shots are quick; Gus's mitten does not visibly grip the phone.

Rubric (training/rubric.md), self-score: story 4, clarity 4, sync 4, look 3.5, rules 5 (no text over footage/phone screen - QA assert passed; no invented numbers).
