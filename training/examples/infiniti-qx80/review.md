# Infiniti QX80 scan reel v3 - self-review (training/rubric.md)

Output: `/home/user/media/infiniti-qx80/out/infiniti_qx80_v3.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.80 s, 1164 frames.
v2 = the user's all-reels v2 brief (relayed by the parent + WRX VA sessions) via the scene-director/director agents
(direction.md, director.md). v1 review: review_v1.md, v2: review_v2.md.
v3 = v2 re-framed for the parent addendum (A cropping): N0, s5, N1, N2, N3 re-rendered; first/mid/last of every shot checked
on the delivered file (nothing clipped except the grille/wheel detail shots, which fill the frame by design). B: each section
appears once (direction.md table). C: no bumper-removed state scan exists for this car -> no hero beat, no labels.
D: only the hood opens (registered open-state scan).

| # | Criterion | v1 | v2 | Notes |
|---|---|---|---|---|
| 1 | Hook | 4 | 4 | Whole car in frame, orbiting from frame 1 (v1 cropped the rear). Slow string intro, no transformation in 1.5 s. |
| 2 | Beat sync | 5 | 4 | Cut frames 159/237/315/471/705/822 exact; vs decoded audio (cutcheck.py, 1 ms RMS half-rise): +4, +35, -3, +107, -42, +1 ms. The +107 cut (music 16.362) sits in a flat sustained string passage (-18/-19 dB, no hit within 0.4 s) - kept on the grid. Last cut is the fade into the logo (34.562). Part moves land on beats 17.01/18.96/20.91/21.56 (lift)/24.81/25.46, hood shuts on the 32.00 step. |
| 3 | 1:1 match | n/a | n/a | Scan-only. |
| 4 | Scan quality | 3 | 3 | Clean car for the opener, close-ups and the end (reassembly swaps to the full car at lock - no seams). Exploded section: part scans show streaky shading where they sit on the car, and the fender/bumper-corner holes are visible while parts are out (kept small: 0.25-0.45 m moves, toward the lens). |
| 5 | Story | 4 | 5 | Order follows the scan data: whole -> grille -> wheel/vent -> hood state -> RF corner parts one per hit (camera stays on the section) -> rear parts -> reassembly from the unseen front-left -> fade -> small logo. No repeated view; v1's redundant rear orbit and rotating top-down cut. |
| 6 | Grade | 5 | 5 | All scan, AgX. Luma scan of every render: no dropouts (persistent data off on animated shots). |
| 7 | Text | 5 | 5 | None (brief). |
| 8 | Ending | 4 | 5 | 1.3 s fade to render-black, then a 360 px logo over the track's fade; video ends as the music goes silent. |
| 9 | Technical | 5 | 5 | Spec met; no black/dup frames at cuts. |

Likely reviewer flags: streaky part shading during N1/N2; whole-car shots (N0, N3) leave the car ~55-60 % of the 9:16 width - the price of no clipping on a 5.4 m SUV.
