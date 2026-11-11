# MR2 SW20 scan-process reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/mr2_sw20_scan_v1.mp4` — 1080×1920, 30 fps, 29.30 s (879 frames), AAC, faststart.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | crew scanning the open trunk from frame 0; 1:1 cut to the scan on the drop at 3.20 s (music starts on a real kick 2 accents before the drop). Not < 1.5 s, but the drop sits at 3.2 s in this track |
| 2 | Beat sync | 5 | 8 hard cuts measured from frame diffs vs kicks in the delivered audio: -10, +7, 0, -1, -10, +7, 0, +16 ms (all < 1/2 frame). v1-pre had every cut +1 frame; first clip shortened to 95 frames |
| 3 | 1:1 match | 4 | Rear (v_1602_50 @ 4.400 -> Interior scan): RMSE 2.9 px, onion aligns lid, prop rod, MR2 garnish, plate, exhaust. Side (v_1433_07 @ 2.300 -> T-Top Off + T-tops composite): RMSE 8.2 px (rounded fuel-door corners), onion aligns quarter window, louvers, fuel door, arch, sill; the frunk lid sits ~8° lower in the scan than in the shoot (not rigid between sessions) |
| 4 | Scan quality | 4 | silver on black, 4 mm; ground removed after re-levelling on the true floor. Taillight lenses/black garnish mesh did not scan (holes), loose exhaust pipe hangs under the rear; doors are inner-face only so their outer side shows the mirrored inner panel while spinning |
| 5 | Story | 4 | real car -> scan -> crew scanning (screen, door panel, side) -> scan with T-tops lifting off -> Artec Studio -> doors + T-tops explode/spin -> x-ray reassembly -> SW20 listing. No real removal footage exists in the dump (all clips are scanning), so the removal is told in the scan |
| 6 | Grade | 4 | all HLG clips tonemapped (hable); daylight shop footage consistent; screen recording is a 2.7x upscale of the Artec viewport (soft, 1 s) |
| 7 | Text | 5 | only STL-header numbers (34,993,395 / 34,998,108) and a verified claim (inner door panels); ≤2 items; never on IRL; no website specs |
| 8 | Ending | 4 | dissolve to the SW20 listing, title, logo, URL fading in last; music fade 0.9 s at the track's end. Listing hero is the 2025 assembled car, so no angle-matched morph |
| 9 | Technical | 4 | 1080×1920/30/yuv420p/AAC/faststart; the assembler's 1-frame clone before each cut shows as one duplicated frame before every cut |

## Known issues / v2 ideas
- S3: the near (left) door dips below the car while edge-on mid-spin (perspective from the high camera) - lift doors more or stack them (one above, one below).
- Side 1:1: re-hinge the frunk lid to the shoot angle (like huracan hinge.py) so the lid doesn't jump at the cut.
- A cabin 1:1 (v_1447_56 / v_1529_27) was attempted and dropped: closed sprayed-glass cabin + mixed door states + ambiguous landmarks.
