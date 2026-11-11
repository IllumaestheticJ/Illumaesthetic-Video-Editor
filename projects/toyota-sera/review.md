# Toyota Sera scan reel - self-review (training/rubric.md)

Deliverable: `/home/user/media/work/sera/out/toyota_sera_v2.mp4` - 1080x1920, 30 fps, 39.27 s, scan only, no text.
Shot order: low front 3/4 turntable -> rear 3/4 orbit -> front wheel ECU -> nose/headlamp slide -> hood opens ->
both butterfly doors open -> rise to top-down -> exploded view (5 panels) -> ILLUMAESTHETIC logo.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | The car is turning from frame 1. There's no transformation in the first 1.5 s; the brief's Temerario order opens on turntables |
| 2 | Beat sync | 5 | Cuts measured from frame diffs at 4.833/9.633/12.033/14.433/17.433/21.633/24.033/34.833 s = -2 ms from the kick grid (0.0355 + 0.59999 n), re-measured on the output's own audio. Big moments sit on 8-beat phrase downbeats: separation 24.035, lock 33.635 |
| 3 | 1:1 match | n/a | Scan-only reel (brief). The IRL footage is listed in clips.md for a future 1:1 version |
| 4 | Scan quality | 4 | No ground scraps (footprint crop + islands); levelled frame; every state/part registered (0.8-3 mm, overlays looked at). Weak spots: grille vents and a few hood specks are dark scan holes (real data, small, moving); a thin real flange under the hood's leading edge rises with it |
| 5 | Story | 4 | Reads as "this car, fully scanned, inside and out": exterior, details, real engine bay (Hood open), real interior (Door Open), every panel a real scan. No IRL, as briefed |
| 6 | Grade | 5 | Satin silver on black, AgX, -0.35 EV, measured: 0 EV clipped 9 % of car pixels in a front 3/4; the house look is consistent across every shot |
| 7 | Text | 5 | None (brief) |
| 8 | Ending | 4 | Logo card hard-cuts on beat 58 (34.835 s) and fades with the track's decay. The generated track stops abruptly at 38.435 s, so the last ~0.8 s is reverb tail under the fade |
| 9 | Technical | 4 | 1080x1920, 30 fps, yuv420p, AAC 44.1 kHz, faststart, no black frames. The assembler holds the last frame for 1 frame before 3 of the cuts (522, 648, 1044) |

## What I'd want the reviewer to check
- Exploded view size: tightened after v1 (car read ~45 % of frame width). Panels stack above the car and stay in frame.
- Hood opening on frames ~15-20 of that shot: the hood is a full-car skin + the open capture's inner frame. Fixed in
  this version after the first final showed the inner frame poking through, but it's the most constructed object here.

## Process notes for the next agent
- Hinges fitted from open-state captures (tools/hinge_fit.py) work for any axis: the two butterfly doors came out
  mirror-symmetric independently (axes (+-0.60, 0.68, 0.41), 56/57 deg, ~1.05 mm landing).
- Taking a panel's inner side from the open capture: keep only triangles that sit *below* the closed skin after the
  inverse hinge, and loosen landing for closed-panel candidates, or skin strips stay behind.
- 'Rear Bumper Removed' and '... No Tail Lights' on Drive are the same file (md5).
