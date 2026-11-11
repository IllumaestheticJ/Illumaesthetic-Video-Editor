# GT3 RS (992) scan-process reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/gt3rs_scan_process_v1.mp4` — 1080×1920, 30 fps, yuv420p, H.264 + AAC, 37.9 s.
Music: hf_20261111_055731 GT3 RS track (music ends ~36.3 s, faded).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | real car on the lift settles head-on, 1:1 cut to scan on the strongest hit (3.80 s) - same as the approved 240SX v4, not inside 1.5 s |
| 2 | Beat sync | 5 | 8 cuts on frames 114 229 343 424 454 564 677 791, measured on the delivered audio: -11..+14 ms from the kicks |
| 3 | 1:1 match | 4 | #1 head-on camA (9 px RMSE, onion: headlights/hood/lip on the car); #2 right side camC (6 px; mirror, wing tip, rear wheel, sill align). Front wheels removed from the scan to match the car on the lift |
| 4 | Scan quality | 4 | clean 3 mm full car; x-ray shows the scanned interior (busy in head-on); carved gaps where parts leave; two ground fragments removed |
| 5 | Story | 5 | real car -> scan -> front aero explodes -> crew scanning the arch plays out -> 1:1 on the drop -> side parts pop -> live scan on the scanner -> rear parts -> everything (incl. wheels) translates home -> listing |
| 6 | Grade | 4 | HLG tonemapped; all IRL from one session, consistent |
| 7 | Text | 5 | scan shots only; numbers from STL headers (24,999,999 full car; 450,000 intake; 1,100,000 diffuser); part list = the exploded scan files |
| 8 | Ending | 5 | reassembly orbit ends on the listing's 360-viewer angle (silhouette fit, ~6 px), morphs to its grey, dissolves; title, logo, URL last |
| 9 | Technical | 5 | no black/dup frames at cuts; whole-frame durations |

## Known issues / ideas for v2
- Opener alternative: v_0130_125414 (crew crouched under the car scanning, tilt up to head-on) - needs a new solve.
- The x-ray head-on is cluttered by the scanned cabin; a part-only silver pass over a faint x-ray could read cleaner.
- Claimed parts are the 12 Drive part scans actually exploded; the Drive folder's other part files (rear bumper, diffuser-2, trims-inner, lower skirt, hood vent interfaces, underbody) were not shown or claimed.
