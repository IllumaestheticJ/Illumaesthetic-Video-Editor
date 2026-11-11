# A90 v2 plan - mirror the Temerario reel shot for shot

Studied the reference frame by frame (2 fps sheets, /home/user/media/a90-supra/ref/seg_*.jpg; 1440x1920, 24 fps, 39.8 s).

## Temerario breakdown (what the user wants)
| # | Time | Shot | Camera | What moves |
|---|---|---|---|---|
| 1 | 0.0-4.0 | Side profile, whole car ~45 % width | static/slow track, eye level | fade up from black over ~1.5 s |
| 2 | 4.2-7.9 | Front 3/4, low | slow orbit/push | nothing - car intact |
| 3 | 8.0-11.4 | Rear 3/4, low | slow orbit | nothing |
| 4 | 11.5-16.2 | Front corner: opens tight on wheel + suspension, pulls back | slow pull-back | ~12.5 s hood lifts on its hinge, bumper/splitter slide forward, reveals radiators, crash structure, suspension |
| 5 | 16.3-20.2 | High overhead diagonal (car corner-to-corner) | slow drift | front parts keep separating forward; front wheels + suspension pull out sideways |
| 6 | 20.3-24.4 | High rear 3/4 | slow orbit | rear/top panels rise and **stack in layers above the car**; doors open; wheels out |
| 7 | 24.5-28.1 | Tight low side, car fills frame | slow track | layered stack holds above; internals visible |
| 8 | 28.2-31.8 | Wide side - the full exploded line-up | slow | everything separated: layers above, wheels out, front/rear clips fore/aft |
| 9 | 31.9-35.5 | Rear 3/4 high | slow orbit | **reassembly** ~32-34 s, then whole car small; fade to black ~35.5-36.5 |
| 10 | 36.5-39.8 | Logo small (~25 % width) on black | - | fade in ~37, hold, fade out ~39 |

Rules taken from it: ~4 s shots, quick soft transitions; the explode starts INSIDE a close-up (shot 4) and runs ~20 s
(half the reel), across several angles; parts separate along clean axes (up in stacked layers, wheels/suspension
sideways, front/rear clips fore/aft); full car with wheels and suspension, so nothing hollow is ever revealed;
light grey satin, darker crevices; reassembly -> fade to black -> small logo.

## A90 mapping (pending: suspension + interior scans from the user's folder)
| # | Time (120 BPM, 2 bars = 4 s) | A90 shot | Parts |
|---|---|---|---|
| 1 | 0-4 | side profile, fade up | car + suspension/wheels if scanned |
| 2 | 4-8 | front 3/4 low | |
| 3 | 8-12 | rear 3/4 low | |
| 4 | 12-16 | tight right-front arch -> pull back; bumper slides forward, fender out, structure revealed | fb_out+fb_in, fender, under front bumper, under fender, suspension |
| 5 | 16-20 | high overhead diagonal | front clip forward, suspension corner sideways, liners |
| 6 | 20-24 | high rear 3/4 | rear bumper aft, trunk lid (2024, registered) rises, interior layers stacked above |
| 7 | 24-28 | tight low side | stack holds |
| 8 | 28-32 | wide side, full exploded line-up | all |
| 9 | 32-35.5 | rear 3/4 high, reassembly on the impact, fade to black | |
| 10 | 36-40 | small logo fade in/out | |
Score: retime cues.json to 120 BPM (shots on 2-bar lines, impact on the reassembly at 34.0 s), material toned down
toward the reference grey, soft 0.3 s transitions instead of hard cuts.
