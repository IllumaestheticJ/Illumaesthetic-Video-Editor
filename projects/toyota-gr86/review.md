# Toyota GR86 / Subaru BRZ (gen 2) - v2 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v2.mp4` (not in git). 1080x1920, 30 fps, 1177 frames / 39.233 s,
h264 yuv420p + AAC, moov first. Scan-only reel (no IRL footage), so criteria 3 and 6 don't apply.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car fully in frame from frame 0, ~20 deg arc + push from the first frame. The v1 0.8 m dolly read as static (ive director: 4.8 s dead), so it was replaced. It is a camera move, not a transformation; the first part move is the hood at 7.4 s. |
| 2 | Beat sync | 5 | Measured on the delivered file's decoded audio (broadband 1 ms RMS, half-rise of the kick): offsets +2, -13, -7, +10, -6, +14 ms (cuts f148, 221, 515, 736, 956, 1103). Target is +-16.7 ms. The accents.py grid sits ~30 ms after the kicks, so every cut moved 1 frame earlier than the grid. |
| 3 | 1:1 match | n/a | Scan only. |
| 4 | Scan quality | 4 | Licence plate flattened in car4 + rear_bumper (tools/deplate.py); it read "9MEN074" at full res in g_rear f1 and s_stack f113 before the fix. No light dropouts: every shot luma-checked (tools/lumacheck.py), no steps > 4. The comp_explode cowl area still shows the scan's dark gaps in the bay at the d_front push-in. Those are real data, not fixed. |
| 5 | Story | 4 | Order is driven by the scan features (direction.md): whole car -> front detail -> front section (hood off, bay, FRONT BUMPER REMOVED structure) -> rear section (REAR BUMPER REMOVED, crash beam push-in) -> top stack -> reassembly -> logo. Each section plays once; no repeated orbits or reused shots; no trunk shot (closed-trunk scan only). |
| 6 | Grade | n/a | No IRL. |
| 7 | Text | 4 | 3 factual labels on scan shots only, each on black above the car: FRONT BUMPER REMOVED / HOOD REMOVED · STATE SCAN, REAR BUMPER REMOVED / STATE SCAN, REAR CRASH BEAM. No numbers. The rubric allows <= 2 items, but the user's v2 brief asked for the bumper-removed data to be labelled, so there are 3 (one at a time). |
| 8 | Ending | 4 | Parts land home at 34.35 s, then a 2 s fade to black starting 0.45 s later (ive director had flagged a 2.4 s dead hold), then a small logo from the 36.766 kick to the end of the audio. |
| 9 | Technical | 5 | Spec above. Frame-diff spikes at every cut (29-78 vs median 0.9), none at the fade->logo, which is a fade by design. No duplicate frames at cuts. |

## Remaining weak spots for the next agent
- The opener's first part transform only comes at 7.4 s. A part move inside 1.5 s would score a 5 hook.
- The ive director still flags f_reassemble's fade as "dead frames": the detector counts a fade as stillness.
- s3_wheel (b_headlight) is a 2.4 s v1 shot reused from 2.4 s; it is the only v1 render left apart from the s7 tail.
