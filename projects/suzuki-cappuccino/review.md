# Self-review - Suzuki Cappuccino scan reel v1 (`/home/user/media/work/out/suzuki_cappuccino_v1.mp4`)

38.87 s, 1080x1920, 30 fps, 11 scan shots + logo, scan only / no text (Temerario format). Scored with `training/rubric.md`.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Car tracking from frame 0 (fades up over 1 s); the transformation itself (front opens) is held for the drop at 15.27 s, by the Temerario order the brief set |
| 2 | Beat sync | 5 | 126 BPM kick-anchored grid (2 ms median kick error). Frame-diff cut detection on the delivered file: every cut at round(beat*30), -14..+10 ms; vs. decoded-audio kicks -10..+12 ms |
| 3 | 1:1 match | n/a | No IRL footage in this format |
| 4 | Scan quality | 4 | Silver on black, no ground. Real-scan caveats visible: speckle on the lower rim / hub in the wheel close-up, holes in the bumper grille, open hood underside is the outer skin seen from below (hood inside never scanned). A sliver of the slid-off front bumper peeks in at the bottom edge for the first ~0.3 s of s09 |
| 5 | Story | 4 | Turntables -> wheel + lamp close-ups -> bumper off / hood up ON THE DROP -> trunk -> top-down -> explode -> float -> reassemble -> logo. Hood/trunk swing on hinges fitted to the captured open lids. Exploded parts read small at 9:16 (the lamps especially) |
| 6 | Grade | 5 | AgX, -0.5 EV silver (huracan-evo measured match to ref), consistent across shots (median car luma 135-192) |
| 7 | Text | 5 | None, per brief |
| 8 | Ending | 5 | s11 fades out, logo on beat 76 (36.224 s), the track's last two hits play under it, ends with the music at 38.87 s (music measured to end ~38.9 s; file is 40.05 s) |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, faststart. No black frames (41 black render frames caught by a per-frame luma scan and re-rendered); no cloned frame before cuts (worked around ive's cut compensation, see editlog). One near-duplicate at 15.30 s = eased camera start |

Next agent / reviewer: the weakest beat is s09-s10 (parts small in frame). If asked for "bigger", go closer on a 3/4 and stack fewer parts per shot.
