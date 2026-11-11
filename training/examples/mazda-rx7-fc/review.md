# Mazda RX-7 FC3S scan reel v2 — self-review (training/rubric.md)

Output: `/home/user/media/work/rx7/out/mazda_rx7_fc_v2.mp4` — 1080x1920, 30 fps, 37.37 s (1121 frames). v1: review_v1.md.
v2 = the user's all-reels brief + addendum (relayed by the parent session): scene order from this car's scan features
(direction.md, scene-director agent), one section per sequence with each part coming off on its own (director.md),
bumper-removed data as the hero beat with short labels, no repeated views, whole car in the opener, fade + small logo.

Order: whole car (front-right 3/4, whole car with margins) -> nose -> hood opens (fitted hinge, captured angle) -> captured
open hood lifts off, camera over the engine bay -> front bumper off, tips to show its scanned inside -> radiator support +
crash beam -> wheel -> mirror/side -> rear bumper off, sinks away, push onto rear crash beam + mounts -> high front-left
reassembly, hood locks on the 32.28 hit, fade -> small ILLUMAESTHETIC logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car turning from frame 1; soft intro, first cut on the 4.54 hit. `ive director` calls 2 s of the slow turntable "dead" (it moves 18->~30 deg) - kept as the opener's hold over the intro. |
| 2 | Beat sync | 5 | Measured on the delivered file against the broadband kick (1 ms RMS half-rise): all 10 cuts within +-16 ms (< 1/2 frame), after music.start 0.023 (grid was 23 ms early) and 3 one-frame moves. |
| 3 | 1:1 match | n/a | Scan only. (Internal match: s6 -> s9 hood swap at frame 374 is invisible - no frame-diff jump.) |
| 4 | Scan quality | 4 | Rear plate flattened (was legible). Known holes kept off-centre/short: rear glass (not shown), tail-lamp lenses, hub specks (skipped), cowl specks. |
| 5 | Story | 5 | Front -> side -> rear, each section once; every opening/removal is a registered state scan of this car (Hood Up, Hood Off Bumper Off, Rear Bumper Removed, Front Face part); the hood that lifts off is the captured open panel. |
| 6 | Grade | 4 | Satin silver on black, -0.5 EV; pads/logo card matched to the render black (4,4,5). |
| 7 | Text | 4 | 7 labels, max 2 on screen, only over scan shots, in black outside the silhouette, plain names of what is visible (ENGINE BAY, FRONT/REAR BUMPER REMOVED, RADIATOR SUPPORT, CRASH BEAM, MOUNTING POINTS); no numbers. MOUNTING POINTS is up 0.9 s - short. |
| 8 | Ending | 5 | Reassembly locks on the hit, 0.57 s fade to black, small logo (378 px) on 33.40, music fades with it. |
| 9 | Technical | 5 | Specs met; every render folder luma-scanned (persistent data off; no dropouts); no unexpected jumps (frame diff). |

## Changes from v1 (each logged in editlog.jsonl)
- Dropped s2 (same view as s1), s7 (spinning top-down over the rear-glass hole), s8 (all parts at once in a wide orbit).
- New per-section shots s9-s13; front bumper flips only because its inside is scanned; hood and rear bumper translate.
- Opener reframed (window + scale 0.88 + pad) so the whole car sits with margins; logo card 82 % -> 35 % width.

## For the next agent
- Run `ive director` on the ASSEMBLED v2 too: my own late camera change (reassembly to front-right 3/4) repeated the
  opener's angle and only the report caught it.
- ScanHUD labels need a non-empty `sub` (" " works) or Remotion throws on interpolate([6, 6]).
- With persistent data off, frames take ~20 s instead of ~12 s; budget for it.
