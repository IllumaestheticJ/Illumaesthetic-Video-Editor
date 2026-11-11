# Mazda Miata ND scan reel - self-review (v2, delivered)

File: `/home/user/media/work/miata/out/miata_nd_v2.mp4` - 1080x1920, 30 fps, 32.4 s (972 frames), h264 yuv420p + AAC, faststart.
Scan only (no IRL, no text), house satin silver on black, original track `mazda-miata-nd_track.mp3` (116 BPM).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | The turntable moves from frame 1, but the first 4.1 s ride the track's pad intro; the first cut is on the first kick. Temerario-style slow open, not a 1.5 s transformation hook |
| 2 | Beat sync | 5 | Cuts measured from frame diffs at 124/248/310/372/497/621/683/869 = plan; decoded audio kicks are -17..+17 ms from each cut (half a frame). Hood/trunk/bumper moves start and land on even-beat kicks; explode locks on the 32.127 s kick (~+1.6 frames from minterpolate src_fps) |
| 3 | 1:1 match | n/a | Scan-only reel by brief; no IRL footage |
| 4 | Scan quality | 4 | Ground cleaned, jack stands dropped, plate characters flattened. Visible scan truth: speckle holes on the hood (top-down, turntable), ragged top edge of the front-bumper part scan, thin single-skin hood/trunk (cut from the car skin - no isolated panel scans exist) |
| 5 | Story | 4 | Turntables -> wheel + lamp close-ups -> front opens to the real engine bay -> rear opens to the real trunk -> top-down -> panels separate and lock home -> logo. Car is smallish in the exploded view (9:16 width limit) |
| 6 | Grade | 5 | Car-pixel luma median 199-203 vs Temerario ref ~200; background RGB 7 matches the logo card |
| 7 | Text | 5 | None (brief) |
| 8 | Ending | 5 | Logo cut on the track's last hit (33.162 s), holds over the decay, fades with the audio |
| 9 | Technical | 5 | No black or duplicated frames (every rendered frame's mean luma scanned; no frozen frames before the logo), exact frame counts via the concat assembler |

## What went wrong on the way (and was fixed)
- Raw Artec frame upside down -> levelled with a flip + RANSAC ground fit (tools/level.py).
- Cycles persistent data killed all lights from s5 frame 36 -> persistent data off (tools/shot.py), frames re-rendered.
- s7 passed straight overhead -> camera roll snapped ~90 deg in one frame before the cut -> re-shot from behind, 12 deg off vertical.
- Licence plate characters legible in the rear 3/4 -> flattened onto the plate plane.
- Grid from `ive beats` (117.5 BPM) drifted ~0.25 s over the track; kick-peak least-squares fit gives 116.01 BPM, 1.5 ms residual.

## Not done / open questions for the reviewer
- No door-open move: the "Side Skirt Off, Door Open" scan has no door in it.
- Front/rear marker and plate-light part scans unused (too small to read in 9:16).
