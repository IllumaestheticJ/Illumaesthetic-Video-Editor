# Stock NB Miata chassis-scan reel v4 — agent self-review (training/rubric.md)

v4 output: `/home/user/media/work/miata/out/nb_miata_scan_v4.mp4` — 1080×1920, 30 fps, AAC, 26.13 s.
Changes from v3 (user feedback "still has references to the video in the text", "beginning shot too cropped - doesn't show the
actual scanning", "use real music" -> "use TikTok trending music"; parent v2 brief): all bracing-test text removed; opener =
tech scanning the engine bay on a wide canvas, 1:1 on the drop into Engine Bay Control; new bumper-removed hero (Bumper Only
slides off Frontend Stripped, push onto the crash beam); side re-framed to the whole jacked car; music = 'Prisoner' (DIDKER),
TikTok CML US 7-day trending #6.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 5 | Frame 1 = Artec scanner in hand over the open bay (scanner, hands, bay all in frame); transformation at 2.80 s on the drop. |
| 2 | Beat sync | 4 | Decoded cuts 2.800 / 6.267 / 13.967 / 15.000 / 18.500 s vs audio onsets -2 / +3 / -9 / -14 / -44 ms. Phonk 808s are syncopated; grid = half beats (0.349 s) from a flux comb, beat confirmed by autocorrelation. |
| 3 | 1:1 match | 4 | Bay: 5 landmarks, f fixed 22 mm, RMSE 4.5 px @4K; onion (match/check_bay.jpg) aligns filter, valve cover, MAF, strut top, badge; intake pipe a few px high. The tech and scanner vanish at the cut (expected). Side: cam_C_crop as v3. |
| 4 | Scan quality | 4 | Hood shards cut (z > 0.92 m) from the bay and stripped scans; the stripped scan ends behind the front wheels (visible as a cut edge at the right of the front shot). |
| 5 | Story | 4 | Scanning -> engine bay -> bumper off / crash beam -> crew at the jacked side -> whole car -> listing. Front-end scans have the strut brace installed, Bay Control doesn't; the brace is not called out. No rear (trunk scans don't register). |
| 6 | Grade | 4 | Rough-cut SDR; IRL opener canvas fill is a darkened blur of itself. |
| 7 | Text | 5 | Only file facts: ENGINE BAY 4,997,392 / FRONT BUMPER REMOVED 4,994,051 / CRASH BEAM (Frontend Stripped scan) / FULL EXTERIOR 24,993,431 triangles (STL headers). Never over IRL. No test numbers. |
| 8 | Ending | 4 | s5 trimmed to the front-left 3/4 landing; 0.5 s dissolve into the listing, title -> logo -> URL last; 5.6 s card. Music fades at 26.1 s mid-section (no natural end). |
| 9 | Technical | 4 | Every frame lit (luma scan; persistent data off for the moving bumper); 0 black frames; IRL side 23.976 pulldown. |

## Known issues / next ideas
- IRL side shot is only 1.03 s (hard cut in the rough cut at 203.75 s); raw camera files would allow longer IRL shots.
- Strut-brace beat dropped: the bar vanishes into the silver bay; a top-down camera or accent material could carry it.
- Music ends on a fade; a track section ending ~26 s after the drop would give a hard out.

---

# Stock NB Miata chassis-scan reel v3 (v2 review kept below) — agent self-review (training/rubric.md)

v3 output: `/home/user/media/work/miata/out/nb_miata_scan_v3.mp4` — NB only, 32.5 s. Changes from v2 (user feedback): Grimace hook, scanner close-up and walk-in removed; the rough cut supplies only the two 1:1 shots (1.0 s each); music starts on track beat 3 so the 1:1 cut still lands on the drop (1.0 s); 1:1 cuts at 1.0 and 7.0 s. Hook 5 (transformation at 1.0 s); Story 4 (the "why bracing" context from Grimace is gone; story = scan -> jacked -> brace -> listing).

v2 output: `/home/user/media/work/miata/out/na_miata_grimace_scan_v2.mp4` — 1080×1920, 30 fps, yuv420p, AAC, 34.57 s.
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
