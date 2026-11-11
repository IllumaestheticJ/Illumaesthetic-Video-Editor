# Subaru WRX VA scan reel v2 — self-review (training/rubric.md)

Output: `/home/user/media/subaru-wrx-va/out/subaru_wrx_va_scan_v2.mp4` (media not committed). v1 review kept in `review_v1.md`.
1080x1920, 30 fps, 923 frames (30.77 s), scan only, same generated track. Labels over scan shots only.
Plan: `direction.md` (scene-director agent: order from scan features), `director.md` (director agent: one focus per shot, redundancy cuts).

Order: whole car front 3/4 → hood-open state → **front bumper hero** (fog bezels out, bumper off and flipped to show its scanned inside, push in on the bumper-removed front end) → hood scoop lift → side profile → wing (rise from under the blade) → trunk-open push-in → top-down reassembly locking on b54 → same camera, clean car, fade → small logo. Front → side → rear → top, no ping-pong, each section once.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, front 3/4, turning from frame 1 with a 0.6 s fade up; first cut at 2.67 s. |
| 2 | Beat sync | 5 | Cuts at f80,164,353,408,462,571,626,735,790, each the nearest frame to the broadband kick attack read on the decoded audio waveform (−13..+15 ms). v1's grid was ~78 ms late (low-pass detector bias); every cut moved 1-3 frames earlier. |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 4 | Same cleaned/deplated scans. Bumper-removed front end shows its real ragged edges; the label says only what is visible (headlight housings, front structure) - no crash beam claimed because it is not legible in the scan. |
| 5 | Story | 5 | Order follows the scan inventory (direction.md). Bumper-removed state gets the longest scene (6.3 s, b12-b26) with three labels. Openings only from registered state scans (hood open, trunk open); wing is not removed (no wing-removed scan). Fewer shots (9 vs 10) and no repeated section. |
| 6 | Grade | n/a | Silver on black, AgX. |
| 7 | Text | 4 | Six short factual labels (HOOD OPEN, FRONT BUMPER REMOVED, BUMPER / SCANNED INSIDE + OUT, BEHIND THE BUMPER, HOOD SCOOP REMOVED, TRUNK OPEN), no numbers. Placed in clear black; the scoop label moved to the top because the car fills the lower frame. |
| 8 | Ending | 5 | Reassembly locks on b54, same camera continues on the clean car, fades to black; small logo (~30 % width) fades in on b58. |
| 9 | Technical | 4 | Every render frame luma-checked (no dark frames, `--no-persist`). First/middle/last frame of every shot measured for edge margins; n3_wing (clipped left), n_side (2 % margin, then off-centre) and the trunk shot were re-framed and re-rendered. minterpolate smeared the flying bumper (zigzag check); those n1 segments got real 30 fps in-between renders. |

## ive director (final)
Flags kept, with reasons (editlog): n1~n_side, n2~n3_wing, n2~n5_trunk are different sections/subjects with similar silhouettes; n4a~n4b is one continuous camera split for the clean-car swap (invisible cut). The s01~s07 flag was fixed by replacing s07 with n5_trunk.

## What the next agent should take from this
- **Measure margins on the first, middle and last frame of every shot** (bbox of luma > 25). Three of six new shots failed it after passing a single-still check.
- **minterpolate breaks on fast separate parts** (a bumper flying off): detect with the zigzag metric (|f_k − avg(neighbours)| alternating high/low). Fix by rendering only the missing even frames at 30 fps: with `seconds` chosen so N30 = 2·N15 − 1, frame 2i−1 at 30 fps is frame i at 15 fps; pre-fill and let the resumable render fill the gaps.
- **Kick grids fitted with a low-passed detector are late** (~78 ms here). Read the attack on the decoded waveform and put each cut on the nearest frame.
- `ive assemble`: the first clip renders one frame long - make it one frame short.
- Remotion `ScanHUD` label crashes on `sub: ""` (interpolate range [6,6]); use `" "` until the component is fixed.
