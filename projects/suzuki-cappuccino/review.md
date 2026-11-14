# Self-review - Suzuki Cappuccino scan reel v1 (`/home/user/media/work/out/suzuki_cappuccino_v1.mp4`)

38.87 s, 1080x1920, 30 fps, 11 scan shots + logo, scan only / no text (Temerario format). Scored with `training/rubric.md`.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Car tracking from frame 0 (fades up over 1 s); the transformation itself (front opens) is held for the drop at 15.27 s, by the Temerario order the brief set |
| 2 | Beat sync | 5 | 126 BPM kick-anchored grid (2 ms median kick error). Frame-diff cut detection on the delivered file: every cut at round(beat*30), -14..+10 ms; vs. decoded-audio kicks -10..+12 ms |
| 3 | 1:1 match | n/a | No IRL footage in this format |
| 4 | Scan quality | 4 | Silver on black, no ground. Real-scan caveats visible: speckle on the lower rim / hub in the wheel close-up, holes in the bumper grille, open hood underside is the outer skin seen from below (hood inside never scanned). A sliver of the slid-off front bumper peeks in at the bottom edge for the first ~0.3 s of s09 |
| 5 | Story | 4 | Turntables -> wheel + lamp close-ups -> bumper off / hood up ON THE DROP -> trunk -> top-down -> explode -> float -> reassemble -> logo. Hood/trunk swing on hinges fitted to the captured open lids. Exploded parts read small at 9:16 (the lamps especially) |
| 6 | Grade | 5 | AgX, -0.5 EV silver (huracan-evo measured match to ref), consistent across shots (median car luma 135-192) |
| 7 | Text | 5 | None, per brief |
| 8 | Ending | 5 | s11 fades out, logo on beat 76 (36.224 s), the track's last two hits play under it, ends with the music at 38.87 s (music measured to end ~38.9 s; file is 40.05 s) |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, faststart. No black frames (41 black render frames caught by a per-frame luma scan and re-rendered); no cloned frame before cuts (worked around ive's cut compensation, see editlog). One near-duplicate at 15.30 s = eased camera start |

Next agent / reviewer: the weakest beat is s09-s10 (parts small in frame). If asked for "bigger", go closer on a 3/4 and stack fewer parts per shot.

---

# Self-review - v2 (`/home/user/media/work/out/suzuki_cappuccino_v2.mp4`)

User v2 brief (all V1 videos) + addendum A-D. 38.87 s, 7 scan shots + small logo, section labels. Plan: direction.md / director.md.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 5 | Whole car at ~90 % frame width, constant-speed orbit from frame 1 (no fade-in, no ease-in) |
| 2 | Beat sync | 5 | Cuts on broadband kick-onset frames (onsets.json). tools/cutcheck.py on the delivered file vs decoded audio: all 7 cuts +3.2..+11.1 ms after the kick onset (max 11.1 ms, target <=16.7) |
| 3 | 1:1 match | n/a | No IRL footage in this format |
| 4 | Scan quality | 4 | Removed-state scans shown as captured (radiator / engine bay / rear panel + exhaust). Real-scan holes in grille and under-bay; hood underside is the outer skin seen from below (hood inside never scanned) |
| 5 | Story | 4 | One continuous sequence per section, front -> side -> rear, no repeats: whole car -> lamps out, bumper tips to its inner face, hold on what is behind -> hood opens ON THE DROP into the bay -> wheel -> rear bumper tips, hold on rear end/exhaust -> trunk opens -> progressive explode (rear then front) -> reassembly -> fade -> small logo. Hood/trunk opens swing the lid on hinges fitted to the captured Hood Open / Trunk Open scans (judgement call vs addendum D, flagged to the user) |
| 6 | Grade | 5 | Same AgX -0.5 EV house silver as v1 |
| 7 | Text | 4 | 5 factual labels, never >1 on screen, no numbers, over scan only. ENGINE BAY sits at y 0.78 (inside the bottom-20 % band; the only black space in that shot) |
| 8 | Ending | 5 | Explode -> reassemble -> clean car swaps in on beat 74 -> 0.5 s fade -> logo (width 380) on beat 76, music tail under it |
| 9 | Technical | 4 | 1080x1920 30 fps yuv420p AAC faststart; persistent data off + per-frame luma scan: 0 dark render frames. Two 1-frame holds remain (frames 572, 886: last frame of s3/s5, the 15 fps render was one source frame short after minterpolate and was padded by clone); black frames only in the intended pre-logo fade (1084-1086) |

Weak spots for the next agent: s2 / s5 structure holds leave the lower ~35 % of frame black (labels placed there); x2 lids brush the right edge for ~2 frames while closing.

`ive director`: sections whole 3.9 s / front 15.3 / side 1.9 / rear 8.6 / finale 6.7 s, no flags. Its two repeat hits are the x1->x2 continuous finale move (cut on beat 68) and the s1/x2 whole-car bookend (opposite sides) - both intentional, see editlog.

## v3 self-review (reviewer feedback: bigger logo; bumper / trunk cut lines wrong)

Changes: logo card 380 -> 720 px wide; hood, trunk lid and both bumper seams re-cut with
`tools/panels.py` on the scan's real shut lines (least-cost traces through the panel-gap grooves;
bumper seams from the bumper-off state scans); the five exploded-view shots re-rendered.

| Criterion | Score | Notes |
|---|---|---|
| Hook | 5 | unchanged opener, moving from frame 1 |
| Beat sync | 5 | all 7 cuts within 11.1 ms of the decoded kicks (cutcheck) |
| Scan fidelity | 5 | panels now separate on their real seams; lamps stay on the body as in the state scans |
| Story | 4 | front -> side -> rear -> explode -> reassemble, unchanged |
| Grade | 5 | luma scan clean, no flicker (max jump inside a shot 9.3, all camera moves) |
| Text | 4 | 5 labels, all in black space, no numbers |
| Ending | 5 | logo 720 px, readable on a phone |
| Technical | 4 | s3/s5/x1 ease to a 1-3 frame rest before their cut (render tail margin); black frames 1084-1086 are the intended fade to logo |

Known limits: hood/trunk swings in the explode are hinge animations of the closed panels (open-state
scans are used for the hero beats); the pre-cut rest frames would need the keyframes un-rescaled and a re-render.

## v4 self-review (reviewer: re-edit to the supplied track; corner markers must not come out before the bumper; nest everything)

Changes: music replaced with the reviewer-supplied track (first 40.4 s, start 0.6105 s); all 7 cuts re-placed on individually
measured low-band hits (no grid: the track is live-feel, a fitted grid missed 149/250 beats by > 40 ms); corner markers are now
children of the front bumper (`tools/shot.py` `parents`) - bumper comes off with them in it, they lift out of the tipped bumper,
and on reassembly go back in before the bumper returns; s2/s3/s5/x1/x2 re-rendered to the new lengths; labels re-timed.

| Criterion | Score | Notes |
|---|---|---|
| Hook | 5 | opener moving from frame 1, first hit of the track on frame 3 |
| Beat sync | 5 | 7 cuts within 7.7 ms of the decoded hits (cutcheck); hood swing and clean-car swap also on hits |
| Scan fidelity | 5 | v3 seams kept; removal order now matches the real car (bumper, then markers) |
| Story | 4 | front -> side -> rear -> explode -> reassemble; wheel shot is only 1.3 s |
| Grade | 5 | unchanged look |
| Text | 4 | same 5 labels, re-timed, all in black space (engine-bay label lowered to y 0.84) |
| Ending | 5 | 720 px logo, music fades under it |
| Technical | 5 | no held frames before cuts any more (last key at render end); black frames 1129-1131 are the fade to logo |

Known limits: hood/trunk swings in the explode are hinge animations of the closed panels; the wheel shot is the v1 render trimmed.

## v5 self-review (reviewer: hood cut a little funny when the front bumper comes off; corner markers come out from the front)

Changes: hood nose edge between the lamps re-cut to a smooth arc (panels.py NOSE_EDGE); corner markers now leave through the
bumper's outer face after it is off (bumper off -> inner face -> rights itself -> markers push out forward); bumper parks
and layers upright so the markers stay in front of it; new label FRONT BUMPER LIGHTS / CORNER MARKERS; s2/s3/x1/x2 re-rendered.

| Criterion | Score | Notes |
|---|---|---|
| Hook | 5 | unchanged |
| Beat sync | 5 | 7 cuts within 7.7 ms of the decoded hits |
| Scan fidelity | 5 | smooth hood nose; marker removal direction matches the car |
| Story | 5 | every front part now has its own beat and name |
| Grade | 5 | unchanged |
| Text | 4 | 6 labels, all in black space; sub "CORNER MARKERS" is the reviewer's term, not a file name |
| Ending | 5 | unchanged |
| Technical | 5 | no clipping of removed parts; near-identical frames 305/353 are deliberate rests inside the marker beat |

Known limits: hood/trunk swings in the explode are hinge animations of the closed panels; s5 reused from v4.

## v6 self-review (reviewer: wheel cut at 0:20 unnecessary; open the hood first, then the bumper; hood still cut too far for the split)

Changes: wheel shot dropped (its time goes to the radiator -> engine-bay shot, no music splice); hood swings open first, then
the bumper comes off (inner face, rights itself, markers out through its front); hood re-cut on the real hood/bumper seam
(front-view groove at z 469 mm, lamp corner to lamp corner through the middle of the mouth) and the body rebuilt to match.

| Criterion | Score | Notes |
|---|---|---|
| Hook | 5 | unchanged |
| Beat sync | 5 | 6 cuts within 7.6 ms; hood swing lands on the 6.46 s hit, crane on 16.28 s |
| Scan fidelity | 5 | assembled hood + bumper + body render matches the full-car scan at the nose |
| Story | 5 | technician order: hood, bumper, markers, exposed structure, engine bay; no filler shot |
| Grade | 5 | unchanged |
| Text | 4 | 6 labels in black space |
| Ending | 5 | unchanged |
| Technical | 5 | hood stays in frame through its swing; s5 reused from v4 |
