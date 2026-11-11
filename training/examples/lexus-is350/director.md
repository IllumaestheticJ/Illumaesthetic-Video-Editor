# Lexus IS350 2026 facelift: shot plan (director stage 2, V2)

This plan follows the scene order in `direction.md` and does not change it. The cameras, the part keys (master timeline T = 0 at the 16.063 drop), the labels and the open questions are all in that file. This file adds one focus per shot, the cut list, the holds and the budget.

## Shot table

| Section | Shot | Start-end (s) | Focus (one) | Part action | Why it earns the time | Source |
|---|---|---|---|---|---|---|
| Whole | s2_front34L | 0.000-4.064 | Whole front clip | none | The only closed-exterior wide shot. It orients the viewer | **Re-render**, wider (r +0.55, centre y -1.65) |
| Fascia | s3_grille | 4.064-5.564 | Left grille corner / fog intake | none | 2 mm mesh detail | Reuse |
| Fascia | s8_badge | 5.564-8.064 | Badge bar + centre mesh | none | The facelift signature, never seen close in v1 | **New** |
| Fascia | s4_lamp | 8.064-9.564 | Right headlamp / corner intake | none | Finishes the left-to-right sweep | Reuse |
| Hood | s5_hood f7-46 | 9.564-12.564 | Hood | Hinge opens to the captured pose | A real state | Reuse (trim the in-point, 0.89x) |
| Hood | s5b_bay | 12.564-16.063 | Engine bay | Hood held open | Moves in on the section. Breathes through the break | **New** |
| Bumper | X1_bumper_off | 16.063-18.063 | Front bumper | G forward 0.6 m, then up and out of frame | The drop | **New** |
| Bumper | X1b_structure | 18.063-22.063 | Structure behind the bumper | none (G off screen) | Hero hold: reading the removed-state data | **New** |
| Bumper | X2_inner | 22.063-26.063 | Bumper inner face | Ducts toward the camera, fogs out the front, then radar toward the camera and bracket up | Mounting sides that only part scans can show | **New** |
| Bumper | X3_reassembly | 26.063-30.063 | Bumper returning | Parts back, G home, lock at 28.563 | Resolution, then fade 29.563-30.063 | **New** |
| End | logo | 30.063-33.600 | Small logo | — | Ends with the music's decay | Rebuild the card |

## Cut list (removed from v1)

| Removed | Why |
|---|---|
| s1_front34R | Redundant with s2 (the same face, mirrored) and crops the near fender |
| s6_top | Off-focus (speckled hood, cut edge). Shows the hood closed again after s5 opened it. A rotation that adds nothing |
| s7_explode (single wide orbit, all parts at once) | Too wide, no section focus. Replaced by X1-X3 |
| s8_hero | A third whole-face view, plate dead centre |
| s5 frames 1-6 | A closed-hood wide shot that repeats s2 |

## Holds over 0.75 s

| Hold | Reason |
|---|---|
| s5b, 15.06-16.06 (break) | The camera keeps pushing slowly. The music drops the kick, and the open bay is the reason for the pause |
| X1b, 18.06-22.06 | A slow push with no part motion, so the viewer can read the structure and the two labels (feedback C) |
| X3 lock, 28.563-29.563, then fade | Shows the bumper seated. Slight pull-back |
| Logo, ~2.5 s visible | Ends the video with the track |

## Render budget (15 fps finals)

| | Shots | Frames |
|---|---|---|
| New / re-render | X1 33, X1b 63, X2 63, X3 63, s2 63, s5b 55, s8_badge 41 | **≈ 380** |
| Reused unchanged | s3 24, s4 24, s5 40 | 88 |

- The new renders take about 1.5-2 h on CPU at 14-19 s/frame. Run them one at a time, in the order above.
- Before any of them, cancel the queued old s7/s8 (render_queue.sh pid 10241).
