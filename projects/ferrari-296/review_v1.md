# Ferrari 296 GTB scan reel v1 - self-review (training/rubric.md)

Output: `/home/user/media/work/f296/out/ferrari_296_v1.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.97 s (1169 frames).
Checked: contact sheet of every shot, labelled strips +-1 frame around all 8 cuts, full-size frames mid-separation and
mid-reassembly (interpolation ghosting), per-frame max-luma scan of every render (caught 127 black explode frames).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Turntable moves from frame 1, music enters at 0.43 s. Scan-only brief, so no IRL->scan transformation to open on. |
| 2 | Beat sync | 5 | Cuts measured from frame diffs at frames 152, 292, 361, 431, 553, 622, 692, 1040 = round(accent*30) of the track's measured accents (5.077, 9.719, 12.04, 14.361, 18.423, 20.744, 23.066, 34.671). Separation starts on 23.066 (loudest), lock on 32.350 (heaviest bass). |
| 3 | 1:1 match | n/a | Scan-only reel (Temerario style); no IRL footage. |
| 4 | Scan quality | 3 | Silver-on-black, no ground or debris (front-bumper strap removed). Weak spots: front intake grille shows ragged scan gaps in the nose detail (12.0-14.4 s); frunk under the hood has dark coverage holes from the state scan (16-18 s); the rear bumper's inner edge is ragged in flight. Tail lamps (lens holes) avoided entirely. |
| 5 | Story | 4 | Temerario order: 3/4 turntable, rear orbit, wheel/brake ECU, nose detail, hood open, engine lid open, top-down, exploded view (separate -> orbit front-right to rear-right -> reassemble) -> logo. Only right-side fender/skirt exist as part scans, so the explode favours the right side. |
| 6 | Grade | 5 | One AgX look throughout; logo card black matched to the renders (RGB 7,7,9). |
| 7 | Text | 5 | No text (brief); logo only. |
| 8 | Ending | 4 | Logo cuts in on the 34.67 s beat, holds through the track's fade, fades to black by 38.97 s. |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, no black/dup frames at cuts; last frame black (fade). |

## Things the reviewer may push on
- Car size in the side-on middle of the explode (camera pulled to 9.3 m so the 6.6 m exploded length fits 9:16).
- s1/s2 both finish near a side profile (opposite sides).
- Music: generated track from the coordinating session (not a Dropbox reel track); procedural fallback in tools/music.py.

## For the next agent
- Cycles persistent data can silently produce black frames in long, heavy animated scenes (here after frame 48 of an
  8M-tri, 7-part explode). Scan renders for max luma before assembling; re-render in 40-frame chunks (`frame_range`).
- Part-state composites (tools/composite.py): per-panel fill zones + "new geometry only" (>7 mm from the car) +
  de-duplicated fills give a clean "panels off" body from Artec state scans.
