# Mazda RX-7 FC3S scan reel v1 — self-review (training/rubric.md)

Output: `/home/user/media/work/rx7/out/mazda_rx7_fc_v1.mp4` — 1080x1920, 30 fps, 37.37 s (1121 frames), scan only, no text.
Shot order: front 3/4 turntable → rear 3/4 orbit → wheel ECU → nose ECU → hood opens on fitted hinge → mirror glide →
top-down → exploded view (hood, front face, rear bumper out and back) → ILLUMAESTHETIC card.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Camera orbits from frame 1; soft musical intro, so the first cut waits for the hit at 4.53 s. |
| 2 | Beat sync | 5 | Grid fit on hit/snare flux (bass is eighth notes, kick-band unusable). Delivered file: all 8 cuts −14..+8 ms from an onset (< ½ frame). |
| 3 | 1:1 match | n/a | Scan-only reel, no IRL. |
| 4 | Scan quality | 3 | S5 scans clean after levelling; known holes: rear glass (dark in top-down), tail-lamp lenses (not featured), wheel hub specks. Pop-ups down in every scan. |
| 5 | Story | 4 | Temerario structure: whole car → details → hood opens → top-down → exploded panels lock back on the breakdown's last hit (32.28 s) → logo on 33.4 s. |
| 6 | Grade | 4 | Satin silver on pure black, exposure −0.5 for all shots (car median luma ≈ reference). |
| 7 | Text | 5 | None. |
| 8 | Ending | 5 | Logo cut on the section hit at 33.4 s, fades in from black; music ends ~36.6 s, 0.8 s audio fade. |
| 9 | Technical | 4 | Specs met; 15 fps renders minterpolated to 30. s8 first render lost lighting from frame 102 (no log error) — caught by frame-diff scan, range re-rendered. |

## For the next agent
- Parts flying out along the car's length don't fit 9:16 from a side view; keep the explode orbit in 3/4 (30–64°) and lift parts in Z.
- A 2-key orbit interpolates loc on the chord; sample the arc (shots.py s8 uses 11 keys).
- Always frame-diff/luma-scan the assembled reel: a long Cycles job can silently render unlit frames.
