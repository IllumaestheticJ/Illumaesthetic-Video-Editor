# Self-review: Pip & Gus Ep 9 "Gluing 3D prints" (finale), v1

Output: `pip-gus-ep9-glue_v1.mp4`, 49.77 s, 1493 frames, 1080x1920, 30 fps, h264 yuv420p + AAC, faststart.
-14.0 LUFS integrated, -1.2 dBFS sample peak. Measured; nothing is estimated.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Opens on Pip next to the pile of printed bumper pieces, with the first line inside 0.1 s. No big motion in the first 1.5 s. |
| 2 | Beat sync | 4 | The music lift lands on the Part B cut (37.967 s). The cartoon cuts follow the dialogue, not the beat (series format). |
| 3 | 1:1 match | n/a | No real-to-scan cut in this format. Real footage comes in through the phone push-in, a hard cut with no dissolve. |
| 4 | Scan quality | n/a | No scan. |
| 5 | Story | 4 | Pile, then four methods by use (superglue for mold masters, epoxy fills gaps, hot staples and plastic welding for strength, acetone only for ASA/ABS), then "depends what it's for", the real timelapse, the 350Z, and the bumper on Pip's car as the series payoff. |
| 6 | Grade | 4 | Timelapse is clean and portrait. The 350Z got a light eq grade. Both read as one shop. |
| 7 | Text | 4 | Only the word-by-word dialogue captions. No numbers or specs. Nothing over real footage: the build check passes with 0 frames, after cutting the last caption page short at 37.50 s, before the phone screen reaches it. |
| 8 | Ending | 4 | Logo card for the last 3 s. Final chord 0.8 s into the card, then a 0.6 s tail fade. No call to action (owner rule). |
| 9 | Technical | 5 | All frames present. The brightness check found no blank or blown-out frames among the 1253 renders. Cuts checked by frame sheet. |

## Weak spots (for the next pass)
- E13 tag: Pip is half out of frame on the left and turned toward the car during "I printed the bumper I wanted."
  The line still reads, but a reframe (camera about 0.4 m right, or Pip about 0.3 m inward) would show their face. Re-rendering costs about 25 min (114 frames).
- E5 epoxy close-up: Gus's head is cropped at the frame edge, as staged in the animatic.
- Runtime is 49.8 s against the 42 s voice take: Part B (5 s) and the logo card (3 s) sit outside the take.

## Learned
- Corner-pinned real footage in a phone push-in will collide with the caption box near the end of the push.
  Derive the last caption's end time from `screen_corners.json` instead of hand-trimming it (`tools/ep9_gfx.py: phone_clash_t`).
- 0.75 scale at 4 spp in EEVEE was about 13 s per frame on 4 cores, with no visible loss after upscaling to 1080x1920.

## v2 (owner feedback on v1)
- Captions moved to the bottom band (y=1645). They no longer cover the characters, tools or the part in any shot (checked on a frame per shot). Text 4 -> 5.
- Hot staples: W-wave staples between copper prongs, white-hot with a halo while pressed, melt pool, then they cool orange and then to dark metal.
- Plastic weld: a soldering iron (spade tip, cord) plus a white filler rod fed into the tip, with light smoke. The white bead is subtle against the white part.
- Finished 350Z: DSCF6605, a straight-on front view with a slow push-in (was DSCF6634, off-angle).
- Still open: Pip is half out of frame on the left in the E13 tag.

## v3 (owner feedback on v2)
- Table layout: mold box lengthwise on the table end, acetone back-left. The master turns and lands inside the box. `--ep9 clip` finds 0 hand, tool or part vertices inside a box wall or the jar on all 1253 frames. The E2 camera was panned so the whole drop is in frame.
- Finished 350Z: DSCF6633 (outdoors after the job), front 3/4.
- E13 ending reframed: Pip is 3/4 to camera with the face visible, and the bumper stays clear.
- Learned: run a numeric interpenetration check on every frame after any prop/layout change. A contact sheet missed the box overlap in v1/v2.
