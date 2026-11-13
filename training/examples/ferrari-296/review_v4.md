# Ferrari 296 GTB scan reel v4 - self-review (v2: review_v2.md, v1: review_v1.md)

v4 answers the all-reels brief + addendum A-D (relayed from the user) on top of the v3 director plan:
scene order by the scene director (direction.md) - whole car -> wheel -> FRONT (hood opens from the scanned open state,
bumper out and turned to show its inner face, then the FRONT BUMPER REMOVED hero) -> SIDE (fender, skirt off) -> REAR
(REAR BUMPER REMOVED hero, louvre lifts off -> ENGINE BAY) -> full explode locks home -> fade -> small logo.
Each section appears once (front -> side -> rear, no ping-pong). Labels only over the bumper-removed / engine-bay scan
shots, wording from the scan files.

Output: `/home/user/media/work/f296/out/ferrari_296_v4.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC, 39.00 s (1170 frames).
Cut frames 153, 222, 482, 622, 762, 901, 1005 (assemble_cuts.py, no repeated frame at any cut).

Checked: max luma of every render frame (caught f5_front 31-40 black again even in a fresh process -> re-rendered);
first/middle/last contact sheet of every shot (rule A); label frames composited (two labels moved/shortened + halo
after they ran over bright geometry); per-frame near-duplicate scan of the final mp4 (found 2-3 clone-padded frames at 4
clip ends -> fixed, now 0); `ive director` (one flag, see below); cuts against the decoded audio.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, centred with margins (y 607-836 of 1440), turning from frame 1. |
| 2 | Beat sync | 4 | All cuts on the 103.4 BPM grid. Measured on the decoded track: the sub-bass is a sustained drone, no kick transients. The two cuts with a strong broadband transient within 2 frames were moved onto it (153: +13 ms, 482: +3 ms). The other five have no strong transient within +-150 ms (beatless passages), so they stay on the grid. |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 3 | Composite interiors are ragged where the state scans overlap (frunk holes, bumper inner face speckle); grille gaps. Real data, not hidden. |
| 5 | Story | 4 | One continuous sequence per section, hero beats on both bumper-removed scans, opening only from data (hood: scanned open state; engine louvre lifts off, no hinge, no trunk shot). |
| 6 | Grade | 5 | One AgX silver look; logo card black matched (7,7,9). |
| 7 | Text | 4 | 3 labels, scan shots only, no numbers: FRONT BUMPER / REMOVED - CRASH BEAM; REAR BUMPER / REMOVED - REAR STRUCTURE; ENGINE BAY / ENGINE COVER REMOVED. Dark halo (ScanHUD `shadow: true`) keeps them legible over bright scan; front sub line still crosses some structure. |
| 8 | Ending | 5 | x_lock fades to black (0.5 s), then the small logo (380 px) fades in/out with the track's fade. |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, faststart; 0 black frames outside the intended fade, 0 duplicated frames before the logo. |

## Open points the reviewer may push on
- `ive director` flags s1_wide ~ x_lock (IoU 0.70): both are side-ish 3/4 wides of the whole car. Kept: x_lock is the
  exploded car flying home (the brief's "exploded view that reassembles"), and it is the bookend before the fade.
- x_lock opens with rear-bumper pieces entering from the frame edges; x_side's skirt slides out of frame at its end.
- Frames inside clips are stretched up to 2.8 % (input rate 14.58-14.81 fps instead of 15) to avoid clone padding.

## For the next agent
- `ive assemble`/_render_clip pads short interpolated clips by cloning the last frame (tpad). minterpolate turns N
  renders at r fps into only (N-1)*30/r - 1 frames, so a clip cut to 2N frames stalls for 2-3 frames before its cut.
  Scan the final mp4 for near-identical consecutive frames; fix by lowering src_fps to (N-1)*30/(n+2) (assemble_cuts.py
  does this) or by rendering one extra 15 fps frame per shot.
- Persistent data off + 40-frame chunks still produced a 10-frame black run once: the per-frame luma scan is mandatory.
- A generated track may have no kick at all in the low band; measure transients in the 2-8 kHz band before claiming
  "cut on the kick".
