# 240SX scan reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/240sx_scan_v1.mp4` — 1080×1920, 30 fps, 22.77 s, AAC.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | opens on IRL crew walk-around (same as approved reel); no transformation until 8.1 s |
| 2 | Beat sync | 5 | all 8 cuts on the 95.7 BPM grid (after fixing 1-frame-per-cut drift) |
| 3 | 1:1 match | 5 | rear 3/4 frame @ v_1838_02 3.800 s; solve RMSE 3.0 px; overlay confirms silhouette + seams |
| 4 | Scan quality | 3 | clean full-car scan; small ground scrap still attached to the bumper part; 4 mm decimation softer than Temerario |
| 5 | Story | 4 | walk-around → scanning → becomes scan → side → real bumper pull → scan bumper explodes → hero → logo |
| 6 | Grade | 4 | HLG tonemapped consistently; scan bg (~RGB 5) vs logo card (0) slight mismatch at 20.1 s |
| 7 | Text | 4 | true data only (STL tri counts, 4,527 mm measured); small sizes may be tight on phones |
| 8 | Ending | 5 | logo card on final downbeat, music fades |
| 9 | Technical | 5 | duration within 1 frame of audio; no dup/black frames at cuts |

## Known issues / v2 ideas
- Side + hero shots frame the car small (≈45 % width). Tighter framing or a slow push would read better on phones.
- Render hero close-ups at 2 mm decimation for Temerario-level surface detail.
- Exploded shot: crop the bumper part's ground scrap; keep the whole car in frame.
- Consider a stronger hook: open on the 1:1 cut itself or a scan flash-forward (Civic reel pattern: CG hook first).
