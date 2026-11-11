# Infiniti QX80 scan reel v1 - self-review (training/rubric.md)

Output: `/home/user/media/infiniti-qx80/out/infiniti_qx80_v1.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.80 s, 1164 frames.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Turntable moves from frame 1; no transformation in the first 1.5 s (scan-only Temerario brief, slow string intro). |
| 2 | Beat sync | 5 | Frame-diff cuts at 159/257/315/393/549/627/1017 = targets exactly; music t = video t + 0.66 -> 5.96/9.21/11.16/13.76/18.96/21.56/34.56 (<= 2 ms off the 0.650 s grid). Hood opens 14.41, explode separates on the lift 21.56, locks on the strongest accent 31.96. |
| 3 | 1:1 match | n/a | Scan-only brief, no IRL footage. |
| 4 | Scan quality | 3 | Silver on black, no ground, wheels/grille resolved. Faint seam lines at the fender/bumper joints in assembled explode frames (part scans vs car surface); open hood/explode reveal partial under-hood capture with dark gaps; top-down roof reads very bright (near clipping). |
| 5 | Story | 4 | Turntables -> grille/wheel close-ups -> hood opens -> top-down -> 6-panel explode + reassembly -> logo, per Temerario. Explode panels are small in 9:16 (car ~60 % width at 8.4-8.8 m); hood brushes the right edge late in the orbit. |
| 6 | Grade | 5 | All scan, AgX, consistent. |
| 7 | Text | 5 | None (brief). |
| 8 | Ending | 4 | Logo cut on the 34.56 accent, fades out with the track; music measured silent at 39.5 s (video ends 38.80). |
| 9 | Technical | 5 | Spec met; no black/dup frames at cuts (frame-diff check). |

Things a reviewer is likely to flag: explode framing small; seams at part joints; bright roof in top-down (huracan used -0.5 EV).
Re-renders done before delivery: s1 (grille was cropped off), s2 (tail lamps cropped off).
