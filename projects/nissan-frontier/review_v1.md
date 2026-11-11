# Nissan Frontier Pro-4X scan reel v1 - self-review (training/rubric.md)

Output: /home/user/media/work/frontier/out/nissan_frontier_v1.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.37 s (1151 frames).
Scan only (no IRL footage, no text). Music: the reel's own generated track (nissan-frontier_track.mp3).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Front 3/4 turntable moving from frame 1; no transformation until the drop (by design: scan-only Temerario style) |
| 2 | Beat sync | 5 | Cuts measured from frame diffs: 4.867/9.667/12.100/14.500/19.333/22.967/33.833 vs 4.852/9.681/12.095/14.509/19.337/22.959/33.822 - all within +-15 ms (< 1/2 frame). Close-up lands on the drop (9.681); bumper lands on 16.923, hood on 18.130; parts start home on the 27.787 crash and lock on 31.408 |
| 3 | 1:1 match | n/a | No IRL footage in this brief |
| 4 | Scan quality | 4 | Lift pads/ground removed, mirrors kept; silver on black. No wheels anywhere (truck was scanned on a lift) - the arch close-up (s4) shows the real suspension but reads busy/dark in its lower half; hood underside is the outer shell only (closed-hood scan) |
| 5 | Story | 4 | Turntables -> grille/arch close-ups -> front opens (bumper off, hood up, engine bay from the 'Bumper and Hood Removed' scan) -> top-down -> explode (hood, bumper, grille, flares) -> reassembled -> logo |
| 6 | Grade | 4 | AgX, -0.5 EV; car median 183 / p90 249 vs ref ~200/231 - top-down roof still close to clipping |
| 7 | Text | 5 | None (brief) |
| 8 | Ending | 5 | Logo card (illumaesthetic.com header logo) from 33.82 s, fades with the track's tail; video ends 38.37 s where the music has decayed to -51 dB |
| 9 | Technical | 4 | Spec correct; one held frame before each cut (assembler's documented cut compensation); 1 frame shorter than planned (1151 vs 1152) |

What to try next if the reviewer wants more: replace s4 with a rear-quarter/bed-rail close-up, or light the arch from below;
split the flares into left/right so they move outward instead of up; a slower separation ease (parts are fully out ~0.6 s after the cut).
