# C5 Corvette scan-process reel v2 - agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/c5_scan_process_v2.mp4` - 1080x1920, 30 fps, 29.97 s (cuts K3/K7 nudged 1 frame to the measured kicks: all cuts 0-17 ms), H.264 yuv420p + AAC.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | real stock C5 rear pass, 1:1 cut to the scan on the kick drop at 2.17 s (track intro has no kicks before 9.32 s, so 2.2 s of IRL is the minimum on-beat hook) |
| 2 | Beat sync | 5 | 7 hard cuts at frames 65/163/229/294/327/491/524, 0-17 ms after the kick peaks measured in the delivered audio; dissolve into the listing sits between K18 and K19 |
| 3 | 1:1 match | 4 | cut A (rear 3/4, cam_A RMSE 5 px): taillights, lettering, plate recess, silhouette overlap within a few px. Cut B (stripped right front, RMSE 14 px): door edge, arch and sill align; wheel differs (car runs aftermarket wheels, scan has stock) and the real hood is up while no hood-open scan could be registered |
| 4 | Scan quality | 3 | silver-on-black; stripped composite is clean after dropping duplicate hood / ground / re-steered wheel; some ragged scan borders on the exposed structure and the state-scan front edge |
| 5 | Story | 4 | real car -> scan -> crew pulls fender + bumper -> stripped scan, parts out + spin (inside + outside) -> real removed fender -> x-ray reassembly -> listing. Missing: no shot of the handheld scanner (none exists in the dump) |
| 6 | Grade | 4 | all DJI clips are SDR bt709 (no HLG); late-afternoon outdoor warmth consistent across IRL shots |
| 7 | Text | 4 | only on scan shots, <=2 items, numbers from STL headers (8,255,611 full car; 6,293,120 = Fender outer 2,580,796 + Fender Inner 3,712,324); inside+outside verified from raw normals. v1's counter showed 8,247,549 (ScanHUD easing bug) - replaced by a static label |
| 8 | Ending | 4 | x-ray reassembly ends on the listing hero's angle (silhouette IoU 0.91), morphs to its grey, dissolves; title -> page -> logo -> URL last; music fades with the card |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC; no black/duplicate frames at cuts |

## Known issues / next version
- Cut B: a hood-open state would make the 1:1 tighter; the 'C5 Supplement Hood Open' scan needs a manual initial alignment before ICP.
- Scan shots end slightly small in A (car ~70 % width at the end of the pull-back).
- If the team has any footage of the Artec Leo on this car (2023 or 2024 sessions), it would replace the 0059 fender shot.

## v2 (user feedback on v1: "great, but don't spin or flip unless it shows the backside")
- scan_B parts no longer spin 360 deg: each turns once (fender -146 deg, bumper +124 deg about Z) so its scanned inside faces the camera and holds
  under the INSIDE + OUTSIDE label. Everything else unchanged; cuts unchanged.
