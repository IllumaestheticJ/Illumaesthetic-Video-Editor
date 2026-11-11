# NA Miata "Grimace" / stock NB chassis-scan reel v2 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/na_miata_grimace_scan_v2.mp4` — 1080×1920, 30 fps, yuv420p, AAC, 34.57 s.
(v1 = same cut with the S2 labels over the white car body; fixed in v2.)

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Grimace sweeps past at Sonoma (0–1.5 s), scanner close-up at 1.5 s, first 1:1 transformation at 3.03 s on the drop. Not a transformation inside 1.5 s, but motion from frame 1. |
| 2 | Beat sync | 4 | Cuts measured from frame diffs at 1.533 / 3.033 / 8.033 / 10.533 / 15.567 / 20.567 / 24.567 s, all = round(beat·30) on the 0.501 s grid. Grid from max-rise onsets; kick-band fit was loose (127 ms rms) in this garage-rock mix, so the grid itself is ±1 frame uncertain. |
| 3 | 1:1 match | 4 | Cut 1 (187.70 s front 3/4 → Control Ground scan): badge, hood seam, headlight, grille, wipers within a few px. Cut 2 (204.70 s door/jack → jacked exterior): handle and door gap within a few px, rear arch flare still ~20–35 px off in the 9:16 output (RMSE 10 px @4K). |
| 4 | Scan quality | 4 | Silver on black, 3 mm full car / 2 mm engine bay. Engine-bay scan has scanned shards at the cowl (top of the bay) and a rough wheel on the jacked scan. Strut bar is the real scanned part (ICP diff of two bay states). |
| 5 | Story | 4 | Grimace (why) → crew scans the stock NB → becomes scan → jacked → strut brace out/in → listing. Grimace itself was never scanned (cage); user OK'd the NB story. |
| 6 | Grade | 4 | Rough-cut footage is the team's graded SDR; Grimace iPhone clip tonemapped from HLG. Warmth differs a little between track (daylight) and shop shots. |
| 7 | Text | 4 | Only PDF/STL numbers: 24,997,127 triangles (STL header), 960.948 mm control engine-bay width, +1.695 mm jacked, +0.731 mm with strut brace. ≤2 items, never over IRL. S2 sub-line grazes the tyre in places. |
| 8 | Ending | 5 | Orbit lands on the listing's own render angle, grades to listing grey, 0.5 s dissolve into the NB 3D-scan listing; title → logo → URL last; music fades at the end of the riff. |
| 9 | Technical | 4 | Specs correct, every frame lit (persistent data off for animated-part shots). 23.976→30 pulldown repeats every 5th frame on the rough-cut shots; one cloned frame before each cut (assembler hold). |

## Known issues / next ideas
- S2 pulls back to the rear quarter, so the jacked front corner leaves frame while "ONE CORNER JACKED" is on screen — an orbit toward the front would show the jack.
- S5 starts small (wide orbit to the listing framing); a tighter start would read better on phones.
- IRL clips are only 1.5–2.5 s: the rough cut is the only scanning footage and most spans carry burned-in text. Raw camera files would allow longer, cleaner shots and a lower-angle hero cut (140.5–141.7 s push-in).
- Fender-brace and fender+strut numbers (+0.237 / +0.436 mm) are verified but unused; a heatmap beat (deviation colours from the PDFs' scans) could carry them.
