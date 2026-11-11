# Mazda Miata NC scan reel v2 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/mazda_miata_nc_v2.mp4` — 1080×1920, 30 fps, yuv420p, AAC, faststart, 37.97 s (1139 frames).
Rebuilt from user feedback ("rotations wasted; focus on the front bumper, THEN the rear"; "label the scans") and the parent v2 brief + addendum. Plan: `direction.md`.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | whole car with margins, push-in moving from frame 1; first transformation (bumper off) at 7.4 s — after the wheel + lamp details |
| 2 | Beat sync | 5 | 10 cuts measured on decoded audio (kickcheck, 40–120 Hz): 8 within ±0.4 frame; 142 (+0.55) and 840 (−0.52) are kicks falling between two frames. No cuts in the kick-less breakdown; hood lifts off on the drop (18.70 s) |
| 3 | 1:1 match | n/a | scan-only brief |
| 4 | Scan quality | 4 | rear plate flattened (deplate) before rear/end renders; wheel close-up still shows scan holes in the spokes; engine bay has scan gaps (true data, not hidden) |
| 5 | Story | 4 | whole → wheel → lamp → bumper off → what was under it (hero, labelled) → hood opens → hood off on drop → trunk opens → top view, panels home → clean car fades → logo. Front → rear, no ping-pong, no turntables. Director still flags lamp~b2~b3a as one front view (different scan states, kept deliberately) |
| 6 | Grade | 5 | house satin silver on black; every frame luma-scanned, no dark frames |
| 7 | Text | 4 | six labels, factual only (what was scanned / which states exist), no numbers; dark halo added for legibility over silver. Rubric says ≤2 items — the user explicitly asked for scan labels, so six short ones, never two at once |
| 8 | Ending | 5 | clean car fades out over 12 frames, then a small (460 px) logo to the end of the music; the last scene isn't held |
| 9 | Technical | 5 | spec correct; frames ±1 around each cut checked; the only black stretch is the logo card |

## What changed from v1
- All turntables/orbits removed; one sequence per section, front → rear; camera moves in on each part as it comes off.
- Bumper-removed state is the hero: 5.2 s push-in on what the bumper covered, labelled.
- Trunk lid only opens (no removed-lid scan exists); v1 lift-off dropped.
- Labels describe scans; ending fade + small logo.

## Process issues worth remembering
- A 7-shot final queue at 12 spp took > 2 h; the background job was killed at the limit. shot.py is resumable, so re-queueing the remaining shots lost nothing — split long queues into ≤ 2 h chunks.
- Silver scans are bright: any label not over black needs `shadow: true` (check full-res crops, not thumbnails).
- Director "repeated view" flags compare silhouettes, so successive states of one section register as repeats; justify or cut each.

## Open questions for the reviewer
- Drive calls the headlight scan "Left Bucket" but the close-up shows the car's right lamp.
- No hood-underside or lid-removed scans, so neither is shown.

---

# Mazda Miata NC scan reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/mazda_miata_nc_v1.mp4` — 1080×1920, 30 fps, yuv420p, AAC, 37.97 s (1139 frames).
Temerario-style, scan only (no IRL, no text). Music: original track supplied by the parent session (103.0 BPM kick grid).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | opens on a slow front 3/4 turntable — moving, but nothing transforms until the hood opens at 11.1 s |
| 2 | Beat sync | 5 | all 9 cuts on the fitted kick grid (frames round(t·30), ≤½ frame); explode starts on the drop (18.70 s), panels lock on beat 30.34 |
| 3 | 1:1 match | n/a | scan-only brief, no IRL→scan cut |
| 4 | Scan quality | 4 | levelled + registered state scans (overlays checked); hood cut from seam map, lid from absent-mask with fitted hinge (median 1.0 mm); small dark cowl patch in the explode base, lid rear-face blocks move with the lid; 4 mm decimation is softer than Temerario in the wheel close-up (scan holes visible on the tyre bead) |
| 5 | Story | 4 | turntables → close-ups (wheel, lamp) → hood opens → trunk opens → top-down → exploded view (bumper, hood, trunk lid: all the part/state scans support) → hero → logo |
| 6 | Grade | 4 | house satin silver on black throughout; no IRL footage |
| 7 | Text | 5 | none (brief) |
| 8 | Ending | 5 | logo card over the last 6 beats + tail, ends with the music (last audio ≈37.9 s), 0.5 s audio fade |
| 9 | Technical | 5 | spec correct; blackdetect clean; frames ±1 around each cut checked, no dup/black frames |

## Process issues worth remembering
- s8 first two final renders had unlit frames (pure black car on the world bg, 69–125 frames) while single-frame
  test renders were fine. Cause: `render.use_persistent_data = True` in animation renders lost every light partway
  through. Fixed by turning it off in tools/shot.py and re-rendering only the dark frames. My first diagnosis
  (camera behind the area light) was wrong — a single-frame test can't reproduce it. **Brightness-scan every
  rendered sequence before assembling.**

## Known issues / v2 ideas
- Exploded view is wide (car ≈60 % width) because the parts stack above the car in 9:16; a second tighter pass on the bumper flip would read better on phones.
- Only three panels separate — doors/fenders have no removed-state scans.
- Stronger hook: open on the hood already moving or a fast push into the headlight.
