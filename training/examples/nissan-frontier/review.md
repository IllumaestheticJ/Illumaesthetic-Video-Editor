# Nissan Frontier Pro-4X -> RONIN reel v6 - self-review (training/rubric.md). Earlier: review_v5.md ... review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v6.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, 53.6 s, 1608 frames.
v6 (user notes on v5): grille install without clipping + grille lights, bumper bar, wheels modelled from the SEMA clips, higher
lift (0.20 m), livery shot lands on the camera solved against IMG_3223 -> 1:1 CUT to the real truck -> IMG_3239 side pass ->
MotoIQ photo + logo card.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | unchanged |
| 2 | Beat sync | 5 | cut frames on measured onsets: +4/-9/-15/+11/+3/+2 ms for the six new cuts (1:1 cut +11 ms) |
| 3 | 1:1 match | 4 | solve RMSE 2.8 px (6 landmarks, focal fixed 28 mm, 6.7 deg roll); onion match/check_3223_final.jpg: cab, grille, headlight, mirror, wheels, bar overlap; real truck has a roof rack/lights and rock sliders the scan lacks; front-left wheel is articulated on a rock |
| 4 | Scan quality | 3 | grille + fenders = team CAD; wheels, bar, skid, LED bars = stand-ins modelled from footage; turbo = label only |
| 5 | Story | 5 | stock scan -> sections -> Ronin upgrades -> livery -> the real truck |
| 6 | Grade | 4 | HLG clips tonemapped; livery teal a little brighter/greener than the real wrap |
| 7 | Text | 4 | labels only over scan shots, none over the real footage; logo sits below the photo, not on it |
| 8 | Ending | 5 | real footage payoff, then photo + logo card over the track's tail |
| 9 | Technical | 5 | exact frames, luma clean (one flagged jump = parts crossing frame) |

Known gaps: Ronin side shots are wide (truck small in 9:16); Q2/Q3 labels are on screen ~0.5-0.6 s each (tight); MotoIQ photo is
the 928x580 image the user attached (soft at 1080 wide).
