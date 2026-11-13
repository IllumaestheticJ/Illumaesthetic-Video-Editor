# Lamborghini Revuelto scan reel v3 — self-review (training/rubric.md)

Output: `/home/user/media/work/out/lamborghini_revuelto_v3.mp4` — 1080x1920, 30 fps, 34.60 s (1038 frames), h264 yuv420p + AAC.
Earlier versions: review_v2.md (v2.1), review_v1.md. v3 answers the reviewer's notes on v2.1: "the wheels are oddly cut
flat" and "exploded views of the individual parts removed from the front and rear bumpers".

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | Whole car (front-left 3/4, fully in frame) pushing in under the quiet intro; first transformation at 4.6 s (front bumper off). |
| 2 | Beat sync | 4 | Cuts on bar downbeats (frames 139/279/419/490/630/771/912). On the delivered audio the nearest detected onsets are -25..+9 ms from the cuts at 9.30-25.70 s; the 4.63 s cut sits on the grid in a passage with no clear onset. Parts lock at 27.967, logo on the loudest hit 30.40. No duplicated or frozen frame at any cut. |
| 3 | 1:1 match | n/a | Scan-only format. |
| 4 | Scan quality | 4 | Tyres are round again (the "ground" plane was the undertray; geometry re-cleaned with tools/clean2.py). Bumper sub-part scans registered 2.1-3.6 mm to the bumper scans and tint-checked. State-scan structure is ragged at its edges; scan-noise specks under the open lid. |
| 5 | Story | 5 | Front -> front bumper alone (inner face, outer face, its scanned pieces separate) -> left side -> rear -> rear bumper alone (same pattern) -> everything slams home on the climax -> logo. One continuous sequence per section; only openings/removals with scan data. |
| 6 | Grade | 4 | AgX -0.5 EV silver on black, consistent; bumper-only shots are darker overall (small subject on black). |
| 7 | Text | 4 | Eight short labels, one at a time, only over scan shots, in clear black (bumper-parts labels moved below the pieces after the first assembly showed a collision). Triangle counts from the STL headers; part names from the scan file names. |
| 8 | Ending | 4 | 0.5 s fade, 720 px logo (newest standing lesson: 380 px was too small) on the loudest hit, rides the decay. |
| 9 | Technical | 5 | Spec met; per-frame luma scan of every render: no dropouts. |

## Known weaknesses
- Left out of the bumper explodes on purpose: reverse light and plate light (not bumper parts / not registered), exhaust tips.
- The rear bumper's pieces are fewer and larger than the front's ten, so that explode reads simpler.
- v3_side is short (2.4 s) to make room for the two bumper shots.
- Part scans exist for the car's left side only, so the side section shows one side.
