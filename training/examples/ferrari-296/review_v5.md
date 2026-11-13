# Ferrari 296 GTB scan reel v5 - self-review (v4: review_v4.md)

User on v4: "re-edit it to this song (Buckshot Roulette OST - General Release), learn from the GT3RS video editor on what
to change. right now, not enough of the parts are blown up or shown."

v5: 9 moving parts (v4: 7) - hood, front bumper, + FRONT WHEEL (arch filled from the wheel-off "Brake Disk" state scan:
disc, caliper, hub, liner), fender, side skirt, rear bumper, diffuser, engine cover, + EXHAUST TIP. GT3RS pattern:
every part comes off on a kick where the camera is and STAYS off (progressive explode), one label per part, then all 9
blast out together on the drop (k57), drift, fly home k69 and lock k71, fade, logo (660 px).

Output: `/home/user/media/work/f296/out/ferrari_296_v5.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.00 s (1140 frames).
Cut frames 124, 298, 347, 446, 521, 732, 956.

Checked: max luma of every render frame (0 bad); first/quarter/middle/three-quarter/last sheets of the new shots;
frames at every label window before placing labels and again composited (labels type on, all complete); per-frame
near-duplicate + dark scan of the final mp4 (0 / 0 before the fade); cuts vs measured kicks; `ive director`; probe.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car turning from frame 1 over the intro bars. |
| 2 | Beat sync | 5 | Kicks measured on the decoded 40-120 Hz band; every cut within +-16 ms (half a frame) of a kick; drop cut on k57. Part motions start on kicks (wheel k27, fender k30, skirt k35, rear bumper k37, diffuser k38, cover k42, exhaust k46, blast k57, lock k71). |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 3 | Composite interiors ragged where state scans overlap; rear bumper inner face speckled; wheel bottom 31 mm completed by rotating the wheel 144 deg (5 double spokes, spoke-for-spoke). |
| 5 | Story | 4 | front -> wheel -> side -> rear -> everything off from above -> drop blast -> lock. Parts stay off, so by the breakdown the car is visibly stripped. |
| 6 | Grade | 5 | One AgX silver look across old and new shots. |
| 7 | Text | 4 | 9 labels, one per part, scan shots only, wording from scan files, no numbers. Short windows on the side shot (30-32 frames) because the parts come off fast on consecutive kicks. |
| 8 | Ending | 5 | Lock on k71, fade, logo in on k77 with the track fade. |
| 9 | Technical | 5 | Spec correct; 0 duplicated/black frames before the fade. |

## Open points
- `ive director`: s1_wide ~ v5_drop (IoU 0.71) - bookend whole-car view, kept. v5_drop "dead frames 1.7 s" = the locked
  car holding before the fade, kept.
- The drop opens with the front bumper partly leaving frame bottom-right.

## For the next agent
- Wheel axle: least-squares intersection of tread-triangle normals, not a hub-face circle fit (that was 100 mm off).
- shot.py: aiming the camera target LOWER moves the subject UP in frame.
- Don't retime interpolated renders with `speed:` (drops 1 frame in 19 -> judder); change `src_fps` instead.
