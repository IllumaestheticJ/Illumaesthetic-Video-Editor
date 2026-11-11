# Subaru WRX VA scan reel v1 — self-review (training/rubric.md)

Output: `/home/user/media/subaru-wrx-va/out/subaru_wrx_va_scan_v1.mp4` (media not committed).
1080x1920, 30 fps, 923 frames (30.77 s), scan only (no IRL, no text), original generated track (132.4 BPM).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Turntable is moving from frame 1 with a 0.6 s fade up from black; the first change of view is the b8 cut at 3.67 s (a Temerario-style slow open, not a punchy hook). |
| 2 | Beat sync | 4 | All 9 cuts land on their planned frames (frame-diff of the output: 110, 219, 274, 328, 382, 464, 518, 627, 790). Each is the nearest frame to the fitted kick grid (`beats`, all within ½ frame). Measured against the decoded audio, broadband kick onsets sit −44..+28 ms from the cut. The b28 cut's onset reading was ambiguous (a pre-hit at 12.66 s). That is within ±1 frame for 7/9 cuts and slightly over for b58 (logo, −44 ms) and b34 (+28 ms). |
| 3 | 1:1 match | n/a | Scan-only reel by brief; no IRL→scan cut. |
| 4 | Scan quality | 4 | Ground removed (tools/clean.py), plate deplated (tools/deplate.py; checked in s02, s05, s07). Open hood/trunk are composites of the state scans (no hollow shells). Visible scan artefacts remain: ragged edges on the headlight lens (unscanned glass), on the grille mesh, and on the trunk-lid underside. The explode base shows the bumper-removed front structure as scanned (rough edges where the bumper meets). |
| 5 | Story | 4 | Turntables → close-ups (wheel, front, wing) → hood open → trunk open → top-down → explode (bumper, fog bezels, scoop, wing lift; bumper turns to show its inside; locks home on b54) → logo. Every exploded part is our own part / removed-state scan, registered in the car frame (regcheck medians 1.7–2.9 mm, red-over-silver renders in regcheck/). |
| 6 | Grade | n/a | No IRL footage. Silver-on-black house look via scan_render (AgX). |
| 7 | Text | 5 | No text (brief). |
| 8 | Ending | 4 | Logo card on the b58 kick (26.33 s), holds through the track's last hit (b64 29.07 s), fades out over the last 1.6 s with a 1.2 s audio fade; the music is at −31 dB by 29.5 s. |
| 9 | Technical | 4 | 1080x1920, 30 fps, crf 16. Renders are 15 fps minterpolated to 30. The explode first rendered with the lights dropping out from frame 43 (black silhouette 23.6–26.3 s). That was caught on the assembled contact sheet. Frames 43–82 were re-rendered, the lights dropped again at frame 61, and frames 61–82 were then rendered with `--no-persist`. All 82 frames are now lit (min luma 23); there is no brightness step at the joins (27.0/27.0 at 42/43, 26.0/26.0 at 60/61). Output: h264 yuv420p + AAC, 923 frames, cuts at the planned frames. Rendered shots play at ~1.38x (trunk 1.76x) because they were planned before the track arrived; motion stays smooth after interpolation. |

## What the next agent should take from this
- **Check brightness per frame of every long Cycles render.** With `use_persistent_data` the studio lights can silently drop mid-animation. Signs: render time per frame halves, frame mean luma drops (27 → 6), and the log has no error. A one-line PIL luma scan over the PNGs catches it before assembly. Re-rendering with persistence on dropped the lights again after 18 frames; `tools/shots.py --no-persist` fixed it (about 10 s/frame instead of 7).
- Plan shot lengths after the music arrives when possible; speeding renders 1.38x worked but wastes render time.
- Low-passed "kick" detectors read 40–70 ms late against the broadband onset; measure the cut against the broadband onset (half-rise of a 1 ms RMS envelope).
