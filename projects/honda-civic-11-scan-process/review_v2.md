# Honda Civic EK scan-process reel v2 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/civic_ek_scan_process_v2.mp4` — 1080×1920, 30 fps, 29.37 s, H.264 yuv420p + AAC. v1 review: `review_v1.md`.
v2 = reviewer feedback on v1: (1) nothing comes off the car — the bumper was never pulled and there's no separate scan of it,
so the exploded view and the reassembly are gone; (2) trending music: "Time Back" (Sinny & 7vvch), #4 on TikTok's
Commercial Music Library US 7-day chart, re-cut to its measured kicks.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 5 | powdering shot over the riser → 1.5 s of silence → 1:1 cut to the scan on the drop kick (3.20 s) |
| 2 | Beat sync | 5 | 6 hard cuts measured on the delivered file: −12…+11 ms from the kick peaks (tools/cutcheck.py); holds 1.1–6.6 s |
| 3 | 1:1 match | 4 | unchanged from v1 (cam_A 18.3 mm, cam_B 28 mm; scan wipers differ from the shoot) |
| 4 | Scan quality | 5 | intact full-car scan only — no cut panels, no open shells, no debris |
| 5 | Story | 5 | powder → scan (drop) → handheld scanner → scan orbit of the whole car → software aligning passes → scan line turns the raw scan into the listing model → listing |
| 6 | Grade | 4 | HLG tonemapped; software beat is an upscaled viewport crop |
| 7 | Text | 5 | 24,997,508 triangles (STL header); EXTERIOR SCAN / HONDA CIVIC EK HATCHBACK; nothing claimed about parts |
| 8 | Ending | 5 | sweep lands on the listing's 360 view, morphs to its greys, dissolves; title → logo → URL last; ends on the kick at 62.27 s with a 1 s fade |
| 9 | Technical | 5 | 29.37 s; cut holds verified frame-accurately |

## Learned this round
- Don't animate parts off the car without a matching physical removal + part scan (standing rule now).
- Trending music source that is licensed for brand posts: Higgsfield `tiktok_music_trending` (TikTok Commercial Music Library);
  the preview_url is the full track (sf16-ies-music-sg.tiktokcdn.com, already allowed).
- Drop-section kicks can drift off a fitted grid (40 ms rms here): cut on measured kicks.
