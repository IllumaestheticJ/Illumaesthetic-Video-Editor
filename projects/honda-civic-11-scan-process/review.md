# Honda Civic EK scan-process reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/civic_ek_scan_process_v1.mp4` — 1080×1920, 30 fps, 29.90 s, H.264 yuv420p + AAC.
Format follows the final 240SX reel: IRL → 1:1 on the drop → scan → crew scanning → 1:1 → exploded scan → software →
x-ray reassembly → dissolve into this car's scan-data listing (WebZoom, logo, URL last).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 5 | crew powdering the car, 1:1 cut to the scan on the drop at 3.20 s |
| 2 | Beat sync | 5 | 6 hard cuts measured on the delivered file (tools/cutcheck.py): −7…+17 ms from the kick peaks; holds 0.63–6.60 s on the phrase accents |
| 3 | 1:1 match | 4 | A (front 3/4, f 18.3 mm, LM + silhouette refine): grille, plate, lamps, roof on the IRL silhouette. B (fender close-up, f 28 mm): marker, seam, arch, rocker, hood edge align; the scan's wipers sit differently from the shoot |
| 4 | Scan quality | 4 | 3 mm decimation, ground cropped, yaw-aligned; bumper scraps reassigned so nothing floats when parts leave. Parts are cut from one full-car scan, so their backs are open shells (kept rotations to ±38°) |
| 5 | Story | 5 | real car → scanned (powder, handheld scanner) → scan → parts → software alignment → reassembly → listing |
| 6 | Grade | 4 | HLG tonemapped (hable) on all iPhone clips; software clip is upscaled 2.2× from a viewport crop (soft but readable) |
| 7 | Text | 5 | only on scan shots: 24,997,508 triangles (STL header) and "EXTERIOR SCAN / HONDA CIVIC EK HATCHBACK" (listing says Exterior Only; verified parts have no inside) |
| 8 | Ending | 5 | x-ray orbit ends on the listing's 360 view (silhouette chamfer ~1 px), morphs to the listing greys (car 136 vs 135, bg 26 vs 26), dissolves; title → logo → ILLUMAESTHETIC.COM last; track ends naturally with an 0.8 s fade |
| 9 | Technical | 5 | 29.90 s video vs 29.94 s of track left; no black/dup frames at cuts other than the assembler's 1-frame hold |

## Deviations from the brief (and why)
- The footage is a **6th-gen EK hatch**, not an 11th gen → Drive `Honda Civic EK` full-car scan (the brief said to use the
  matching folder if it isn't 11th gen).
- **No part-state scans** exist for the EK and the footage has no panel removal → the second 1:1 cut goes to the full-car scan
  and the explode uses panels cut from it. No "inside + outside" claim (it isn't true for this data).
- Second 1:1 cut was solved on the cut frame itself (the camera never holds still during the scanner pass), so no
  phaseCorrelate drift absorption was needed.
- Focal is not the same in both clips: 18.3 mm (opening pull-back) vs 28 mm (scanner pass) — each verified with onions.

## Known issues / v2 ideas
- The unused rear spray shot (v_1958_06) could replace the 0.63 s scanner beat if the reviewer wants more prep.
- Software beat could use the final gold mesh orbit (sr_1429_30) instead of the alignment view.
