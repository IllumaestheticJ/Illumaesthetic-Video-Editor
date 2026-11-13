# Review - GT3 vs GT3 RS (992) split-screen, v4 (60 fps)

Output: /home/user/media/work/gt3vs/out/gt3_vs_gt3rs_v4_60fps.mp4 (1080x1920, 60 fps, 37.8 s). Previous: review_v3.md.

## What changed (user feedback on v3)
1. Tail sweeps re-rendered natively at 60 fps (g_orbit, r_orbit: 120 frames each) - no interpolation smear there.
2. GT3 rear section: after the rear parts are off the diffuser slides aside and the camera drops under the tail and looks
   up at the exhaust / engine underside (label "EXHAUST - UNDERSIDE"), held ~2.5 beats.
3. Opening plays 2x: whole-car shot 4 beats (was 8), front section 6 beats (was 12); music start +4.700 s so all later
   cuts keep their musical position. Reel is 4.7 s shorter.

## Self-score (training/rubric.md, 1-5)
- Story / pacing: 4 - first part reveal now at ~2.1 s instead of 4.3 s.
- Match / transition: 4 - unchanged listing landing (IoU 0.977 / 0.962), now crisp at 60 fps.
- Scan look: 4 - the underside exhaust view is the cleanest GT3 strip-down frame; bumper-off structure from behind is still fragmented.
- Sync: 3 - retimed opening cuts sit on beats 4 and 10 of the new start by arithmetic; not re-measured against the kick band.
- Text: 4.

## Known limits / open
- Everything except the two sweeps and the website end card is still 15 fps Blender output motion-interpolated to 60.
- In g_rear the diffuser ends 2 m to the side; g_side / g_wide (not re-rendered) still show it at its old rest offset.
- No dedicated GT3 rear bumper-off capture found (see review_v3.md).
- Only the 60 fps file was assembled for v4 (split.json holds the 30 fps timeline).
