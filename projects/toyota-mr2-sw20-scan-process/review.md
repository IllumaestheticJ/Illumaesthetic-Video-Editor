# MR2 SW20 scan-process reel v3 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/mr2_sw20_scan_v3.mp4` — 1080×1920, 30 fps, 31.40 s (942 frames), AAC, faststart.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | crew scanning the open trunk from frame 0; 1:1 cut to the scan on the drop at 3.20 s (music starts on a real kick 2 accents before the drop). Not < 1.5 s, but the drop sits at 3.2 s in this track |
| 2 | Beat sync | 5 | v3 on Riders on the Storm (102 BPM): 9 cuts/dissolve starts vs kicks in the delivered audio: -4, +5, -6, -12, -2, +1, -5, -12, +13 ms |
| 3 | 1:1 match | 4 | Rear (v_1602_50 @ 4.400 -> Interior scan): RMSE 2.9 px, onion aligns lid, prop rod, MR2 garnish, plate, exhaust. Side (v_1433_07 @ 2.300 -> T-Top Off + T-tops composite): RMSE 8.2 px (rounded fuel-door corners), onion aligns quarter window, louvers, fuel door, arch, sill; the frunk lid sits ~8° lower in the scan than in the shoot (not rigid between sessions) |
| 4 | Scan quality | 4 | silver on black, 4 mm; ground removed after re-levelling on the true floor. Taillight lenses/black garnish mesh did not scan (holes), loose exhaust pipe hangs under the rear; doors are inner-face only so their outer side shows the mirrored inner panel while spinning |
| 5 | Story | 4 | real car -> scan -> crew scanning (screen, door panel, side) -> scan with T-tops lifting off -> Artec Studio -> doors + T-tops explode/spin -> x-ray reassembly -> SW20 listing. No real removal footage exists in the dump (all clips are scanning), so the removal is told in the scan |
| 6 | Grade | 4 | all HLG clips tonemapped (hable); daylight shop footage consistent; screen recording is a 2.7x upscale of the Artec viewport (soft, 1 s) |
| 7 | Text | 5 | (counter easing showed 34,959,222 in v2 as first delivered - replaced by a static exact label) only STL-header numbers (34,993,395 / 34,998,108) and a verified claim (inner door panels); ≤2 items; never on IRL; no website specs |
| 8 | Ending | 5 | v2 (user: 'needs a better final cut into the product listing'): x-ray orbits to the solved listing-hero camera, morphs to listing-grey clay (bg 64 vs 63), dissolves into the hero held 0.6 s - the chassis turns into the listing car at the same pose (2025 full-car scan ICP-registered, IoU 0.89); then zoom-out, logo, URL last |
| 9 | Technical | 4 | 1080×1920/30/yuv420p/AAC/faststart; the assembler's 1-frame clone before each cut shows as one duplicated frame before every cut |

## Known issues / v2 ideas
- S3: the near (left) door dips below the car while edge-on mid-spin (perspective from the high camera) - lift doors more or stack them (one above, one below).
- Side 1:1: re-hinge the frunk lid to the shoot angle (like huracan hinge.py) so the lid doesn't jump at the cut.
- A cabin 1:1 (v_1447_56 / v_1529_27) was attempted and dropped: closed sprayed-glass cabin + mixed door states + ambiguous landmarks.

## v1 -> v2
- User feedback (23.6 s): better final cut into the product listing. Fixed as above; everything before 19.3 s unchanged.

## v2 -> v3
- User: 'slop music' -> real NFSU2 track, Riders on the Storm (user upload). Re-timed on its kick accents (1.1765 s), beat entry on the 1:1 rear cut, renders reused slowed ~6 %, ends on a kick at 31.4 s with a 1.2 s fade.
