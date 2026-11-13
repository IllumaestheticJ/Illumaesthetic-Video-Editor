# Honda S2000 AP1 scan reel — self-review v7 (`/home/user/media/work/s2k/out/honda_s2000_v7.mp4`)

v7 = v6 + the reviewer's requested real-footage opening: 0.93 s of the car being powder-scanned (front-on, Dropbox scan video 5:58.7-5:59.6) -> hard 1:1 cut on the kick at 0.945 s (cut -11 ms) into the scan from the solved camera (match/cam.json, onion-checked: emblem, headlights, tow cover, windshield, bumper coincide). Landscape footage shown as a full-width band over its blurred fill; no text over it. Rows 1 and 3 below are updated for v7.

v6 = all-reels v2 brief + addendum A-D + this reel's feedback ("last scenes held too long", "rear trunk data is made-up").
Plan: `direction.md` / `director.md`. Earlier reviews: review_v3.md, review_v4.md.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 5 | Real car being scanned from frame 1, transforms into its scan at 0.93 s (1:1), then the scan pulls back to the whole car |
| 2 | Beat sync | 5 | Measured on the DECODED audio of the delivered file (tools/kickcheck.py, 1.45 ms hop): 10 kick cuts within ±15 ms. Three cuts sit on bars without a kick (drums-out b28; drumless outro b68/b76) on the drift-corrected grid. The bumper comes off on the drop |
| 3 | 1:1 match | 4 | Onion overlay of the cut frame aligns all rigid features; solve RMSE 6.7 px (residual on grille/fog edges that differ between car and scan); the real car has wheels, the scan does not, so the wheels vanish at the cut. The 720p band is soft next to the 1080x1920 renders |
| 4 | Scan quality | 4 | Silver on black; 2 mm detail for side/rear/headlight; the bumper-removed structure, bumper inner side scanned. Minus: car scanned without wheels; some stringy debris under the radiator support |
| 5 | Story | 5 | One lap: front-left wide -> side detail -> rear wide + detail -> over the top -> headlight -> bumper-removed hero section (off on the drop, 3 structure angles, inner side, back on) -> pull-out, fade, small logo. Each section once. Only real data: Bumper Only is the only moving part; no hood animation, no trunk |
| 6 | Grade | 5 | AgX, no colour; F7 fades to black into the logo card |
| 7 | Text | 5 | 3 labels over the bumper section only, max 1 on screen, outside the subject: FRONT BUMPER REMOVED · 3,999,999 TRIANGLES (Bumper Removed STL header), BUMPER BEAM (visible beam with tow-eye), FRONT BUMPER · INNER SIDE · 4,000,000 TRIANGLES (Bumper Only header) |
| 8 | Ending | 5 | Bumper locks, short pull-out, fade, small logo (~30 % width) through the track's hard stop; 37.2 s |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC; every render scanned for dark frames (none; persistent data off on animated shots); no duplicated cut frames |

## Changes from v4
- Dropped: hood hinge (never captured open; addendum D), trunk opening + lid (no real open-trunk scan), wide one-burst explode,
  repeated front/rear turntables (director report), s5/s6 (fake hood).
- Added: W1/R1 whole-car wides with margins, F1-F7 bumper-removed hero section, labels, small logo, kick-measured cuts.

## Open
- None. IRL opening delivered in v7.
