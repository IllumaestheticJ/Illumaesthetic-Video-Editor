# Self-review — Subaru Impreza GD trio (bugeye / blobeye / hawkeye) scan showcase, v1

Deliverable: `/home/user/media/work/gd3/out/subaru_gd_trio_v1.mp4`. 1080×1920, 30 fps, 18.9 s, scan only.
Directed by the scene-director agent (`direction.md`); built after the user's notes on the blobeye reel v3: "video too long,
focuses too long on the wrong things", "logo too small", "change music to rally house - do a showcase of all 3 GD scans".

Five camera moves down the car's left side (front 3/4 → front detail → rear 3/4 → rear detail → top). Each is rendered on the
three full-car scans, which are registered into one frame, and cuts bugeye → blobeye → hawkeye on a kick from the same camera.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole bugeye moving from frame 1 with its name; first car swap at 1.7 s. |
| 2 | Beat sync | 5 | All 15 cuts measured on the decoded audio of the delivered file: −17 to +11 ms from the kick attack, mean −3 ms. |
| 3 | 1:1 match | 4 | Car-to-car instead of IRL-to-scan: roof, glass and doors hold still across every cut (hawk 1.5 mm, bug 2.4 mm median to the blobeye). Not measured in pixels on the final file. |
| 4 | Scan quality | 4 | Full-car scans only, as captured. Open grille holes on the blobeye and hawkeye; licence plates legible in the rear shots. |
| 5 | Story | 4 | One idea: same shell, three faces. No parts, no states. |
| 6 | Grade | 5 | Light rig pinned to one bbox for all cars; every segment passed the luma check (≥ 0.98). |
| 7 | Text | 5 | Three names only, on black under the car, one at a time. No years (not in the scan data). |
| 8 | Ending | 4 | 720 px logo cut in on the last kick, 1.8 s, fades with the music tail. |
| 9 | Technical | 4 | yuv420p, AAC, faststart. One repeated frame at each cut (assembler hold). |

## Director report
`ive director` flags the same-camera car swaps as repeated views. They are the point of the reel, reviewed and kept.

## Changes from the director's plan
- Top view focal 30 → 38 (car filled about 55 % of the frame height in the preview).
- Logo held 1.8 s instead of 1.5 s, with a 0.1 s fade-in on the kick.

## Open for the user
- Model years on the labels (left off).
- The blobeye bumper-removed scan (left out; earlier brief made it the hero).
- Hawkeye has 16 beats on screen against 12 each for the other two.

## v2 (user: "re-edit to this music", uploaded RALLY HOUSE 002)
Deliverable: `/home/user/media/work/gd3/out/subaru_gd_trio_v2.mp4`, 20.43 s. Same 15 renders, re-timed (`tools/make_yaml_v2.py`).
- Track: 122 BPM, bar 1.967 s, syncopated; break 11.83-15.81 s, drop at 15.81 s. Music starts at 9.94 s.
- Structure: bugeye on the last intro bar, blobeye from the last kick into the break, hawkeye on a synth accent in the break
  (14.03 s, not a kick), face detail on the drop, then a car swap every half bar; the blobeye top view holds a full bar.
- Beat sync 5: 14 kick cuts measured on the delivered file's decoded audio at -16 to +17 ms (half a frame is 16.7 ms).
- Playback 12-14.4 src fps for most segments (planned 15); the bugeye top view runs at 6.6 src fps over a full bar - slowest
  motion in the reel, interpolated.
- Hawkeye front-detail and top segments play their first half only, so the hawkeye no longer gets extra screen time.
