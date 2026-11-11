# 240SX scan reel v3 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/240sx_scan_v3.mp4` — 1080×1920, 30 fps, 27.80 s, AAC (track extended 8 beats).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 5 | rear 1:1 cut at 1.82 s |
| 2 | Beat sync | 5 | cuts at 1.82 / 6.85 / 9.38 / 14.42 / 16.95 / 21.99 (measured onsets); splice keeps the grid |
| 3 | 1:1 match | 4 | rear: 3 px; front: 8 px RMSE (lamp heights differ scan vs shoot) - overlay aligned on bumper/width |
| 4 | Scan quality | 4 | parts spin left/right without collisions; brief edge-on beam during spin |
| 5 | Story | 5 | real→scan rear teardown → real front → scan front teardown → scanner → reassembly → listing |
| 6 | Grade | 4 | unchanged |
| 7 | Text | 5 | inside+outside only where verified; 4,527 mm removed; CTA on the web page |
| 8 | Ending | 5 | reassembly orbit lands on the listing render's angle → dissolve → zoom out on the hit |
| 9 | Technical | 5 | 27.80 s = audio; no dup/black frames |

## Known issues / ideas
- Front shot keeps the car small (it has to match the wide IRL frame); a slower, longer push after the bumper spins would help.
- Listing dissolve is ~near-1:1 (tail offset a few %); a proper camera solve against the listing image would make it exact.
