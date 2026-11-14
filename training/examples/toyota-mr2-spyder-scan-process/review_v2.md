# Toyota MR2 Spyder scan-process reel v2 - agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/mr2_scan_process_v2.mp4` - 1080x1920, 30 fps, yuv420p, AAC, faststart, 24.03 s.
v1 was assembled internally only; v2 folds in the user rules relayed for all V1 reels (scene director, lighting/cut checks,
cropping, redundancy, bumper-removed rule, HUD exact counts) before the first delivery.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | real crew scanning from frame 0; 1:1 cut to the scan on the drop at 3.20 s (6 beats in, like the 240SX's 3.07 s) |
| 2 | Beat sync | 4 | cuts measured on the DECODED audio (tools/cutcheck.py, 1 ms RMS half-rise): 193/353/418 within 0.5 fr, 96 within 1 fr, 289/546 ~+0.5-0.9 fr to the main hit (music start moved +67 ms after the first measurement) |
| 3 | 1:1 match | 4 | cut A (front 3/4, silhouette solve, f 22 mm): windshield, mirror, headlight, wheel coincide; cut B (rear): tail lamp, plate recess, louvres coincide. Real car has a scooped hood + wing that no scan has, so those vanish across the cuts |
| 4 | Scan quality | 4 | silver on black; clean; dark scan holes in the front intake slit and lower rear grille; stock hood |
| 5 | Story | 4 | scanning (front) -> scan -> hardtop lifted off -> scanning (rear) -> scan -> registered lid-open state, lid explodes (ribbed underside + louvred top) -> x-ray reassembly -> listing at the same angle |
| 6 | Grade | 4 | FX3A S-Log3 graded with a generated S-Log3/S-Gamut3.Cine->709 LUT; DJI bt709 untouched; warmth consistent |
| 7 | Text | 5 | only on scan shots; exact STL header counts (14,999,997 / 7,000,064) as static labels (counter bug avoided); "inside + outside" verified on renders of the lid alone |
| 8 | Ending | 4 | x-ray morphs to listing grey on the hero angle and dissolves into the listing; title, logo, URL last; ends on the music's decay |
| 9 | Technical | 4 | no black frames; luma continuous in every render (no light dropouts); IRL clips are 23.976 so 24->30 pulldown repeats every 5th frame inside IRL shots |

## Known issues / for the reviewer
- No front-bumper-removed section: the 2024 front-end state scans do not register to this car (nose/fenders 50-70 mm off), so
  showing them would be data that is not this car's front. Needs a new front-removed scan of this car if wanted.
- Real-footage framing: DJI clips are already full native portrait; the FX3A hardtop shot is now a 3:4 window on a blurred fill.
- Scale jump at 18.2 s (tight lid -> wide x-ray start); the wing and scooped hood exist only in footage.
