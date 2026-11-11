# A90 Supra scan-process reel v1 (240SX format, option b) — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/a90_scan_process_v4.mp4` — 1080×1920, 30 fps, yuv420p, H.264 + AAC, faststart, 31.0 s.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | the real Supra pulls up behind the camera car from frame 0; 1:1 transformation at 3.17 s (bar-2 downbeat, as in the approved 240SX at 3.07 s), not inside 1.5 s |
| 2 | Beat sync | 5 | all 6 cuts within ±15 ms of the measured kicks in the delivered audio (3.181, 8.185, 9.433, 10.681, 15.679, 16.306); holds vary 5/8/2/2/8/1/12 beats; parts land 18.18/19.43/20.68; zoom-out lands 25.68 |
| 3 | 1:1 match | 5 | cam_A (fixed 28 mm, RMSE 4.2 px); output frames 94/95 onion: exhausts, emblem, badge, lamps, plate recess, mirror and roofline align; silhouette bbox of s1 frame 1 within 1-7 px of the solved render |
| 4 | Scan quality | 4 | silver on black; no ground; exposed rear/front structure after the carve is the chassis scan's own underside and reads a little ragged around the tail-light cut; no wheels in any A90 scan (car on stands) |
| 5 | Story | 3 | real car → becomes scan → bumpers off (inside+outside) → x-ray reassembly → listing. **No footage of the crew scanning or removing parts exists** (option b), so the "scan process" beat is carried by the scan explodes + the real bumper-off shop shot |
| 6 | Grade | 4 | all HLG clips tonemapped (hable); shop clip is cooler/brighter than the dusk street clips |
| 7 | Text | 5 | only on scan shots; STL-header numbers (8,400,496 chassis; 1,989,952 + 1,991,743 = 3,981,695 front bumper); inside+outside verified on the renders for both bumpers; ≤2 items |
| 8 | Ending | 4 | x-ray morphs to the listing grey on the solved listing camera (IoU 0.955), 0.5 s dissolve; title → logo → ILLUMAESTHETIC.COM last; the track ends hard at 29.75 s so the last 1.25 s of the URL card is silent (brief: ~31 s) |
| 9 | Technical | 5 | 930 frames, no black frames; a few cloned frames at shot tails (render/interp length padding), none across a cut |

## Known issues / next version
- If the shop ever films the A90 being scanned or a bumper/tail light coming off, swap the shop + pan inserts for it and add a second 1:1 cut on the part-state scan (the 240SX front-bumper pattern).
- The listing screenshot carries the viewer's "Drag to rotate" hint and buttons during the dissolve.
- Tail-light scans unused (no matching footage, partial-housing scans only).
